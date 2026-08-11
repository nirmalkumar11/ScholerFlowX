from research_paper_ai.validators.review_generator import (
    ReviewGenerator
)

errors = [
    "Forbidden term found: talukder",
    "Forbidden term found: precision",
    "Forbidden term found: future research"
]

report = (
    ReviewGenerator.generate(
        manuscript_text="sample",
        validation_errors=errors
    )
)

print(report)

assert report.score == 70
assert report.accepted is False

print(
    "\nREVIEW REPORT TEST PASSED"
)