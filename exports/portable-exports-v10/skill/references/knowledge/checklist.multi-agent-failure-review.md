---
id: checklist.multi-agent-failure-review
title: Multi-agent hibafelülvizsgálat
kind: checklist
maturity: reviewed
confidence: medium
language: hu
tags: [failure, review, multi-agent]
aliases: [multi agent hibamód audit]
relations:
  - type: supports
    target: failure-mode.multi-agent-error-amplification
---

## Lényeg

Vizsgáld az eredeti hibát, első továbbadást, ellenőrzési pontokat, tulajdonost, párhuzamos konfliktust, retryt, végső hatást és containmentet.

## Miért működik

A lista megkülönbözteti a lokális modellhibát a koordináció által létrehozott vagy felerősített hibától.

## Mikor alkalmazd

Futtasd minden több-agent incidens és jelentős regresszió után.

## Mikor ne alkalmazd

Ne állj meg az utolsó hibázó agentnél, ha a korábbi handoff vagy közös állapot okozta a helyzetet.

## Döntési szabály

Az első hiányzó vagy hibás kontrollpont legyen a javítás elsődleges célja.

## Hibamódok

Személyes hibáztatás, hiányos trace és korrelációs azonosító nélküli log téves gyökérokot adhat.

## Kapcsolatok

A lista a multi-agent hibafelerősítés ismert kockázatát vizsgálja.

## Ellenőrzés

Játsszd vissza az üzenet- és állapotsort, majd bizonyítsd, hogy az új kontroll megszakítja a láncot.
