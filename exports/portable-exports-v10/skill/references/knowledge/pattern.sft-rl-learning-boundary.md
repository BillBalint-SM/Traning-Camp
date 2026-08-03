---
id: pattern.sft-rl-learning-boundary
title: SFT és RL tanulási határ
kind: pattern
maturity: reviewed
confidence: high
language: hu
tags: [post-training, sft, rl, learning]
aliases: [sft rl boundary, sft rl határ]
relations:
  - type: supports
    target: decision-guide.sft-or-rl
---

## Lényeg

SFT-vel tanítsd meg a kívánt válaszformát, eszközhívási mintát vagy példaszerű viselkedést; RL-t akkor használj, ha a több lépéses döntési út következményét környezetben és visszajelzéssel lehet mérni.

## Miért működik

Az SFT a demonstrációt másolja, az RL a visszacsatolás alapján választ viselkedést; a kettő más információt és más hibát kezel.

## Mikor alkalmazd

Használd képességhiány diagnózisánál, amikor el kell dönteni, hogy adatpélda, környezet, jutalomjel vagy futtatási keret a szűk keresztmetszet.

## Mikor ne alkalmazd

Ne indíts RL-t, ha nincs megbízható környezet vagy mérhető jutalom, és ne várj SFT-től stabil hosszú távú optimalizációt csak több példától.

## Döntési szabály

Ha egy szakértő rövid, ellenőrizhető demonstrációban meg tudja mutatni a helyes választ, kezdd SFT-vel; ha a minőség csak a következményből látszik, építs előbb értékelhető környezetet.

## Hibamódok

A gyenge jutalomra optimalizált RL kihasználhatja a mérőt, az irreleváns vagy zajos SFT-adat pedig megerősítheti a hibás mintát.

## Kapcsolatok

Az adat és környezet elsődlegessége korlátozza, az értékelési környezet pedig a valós visszajelzés alapja.

## Ellenőrzés

Hasonlítsd össze a demonstrációs, a környezeti és az éles feladaton mért teljesítményt, és csak azonos sikerdefiníció mellett vonj le tanulási következtetést.
