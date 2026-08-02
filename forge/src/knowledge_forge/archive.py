import os
import stat
import tempfile
from pathlib import Path, PurePosixPath
from zipfile import ZIP_STORED, BadZipFile, ZipFile, ZipInfo

from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.package import validate_package

_ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def _safe_zip_member(name: str) -> bool:
    if "\\" in name:
        return False
    candidate = PurePosixPath(name)
    return bool(candidate.parts) and not candidate.is_absolute() and ".." not in candidate.parts


def _archive_members(manifest: dict[str, object]) -> list[str]:
    files = manifest["files"]
    if not isinstance(files, list):
        raise KnowledgeForgeError("Package manifest files must be an array")
    return sorted([entry["path"] for entry in files] + ["manifest.json"])


def _zip_info(member: str) -> ZipInfo:
    info = ZipInfo(member, date_time=_ZIP_TIMESTAMP)
    info.compress_type = ZIP_STORED
    info.create_system = 3
    info.external_attr = (stat.S_IFREG | 0o644) << 16
    return info


def _write_archive(pack_root: Path, archive_path: Path, members: list[str]) -> None:
    if archive_path.is_symlink() or archive_path.parent.is_symlink():
        raise KnowledgeForgeError("Archive destination must not use symlinks")
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=archive_path.parent, delete=False) as handle:
            temporary_path = Path(handle.name)
        with ZipFile(temporary_path, "w", ZIP_STORED) as archive:
            for member in members:
                archive.writestr(_zip_info(member), (pack_root / member).read_bytes())
        os.replace(temporary_path, archive_path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def verify_archive(archive_path: Path, schema_dir: Path, markers: list[str]) -> None:
    try:
        with ZipFile(archive_path) as archive:
            infos = archive.infolist()
            names = [info.filename for info in infos]
            if len(names) != len(set(names)):
                raise KnowledgeForgeError("Archive contains duplicate ZIP members")
            for info in infos:
                mode = info.external_attr >> 16
                if (
                    not _safe_zip_member(info.filename)
                    or info.is_dir()
                    or stat.S_IFMT(mode) == stat.S_IFLNK
                ):
                    raise KnowledgeForgeError("Archive contains an unsafe ZIP member")
            with tempfile.TemporaryDirectory() as temporary_directory:
                package_root = Path(temporary_directory)
                for info in infos:
                    destination = package_root / PurePosixPath(info.filename)
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_bytes(archive.read(info))
                manifest = validate_package(package_root, schema_dir, markers)
                if names != _archive_members(manifest):
                    raise KnowledgeForgeError("Archive inventory does not match manifest")
    except BadZipFile as error:
        raise KnowledgeForgeError("Cannot read package archive") from error


def build_archive(
    pack_root: Path, archive_path: Path, schema_dir: Path, markers: list[str]
) -> None:
    manifest = validate_package(pack_root, schema_dir, markers)
    _write_archive(pack_root, archive_path, _archive_members(manifest))
    verify_archive(archive_path, schema_dir, markers)
