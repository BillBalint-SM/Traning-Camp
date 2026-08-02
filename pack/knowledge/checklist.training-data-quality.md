---
id: checklist.training-data-quality
title: Tanítási adatminőség ellenőrzése
kind: checklist
maturity: reviewed
confidence: medium
language: hu
tags: [training-data, quality, governance]
aliases: [tanítóadat minőségi kapu]
relations:
  - type: supports
    target: procedure.sft-data-pipeline
---

## Lényeg

Ellenőrizd a relevanciát, helyességet, sokféleséget, duplikációt, nehézségi eloszlást, jogosultságot, személyes adatot és train–test szeparációt.

## Miért működik

A többdimenziós kapu megakadályozza, hogy a rekordmennyiség elfedje az ismétlődő vagy hibás tanulási jelet.

## Mikor alkalmazd

Futtasd minden adatkészlet-verzió befagyasztása előtt és minden jelentős adatforrás-változás után.

## Mikor ne alkalmazd

Ne elégedj meg csak automatikus statisztikával olyan tartalomnál, amely szakértői helyességet vagy biztonsági megítélést igényel.

## Döntési szabály

Az adatkészlet csak akkor adható tovább, ha minden kötelező kapu mért eredménye és elutasítási oka visszaolvasható.

## Hibamódok

Rejtett sablonismétlés, benchmark-szivárgás, többségi torzítás és hibás negatív példa túlbecsült teljesítményt okoz.

## Kapcsolatok

Az ellenőrzőlista az SFT adatfolyamat minőségi kapuja.

## Ellenőrzés

Őrizd meg a metrikákat, mintákat, annotátori egyezést, deduplikációs kulcsot és a kizárt rekordok okeloszlását.
