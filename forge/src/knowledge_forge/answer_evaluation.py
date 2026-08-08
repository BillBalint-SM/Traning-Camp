import re
from pathlib import Path

from knowledge_forge.contracts import validate_record
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.hashing import sha256_bytes
from knowledge_forge.io import canonical_json_bytes, write_json_atomic
from knowledge_forge.measurement import validate_context_trace

_SCHEMA_PATH = (
    Path(__file__).parents[2] / "schemas" / "answer-evaluation-request.schema.json"
)
_IDENTIFIER_PATTERN = re.compile(r"^[a-z][a-z0-9.-]*$")


def _require_identifier(value: object, label: str) -> str:
    if not isinstance(value, str) or not _IDENTIFIER_PATTERN.fullmatch(value):
        raise KnowledgeForgeError(f"Answer evaluation request {label} is invalid")
    return value


def _require_identifier_list(value: object, label: str) -> list[str]:
    if not isinstance(value, list):
        raise KnowledgeForgeError(f"Answer evaluation request {label} must be an array")
    identifiers = [_require_identifier(item, label) for item in value]
    if identifiers != sorted(identifiers):
        raise KnowledgeForgeError(f"Answer evaluation request {label} must be sorted")
    if len(identifiers) != len(set(identifiers)):
        raise KnowledgeForgeError(
            f"Answer evaluation request {label} contains duplicates"
        )
    return identifiers


def _require_digest(value: object, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise KnowledgeForgeError(f"Answer evaluation request {label} is invalid")
    return value


def build_answer_evaluation_request(
    case_id: str,
    query: str,
    strategy_id: str,
    context_trace: dict[str, object],
    expected_module_ids: list[str],
) -> dict[str, object]:
    _require_identifier(case_id, "case ID")
    _require_identifier(strategy_id, "strategy ID")
    if not isinstance(query, str) or not query:
        raise KnowledgeForgeError("Answer evaluation request query must be a non-empty string")
    validate_context_trace(context_trace)
    query_sha256 = sha256_bytes(query.encode("utf-8"))
    if context_trace.get("query_sha256") != query_sha256:
        raise KnowledgeForgeError("Answer evaluation request query does not match context trace")
    expected_ids = _require_identifier_list(expected_module_ids, "expected module IDs")
    request_without_digest: dict[str, object] = {
        "format_version": 1,
        "kind": "answer-evaluation-request",
        "case_id": case_id,
        "query_sha256": query_sha256,
        "export_sha256": _require_digest(
            context_trace.get("export_sha256"), "context trace export digest"
        ),
        "strategy_id": strategy_id,
        "context_trace_sha256": _require_digest(
            context_trace.get("trace_sha256"), "context trace digest"
        ),
        "expected_module_ids": expected_ids,
    }
    request = dict(request_without_digest)
    request["request_sha256"] = sha256_bytes(
        canonical_json_bytes(request_without_digest)
    )
    validate_answer_evaluation_request(request)
    return request


def validate_answer_evaluation_request(request: dict[str, object]) -> None:
    if not isinstance(request, dict):
        raise KnowledgeForgeError("Answer evaluation request must be an object")
    validate_record(_SCHEMA_PATH, request, "answer evaluation request")
    _require_identifier(request.get("case_id"), "case ID")
    _require_identifier(request.get("strategy_id"), "strategy ID")
    _require_digest(request.get("query_sha256"), "query digest")
    _require_digest(request.get("export_sha256"), "export digest")
    _require_digest(request.get("context_trace_sha256"), "context trace digest")
    _require_identifier_list(request.get("expected_module_ids"), "expected module IDs")
    claimed_digest = _require_digest(request.get("request_sha256"), "request digest")
    without_digest = {key: value for key, value in request.items() if key != "request_sha256"}
    if sha256_bytes(canonical_json_bytes(without_digest)) != claimed_digest:
        raise KnowledgeForgeError("Answer evaluation request digest mismatch")


def _assert_safe_output_path(request_path: Path) -> None:
    if request_path.is_symlink():
        raise KnowledgeForgeError(
            "Answer evaluation request output must not be a symbolic link: "
            f"{request_path.name}"
        )
    for parent in request_path.parents:
        if parent == parent.parent:
            break
        if parent.exists() and parent.is_symlink():
            raise KnowledgeForgeError(
                "Answer evaluation request output parent must not be a symbolic link: "
                f"{parent.name}"
            )


def write_answer_evaluation_request(
    request_path: Path, request: dict[str, object]
) -> None:
    validate_answer_evaluation_request(request)
    _assert_safe_output_path(request_path)
    if request_path.exists():
        raise KnowledgeForgeError(
            f"Answer evaluation request output already exists: {request_path.name}"
        )
    write_json_atomic(request_path, request)
