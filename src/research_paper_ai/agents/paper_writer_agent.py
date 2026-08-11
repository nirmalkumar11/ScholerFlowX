from crewai import Agent

from research_paper_ai.llm.groq_llm import get_llm


def create_paper_writer_agent():
    return Agent(
        role="Academic Research Paper Writer",
        goal=(
            "Write a complete academic research paper "
            "using the provided research plan and literature."
        ),
        backstory=(
            "You are a senior researcher and academic writer "
            "specializing in scientific publications."
        ),
        llm=get_llm(),
        verbose=True,
        allow_delegation=False
    )