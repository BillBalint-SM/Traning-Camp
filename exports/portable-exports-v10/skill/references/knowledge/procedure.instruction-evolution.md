---
id: procedure.instruction-evolution
title: Instrukció kontrollált fejlesztése
kind: procedure
maturity: reviewed
confidence: medium
language: hu
tags: [instructions, evolution, evaluation]
aliases: [tapasztalat instrukcióvá]
relations:
  - type: depends_on
    target: procedure.prompt-structure-design
---

## Lényeg

Az ismétlődő döntési hibát minimális, egyértelmű utasításjelöltté alakítsd, majd izoláltan értékeld, verziózd és fokozatosan add ki.

## Miért működik

Az instrukció gyorsan módosítható és visszagörgethető, miközben a pontos hibához köthető viselkedési korrekciót ad.

## Mikor alkalmazd

Használd, ha a kívánt viselkedés deklaratív szabályként vagy döntési prioritásként megfogalmazható.

## Mikor ne alkalmazd

Ne növeld végtelen szabályhalmazzá a promptot, és ne használj instrukciót determinisztikus validáció vagy jogosultsági kontroll helyett.

## Döntési szabály

Csak akkor add hozzá az instrukciót, ha célzott teszten javít, általános regressziós készleten nem ront, és nincs egyszerűbb kód- vagy eszközmegoldás.

## Hibamódok

Szabályütközés, sorrendfüggés, kontextusfelduzzadás és túlillesztett kivétel rontja a következetességet.

## Kapcsolatok

Az eljárás a strukturált promptarchitektúra szerkeszthető rétegére épül.

## Ellenőrzés

Abláld az új utasítást, mérd a célhibát és a teljes regressziós készletet, majd olvasd vissza a kiadott verziót.
