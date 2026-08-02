from pathlib import Path
from shutil import copytree
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile

import pytest
from knowledge_forge.archive import build_archive, verify_archive
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.package import validate_package

ROOT = Path(__file__).parents[1]
PACK_ROOT = ROOT / "pack"
SCHEMA_ROOT = ROOT / "forge" / "schemas"


def test_build_archive_has_only_manifest_allowlist_members(tmp_path: Path) -> None:
    archive_path = tmp_path / "knowledge-package-v0.zip"

    build_archive(PACK_ROOT, archive_path, SCHEMA_ROOT, [])

    assert archive_path.is_file()
    verify_archive(archive_path, SCHEMA_ROOT, [])


def test_build_archive_uses_store_mode_for_cross_runtime_determinism(
    tmp_path: Path,
) -> None:
    archive_path = tmp_path / "knowledge-package-v0.zip"

    build_archive(PACK_ROOT, archive_path, SCHEMA_ROOT, [])

    with ZipFile(archive_path) as archive:
        assert {info.compress_type for info in archive.infolist()} == {ZIP_STORED}


def test_relocated_package_validates_without_modification(tmp_path: Path) -> None:
    relocated_pack = tmp_path / "relocated-pack"
    copytree(PACK_ROOT, relocated_pack)

    validate_package(relocated_pack, SCHEMA_ROOT, [])


def test_verify_archive_rejects_zip_slip_member(tmp_path: Path) -> None:
    archive_path = tmp_path / "zip-slip.zip"
    with ZipFile(archive_path, "w", ZIP_DEFLATED) as archive:
        archive.writestr("../escape.txt", "blocked")

    with pytest.raises(KnowledgeForgeError, match="unsafe ZIP member"):
        verify_archive(archive_path, SCHEMA_ROOT, [])
