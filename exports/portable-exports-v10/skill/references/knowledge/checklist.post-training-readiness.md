---
id: checklist.post-training-readiness
title: Utótanítási készenléti kapu
kind: checklist
maturity: reviewed
confidence: medium
language: hu
tags: [post-training, readiness, governance]
aliases: [utótanítási készenlét]
relations:
  - type: depends_on
    target: procedure.evaluation-environment-design
---

## Lényeg

Legyen explicit célképesség, baseline, holdout, validált adat és környezet, költségkeret, biztonsági teszt, megállási feltétel, verziózás és rollback.

## Miért működik

A kapu a drága és állapotmódosító tanítást csak akkor engedi elindulni, amikor a javulás és a károkozás egyaránt mérhető.

## Mikor alkalmazd

Futtasd minden tréningrun jóváhagyása és minden jelentős hiperparaméter- vagy adatváltozás előtt.

## Mikor ne alkalmazd

Ne helyettesítsd vele a futás közbeni monitorozást és a tanítás utáni független release-kaput.

## Döntési szabály

Egyetlen hiányzó kötelező elem esetén a tanítás nem indul; a hiányt a megfelelő adat-, környezet- vagy governance-folyamatban kell megszüntetni.

## Hibamódok

Rögzítetlen baseline, szivárgó holdout, ellenőrizetlen jutalom és rollback nélküli kiadás mérhetetlen vagy tartós regressziót okoz.

## Kapcsolatok

A kapu az értékelési környezet stabilitásától függ.

## Ellenőrzés

Őrizd meg a kapu minden mezőjének bizonyítékát és a jóváhagyott konfiguráció tartalmi hash-ét.
