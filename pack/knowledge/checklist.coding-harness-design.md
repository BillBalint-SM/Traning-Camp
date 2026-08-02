---
id: checklist.coding-harness-design
title: Coding harness ellenőrzőlista
kind: checklist
maturity: reviewed
confidence: high
language: hu
tags: [coding-agent, harness, tools, verification]
aliases: [coding agent harness]
relations:
  - type: supports
    target: checklist.harness-function-coverage
---

## Lényeg

A coding harness biztosítson repository-felderítést, keresést, célzott olvasást, patch-alapú írást, parancsfuttatást, tesztkimenetet, Git-állapotot és megszakíthatóságot.

## Miért működik

A modell akkor tud megbízhatóan kódot módosítani, ha a környezet pontos megfigyelést és korlátozott, visszaolvasható műveleteket ad.

## Mikor alkalmazd

Coding-agent platform, CLI vagy automatikus fejlesztési workflow tervezésekor alkalmazd.

## Mikor ne alkalmazd

Ne adj több végrehajtási képességet, mint amennyit a támogatott repository-feladatok igényelnek.

## Döntési szabály

Minden képességhez legyen explicit bemenet, hatókör, hiba, megszakítás, eredmény és auditálható nyom.

## Hibamódok

A csak shellre épített harness túl széles, a keresés vagy diff nélküli harness pedig vak módosításokra kényszerít.

## Kapcsolatok

A harness funkciólefedettségét támogatja; a coding security korlátozza, a workflow használja.

## Ellenőrzés

Valós repository-feladaton igazold, hogy minden lépés megfigyelhető, megállítható, hatókörben marad és visszaellenőrizhető.
