from pathlib import Path

from research_paper_ai.services.latex_exporter import LatexExporter


def test_export_writes_tex_and_bib(tmp_path: Path):
    result = LatexExporter.export(
        latex_content=r"\documentclass{article}\begin{document}OK\end{document}",
        bibtex_content="@article{paper1,title={Example}}",
        output_dir=tmp_path,
    )

    tex = Path(result["tex_file"])
    bib = Path(result["bib_file"])

    assert tex.is_file()
    assert bib.is_file()
    assert "documentclass" in tex.read_text()
    assert "@article" in bib.read_text()
