from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

from research_paper_ai.pipeline.formatter_pipeline import (
    run_formatter_pipeline,
)



# ============================================================================
# PATHS
# ============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

OUTPUT_DIR = PROJECT_ROOT / "workspace" / "output"

# Load local .env when running locally.
# Render uses its Environment Variables instead.
load_dotenv(PROJECT_ROOT / ".env")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================================
# ENVIRONMENT
# ============================================================================

PORT = int(os.environ.get("PORT", 5002))

# Your Vercel frontend URL.
#
# Local:
#   FRONTEND_URL=http://localhost:5173
#
# Production:
#   FRONTEND_URL=https://your-vercel-app.vercel.app
#
FRONTEND_URL = os.environ.get("FRONTEND_URL", "").strip()


# ============================================================================
# FLASK APP
# ============================================================================

app = Flask(__name__)


# ============================================================================
# CORS
# ============================================================================

FRONTEND_URL = os.environ.get(
    "FRONTEND_URL",
    "*"
).strip()

CORS(
    app,
    origins=FRONTEND_URL,
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

if FRONTEND_URL:
    # Production / configured frontend
    CORS(
        app,
        origins=[
            FRONTEND_URL,
        ],
        methods=[
            "GET",
            "POST",
            "OPTIONS",
        ],
        allow_headers=[
            "Content-Type",
            "Authorization",
        ],
    )
else:
    # Local development fallback.
    #
    # This allows:
    # http://localhost:5173
    # http://127.0.0.1:5173
    #
    CORS(
        app,
        origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        methods=[
            "GET",
            "POST",
            "OPTIONS",
        ],
        allow_headers=[
            "Content-Type",
            "Authorization",
        ],
    )


# ============================================================================
# HELPERS
# ============================================================================


def _file_response(path: Path):
    """
    Return a generated file or a JSON 404 response.
    """

    path = path.resolve()

    if not path.is_file():
        return jsonify({
            "status": "error",
            "message": f"Generated file not found: {path.name}",
        }), 404

    return send_file(
        path,
        as_attachment=True,
        download_name=path.name,
    )


def _pipeline_result_to_dict(result):
    """
    Convert formatter pipeline result into a JSON-safe dictionary.

    Supports:
        - dict
        - PipelineResult-like objects
        - pathlib.Path
    """

    # ------------------------------------------------------------------------
    # Dictionary result
    # ------------------------------------------------------------------------

    if isinstance(result, dict):
        result_data = {}

        for key, value in result.items():

            if isinstance(value, Path):
                result_data[key] = str(value)
            else:
                result_data[key] = value

        return result_data

    # ------------------------------------------------------------------------
    # PipelineResult-like object
    # ------------------------------------------------------------------------

    result_data = {}

    for attribute in (
        "manuscript_file",
        "bibtex_file",
        "latex_file",
        "pdf_file",
    ):
        if hasattr(result, attribute):

            value = getattr(result, attribute)

            if value is not None:
                result_data[attribute] = str(value)

    # ------------------------------------------------------------------------
    # Path result
    # ------------------------------------------------------------------------

    if isinstance(result, Path):
        result_data["output_file"] = str(result)

    # ------------------------------------------------------------------------
    # Fallback
    # ------------------------------------------------------------------------

    if not result_data:
        result_data["result"] = str(result)

    return result_data


def _public_result_urls(base_url: str):
    """
    Generate public download URLs.

    Files remain stored on the backend filesystem.
    """

    return {
        "pdf_url": f"{base_url}/download/pdf",
        "latex_url": f"{base_url}/download/tex",
        "manuscript_url": f"{base_url}/download/manuscript",
        "bib_url": f"{base_url}/download/bib",
    }


# ============================================================================
# HEALTH CHECK
# ============================================================================


@app.get("/health")
def health():
    """
    Health check endpoint.

    Used by:
        - Render
        - monitoring
        - local development
    """

    return jsonify({
        "status": "ok",
        "service": "Research Paper Formatter",
    })


# ============================================================================
# FORMAT PAPER
# ============================================================================


@app.post("/format-paper")
def format_paper():
    """
    Format a research paper.

    Primary frontend request:

        POST /format-paper

        Content-Type: application/json

        {
            "paper_content": "..."
        }

    The frontend is expected to extract text from the uploaded PDF
    and send that text to this API.

    Also supports text / Markdown multipart uploads.

    Direct PDF multipart uploads are intentionally rejected.
    """

    try:

        paper_content = ""

        # ====================================================================
        # JSON REQUEST
        # ====================================================================

        if request.is_json:

            data = request.get_json(
                silent=True
            ) or {}

            paper_content = str(
                data.get("paper_content", "")
            ).strip()

        # ====================================================================
        # MULTIPART REQUEST
        # ====================================================================

        elif "file" in request.files:

            uploaded = request.files["file"]

            # ----------------------------------------------------------------
            # Validate filename
            # ----------------------------------------------------------------

            if not uploaded.filename:

                return jsonify({
                    "status": "error",
                    "message": "No file selected.",
                }), 400

            # ----------------------------------------------------------------
            # Reject direct PDF uploads
            # ----------------------------------------------------------------

            if uploaded.mimetype == "application/pdf":

                return jsonify({
                    "status": "error",
                    "message": (
                        "Direct PDF upload is not supported by this API. "
                        "Extract the PDF text in the frontend and send it "
                        "as JSON using the 'paper_content' field."
                    ),
                }), 415

            # ----------------------------------------------------------------
            # Read text / Markdown
            # ----------------------------------------------------------------

            raw = uploaded.read()

            paper_content = raw.decode(
                "utf-8",
                errors="replace",
            ).strip()

        # ====================================================================
        # INVALID REQUEST
        # ====================================================================

        else:

            return jsonify({
                "status": "error",
                "message": (
                    "Invalid request. Send JSON containing "
                    "'paper_content'."
                ),
            }), 400

        # ====================================================================
        # VALIDATE PAPER CONTENT
        # ====================================================================

        if not paper_content:

            return jsonify({
                "status": "error",
                "message": (
                    "paper_content is required "
                    "and cannot be empty."
                ),
            }), 400

        # ====================================================================
        # LOG REQUEST
        # ====================================================================

        print()
        print("=" * 70)
        print("RESEARCH PAPER FORMATTER")
        print("=" * 70)

        print(
            f"Paper characters: {len(paper_content):,}"
        )

        print(
            f"Output directory: {OUTPUT_DIR}"
        )

        print("=" * 70)

        # ====================================================================
        # RUN FORMATTER PIPELINE
        # ====================================================================

        result = run_formatter_pipeline(
            paper_content=paper_content,
            output_dir=OUTPUT_DIR,
        )

        # ====================================================================
        # CONVERT RESULT
        # ====================================================================

        result_data = _pipeline_result_to_dict(
            result
        )

        # ====================================================================
        # BUILD PUBLIC RESPONSE
        # ====================================================================

        base_url = os.environ.get(
            "PUBLIC_API_URL",
            "https://scholerflowxx.onrender.com",
        ).rstrip("/")

     
        response_data = {
            "status": "success",
            "pdf_url": f"{base_url}/download/pdf",
            "latex_url": f"{base_url}/download/tex",
            "manuscript_url": f"{base_url}/download/manuscript",
            "bib_url": f"{base_url}/download/bib",
        }
        # Add pipeline metadata.
        #
        # We intentionally keep the internal filesystem paths out of the
        # primary response if possible.
        #
        # The frontend should use the *_url fields.
        for key, value in result_data.items():

            if key.endswith("_file"):

                # Convert filesystem fields to public URLs instead
                continue

            if key == "output_file":
                continue

            response_data[key] = value

        # ====================================================================
        # PIPELINE COMPLETE
        # ====================================================================

        print()
        print("=" * 70)
        print("PIPELINE COMPLETE")
        print("=" * 70)

        return jsonify(
            response_data
        ), 200

    except Exception as exc:

        app.logger.exception(
            "Formatter pipeline failed"
        )

        return jsonify({
            "status": "error",
            "message": str(exc),
        }), 500


# ============================================================================
# DOWNLOAD ENDPOINTS
# ============================================================================


@app.get("/download/pdf")
def download_pdf():
    """
    Download generated PDF.
    """

    return _file_response(
        OUTPUT_DIR / "main.pdf"
    )


@app.get("/download/tex")
def download_tex():
    """
    Download generated LaTeX file.
    """

    return _file_response(
        OUTPUT_DIR / "main.tex"
    )


@app.get("/download/manuscript")
def download_manuscript():
    """
    Download generated Markdown manuscript.
    """

    return _file_response(
        OUTPUT_DIR / "manuscript.md"
    )


@app.get("/download/bib")
def download_bib():
    """
    Download generated BibTeX references.
    """

    return _file_response(
        OUTPUT_DIR / "references.bib"
    )


# ============================================================================
# ERROR HANDLERS
# ============================================================================


@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "status": "error",
        "message": "Endpoint not found.",
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):

    return jsonify({
        "status": "error",
        "message": "HTTP method not allowed.",
    }), 405


@app.errorhandler(413)
def request_too_large(error):

    return jsonify({
        "status": "error",
        "message": "Request is too large.",
    }), 413


# ============================================================================
# LOCAL DEVELOPMENT
# ============================================================================


if __name__ == "__main__":

    print()
    print("=" * 70)
    print("Research Paper Formatter API")
    print("=" * 70)

    print(
        f"Port: {PORT}"
    )

    if FRONTEND_URL:
        print(
            f"CORS frontend: {FRONTEND_URL}"
        )
    else:
        print(
            "CORS: localhost frontend"
        )

    print(
        f"Output directory: {OUTPUT_DIR}"
    )

    print("=" * 70)
    print()

    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=False,
    )