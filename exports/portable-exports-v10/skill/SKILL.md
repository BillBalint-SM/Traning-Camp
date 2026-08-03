---
name: portable-agent-knowledge
description: Route agent-system questions through the validated knowledge references.
---

# Portable agent knowledge

Before using this skill, verify `../export.json` and its declared file hashes.
Load `references/indexes/l0.json` to select one area, then load only that area's
L1 index and the smallest sufficient modules from `references/knowledge/`.
For an ambiguous question, report the competing areas and request clarification.
For an uncovered question, state that no reliable route exists in this package.
Use `references/graph/canonical.json` only to expand direct relations after a
module has been selected.
