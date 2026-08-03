---
id: pattern.task-distribution-coverage
title: Feladat-eloszlás lefedettség
kind: pattern
maturity: reviewed
confidence: high
language: hu
tags: [evaluation, tasks, coverage, distribution]
aliases: [task distribution coverage, feladateloszlás lefedettség]
relations:
  - type: depends_on
    target: procedure.evaluation-environment-design
---

## Lényeg

Az értékelési feladatokat ne egy átlagos példára építsd: fedj le könnyű és nehéz esetet, eltérő eszközutat, hibás bemenetet, ritka kivételt és üzletileg fontos szegmenst.

## Miért működik

Az átlagos pontszám elrejtheti, hogy a rendszer egy kritikus kisebbségi esetben használhatatlan vagy veszélyes.

## Mikor alkalmazd

Használd benchmark, regressziós készlet, elfogadási teszt vagy modellválasztási kísérlet összeállításánál.

## Mikor ne alkalmazd

Ne maximalizáld a példák számát lefedettség címén, ha nincs egyértelmű döntés, amelyet az adott feladatcsoport befolyásol.

## Döntési szabály

Minden új példához nevezd meg, mely kockázatot, képességet vagy valós forgalmi szegmenst reprezentál, és melyik meglévő példától különbözik.

## Hibamódok

Az ismétlődő, könnyű feladatok túlértékelik a rendszert, az irreális szélső esetek pedig félreviszik a fejlesztési prioritást.

## Kapcsolatok

Az értékelési környezet adja a keretet, a mérőszám-választás pedig meghatározza, hogyan súlyozd a szegmenseket.

## Ellenőrzés

Készíts lefedettségi táblát feladatkomplexitás, eszközhasználat, kockázat és sikerellenőrzés szerint, majd keresd a hiányzó cellákat.
