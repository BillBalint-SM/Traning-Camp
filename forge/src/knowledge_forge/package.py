from pathlib import Path

from knowledge_forge.contracts import validate_record
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.frontmatter import parse_knowledge_module
from knowledge_forge.graph import build_graph
from knowledge_forge.indexes import build_indexes, load_areas
from knowledge_forge.io import read_json
from knowledge_forge.leakage import check_content_neutrality
from knowledge_forge.manifest import validate_manifest
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


def _require_exact_json(
    path: Path, expected: object, schema_path: Path, label: str
) -> None:
    actual = read_json(path)
    validate_record(schema_path, actual, label)
    if actual != expected:
        raise KnowledgeForgeError(f"Package artifact is stale: {path.name}")


def _validate_skill(pack_root: Path) -> None:
    skill_path = pack_root / "skills" / "SKILL.md"
    if skill_path.is_symlink() or not skill_path.is_file():
        raise KnowledgeForgeError("Package routing skill must be a regular file")
    content = skill_path.read_text(encoding="utf-8")
    forbidden_sections = (
        "## Lényeg",
        "## Miért működik",
        "## Mikor alkalmazd",
        "## Mikor ne alkalmazd",
        "## Döntési szabály",
        "## Hibamódok",
        "## Kapcsolatok",
        "## Ellenőrzés",
    )
    if any(section in content for section in forbidden_sections):
        raise KnowledgeForgeError("Routing skill must not embed module body sections")


def validate_package(
    pack_root: Path, schema_dir: Path, markers: list[str]
) -> dict[str, object]:
    manifest = validate_manifest(pack_root, schema_dir / "package-manifest.schema.json")
    manifest_files = [entry["path"] for entry in manifest["files"]]
    check_content_neutrality(pack_root, manifest_files, markers)
    modules = discover_modules(pack_root, schema_dir / "knowledge-module.schema.json")
    areas = load_areas(pack_root / "indexes" / "areas.json")
    indexes = build_indexes(modules, areas)
    _require_exact_json(
        pack_root / "indexes" / "l0.json",
        indexes["l0"],
        schema_dir / "package-index.schema.json",
        "L0 package index",
    )
    for area_id, index in indexes["l1"].items():
        _require_exact_json(
            pack_root / "indexes" / "l1" / f"{area_id}.json",
            index,
            schema_dir / "package-index.schema.json",
            f"L1 package index {area_id}",
        )
    graph = build_graph(modules)
    _require_exact_json(
        pack_root / "graph" / "canonical.json",
        graph,
        schema_dir / "canonical-graph.schema.json",
        "canonical package graph",
    )
    _validate_skill(pack_root)
    return manifest
