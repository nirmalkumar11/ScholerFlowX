from crewai import (
    Agent,
    Task,
    Crew
)

from research_paper_ai.llm.groq_llm import (
    get_llm
)


class PaperFormatter:

    @staticmethod
    def format(
        paper_content
    ):

        agent = Agent(
            role=
            "Research Paper Formatter",

            goal=
            (
                "Convert research papers "
                "into a clean academic "
                "structure."
            ),

            backstory=
            (
                "You are an expert "
                "academic editor."
            ),

            llm=get_llm(),

            verbose=True
        )

        task = Task(
            description=f"""
You will receive a research paper.

DO NOT invent information.

DO NOT add new citations.

DO NOT remove content.

Normalize the structure.

Return markdown using:

# Title

# Abstract

# Introduction

# Literature Review

# Methodology

# Results

# Discussion

# Conclusion

# References

Research Paper:

{paper_content}
""",

            expected_output=
            """
A fully formatted
academic paper
in markdown.
""",

            agent=agent
        )

        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )

        result = crew.kickoff()

        return str(result)