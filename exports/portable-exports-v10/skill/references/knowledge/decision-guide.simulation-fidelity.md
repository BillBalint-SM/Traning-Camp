---
id: decision-guide.simulation-fidelity
title: Szimulációs hűség választása
kind: decision-guide
maturity: reviewed
confidence: high
language: hu
tags: [evaluation, simulation, fidelity, environment]
aliases: [szimuláció hűség trade-off]
relations:
  - type: supports
    target: procedure.evaluation-environment-design
---
## Lényeg
A szimuláció hűségét ahhoz a döntéshez válaszd, amelyet mérni akarsz: csak a kimenetet befolyásoló környezeti részleteket modellezd pontosan.
## Miért működik
A kisebb szimuláció olcsó és gyors, a kritikus valósághű rész pedig megőrzi a mérés külső érvényességét.
## Mikor alkalmazd
Drága, veszélyes, lassú vagy nehezen ismételhető környezet értékelésekor alkalmazd.
## Mikor ne alkalmazd
Ne következtess valós teljesítményre olyan szimulációból, amely a rendszer fő hibaforrását kihagyja.
## Döntési szabály
Azonosítsd a döntésérzékeny változókat, modellezd őket, a többit egyszerűsítsd és jelöld korlátnak.
## Hibamódok
A szimulációs rés kihasználható shortcutot tanít vagy irreális sikerrátát mutat.
## Kapcsolatok
Az evaluation environment designot támogatja; a domain randomization a túlillesztést csökkenti.
## Ellenőrzés
Kis valós mintán hasonlítsd a hibamódok, rangsorok és teljesítménytrendek egyezését.
