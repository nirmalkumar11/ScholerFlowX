from dataclasses import dataclass, field


@dataclass
class ReviewReport:
    """Validation result for a manuscript.

    Defaults make the model safe to construct during initial workflow setup.
    """

    score: int = 100
    accepted: bool = True
    comments: list[str] = field(default_factory=list)
