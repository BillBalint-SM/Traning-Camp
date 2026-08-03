import os
import re
import stat
import tempfile
from pathlib import Path, PurePosixPath
from typing import cast
from zipfile import ZIP_STORED, BadZipFile, ZipFile, ZipInfo

from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.io import read_json
from knowledge_forge.paths import require_regular_file
from knowledge_forge.portability import verify_portable_export

_ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
_REGULAR_FILE_MODE = stat.S_IFREG | 0o644
_DRIVE_PREFIX = re.compile(r"^[A-Za-z]:")


def _safe_zip_member(name: str) -> bool:
    if not name or "\\" in name or _DRIVE_PREFIX.match(name):
        return False
    candidate = PurePosixPath(name)
    return bool(candidate.parts) and not candidate.is_absolute() and ".." not in candidate.parts


def _archive_members(manifest: dict[str, object]) -> list[str]:
    entries = manifest.get("files")
    if not isinstance(entries, list):
        raise KnowledgeForgeError("Portable export manifest files must be an array")
    members: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise KnowledgeForgeError("Portable export file entry must be an object")
        relative = entry.get("path")
        if not isinstance(relative, str) or not _safe_zip_member(relative):
            raise KnowledgeForgeError("Portable export file path is unsafe")
        if relative in members:
            raise KnowledgeForgeError(f"Portable export file is duplicated: {relative}")
        members.append(relative)
    members.append("export.json")
    return sorted(members)


def _zip_info(member: str) -> ZipInfo:
    info = ZipInfo(member, date_time=_ZIP_TIMESTAMP)
    info.compress_type = ZIP_STORED
    info.create_system = 3
    info.external_attr = _REGULAR_FILE_MODE << 16
    return info


def _validate_destination(bundle_path: Path) -> None:
    if bundle_path.is_symlink():
        raise KnowledgeForgeError(
            f"Portable bundle destination must not be a symbolic link: {bundle_path.name}"
        )
    if bundle_path.exists():
        raise KnowledgeForgeError(
            f"Portable bundle destination already exists: {bundle_path.name}"
        )
    current = bundle_path.parent
    while current != current.parent:
        if current.is_symlink():
            raise KnowledgeForgeError(
                f"Portable bundle destination must not use a symbolic link: {current.name}"
            )
        current = current.parent
    bundle_path.parent.mkdir(parents=True, exist_ok=True)
    if bundle_path.parent.is_symlink():
        raise KnowledgeForgeError(
            f"Portable bundle destination must not use a symbolic link: {bundle_path.parent.name}"
        )


def _source_bytes(export_root: Path, member: str) -> bytes:
    source = export_root / member
    if source.is_symlink():
        raise KnowledgeForgeError(
            f"Portable export source must not be a symbolic link: {member}"
        )
    if not source.is_file():
        raise KnowledgeForgeError(f"Portable export source is not a regular file: {member}")
    return source.read_bytes()


def _write_bundle(
    export_root: Path,
    bundle_path: Path,
    members: list[str],
) -> None:
    _validate_destination(bundle_path)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=bundle_path.parent, delete=False) as handle:
            temporary_path = Path(handle.name)
        with ZipFile(temporary_path, "w", ZIP_STORED) as archive:
            for member in members:
                archive.writestr(_zip_info(member), _source_bytes(export_root, member))
        if bundle_path.is_symlink():
            raise KnowledgeForgeError(
                f"Portable bundle destination must not be a symbolic link: {bundle_path.name}"
            )
        if bundle_path.exists():
            raise KnowledgeForgeError(
                f"Portable bundle destination already exists: {bundle_path.name}"
            )
        os.replace(temporary_path, bundle_path)
        temporary_path = None
    except KnowledgeForgeError:
        raise
    except OSError as error:
        raise KnowledgeForgeError(
            f"Cannot write portable bundle: {bundle_path.name}"
        ) from error
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def _verify_member_metadata(info: ZipInfo) -> None:
    mode = info.external_attr >> 16
    if (
        not _safe_zip_member(info.filename)
        or info.is_dir()
        or info.create_system != 3
        or info.compress_type != ZIP_STORED
        or info.date_time != _ZIP_TIMESTAMP
        or mode != _REGULAR_FILE_MODE
        or info.extra
        or info.comment
    ):
        raise KnowledgeForgeError("Portable bundle contains an unsafe ZIP member")


def verify_portable_bundle(bundle_path: Path) -> dict[str, object]:
    require_regular_file(bundle_path, "Portable bundle")
    try:
        with ZipFile(bundle_path) as archive:
            infos = archive.infolist()
            names = [info.filename for info in infos]
            if len(names) != len(set(names)):
                raise KnowledgeForgeError("Portable bundle contains duplicate ZIP members")
            if names != sorted(names):
                raise KnowledgeForgeError("Portable bundle members are not sorted")
            for info in infos:
                _verify_member_metadata(info)
            with tempfile.TemporaryDirectory(prefix="portable-bundle-") as temporary_root:
                extracted_root = Path(temporary_root)
                for info in infos:
                    destination = extracted_root / PurePosixPath(info.filename)
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_bytes(archive.read(info))
                manifest_payload = read_json(extracted_root / "export.json")
                if not isinstance(manifest_payload, dict):
                    raise KnowledgeForgeError(
                        "Portable bundle manifest must be an object"
                    )
                manifest = cast(dict[str, object], manifest_payload)
                if names != _archive_members(manifest):
                    raise KnowledgeForgeError(
                        "Portable bundle inventory does not match manifest"
                    )
                manifest = verify_portable_export(extracted_root)
                return manifest
    except BadZipFile as error:
        raise KnowledgeForgeError("Cannot read portable bundle archive") from error
    except OSError as error:
        raise KnowledgeForgeError(
            f"Cannot read portable bundle: {bundle_path.name}"
        ) from error


def build_portable_bundle(
    export_root: Path,
    bundle_path: Path,
) -> dict[str, object]:
    if export_root.is_symlink() or not export_root.is_dir():
        raise KnowledgeForgeError("Portable export input must be a directory")
    manifest = verify_portable_export(export_root)
    members = _archive_members(manifest)
    _write_bundle(export_root, bundle_path, members)
    return verify_portable_bundle(bundle_path)
