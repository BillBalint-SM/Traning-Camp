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


def _write_disposition_inputs(
    workspace: Path, unit_id: str, module_ids: list[str]
) -> None:
    units_path = workspace / "private/normalized/units.jsonl"
    known_units = {
        json.loads(line)["unit_id"]
        for line in units_path.read_text(encoding="utf-8").splitlines()
        if line
    }
    if unit_id not in known_units:
        with units_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps({"unit_id": unit_id}) + "\n")
    dispositions_path = workspace / "private/audit/unit-dispositions.json"
    dispositions_path.parent.mkdir(parents=True, exist_ok=True)
    state = "corroborating" if module_ids else "structural"
    reason = "corroborates-existing-module" if module_ids else "preamble"
    payload = {
        "format_version": 1,
        "unit_disposition": [
            {
                "unit_id": unit_id,
                "state": state,
                "reason": reason,
                "module_ids": module_ids,
            }
        ],
    }
    dispositions_path.write_text(json.dumps(payload), encoding="utf-8")


def _disposition_arguments(workspace: Path) -> list[str]:
    return [
        "verify-unit-disposition",
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
        "--dispositions",
        "private/audit/unit-dispositions.json",
        "--report",
        "private/audit/unit-coverage.json",
    ]


def test_cli_verifies_complete_unit_disposition(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    module_ids = sorted(path.stem for path in (workspace / "pack/knowledge").glob("*.md"))
    _write_coverage_inputs(workspace, module_ids)
    _write_disposition_inputs(workspace, "unit-structural", [])

    assert run(_disposition_arguments(workspace)) == 0

    report = json.loads(
        (workspace / "private/audit/unit-coverage.json").read_text(encoding="utf-8")
    )
    assert report["unit_count"] == 2
    assert report["promoted_unit_count"] == 1
    assert report["disposition_count"] == 1
    assert report["state_counts"] == {"structural": 1}


def test_cli_rejects_missing_unit_disposition(
    tmp_path: Path, capsys: object
) -> None:
    workspace = _workspace(tmp_path)
    module_ids = sorted(path.stem for path in (workspace / "pack/knowledge").glob("*.md"))
    _write_coverage_inputs(workspace, module_ids)
    _write_disposition_inputs(workspace, "unit-structural", [])
    disposition_path = workspace / "private/audit/unit-dispositions.json"
    payload = json.loads(disposition_path.read_text(encoding="utf-8"))
    payload["unit_disposition"] = []
    disposition_path.write_text(json.dumps(payload), encoding="utf-8")

    assert run(_disposition_arguments(workspace)) == 2
    assert "Unit disposition is missing unit" in capsys.readouterr().err
    assert not (workspace / "private/audit/unit-coverage.json").exists()


def test_cli_rejects_disposition_overlap_with_promoted_unit(
    tmp_path: Path, capsys: object
) -> None:
    workspace = _workspace(tmp_path)
    module_ids = sorted(path.stem for path in (workspace / "pack/knowledge").glob("*.md"))
    _write_coverage_inputs(workspace, module_ids)
    _write_disposition_inputs(workspace, "unit-reviewed", [])

    assert run(_disposition_arguments(workspace)) == 2
    assert "Unit disposition overlaps promoted unit" in capsys.readouterr().err
    assert not (workspace / "private/audit/unit-coverage.json").exists()


def test_cli_rejects_unknown_disposition_module(
    tmp_path: Path, capsys: object
) -> None:
    workspace = _workspace(tmp_path)
    module_ids = sorted(path.stem for path in (workspace / "pack/knowledge").glob("*.md"))
    _write_coverage_inputs(workspace, module_ids)
    _write_disposition_inputs(
        workspace, "unit-corroborating", ["principle.unknown"]
    )

    assert run(_disposition_arguments(workspace)) == 2
    assert "Unit disposition has unknown module" in capsys.readouterr().err
    assert not (workspace / "private/audit/unit-coverage.json").exists()


def test_cli_rejects_invalid_disposition_state_reason(
    tmp_path: Path, capsys: object
) -> None:
    workspace = _workspace(tmp_path)
    module_ids = sorted(path.stem for path in (workspace / "pack/knowledge").glob("*.md"))
    _write_coverage_inputs(workspace, module_ids)
    _write_disposition_inputs(workspace, "unit-structural", [])
    disposition_path = workspace / "private/audit/unit-dispositions.json"
    payload = json.loads(disposition_path.read_text(encoding="utf-8"))
    payload["unit_disposition"][0]["reason"] = "corroborates-existing-module"
    disposition_path.write_text(json.dumps(payload), encoding="utf-8")

    assert run(_disposition_arguments(workspace)) == 2
    assert "Unit disposition has invalid structural entry" in capsys.readouterr().err
    assert not (workspace / "private/audit/unit-coverage.json").exists()


def _write_routing_evaluation_suite(workspace: Path, threshold: int) -> Path:
    l0 = json.loads((workspace / "pack/indexes/l0.json").read_text(encoding="utf-8"))
    area_ids = sorted(area["id"] for area in l0["areas"])
    module_areas = {
        module["id"]: area_id
        for area_id in area_ids
        for module in json.loads(
            (workspace / f"pack/indexes/l1/{area_id}.json").read_text(
                encoding="utf-8"
            )
        )["modules"]
    }
    cases = [
        {
            "id": f"canonical.{module_id}.01",
            "category": "canonical",
            "query": "zzzxxyy",
            "expected_status": "covered",
            "expected_area_id": module_areas[module_id],
            "expected_module_ids": [module_id],
            "expected_alternatives": [],
        }
        for module_id in sorted(module_areas)
    ]
    cases.extend(
        {
            "id": f"paraphrase.{area_id}.{number:02d}",
            "category": "paraphrase",
            "query": "zzzxxyy",
            "expected_status": "covered",
            "expected_area_id": area_id,
            "expected_module_ids": [
                next(
                    module_id
                    for module_id, owner in sorted(module_areas.items())
                    if owner == area_id
                )
            ],
            "expected_alternatives": [],
        }
        for area_id in area_ids
        for number in range(1, 5)
    )
    cases.extend(
        {
            "id": f"negative.unsupported.{number:02d}",
            "category": "negative",
            "query": "zzzxxyy",
            "expected_status": "not-covered",
            "expected_area_id": None,
            "expected_module_ids": [],
            "expected_alternatives": [],
        }
        for number in range(1, 21)
    )
    cases.extend(
        {
            "id": f"ambiguous.cross-area.{number:02d}",
            "category": "ambiguous",
            "query": "zzzxxyy",
            "expected_status": "ambiguous",
            "expected_area_id": None,
            "expected_module_ids": [],
            "expected_alternatives": area_ids[:2],
        }
        for number in range(1, 11)
    )
    payload = {
        "format_version": 1,
        "expected_counts": {
            "canonical": 193,
            "paraphrase": 40,
            "negative": 20,
            "ambiguous": 10,
        },
        "thresholds": {
            "canonical_area_percent": threshold,
            "canonical_module_percent": threshold,
            "paraphrase_percent": threshold,
            "negative_percent": threshold,
            "ambiguous_percent": threshold,
        },
        "cases": cases,
    }
    suite_path = workspace / "forge/evals/routing-test.json"
    suite_path.parent.mkdir(parents=True, exist_ok=True)
    suite_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return suite_path


def _routing_evaluation_arguments(workspace: Path) -> list[str]:
    return [
        "verify-routing-evaluation",
        "--workspace",
        str(workspace),
        "--pack",
        "pack",
        "--schemas",
        "forge/schemas",
        "--suite",
        "forge/evals/routing-test.json",
        "--report",
        "private/audit/routing-evaluation.json",
    ]


def test_cli_verifies_passing_routing_evaluation(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    _write_routing_evaluation_suite(workspace, 0)

    assert run(_routing_evaluation_arguments(workspace)) == 0
    report = json.loads(
        (workspace / "private/audit/routing-evaluation.json").read_text(
            encoding="utf-8"
        )
    )
    assert report["status"] == "passed"
    assert report["case_count"] == 263


def test_cli_preserves_failed_routing_evaluation_report(
    tmp_path: Path, capsys: object
) -> None:
    workspace = _workspace(tmp_path)
    _write_routing_evaluation_suite(workspace, 100)

    assert run(_routing_evaluation_arguments(workspace)) == 2
    assert "Routing evaluation failed" in capsys.readouterr().err
    report = json.loads(
        (workspace / "private/audit/routing-evaluation.json").read_text(
            encoding="utf-8"
        )
    )
    assert report["status"] == "failed"
    assert report["failures"]


def test_cli_rejects_absolute_routing_suite_path(
    tmp_path: Path, capsys: object
) -> None:
    workspace = _workspace(tmp_path)
    suite_path = _write_routing_evaluation_suite(workspace, 0)
    arguments = _routing_evaluation_arguments(workspace)
    arguments[arguments.index("--suite") + 1] = str(suite_path.resolve())

    assert run(arguments) == 2
    assert "Path must be relative" in capsys.readouterr().err


def test_cli_rejects_escaping_routing_report_path(
    tmp_path: Path, capsys: object
) -> None:
    workspace = _workspace(tmp_path)
    _write_routing_evaluation_suite(workspace, 0)
    arguments = _routing_evaluation_arguments(workspace)
    arguments[arguments.index("--report") + 1] = "../routing-evaluation.json"

    assert run(arguments) == 2
    assert "Path escapes workspace root" in capsys.readouterr().err


def test_cli_rejects_routing_suite_symlink(tmp_path: Path, capsys: object) -> None:
    workspace = _workspace(tmp_path)
    suite_path = _write_routing_evaluation_suite(workspace, 0)
    target_path = suite_path.with_name("routing-target.json")
    suite_path.replace(target_path)
    try:
        suite_path.symlink_to(target_path)
    except OSError:
        pytest.skip("Symlink creation is unavailable")

    assert run(_routing_evaluation_arguments(workspace)) == 2
    assert "must not be a symbolic link" in capsys.readouterr().err
