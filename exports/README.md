# Portable agent knowledge export

`portable-exports-v10/` is a verified, source-neutral interchange artifact.
It can be copied into an agent runtime without the forge workspace.

Use `portable-exports-v10/export.json` as the integrity entrypoint. The
manifest contains the export digest and every profile file hash.

- `skill/` contains the progressive-disclosure Agent Skills profile.
- `rag/` contains complete JSONL documents for retrieval imports.
- `graph/` contains stable nodes and typed edges for graph imports.

The verified export digest is:

```text
bb210e0f528ea31a83c1eeaf6011fdecdbcbd60fa7ed63f99e55be0a456cdcc2
```
