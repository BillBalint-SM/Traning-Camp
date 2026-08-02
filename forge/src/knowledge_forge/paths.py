import os
from pathlib import Path

from knowledge_forge.errors import KnowledgeForgeError


def resolve_within(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KnowledgeForgeError(f"Path must be relative: {relative_path.name}")
    resolved_root = root.resolve()
    resolved_path = (resolved_root / relative_path).resolve()
    if not resolved_path.is_relative_to(resolved_root):
        raise KnowledgeForgeError(
            f"Path escapes workspace root: {relative_path.as_posix()}"
        )
    return resolved_path


def resolve_regular_within(root: Path, relative_path: Path, label: str) -> Path:
    if relative_path.is_absolute():
        raise KnowledgeForgeError(f"Path must be relative: {relative_path.name}")
    resolved_root = root.resolve()
    candidate = Path(os.path.abspath(resolved_root / relative_path))
    resolved_target = candidate.resolve()
    if not resolved_target.is_relative_to(resolved_root):
        raise KnowledgeForgeError(
            f"Path escapes workspace root: {relative_path.as_posix()}"
        )
    current = resolved_root
    for part in relative_path.parts:
        current /= part
        if current.is_symlink():
            raise KnowledgeForgeError(
                f"{label} must not be a symbolic link: {relative_path.name}"
            )
    require_regular_file(candidate, label)
    return candidate


def resolve_new_directory_within(
    root: Path,
    relative_path: Path,
    required_parent: Path,
    label: str,
) -> Path:
    if relative_path.is_absolute():
        raise KnowledgeForgeError(f"Path must be relative: {relative_path.name}")
    resolved_root = root.resolve()
    candidate = Path(os.path.abspath(resolved_root / relative_path))
    if not candidate.is_relative_to(resolved_root):
        raise KnowledgeForgeError(
            f"Path escapes workspace root: {relative_path.as_posix()}"
        )
    allowed_root = Path(os.path.abspath(resolved_root / required_parent))
    if candidate == allowed_root or not candidate.is_relative_to(allowed_root):
        raise KnowledgeForgeError(
            f"{label} must be inside {required_parent.as_posix()}"
        )
    current = resolved_root
    for part in relative_path.parts:
        current /= part
        if current.is_symlink():
            raise KnowledgeForgeError(
                f"{label} must not contain a symbolic link: {current.name}"
            )
    if candidate.exists():
        raise KnowledgeForgeError(f"{label} already exists: {candidate.name}")
    if not candidate.resolve().is_relative_to(allowed_root.resolve()):
        raise KnowledgeForgeError(
            f"Path escapes workspace root: {relative_path.as_posix()}"
        )
    return candidate


def require_regular_file(path: Path, label: str) -> None:
    if path.is_symlink():
        raise KnowledgeForgeError(f"{label} must not be a symbolic link: {path.name}")
    if not path.is_file():
        raise KnowledgeForgeError(f"{label} is not a regular file: {path.name}")
