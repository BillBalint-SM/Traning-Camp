from pathlib import Path
from shutil import copytree
from typing import cast

from knowledge_forge.lexical_index import (
    _tokenize,
    build_portable_lexical_index,
    load_portable_context_lexical,
    verify_portable_lexical_index,
)
from knowledge_forge.measurement import build_context_trace, validate_context_trace
from knowledge_forge.portability import (
    load_verified_portable_modules,
    verify_portable_export,
)

ROOT = Path(__file__).parents[1]
PORTABLE_EXPORT_ROOT = ROOT / "exports" / "portable-exports-v10"


def _copy_export(tmp_path: Path, name: str) -> Path:
    destination = tmp_path / name
    copytree(PORTABLE_EXPORT_ROOT, destination)
    return destination


def test_tokenize_nfkc_casefolds_and_splits_identifier_segments() -> None:
    assert _tokenize("Ａgent-Tool.Contract") == ["agent", "tool", "contract"]


def test_builds_byte_identical_indexes_from_equivalent_verified_exports(
    tmp_path: Path,
) -> None:
    first_export = _copy_export(tmp_path, "first-export")
    second_export = _copy_export(tmp_path, "second-export")
    first_index = tmp_path / "derived" / "first-index"
    second_index = tmp_path / "derived" / "second-index"

    first_manifest = build_portable_lexical_index(first_export, first_index)
    second_manifest = build_portable_lexical_index(second_export, second_index)

    assert first_manifest == second_manifest
    assert (first_index / "index.json").read_bytes() == (
        second_index / "index.json"
    ).read_bytes()
    assert verify_portable_lexical_index(first_export, first_index) == cast(
        dict[str, object], first_manifest
    )


def test_public_verified_module_loader_returns_portable_content_hashes(
    tmp_path: Path,
) -> None:
    export_root = _copy_export(tmp_path, "portable-export")
    verify_portable_export(export_root)

    modules = load_verified_portable_modules(
        export_root,
        ["procedure.tool-contract-design"],
    )

    assert modules[0]["id"] == "procedure.tool-contract-design"
    assert len(cast(str, modules[0]["content_sha256"])) == 64
    assert "Eszközszerződés" in cast(str, modules[0]["text"])


def test_lexical_context_loads_one_verified_module_without_relations(
    tmp_path: Path,
) -> None:
    export_root = _copy_export(tmp_path, "portable-export")
    index_root = tmp_path / "derived" / "index"
    build_portable_lexical_index(export_root, index_root)

    context = load_portable_context_lexical(
        export_root,
        index_root,
        "Eszközszerződés",
        100000,
    )

    assert context["status"] == "covered"
    assert context["area_id"] == "tool-execution"
    assert context["module_ids"] == ["procedure.tool-contract-design"]
    assert context["expanded_module_ids"] == ["procedure.tool-contract-design"]
    assert context["relations"] == []
    assert context["budget"] == {
        "format_version": 1,
        "max_chars": 100000,
        "used_chars": len(cast(str, cast(list[dict[str, object]], context["modules"])[0]["text"])),
        "omitted_module_ids": [],
    }
    trace = build_context_trace(
        "Eszközszerződés",
        context,
        0,
        {"route": 0, "load": 1, "total": 1},
    )
    validate_context_trace(trace)


def test_lexical_uncovered_contexts_admit_no_modules(tmp_path: Path) -> None:
    export_root = _copy_export(tmp_path, "portable-export")
    index_root = tmp_path / "derived" / "index"
    build_portable_lexical_index(export_root, index_root)

    for query, status in (("agent", "ambiguous"), ("zzzxxyy", "not-covered")):
        context = load_portable_context_lexical(export_root, index_root, query, 100000)
        assert context["status"] == status
        assert context["modules"] == []
        assert context["expanded_module_ids"] == []
        assert context["budget"]["used_chars"] == 0
