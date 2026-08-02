---
id: decision-guide.metric-selection
title: Agent mérőszám választása
kind: decision-guide
maturity: reviewed
confidence: high
language: hu
tags: [evaluation, metrics, quality, cost]
aliases: [metric selection, mérőszám választás]
relations:
  - type: depends_on
    target: procedure.agent-evaluation-loop
---

## Lényeg

Olyan mérőszámot válassz, amely a felhasználói célt, a biztonsági korlátot és az operációs költséget együtt tükrözi, nem csak a modell szövegminőségét.

## Miért működik

Egyetlen pontszám könnyen optimalizálható a valódi cél rovására; a kiegyensúlyozott metrikarendszer láthatóvá teszi a trade-offot.

## Mikor alkalmazd

Használd modellválasztásnál, promptváltoztatásnál, eszközbővítésnél és kiadási döntésnél.

## Mikor ne alkalmazd

Ne mérj mindent, amit könnyű mérni; a nem döntéstámogató metrika zajt és optimalizálási torzítást okoz.

## Döntési szabály

Minden fő mutató mellé tegyél egy korlátmutatót: például a sikerarány mellé költséget, a gyorsaság mellé hibaarányt, az autonómia mellé emberi beavatkozást.

## Hibamódok

A proxy-metrika önálló célként való kezelése, az eltérő feladatszegmensek összevonása és a bizonytalan mérésből levont erős következtetés félrevezető.

## Kapcsolatok

Az ablációs kísérlet validálja, a feladat-eloszlás pedig kontextusba helyezi a mutatókat.

## Ellenőrzés

Mutasd ki, hogy a választott metrika rangsora összhangban van-e független, emberileg ellenőrzött sikerpéldákkal és a nem kívánt mellékhatásokkal.
