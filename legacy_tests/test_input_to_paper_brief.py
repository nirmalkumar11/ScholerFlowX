from research_paper_ai.ingestion.research_package_builder import (
    ResearchPackageBuilder
)

from research_paper_ai.crews.research_crew import (
    run_input_understanding
)

from research_paper_ai.parsers.paper_brief_parser import (
    PaperBriefParser
)


package = ResearchPackageBuilder.build()

raw_output = run_input_understanding(
    package.raw_text
)

paper_brief = PaperBriefParser.parse(
    str(raw_output)
)

print("\n=== STRUCTURED PAPER BRIEF ===\n")

print(paper_brief)

print("\nINTEGRATION TEST PASSED")