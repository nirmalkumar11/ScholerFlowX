import shutil
from pathlib import Path

import pytest

from research_paper_ai.services.pdf_compiler import PDFCompiler


@pytest.mark.skipif(
    shutil.which("pdflatex") is None,
    reason="pdflatex is not installed",
)
def test_pdf_compiler_creates_pdf(tmp_path: Path):
    (tmp_path / "main.tex").write_text(
        r"""\documentclass{article}
\begin{document}
Hello World
\end{document}
""",
        encoding="utf-8",
    )

    pdf = Path(PDFCompiler.compile(tmp_path))

    assert pdf.is_file()
    assert pdf.stat().st_size > 0
