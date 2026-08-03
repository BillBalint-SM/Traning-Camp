---
id: pattern.task-complexity-ladder
title: Feladatkomplexitási létra
kind: pattern
maturity: reviewed
confidence: high
language: hu
tags: [evaluation, complexity, tasks, coverage]
aliases: [eval komplexitási szintek]
relations:
  - type: supports
    target: pattern.task-distribution-coverage
---
## Lényeg
Építs feladatlépcsőt egyetlen döntéstől több eszközön, hosszú horizonton és bizonytalan visszajelzésen át az összetett feladatig.
## Miért működik
A teljesítmény töréspontja megmutatja, melyik koordinációs vagy kontextusképesség hiányzik.
## Mikor alkalmazd
Képességhatár, modellkülönbség vagy regresszió lokalizálásakor alkalmazd.
## Mikor ne alkalmazd
Ne tekintsd a hosszabb feladatot automatikusan nehezebbnek, ha a lépések függetlenek vagy determinisztikusak.
## Döntési szabály
Egyszerre csak egy komplexitási dimenziót emelj: lépésszámot, eszközválasztást, bizonytalanságot vagy állapotfüggést.
## Hibamódok
Az összekevert nehézségi dimenziók nem mutatják meg a romlás okát.
## Kapcsolatok
A task distribution coverage-et támogatja és az ablation loophoz ad diagnosztikai szeleteket.
## Ellenőrzés
Mérd a sikergörbét szintenként, és igazold, hogy a szintek között egy deklarált dimenzió változik.
