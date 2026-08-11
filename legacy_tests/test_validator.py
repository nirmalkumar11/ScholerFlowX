from research_paper_ai.validators.manuscript_validator import (
    ManuscriptValidator
)

sample = """
Talukder et al. reported...
Precision was 95%.
Future research should...
"""

errors = (
    ManuscriptValidator.validate(
        sample
    )
)

print(errors)

assert len(errors) > 0

print(
    "\nVALIDATOR TEST PASSED"
)