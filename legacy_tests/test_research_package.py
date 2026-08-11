from research_paper_ai.ingestion.research_package_builder import (
    ResearchPackageBuilder
)


package = ResearchPackageBuilder.build()

print("\n=== Research Package Created ===\n")

print("Documents:", len(package.documents))
print("Images:", len(package.images))
print("Diagrams:", len(package.diagrams))
print("Datasets:", len(package.datasets))

print("\nMetadata:")
print(package.metadata)

print("\nRaw Text Length:")
print(len(package.raw_text))

print("\nPreview:")
print(package.raw_text[:300])

print("\nRESEARCH PACKAGE TEST PASSED")