# src/research_paper_ai/utils/ranking_utils.py

def get_top_papers(
    rankings,
    top_k=3
):
    sorted_rankings = sorted(
        rankings,
        key=lambda x: x["ranked"].score,
        reverse=True
    )

    unique_papers = []
    seen_titles = set()

    for item in sorted_rankings:

        paper = item["paper"]

        title = paper.title.strip()

        if title in seen_titles:
            continue

        seen_titles.add(title)

        unique_papers.append(
            paper
        )

        if len(unique_papers) >= top_k:
            break

    return unique_papers