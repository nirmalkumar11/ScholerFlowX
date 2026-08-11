from research_paper_ai.models.review_report import (
    ReviewReport
)

from research_paper_ai.crews.rewrite_crew import (
    rewrite_manuscript
)

sample_manuscript = """
Talukder et al. reported...

Precision was 95%.

Future research should...
"""

report = ReviewReport(
    score=70,
    accepted=False,
    comments=[
        "Forbidden term found: talukder",
        "Forbidden term found: precision",
        "Forbidden term found: future research"
    ]
)

rewritten = rewrite_manuscript(
    sample_manuscript,
    report
)

print(
    "\n===== REWRITTEN =====\n"
)

print(rewritten)