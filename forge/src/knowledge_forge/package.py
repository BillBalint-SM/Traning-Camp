from pathlib import Path

from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.frontmatter import parse_knowledge_module
from knowledge_forge.models import KnowledgeModule


def _require_directory(path: Path, label: str) -> Path:
    if path.is_symlink():
        raise KnowledgeForgeError(f"{label} must not be a symlink: {path.name}")
    if not path.is_dir():
        raise KnowledgeForgeError(f"{label} must be a directory: {path.name}")
    return path


def _module_paths(knowledge_root: Path) -> list[Path]:
    paths: list[Path] = []
    for candidate in sorted(knowledge_root.rglob("*"), key=lambda path: path.as_posix()):
        if candidate.is_symlink():
            raise KnowledgeForgeError(
                f"Knowledge module tree must not contain symlinks: {candidate.name}"
            )
        if candidate.is_file() and candidate.suffix == ".md":
            paths.append(candidate)
    if not paths:
        raise KnowledgeForgeError("Package has no knowledge modules")
    return paths


def _require_unique_ids(modules: list[KnowledgeModule]) -> None:
    identifiers = [module["metadata"]["id"] for module in modules]
    if len(set(identifiers)) != len(identifiers):
        raise KnowledgeForgeError("Duplicate module ID")


def _require_unique_default_aliases(modules: list[KnowledgeModule]) -> None:
    seen: dict[str, str] = {}
    for module in modules:
        metadata = module["metadata"]
        if metadata["maturity"] == "deprecated":
            continue
        for alias in metadata["aliases"]:
            normalized = alias.casefold()
            existing = seen.get(normalized)
            if existing is not None and existing != metadata["id"]:
                raise KnowledgeForgeError(
                    f"Ambiguous alias: {alias} matches {existing} and {metadata['id']}"
                )
            seen[normalized] = metadata["id"]


def _require_valid_relation_targets(modules: list[KnowledgeModule]) -> None:
    identifiers = {module["metadata"]["id"] for module in modules}
    for module in modules:
        identifier = module["metadata"]["id"]
        for relation in module["metadata"]["relations"]:
            target = relation["target"]
            if target == identifier:
                raise KnowledgeForgeError(f"Self relation is not allowed: {identifier}")
            if target not in identifiers:
                raise KnowledgeForgeError(
                    f"Relation has missing target: {identifier} -> {target}"
                )


def validate_module_set(modules: list[KnowledgeModule]) -> None:
    if not modules:
        raise KnowledgeForgeError("Package has no knowledge modules")
    _require_unique_ids(modules)
    _require_unique_default_aliases(modules)
    _require_valid_relation_targets(modules)


def discover_modules(pack_root: Path, schema_path: Path) -> list[KnowledgeModule]:
    knowledge_root = _require_directory(pack_root / "knowledge", "Knowledge root")
    modules: list[KnowledgeModule] = []
    for module_path in _module_paths(knowledge_root):
        module = parse_knowledge_module(module_path, schema_path)
        if module_path.stem != module["metadata"]["id"]:
            raise KnowledgeForgeError(
                f"Knowledge module filename must match its ID: {module_path.name}"
            )
        modules.append(module)
    validate_module_set(modules)
    return sorted(modules, key=lambda module: module["metadata"]["id"])
