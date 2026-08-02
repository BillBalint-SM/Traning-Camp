---
id: procedure.evolution-validation-release-rollback
title: Fejlődési jelölt validálása, kiadása és visszagörgetése
kind: procedure
maturity: reviewed
confidence: medium
language: hu
tags: [validation, release, rollback]
aliases: [validáljam adjam ki és görgessem vissza az agent fejlődését]
relations:
  - type: depends_on
    target: procedure.continual-improvement-release-loop
---

## Lényeg

A fejlődési jelöltet elkülönített regresszión, árnyékfutáson vagy kis mintás rollouton validáld, verziózottan add ki, és előre tesztelt visszagörgetési feltétellel monitorozd.

## Miért működik

A fokozatos kitettség korlátozza a hiba hatását, a verziózott artifact pedig gyors és egyértelmű visszaállítást tesz lehetővé.

## Mikor alkalmazd

Használd tudás-, instrukció-, program- és paraméterváltoztatás minden éles promóciójánál.

## Mikor ne alkalmazd

Ne engedj közvetlen automatikus kiadást, ha a hatás nem izolálható, a metrika késik vagy nincs visszaállítható előző állapot.

## Döntési szabály

Csak akkor növeld a rolloutot, ha a célmetrika javul, a guardrail metrikák nem romlanak, és a rollback próba sikeres.

## Hibamódok

Túl rövid megfigyelési ablak, kevert verzió, hiányzó kontroll és nem gyakorolt rollback tartós regressziót okozhat.

## Kapcsolatok

Az eljárás a folyamatos fejlesztés általános kiadási hurkára épül.

## Ellenőrzés

Olvasd vissza az aktív verziót, ellenőrizd a metrikák szeparációját, majd próbáld ki a rollbacket kontrollált környezetben.
