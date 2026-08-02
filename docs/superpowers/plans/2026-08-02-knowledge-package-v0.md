# Source-Neutral Knowledge Package v0 Implementation Plan

**Status:** Implemented and verified against the approved local validation material on 2026-08-02.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Build the first portable, agent-visible Hungarian knowledge package with trusted modules, deterministic L0-to-L2 routing, canonical relation graph, leak-safe manifest validation, and a relocatable ZIP archive.

**Architecture:** Human-reviewed Markdown modules under `pack/knowledge/` are the canonical semantic layer. A narrow Python package reads safe YAML front matter, validates the module contract, deterministically derives indexes, graph, and manifest, then validates and archives only the declared `pack/` files. Private review mapping remains ignored and is checked separately; it is never read by package routing or copied into the archive.

**Tech Stack:** Python 3.10+, `PyYAML` safe loading, `jsonschema`, standard-library `hashlib`, `zipfile`, and `tempfile`, `uv`, `pytest`, and `ruff`.

## Global Constraints

- Agent-visible content is Hungarian-first, uses English technical aliases where useful, and contains no origin, author, publication, acquisition, filename, private-path, URL, or processing-history reference.
- `pack/` is the only canonical agent-visible tree. `inputs/`, `private/`, `work/`, `forge/`, `tests/`, `derived/`, `dist/`, and docs are never routing inputs or archive members.
- Use `yaml.safe_load`; never use `yaml.load` or an unsafe loader.
- Module IDs are lowercase dot-separated semantic identities. Supported kinds, maturities, section names, and relation types are exactly those in the approved design specification.
- Public package data is deterministic: UTF-8, LF-terminated, sorted by relative path or stable ID, and has no timestamps or absolute paths.
- Every changed behavior follows red → green testing. Tests use only synthetic modules and seed markers; actual private content is inspected only in the final local validation task.
- No AI Booster Kit change, hosted retrieval service, vector database, model training, remote repository change, publication, UA scan, or Graphify scan belongs to this slice.
- Commit each independently reviewable task. Do not commit private inputs, private promotion mappings, work artifacts, visual renderings, or ZIP outputs.

---

## File Structure

| Path | Responsibility |
| --- | --- |
| `pyproject.toml`, `uv.lock` | Add and lock safe YAML parsing dependency. |
| `forge/schemas/knowledge-module.schema.json` | Machine contract for parsed module front matter. |
| `forge/schemas/package-index.schema.json` | Contract for compact L0 and L1 route indexes. |
| `forge/schemas/canonical-graph.schema.json` | Contract for generated nodes and directed edges. |
| `forge/schemas/package-manifest.schema.json` | Contract for package inventory and digests. |
| `forge/src/knowledge_forge/frontmatter.py` | Safe front-matter parsing and required-section checks. |
| `forge/src/knowledge_forge/package.py` | Module discovery, package-tree validation, and pack-relative safety checks. |
| `forge/src/knowledge_forge/indexes.py` | Deterministic L0 and L1 index generation. |
| `forge/src/knowledge_forge/graph.py` | Deterministic canonical graph generation and validation. |
| `forge/src/knowledge_forge/routing.py` | Pure deterministic query routing over L0/L1 metadata. |
| `forge/src/knowledge_forge/hashing.py` | Extend streaming file hashing with byte hashing for package digests. |
| `forge/src/knowledge_forge/manifest.py` | File inventory, hash verification, and package digest. |
| `forge/src/knowledge_forge/leakage.py` | Content-neutrality and package-boundary checks. |
| `forge/src/knowledge_forge/archive.py` | Allowlist ZIP construction and clean extraction verification. |
| `forge/src/knowledge_forge/cli.py` | `build-package`, `verify-package`, `route`, and `archive-package` commands. |
| `pack/knowledge/*.md` | Fifteen curated, source-neutral Hungarian L2 modules. |
| `pack/indexes/areas.json` | Authored L0 topic map and L1 area definitions used to derive indexes. |
| `pack/graph/canonical.json` | Generated canonical graph. |
| `pack/indexes/l0.json`, `pack/indexes/l1/*.json` | Generated progressive-disclosure indexes. |
| `pack/skills/SKILL.md` | Host-neutral, compact routing instructions. |
| `pack/manifest.json` | Generated package inventory and digest. |
| `tests/test_frontmatter.py` | Module parsing, schema, and section rejection tests. |
| `tests/test_package.py` | Public package tree, module set, and duplicate safety tests. |
| `tests/test_routing.py` | Positive, negative, ambiguous, and context-budget route tests. |
| `tests/test_manifest.py` | Hash, undeclared-file, path, and leakage gate tests. |
| `tests/test_archive.py` | ZIP inventory, relocation, and clean extraction checks. |
| `tests/test_cli_package.py` | End-to-end package command tests. |

## Representative v0 Module Set

The semantic corpus is deliberately representative rather than exhaustive. Every file follows the same eight Hungarian body sections and is original, decision-oriented prose.

| ID | Kind | L1 area |
| --- | --- | --- |
| `principle.agent-operating-model` | principle | `core-agent-systems` |
| `principle.context-is-finite` | principle | `context-and-knowledge` |
| `pattern.context-budget-allocation` | pattern | `context-and-knowledge` |
| `pattern.context-compression` | pattern | `context-and-knowledge` |
| `decision-guide.memory-vs-retrieval` | decision-guide | `context-and-knowledge` |
| `procedure.user-memory-lifecycle` | procedure | `context-and-knowledge` |
| `procedure.tool-contract-design` | procedure | `tool-execution` |
| `checklist.tool-safety-boundary` | checklist | `tool-execution` |
| `pattern.tool-discovery` | pattern | `tool-execution` |
| `procedure.agent-evaluation-loop` | procedure | `evaluation-and-improvement` |
| `decision-guide.sft-or-rl` | decision-guide | `evaluation-and-improvement` |
| `pattern.experience-driven-improvement` | pattern | `evaluation-and-improvement` |
| `concept.multimodal-interaction-boundary` | concept | `interaction-and-collaboration` |
| `pattern.multi-agent-context-boundaries` | pattern | `interaction-and-collaboration` |
| `failure-mode.unvalidated-autonomy` | failure-mode | `interaction-and-collaboration` |

### Task 1: Add safe module contracts and front-matter parsing

**Files:**
- Modify: `pyproject.toml`
- Modify: `uv.lock`
- Create: `forge/schemas/knowledge-module.schema.json`
- Create: `forge/src/knowledge_forge/frontmatter.py`
- Modify: `forge/src/knowledge_forge/models.py`
- Test: `tests/test_frontmatter.py`

**Interfaces:**
- Consumes: `validate_record(schema_path: Path, record: object, label: str)` and `sha256_file(path: Path, chunk_size: int) -> str`.
- Produces: `KnowledgeModuleMetadata`, `KnowledgeModule`, `parse_knowledge_module(module_path: Path, schema_path: Path) -> KnowledgeModule`, and `REQUIRED_SECTIONS: tuple[str, ...]`.

- [x] **Step 1: Write failing module parsing tests**

```python
def test_parse_knowledge_module_accepts_safe_yaml_and_required_sections(tmp_path: Path) -> None:
    module_path = tmp_path / "principle.example.md"
    module_path.write_text(VALID_MODULE, encoding="utf-8", newline="\n")

    module = parse_knowledge_module(module_path, SCHEMA_PATH)

    assert module["metadata"]["id"] == "principle.example"
    assert module["content_sha256"] == sha256_file(module_path, 1024)


def test_parse_knowledge_module_rejects_missing_required_section(tmp_path: Path) -> None:
    module_path = tmp_path / "principle.example.md"
    module_path.write_text(VALID_MODULE.replace("## Ellenőrzés\n", ""), encoding="utf-8")

    with pytest.raises(KnowledgeForgeError, match="missing required sections"):
        parse_knowledge_module(module_path, SCHEMA_PATH)
```

Use `VALID_MODULE` with only `safe_load`-compatible primitive YAML values and all eight headings. Add tests for a non-object YAML root and an unknown front-matter key.

- [x] **Step 2: Run the focused test and confirm the missing-module failure**

Run: `uv run pytest -v tests/test_frontmatter.py`

Expected: collection fails because `knowledge_forge.frontmatter` does not exist.

- [x] **Step 3: Add the locked safe-YAML dependency and module schema**

Run `uv add pyyaml`, inspect `pyproject.toml` and `uv.lock`, then define an object-only schema with `additionalProperties: false` and these exact front-matter keys:

```json
{
  "required": ["id", "title", "kind", "maturity", "confidence", "language", "tags", "aliases", "relations"],
  "properties": {
    "id": {"pattern": "^[a-z][a-z0-9]*(\\.[a-z0-9-]+)+$"},
    "kind": {"enum": ["principle", "concept", "pattern", "decision-guide", "failure-mode", "procedure", "checklist", "experiment"]},
    "maturity": {"enum": ["candidate", "reviewed", "validated", "deprecated"]},
    "confidence": {"enum": ["low", "medium", "high"]},
    "language": {"const": "hu"}
  }
}
```

Require non-empty unique string `tags` and `aliases`; require relations with `type` from the six approved relation names and a valid target ID.

- [x] **Step 4: Implement strict safe parsing and section checks**

```python
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


def parse_knowledge_module(module_path: Path, schema_path: Path) -> KnowledgeModule:
    raw = module_path.read_text(encoding="utf-8")
    metadata_text, body = _split_front_matter(raw, module_path)
    metadata = yaml.safe_load(metadata_text)
    if not isinstance(metadata, dict):
        raise KnowledgeForgeError(f"Module front matter must be an object: {module_path.name}")
    validate_record(schema_path, metadata, f"knowledge module {module_path.name}")
    _require_sections(body, module_path)
    return {"metadata": cast(KnowledgeModuleMetadata, metadata), "body": body, "content_sha256": sha256_file(module_path, 1024)}
```

`_split_front_matter` requires opening and closing `---` lines at the start of the file, rejects multiple YAML documents, and preserves the body verbatim after the delimiter. `_require_sections` accepts headings only in the declared order and rejects duplicates.

- [x] **Step 5: Run focused tests and static checks**

Run:

```powershell
uv run pytest -v tests/test_frontmatter.py
uv run ruff check forge/src/knowledge_forge/frontmatter.py tests/test_frontmatter.py
```

Expected: all front-matter tests pass, including unsafe/invalid-shape rejection.

- [x] **Step 6: Commit safe module contracts**

```powershell
git add pyproject.toml uv.lock forge/schemas/knowledge-module.schema.json forge/src/knowledge_forge/frontmatter.py forge/src/knowledge_forge/models.py tests/test_frontmatter.py
git commit -m "feat: add safe knowledge module contracts"
```

### Task 2: Create and validate the source-neutral v0 module set

**Files:**
- Create: `pack/knowledge/*.md` for the fifteen IDs in the representative module table
- Create: `pack/indexes/areas.json`
- Create: `forge/src/knowledge_forge/package.py`
- Test: `tests/test_package.py`

**Interfaces:**
- Consumes: `parse_knowledge_module(module_path, schema_path)` from Task 1.
- Produces: `discover_modules(pack_root: Path, schema_path: Path) -> list[KnowledgeModule]` and `validate_module_set(modules: list[KnowledgeModule]) -> None`.

- [x] **Step 1: Write failing public-package tree tests**

```python
def test_discover_modules_returns_the_curated_v0_set() -> None:
    modules = discover_modules(PACK_ROOT, SCHEMA_PATH)

    assert {module["metadata"]["id"] for module in modules} == EXPECTED_IDS
    assert all(module["metadata"]["language"] == "hu" for module in modules)


def test_validate_module_set_rejects_duplicate_aliases_in_one_area(tmp_path: Path) -> None:
    modules = [module_with_alias("azonos"), another_module_with_alias("azonos")]

    with pytest.raises(KnowledgeForgeError, match="Ambiguous alias"):
        validate_module_set(modules)
```

`EXPECTED_IDS` is the exact fifteen-ID set above. Add duplicate ID, case-colliding path, and deprecated default-route eligibility rejection tests.

- [x] **Step 2: Run the focused test and confirm failure**

Run: `uv run pytest -v tests/test_package.py`

Expected: collection fails because `knowledge_forge.package` does not exist.

- [x] **Step 3: Author the canonical modules and L0/L1 area declaration**

Every module uses this exact skeleton, with original Hungarian prose rather than copied sentences:

```markdown
---
id: principle.agent-operating-model
title: Agent működési modell
kind: principle
maturity: validated
confidence: high
language: hu
tags: [agent, context, tools]
aliases: [agent operating model, ügynök működési modell]
relations:
  - type: supports
    target: principle.context-is-finite
---

## Lényeg

...

## Miért működik

...

## Mikor alkalmazd

...

## Mikor ne alkalmazd

...

## Döntési szabály

...

## Hibamódok

...

## Kapcsolatok

...

## Ellenőrzés

...
```

Use `validated` only where the module supplies a concrete check, worked decision rule, or reproducible reasoning. Do not include Markdown links, URLs, input terms, named people, publication references, chapter references, or private identifiers. `areas.json` declares the five area IDs, their Hungarian titles, their routing aliases, and the exact L2 IDs assigned to each area.

- [x] **Step 4: Implement package discovery and set validation**

```python
def discover_modules(pack_root: Path, schema_path: Path) -> list[KnowledgeModule]:
    knowledge_root = _require_directory(pack_root / "knowledge")
    module_paths = sorted(knowledge_root.rglob("*.md"), key=lambda path: path.as_posix())
    if not module_paths:
        raise KnowledgeForgeError("Package has no knowledge modules")
    return [parse_knowledge_module(path, schema_path) for path in module_paths]


def validate_module_set(modules: list[KnowledgeModule]) -> None:
    _require_unique_ids(modules)
    _require_unique_default_aliases(modules)
    _require_valid_relation_targets(modules)
```

Reject symlinked modules, modules outside `pack/knowledge`, duplicate IDs, duplicate case-insensitive paths, ambiguous aliases among non-deprecated modules, relations to missing IDs, and self-relations.

- [x] **Step 5: Run focused package tests**

Run: `uv run pytest -v tests/test_frontmatter.py tests/test_package.py`

Expected: curated set and every structural negative case pass.

- [x] **Step 6: Commit the curated semantic layer**

```powershell
git add pack/knowledge pack/indexes/areas.json forge/src/knowledge_forge/package.py tests/test_package.py
git commit -m "feat: add curated knowledge modules"
```

### Task 3: Generate progressive indexes, canonical graph, and deterministic routes

**Files:**
- Create: `forge/schemas/package-index.schema.json`
- Create: `forge/schemas/canonical-graph.schema.json`
- Create: `forge/src/knowledge_forge/indexes.py`
- Create: `forge/src/knowledge_forge/graph.py`
- Create: `forge/src/knowledge_forge/routing.py`
- Create: `pack/indexes/l0.json`
- Create: `pack/indexes/l1/core-agent-systems.json`
- Create: `pack/indexes/l1/context-and-knowledge.json`
- Create: `pack/indexes/l1/tool-execution.json`
- Create: `pack/indexes/l1/evaluation-and-improvement.json`
- Create: `pack/indexes/l1/interaction-and-collaboration.json`
- Create: `pack/graph/canonical.json`
- Test: `tests/test_routing.py`

**Interfaces:**
- Consumes: `discover_modules`, `validate_module_set`, and `areas.json` from Task 2.
- Produces: `build_indexes(modules: list[KnowledgeModule], areas: list[AreaDefinition]) -> PackageIndexes`, `build_graph(modules: list[KnowledgeModule], module_paths: dict[str, str]) -> CanonicalGraph`, and `route_query(query: str, indexes: PackageIndexes) -> RouteResult`.

- [x] **Step 1: Write failing graph and route tests**

```python
def test_route_query_selects_minimal_context_for_compression() -> None:
    result = route_query("Mikor kell a kontextust tömöríteni?", INDEXES)

    assert result["status"] == "covered"
    assert result["area_id"] == "context-and-knowledge"
    assert result["module_ids"] == ["pattern.context-compression"]


def test_route_query_returns_not_covered_without_inventing_route() -> None:
    result = route_query("Melyik notebook gépet válasszam?", INDEXES)

    assert result == {"status": "not-covered", "area_id": None, "module_ids": []}
```

Add an ambiguous query asserting two named areas for `"MCP vagy több ügynök együttműködés?"`, a dangling graph target case, a graph self-edge case, and byte-budget assertions of `len(canonical_json_bytes(l0)) <= 8192` and each L1 file `<= 8192` bytes.

- [x] **Step 2: Run routing tests and confirm failure**

Run: `uv run pytest -v tests/test_routing.py`

Expected: collection fails because `knowledge_forge.indexes` and `knowledge_forge.routing` do not exist.

- [x] **Step 3: Implement sorted L0/L1 index generation**

`areas.json` is the only human-authored routing declaration. Build `l0.json` with area ID, Hungarian title, aliases, and L1 relative path only; build each L1 file with concise principles, decision boundaries, and sorted L2 module descriptors `{id, title, kind, maturity, confidence, tags, aliases}`. Do not copy module bodies into indexes.

```python
def build_indexes(modules: list[KnowledgeModule], areas: list[AreaDefinition]) -> PackageIndexes:
    by_id = {module["metadata"]["id"]: module for module in modules}
    _validate_area_assignments(areas, by_id)
    return {
        "l0": _build_l0(areas),
        "l1": {area["id"]: _build_l1(area, by_id) for area in sorted(areas, key=lambda item: item["id"])},
    }
```

- [x] **Step 4: Implement graph generation and pure routing**

`canonical.json` contains sorted `nodes` and `edges`; every node has the fields mandated by the design specification. `route_query` uses Unicode normalization, `casefold`, exact token matching, then deterministic descending score and lexical-ID tiebreaking. A tie across areas returns `{status: "ambiguous", area_id: None, module_ids: [], alternatives: [...]}`. A zero score returns the exact `not-covered` shape from the test.

- [x] **Step 5: Generate derived canonical files and run focused checks**

Run:

```powershell
uv run pytest -v tests/test_package.py tests/test_routing.py
uv run ruff check forge/src/knowledge_forge/indexes.py forge/src/knowledge_forge/graph.py forge/src/knowledge_forge/routing.py
```

Expected: graph edges resolve, L0/L1 stay under budget, and all positive, negative, and ambiguous routes pass.

- [x] **Step 6: Commit routing and graph generation**

```powershell
git add forge/schemas/package-index.schema.json forge/schemas/canonical-graph.schema.json forge/src/knowledge_forge/indexes.py forge/src/knowledge_forge/graph.py forge/src/knowledge_forge/routing.py pack/indexes/l0.json pack/indexes/l1 pack/graph/canonical.json tests/test_routing.py
git commit -m "feat: add deterministic package routing"
```

### Task 4: Add manifest, leakage gate, and complete package validation

**Files:**
- Create: `forge/schemas/package-manifest.schema.json`
- Modify: `forge/src/knowledge_forge/hashing.py`
- Create: `forge/src/knowledge_forge/manifest.py`
- Create: `forge/src/knowledge_forge/leakage.py`
- Modify: `forge/src/knowledge_forge/package.py`
- Create: `pack/skills/SKILL.md`
- Create: `pack/manifest.json`
- Test: `tests/test_manifest.py`

**Interfaces:**
- Consumes: modules, indexes, and graph from Tasks 2–3; `sha256_file`; `validate_record`.
- Produces: `sha256_bytes(data: bytes) -> str`, `build_manifest(pack_root: Path) -> PackageManifest`, `validate_package(pack_root: Path, schema_dir: Path, markers: list[str]) -> PackageManifest`, and `write_manifest(pack_root: Path) -> PackageManifest`.

- [x] **Step 1: Write failing manifest and leakage tests**

```python
def test_validate_package_rejects_undeclared_file(tmp_path: Path) -> None:
    package_root = copy_clean_package(tmp_path)
    (package_root / "knowledge" / "unlisted.md").write_text("x", encoding="utf-8")

    with pytest.raises(KnowledgeForgeError, match="undeclared package file"):
        validate_package(package_root, SCHEMA_PATH, [])


def test_validate_package_rejects_seeded_private_marker(tmp_path: Path) -> None:
    package_root = copy_clean_package(tmp_path)
    skill_path = package_root / "skills" / "SKILL.md"
    skill_path.write_text(skill_path.read_text(encoding="utf-8") + "\nprivate-seed-marker\n", encoding="utf-8")

    with pytest.raises(KnowledgeForgeError, match="forbidden content marker"):
        validate_package(package_root, SCHEMA_PATH, ["private-seed-marker"])
```

Add stale hash, absolute path, symlink, private-prefix, and harmless-technical-phrase tests. Assert the skill contains only routing instructions and rejects any full L2 body-section heading.

- [x] **Step 2: Run manifest tests and confirm failure**

Run: `uv run pytest -v tests/test_manifest.py`

Expected: collection fails because the manifest and leakage modules do not exist.

- [x] **Step 3: Implement an allowlist manifest and package digest**

The only allowed package-relative prefixes are `knowledge/`, `indexes/`, `graph/`, and `skills/`, plus root `manifest.json`. Reject all physical files not declared in the manifest. The manifest lists each non-manifest relative path and SHA-256 hash sorted lexically; its `package_sha256` is the SHA-256 of canonical JSON bytes for that sorted list. Never include a timestamp, host path, or provenance field.

```python
def build_manifest(pack_root: Path) -> PackageManifest:
    files = _declared_files(pack_root)
    inventory = [{"path": path, "sha256": sha256_file(pack_root / path, 1024)} for path in files]
    return {"format_version": 1, "files": inventory, "package_sha256": sha256_bytes(canonical_json_bytes(inventory))}
```

- [x] **Step 4: Implement narrow leakage checks and routing skill**

`leakage.py` scans declared UTF-8 text files for caller-supplied non-empty markers, absolute-path patterns, private directory prefixes, credentials, and explicit origin-reference tokens. It must not reject the technical phrase `source code`. The public skill says to load L0, select one L1 area, load only needed L2 IDs, surface ambiguity, return `not covered` when appropriate, and never scan outside `pack/`.

- [x] **Step 5: Run manifest and package checks**

Run:

```powershell
uv run pytest -v tests/test_manifest.py tests/test_package.py tests/test_routing.py
uv run ruff check forge/src/knowledge_forge/manifest.py forge/src/knowledge_forge/leakage.py forge/src/knowledge_forge/package.py
```

Expected: stale, undeclared, leaking, symlinked, and malformed packages fail closed; the clean package validates.

- [x] **Step 6: Commit package validation**

```powershell
git add forge/schemas/package-manifest.schema.json forge/src/knowledge_forge/hashing.py forge/src/knowledge_forge/manifest.py forge/src/knowledge_forge/leakage.py forge/src/knowledge_forge/package.py pack/skills/SKILL.md pack/manifest.json tests/test_manifest.py
git commit -m "feat: validate source-neutral package exports"
```

### Task 5: Build relocatable archives and expose package CLI commands

**Files:**
- Create: `forge/src/knowledge_forge/archive.py`
- Modify: `forge/src/knowledge_forge/cli.py`
- Test: `tests/test_archive.py`
- Test: `tests/test_cli_package.py`

**Interfaces:**
- Consumes: `validate_package(pack_root, schema_dir, markers) -> PackageManifest` from Task 4.
- Produces: `build_archive(pack_root: Path, archive_path: Path, schema_dir: Path, markers: list[str]) -> None`, `verify_archive(archive_path: Path, schema_dir: Path, markers: list[str]) -> None`, plus `build-package`, `verify-package`, `route`, and `archive-package` CLI commands.

- [x] **Step 1: Write failing archive and CLI integration tests**

```python
def test_build_archive_has_only_manifest_allowlist_members(tmp_path: Path) -> None:
    archive_path = tmp_path / "knowledge-package-v0.zip"

    build_archive(PACK_ROOT, archive_path, SCHEMA_PATH, [])

    assert archive_path.is_file()
    verify_archive(archive_path, SCHEMA_PATH, [])


def test_cli_routes_a_positive_query(capsys: pytest.CaptureFixture[str]) -> None:
    status = run(["route", "--pack", "pack", "--query", "Hogyan tervezzek eszköz szerződést?"])

    assert status == 0
    assert "procedure.tool-contract-design" in capsys.readouterr().out
```

Add a relocation test copying `pack/` to a new temporary directory before `validate_package`, and a ZIP-slip inventory test with a synthetic `../escape` member that must fail before extraction.

- [x] **Step 2: Run archive tests and confirm failure**

Run: `uv run pytest -v tests/test_archive.py tests/test_cli_package.py`

Expected: collection fails because `knowledge_forge.archive` does not exist and the CLI has no package commands.

- [x] **Step 3: Implement archive construction and clean extraction validation**

```python
def build_archive(pack_root: Path, archive_path: Path, schema_dir: Path, markers: list[str]) -> None:
    manifest = validate_package(pack_root, schema_dir, markers)
    members = [entry["path"] for entry in manifest["files"]] + ["manifest.json"]
    with ZipFile(archive_path, "w", ZIP_DEFLATED) as archive:
        for member in sorted(members):
            archive.write(pack_root / member, member)
    verify_archive(archive_path, schema_dir, markers)
```

`verify_archive` rejects absolute, backslash, drive-qualified, and `..` paths before extraction. It extracts to a fresh temporary directory, ensures the ZIP inventory exactly equals manifest allowlist plus `manifest.json`, and reruns `validate_package` on the extracted tree.

- [x] **Step 4: Extend the fail-closed CLI**

Add explicit required arguments without defaults:

```text
knowledge-forge build-package --workspace <root> --pack <relative-pack> --schemas <relative-schemas>
knowledge-forge verify-package --workspace <root> --pack <relative-pack> --schemas <relative-schemas> --markers <relative-private-markers>
knowledge-forge route --workspace <root> --pack <relative-pack> --query <text>
knowledge-forge archive-package --workspace <root> --pack <relative-pack> --schemas <relative-schemas> --markers <relative-private-markers> --archive <relative-dist-zip>
```

Commands must resolve paths through `resolve_within`, emit only content-safe errors, and never print private marker values or package body text during verification.

- [x] **Step 5: Run focused tests and commit archive/CLI delivery**

Run:

```powershell
uv run pytest -v tests/test_archive.py tests/test_cli_package.py
uv run ruff check .
```

Then commit:

```powershell
git add forge/src/knowledge_forge/archive.py forge/src/knowledge_forge/cli.py tests/test_archive.py tests/test_cli_package.py
git commit -m "feat: archive portable knowledge packages"
```

### Task 6: Verify the complete v0 package against local private validation material

**Files:**
- Create locally only: `private/provenance/promotion-map.json`
- Create locally only: `private/leakage/markers.json`
- Create locally only: `inputs/*`, `work/extracted/*`, `work/normalized/*`, `dist/knowledge-package-v0.zip`
- Modify: `docs/superpowers/specs/2026-08-02-portable-agent-knowledge-forge-design.md`
- Modify: `docs/superpowers/plans/2026-08-02-knowledge-package-v0.md`

**Interfaces:**
- Consumes: all Tasks 1–5 plus existing intake, extraction, normalization, and foundation verification commands.
- Produces: a clean tracked `pack/` and ignored local validation artifacts whose verification status is reproducible.

- [x] **Step 1: Run the full automated suite before private validation**

Run:

```powershell
uv run ruff check .
uv run pytest -v
```

Expected: every test is green before private material is present in this worktree.

- [x] **Step 2: Recreate the private intake and foundation artifacts locally**

Use the approved local inputs with the existing `intake`, `extract-epub`, `probe-pdf`, `normalize`, and `verify-foundation` commands. Confirm matching content-addressed input hashes and keep every generated file under ignored paths.

- [x] **Step 3: Create a private promotion and leakage review mapping**

`promotion-map.json` maps every one of the fifteen public module IDs to one or more private normalized unit IDs and records only `reviewed` or `validated` maturity. `markers.json` contains the exact input-specific words and identifiers that public content must not contain. Neither file is read by routing, graph construction, manifest construction, or archive contents.

- [x] **Step 4: Build, verify, relocate, and archive the package**

Run:

```powershell
uv run knowledge-forge build-package --workspace . --pack pack --schemas forge/schemas
uv run knowledge-forge verify-package --workspace . --pack pack --schemas forge/schemas --markers private/leakage/markers.json
uv run knowledge-forge archive-package --workspace . --pack pack --schemas forge/schemas --markers private/leakage/markers.json --archive dist/knowledge-package-v0.zip
```

Copy `pack/` to a fresh temporary directory and rerun `verify-package` against the copy using the same marker set. Hash the generated `l0.json`, all L1 files, `canonical.json`, `manifest.json`, and ZIP; rerun the build and assert every digest is identical.

- [x] **Step 5: Inspect boundaries and review the final diff**

Run:

```powershell
git check-ignore -v -- inputs private work derived dist .worktrees
git status --short
git diff --check feature...HEAD
git diff --stat feature...HEAD
```

Confirm the tracked tree contains only code, schemas, canonical pack files, tests, lockfile, and current-status documentation. Confirm no private output is staged or included in `pack/`.

- [x] **Step 6: Record completion and commit the verified v0 state**

Update status text only after all gates pass, then commit the remaining generated canonical package files and documentation status:

```powershell
git add pack docs/superpowers/specs/2026-08-02-portable-agent-knowledge-forge-design.md docs/superpowers/plans/2026-08-02-knowledge-package-v0.md
git commit -m "feat: deliver portable knowledge package v0"
```

## Plan Self-Review

### Spec coverage

- Curated Hungarian L2 content with required metadata and eight body sections: Tasks 1–2.
- Stable IDs, content hashes, compact L0/L1 indexes, canonical graph, and deterministic routing: Task 3.
- Source-neutral allowlist, manifest, marker-based leakage detection, skill structure, and no private directory access: Task 4.
- Relocation, ZIP creation, ZIP-slip defense, exact archive inventory, and package CLI: Task 5.
- Private semantic mapping, actual local review, reproducibility, export boundary, and final status: Task 6.
- Optional UA/Graphify maps are deliberately excluded until the canonical package has passed Task 6, as specified.

### Placeholder scan

The plan contains no deferred implementation markers. Each task names the relevant paths, interfaces, failure expectation, checks, and commit boundary.

### Type consistency

`KnowledgeModule` flows from parsing to package validation, index/graph generation, manifest validation, routing, and archive validation. `PackageManifest` is the sole file allowlist used by both `validate_package` and ZIP creation. All CLI paths are workspace-relative and resolve through the existing `resolve_within` boundary.
