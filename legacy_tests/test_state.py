from research_paper_ai.models.paper_brief import PaperBrief
from research_paper_ai.models.research_plan import ResearchPlan
from research_paper_ai.models.literature_corpus import LiteratureCorpus
from research_paper_ai.models.citation_package import CitationPackage
from research_paper_ai.models.manuscript import Manuscript
from research_paper_ai.models.review_report import ReviewReport

from research_paper_ai.state.workflow_state import WorkflowState
from research_paper_ai.state.checkpoints import CheckpointManager


state = WorkflowState(
    paper_brief=PaperBrief(topic="AI Research"),
    research_plan=ResearchPlan(),
    literature_corpus=LiteratureCorpus(),
    citation_package=CitationPackage(),
    manuscript=Manuscript(),
    review_report=ReviewReport()
)

CheckpointManager.save(
    state,
    "workspace/intermediate/workflow_state.json"
)

loaded = CheckpointManager.load(
    "workspace/intermediate/workflow_state.json"
)

print(loaded)

print("\nSTATE TEST PASSED")