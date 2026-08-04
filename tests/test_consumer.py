import json
from pathlib import Path
from typing import cast

import pytest
from knowledge_forge.consumer import (
    consume_portable_export,
    validate_consumer_result,
    write_consumer_result,
)
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.hashing import sha256_bytes
from knowledge_forge.io import canonical_json_bytes
from knowledge_forge.portability import build_portable_exports

ROOT = Path(__file__).parents[1]
PACK_ROOT = ROOT / "pack"
SCHEMA_ROOT = ROOT / "forge" / "schemas"


def _export_root(tmp_path: Path) -> Path:
    output_root = tmp_path / "exports" / "portable"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)
    return output_root


def test_consume_returns_covered_context_and_metadata_receipt(tmp_path: Path) -> None:
    export_root = _export_root(tmp_path)

    result = consume_portable_export(export_root, "Eszközszerződés", 0, None)

    assert result["format_version"] == 1
    assert result["kind"] == "portable-consumer-result"
    assert result["export_sha256"] == result["context"]["export_sha256"]
    context = cast(dict[str, object], result["context"])
    receipt = cast(dict[str, object], result["receipt"])
    assert context["status"] == "covered"
    assert context["module_ids"] == ["procedure.tool-contract-design"]
    assert receipt["admitted_module_ids"] == context["expanded_module_ids"]
    assert receipt["omitted_module_ids"] == []
    assert "text" not in receipt
    assert "Eszközszerződés" not in canonical_json_bytes(receipt).decode("utf-8")
    validate_consumer_result(result)


def test_consume_graph_and_budget_are_deterministic(tmp_path: Path) -> None:
    export_root = _export_root(tmp_path)

    first = consume_portable_export(export_root, "Eszközszerződés", 1, 2000)
    second = consume_portable_export(export_root, "Eszközszerződés", 1, 2000)

    assert canonical_json_bytes(first) == canonical_json_bytes(second)
    context = cast(dict[str, object], first["context"])
    budget = cast(dict[str, object], context["budget"])
    receipt = cast(dict[str, object], first["receipt"])
    assert context["relation_depth"] == 1
    assert isinstance(context["relations"], list)
    assert budget["max_chars"] == 2000
    assert cast(int, budget["used_chars"]) <= 2000
    assert cast(list[str], receipt["omitted_module_ids"])


@pytest.mark.parametrize(
    ("query", "status"),
    [("agent", "ambiguous"), ("zzzxxyy", "not-covered")],
)
def test_consume_fail_closed_routes_have_no_admitted_modules(
    tmp_path: Path, query: str, status: str
) -> None:
    result = consume_portable_export(_export_root(tmp_path), query, 1, None)

    context = cast(dict[str, object], result["context"])
    receipt = cast(dict[str, object], result["receipt"])
    assert context["status"] == status
    assert context["modules"] == []
    assert receipt["admitted_module_ids"] == []
    assert receipt["module_hashes"] == {}


@pytest.mark.parametrize("relation_depth", [-1, 2, True])
def test_consume_rejects_invalid_depth(tmp_path: Path, relation_depth: object) -> None:
    with pytest.raises(KnowledgeForgeError, match="depth"):
        consume_portable_export(
            _export_root(tmp_path),
            "Eszközszerződés",
            cast(int, relation_depth),
            None,
        )


def test_consume_rejects_tampered_export(tmp_path: Path) -> None:
    export_root = _export_root(tmp_path)
    module_path = (
        export_root
        / "skill"
        / "references"
        / "knowledge"
        / "procedure.tool-contract-design.md"
    )
    module_path.write_text(module_path.read_text(encoding="utf-8") + "\nDelta\n", encoding="utf-8")

    with pytest.raises(KnowledgeForgeError, match="hash mismatch"):
        consume_portable_export(export_root, "Eszközszerződés", 0, None)


def test_write_consumer_result_is_atomic_and_preserves_existing_output(
    tmp_path: Path,
) -> None:
    result = consume_portable_export(_export_root(tmp_path), "Eszközszerződés", 0, None)
    output_path = tmp_path / "work" / "consumer-result.json"
    write_consumer_result(output_path, result)
    assert json.loads(output_path.read_text(encoding="utf-8")) == result

    output_path.write_text("sentinel\n", encoding="utf-8")
    with pytest.raises(KnowledgeForgeError, match="already exists"):
        write_consumer_result(output_path, result)
    assert output_path.read_text(encoding="utf-8") == "sentinel\n"


def test_validate_consumer_result_rejects_receipt_hash_drift(tmp_path: Path) -> None:
    result = consume_portable_export(_export_root(tmp_path), "Eszközszerződés", 0, None)
    receipt = cast(dict[str, object], result["receipt"])
    hashes = cast(dict[str, str], receipt["module_hashes"])
    hashes["procedure.tool-contract-design"] = sha256_bytes(b"tampered")

    with pytest.raises(KnowledgeForgeError, match="receipt module hash"):
        validate_consumer_result(result)
