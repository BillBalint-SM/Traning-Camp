---
id: procedure.pairwise-model-ranking
title: Páronkénti modellrangsorolás
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [evaluation, ranking, models, pairwise]
aliases: [modellek páros összehasonlítása]
relations:
  - type: supports
    target: decision-guide.agent-model-selection
---
## Lényeg
Két rendszer válaszát ugyanazon feladaton, vakon és kiegyensúlyozott bemutatási sorrendben hasonlítsd össze, majd aggregáld a preferenciákat.
## Miért működik
A relatív választás gyakran stabilabb, mint az abszolút skála, különösen szubjektív minőségnél.
## Mikor alkalmazd
Közeli modellek, promptok vagy agent-változatok rangsorolásakor alkalmazd.
## Mikor ne alkalmazd
Ne rangsorolj eltérő feladatmintán vagy eltérő tool-környezettel futott rendszereket.
## Döntési szabály
Randomizáld a sorrendet, engedd a döntetlent, és tarts külön eredményt feladatszegmensenként.
## Hibamódok
A pozíciótorzítás és a nem független párok hamis rangsort adnak.
## Kapcsolatok
Az agent model selectiont támogatja és a judge calibration pontosságától függ.
## Ellenőrzés
Sorrendcserével és ismétléssel mérd a preferencia stabilitását és a konfidenciaintervallumot.
