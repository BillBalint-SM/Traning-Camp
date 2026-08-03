---
id: decision-guide.voice-architecture-selection
title: Hanginterakciós architektúra választása
kind: decision-guide
maturity: reviewed
confidence: high
language: hu
tags: [voice, multimodal, realtime, interaction]
aliases: [voice architecture selection, hangarchitektúra választás]
relations:
  - type: applies_to
    target: concept.multimodal-interaction-boundary
---

## Lényeg

Kaszkádos hangláncot válassz, ha az átláthatóság és a komponensenkénti kontroll fontos; egységes multimodális modellt, ha a kontextus és a természetes váltás fontosabb; teljes duplex megoldást, ha a megszakítás és az egyidejű beszéd elsőrendű követelmény.

## Miért működik

A három architektúra eltérően kezeli a késleltetést, a hibadiagnózist, a kontextusátadást és az interakció természetességét.

## Mikor alkalmazd

Használd hangalapú ügyintéző, asszisztens, valós idejű beszélgetés vagy multimodális interfész megtervezésekor.

## Mikor ne alkalmazd

Ne válassz teljes duplex rendszert csak a látvány kedvéért, ha a feladat természeténél fogva turn-based és az üzleti érték az ellenőrizhetőségben van.

## Döntési szabály

Ha fontos a komponensenkénti audit és javítás, kezdd kaszkáddal; ha az átadott kontextus elvesztése a fő hiba, vizsgálj egységes modellt; ha a felhasználó gyakran félbeszakít, tervezz duplex megszakításkezelést.

## Hibamódok

A túl hosszú lánc hangból szövegbe és vissza késleltetést vagy jelentésvesztést okoz, a túl egységes megoldás pedig nehezítheti a hibakeresést.

## Kapcsolatok

A gyors–lassú interakciós hurok az architektúra válaszidejét egészíti ki, a multimodális határ pedig a modalitások közötti bizonytalanságot kezeli.

## Ellenőrzés

Mérd külön a megszakítási késleltetést, a félreértési arányt, a végponttól végpontig tartó választ és a felhasználó által korrigált fordulatok arányát.
