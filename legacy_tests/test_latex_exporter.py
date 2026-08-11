from research_paper_ai.services.latex_exporter import (
    LatexExporter
)

latex_content = r"""
\documentclass{article}
\begin{document}
Hello World
\end{document}
"""

bibtex_content = """
@article{paper1,
  title={Example}
}
"""

files = (
    LatexExporter.export(
        latex_content=latex_content,
        bibtex_content=bibtex_content,
        output_dir=
        "workspace/outputs"
    )
)

print(
    "\n===== FILES =====\n"
)

print(files)

print(
    "\nLATEX EXPORT TEST PASSED"
)