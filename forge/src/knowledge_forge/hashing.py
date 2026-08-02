import hashlib
from pathlib import Path

from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.paths import require_regular_file


def sha256_file(path: Path, chunk_size: int) -> str:
    require_regular_file(path, "hash input")
    if chunk_size <= 0:
        raise KnowledgeForgeError("Hash chunk size must be positive")
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
