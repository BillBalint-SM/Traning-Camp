# Feedback synthesis — Traning Camp adoption needs

> **Státusz (2026-08-08):** Történeti kutatási szintézis. A felhasználói
> feladatok és guardrailok továbbra is relevánsak, de az `Observed` rész
> repository-, branch- és tesztszám-snapshotjai nem aktuális állapotjelentések.
> Aktuális döntéshez a friss `WORK_STATE` és a merge-elt implementációs bizonyíték
> az irányadó.

**Dátum:** 2026-08-03
**Scope:** a jelenlegi repository-artifactokból és a kutatási feladat céljából levezethető felhasználói igények.
**Bizonyítási szabály:** az `Observed` állítások helyi fájlokra, tesztekre és friss work-state-re támaszkodnak; az `Inferred` állítások következtetések, nem mért felhasználói interjúk.

## 1. Observed project signals

- A portable export egy másolható, source-neutral artifact: Agent Skills, RAG JSONL és graph JSONL formátumot, manifestet és digestet ad.
- A kanonikus csomag jelenlegi snapshotja **193 modulból, 10 területből és 196 kapcsolatból** áll; a package manifest 207 hash-elt fájlt tartalmaz.
- A fogyasztói út v13–v17-ben route → verify/load → receipt → graph-neighborhood → character budget irányban bővült. A boundary read-only és modellfüggetlen.
- Az ambiguity/not-covered útvonalak fail-closed módon üresek maradnak; ez bizalmi és prompt-injection-korlát, nem puszta UX-döntés.
- A routing-evaluation 263 esetet fed le; ez routing- és integritási jel, nem downstream answer-quality vagy runtime-trace mérés.
- A jelenlegi tesztfuttatás teljes kimenete `186 passed` volt, de a 120 másodperces wrapper timeouttal zárult; ezt erős jelként, nem normál exit-code bizonyítékként kell kezelni.
- A v14 specifikáció státusza `Implementing`, miközben a későbbi v16 és v17 specifikációk `Implemented and verified` státuszt jeleznek. Ez dokumentációs bizalom- és onboarding-kockázat.

## 2. Inferred user jobs

1. **Importálni akarok kevés beállítással.** Egy másik agent runtime-ba a csomagolás, verzió-kompatibilitás és betöltés útja legyen egyértelmű és parancsszinten kipróbálható.
2. **Ellenőrizhető kontextust akarok.** A válaszadó agent ne csak szöveget kapjon, hanem route-ot, digestet, modulazonosítót és budget/omission bizonyítékot is.
3. **Korlátozni akarom a kontextus növekedését.** A minimal, deterministic, fail-closed alapértelmezés fontosabb, mint a korlátlan GraphRAG-szerű bővítés.
4. **El akarom kerülni a rejtett platformfüggést.** A canonical package ne legyen MCP-, A2A-, vendor- vagy tokenizer-specifikus; ezek csak opcionális adapterek legyenek.
5. **Látni akarom, hogy valóban jobb lett-e.** A routing pass nem elég: szükséges a context admission, latency/cost, receipt-integrity és downstream answer-quality mérési szerződése.

## 3. Prioritized feedback themes

| Prioritás | Téma | Miért most? | Bizonyíték |
|---|---|---|---|
| P0 | Export/context conformance és verziózási contract | Az importálhatóság az alapérték; adapter nélkül nehéz reprodukálni | Observed + external landscape |
| P0 | Egyértelmű consumer quickstart / install boundary | A portable artifact jelenleg erős, de a „hogyan kötöm be?” út nincs egyetlen szerződésben | Inferred from artifact shape |
| P1 | Runtime-semleges telemetry és answer-level evaluation | A 263 routing eset nem méri a tényleges agent-használati eredményt | Observed gap |
| P1 | Státusz- és dokumentációs konzisztencia | A v14 `Implementing` jelzés félrevezeti a következő implementációt | Observed |
| P2 | Opcionális MCP read-only adapter | Hasznos lehet, de csak a verified `verify/route/load/receipt` boundary fölött | External trend + dependency order |
| P2 | Mélyebb/global GraphRAG, A2A, signed provenance | Nagyobb költség, governance és minőségi kockázat; előbb mérés kell | External trend + risk inference |

## 4. Open questions before build

- Melyik első fogyasztói runtime a referencia: Agent Skills mappa, Python API/CLI, RAG import, vagy graph import?
- A consumer contract mely mezőit kell stabil API-ként verziózni: export format, graph schema, routing-evaluation, receipt és budget?
- A karakterbudget maradjon modellfüggetlen felső korlát, vagy kell külön, explicit tokenizer-adapter?
- Mely downstream sikerkritériumok számítanak: retrieval precision/recall, answer faithfulness, latency, token-cost, vagy ezek kombinációja?
- A telemetry alapértelmezésben csak digest/metaadat legyen, vagy kérhető legyen redaktált modul-szöveg is?
- A dokumentációs státuszokat milyen egyetlen release-gate frissíti, hogy a „planned / implementing / verified” eltérés ne maradjon fenn?

## 5. Guardrails

- A canonical package, derived graph és runtime adapter maradjon külön réteg.
- MCP/A2A eszköz- vagy végrehajtási képesség ne kerüljön be implicit módon a portable exportba.
- A GraphRAG-derived edge/summary ne írja felül a hash-elt, model-free canonical graphot.
- A „kész” állítást csak normál exit-code-dal és a releváns consumer smoke/evaluation gate-ekkel támasszuk alá.
