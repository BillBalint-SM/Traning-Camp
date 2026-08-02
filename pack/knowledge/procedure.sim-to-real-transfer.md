---
id: procedure.sim-to-real-transfer
title: Szimulációból valós rendszerbe átvitel
kind: procedure
maturity: reviewed
confidence: medium
language: hu
tags: [sim-to-real, robotics, validation]
aliases: [sim2real átviteli rés]
relations:
  - type: depends_on
    target: pattern.domain-randomization
---

## Lényeg

Mérd a szimulációs rést, randomizáld a bizonytalan fizikai paramétereket, kalibrálj valós mintán, majd fokozatos korlátokkal növeld a valós kitettséget.

## Miért működik

A változatosság csökkenti az egyetlen szimulátor sajátosságaira túlillesztést, a valós kalibráció pedig megmutatja a maradék rést.

## Mikor alkalmazd

Használd fizikai vagy eszközközeli politika valós telepítése előtt.

## Mikor ne alkalmazd

Ne tekints szimulációs sikert valós biztonsági bizonyítéknak.

## Döntési szabály

Valós rollout csak előre rögzített résküszöb, védőkorlát, emberi felügyelet és azonnali leállítás mellett indulhat.

## Hibamódok

Szenzorzaj, súrlódás, késés, hardverszórás és ismeretlen környezeti esemény súlyos eloszlásváltást okoz.

## Kapcsolatok

Az eljárás a domain randomizációs mintára épül.

## Ellenőrzés

Vezess szimuláció–valós páros metrikát, kanári feladatot, incidensnaplót és automatikus leállítási próbát.
