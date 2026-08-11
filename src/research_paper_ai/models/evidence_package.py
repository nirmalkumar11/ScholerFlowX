from dataclasses import dataclass, field


@dataclass
class EvidenceItem:
    paper_title: str
    methodologies: list[str] = field(default_factory=list)
    datasets: list[str] = field(default_factory=list)
    results: list[str] = field(default_factory=list)


@dataclass
class EvidencePackage:
    evidence_items: list[EvidenceItem] = field(
        default_factory=list
    )