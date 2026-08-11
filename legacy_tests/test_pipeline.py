from research_paper_ai.pipeline.research_pipeline import (
    run_research_pipeline
)

from research_paper_ai.models.paper_brief import (
    PaperBrief
)

paper_brief = PaperBrief(
    topic=
    "AI for Lung Cancer Detection",

    domain=
    "Healthcare AI",

    paper_type=
    "Research Paper",

    objectives=[
        "Improve diagnostic accuracy",
        "Reduce false positives"
    ],

    keywords=[
        "AI",
        "Lung Cancer",
        "Deep Learning"
    ]
)

result = run_research_pipeline(
    paper_brief
)

print(
    "\n===== PIPELINE RESULT =====\n"
)

print(result)

print(
    "\nPIPELINE TEST PASSED"
)