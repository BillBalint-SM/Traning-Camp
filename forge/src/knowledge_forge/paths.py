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


def require_regular_file(path: Path, label: str) -> None:
    if path.is_symlink():
        raise KnowledgeForgeError(f"{label} must not be a symbolic link: {path.name}")
    if not path.is_file():
        raise KnowledgeForgeError(f"{label} is not a regular file: {path.name}")
