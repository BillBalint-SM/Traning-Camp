---
id: pattern.event-driven-agent-execution
title: Eseményvezérelt agent végrehajtás
kind: pattern
maturity: reviewed
confidence: high
language: hu
tags: [tools, events, async, agent, execution]
aliases: [event driven agent, eseményvezérelt agent]
relations:
  - type: applies_to
    target: procedure.tool-contract-design
---

## Lényeg

Az agent ne csak kérésre induljon: fogadjon eseményt, állítson elő egy korrelálható munkafeladatot, végezzen korlátozott feldolgozást, majd jelentse vagy ütemezze a következő lépést.

## Miért működik

Az eseményválasztás és a hosszú futás szétválasztása lehetővé teszi, hogy a rendszer gyorsan reagáljon, miközben a lassú munka nem blokkolja az új ingereket.

## Mikor alkalmazd

Használd változásértesítés, időzített ellenőrzés, üzenet, riasztás vagy több rendszer közötti állapotváltás feldolgozásakor.

## Mikor ne alkalmazd

Ne alakíts minden egyszeri felhasználói kérdést háttérfolyamattá, ha a közvetlen válasz egyszerűbb és átláthatóbb.

## Döntési szabály

Eseményvezérelt futás csak akkor induljon, ha az esemény azonosítható, deduplikálható, jogosult és egyértelműen meghatározza a munkafeladatot.

## Hibamódok

A duplikált esemény, az elveszett korrelációs azonosító és a visszajelzés nélküli háttérmunka ismételt vagy láthatatlan végrehajtást okoz.

## Kapcsolatok

Az aszinkron megszakítás kezelése és az eszközeredmény ellenőrzése teszi biztonságossá a futási mintát.

## Ellenőrzés

Szimulálj ismételt, késő, hibás és visszavont eseményt, és ellenőrizd, hogy minden esetben legfeljebb egy érvényes feladat jut végrehajtásig.
