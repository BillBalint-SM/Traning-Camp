import re
from pathlib import Path
from typing import cast

import yaml

from knowledge_forge.contracts import validate_record
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.hashing import sha256_file
from knowledge_forge.models import KnowledgeModule, KnowledgeModuleMetadata

REQUIRED_SECTIONS = (
    "Lényeg",
    "Miért működik",
    "Mikor alkalmazd",
    "Mikor ne alkalmazd",
    "Döntési szabály",
    "Hibamódok",
    "Kapcsolatok",
    "Ellenőrzés",
)

_HEADING_PATTERN = re.compile(r"^## ([^\r\n]+)\s*$", re.MULTILINE)


def _split_front_matter(raw: str, module_path: Path) -> tuple[str, str]:
    lines = raw.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise KnowledgeForgeError(
            f"Module must start with a front matter delimiter: {module_path.name}"
        )
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            metadata = "".join(lines[1:index])
            body = "".join(lines[index + 1 :])
            if not metadata:
                raise KnowledgeForgeError(
                    f"Module front matter must not be empty: {module_path.name}"
                )
            if not body:
                raise KnowledgeForgeError(
                    f"Module body must not be empty: {module_path.name}"
                )
            return metadata, body
    raise KnowledgeForgeError(
        f"Module front matter has no closing delimiter: {module_path.name}"
    )


def _require_sections(body: str, module_path: Path) -> None:
    headings = tuple(match.group(1) for match in _HEADING_PATTERN.finditer(body))
    missing = [section for section in REQUIRED_SECTIONS if section not in headings]
    if missing:
        raise KnowledgeForgeError(
            "Module is missing required sections: "
            + ", ".join(missing)
            + f": {module_path.name}"
        )
    if headings != REQUIRED_SECTIONS:
        raise KnowledgeForgeError(
            f"Module sections must match the required order exactly: {module_path.name}"
        )


def parse_knowledge_module(module_path: Path, schema_path: Path) -> KnowledgeModule:
    raw = module_path.read_text(encoding="utf-8")
    metadata_text, body = _split_front_matter(raw, module_path)
    try:
        metadata = yaml.safe_load(metadata_text)
    except yaml.YAMLError as error:
        raise KnowledgeForgeError(
            f"Module front matter is invalid YAML: {module_path.name}"
        ) from error
    if not isinstance(metadata, dict):
        raise KnowledgeForgeError(
            f"Module front matter must be an object: {module_path.name}"
        )
    validate_record(schema_path, metadata, f"knowledge module {module_path.name}")
    _require_sections(body, module_path)
    return {
        "metadata": cast(KnowledgeModuleMetadata, metadata),
        "body": body,
        "content_sha256": sha256_file(module_path, 1024),
    }
