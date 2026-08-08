# Trend landscape memo — portable agent knowledge and context injection

> **Státusz (2026-08-08):** Történeti kutatási snapshot. A repository- és
> protokollállítások a 2026-08-03-i állapotot rögzítik; új döntéshez mindig a
> friss `WORK_STATE` és az aktuális elsődleges specifikáció az irányadó. A memo
> megállapításai a kapcsolódó feedback-szintézis és sprintjavaslat kiindulópontjai.

**Dátum:** 2026-08-03
**Scope:** portable, agent-agnostic knowledge/context injection; graph/RAG; multi-agent orchestration; evaluation; reproducible exports.
**Módszer:** a repository jelenlegi állapotának helyi ellenőrzése és elsődleges, hivatalos specifikációk/dokumentációk célzott áttekintése. A külső állítások nem tekintendők a projekt saját szerződésének.

## 1. Mi van már a Traning Campben?

Helyi `WORK_STATE` preflight: `feature`, `bde65e195f2ea8ce03887c10251df4d903b77f09`, clean worktree, `origin/feature` upstream (2026-08-03 14:44 UTC).

- A kanonikus csomag `pack/manifest.json`-ben hash-elt fájllistát és csomag-digestet tartalmaz; a helyi export manifestje szerint **193 modul, 10 terület, 196 kapcsolat**.
- A `pack/skills/SKILL.md` determinisztikus, progressive-disclosure routing protokollt ad: L0 → egy L1 → legkisebb elégséges modul; ambiguity/not-covered és közvetlen graph-expansion szabályokkal.
- A v10–v12 szerződések három hordozható profilt (Agent Skills, RAG JSONL, graph JSONL), teljes export-verifikációt és read-only delta jelentést adnak.
- A v13–v17 irány a fogyasztó oldali route/load/receipt/graph-neighborhood/budget boundary: verifikált export, modulonkénti hash receipt, 0/1-hop determinisztikus bővítés, legfeljebb 100 000 karakteres budget; nincs modellhívás, embedding, vector DB vagy runtime-adapter.
- A routing-evaluation 263 esettel méri a canonical/paraphrase/negative/ambiguous útvonalakat. Ez routing- és integritásbizonyíték, nem válaszminőség- vagy runtime-trace bizonyíték.

## 2. Külső trendjelek és következményük

| Trend | Elsődleges jel, recency | Mit jelent a projektre nézve? |
|---|---|---|
| **Agent Skills mint hordozható konvenció** | Az [Agent Skills specifikáció](https://agentskills.io/specification) háromlépcsős progressive disclosure-t ír le (metadata, aktivált `SKILL.md`, szükség szerinti `references/`/`scripts/`/`assets/`), relatív hivatkozásokat és `skills-ref validate` ellenőrzést; a specifikáció 2026-08-03-án frissen olvasható. **Bizalom: magas a formátumra, közepes az ökoszisztéma-adoptációra.** | A v10 export és a v13 route entrypoint jó irányban van. Kis, olcsó gate: a generált `skill/SKILL.md` hivatalos `skills-ref` validálása és a metadata/reference closure külön jelentése. A progressive disclosure-t és az automatikus context-betöltés tilalmát meg kell tartani. |
| **MCP: context és eszközök külön kontrollsíkja** | A jelenlegi [MCP 2025-11-25 specifikáció](https://modelcontextprotocol.io/specification/2025-11-25) és [server overview](https://modelcontextprotocol.io/specification/2025-11-25/server/index) a `Prompts` (user-controlled), `Resources` (application-controlled) és `Tools` (model-controlled) primitíveket választja szét, valamint explicit consent-, privacy- és tool-safety elveket ír elő. **Bizalom: magas; protocol-version drift: kezelendő.** | A portable export maradjon artifact, ne váljon implicit MCP-szerverré. Későbbi, opcionális read-only MCP resource adapter természetes illesztés lehet a `verify/load/receipt` API-ra; tool-oldali írás/végrehajtás csak külön policy- és consent-szerződéssel. |
| **Agent–agent interoperability (A2A) és semleges governance** | A [Linux Foundation A2A announcement](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents) (2025-06-23) és az [A2A specifikáció](https://github.com/a2aproject/A2A/blob/main/docs/specification.md) async-first task lifecycle-t, AgentCardot, artifactokat és opaque executiont definiál. Az [AAIF bejelentése](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation?hs_amp=true) (2025-12-09) MCP-t, goose-t és AGENTS.md-t semleges alapítványi környezetbe helyezett. **Bizalom: magas a szabványosítási jelre, közepes az érettségre.** | Ez runtime-interoperabilitás, nem tudás-export formátum. A jövőben egy export capability/AgentCard leírhatná, hogy milyen route/load műveletet kínál, de most nem érdemes a v17 artifactot A2A task-protokollal összekeverni. |
| **GraphRAG: local/global/DRIFT retrieval** | A [Microsoft GraphRAG query overview](https://microsoft.github.io/graphrag/query/overview/) local search-t (KG + text chunks), global search-t (community reports, map-reduce) és DRIFT search-t (community-guided follow-up) különíti el; a global út resource-intensive. A [GraphRAG tanulmány](https://arxiv.org/abs/2404.16130) globális, corpus-szintű kérdéseknél javulást ír le naïve RAG-hoz képest. **Bizalom: magas a módszertani jelre, közepes a konkrét domain-átvihetőségre.** | A v16 egy-hop, determinisztikus expansionje jó, kontrollált local baseline. Global/community summary vagy LLM-derived graph csak külön, derived rétegként és fixture-alapú benchmark után jöjjön; a kanonikus, hash-elt gráfot ne keverjük model-generated élekkel. |
| **Multi-agent orchestration: workflow előbb, autonómia csak indokoltan** | Anthropic különbséget tesz workflow és runtime-döntést hozó agent között az [Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents) anyagban. Ugyanez a vendor 2026-os architekturális útmutatója a költségkorlátokra hívja fel a figyelmet: multi-agent rendszerek kb. 10–15× tokenhasználatot és hosszabb delivery-t igényelhetnek ([PDF, pp. 22–23](https://resources.anthropic.com/hubfs/Building%20Effective%20AI%20Agents-%20Architecture%20Patterns%20and%20Implementation%20Frameworks.pdf)). **Bizalom: közepes; vendor guidance, nem független benchmark.** | A Traning Camp export legyen semleges substrate bármely orchestratorhoz. A route/load/budget határ most jobb kontrollpont, mint a manager-worker logika beégetése. Következő mérés: ugyanaz a context fixture single-agent/workflow/multi-agent fogyasztókkal, token-, latency- és quality-gate-ekkel. |
| **RAG- és agent-evaluation a retrievalen túl** | Az [ARES (NAACL 2024)](https://aclanthology.org/2024.naacl-long.20/) context relevance, answer faithfulness és answer relevance dimenziókat mér; synthetic judge-okat kis emberi kalibrációval használ. Az [OpenAI Agents SDK tracing](https://openai.github.io/openai-agents-python/tracing/) trace/span szinten rögzíthet generation, tool-call, handoff és guardrail eseményeket, érzékeny adatkapcsolóval. **Bizalom: magas az elvekben; vendor tracing csak egy lehetséges runtime.** | A jelenlegi 263 routing eset nem answer-level eval. Hasznos, modell-független következő réteg: route recall/precision, admitted/omitted module, budget adherence, receipt-digest és downstream answer-eval adapterenként. A receipt digest legyen trace metadata, a modul teljes szövege pedig csak explicit policy mellett kerüljön trace-be. |
| **Reproducible export + provenance** | A [Reproducible Builds planning guide](https://reproducible-builds.org/docs/plans/) byte-for-byte újraépítést, környezeti varianciák kezelését és egyszerű összehasonlítási protokollt kér. A [SLSA provenance spec](https://slsa.dev/spec/v1.0-rc1/provenance) az artifact digestet a build/source/dependency provenance-hoz köti. **Bizalom: magas az integritási alapelvben.** | A v10–v12 per-file hash + export digest már erős reproducibility/integrity alap. Hiányzó, külön scope-ba való lehetőség: aláírt in-toto/SLSA attestation és build-environment leírás. A digest önmagában integrity receipt, nem hitelesség, ha a várt digest nincs trusted csatornán rögzítve. |

## 3. Gaps és lehetőségek (prioritás szerint)

### Most — kis, bizonyíték-alapú javítások

1. **Skill conformance:** a generated Agent Skills profilt futtassuk hivatalos `skills-ref` validatorral; rögzítsük a validációt a portable-export gate-ben.
2. **Context conformance:** a routing gate mellé modell nélküli fixture-ek: kiválasztott modul-id-k, hash receipt, graph endpoint closure, admitted/omitted budget és determinisztikus byte-output.
3. **Version pinning:** az export manifestben és a fogyasztói receiptben legyen explicit export format, graph schema és routing-evaluation verzió; a külső MCP/A2A protokollverziót ne hagyjuk implicitnek.

### Next — csak mérés után

4. **Optional runtime telemetry contract:** egy kis, vendor-semleges JSONL trace, amely query hash-t, route státuszt, export/module digestet, budgetet és időzítést tartalmaz, de alapértelmezésben nem küld tartalmat.
5. **Graph strategy benchmark:** depth-1 direct neighborhood kontra külön derived local/global/community index; a kanonikus graph maradjon változatlan és model-free.
6. **Optional MCP resource adapter:** `verify`, `route`, `load` és `receipt` read-only erőforrásként; tool/írási út külön security reviewval.

### Later — külső governance vagy erős biztonsági igény esetén

7. **A2A capability descriptor/AgentCard:** csak akkor, ha a rendszer ténylegesen agentek között delegál, nem pusztán exportot ad át.
8. **SLSA/in-toto attestation vagy OCI artifact packaging:** akkor éri meg, ha több, egymástól független build/publisher vagy registry jelenik meg.

## 4. Döntési guardrailok

- A standardok nem azonosak: Agent Skills = hordozható skill-folder convention; MCP = runtime context/tool protocol; A2A = agent–agent task protocol. Egyik sem helyettesíti a kanonikus package/manifest/receipt szerződést.
- A v17 karakterbudget nem tokenizer- vagy modell-token budget. Token-aware adapter csak deklarált tokenizerrel, mérhető overflow/latency tesztekkel és explicit failure móddal jöjjön.
- A GraphRAG model-generated summaries/edges minőségi és költségkockázatot hoznak. Derived output és kanonikus output külön hash-/promotion-gate nélkül nem keverhető.
- MCP és Agent Skills `scripts/`/tools használatakor a csomagolt tartalom nem megbízható utasítás: default legyen read-only, no implicit execution, explicit user consent.

## 5. Confidence / recency

- **Repository facts:** magas bizalom; helyi fájlok és preflight, 2026-08-03.
- **Normative protocol/format claims:** magas bizalom; hivatalos specifikációk és vendor dokumentációk, frissen ellenőrizve 2026-08-03-án.
- **Architecture/cost/adoption claims:** közepes bizalom; főként vendor guidance vagy 2024–2025-ös kutatás, ezért domain- és runtime-függők.
- **Recommendation confidence:** a Skills + digest + read-only boundary megtartása magas; MCP/A2A adapter, global GraphRAG és signed provenance alacsonyabb, feltételes (mérési és governance-jel szükséges).
