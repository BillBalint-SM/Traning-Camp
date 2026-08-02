from pathlib import Path
from shutil import copytree

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
