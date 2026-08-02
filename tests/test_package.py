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
    "checklist.agent-observability",
    "checklist.agent-task-contract",
    "checklist.prompt-injection-boundary",
    "checklist.shared-state-concurrency-control",
    "principle.agent-operating-model",
    "principle.context-is-finite",
    "principle.environment-data-before-algorithm",
    "principle.harness-engineering",
    "principle.planning-control-separation",
    "pattern.context-budget-allocation",
    "pattern.context-compression",
    "pattern.agent-status-representation",
    "pattern.dynamic-skill-loading",
    "pattern.event-driven-agent-execution",
    "pattern.fast-slow-interaction-loop",
    "pattern.hierarchical-context-compression",
    "decision-guide.memory-vs-retrieval",
    "decision-guide.metric-selection",
    "decision-guide.multi-agent-topology-selection",
    "decision-guide.retrieval-strategy-selection",
    "decision-guide.tool-granularity",
    "decision-guide.voice-architecture-selection",
    "decision-guide.workflow-or-autonomy",
    "concept.context-cache-architecture",
    "concept.structured-knowledge-index",
    "concept.tool-capability-taxonomy",
    "procedure.user-memory-lifecycle",
    "procedure.ablation-and-experiment-loop",
    "procedure.async-interruption-handling",
    "procedure.continual-improvement-release-loop",
    "procedure.evaluation-environment-design",
    "procedure.gui-action-grounding",
    "procedure.multi-agent-handoff-contract",
    "procedure.retrieval-pipeline-design",
    "procedure.system-prompt-architecture",
    "procedure.tool-contract-design",
    "checklist.tool-safety-boundary",
    "checklist.tool-result-verification",
    "pattern.tool-discovery",
    "pattern.react-observe-act-loop",
    "procedure.agent-evaluation-loop",
    "decision-guide.sft-or-rl",
    "pattern.experience-driven-improvement",
    "pattern.sft-rl-learning-boundary",
    "pattern.task-distribution-coverage",
    "concept.multimodal-interaction-boundary",
    "pattern.multi-agent-context-boundaries",
    "failure-mode.model-only-system-design",
    "failure-mode.multi-agent-error-amplification",
    "failure-mode.unsafe-tool-expansion",
    "failure-mode.unvalidated-autonomy",
    "checklist.harness-function-coverage",
    "checklist.isolated-tool-execution",
    "checklist.knowledge-freshness-governance",
    "checklist.memory-privacy-sanitization",
    "concept.api-message-context-model",
    "concept.context-isolation-strategy",
    "concept.dense-retrieval",
    "concept.observation-action-interface",
    "concept.perception-execution-collaboration-tools",
    "concept.sparse-retrieval",
    "decision-guide.agent-model-selection",
    "decision-guide.few-shot-example-selection",
    "decision-guide.memory-capability-evaluation",
    "decision-guide.memory-representation-selection",
    "decision-guide.multimodal-information-processing",
    "decision-guide.process-instructions-or-rule-stack",
    "decision-guide.status-update-placement",
    "decision-guide.tool-or-skill-executor",
    "pattern.agentic-retrieval-control",
    "pattern.contextual-retrieval",
    "pattern.editable-context-notes",
    "pattern.filesystem-knowledge-organization",
    "pattern.memory-hierarchy",
    "principle.tool-interface-fidelity",
    "procedure.business-rule-compilation",
    "procedure.cache-stable-context-layout",
    "procedure.document-chunking-strategy",
    "procedure.guardrail-design",
    "procedure.human-escalation-design",
    "procedure.hybrid-retrieval-fusion",
    "procedure.mcp-tool-selection",
    "procedure.memory-consolidation",
    "procedure.proactive-tool-discovery",
    "procedure.prompt-structure-design",
    "procedure.status-signal-design",
    "procedure.user-communication-during-async-execution",
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


def test_discover_modules_returns_the_curated_v1_set() -> None:
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
