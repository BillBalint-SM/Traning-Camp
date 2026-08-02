---
id: procedure.tool-call-reinforcement-learning
title: Eszközhívás megerősítéses tanítása
kind: procedure
maturity: reviewed
confidence: medium
language: hu
tags: [tool-calling, rl, execution]
aliases: [megerősítéses tanulással a tool callingot]
relations:
  - type: depends_on
    target: procedure.tool-contract-design
---

## Lényeg

Az eszközhívási RL-t stabil sémára, izolált végrehajtásra, állapot-visszaolvasásra és feladatszintű jutalomra építsd.

## Miért működik

A modell nem csak a hívás formátumát, hanem a kiválasztás, argumentumadás, eredményértelmezés és folytatás következményét tanulja.

## Mikor alkalmazd

Használd, ha több érvényes eszközstratégia közül a teljes végrehajtási eredmény alapján kell választani.

## Mikor ne alkalmazd

Ne engedj tanulási futást produkciós jogosultsággal, visszafordíthatatlan műveletekkel vagy nem izolált adatokon.

## Döntési szabály

Előbb érd el a formai érvényességet és a sandbox-biztonságot, majd a feladatsikert optimalizáld RL-lel.

## Hibamódok

A modell üres sikerjelzést, olcsó eszközt vagy környezeti hibát optimalizálhat a valódi feladat helyett.

## Kapcsolatok

Az eljárás a stabil és explicit eszközszerződésre épül.

## Ellenőrzés

Mérd külön az eszközválasztást, sémaérvényességet, végrehajtási sikert, állapotváltozást, költséget és tiltott próbálkozást.
