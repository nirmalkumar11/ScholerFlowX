from research_paper_ai.ingestion.research_package_builder import (
    ResearchPackageBuilder
)

from research_paper_ai.crews.research_crew import (
    run_input_understanding
)


package = ResearchPackageBuilder.build()

result = run_input_understanding(
    package.raw_text
)

print("\n===== PAPER BRIEF =====\n")
print(result)
