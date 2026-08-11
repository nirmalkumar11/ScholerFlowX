from dataclasses import dataclass


@dataclass
class PipelineResult:
    manuscript_file: str
    bibtex_file: str
    latex_file: str
    pdf_file: str