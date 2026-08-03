"""Validate an Agent Skills profile with the official reference validator."""

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def _skill_name(skill_directory: Path) -> str:
    skill_path = skill_directory / "SKILL.md"
    content = skill_path.read_text(encoding="utf-8")
    match = re.search(r"^name:\s*([a-z0-9][a-z0-9-]*)\s*$", content, re.MULTILINE)
    if match is None:
        raise ValueError("SKILL.md must declare a lowercase hyphenated name")
    return match.group(1)


def validate_skill(skill_directory: Path) -> int:
    if not skill_directory.is_dir():
        print(
            f"Agent Skills profile must be a directory: {skill_directory}",
            file=sys.stderr,
        )
        return 2
    skill_path = skill_directory / "SKILL.md"
    if not skill_path.is_file():
        print(
            f"Agent Skills profile is missing SKILL.md: {skill_directory}",
            file=sys.stderr,
        )
        return 2
    validator = shutil.which("agentskills")
    if validator is None:
        print(
            "Agent Skills validator is unavailable. Install it with: "
            "uv tool install skills-ref==0.1.1. For a one-off validation, run: "
            "uvx --from skills-ref==0.1.1 agentskills validate <skill-dir>",
            file=sys.stderr,
        )
        return 2
    try:
        skill_name = _skill_name(skill_directory)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Agent Skills profile cannot be prepared: {error}", file=sys.stderr)
        return 2
    try:
        with tempfile.TemporaryDirectory(prefix="agent-skills-") as temporary_root:
            validation_directory = Path(temporary_root) / skill_name
            shutil.copytree(skill_directory, validation_directory)
            result = subprocess.run(
                [validator, "validate", str(validation_directory)], check=False
            )
    except OSError as error:
        print(f"Agent Skills validator could not run: {error}", file=sys.stderr)
        return 2
    return result.returncode


def main(arguments: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_directory", type=Path)
    namespace = parser.parse_args(arguments)
    return validate_skill(namespace.skill_directory)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
