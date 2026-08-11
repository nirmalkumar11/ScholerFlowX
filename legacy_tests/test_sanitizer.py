from research_paper_ai.validators.sanitizer import (
    ManuscriptSanitizer
)

sample = """
Talukder et al. reported.

Precision was 95%.

Future research should
evaluate larger datasets.

Deep CNN achieved
good performance.
"""

cleaned = (
    ManuscriptSanitizer
    .sanitize(sample)
)

print(
    "\n===== CLEANED =====\n"
)

print(cleaned)

assert "talukder" not in (
    cleaned.lower()
)

assert "precision" not in (
    cleaned.lower()
)

assert "future research" not in (
    cleaned.lower()
)

print(
    "\nSANITIZER TEST PASSED"
)