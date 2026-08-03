---
id: concept.variable-length-agent-policy
title: Változó hosszúságú agent politika
kind: concept
maturity: reviewed
confidence: medium
language: hu
tags: [policy, actions, language-model]
aliases: [változó hosszúságú cselekvés]
relations:
  - type: depends_on
    target: concept.agent-environment-learning-loop
---

## Lényeg

Nyelvi agentnél egy cselekvés gyakran teljes token-szekvencia, eszközhívás vagy strukturált üzenet, nem egyetlen rögzített diszkrét választás.

## Miért működik

A helyes cselekvési egység kijelölése megakadályozza, hogy a tanítás a formátum közepén adjon félrevezető visszajelzést.

## Mikor alkalmazd

Használd, amikor a modell szabad szöveget, kódot vagy változó hosszúságú argumentumokat generál.

## Mikor ne alkalmazd

Ne növeld feleslegesen az akcióteret, ha a feladat biztonságosan megoldható zárt, rögzített műveletkészlettel.

## Döntési szabály

A környezet számára atomi és validálható legkisebb teljes kimenetet tekintsd egy cselekvésnek.

## Hibamódok

Tokenenkénti és környezeti lépések összekeverése hibás jutalommegosztást és érvénytelen trajektóriákat eredményez.

## Kapcsolatok

A fogalom az agent–környezet hurok cselekvési komponensét pontosítja.

## Ellenőrzés

Ellenőrizd, hogy minden naplózott akció önmagában parse-olható, végrehajtható vagy egyértelműen elutasítható.
