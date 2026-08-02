import hashlib
from pathlib import Path

import pytest
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.hashing import sha256_file
from knowledge_forge.io import (
    canonical_json_bytes,
    read_json,
    read_jsonl,
    write_json_atomic,
    write_jsonl_atomic,
)


def test_canonical_json_is_sorted_utf8_and_newline_terminated() -> None:
    payload = {"z": "árvíz", "a": 1}
    assert canonical_json_bytes(payload) == '{"a":1,"z":"árvíz"}\n'.encode()


def test_json_and_jsonl_round_trip(tmp_path: Path) -> None:
    json_path = tmp_path / "record.json"
    jsonl_path = tmp_path / "records.jsonl"
    write_json_atomic(json_path, {"value": 2})
    write_jsonl_atomic(jsonl_path, [{"id": "a"}, {"id": "b"}])
    assert read_json(json_path) == {"value": 2}
    assert read_jsonl(jsonl_path) == [{"id": "a"}, {"id": "b"}]


def test_sha256_file_matches_hashlib(tmp_path: Path) -> None:
    path = tmp_path / "payload.bin"
    path.write_bytes(b"knowledge-forge")
    assert sha256_file(path, 4) == hashlib.sha256(b"knowledge-forge").hexdigest()


def test_sha256_file_rejects_non_positive_chunk_size(tmp_path: Path) -> None:
    path = tmp_path / "payload.bin"
    path.write_bytes(b"knowledge-forge")
    with pytest.raises(KnowledgeForgeError, match="chunk size must be positive"):
        sha256_file(path, 0)
