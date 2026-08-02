from pathlib import Path, PurePosixPath
from typing import cast

from knowledge_forge.contracts import validate_record
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.hashing import sha256_bytes, sha256_file
from knowledge_forge.io import canonical_json_bytes, read_json, write_json_atomic

_ALLOWED_ROOTS = {"knowledge", "indexes", "graph", "skills"}
_MANIFEST_NAME = "manifest.json"


def _require_pack_root(pack_root: Path) -> None:
    if pack_root.is_symlink():
        raise KnowledgeForgeError("Package root must not be a symlink")
    if not pack_root.is_dir():
        raise KnowledgeForgeError("Package root must be a directory")


def _safe_member_path(relative_path: str) -> bool:
    if "\\" in relative_path:
        return False
    candidate = PurePosixPath(relative_path)
    if candidate.is_absolute() or ".." in candidate.parts or not candidate.parts:
        return False
    if len(candidate.parts) == 1:
        return relative_path == _MANIFEST_NAME
    return candidate.parts[0] in _ALLOWED_ROOTS


def _package_files(pack_root: Path) -> list[str]:
    _require_pack_root(pack_root)
    files: list[str] = []
    casefolded: set[str] = set()
    for candidate in sorted(pack_root.rglob("*"), key=lambda path: path.as_posix()):
        if candidate.is_symlink():
            raise KnowledgeForgeError(
                f"Package tree must not contain symlinks: {candidate.name}"
            )
        if not candidate.is_file():
            continue
        relative_path = candidate.relative_to(pack_root).as_posix()
        if not _safe_member_path(relative_path):
            raise KnowledgeForgeError(f"Forbidden package path: {relative_path}")
        normalized = relative_path.casefold()
        if normalized in casefolded:
            raise KnowledgeForgeError(f"Case-colliding package path: {relative_path}")
        casefolded.add(normalized)
        if relative_path != _MANIFEST_NAME:
            files.append(relative_path)
    return sorted(files)


def build_manifest(pack_root: Path) -> dict[str, object]:
    files = _package_files(pack_root)
    inventory = [
        {"path": relative_path, "sha256": sha256_file(pack_root / relative_path, 1024)}
        for relative_path in files
    ]
    return {
        "format_version": 1,
        "files": inventory,
        "package_sha256": sha256_bytes(canonical_json_bytes(inventory)),
    }


def write_manifest(pack_root: Path) -> dict[str, object]:
    manifest = build_manifest(pack_root)
    write_json_atomic(pack_root / _MANIFEST_NAME, manifest)
    return manifest


def _manifest_inventory(manifest: dict[str, object]) -> list[dict[str, str]]:
    files = cast(list[dict[str, str]], manifest["files"])
    declared_paths = [entry["path"] for entry in files]
    if declared_paths != sorted(declared_paths):
        raise KnowledgeForgeError("Manifest file inventory must be sorted")
    if len(set(declared_paths)) != len(declared_paths):
        raise KnowledgeForgeError("Manifest contains duplicate file paths")
    for relative_path in declared_paths:
        if not _safe_member_path(relative_path) or relative_path == _MANIFEST_NAME:
            raise KnowledgeForgeError("Manifest contains an unsafe package path")
    return files


def validate_manifest(pack_root: Path, schema_path: Path) -> dict[str, object]:
    manifest_path = pack_root / _MANIFEST_NAME
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise KnowledgeForgeError("Package manifest must be a regular file")
    manifest = read_json(manifest_path)
    validate_record(schema_path, manifest, "package manifest")
    if not isinstance(manifest, dict):
        raise KnowledgeForgeError("Package manifest root must be an object")
    inventory = _manifest_inventory(manifest)
    declared_paths = [entry["path"] for entry in inventory]
    actual_paths = _package_files(pack_root)
    undeclared = sorted(set(actual_paths) - set(declared_paths))
    if undeclared:
        raise KnowledgeForgeError(f"Undeclared package file: {undeclared[0]}")
    missing = sorted(set(declared_paths) - set(actual_paths))
    if missing:
        raise KnowledgeForgeError(f"Manifest declares missing package file: {missing[0]}")
    for entry in inventory:
        actual_hash = sha256_file(pack_root / entry["path"], 1024)
        if actual_hash != entry["sha256"]:
            raise KnowledgeForgeError(f"Stale manifest hash: {entry['path']}")
    expected_digest = sha256_bytes(canonical_json_bytes(inventory))
    if manifest["package_sha256"] != expected_digest:
        raise KnowledgeForgeError("Stale package digest")
    return manifest
