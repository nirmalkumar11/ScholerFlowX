from crewai import Task


def create_paper_writing_task(
    agent,
    paper_brief,
    research_plan,
    evidence_package,
    citation_package
):


    evidence_text = ""

    for idx, evidence in enumerate(
        evidence_package.evidence_items,
        start=1
    ):
        evidence_text += f"""

Study {idx}

Title:
{evidence.paper_title}

Methodologies:
{chr(10).join("- " + m for m in evidence.methodologies)}

Datasets:
{chr(10).join("- " + d for d in evidence.datasets)}

Results:
{chr(10).join("- " + r for r in evidence.results)}

"""

    return Task(
        description=f"""
You are an academic research paper writer.

You MUST generate the paper.

DO NOT ask questions.

DO NOT request additional information.

DO NOT explain limitations.

DO NOT refuse.

DO NOT say:
"I need more information"
"Please provide more details"
"Incomplete instructions"

Use only the provided information.

If information is missing:

write exactly:

Information not provided in the source material.

Your job is to generate the paper now.

====================================================
CRITICAL RULES
====================================================

FACT LOCK MODE

You are NOT allowed to introduce
any information that does not appear
inside EXTRACTED EVIDENCE.

If a statement cannot be directly
traced to EXTRACTED EVIDENCE,
do not write it.

Do not expand abbreviations.

Do not infer methodology details.

Do not infer datasets.

Do not infer metrics.

Do not infer authors.

Do not infer publication years.

Do not infer clinical relevance.

Do not infer limitations.

Do not infer future work.

ONLY use information explicitly provided.

The EXTRACTED EVIDENCE section
is the source of truth.

Never use information outside
the extracted evidence.

Never infer missing results.

Never invent metrics.

Never invent datasets.

NEVER invent:

- datasets
- experiments
- evaluation metrics
- accuracy values
- precision values
- recall values
- F1 scores
- sample sizes
- institutions
- hospitals
- benchmark results
- citations
- references

If information is missing, write exactly:

Information not provided in the source material.

Every methodology description
must identify which paper
reported it.

Every result must identify
which paper reported it.

Never describe methods
or results as your own work.

Use phrases such as:

- Talukder et al. reported...
- Darvish et al. described...
- Mishra et al. proposed...
- The study demonstrated...

====================================================
INPUT
====================================================

TOPIC:
{paper_brief.topic}

DOMAIN:
{paper_brief.domain}

OBJECTIVES:
{paper_brief.objectives}

KEYWORDS:
{paper_brief.keywords}

====================================================
EXTRACTED EVIDENCE
====================================================

{evidence_text}

====================================================
AVAILABLE REFERENCES
====================================================

{citation_package.bibtex_content}

====================================================
OUTPUT FORMAT
====================================================

# Title

# Abstract

# Introduction

# Literature Review

Create one subsection per study.

Only restate:

- title
- methodology
- dataset
- result

from EXTRACTED EVIDENCE.

Do not add any other information.

# Methodology

For each methodology include:

Study:
Method:
Dataset:
Purpose:

Examples include:

- Deep learning architectures
- CNN models
- Ensemble learning
- Feature extraction methods
- Datasets used
- Clinical data usage

Always attribute methodologies
to the original studies.

If no methodology information
exists in any retrieved paper,
write:

Information not provided in the source material.

# Results

For each study include:

Study:
Key Findings:
Reported Metrics:

Include:

- Accuracy
- Precision
- Recall
- Performance observations
- Clinical relevance

Never present results as your own.

Always attribute findings
to the original study.

If no results exist in the
retrieved papers, write:

Information not provided in the source material.

# Discussion

Compare studies using only
the methodologies, datasets
and results provided.

Do not introduce new claims.

Do not discuss clinical impact.

Do not discuss future work.

Do not discuss limitations unless
they are explicitly present in
EXTRACTED EVIDENCE.

# Conclusion

Summarize only the extracted evidence.

Do not introduce new findings.

Do not make recommendations.

Do not suggest future research.

# References

List only references provided in
AVAILABLE REFERENCES.
""",
        expected_output="""
A complete academic manuscript in markdown format.

You MUST return the following sections.

# Title

# Abstract

# Introduction

# Literature Review

# Methodology

# Results

# Discussion

# Conclusion

# References

Do not return anything else.""",
        agent=agent
    )