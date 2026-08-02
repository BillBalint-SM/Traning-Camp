---
id: procedure.agent-cost-analysis
title: Agent teljesköltség-elemzése
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [agent, cost, latency, tools]
aliases: [agent teljes futási költségét]
relations:
  - type: supports
    target: decision-guide.model-selection-dimensions
---
## Lényeg
Az agent költségébe számítsd bele a modell-tokeneket, tool-hívást, retry-t, infrastruktúrát, emberi felügyeletet, késleltetést és hibás futás korrekcióját.
## Miért működik
A válaszonkénti modellár csak egy része a teljes feladat sikeres lezárásához szükséges ráfordításnak.
## Mikor alkalmazd
Modellválasztás, kapacitástervezés vagy optimalizálás előtt alkalmazd.
## Mikor ne alkalmazd
Ne hasonlíts költséget eltérő sikerrátájú vagy minőségi küszöbű rendszerek között normalizálás nélkül.
## Döntési szabály
Számíts sikeres, ellenőrzött feladatra jutó teljes költséget és külön tail-költséget a hibás, hosszú futásokra.
## Hibamódok
A retry, cache-miss, külső API és emberi review kihagyása mesterségesen olcsó rendszert mutat.
## Kapcsolatok
A model selection dimensions döntését támogatja; az observability adja a futási adatot.
## Ellenőrzés
Egyeztesd a számított költséget valós számlázási és futási naplómintával, majd bontsd fel feladattípus szerint.
