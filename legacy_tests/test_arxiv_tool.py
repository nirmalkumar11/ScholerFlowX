from research_paper_ai.tools.arxiv_tool import (
    ArxivTool
)


papers = ArxivTool.search(
    query="lung cancer deep learning",
    max_results=3
)

print("\n=== ARXIV RESULTS ===\n")

for idx, paper in enumerate(
    papers,
    start=1
):
    print(f"\nPaper {idx}")
    print("Title:", paper.title)
    print("Authors:", ", ".join(paper.authors))
    print("Published:", paper.published)
    print("URL:", paper.arxiv_url)

print("\nARXIV TOOL TEST PASSED")