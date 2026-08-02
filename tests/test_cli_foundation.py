import json
from pathlib import Path
from shutil import copytree
from zipfile import ZIP_DEFLATED, ZipFile

import pytest
from knowledge_forge.cli import run
from pypdf import PdfWriter


def _write_epub(path: Path) -> None:
    container = """<?xml version="1.0"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles><rootfile full-path="OEBPS/content.opf"/></rootfiles>
</container>"""
    opf = """<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf">
  <manifest><item id="chapter" href="chapter.xhtml" media-type="application/xhtml+xml"/></manifest>
  <spine><itemref idref="chapter"/></spine>
</package>"""
    with ZipFile(path, "w", ZIP_DEFLATED) as archive:
        archive.writestr("META-INF/container.xml", container)
        archive.writestr("OEBPS/content.opf", opf)
        archive.writestr("OEBPS/chapter.xhtml", "<h1>Topic</h1><p>Knowledge</p>")


def _write_pdf(path: Path) -> None:
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=300)
    with path.open("wb") as stream:
        writer.write(stream)


def _pipeline_arguments(workspace: Path) -> dict[str, list[str]]:
    return {
        "intake_epub": [
            "intake",
            "--workspace",
            str(workspace),
            "--role",
            "primary-text",
            "--media-type",
            "application/epub+zip",
            "--source",
            str(workspace / "source.epub"),
            "--registry",
            "private/provenance/input-registry.json",
        ],
        "intake_pdf": [
            "intake",
            "--workspace",
            str(workspace),
            "--role",
            "layout-crosscheck",
            "--media-type",
            "application/pdf",
            "--source",
            str(workspace / "source.pdf"),
            "--registry",
            "private/provenance/input-registry.json",
        ],
        "extract": [
            "extract-epub",
            "--workspace",
            str(workspace),
            "--role",
            "primary-text",
            "--registry",
            "private/provenance/input-registry.json",
            "--documents",
            "work/extracted/documents.jsonl",
        ],
        "probe": [
            "probe-pdf",
            "--workspace",
            str(workspace),
            "--role",
            "layout-crosscheck",
            "--registry",
            "private/provenance/input-registry.json",
            "--probe",
            "work/extracted/pdf-probe.json",
        ],
        "normalize": [
            "normalize",
            "--workspace",
            str(workspace),
            "--documents",
            "work/extracted/documents.jsonl",
            "--units",
            "work/normalized/units.jsonl",
            "--registry",
            "private/provenance/input-registry.json",
            "--probe",
            "work/extracted/pdf-probe.json",
            "--ledger",
            "private/provenance/ledger.json",
        ],
        "verify": [
            "verify-foundation",
            "--workspace",
            str(workspace),
            "--schemas",
            "forge/schemas",
            "--registry",
            "private/provenance/input-registry.json",
            "--documents",
            "work/extracted/documents.jsonl",
            "--probe",
            "work/extracted/pdf-probe.json",
            "--units",
            "work/normalized/units.jsonl",
            "--ledger",
            "private/provenance/ledger.json",
        ],
    }


def _run_pipeline(workspace: Path) -> dict[str, list[str]]:
    copytree(
        Path(__file__).parents[1] / "forge" / "schemas",
        workspace / "forge" / "schemas",
    )
    _write_epub(workspace / "source.epub")
    _write_pdf(workspace / "source.pdf")
    arguments = _pipeline_arguments(workspace)
    assert run(arguments["intake_epub"]) == 0
    assert run(arguments["intake_pdf"]) == 0
    assert run(arguments["extract"]) == 0
    assert run(arguments["probe"]) == 0
    assert run(arguments["normalize"]) == 0
    return arguments


def test_cli_runs_foundation_pipeline_idempotently(tmp_path: Path) -> None:
    arguments = _run_pipeline(tmp_path)
    registry_path = tmp_path / "private/provenance/input-registry.json"
    first_registry_bytes = registry_path.read_bytes()
    assert run(arguments["intake_epub"]) == 0
    assert run(arguments["intake_pdf"]) == 0
    assert registry_path.read_bytes() == first_registry_bytes
    assert (tmp_path / "work/extracted/documents.jsonl").is_file()
    assert (tmp_path / "work/extracted/pdf-probe.json").is_file()
    assert (tmp_path / "work/normalized/units.jsonl").is_file()
    assert (tmp_path / "private/provenance/ledger.json").is_file()
    assert not (tmp_path / "pack").exists()
    assert run(arguments["verify"]) == 0


def test_cli_verify_reports_tampered_registry(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    arguments = _run_pipeline(tmp_path)
    registry_path = tmp_path / "private/provenance/input-registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry[0]["size_bytes"] += 1
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    assert run(arguments["verify"]) == 2
    captured = capsys.readouterr()
    assert "size mismatch" in captured.err
