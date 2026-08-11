# src/research_paper_ai/validators/manuscript_validator.py

class ManuscriptValidator:

    FORBIDDEN_TERMS = [
        "talukder",
        "precision",
        "future research"
    ]

    REQUIRED_SECTIONS = [
        "# Title",
        "# Abstract",
        "# Introduction",
        "# Literature Review",
        "# Methodology",
        "# Results",
        "# Discussion",
        "# Conclusion",
        "# References"
    ]

    @staticmethod
    def validate(text):

        errors = []

        lower_text = text.lower()

        # Check forbidden terms
        for term in (
            ManuscriptValidator
            .FORBIDDEN_TERMS
        ):

            if term in lower_text:

                errors.append(
                    f"Forbidden term found: {term}"
                )

        # Check required sections
        for section in (
            ManuscriptValidator
            .REQUIRED_SECTIONS
        ):

            if section.lower() not in lower_text:

                errors.append(
                    f"Missing section: {section}"
                )

        # Check minimum length
        if len(text.strip()) < 500:

            errors.append(
                "Manuscript too short"
            )

        return errors