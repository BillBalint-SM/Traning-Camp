---
id: pattern.on-policy-distillation
title: Saját eloszlású tanár-desztilláció
kind: pattern
maturity: reviewed
confidence: medium
language: hu
tags: [distillation, on-policy, efficiency]
aliases: [on policy desztilláció]
relations:
  - type: supports
    target: checklist.post-training-readiness
---

## Lényeg

A tanuló saját aktuális politikájából mintáz trajektóriákat, majd egy erősebb tanár ezekre ad javított választ vagy visszajelzést.

## Miért működik

A tanár pontosan azokon az állapotokon segít, amelyeket a tanuló valóban elér, így csökken a demonstráció és a futási eloszlás közötti rés.

## Mikor alkalmazd

Használd, ha van megbízhatóbb tanár és a tanuló hibái a saját trajektóriáin jól megfigyelhetők.

## Mikor ne alkalmazd

Ne használd vakon, ha a tanár nem ellenőrizhető, ugyanazt a torzítást hordozza vagy érzékeny adatot kapna.

## Döntési szabály

Csak olyan tanári javítást taníts vissza, amely független értékelésben jobb a tanuló eredeti kimeneténél.

## Hibamódok

Tanárhiba, eloszlásbeszűkülés és túl agresszív utánzás gyengítheti a tanuló saját jó stratégiáit.

## Kapcsolatok

A minta a post-training készenléti kapu egyik mintahatékony lehetősége.

## Ellenőrzés

Tarts kontrollcsoportot tanári javítás nélkül, és mérd a nettó nyereséget költség, változatosság és holdout siker mellett.
