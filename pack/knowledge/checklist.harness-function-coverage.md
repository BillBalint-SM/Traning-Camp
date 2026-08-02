---
id: checklist.harness-function-coverage
title: Futtatási keret funkciólefedettsége
kind: checklist
maturity: reviewed
confidence: high
language: hu
tags: [harness, orchestration, state, safety]
aliases: [harness ellenőrzőlista]
relations:
  - type: supports
    target: principle.harness-engineering
---

## Lényeg

A futtatási keretnek külön felelőse legyen a kontextus összeállítására, a döntési ciklusra, az eszközvégrehajtásra, az állapotkezelésre és a biztonsági megszakításra.

## Miért működik

A teljes rendszer kritikus funkciói így nem rejtőznek egyetlen promptban vagy modellválaszban.

## Mikor alkalmazd

Tervezési review, incident utáni elemzés vagy új agent képesség kiadása előtt használd.

## Mikor ne alkalmazd

Ne kezeld merev réteglistaként; kis, determinisztikus workflow-nál az indokolatlan komponensek csak hibapontot adnak.

## Döntési szabály

Minden funkciónál jelöld ki a bemenetet, a tulajdonost, a hibajelet, a visszaállítási utat és a hozzá tartozó mérést.

## Hibamódok

Lefedetlen állapot-, időkorlát- vagy jogosultságkezelés esetén az agent látszólag jól válaszol, de kontrollálhatatlanul fut.

## Kapcsolatok

A harness engineering elvét konkretizálja; az agent task contract és a guardrail tervezés ad hozzá részletes szerződést.

## Ellenőrzés

Egy review táblában minden kritikus futási funkcióhoz legyen felelős komponens, negatív teszt és operatív jel.
