---
id: concept.structured-knowledge-index
title: Strukturált tudásindex
kind: concept
maturity: reviewed
confidence: high
language: hu
tags: [knowledge, index, metadata, graph]
aliases: [strukturált tudásindex, tudásgráf indexelés]
relations:
  - type: supports
    target: procedure.retrieval-pipeline-design
---

## Lényeg

A tudást ne csak szövegdarabokként tárold: adj hozzá típust, időbeliséget, tulajdonost, jogosultságot, kapcsolódó fogalmat és ellenőrzési állapotot.

## Miért működik

A strukturált jel segít szűrni, összekapcsolni és időben értelmezni az információt, ezért a kereső nem pusztán szöveghasonlóságra támaszkodik.

## Mikor alkalmazd

Használd heterogén, üzletileg fontos vagy gyakran frissülő tudásnál, ahol a dokumentum neve önmagában nem elég a relevancia eldöntéséhez.

## Mikor ne alkalmazd

Ne modellezz túl részletes gráfot, ha az adat nem tartható naprakészen vagy a kapcsolatok nem befolyásolják a döntést.

## Döntési szabály

Csak olyan mezőt vagy kapcsolatot vezess be, amely szűrést, jogosultsági döntést, időbeli érvényességet vagy bizonyíték-visszakeresést javít.

## Hibamódok

Az elavult metaadat, a bizonytalan kapcsolat és a tulajdonos nélküli rekord hamis pontosságot adhat a keresésnek.

## Kapcsolatok

A retrieval-folyamat felhasználja, a tudásfrissítés és a memória-életciklus pedig fenntartja a minőségét.

## Ellenőrzés

Válassz reprezentatív kérdéseket, és mérd meg, hogy a strukturált szűrés növeli-e a releváns találatot anélkül, hogy elfedné a szükséges bizonyítékot.
