import stat
from pathlib import Path
from shutil import copytree
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile, ZipInfo

import pytest
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.portable_archive import (
    build_portable_bundle,
    verify_portable_bundle,
)

ROOT = Path(__file__).parents[1]
EXPORT_ROOT = ROOT / "exports" / "portable-exports-v10"


def test_build_portable_bundle_round_trips_manifest_and_root_layout(
    tmp_path: Path,
) -> None:
    bundle_path = tmp_path / "portable-exports-v10.zip"

    manifest = build_portable_bundle(EXPORT_ROOT, bundle_path)

    assert manifest["kind"] == "portable-agent-exports"
    assert (
        verify_portable_bundle(bundle_path)["export_sha256"]
        == manifest["export_sha256"]
    )
    with ZipFile(bundle_path) as archive:
        names = archive.namelist()
    declared = [entry["path"] for entry in manifest["files"]]
    assert names == sorted([*declared, "export.json"])
    assert all("/" in name or name == "export.json" for name in names)


def test_build_portable_bundle_is_byte_identical(tmp_path: Path) -> None:
    first = tmp_path / "first.zip"
    second = tmp_path / "second.zip"

    build_portable_bundle(EXPORT_ROOT, first)
    build_portable_bundle(EXPORT_ROOT, second)

    assert first.read_bytes() == second.read_bytes()


def test_build_portable_bundle_uses_store_mode_and_fixed_metadata(
    tmp_path: Path,
) -> None:
    bundle_path = tmp_path / "portable.zip"
    build_portable_bundle(EXPORT_ROOT, bundle_path)

    with ZipFile(bundle_path) as archive:
        assert [info.filename for info in archive.infolist()] == sorted(
            info.filename for info in archive.infolist()
        )
        assert {info.compress_type for info in archive.infolist()} == {ZIP_STORED}
        assert {info.date_time for info in archive.infolist()} == {
            (1980, 1, 1, 0, 0, 0)
        }
        assert {info.external_attr >> 16 for info in archive.infolist()} == {
            (stat.S_IFREG | 0o644)
        }


@pytest.mark.parametrize(
    "member",
    [
        "../escape.txt",
        "/absolute.txt",
        "C:/drive.txt",
        "skill\\escape.txt",
    ],
)
def test_verify_portable_bundle_rejects_unsafe_member(
    tmp_path: Path,
    member: str,
) -> None:
    bundle_path = tmp_path / "unsafe.zip"
    with ZipFile(bundle_path, "w", ZIP_DEFLATED) as archive:
        archive.writestr(member, b"blocked")

    with pytest.raises(KnowledgeForgeError, match="unsafe ZIP member"):
        verify_portable_bundle(bundle_path)


def test_verify_portable_bundle_rejects_duplicate_member(tmp_path: Path) -> None:
    bundle_path = tmp_path / "duplicate.zip"
    with ZipFile(bundle_path, "w") as archive:
        archive.writestr("export.json", b"{}")
        archive.writestr("export.json", b"{}")

    with pytest.raises(KnowledgeForgeError, match="duplicate"):
        verify_portable_bundle(bundle_path)


def test_build_portable_bundle_rejects_tampered_export(tmp_path: Path) -> None:
    export_root = tmp_path / "export"
    copytree(EXPORT_ROOT, export_root)
    (export_root / "rag" / "documents.jsonl").write_text(
        "tampered\n",
        encoding="utf-8",
    )

    with pytest.raises(KnowledgeForgeError, match="hash mismatch"):
        build_portable_bundle(export_root, tmp_path / "tampered.zip")


def test_verify_portable_bundle_rejects_missing_and_extra_members(
    tmp_path: Path,
) -> None:
    bundle_path = tmp_path / "portable.zip"
    build_portable_bundle(EXPORT_ROOT, bundle_path)

    missing_path = tmp_path / "missing.zip"
    with ZipFile(missing_path, "w") as archive, ZipFile(bundle_path) as source:
        for info in source.infolist()[:-1]:
            archive.writestr(info, source.read(info))
    with pytest.raises(KnowledgeForgeError, match="inventory"):
        verify_portable_bundle(missing_path)

    extra_path = tmp_path / "extra.zip"
    with ZipFile(bundle_path) as source:
        members = [
            (info.filename, source.read(info)) for info in source.infolist()
        ]
    with ZipFile(extra_path, "w") as archive:
        for name, content in sorted([*members, ("extra.txt", b"unexpected")]):
            info = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_STORED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, content)
    with pytest.raises(KnowledgeForgeError, match="inventory"):
        verify_portable_bundle(extra_path)


def test_build_portable_bundle_rejects_existing_file_destination(
    tmp_path: Path,
) -> None:
    bundle_path = tmp_path / "portable.zip"
    bundle_path.write_bytes(b"existing")

    with pytest.raises(KnowledgeForgeError, match="already exists"):
        build_portable_bundle(EXPORT_ROOT, bundle_path)


def test_build_portable_bundle_rejects_existing_directory_destination(
    tmp_path: Path,
) -> None:
    bundle_path = tmp_path / "portable.zip"
    bundle_path.mkdir()

    with pytest.raises(KnowledgeForgeError, match="already exists"):
        build_portable_bundle(EXPORT_ROOT, bundle_path)


def test_verify_portable_bundle_rejects_directory_member(tmp_path: Path) -> None:
    bundle_path = tmp_path / "directory.zip"
    with ZipFile(bundle_path, "w") as archive:
        archive.writestr("skill/", b"")

    with pytest.raises(KnowledgeForgeError, match="unsafe ZIP member"):
        verify_portable_bundle(bundle_path)


def test_build_portable_bundle_rejects_symlink_destination(
    tmp_path: Path,
) -> None:
    target = tmp_path / "target.zip"
    target.write_bytes(b"target")
    bundle_path = tmp_path / "link.zip"
    try:
        bundle_path.symlink_to(target)
    except OSError:
        pytest.skip("Symlink creation is unavailable")

    with pytest.raises(KnowledgeForgeError, match="symbolic link"):
        build_portable_bundle(EXPORT_ROOT, bundle_path)
