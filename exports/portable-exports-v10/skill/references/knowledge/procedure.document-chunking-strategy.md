---
id: procedure.document-chunking-strategy
title: Dokumentumdarabolási stratégia
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [retrieval, chunking, documents, context]
aliases: [dokumentum chunkolás]
relations:
  - type: supports
    target: procedure.retrieval-pipeline-design
---

## Lényeg

Dokumentumot jelentési egységek mentén darabolj, és őrizd meg a cím-, szakasz-, forrás- és szomszédsági kapcsolatot minden részletnél.

## Miért működik

A visszakeresés így elég kicsi egységet kap a pontossághoz, de nem veszíti el a válasz értelmezéséhez szükséges környezetet.

## Mikor alkalmazd

Új tudásbázis, hosszú dokumentum vagy gyenge találati pontosság esetén alkalmazd.

## Mikor ne alkalmazd

Ne használj kizárólag fix karakterszámot, ha a dokumentum világos cím- és bekezdésszerkezettel rendelkezik.

## Döntési szabály

Kezdd szemantikus határokkal, majd a túl nagy egységet bontsd, a túl rövidet pedig kapcsolt kontextussal egészítsd ki.

## Hibamódok

A túl nagy chunk zajt és drága kontextust, a túl kicsi chunk félreérthető idézetet és elveszett feltételt okoz.

## Kapcsolatok

A retrieval pipeline-t támogatja; a hibrid és kontextuális visszakeresés a darabok rangsorolását javítja.

## Ellenőrzés

Valós kérdéseken mérd a releváns részlet megtalálását, a szükséges környezet teljességét és a nem releváns szöveg arányát.
