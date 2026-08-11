from research_paper_ai.crews.revision_loop import (
    revise_until_valid
)

sample_manuscript = """
Talukder et al. reported
strong results.

Precision was 95%.

Future research should
evaluate larger datasets.
"""

final_text, report = (
    revise_until_valid(
        sample_manuscript,
        max_attempts=3
    )
)

print(
    "\n===== FINAL MANUSCRIPT =====\n"
)

print(final_text)

print(
    "\n===== FINAL REPORT =====\n"
)

print(report)

print(
    "\nREVISION LOOP TEST PASSED"
)