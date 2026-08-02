---
id: procedure.async-interruption-handling
title: Aszinkron megszakítás kezelése
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [tools, async, interruption, cancellation, agent]
aliases: [async interruption, aszinkron megszakítás]
relations:
  - type: depends_on
    target: pattern.event-driven-agent-execution
---

## Lényeg

Hosszú futásnál külön kezeld a megszakítás kérését, a biztonságos leállási pontot, a részleges állapot mentését, az idempotens visszavonást és a felhasználói visszajelzést.

## Miért működik

A megszakítás nem hibaüzenet, hanem állapotátmenet: csak akkor megbízható, ha a folyamat tudja, mi már történt, mi ismételhető és mi nem.

## Mikor alkalmazd

Használd háttérmunkánál, több eszközhívásos folyamatnál, felhasználó által leállítható feladatnál és lejáró jogosultság esetén.

## Mikor ne alkalmazd

Ne szakíts félbe tranzakciót kontroll nélkül olyan ponton, ahol a részleges módosítás nagyobb kárt okoz, mint a művelet befejezése.

## Döntési szabály

Minden külső hatás előtt jelölj ki leállási pontot; megszakításkor előbb állítsd meg az új mellékhatást, majd rögzítsd a már bekövetkezett állapotot.

## Hibamódok

A vak folyamatleállítás duplikált újrapróbálást, félbehagyott erőforrást vagy hamis sikerjelzést okozhat.

## Kapcsolatok

Az eseményvezérelt végrehajtás aktiválja, az eszközeredmény ellenőrzése pedig lezárja a megszakítás utáni állapotot.

## Ellenőrzés

Indíts megszakítást minden kritikus lépés előtt és után, majd igazold, hogy a végső állapot, a napló és az újraindítási viselkedés egyaránt konzisztens.
