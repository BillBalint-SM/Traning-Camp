---
id: procedure.user-memory-lifecycle
title: Felhasználói memória életciklusa
kind: procedure
maturity: validated
confidence: high
language: hu
tags: [memory, consent, lifecycle]
aliases: [user memory lifecycle, felhasználói memória kezelése]
relations:
  - type: depends_on
    target: decision-guide.memory-vs-retrieval
---

## Lényeg

A memória kezelése külön folyamat: jelölt adat, ellenőrzés, jóváhagyás, használat, felülvizsgálat és törlés.

## Miért működik

Az életciklus elválasztja a pillanatnyi beszélgetési részletet a valóban tartós információtól. A visszavonhatóság és az átláthatóság így nem utólagos javítás.

## Mikor alkalmazd

Használd, amikor az agent több alkalommal dolgozik ugyanazzal a személlyel vagy csapattal.

## Mikor ne alkalmazd

Ne hozz létre tartós memóriát hallgatólagos feltételezésből, és ne tárolj olyan adatot, amelynek nincs egyértelmű jövőbeli haszna.

## Döntési szabály

Új bejegyzést csak akkor rögzíts, ha a tartósság indoka, a várható felhasználás és a felülvizsgálat módja is megnevezhető.

## Hibamódok

A beleegyezés nélküli vagy lejárat nélküli memória bizalmi és pontossági kockázat. A túl általános bejegyzés félreviszi a későbbi routingot.

## Kapcsolatok

Az eljárás a memória és visszakeresés közötti döntésre épül.

## Ellenőrzés

Időszakosan listázd a bejegyzéseket, jelöld az elavultakat, és ellenőrizd, hogy mindegyikhez tartozik-e használati cél vagy törlési szabály.
