---
id: pattern.full-duplex-conversation
title: Full-duplex beszélgetés
kind: pattern
maturity: reviewed
confidence: medium
language: hu
tags: [full-duplex, interruption, realtime]
aliases: [full duplex beszélgetés megszakítását]
relations:
  - type: depends_on
    target: procedure.async-interruption-handling
---

## Lényeg

A rendszer egyszerre hallhat és beszélhet, ezért minden kimenet megszakítható, az új bemenet pedig prioritással frissíti a közös beszélgetési állapotot.

## Miért működik

Az átfedő csatorna természetes közbevágást, gyors korrekciót és folyamatos backchannel-jelzést tesz lehetővé.

## Mikor alkalmazd

Használd szabad beszélgetésnél, ahol a felhasználó bármikor pontosíthat vagy leállíthat.

## Mikor ne alkalmazd

Ne engedj párhuzamos beszédet olyan utasításnál, ahol a teljes, visszaigazolt tartalom kritikus.

## Döntési szabály

Felhasználói beszédkezdetkor állítsd le vagy halkítsd a kimenetet, őrizd meg az elhangzott határt, majd abból folytasd az állapotot.

## Hibamódok

Önvisszhang, kölcsönös közbevágás, elveszett kontextus és duplikált válasz instabil párbeszédet okoz.

## Kapcsolatok

A minta az általános aszinkron megszakításkezelésre épül.

## Ellenőrzés

Tesztelj korai, középső és késői közbevágást, zajt, visszhangot és helyes folytatási pontot.
