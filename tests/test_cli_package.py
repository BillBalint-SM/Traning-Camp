import json
from pathlib import Path
from shutil import copytree

import pytest
from knowledge_forge.cli import run

ROOT = Path(__file__).parents[1]
PACK_ROOT = ROOT / "pack"
SCHEMA_ROOT = ROOT / "forge" / "schemas"


def _workspace(tmp_path: Path) -> Path:
    copytree(PACK_ROOT, tmp_path / "pack")
    copytree(SCHEMA_ROOT, tmp_path / "forge" / "schemas")
    markers_path = tmp_path / "private" / "leakage" / "markers.json"
    markers_path.parent.mkdir(parents=True)
    markers_path.write_text("[]\n", encoding="utf-8")
    return tmp_path


def test_cli_build_verify_route_and_archive_package(
    tmp_path: Path, capsys: object
) -> None:
    workspace = _workspace(tmp_path)
    workspace_text = str(workspace)

    assert run(
        [
            "build-package",
            "--workspace",
            workspace_text,
            "--pack",
            "pack",
            "--schemas",
            "forge/schemas",
        ]
    ) == 0
    assert run(
        [
            "verify-package",
            "--workspace",
            workspace_text,
            "--pack",
            "pack",
            "--schemas",
            "forge/schemas",
            "--markers",
            "private/leakage/markers.json",
        ]
    ) == 0
    assert run(
        [
            "route",
            "--workspace",
            workspace_text,
            "--pack",
            "pack",
            "--query",
            "Eszközszerződés",
        ]
    ) == 0
    assert "procedure.tool-contract-design" in capsys.readouterr().out
    assert run(
        [
            "archive-package",
            "--workspace",
            workspace_text,
            "--pack",
            "pack",
            "--schemas",
            "forge/schemas",
            "--markers",
            "private/leakage/markers.json",
            "--archive",
            "dist/knowledge-package-v0.zip",
        ]
    ) == 0
    assert (workspace / "dist" / "knowledge-package-v0.zip").is_file()


def test_cli_inspect_package_emits_canonical_profile(
    tmp_path: Path, capsys: object
) -> None:
    workspace = _workspace(tmp_path)

    assert run(
        [
            "inspect-package",
            "--workspace",
            str(workspace),
            "--pack",
            "pack",
            "--schemas",
            "forge/schemas",
        ]
    ) == 0

    output = capsys.readouterr().out
    profile = json.loads(output)
    assert profile["format_version"] == 1
    assert profile["module_count"] == 193
    assert profile["area_count"] == 10
    assert profile["relation_count"] >= 193
    assert profile["language_counts"] == {"hu": 193}
    assert profile["maturity_counts"]["deprecated"] == 0
    assert len(profile["package_sha256"]) == 64
    assert output == json.dumps(
        profile,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ) + "\n"


def _write_coverage_inputs(workspace: Path, module_ids: list[str]) -> None:
    units_path = workspace / "private" / "normalized" / "units.jsonl"
    units_path.parent.mkdir(parents=True)
    units_path.write_text('{"unit_id":"unit-reviewed"}\n', encoding="utf-8")
    reviews_path = workspace / "private" / "provenance"
    reviews_path.mkdir(parents=True)
    payload = {
        "format_version": 1,
        "promotion_review": [
            {
                "module_id": module_id,
                "unit_ids": ["unit-reviewed"],
                "review_state": "reviewed",
            }
            for module_id in module_ids
        ],
    }
    (reviews_path / "promotion-map.json").write_text(
        json.dumps(payload), encoding="utf-8"
    )


def _coverage_arguments(workspace: Path) -> list[str]:
    return [
        "verify-promotion-coverage",
        "--workspace",
        str(workspace),
        "--pack",
        "pack",
        "--schemas",
        "forge/schemas",
        "--units",
        "private/normalized/units.jsonl",
        "--reviews",
        "private/provenance",
        "--report",
        "private/audit/coverage.json",
    ]


def test_cli_verifies_exact_promotion_coverage(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    module_ids = sorted(path.stem for path in (workspace / "pack/knowledge").glob("*.md"))
    _write_coverage_inputs(workspace, module_ids)

    assert run(_coverage_arguments(workspace)) == 0

    report = json.loads(
        (workspace / "private/audit/coverage.json").read_text(encoding="utf-8")
    )
    assert report["format_version"] == 1
    assert report["module_count"] == 193
    assert report["review_file_count"] == 1
    assert report["unique_unit_count"] == 1
    assert len(report["coverage_sha256"]) == 64


def test_cli_rejects_missing_promotion_coverage(
    tmp_path: Path, capsys: object
) -> None:
    workspace = _workspace(tmp_path)
    module_ids = sorted(path.stem for path in (workspace / "pack/knowledge").glob("*.md"))
    _write_coverage_inputs(workspace, module_ids[1:])

    assert run(_coverage_arguments(workspace)) == 2
    assert "Promotion coverage is missing module" in capsys.readouterr().err
    assert not (workspace / "private/audit/coverage.json").exists()


def test_cli_rejects_duplicate_promotion_coverage(
    tmp_path: Path, capsys: object
) -> None:
    workspace = _workspace(tmp_path)
    module_ids = sorted(path.stem for path in (workspace / "pack/knowledge").glob("*.md"))
    _write_coverage_inputs(workspace, module_ids + [module_ids[0]])

    assert run(_coverage_arguments(workspace)) == 2
    assert "Promotion coverage contains duplicate module" in capsys.readouterr().err
    assert not (workspace / "private/audit/coverage.json").exists()


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        (
            "review_state",
            "candidate",
            "Promotion coverage contains unreviewed module",
        ),
        (
            "unit_ids",
            ["unit-missing"],
            "Promotion coverage has unknown unit endpoint",
        ),
    ],
)
def test_cli_rejects_invalid_promotion_endpoint(
    tmp_path: Path,
    capsys: object,
    field: str,
    value: object,
    message: str,
) -> None:
    workspace = _workspace(tmp_path)
    module_ids = sorted(path.stem for path in (workspace / "pack/knowledge").glob("*.md"))
    _write_coverage_inputs(workspace, module_ids)
    review_path = workspace / "private/provenance/promotion-map.json"
    payload = json.loads(review_path.read_text(encoding="utf-8"))
    payload["promotion_review"][0][field] = value
    review_path.write_text(json.dumps(payload), encoding="utf-8")

    assert run(_coverage_arguments(workspace)) == 2
    assert message in capsys.readouterr().err
    assert not (workspace / "private/audit/coverage.json").exists()


def test_cli_rejects_unknown_promoted_module(
    tmp_path: Path, capsys: object
) -> None:
    workspace = _workspace(tmp_path)
    module_ids = sorted(path.stem for path in (workspace / "pack/knowledge").glob("*.md"))
    _write_coverage_inputs(workspace, module_ids + ["principle.unknown"])

    assert run(_coverage_arguments(workspace)) == 2
    assert "Promotion coverage contains unknown module" in capsys.readouterr().err
    assert not (workspace / "private/audit/coverage.json").exists()
