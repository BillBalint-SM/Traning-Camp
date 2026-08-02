---
id: procedure.tool-contract-design
title: Eszközszerződés tervezése
kind: procedure
maturity: validated
confidence: high
language: hu
tags: [tools, contracts, validation]
aliases: [tool contract design, eszközszerződés]
relations:
  - type: supports
    target: checklist.tool-safety-boundary
---

## Lényeg

Minden eszközhívásnak legyen pontos bemeneti sémája, jogosultsági határa, megfigyelhető kimenete, idempotencia-szabálya és hibaformátuma.

## Miért működik

Az explicit szerződés kiszámíthatóvá teszi, mit tehet a modell, és mit kell a futtatórendszernek ellenőriznie. A modell ekkor nem találgat API-viselkedést.

## Mikor alkalmazd

Alkalmazd bármely adatkérés, fájlművelet, böngészés, üzenetküldés vagy külső rendszerhez kapcsolódó végrehajtás előtt.

## Mikor ne alkalmazd

Ne adj széles, többértelmű univerzális eszközt, ha két szűk művelet külön is ellenőrizhető.

## Döntési szabály

Egy eszköz akkor kész, ha a siker, a visszautasítás és a részleges hiba is géppel olvasható, és a mellékhatás előre látható.

## Hibamódok

A rejtett alapértelmezések, a szabad szöveges paraméterek és a homályos hibák önkényes újrapróbálkozást vagy nem kívánt mellékhatást okoznak.

## Kapcsolatok

Az eljárás a biztonsági határlistát támogatja, és alapja az eszközfelfedezésnek.

## Ellenőrzés

Futtass pozitív, érvénytelen bemeneti, jogosulatlan és ismételt hívási próbát; mindegyiknek egyértelmű, ellenőrizhető eredményt kell adnia.
