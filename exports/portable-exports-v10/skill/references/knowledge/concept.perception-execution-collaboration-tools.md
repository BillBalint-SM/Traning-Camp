---
id: concept.perception-execution-collaboration-tools
title: Érzékelő, végrehajtó és együttműködési eszközök
kind: concept
maturity: reviewed
confidence: high
language: hu
tags: [tools, perception, execution, collaboration]
aliases: [eszköz szerepkörök]
relations:
  - type: supports
    target: concept.tool-capability-taxonomy
---

## Lényeg

Különítsd el a világ állapotát olvasó, a világot módosító és más szereplőkkel információt vagy kontrollt cserélő eszközöket.

## Miért működik

A három szerep eltérő jogosultságot, hibakezelést, visszajelzést és auditkövetelményt igényel.

## Mikor alkalmazd

Eszközkatalógus, jogosultsági modell vagy orchestration-folyamat tervezésekor alkalmazd.

## Mikor ne alkalmazd

Ne kezeld az együttműködési üzenetet ártalmatlan olvasásként, ha az másik agent vagy ember viselkedését befolyásolja.

## Döntési szabály

Minden eszköznél nevezd meg az elsődleges szerepet, a hatás hatókörét és azt, hogy az eredmény megfigyelés, állapotváltozás vagy átadási szerződés.

## Hibamódok

A szerepek összemosása miatt egy lekérdezésnek hitt művelet írhat adatot, vagy egy üzenet kontrollálatlan delegációvá válhat.

## Kapcsolatok

Az eszközképesség-taxonómiát támogatja; a biztonsági határ a végrehajtó és együttműködési oldal kockázatát kezeli.

## Ellenőrzés

Leltározd az eszközöket szerep szerint, és igazold, hogy mindegyikhez illeszkedik a jogosultság, a napló és a visszaellenőrzés.
