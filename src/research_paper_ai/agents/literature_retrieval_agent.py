from crewai import Agent

from research_paper_ai.llm.groq_llm import get_llm


def create_literature_retrieval_agent():
    return Agent(
        role="Literature Retrieval Specialist",
        goal=(
            "Determine the best academic search query "
            "for retrieving relevant research papers."
        ),
        backstory=(
            "You are an academic librarian and research expert. "
            "Your job is to transform research plans into "
            "high-quality search queries."
        ),
        llm=get_llm(),
        verbose=True,
        allow_delegation=False
    )