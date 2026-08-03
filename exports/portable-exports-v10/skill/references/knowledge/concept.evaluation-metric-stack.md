---
id: concept.evaluation-metric-stack
title: Értékelési metrikarétegek
kind: concept
maturity: reviewed
confidence: high
language: hu
tags: [evaluation, metrics, quality, cost]
aliases: [eval metrikastack]
relations:
  - type: supports
    target: decision-guide.metric-selection
---
## Lényeg
A metrikarendszer külön rétegen mérje a feladatsikert, részlépéseket, biztonságot, késleltetést, költséget és felhasználói kontrollt.
## Miért működik
Egyetlen átlagpont elrejti, hogy a rendszer milyen áron vagy kockázattal érte el az eredményt.
## Mikor alkalmazd
Agent scorecard, modellválasztás vagy kiadási gate tervezésekor alkalmazd.
## Mikor ne alkalmazd
Ne adj azonos súlyt minden mérőszámnak üzleti és kockázati prioritás nélkül.
## Döntési szabály
Legyen egy elsődleges sikerjel, kötelező guardrail metrikák és diagnosztikai másodlagos jelek.
## Hibamódok
A kompozit pontszám kompenzálhat súlyos biztonsági hibát kis költségjavulással.
## Kapcsolatok
A metric selectiont támogatja; a cost analysis és observability szolgáltat adatot.
## Ellenőrzés
Mutass be olyan példát, ahol minden réteg külön döntési információt ad, és guardrail-sértés nem átlagolható el.
