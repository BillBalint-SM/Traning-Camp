import json
from pathlib import Path
from shutil import copytree

from knowledge_forge.cli import run

ROOT = Path(__file__).parents[1]
PORTABLE_EXPORT_ROOT = ROOT / "exports" / "portable-exports-v10"


def _workspace(tmp_path: Path) -> Path:
    workspace = tmp_path / "workspace"
    copytree(PORTABLE_EXPORT_ROOT, workspace / "exports" / "portable-exports-v10")
    return workspace


def test_cli_builds_and_verifies_a_portable_lexical_index(
    tmp_path: Path, capsys: object
) -> None:
    workspace = _workspace(tmp_path)
    arguments = [
        "build-portable-lexical-index",
        "--workspace",
        str(workspace),
        "--export",
        "exports/portable-exports-v10",
        "--index",
        "derived/portable-lexical-index-v1",
    ]

    assert run(arguments) == 0

    build_summary = json.loads(capsys.readouterr().out)
    assert build_summary["status"] == "PASS"
    assert build_summary["kind"] == "portable-lexical-index"
    assert (workspace / "derived" / "portable-lexical-index-v1" / "index.json").is_file()
    assert run(
        [
            "verify-portable-lexical-index",
            "--workspace",
            str(workspace),
            "--export",
            "exports/portable-exports-v10",
            "--index",
            "derived/portable-lexical-index-v1",
        ]
    ) == 0
    verify_summary = json.loads(capsys.readouterr().out)
    assert verify_summary["status"] == "PASS"
    assert verify_summary["export_sha256"] == build_summary["export_sha256"]
