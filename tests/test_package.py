from pathlib import Path

import pytest
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.package import discover_modules, validate_module_set

PACK_ROOT = Path(__file__).parents[1] / "pack"
SCHEMA_PATH = (
    Path(__file__).parents[1]
    / "forge"
    / "schemas"
    / "knowledge-module.schema.json"
)
EXPECTED_IDS = {
    "principle.agent-operating-model",
    "principle.context-is-finite",
    "pattern.context-budget-allocation",
    "pattern.context-compression",
    "decision-guide.memory-vs-retrieval",
    "procedure.user-memory-lifecycle",
    "procedure.tool-contract-design",
    "checklist.tool-safety-boundary",
    "pattern.tool-discovery",
    "procedure.agent-evaluation-loop",
    "decision-guide.sft-or-rl",
    "pattern.experience-driven-improvement",
    "concept.multimodal-interaction-boundary",
    "pattern.multi-agent-context-boundaries",
    "failure-mode.unvalidated-autonomy",
}


def _module(identifier: str, alias: str, target: str) -> dict[str, object]:
    return {
        "metadata": {
            "id": identifier,
            "title": identifier,
            "kind": "principle",
            "maturity": "validated",
            "confidence": "high",
            "language": "hu",
            "tags": ["teszt"],
            "aliases": [alias],
            "relations": [{"type": "supports", "target": target}],
        },
        "body": "teszt",
        "content_sha256": "0" * 64,
    }


def test_discover_modules_returns_the_curated_v0_set() -> None:
    modules = discover_modules(PACK_ROOT, SCHEMA_PATH)

    assert {module["metadata"]["id"] for module in modules} == EXPECTED_IDS
    assert all(module["metadata"]["language"] == "hu" for module in modules)


def test_validate_module_set_rejects_duplicate_aliases() -> None:
    modules = [
        _module("principle.first", "azonos", "principle.second"),
        _module("principle.second", "azonos", "principle.first"),
    ]

    with pytest.raises(KnowledgeForgeError, match="Ambiguous alias"):
        validate_module_set(modules)


def test_validate_module_set_rejects_self_relation() -> None:
    modules = [_module("principle.first", "első", "principle.first")]

    with pytest.raises(KnowledgeForgeError, match="Self relation"):
        validate_module_set(modules)


def test_validate_module_set_rejects_missing_relation_target() -> None:
    modules = [_module("principle.first", "első", "principle.missing")]

    with pytest.raises(KnowledgeForgeError, match="missing target"):
        validate_module_set(modules)
