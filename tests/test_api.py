from pathlib import Path

import research_paper_ai.api.app as app_module


def test_health():
    client = app_module.app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_format_requires_content():
    client = app_module.app.test_client()
    response = client.post(
        "/format-paper",
        json={"paper_content": ""},
    )
    assert response.status_code == 400


def test_format_returns_download_urls(monkeypatch, tmp_path):
    class Result:
        manuscript_file = str(tmp_path / "manuscript.md")
        bibtex_file = str(tmp_path / "references.bib")
        latex_file = str(tmp_path / "main.tex")
        pdf_file = str(tmp_path / "main.pdf")

    monkeypatch.setattr(
        app_module,
        "OUTPUT_DIR",
        tmp_path,
    )
    monkeypatch.setattr(
        app_module,
        "run_formatter_pipeline",
        lambda paper_content, output_dir: Result(),
    )

    client = app_module.app.test_client()
    response = client.post(
        "/format-paper",
        json={"paper_content": "sample paper"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["pdf_url"].endswith("/download/pdf")
