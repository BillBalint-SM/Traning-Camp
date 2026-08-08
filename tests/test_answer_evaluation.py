from pathlib import Path
from shutil import copytree

from knowledge_forge.answer_evaluation import (
    build_answer_evaluation_request,
    validate_answer_evaluation_request,
)
from knowledge_forge.hashing import sha256_bytes
from knowledge_forge.io import canonical_json_bytes
from knowledge_forge.lexical_index import (
    build_portable_lexical_index,
    load_portable_context_lexical,
)
from knowledge_forge.measurement import build_context_trace

ROOT = Path(__file__).parents[1]
PORTABLE_EXPORT_ROOT = ROOT / "exports" / "portable-exports-v10"


def _context_trace(tmp_path: Path) -> dict[str, object]:
    export_root = tmp_path / "portable-export"
    index_root = tmp_path / "derived" / "index"
    copytree(PORTABLE_EXPORT_ROOT, export_root)
    build_portable_lexical_index(export_root, index_root)
    context = load_portable_context_lexical(
        export_root,
        index_root,
        "Eszközszerződés",
        100000,
    )
    return build_context_trace(
        "Eszközszerződés",
        context,
        0,
        {"route": 0, "load": 1, "total": 1},
    )


def test_answer_request_binds_case_query_trace_and_expected_modules(
    tmp_path: Path,
) -> None:
    trace = _context_trace(tmp_path)

    request = build_answer_evaluation_request(
        "canonical.procedure.tool-contract-design.01",
        "Eszközszerződés",
        "lexical-v1",
        trace,
        ["procedure.tool-contract-design"],
    )

    validate_answer_evaluation_request(request)
    serialized = canonical_json_bytes(request).decode("utf-8")
    assert request["query_sha256"] == sha256_bytes("Eszközszerződés".encode())
    assert request["context_trace_sha256"] == trace["trace_sha256"]
    assert "Eszközszerződés" not in serialized
    assert '"text"' not in serialized
