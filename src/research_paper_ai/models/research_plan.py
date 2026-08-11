# src/research_paper_ai/models/research_plan.py

from dataclasses import dataclass, field


@dataclass
class ResearchPlan:
    title: str = ""

    outline: list[str] = field(default_factory=list)

    research_questions: list[str] = field(default_factory=list)

    literature_requirements: list[str] = field(default_factory=list)

    raw_plan: str = ""