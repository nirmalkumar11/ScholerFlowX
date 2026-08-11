class ManuscriptSanitizer:

    FORBIDDEN_TERMS = [
        "talukder",
        "precision",
        "future research"
    ]

    @staticmethod
    def sanitize(text):

        cleaned = text

        lines = cleaned.splitlines()

        filtered_lines = []

        for line in lines:

            lower_line = line.lower()

            should_remove = False

            for term in (
                ManuscriptSanitizer
                .FORBIDDEN_TERMS
            ):

                if term in lower_line:
                    should_remove = True
                    break

            if not should_remove:
                filtered_lines.append(
                    line
                )

        return "\n".join(
            filtered_lines
        )