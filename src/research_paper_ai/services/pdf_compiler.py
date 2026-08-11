from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


class PDFCompiler:
    """Compile a LaTeX document into PDF using a local TeX installation."""

    @staticmethod
    def _run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
        executable = shutil.which(command[0])

        if executable is None:
            raise RuntimeError(
                f"Required executable '{command[0]}' was not found on PATH. "
                "Install a LaTeX distribution such as MacTeX on macOS."
            )

        return subprocess.run(
            command,
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )

    @staticmethod
    def compile(output_dir: str | Path) -> str:
        output_path = Path(output_dir).expanduser().resolve()
        tex_file = output_path / "main.tex"

        if not tex_file.is_file():
            raise FileNotFoundError(f"{tex_file} not found")

        first = PDFCompiler._run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
            output_path,
        )

        pdf_file = output_path / "main.pdf"

        if first.returncode != 0 or not pdf_file.is_file():
            log = first.stdout + "\n" + first.stderr
            raise RuntimeError(
                "pdflatex failed on the first pass.\n\n"
                + log[-6000:]
            )

        # Only run BibTeX when the LaTeX auxiliary file contains citations.
        aux_file = output_path / "main.aux"
        aux_text = (
            aux_file.read_text(encoding="utf-8", errors="ignore")
            if aux_file.is_file()
            else ""
        )

        if "\\citation" in aux_text:
            bib_file = output_path / "references.bib"

            if not bib_file.is_file():
                raise FileNotFoundError(
                    f"{bib_file} is required because the document contains citations."
                )

            bib = PDFCompiler._run(
                ["bibtex", "main"],
                output_path,
            )

            if bib.returncode != 0:
                raise RuntimeError(
                    "bibtex failed.\n\n"
                    + (bib.stdout + "\n" + bib.stderr)[-6000:]
                )

            for _ in range(2):
                result = PDFCompiler._run(
                    [
                        "pdflatex",
                        "-interaction=nonstopmode",
                        "-halt-on-error",
                        "main.tex",
                    ],
                    output_path,
                )

                if result.returncode != 0:
                    raise RuntimeError(
                        "pdflatex failed while resolving bibliography.\n\n"
                        + (result.stdout + "\n" + result.stderr)[-6000:]
                    )

        if not pdf_file.is_file():
            raise RuntimeError("PDF generation failed: main.pdf was not created.")

        return str(pdf_file)
