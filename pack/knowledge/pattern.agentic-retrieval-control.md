---
id: pattern.agentic-retrieval-control
title: Agent által vezérelt visszakeresés
kind: pattern
maturity: reviewed
confidence: high
language: hu
tags: [retrieval, agent, tools, verification]
aliases: [agentic RAG vezérlés]
relations:
  - type: depends_on
    target: procedure.retrieval-pipeline-design
---
## Lényeg
Az agent a keresést megfigyelés–lekérdezés–értékelés ciklusban vezesse, ne egyetlen, vak top-k eredményre építsen.
## Miért működik
A keresési hiány, ellentmondás és bizonytalanság új lekérdezéssel vagy eszközzel kezelhető.
## Mikor alkalmazd
Többlépéses kutatásnál és összetett, bizonyítékigényes válasznál alkalmazd.
## Mikor ne alkalmazd
Ne indíts nyílt végű keresési hurkot egyszerű, jól indexelt kérdésre.
## Döntési szabály
Minden keresési lépésnek legyen hipotézise, költségkerete, megállási feltétele és bizonyítékellenőrzése.
## Hibamódok
A kontroll nélküli agent keresési spirál költséget éget és megerősíti saját hibás feltételezését.
## Kapcsolatok
A retrieval pipeline-ra épül, a tool eredményellenőrzés korlátozza a következtetést.
## Ellenőrzés
Mérd a plusz körök által javított válaszarányt, a megállási pontokat és a felesleges hívásokat.
