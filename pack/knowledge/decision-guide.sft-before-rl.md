---
id: decision-guide.sft-before-rl
title: SFT az RL előtt
kind: decision-guide
maturity: reviewed
confidence: medium
language: hu
tags: [sft, rl, sequencing]
aliases: [sft-t rl előtt]
relations:
  - type: depends_on
    target: principle.sft-behavior-imitation
---

## Lényeg

Az RL előtt akkor érdemes SFT-t használni, ha a modell még nem képes stabilan előállítani értékelhető, szabályos és releváns cselekvéseket.

## Miért működik

Az SFT használható kezdeti viselkedési eloszlást ad, így az RL nem égeti el a mintákat nyilvánvalóan hibás vagy formailag érvénytelen próbálkozásokra.

## Mikor alkalmazd

Válaszd eszközhívási formátum, alapfolyamat vagy biztonsági konvenció kialakítására a céloptimalizálás előtt.

## Mikor ne alkalmazd

Hagyd ki, ha a kiinduló modell már megfelelően felfedezi a cselekvési teret, a demonstrációk pedig gyengébbek lennének a saját jó próbáinál.

## Döntési szabály

Ha a baseline futások nagy része nem jut el érvényesen pontozható állapotig, stabilizálj SFT-vel; ha eljut, közvetlenül vizsgáld az RL-t.

## Hibamódok

A túl sok SFT beszűkítheti a feltárást, a rossz demonstráció pedig olyan lokális optimumhoz kötheti a modellt, amelyet az RL nehezen hagy el.

## Kapcsolatok

A döntés az SFT demonstrációs természetére épül.

## Ellenőrzés

Hasonlítsd össze az érvényes trajektóriák arányát és a felfedezési változatosságot SFT előtt és után.
