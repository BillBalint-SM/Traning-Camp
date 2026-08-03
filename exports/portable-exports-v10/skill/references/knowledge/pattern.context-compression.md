---
id: pattern.context-compression
title: Kontextustömörítés döntési állapottal
kind: pattern
maturity: validated
confidence: high
language: hu
tags: [context-engineering, compression, state]
aliases: [context compression, kontextustömörítés]
relations:
  - type: depends_on
    target: principle.context-is-finite
  - type: prevents
    target: failure-mode.unvalidated-autonomy
---

## Lényeg

A hosszú előzményt ne rövid szövegre, hanem döntési állapotra tömörítsd: cél, már igazolt tények, nyitott kérdések, tilalmak, következő lépés és bizonyítékok.

## Miért működik

Az állapotcentrikus kivonat a folyamat folytonosságát őrzi, nem a beszélgetés sorrendjét. Így a következő agent kör ugyanazzal a döntési alapállapottal indulhat.

## Mikor alkalmazd

Alkalmazd, amikor a beszélgetés vagy a megfigyelések már nem férnek el, de a feladat több lépésben folytatódik.

## Mikor ne alkalmazd

Ne használd bizonyíték helyett olyan vitás állításnál, amelyet a következő lépésnek eredeti részletből kell ellenőriznie.

## Döntési szabály

A kivonat minden mondata jelölje, hogy tény, feltételezés, tiltás vagy nyitott kérdés; bizonytalan állítást ne emelj végleges szabállyá.

## Hibamódok

A rossz tömörítés eltünteti a kivételeket, összekeveri a javaslatot a döntéssel, vagy régi eszközeredményt aktuálisnak mutat.

## Kapcsolatok

A minta a véges keret miatt szükséges, és az ellenőrizetlen önállóság kockázatát csökkenti.

## Ellenőrzés

Adj a kivonatból újraindított futásnak egy ismert következő feladatot; akkor jó, ha ugyanazokat a korlátokat és nyitott kérdéseket azonosítja.
