from dataclasses import dataclass, field


@dataclass
class PaperBrief:
    topic: str = ""
    domain: str = ""
    paper_type: str = ""
    objectives: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)