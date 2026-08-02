---
id: principle.agent-tool-bootstrapping
title: Agent eszköz-önépítés
kind: principle
maturity: reviewed
confidence: high
language: hu
tags: [agent, code, tools, bootstrapping]
aliases: [agent saját eszközt készít]
relations:
  - type: depends_on
    target: principle.code-as-meta-capability
---

## Lényeg

Az agent létrehozhat új segédeszközt saját feladatához, de az eszköz csak teszt, review, jogosultsági besorolás és explicit promóció után válhat újrahasználható képességgé.

## Miért működik

Így a tapasztalatból valódi automatizálás születhet anélkül, hogy egyetlen futás kódja azonnal megbízható platformképességgé válna.

## Mikor alkalmazd

Ismétlődő hiány, stabil szerződés és mérhető haszon esetén alkalmazd.

## Mikor ne alkalmazd

Ne promótálj egyszeri scriptet, nem determinisztikus workaroundot vagy titkot tartalmazó kódot.

## Döntési szabály

Különítsd el a feladatszintű prototípust, a review-zott eszközjelöltet és a verziózott, támogatott képességet.

## Hibamódok

A kontroll nélküli önbővítés jogosultságot halmoz, duplikálja a toolokat és tartósítja a hibás feltevést.

## Kapcsolatok

A kód metaképességére épül; a proaktív tool discovery és a continual improvement loop kezeli az életciklust.

## Ellenőrzés

Új környezetben futtasd a szerződéses teszteket, vizsgáld a dependency- és biztonsági hatást, majd mérd a valós feladatjavulást.
