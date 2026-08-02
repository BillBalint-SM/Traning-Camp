from pathlib import Path

from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.io import write_json_atomic
from knowledge_forge.models import KnowledgeModule


def build_graph(modules: list[KnowledgeModule]) -> dict[str, object]:
    identifiers = {module["metadata"]["id"] for module in modules}
    nodes: list[dict[str, object]] = []
    edges: list[dict[str, str]] = []
    edge_keys: set[tuple[str, str, str]] = set()
    for module in sorted(modules, key=lambda item: item["metadata"]["id"]):
        metadata = module["metadata"]
        identifier = metadata["id"]
        nodes.append(
            {
                "id": identifier,
                "title": metadata["title"],
                "kind": metadata["kind"],
                "maturity": metadata["maturity"],
                "confidence": metadata["confidence"],
                "tags": sorted(metadata["tags"]),
                "path": f"knowledge/{identifier}.md",
                "content_sha256": module["content_sha256"],
            }
        )
        for relation in metadata["relations"]:
            target = relation["target"]
            if target not in identifiers:
                raise KnowledgeForgeError(
                    f"Graph relation has missing target: {identifier} -> {target}"
                )
            if target == identifier:
                raise KnowledgeForgeError(f"Graph self relation is not allowed: {identifier}")
            edge_key = (identifier, relation["type"], target)
            if edge_key in edge_keys:
                raise KnowledgeForgeError(
                    f"Duplicate graph relation: {identifier} -> {target}"
                )
            edge_keys.add(edge_key)
            edges.append(
                {"source": identifier, "type": relation["type"], "target": target}
            )
    return {
        "format_version": 1,
        "nodes": nodes,
        "edges": sorted(
            edges,
            key=lambda edge: (edge["source"], edge["type"], edge["target"]),
        ),
    }


def write_graph(pack_root: Path, graph: dict[str, object]) -> None:
    write_json_atomic(pack_root / "graph" / "canonical.json", graph)
