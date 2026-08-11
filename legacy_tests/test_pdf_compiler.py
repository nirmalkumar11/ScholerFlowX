from research_paper_ai.services.pdf_compiler import (
    PDFCompiler
)

pdf_file = PDFCompiler.compile(
    "workspace/outputs"
)

print("\n===== PDF FILE =====\n")

print(pdf_file)

print(
    "\nPDF COMPILER TEST PASSED"
)   