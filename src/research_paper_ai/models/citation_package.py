from dataclasses import dataclass


@dataclass
class CitationPackage:
    bibtex_content: str = ""