from pathlib import Path

import pytest
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.paths import require_regular_file, resolve_within


def test_resolve_within_accepts_relative_child(tmp_path: Path) -> None:
    assert resolve_within(tmp_path, Path("work/extracted")) == (
        tmp_path / "work" / "extracted"
    ).resolve()


def test_resolve_within_rejects_parent_escape(tmp_path: Path) -> None:
    with pytest.raises(KnowledgeForgeError, match="escapes workspace root"):
        resolve_within(tmp_path, Path("../outside"))


def test_resolve_within_rejects_absolute_path(tmp_path: Path) -> None:
    with pytest.raises(KnowledgeForgeError, match="must be relative"):
        resolve_within(tmp_path, (tmp_path / "absolute").resolve())


def test_require_regular_file_rejects_directory(tmp_path: Path) -> None:
    with pytest.raises(KnowledgeForgeError, match="is not a regular file"):
        require_regular_file(tmp_path, "test artifact")


def test_require_regular_file_rejects_symlink(tmp_path: Path) -> None:
    target = tmp_path / "target.txt"
    target.write_text("content", encoding="utf-8")
    link = tmp_path / "link.txt"
    try:
        link.symlink_to(target)
    except OSError as error:
        pytest.skip(f"Filesystem does not permit test symlink creation: {error.winerror}")
    with pytest.raises(KnowledgeForgeError, match="must not be a symbolic link"):
        require_regular_file(link, "test artifact")
