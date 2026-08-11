

from dataclasses import dataclass

from research_paper_ai.models.research_package import ResearchPackage
from research_paper_ai.models.paper_brief import PaperBrief
from research_paper_ai.models.research_plan import ResearchPlan
from research_paper_ai.models.literature_corpus import LiteratureCorpus
from research_paper_ai.models.citation_package import CitationPackage
from research_paper_ai.models.manuscript import Manuscript
from research_paper_ai.models.review_report import ReviewReport


@dataclass
class WorkflowState:
    research_package: ResearchPackage

    paper_brief: PaperBrief

    research_plan: ResearchPlan

    literature_corpus: LiteratureCorpus

    citation_package: CitationPackage

    manuscript: Manuscript

    review_report: ReviewReport