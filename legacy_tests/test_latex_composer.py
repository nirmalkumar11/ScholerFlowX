from research_paper_ai.services.latex_composer import (
    LatexComposer
)

sample_markdown = """
# Title

AI for Lung Cancer Detection

# Abstract

This paper explores AI methods.

# Introduction

Introduction text.

# Literature Review

Review text.

# Methodology

Method text.

# Results

Results text.

# Discussion

Discussion text.

# Conclusion

Conclusion text.

# References

[1] Example Paper
"""

latex_doc = (
    LatexComposer.compose(
        sample_markdown
    )
)

print(
    "\n===== LATEX =====\n"
)

print(
    latex_doc.content
)

assert (
    "\\documentclass"
    in latex_doc.content
)

assert (
    "\\begin{abstract}"
    in latex_doc.content
)

assert (
    "\\section{Introduction}"
    in latex_doc.content
)

assert (
    "\\end{document}"
    in latex_doc.content
)

print(
    "\nLATEX COMPOSER TEST PASSED"
)