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

load_dotenv(PROJECT_ROOT / ".env")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================================
# FLASK APP
# ============================================================================

app = Flask(__name__)

# Allow the Vercel frontend to communicate with this backend.
#
# For initial deployment, this allows all origins.
# After your Vercel URL is known, restrict this to your frontend domain.
CORS(app)


# ============================================================================
# HELPERS
# ============================================================================

def _file_response(path: Path):
    """
    Return a generated file or a useful JSON 404 response.
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
    Convert the formatter pipeline result into a JSON-safe dictionary.

    Supports:
    - PipelineResult objects
    - pathlib.Path
    - dictionaries
    """

    if isinstance(result, dict):
        return {
            key: str(value) if isinstance(value, Path) else value
            for key, value in result.items()
        }

    # PipelineResult object
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

    # If the pipeline returns a Path directly
    if isinstance(result, Path):
        result_data["output_file"] = str(result)

    # Fallback
    if not result_data:
        result_data["result"] = str(result)

    return result_data


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health")
def health():
    """
    Health check endpoint.

    Used by Render to verify that the backend is running.
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

    Expected request from the Vercel frontend:

        Content-Type: application/json

        {
            "paper_content": "..."
        }

    The formatter pipeline receives the extracted paper text.
    """

    try:
        paper_content = ""

        # ------------------------------------------------------------------
        # JSON request
        # ------------------------------------------------------------------

        if request.is_json:
            data = request.get_json(silent=True) or {}

            paper_content = str(
                data.get("paper_content", "")
            ).strip()

        # ------------------------------------------------------------------
        # Multipart request
        # ------------------------------------------------------------------

        elif "file" in request.files:
            uploaded = request.files["file"]

            if not uploaded.filename:
                return jsonify({
                    "status": "error",
                    "message": "No file selected.",
                }), 400

            # --------------------------------------------------------------
            # PDF
            # --------------------------------------------------------------

            if uploaded.mimetype == "application/pdf":
                return jsonify({
                    "status": "error",
                    "message": (
                        "Direct PDF upload is not supported by this endpoint. "
                        "Extract the PDF text in the frontend and send it "
                        "using the 'paper_content' JSON field."
                    ),
                }), 415

            # --------------------------------------------------------------
            # Text / Markdown / plain files
            # --------------------------------------------------------------

            raw = uploaded.read()

            paper_content = raw.decode(
                "utf-8",
                errors="replace",
            ).strip()

        # ------------------------------------------------------------------
        # Unsupported request
        # ------------------------------------------------------------------

        else:
            return jsonify({
                "status": "error",
                "message": (
                    "Send JSON containing a non-empty "
                    "'paper_content' field."
                ),
            }), 400

        # ------------------------------------------------------------------
        # Validate content
        # ------------------------------------------------------------------

        if not paper_content:
            return jsonify({
                "status": "error",
                "message": (
                    "paper_content is required and "
                    "cannot be empty."
                ),
            }), 400

        # ------------------------------------------------------------------
        # Log request
        # ------------------------------------------------------------------

        print("\n" + "=" * 60)
        print("FORMATTER PIPELINE")
        print("=" * 60)
        print(f"Characters: {len(paper_content):,}")
        print(f"Output directory: {OUTPUT_DIR}")
        print("=" * 60)

        # ------------------------------------------------------------------
        # Run CrewAI / LiteLLM / Groq pipeline
        # ------------------------------------------------------------------

        result = run_formatter_pipeline(
            paper_content=paper_content,
            output_dir=OUTPUT_DIR,
        )

        result_data = _pipeline_result_to_dict(result)

        print("=" * 60)
        print("PIPELINE COMPLETE")
        print("=" * 60)

        # ------------------------------------------------------------------
        # Build API response
        # ------------------------------------------------------------------

        base_url = request.host_url.rstrip("/")

        response_data = {
            "status": "success",

            "pdf_url": f"{base_url}/download/pdf",

            "latex_url": f"{base_url}/download/tex",

            "manuscript_url": (
                f"{base_url}/download/manuscript"
            ),

            "bib_url": f"{base_url}/download/bib",
        }

        response_data.update(result_data)

        return jsonify(response_data), 200

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
    Download generated manuscript.
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
        "message": "Uploaded request is too large.",
    }), 413


# ============================================================================
# LOCAL DEVELOPMENT
# ============================================================================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5002)
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
    )