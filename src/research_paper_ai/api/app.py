from __future__ import annotations
import os
from pathlib import Path
from urllib.parse import quote

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS

from research_paper_ai.pipeline.formatter_pipeline import run_formatter_pipeline


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = PROJECT_ROOT / "workspace" / "output"
FRONTEND_DIR = PROJECT_ROOT / "frontend_dist"

load_dotenv(PROJECT_ROOT / ".env")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__, static_folder=None)
CORS(app)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _file_response(path: Path):
    """Return a generated file or a useful JSON 404."""
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
    """Convert PipelineResult/path/dict results into a JSON-safe payload."""
    if isinstance(result, dict):
        return result

    return {
        "manuscript_file": str(result.manuscript_file),
        "bibtex_file": str(result.bibtex_file),
        "latex_file": str(result.latex_file),
        "pdf_file": str(result.pdf_file),
    }


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------

@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "Research Paper Formatter",
    })


@app.post("/format-paper")
def format_paper():
    """
    Format a manuscript.

    Supported request formats:

    1. JSON:
       {"paper_content": "..."}

    2. multipart/form-data:
       file=<text/markdown/pdf file>

    The current web UI extracts PDF text in the browser and uses the JSON form.
    """
    try:
        paper_content = ""

        # JSON request from the React frontend.
        if request.is_json:
            data = request.get_json(silent=True) or {}
            paper_content = str(data.get("paper_content", "")).strip()

        # Also support direct multipart uploads for API clients.
        elif "file" in request.files:
            uploaded = request.files["file"]

            if not uploaded.filename:
                return jsonify({
                    "status": "error",
                    "message": "No file selected.",
                }), 400

            raw = uploaded.read()

            # The frontend currently extracts PDF text before calling this
            # endpoint. Direct PDF uploads therefore require a PDF extractor,
            # which is intentionally not hidden behind a misleading fallback.
            if uploaded.mimetype == "application/pdf":
                return jsonify({
                    "status": "error",
                    "message": (
                        "PDF uploads are not accepted directly by this API. "
                        "Extract the PDF text in the frontend and send it as "
                        "JSON field 'paper_content'."
                    ),
                }), 415

            paper_content = raw.decode("utf-8", errors="replace").strip()

        else:
            return jsonify({
                "status": "error",
                "message": (
                    "Send JSON with a non-empty 'paper_content' field."
                ),
            }), 400

        if not paper_content:
            return jsonify({
                "status": "error",
                "message": "paper_content is required and cannot be empty.",
            }), 400

        print("\n===== FORMATTER PIPELINE =====")
        print(f"Characters: {len(paper_content):,}")

        result = run_formatter_pipeline(
            paper_content=paper_content,
            output_dir=OUTPUT_DIR,
        )

        result_data = _pipeline_result_to_dict(result)

        print("===== PIPELINE COMPLETE =====")

        return jsonify({
            "status": "success",
            "pdf_url": f"{request.host_url.rstrip('/')}/download/pdf",
            "latex_url": f"{request.host_url.rstrip('/')}/download/tex",
            "manuscript_url": (
                f"{request.host_url.rstrip('/')}/download/manuscript"
            ),
            **result_data,
        })

    except Exception as exc:
        app.logger.exception("Formatter pipeline failed")
        return jsonify({
            "status": "error",
            "message": str(exc),
        }), 500


@app.get("/download/pdf")
def download_pdf():
    return _file_response(OUTPUT_DIR / "main.pdf")


@app.get("/download/tex")
def download_tex():
    return _file_response(OUTPUT_DIR / "main.tex")


@app.get("/download/manuscript")
def download_manuscript():
    return _file_response(OUTPUT_DIR / "manuscript.md")


@app.get("/download/bib")
def download_bib():
    return _file_response(OUTPUT_DIR / "references.bib")


# ---------------------------------------------------------------------------
# Frontend
# ---------------------------------------------------------------------------

@app.get("/")
def home():
    index_file = FRONTEND_DIR / "index.html"

    if index_file.is_file():
        return send_from_directory(FRONTEND_DIR, "index.html")

    return jsonify({
        "service": "Research Paper Formatter",
        "status": "running",
        "message": (
            "Frontend build not found. Run `cd frontend && npm install && "
            "`npm run build`."
        ),
    })


@app.get("/<path:path>")
def frontend_assets(path):
    """Serve Vite assets and fall back to index.html for SPA routes."""
    if path.startswith(("format-paper", "download/", "health")):
        return jsonify({"status": "not found"}), 404

    asset_path = FRONTEND_DIR / path

    if asset_path.is_file():
        return send_from_directory(FRONTEND_DIR, path)

    index_file = FRONTEND_DIR / "index.html"

    if index_file.is_file():
        return send_from_directory(FRONTEND_DIR, "index.html")

    return jsonify({
        "status": "error",
        "message": "Frontend build not found.",
    }), 404


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5002)),
        debug=False,
    )
