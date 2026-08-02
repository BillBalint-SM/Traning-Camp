---
id: procedure.ablation-and-experiment-loop
title: Ablációs és kísérleti hurok
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [evaluation, ablation, experiment, regression]
aliases: [ablation experiment, ablációs kísérlet]
relations:
  - type: depends_on
    target: decision-guide.metric-selection
---

## Lényeg

Egy kísérletben egyszerre egy feltételezett hatású változót módosíts, tartsd állandón a környezetet, és előre rögzítsd, milyen mérés igazol vagy cáfol.

## Miért működik

Az abláció elválasztja a valódi mechanizmust a véletlen javulástól vagy a több egyidejű változás összhatásáról szóló történettől.

## Mikor alkalmazd

Használd új prompt, eszköz, modell, kontextusstratégia, guardrail vagy orchestration elem bevezetésekor.

## Mikor ne alkalmazd

Ne várj tökéletes izolációt valós rendszerben; ha nem izolálható minden tényező, rögzítsd a bizonytalanságot és csökkentsd a következtetés erejét.

## Döntési szabály

Minden változtatáshoz legyen kontroll, célmérés, korlátmérés, előre rögzített döntési küszöb és visszavonási feltétel.

## Hibamódok

A több változó egyidejű módosítása, a kiválasztott példák utólagos szűkítése és a csak átlagot néző értékelés hamis okságot mutat.

## Kapcsolatok

A mérőszám-választást használja, az observability pedig a nem várt regressziók magyarázatát támogatja.

## Ellenőrzés

Ugyanaz a hipotézis kontrollált újrafuttatásban is ugyanabba az irányba mozdítsa a fő- és korlátmutatókat, vagy a kiadás maradjon visszatartva.
