from pathlib import Path


class LatexExporter:

    @staticmethod
    def export(
        latex_content,
        bibtex_content,
        output_dir
    ):

        output_path = Path(
            output_dir
        )

        output_path.mkdir(
            parents=True,
            exist_ok=True
        )

        tex_file = (
            output_path / "main.tex"
        )

        bib_file = (
            output_path / "references.bib"
        )

        tex_file.write_text(
            latex_content,
            encoding="utf-8"
        )

        bib_file.write_text(
            bibtex_content,
            encoding="utf-8"
        )

        return {
            "tex_file": str(tex_file),
            "bib_file": str(bib_file)
        }