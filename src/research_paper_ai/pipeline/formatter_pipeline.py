from __future__ import annotations

from pathlib import Path

from research_paper_ai.models.pipeline_result import PipelineResult
from research_paper_ai.services.latex_composer import LatexComposer
from research_paper_ai.services.latex_exporter import LatexExporter
from research_paper_ai.services.paper_formatter import PaperFormatter
from research_paper_ai.services.pdf_compiler import PDFCompiler


def run_formatter_pipeline(
    paper_content: str,
    output_dir: str | Path = "workspace/output",
) -> PipelineResult:
    """Run formatting, LaTeX generation, and PDF compilation."""

    if not isinstance(paper_content, str) or not paper_content.strip():
        raise ValueError("paper_content must be a non-empty string.")

    output_path = Path(output_dir).expanduser().resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    print("\n===== STEP 1 =====")
    print("Paper Formatting")

    formatted_paper = PaperFormatter.format(paper_content)

    manuscript_file = output_path / "manuscript.md"
    manuscript_file.write_text(
        str(formatted_paper),
        encoding="utf-8",
    )

    print("\n===== STEP 2 =====")
    print("LaTeX Generation")

    latex_doc = LatexComposer.compose(str(formatted_paper))

    exported_files = LatexExporter.export(
        latex_content=latex_doc.content,
        bibtex_content="",
        output_dir=output_path,
    )

    print("\n===== STEP 3 =====")
    print("PDF Compilation")

    pdf_file = PDFCompiler.compile(output_path)

    return PipelineResult(
        manuscript_file=str(manuscript_file),
        bibtex_file=exported_files["bib_file"],
        latex_file=exported_files["tex_file"],
        pdf_file=str(pdf_file),
    )
