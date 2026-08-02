---
id: decision-guide.memory-capability-evaluation
title: Memóriaképesség értékelése
kind: decision-guide
maturity: reviewed
confidence: high
language: hu
tags: [memory, evaluation, recall, personalization]
aliases: [agent memória értékelés]
relations:
  - type: supports
    target: procedure.user-memory-lifecycle
---

## Lényeg

A memóriát külön értékeld a releváns tény felidézésére, a helyes általánosításra és a nem kívánt vagy elavult emlék elkerülésére.

## Miért működik

A puszta visszahívási arány nem mutatja meg, hogy a rendszer jókor, megfelelő hatáskörben és biztonságosan használja-e az emléket.

## Mikor alkalmazd

Felhasználói preferencia, hosszú távú feladatállapot vagy személyre szabott viselkedés bevezetésekor alkalmazd.

## Mikor ne alkalmazd

Ne mérj valós személyes adattal, ha ugyanaz a döntési tulajdonság szintetikus vagy anonimizált esettel vizsgálható.

## Döntési szabály

Készíts külön tesztet helyes felidézésre, irreleváns emlék elnyomására, elavult adat korrekciójára és törlési kérés utáni viselkedésre.

## Hibamódok

A jó találati arány mellett is káros lehet a memória, ha a modell túl gyakran személyesít, vagy régi adat alapján dönt.

## Kapcsolatok

A felhasználói memória életciklusát támogatja, a hierarchikus memória szervezési dimenziót ad.

## Ellenőrzés

Rögzíts siker-, téves felidézés-, elavulás- és tiltott-felhasználás arányt, majd vizsgáld az eredményt idő és felhasználói helyzet szerint.
