---
id: decision-guide.reward-signal-density
title: Jutalomjel sűrűségének kiválasztása
kind: decision-guide
maturity: reviewed
confidence: medium
language: hu
tags: [reward, density, learning]
aliases: [sűrű vagy ritka jutalomjel]
relations:
  - type: depends_on
    target: concept.multi-turn-credit-assignment
---

## Lényeg

A jutalom sűrűsége kompromisszum: a gyakori jel gyorsabb tanulást, a ritka céljel nagyobb célhűséget adhat.

## Miért működik

A tudatos választás csökkenti a varianciát anélkül, hogy a modell kizárólag könnyen kijátszható köztes proxykat optimalizálna.

## Mikor alkalmazd

Válaszd meg többfordulós feladat vagy hosszú horizontú tanítás előtt.

## Mikor ne alkalmazd

Ne adj minden lépésre jutalmat pusztán azért, mert mérhető; a mérhetőség nem bizonyít célkapcsolatot.

## Döntési szabály

Kezdj a legközvetlenebb végjellel, majd csak olyan köztes jutalmat adj hozzá, amely kontrollált kísérletben javítja a végcélt.

## Hibamódok

Jutalomfarmolás, lépésszám-optimalizálás és túl korai befejezés jelenhet meg rosszul választott sűrűségnél.

## Kapcsolatok

A döntés a kredit-hozzárendelési problémára épül.

## Ellenőrzés

Hasonlítsd össze a jutalomgörbét a független végsikerrel és vizsgáld a köztük növekvő eltérést.
