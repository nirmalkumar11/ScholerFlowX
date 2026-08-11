from pathlib import Path

from research_paper_ai.models.pipeline_result import (
    PipelineResult
)

from research_paper_ai.crews.research_planning_crew import (
    run_research_planning
)

from research_paper_ai.parsers.research_plan_parser import (
    ResearchPlanParser
)

from research_paper_ai.crews.literature_retrieval_crew import (
    run_literature_retrieval
)

from research_paper_ai.crews.evidence_extraction_crew import (
    run_evidence_extraction
)

from research_paper_ai.crews.paper_writing_crew import (
    run_paper_writer
)

from research_paper_ai.services.citation_service import (
    create_citation_package
)

from research_paper_ai.services.latex_composer import (
    LatexComposer
)

from research_paper_ai.services.latex_exporter import (
    LatexExporter
)

from research_paper_ai.services.pdf_compiler import (
    PDFCompiler
)


def run_research_pipeline(
    paper_brief,
    output_dir="workspace/output"
):

    print("\n===== STEP 1 =====")
    print("Research Planning")

    raw_plan = run_research_planning(
        paper_brief
    )

    research_plan = (
        ResearchPlanParser.parse(
            str(raw_plan)
        )
    )

    print("\n===== STEP 2 =====")
    print("Literature Retrieval")

    literature_corpus = (
        run_literature_retrieval(
            research_plan
        )
    )

    print("\n===== STEP 3 =====")
    print("Evidence Extraction")

    evidence_package = (
        run_evidence_extraction(
            literature_corpus.papers
        )
    )

    print("\n===== STEP 4 =====")
    print("Citation Generation")

    citation_package = (
        create_citation_package(
            literature_corpus.papers
        )
    )

    print("\n===== STEP 5 =====")
    print("Paper Writing")

    manuscript = (
        run_paper_writer(
            paper_brief,
            research_plan,
            evidence_package,
            citation_package
        )
    )

    output_path = Path(
        output_dir
    )

    output_path.mkdir(
        parents=True,
        exist_ok=True
    )

    manuscript_file = (
        output_path /
        "manuscript.md"
    )

    manuscript_file.write_text(
        manuscript.content,
        encoding="utf-8"
    )

    print("\n===== STEP 6 =====")
    print("LaTeX Generation")

    latex_doc = (
        LatexComposer.compose(
            manuscript.content
        )
    )

    exported_files = (
        LatexExporter.export(
            latex_content=
            latex_doc.content,

            bibtex_content=
            citation_package.bibtex_content,

            output_dir=
            output_dir
        )
    )

    print("\n===== STEP 7 =====")
    print("PDF Compilation")

    pdf_file = (
        PDFCompiler.compile(
            output_dir
        )
    )

    return PipelineResult(
        manuscript_file=
        str(manuscript_file),

        bibtex_file=
        exported_files[
            "bib_file"
        ],

        latex_file=
        exported_files[
            "tex_file"
        ],

        pdf_file=
        pdf_file
    )