from pathlib import Path
from shutil import copytree

import pytest
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.manifest import write_manifest
from knowledge_forge.package import validate_package

ROOT = Path(__file__).parents[1]
PACK_ROOT = ROOT / "pack"
SCHEMA_ROOT = ROOT / "forge" / "schemas"


def _copy_clean_package(tmp_path: Path) -> Path:
    package_root = tmp_path / "pack"
    copytree(PACK_ROOT, package_root)
    return package_root


def test_validate_package_accepts_clean_package() -> None:
    manifest = validate_package(PACK_ROOT, SCHEMA_ROOT, [])

    assert manifest["format_version"] == 1
    assert manifest["files"]


def test_validate_package_rejects_undeclared_file(tmp_path: Path) -> None:
    package_root = _copy_clean_package(tmp_path)
    (package_root / "knowledge" / "unlisted.md").write_text("x", encoding="utf-8")

    with pytest.raises(KnowledgeForgeError, match="(?i)undeclared package file"):
        validate_package(package_root, SCHEMA_ROOT, [])


def test_validate_package_rejects_seeded_private_marker(tmp_path: Path) -> None:
    package_root = _copy_clean_package(tmp_path)
    skill_path = package_root / "skills" / "SKILL.md"
    skill_path.write_text(
        skill_path.read_text(encoding="utf-8") + "\nprivate-seed-marker\n",
        encoding="utf-8",
    )
    write_manifest(package_root)

    with pytest.raises(KnowledgeForgeError, match="forbidden content marker"):
        validate_package(package_root, SCHEMA_ROOT, ["private-seed-marker"])


def test_validate_package_rejects_stale_file_hash(tmp_path: Path) -> None:
    package_root = _copy_clean_package(tmp_path)
    module_path = package_root / "knowledge" / "principle.context-is-finite.md"
    module_path.write_text(
        module_path.read_text(encoding="utf-8") + "\nKiegészítés.\n",
        encoding="utf-8",
    )

    with pytest.raises(KnowledgeForgeError, match="(?i)stale manifest hash"):
        validate_package(package_root, SCHEMA_ROOT, [])


def test_validate_package_allows_harmless_technical_phrase(tmp_path: Path) -> None:
    package_root = _copy_clean_package(tmp_path)
    skill_path = package_root / "skills" / "SKILL.md"
    skill_path.write_text(
        skill_path.read_text(encoding="utf-8") + "\nA source code kifejezés műszaki szöveg.\n",
        encoding="utf-8",
    )
    write_manifest(package_root)

    validate_package(package_root, SCHEMA_ROOT, ["private-seed-marker"])


def test_validate_package_rejects_full_module_body_in_skill(tmp_path: Path) -> None:
    package_root = _copy_clean_package(tmp_path)
    skill_path = package_root / "skills" / "SKILL.md"
    skill_path.write_text(
        skill_path.read_text(encoding="utf-8") + "\n## Lényeg\n\nNem routing utasítás.\n",
        encoding="utf-8",
    )
    write_manifest(package_root)

    with pytest.raises(KnowledgeForgeError, match="must not embed module body sections"):
        validate_package(package_root, SCHEMA_ROOT, [])
