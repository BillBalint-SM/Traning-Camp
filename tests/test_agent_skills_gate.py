import importlib.util
import json
import shutil
import subprocess
from pathlib import Path
from types import ModuleType
from typing import cast

import pytest
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.hashing import sha256_bytes
from knowledge_forge.io import canonical_json_bytes
from knowledge_forge.portability import build_portable_exports, verify_portable_export

ROOT = Path(__file__).parents[1]
PACK_ROOT = ROOT / "pack"
SCHEMA_ROOT = ROOT / "forge" / "schemas"
GATE_PATH = ROOT / "tools" / "validate_agent_skills.py"


def _refresh_manifest(output_root: Path) -> None:
    manifest_path = output_root / "export.json"
    manifest = cast(
        dict[str, object], json.loads(manifest_path.read_text(encoding="utf-8"))
    )
    entries = cast(list[dict[str, object]], manifest["files"])
    for entry in entries:
        relative = cast(str, entry["path"])
        entry["sha256"] = sha256_bytes((output_root / relative).read_bytes())
    manifest_without_digest = dict(manifest)
    manifest_without_digest.pop("export_sha256", None)
    manifest["export_sha256"] = sha256_bytes(
        canonical_json_bytes(manifest_without_digest)
    )
    manifest_path.write_bytes(canonical_json_bytes(manifest))


def _load_gate() -> ModuleType:
    specification = importlib.util.spec_from_file_location(
        "validate_agent_skills", GATE_PATH
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("Agent Skills conformance gate cannot be loaded")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def test_gate_validates_real_export_from_a_skill_name_directory(
    tmp_path: Path, monkeypatch
) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)
    gate = _load_gate()
    captured: list[Path] = []

    monkeypatch.setattr(gate.shutil, "which", lambda command: "agentskills")

    def validate(command: list[str], check: bool) -> subprocess.CompletedProcess[str]:
        assert command[:2] == ["agentskills", "validate"]
        profile_directory = Path(command[2])
        captured.append(profile_directory)
        assert profile_directory.name == "portable-agent-knowledge"
        assert (profile_directory / "SKILL.md").is_file()
        assert (profile_directory / "references" / "indexes" / "l0.json").is_file()
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(gate.subprocess, "run", validate)

    assert gate.validate_skill(output_root / "skill") == 0
    assert len(captured) == 1
    assert not captured[0].exists()


def test_gate_propagates_invalid_profile_failure(
    tmp_path: Path, monkeypatch
) -> None:
    skill_directory = tmp_path / "skill"
    skill_directory.mkdir()
    (skill_directory / "SKILL.md").write_text(
        "---\nname: fixture\n---\n", encoding="utf-8"
    )
    gate = _load_gate()

    monkeypatch.setattr(gate.shutil, "which", lambda command: "agentskills")
    monkeypatch.setattr(
        gate.subprocess,
        "run",
        lambda command, check: subprocess.CompletedProcess(command, 1),
    )

    assert gate.validate_skill(skill_directory) == 1


def test_gate_fails_closed_when_agentskills_is_unavailable(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    skill_directory = tmp_path / "skill"
    skill_directory.mkdir()
    (skill_directory / "SKILL.md").write_text(
        "---\nname: fixture\ndescription: Fixture skill.\n---\n", encoding="utf-8"
    )
    gate = _load_gate()

    monkeypatch.setattr(gate.shutil, "which", lambda command: None)

    assert gate.validate_skill(skill_directory) == 2
    assert "uvx --from skills-ref==0.1.1 agentskills validate" in capsys.readouterr().err


def test_gate_fails_closed_when_skill_directory_is_missing(
    tmp_path: Path, capsys
) -> None:
    gate = _load_gate()

    assert gate.validate_skill(tmp_path / "missing") == 2
    assert "must be a directory" in capsys.readouterr().err


def test_repository_gate_accepts_real_export(tmp_path: Path) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)

    manifest = verify_portable_export(output_root)

    assert manifest["format_version"] == 1
    assert manifest["profiles"]["skill"]["file_count"] > 0


def test_repository_gate_rejects_skill_reference_closure_fixture(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)
    skill_path = output_root / "skill" / "SKILL.md"
    skill_path.write_text(
        skill_path.read_text(encoding="utf-8")
        + "\n- `references/does-not-exist.json`\n",
        encoding="utf-8",
    )
    _refresh_manifest(output_root)

    with pytest.raises(KnowledgeForgeError, match="reference is unresolved"):
        verify_portable_export(output_root)


def test_official_validator_accepts_real_export_when_installed(
    tmp_path: Path,
) -> None:
    if shutil.which("agentskills") is None:
        pytest.skip("official agentskills validator is not installed")
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)
    gate = _load_gate()

    assert gate.validate_skill(output_root / "skill") == 0


def test_official_validator_rejects_invalid_fixture_when_installed(
    tmp_path: Path,
) -> None:
    if shutil.which("agentskills") is None:
        pytest.skip("official agentskills validator is not installed")
    skill_directory = tmp_path / "fixture"
    skill_directory.mkdir()
    (skill_directory / "SKILL.md").write_text(
        "---\nname: fixture\n---\n", encoding="utf-8"
    )
    gate = _load_gate()

    assert gate.validate_skill(skill_directory) != 0
