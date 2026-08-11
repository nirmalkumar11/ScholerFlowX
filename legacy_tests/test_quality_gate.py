from research_paper_ai.validators.manuscript_validator import (
    ManuscriptValidator
)

bad_text = ""

errors = (
    ManuscriptValidator.validate(
        bad_text
    )
)

print("\n===== ERRORS =====\n")

for error in errors:
    print(error)

assert len(errors) > 0

print(
    "\nQUALITY GATE TEST PASSED"
)