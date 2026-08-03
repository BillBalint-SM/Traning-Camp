import json
from pathlib import Path
from typing import cast

import pytest
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.hashing import sha256_bytes
from knowledge_forge.io import canonical_json_bytes
from knowledge_forge.measurement import (
    build_context_trace,
    validate_context_trace,
    verify_context_traces,
    write_context_traces,
)
from knowledge_forge.portability import (
    build_portable_exports,
    load_portable_context_graph,
)

ROOT = Path(__file__).parents[1]
PACK_ROOT = ROOT / "pack"
SCHEMA_ROOT = ROOT / "forge" / "schemas"


def _context(tmp_path: Path) -> tuple[Path, dict[str, object]]:
    export_root = tmp_path / "exports" / "portable"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, export_root)
    context = load_portable_context_graph(export_root, "Eszközszerződés", 1)
    return export_root, context


def test_build_context_trace_is_metadata_only_and_self_verifying(tmp_path: Path) -> None:
    export_root, context = _context(tmp_path)

    trace = build_context_trace(
        "Eszközszerződés",
        context,
        1,
        {"route": 3, "load": 7, "total": 10},
    )

    validate_context_trace(trace)
    serialized = canonical_json_bytes(trace).decode("utf-8")
    assert "Eszközszerződés" not in serialized
    assert '"text"' not in serialized
    assert trace["export_sha256"] == json.loads(
        (export_root / "export.json").read_text(encoding="utf-8")
    )["export_sha256"]
    assert cast(dict[str, str], trace["timing_ms"])["total"] == 10


def test_trace_writer_and_verifier_bind_records_to_export(tmp_path: Path) -> None:
    export_root, context = _context(tmp_path)
    trace = build_context_trace(
        "Eszközszerződés",
        context,
        1,
        {"route": 3, "load": 7, "total": 10},
    )
    trace_path = tmp_path / "trace" / "contexts.jsonl"

    write_context_traces(trace_path, [trace])

    verified = verify_context_traces(trace_path, export_root)
    assert verified == [trace]


def test_verifier_rejects_trace_with_changed_module_hash(tmp_path: Path) -> None:
    export_root, context = _context(tmp_path)
    trace = build_context_trace(
        "Eszközszerződés",
        context,
        1,
        {"route": 3, "load": 7, "total": 10},
    )
    hashes = cast(dict[str, str], trace["module_hashes"])
    first_module = min(hashes)
    hashes[first_module] = "0" * 64
    trace_without_digest = dict(trace)
    trace_without_digest["trace_sha256"] = sha256_bytes(
        canonical_json_bytes({key: value for key, value in trace.items() if key != "trace_sha256"})
    )
    trace_path = tmp_path / "contexts.jsonl"
    write_context_traces(trace_path, [trace_without_digest])

    with pytest.raises(KnowledgeForgeError, match="module hash mismatch"):
        verify_context_traces(trace_path, export_root)


def test_trace_rejects_inconsistent_budget_and_timing() -> None:
    context = {
        "format_version": 1,
        "status": "not-covered",
        "area_id": None,
        "module_ids": [],
        "alternatives": [],
        "export_sha256": "a" * 64,
        "modules": [],
        "budget": {
            "format_version": 1,
            "max_chars": 20,
            "used_chars": 21,
            "omitted_module_ids": [],
        },
    }
    with pytest.raises(KnowledgeForgeError, match="budget"):
        build_context_trace("unknown", context, 0, {"route": 2, "load": 3, "total": 4})


def test_writer_rejects_empty_trace_file(tmp_path: Path) -> None:
    with pytest.raises(KnowledgeForgeError, match="at least one"):
        write_context_traces(tmp_path / "trace.jsonl", [])
