from research_paper_ai.models.research_plan import (
    ResearchPlan
)

from research_paper_ai.crews.literature_retrieval_crew import (
    run_literature_retrieval
)

from research_paper_ai.crews.literature_ranking_crew import (
    run_literature_ranking
)

from research_paper_ai.parsers.literature_ranking_parser import (
    LiteratureRankingParser
)

from research_paper_ai.utils.ranking_utils import (
    get_top_papers
)

from research_paper_ai.services.citation_service import (
    create_citation_package
)


plan = ResearchPlan(
    title="Deep Learning for Lung Cancer Detection"
)

corpus = run_literature_retrieval(
    plan
)

raw_ranking = run_literature_ranking(
    research_topic=plan.title,
    papers=corpus.papers
)

rankings = LiteratureRankingParser.parse(
    raw_ranking,
    corpus.papers
)

top_papers = get_top_papers(
    rankings,
    top_k=3
)

citation_package = create_citation_package(
    top_papers
)

print("\n===== BIBTEX =====\n")

print(
    citation_package.bibtex_content
)

print(
    "\nCITATION GENERATION TEST PASSED"
)