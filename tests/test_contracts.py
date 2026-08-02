from pathlib import Path

import pytest
from knowledge_forge.contracts import validate_record
from knowledge_forge.errors import KnowledgeForgeError

SCHEMA_DIR = Path(__file__).parents[1] / "forge" / "schemas"


def test_valid_input_record_passes() -> None:
    validate_record(
        SCHEMA_DIR / "input-record.schema.json",
        {
            "role": "primary-text",
            "media_type": "application/epub+zip",
            "sha256": "a" * 64,
            "size_bytes": 10,
            "stored_path": f"inputs/{'a' * 64}.epub",
        },
        "input record",
    )


def test_unknown_property_fails() -> None:
    with pytest.raises(KnowledgeForgeError, match="unexpected"):
        validate_record(
            SCHEMA_DIR / "input-record.schema.json",
            {
                "role": "primary-text",
                "media_type": "application/epub+zip",
                "sha256": "a" * 64,
                "size_bytes": 10,
                "stored_path": f"inputs/{'a' * 64}.epub",
                "unexpected": True,
            },
            "input record",
        )
