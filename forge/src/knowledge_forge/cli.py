import argparse
import sys
from pathlib import Path
from typing import cast

from knowledge_forge.archive import build_archive
from knowledge_forge.audit import (
    inspect_package,
    verify_promotion_coverage,
    verify_unit_disposition,
)
from knowledge_forge.epub import extract_epub
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.indexes import load_indexes
from knowledge_forge.intake import intake_file, upsert_input_record
from knowledge_forge.io import (
    canonical_json_bytes,
    read_json,
    read_jsonl,
    write_json_atomic,
    write_jsonl_atomic,
)
from knowledge_forge.knowledge_map import build_knowledge_map_projection
from knowledge_forge.models import ExtractedDocument, InputRecord, PdfProbe
from knowledge_forge.normalize import normalize_documents
from knowledge_forge.package import build_package, validate_package
from knowledge_forge.paths import (
    resolve_existing_directory_within,
    resolve_new_directory_within,
    resolve_regular_within,
    resolve_within,
)
from knowledge_forge.pdf_probe import DEFAULT_PDF_LIMITS, probe_pdf
from knowledge_forge.portability import (
    build_portable_exports,
    diff_portable_exports,
    load_portable_context,
    load_portable_context_graph,
    route_portable_export,
    verify_portable_export,
)
from knowledge_forge.provenance import build_provenance_ledger
from knowledge_forge.routing import route_query
from knowledge_forge.routing_evaluation import verify_routing_evaluation
from knowledge_forge.verify import verify_foundation


def _add_workspace(subparser: argparse.ArgumentParser) -> None:
    subparser.add_argument("--workspace", type=Path, required=True)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="knowledge-forge")
    subparsers = parser.add_subparsers(dest="command", required=True)

    intake_parser = subparsers.add_parser("intake")
    _add_workspace(intake_parser)
    intake_parser.add_argument("--role", required=True)
    intake_parser.add_argument("--media-type", required=True)
    intake_parser.add_argument("--source", type=Path, required=True)
    intake_parser.add_argument("--registry", type=Path, required=True)

    epub_parser = subparsers.add_parser("extract-epub")
    _add_workspace(epub_parser)
    epub_parser.add_argument("--role", required=True)
    epub_parser.add_argument("--registry", type=Path, required=True)
    epub_parser.add_argument("--documents", type=Path, required=True)

    pdf_parser = subparsers.add_parser("probe-pdf")
    _add_workspace(pdf_parser)
    pdf_parser.add_argument("--role", required=True)
    pdf_parser.add_argument("--registry", type=Path, required=True)
    pdf_parser.add_argument("--probe", type=Path, required=True)

    normalize_parser = subparsers.add_parser("normalize")
    _add_workspace(normalize_parser)
    normalize_parser.add_argument("--documents", type=Path, required=True)
    normalize_parser.add_argument("--units", type=Path, required=True)
    normalize_parser.add_argument("--registry", type=Path, required=True)
    normalize_parser.add_argument("--probe", type=Path, required=True)
    normalize_parser.add_argument("--ledger", type=Path, required=True)

    verify_parser = subparsers.add_parser("verify-foundation")
    _add_workspace(verify_parser)
    verify_parser.add_argument("--schemas", type=Path, required=True)
    verify_parser.add_argument("--registry", type=Path, required=True)
    verify_parser.add_argument("--documents", type=Path, required=True)
    verify_parser.add_argument("--probe", type=Path, required=True)
    verify_parser.add_argument("--units", type=Path, required=True)
    verify_parser.add_argument("--ledger", type=Path, required=True)

    build_package_parser = subparsers.add_parser("build-package")
    _add_workspace(build_package_parser)
    build_package_parser.add_argument("--pack", type=Path, required=True)
    build_package_parser.add_argument("--schemas", type=Path, required=True)

    verify_package_parser = subparsers.add_parser("verify-package")
    _add_workspace(verify_package_parser)
    verify_package_parser.add_argument("--pack", type=Path, required=True)
    verify_package_parser.add_argument("--schemas", type=Path, required=True)
    verify_package_parser.add_argument("--markers", type=Path, required=True)

    route_parser = subparsers.add_parser("route")
    _add_workspace(route_parser)
    route_parser.add_argument("--pack", type=Path, required=True)
    route_parser.add_argument("--query", required=True)

    archive_package_parser = subparsers.add_parser("archive-package")
    _add_workspace(archive_package_parser)
    archive_package_parser.add_argument("--pack", type=Path, required=True)
    archive_package_parser.add_argument("--schemas", type=Path, required=True)
    archive_package_parser.add_argument("--markers", type=Path, required=True)
    archive_package_parser.add_argument("--archive", type=Path, required=True)

    inspect_package_parser = subparsers.add_parser("inspect-package")
    _add_workspace(inspect_package_parser)
    inspect_package_parser.add_argument("--pack", type=Path, required=True)
    inspect_package_parser.add_argument("--schemas", type=Path, required=True)

    coverage_parser = subparsers.add_parser("verify-promotion-coverage")
    _add_workspace(coverage_parser)
    coverage_parser.add_argument("--pack", type=Path, required=True)
    coverage_parser.add_argument("--schemas", type=Path, required=True)
    coverage_parser.add_argument("--units", type=Path, required=True)
    coverage_parser.add_argument("--reviews", type=Path, required=True)
    coverage_parser.add_argument("--report", type=Path, required=True)

    disposition_parser = subparsers.add_parser("verify-unit-disposition")
    _add_workspace(disposition_parser)
    disposition_parser.add_argument("--pack", type=Path, required=True)
    disposition_parser.add_argument("--schemas", type=Path, required=True)
    disposition_parser.add_argument("--units", type=Path, required=True)
    disposition_parser.add_argument("--reviews", type=Path, required=True)
    disposition_parser.add_argument("--dispositions", type=Path, required=True)
    disposition_parser.add_argument("--report", type=Path, required=True)

    routing_evaluation_parser = subparsers.add_parser(
        "verify-routing-evaluation"
    )
    _add_workspace(routing_evaluation_parser)
    routing_evaluation_parser.add_argument("--pack", type=Path, required=True)
    routing_evaluation_parser.add_argument("--schemas", type=Path, required=True)
    routing_evaluation_parser.add_argument("--suite", type=Path, required=True)
    routing_evaluation_parser.add_argument("--report", type=Path, required=True)

    knowledge_map_parser = subparsers.add_parser(
        "build-knowledge-map-projection"
    )
    _add_workspace(knowledge_map_parser)
    knowledge_map_parser.add_argument("--pack", type=Path, required=True)
    knowledge_map_parser.add_argument("--schemas", type=Path, required=True)
    knowledge_map_parser.add_argument("--output", type=Path, required=True)

    portable_exports_parser = subparsers.add_parser("build-portable-exports")
    _add_workspace(portable_exports_parser)
    portable_exports_parser.add_argument("--pack", type=Path, required=True)
    portable_exports_parser.add_argument("--schemas", type=Path, required=True)
    portable_exports_parser.add_argument("--output", type=Path, required=True)

    verify_portable_exports_parser = subparsers.add_parser(
        "verify-portable-exports"
    )
    _add_workspace(verify_portable_exports_parser)
    verify_portable_exports_parser.add_argument("--export", type=Path, required=True)

    diff_portable_exports_parser = subparsers.add_parser("diff-portable-exports")
    _add_workspace(diff_portable_exports_parser)
    diff_portable_exports_parser.add_argument("--base", type=Path, required=True)
    diff_portable_exports_parser.add_argument("--target", type=Path, required=True)

    route_portable_export_parser = subparsers.add_parser(
        "route-portable-export"
    )
    _add_workspace(route_portable_export_parser)
    route_portable_export_parser.add_argument("--export", type=Path, required=True)
    route_portable_export_parser.add_argument("--query", required=True)

    load_portable_context_parser = subparsers.add_parser(
        "load-portable-context"
    )
    _add_workspace(load_portable_context_parser)
    load_portable_context_parser.add_argument(
        "--export", type=Path, required=True
    )
    load_portable_context_parser.add_argument("--query", required=True)

    load_portable_context_graph_parser = subparsers.add_parser(
        "load-portable-context-graph"
    )
    _add_workspace(load_portable_context_graph_parser)
    load_portable_context_graph_parser.add_argument(
        "--export", type=Path, required=True
    )
    load_portable_context_graph_parser.add_argument("--query", required=True)
    load_portable_context_graph_parser.add_argument("--depth", type=int, required=True)
    return parser


def _load_registry(path: Path) -> list[InputRecord]:
    payload = read_json(path)
    if not isinstance(payload, list):
        raise KnowledgeForgeError("Input registry root must be an array")
    return cast(list[InputRecord], payload)


def _record_for_role(records: list[InputRecord], role: str) -> InputRecord:
    matches = [record for record in records if record["role"] == role]
    if len(matches) != 1:
        raise KnowledgeForgeError(f"Input role must resolve exactly once: {role}")
    return matches[0]


def _load_markers(path: Path) -> list[str]:
    payload = read_json(path)
    if not isinstance(payload, list) or not all(
        isinstance(marker, str) for marker in payload
    ):
        raise KnowledgeForgeError("Private marker file must be a JSON string array")
    return cast(list[str], payload)


def _dispatch(namespace: argparse.Namespace) -> int:
    workspace_root = namespace.workspace.resolve()
    if namespace.command == "intake":
        registry_path = resolve_within(workspace_root, namespace.registry)
        records = _load_registry(registry_path) if registry_path.exists() else []
        record = intake_file(
            namespace.source,
            namespace.role,
            namespace.media_type,
            resolve_within(workspace_root, Path("inputs")),
        )
        write_json_atomic(registry_path, upsert_input_record(records, record))
        return 0
    if namespace.command == "extract-epub":
        registry = _load_registry(resolve_within(workspace_root, namespace.registry))
        record = _record_for_role(registry, namespace.role)
        if record["media_type"] != "application/epub+zip":
            raise KnowledgeForgeError(f"Input role is not an EPUB: {record['role']}")
        source_path = resolve_within(workspace_root, Path(record["stored_path"]))
        documents = extract_epub(source_path, record["sha256"])
        write_jsonl_atomic(
            resolve_within(workspace_root, namespace.documents),
            cast(list[dict[str, object]], documents),
        )
        return 0
    if namespace.command == "probe-pdf":
        registry = _load_registry(resolve_within(workspace_root, namespace.registry))
        record = _record_for_role(registry, namespace.role)
        if record["media_type"] != "application/pdf":
            raise KnowledgeForgeError(f"Input role is not a PDF: {record['role']}")
        source_path = resolve_within(workspace_root, Path(record["stored_path"]))
        probe = probe_pdf(source_path, record["sha256"], DEFAULT_PDF_LIMITS)
        write_json_atomic(resolve_within(workspace_root, namespace.probe), probe)
        return 0
    if namespace.command == "normalize":
        documents = cast(
            list[ExtractedDocument],
            read_jsonl(resolve_within(workspace_root, namespace.documents)),
        )
        units = normalize_documents(documents)
        write_jsonl_atomic(
            resolve_within(workspace_root, namespace.units),
            cast(list[dict[str, object]], units),
        )
        registry = _load_registry(resolve_within(workspace_root, namespace.registry))
        probe = cast(PdfProbe, read_json(resolve_within(workspace_root, namespace.probe)))
        ledger = build_provenance_ledger(registry, documents, units, probe)
        write_json_atomic(resolve_within(workspace_root, namespace.ledger), ledger)
        return 0
    if namespace.command == "verify-foundation":
        verify_foundation(
            workspace_root,
            resolve_within(workspace_root, namespace.schemas),
            resolve_within(workspace_root, namespace.registry),
            resolve_within(workspace_root, namespace.documents),
            resolve_within(workspace_root, namespace.probe),
            resolve_within(workspace_root, namespace.units),
            resolve_within(workspace_root, namespace.ledger),
        )
        return 0
    if namespace.command == "build-package":
        build_package(
            resolve_within(workspace_root, namespace.pack),
            resolve_within(workspace_root, namespace.schemas),
        )
        return 0
    if namespace.command == "verify-package":
        validate_package(
            resolve_within(workspace_root, namespace.pack),
            resolve_within(workspace_root, namespace.schemas),
            _load_markers(resolve_within(workspace_root, namespace.markers)),
        )
        return 0
    if namespace.command == "route":
        indexes = load_indexes(resolve_within(workspace_root, namespace.pack))
        print(route_query(namespace.query, indexes))
        return 0
    if namespace.command == "archive-package":
        build_archive(
            resolve_within(workspace_root, namespace.pack),
            resolve_within(workspace_root, namespace.archive),
            resolve_within(workspace_root, namespace.schemas),
            _load_markers(resolve_within(workspace_root, namespace.markers)),
        )
        return 0
    if namespace.command == "inspect-package":
        profile = inspect_package(
            resolve_within(workspace_root, namespace.pack),
            resolve_within(workspace_root, namespace.schemas),
        )
        print(canonical_json_bytes(profile).decode("utf-8"), end="")
        return 0
    if namespace.command == "verify-promotion-coverage":
        verify_promotion_coverage(
            resolve_within(workspace_root, namespace.pack),
            resolve_within(workspace_root, namespace.schemas),
            resolve_within(workspace_root, namespace.units),
            resolve_within(workspace_root, namespace.reviews),
            resolve_within(workspace_root, namespace.report),
        )
        return 0
    if namespace.command == "verify-unit-disposition":
        verify_unit_disposition(
            resolve_within(workspace_root, namespace.pack),
            resolve_within(workspace_root, namespace.schemas),
            resolve_within(workspace_root, namespace.units),
            resolve_within(workspace_root, namespace.reviews),
            resolve_within(workspace_root, namespace.dispositions),
            resolve_within(workspace_root, namespace.report),
        )
        return 0
    if namespace.command == "verify-routing-evaluation":
        verify_routing_evaluation(
            resolve_within(workspace_root, namespace.pack),
            resolve_within(workspace_root, namespace.schemas),
            resolve_regular_within(
                workspace_root,
                namespace.suite,
                "Routing evaluation suite",
            ),
            resolve_within(workspace_root, namespace.report),
        )
        return 0
    if namespace.command == "build-knowledge-map-projection":
        build_knowledge_map_projection(
            resolve_within(workspace_root, namespace.pack),
            resolve_within(workspace_root, namespace.schemas),
            resolve_new_directory_within(
                workspace_root,
                namespace.output,
                Path("derived"),
                "Knowledge map output",
            ),
        )
        return 0
    if namespace.command == "build-portable-exports":
        build_portable_exports(
            resolve_within(workspace_root, namespace.pack),
            resolve_within(workspace_root, namespace.schemas),
            resolve_new_directory_within(
                workspace_root,
                namespace.output,
                Path("derived"),
                "Portable export output",
            ),
        )
        return 0
    if namespace.command == "verify-portable-exports":
        manifest = verify_portable_export(
            resolve_existing_directory_within(
                workspace_root,
                namespace.export,
                "Portable export input",
            )
        )
        print(canonical_json_bytes(manifest).decode("utf-8"), end="")
        return 0
    if namespace.command == "diff-portable-exports":
        base_root = resolve_existing_directory_within(
            workspace_root,
            namespace.base,
            "Portable export base",
        )
        target_root = resolve_existing_directory_within(
            workspace_root,
            namespace.target,
            "Portable export target",
        )
        delta = diff_portable_exports(base_root, target_root)
        print(canonical_json_bytes(delta).decode("utf-8"), end="")
        return 0
    if namespace.command == "route-portable-export":
        result = route_portable_export(
            resolve_existing_directory_within(
                workspace_root,
                namespace.export,
                "Portable export input",
            ),
            namespace.query,
        )
        print(canonical_json_bytes(result).decode("utf-8"), end="")
        return 0
    if namespace.command == "load-portable-context":
        result = load_portable_context(
            resolve_existing_directory_within(
                workspace_root,
                namespace.export,
                "Portable export input",
            ),
            namespace.query,
        )
        print(canonical_json_bytes(result).decode("utf-8"), end="")
        return 0
    if namespace.command == "load-portable-context-graph":
        result = load_portable_context_graph(
            resolve_existing_directory_within(
                workspace_root,
                namespace.export,
                "Portable export input",
            ),
            namespace.query,
            namespace.depth,
        )
        print(canonical_json_bytes(result).decode("utf-8"), end="")
        return 0
    raise KnowledgeForgeError(f"Unsupported command: {namespace.command}")


def run(arguments: list[str]) -> int:
    namespace = _parser().parse_args(arguments)
    try:
        return _dispatch(namespace)
    except KnowledgeForgeError as error:
        print(f"knowledge-forge: {error}", file=sys.stderr)
        return 2


def main() -> int:
    return run(sys.argv[1:])
