from research_paper_ai.models.review_report import (
    ReviewReport
)


class ReviewGenerator:

    @staticmethod
    def generate(
        manuscript_text,
        validation_errors
    ):

        score = 100

        score -= (
            len(validation_errors) * 10
        )

        if score < 0:
            score = 0

        accepted = score >= 80

        return ReviewReport(
            score=score,
            accepted=accepted,
            comments=validation_errors
        )