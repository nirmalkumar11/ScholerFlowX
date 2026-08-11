from research_paper_ai.services.latex_composer import LatexComposer


def test_compose_basic_markdown():
    doc = LatexComposer.compose(
        """# Title

AI for Lung Cancer Detection

# Abstract

This paper explores AI methods.

# Introduction

Introduction text.

# Methodology

Method text.

# Results

Results text.

# Conclusion

Conclusion text.
"""
    )

    assert r"\documentclass{article}" in doc.content
    assert r"\title{AI for Lung Cancer Detection}" in doc.content
    assert r"\begin{abstract}" in doc.content
    assert r"\section{Introduction}" in doc.content
    assert r"\end{document}" in doc.content


def test_compose_escapes_latex_special_characters():
    escaped = LatexComposer.escape_latex("A & B 100% #1 x_y")
    assert r"A \& B 100\% \#1 x\_y" == escaped
