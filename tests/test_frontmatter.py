from pathlib import Path

import pytest
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.frontmatter import REQUIRED_SECTIONS, parse_knowledge_module
from knowledge_forge.hashing import sha256_file

SCHEMA_PATH = (
    Path(__file__).parents[1]
    / "forge"
    / "schemas"
    / "knowledge-module.schema.json"
)


def _module_text(metadata: str, body: str) -> str:
    return f"---\n{metadata}---\n\n{body}"


def _required_body() -> str:
    return "\n\n".join(
        f"## {section}\n\nEllenőrizhető, önálló állítás." for section in REQUIRED_SECTIONS
    ) + "\n"


def _metadata(extra: str) -> str:
    return (
        "id: principle.example\n"
        "title: Példa elv\n"
        "kind: principle\n"
        "maturity: validated\n"
        "confidence: high\n"
        "language: hu\n"
        "tags:\n"
        "  - példa\n"
        "aliases:\n"
        "  - example principle\n"
        "relations:\n"
        "  - type: supports\n"
        "    target: principle.other\n"
        f"{extra}"
    )


def test_parse_knowledge_module_accepts_safe_yaml_and_required_sections(
    tmp_path: Path,
) -> None:
    module_path = tmp_path / "principle.example.md"
    module_path.write_text(
        _module_text(_metadata(""), _required_body()), encoding="utf-8", newline="\n"
    )

    module = parse_knowledge_module(module_path, SCHEMA_PATH)

    assert module["metadata"]["id"] == "principle.example"
    assert module["content_sha256"] == sha256_file(module_path, 1024)
    assert module["body"].endswith("\n")


def test_parse_knowledge_module_rejects_missing_required_section(tmp_path: Path) -> None:
    module_path = tmp_path / "principle.example.md"
    body = _required_body().replace("## Ellenőrzés\n\nEllenőrizhető, önálló állítás.\n", "")
    module_path.write_text(_module_text(_metadata(""), body), encoding="utf-8")

    with pytest.raises(KnowledgeForgeError, match="missing required sections"):
        parse_knowledge_module(module_path, SCHEMA_PATH)


def test_parse_knowledge_module_rejects_non_object_front_matter(tmp_path: Path) -> None:
    module_path = tmp_path / "principle.example.md"
    module_path.write_text(_module_text("nem-objektum\n", _required_body()), encoding="utf-8")

    with pytest.raises(KnowledgeForgeError, match="front matter must be an object"):
        parse_knowledge_module(module_path, SCHEMA_PATH)


def test_parse_knowledge_module_rejects_unknown_front_matter_key(tmp_path: Path) -> None:
    module_path = tmp_path / "principle.example.md"
    module_path.write_text(
        _module_text(_metadata("unexpected: value\n"), _required_body()),
        encoding="utf-8",
    )

    with pytest.raises(KnowledgeForgeError, match="Schema validation failed"):
        parse_knowledge_module(module_path, SCHEMA_PATH)
