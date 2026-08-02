---
id: pattern.domain-randomization
title: Környezeti variációs randomizáció
kind: pattern
maturity: reviewed
confidence: high
language: hu
tags: [simulation, robustness, randomization, evaluation]
aliases: [domain randomization]
relations:
  - type: supports
    target: decision-guide.simulation-fidelity
---
## Lényeg
A szimuláció nem kritikus vizuális, időzítési és környezeti paramétereit kontrollált eloszlásból változtasd, hogy a rendszer ne egyetlen fixture-re illeszkedjen.
## Miért működik
A változatosság a stabil feladatjelek használatára kényszerít, és láthatóvá teszi a környezeti törékenységet.
## Mikor alkalmazd
GUI-, robotikai-, hang- vagy változó külső környezetű agent értékelésekor alkalmazd.
## Mikor ne alkalmazd
Ne randomizáld a sikerkritériumot vagy olyan változót, amely a feladat jelentését módosítja.
## Döntési szabály
Csak valós tartományból mintázz, verziózd a seedet és jelents eredményt eloszlás szerint.
## Hibamódok
A túl széles vagy irreális randomizáció értelmetlen nehézséget, a túl szűk pedig hamis robusztusságot ad.
## Kapcsolatok
A simulation fidelity döntését támogatja és a task distribution coverage környezeti dimenziója.
## Ellenőrzés
Mérd a teljesítményeloszlást seed és paramétertartomány szerint, majd validáld valós mintán.
