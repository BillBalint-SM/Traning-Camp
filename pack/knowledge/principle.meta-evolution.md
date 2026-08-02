---
id: principle.meta-evolution
title: A fejlesztési módszer fejlesztése
kind: principle
maturity: reviewed
confidence: medium
language: hu
tags: [meta-learning, process, evolution]
aliases: [fejlődés módszerének fejlesztése]
relations:
  - type: supports
    target: pattern.continual-evolution-closed-loop
---

## Lényeg

Ne csak az artifactot javítsd; mérd és fejleszd azt a folyamatot is, amely a hibából jelöltet, tesztet, kiadást és visszagörgetést készít.

## Miért működik

A stabil fejlesztési gépezet több jövőbeli problémát old meg következetesen, miközben csökkenti az egyedi kézi beavatkozás és a véletlen promóció arányát.

## Mikor alkalmazd

Használd, amikor elegendő fejlesztési ciklus gyűlt össze a folyamat átfutásának és hibáinak méréséhez.

## Mikor ne alkalmazd

Ne automatizáld tovább a folyamatot, ha a jelenlegi validáció nem különbözteti meg megbízhatóan a valódi javulást a proxyjavulástól.

## Döntési szabály

Csak olyan meta-változtatást adj ki, amely több korábbi eset visszajátszásán jobb jelöltminőséget vagy alacsonyabb hibaarányt ad.

## Hibamódok

A gyorsabb, de gyengébb review, az automatikus önjóváhagyás és a metrikajáték skálázott regressziót okoz.

## Kapcsolatok

Az elv a folyamatos fejlődési zárt hurkot teszi hosszú távon javíthatóvá.

## Ellenőrzés

Mérd a jelöltek elfogadási minőségét, rollback-arányt, átfutási időt és fel nem ismert regressziókat folyamatverziónként.
