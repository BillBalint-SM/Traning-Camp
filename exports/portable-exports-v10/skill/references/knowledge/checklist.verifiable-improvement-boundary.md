---
id: checklist.verifiable-improvement-boundary
title: Ellenőrizhető fejlődés határa
kind: checklist
maturity: reviewed
confidence: medium
language: hu
tags: [verification, improvement, metrics]
aliases: [kész nem jelent fejlődést]
relations:
  - type: supports
    target: procedure.statistical-significance-check
---

## Lényeg

Ellenőrizd, hogy a feladat befejezése valódi célértéket, független végállapotot, reprezentatív eloszlást és statisztikailag értelmezhető javulást jelent-e.

## Miért működik

A lista elválasztja a végrehajtási státuszt a felhasználói vagy rendszerszintű eredménytől.

## Mikor alkalmazd

Használd minden automatikus promóciós szabály és fejlődési KPI tervezésekor.

## Mikor ne alkalmazd

Ne tekints egyetlen sikeres futást, magas proxyértéket vagy tesztbefejezést önmagában fejlődésnek.

## Döntési szabály

Fejlődést csak független baseline-hoz, előre rögzített metrikához és guardrailhez viszonyított ismételt eredmény igazolhat.

## Hibamódok

Goodhart-hatás, szelektív mintavétel, késleltetett kár és eloszlásváltás hamis pozitív fejlődést mutathat.

## Kapcsolatok

Az ellenőrzőlista a statisztikai szignifikancia vizsgálatát egészíti ki szemantikai eredményhatárral.

## Ellenőrzés

Kérj független végállapotot, kontrollcsoportot, konfidenciaintervallumot és külön biztonsági metrikát.
