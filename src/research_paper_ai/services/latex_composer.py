from research_paper_ai.models.latex_document import LatexDocument


class LatexComposer:

    SECTION_MAPPING = {
        "# Introduction": "Introduction",
        "# Literature Review": "Literature Review",
        "# Methodology": "Methodology",
        "# Results": "Results",
        "# Discussion": "Discussion",
        "# Conclusion": "Conclusion",
        "# References": "References"
    }

    @staticmethod
    def escape_latex(text):

        replacements = {
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text

    @staticmethod
    def compose(markdown_text):

        lines = markdown_text.splitlines()

        latex = []

        latex.append(r"\documentclass{article}")
        latex.append(r"\usepackage[utf8]{inputenc}")
        latex.append(r"\usepackage{hyperref}")
        latex.append("")

        latex.append(r"\begin{document}")
        latex.append("")

        i = 0

        while i < len(lines):

            line = lines[i].strip()

            # --------------------
            # Title
            # --------------------
            if line == "# Title":

                title = ""
                j = i + 1

                while j < len(lines):

                    candidate = (lines[j].strip())

                    if candidate:
                        title = candidate
                        break

                    j +=1

                title = (LatexComposer.escape_latex(title))

                latex.append(rf"\title{{{title}}}")
                latex.append(r"\maketitle")

                i = j + 1
                continue

            # --------------------
            # Abstract
            # --------------------
            if line == "# Abstract":

                latex.append(r"\begin{abstract}")

                abstract_lines = []

                j = i + 1

                while (j < len(lines)and not lines[j].startswith("#")):

                    abstract_lines.append(LatexComposer.escape_latex(lines[j]))

                    j += 1

                latex.append("\n".join(abstract_lines))

                latex.append(r"\end{abstract}")

                i = j
                continue

            # --------------------
            # Main Sections
            # --------------------
            if (line in LatexComposer.SECTION_MAPPING):

                section_name = (LatexComposer.SECTION_MAPPING[line])

                latex.append(rf"\section{{{section_name}}}")

                i += 1
                continue

            # --------------------
            # Markdown ##
            # --------------------
            if line.startswith("## "):

                heading = line[3:].strip()

                heading = (LatexComposer.escape_latex(heading))

                latex.append(rf"\subsection{{{heading}}}")

                i += 1
                continue

            # --------------------
            # Markdown ###
            # --------------------
            if line.startswith("### "):

                heading = line[4:].strip()

                heading = (LatexComposer.escape_latex(heading))

                latex.append(rf"\subsubsection{{{heading}}}")

                i += 1
                continue

            line = (LatexComposer.escape_latex(line))

            latex.append(line)

            i += 1

        latex.append("")
        latex.append(r"\bibliographystyle{plain}")

        latex.append(r"\bibliography{references}")

        latex.append("")
        latex.append(r"\end{document}")

        return LatexDocument(
            content="\n".join(
                latex
            )
        )