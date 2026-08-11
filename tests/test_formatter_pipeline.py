from pathlib import Path

import research_paper_ai.pipeline.formatter_pipeline as pipeline


def test_pipeline_wires_services(monkeypatch, tmp_path):
    class FakeFormatter:
        @staticmethod
        def format(content):
            assert content == "input paper"
            return "# Title\n\nFormatted paper"

    class FakeComposer:
        @staticmethod
        def compose(markdown):
            class Doc:
                content = r"\documentclass{article}\begin{document}OK\end{document}"
            return Doc()

    class FakeExporter:
        @staticmethod
        def export(latex_content, bibtex_content, output_dir):
            output = Path(output_dir)
            tex = output / "main.tex"
            bib = output / "references.bib"
            tex.write_text(latex_content)
            bib.write_text(bibtex_content)
            return {"tex_file": str(tex), "bib_file": str(bib)}

    class FakeCompiler:
        @staticmethod
        def compile(output_dir):
            pdf = Path(output_dir) / "main.pdf"
            pdf.write_bytes(b"%PDF-1.4")
            return str(pdf)

    monkeypatch.setattr(pipeline, "PaperFormatter", FakeFormatter)
    monkeypatch.setattr(pipeline, "LatexComposer", FakeComposer)
    monkeypatch.setattr(pipeline, "LatexExporter", FakeExporter)
    monkeypatch.setattr(pipeline, "PDFCompiler", FakeCompiler)

    result = pipeline.run_formatter_pipeline("input paper", tmp_path)

    assert Path(result.manuscript_file).is_file()
    assert Path(result.latex_file).is_file()
    assert Path(result.bibtex_file).is_file()
    assert Path(result.pdf_file).is_file()
