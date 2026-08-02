from knowledge_forge.models import (
    ExtractedDocument,
    InputRecord,
    NormalizedUnit,
    PdfProbe,
)


def build_provenance_ledger(
    inputs: list[InputRecord],
    documents: list[ExtractedDocument],
    units: list[NormalizedUnit],
    pdf_probe: PdfProbe,
) -> dict[str, object]:
    return {
        "schema_version": 1,
        "inputs": sorted(inputs, key=lambda item: item["role"]),
        "documents": sorted(documents, key=lambda item: item["spine_index"]),
        "units": sorted(
            units,
            key=lambda item: (item["document_id"], item["ordinal"]),
        ),
        "pdf_probe": pdf_probe,
    }
