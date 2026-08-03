---
id: decision-guide.status-update-placement
title: Státuszfrissítés elhelyezése
kind: decision-guide
maturity: reviewed
confidence: high
language: hu
tags: [status, context, cache, updates]
aliases: [státuszfrissítés helye]
relations:
  - type: depends_on
    target: procedure.status-signal-design
---

## Lényeg

Gyakran változó státuszt külön, kicsi és cserélhető kontextusblokkban frissíts; ritkán változó állapotot a stabil feladatszerződéshez közel tarts.

## Miért működik

Az elhelyezés eldönti, hogy egy frissítés mennyi kontextust érvénytelenít, és mennyire könnyű az aktuális állapotot ellenőrizni.

## Mikor alkalmazd

Hosszú futás, tokenköltség, cache-hatékonyság vagy megszakítás utáni folytatás problémájánál alkalmazd.

## Mikor ne alkalmazd

Ne optimalizáld túl a helyet, ha a státusz ténylegesen nem befolyásolja a következő döntést.

## Döntési szabály

Az állandó cél és korlát maradjon stabil; a lépés-szintű előrehaladás és átmeneti hiba legyen közvetlenül cserélhető, egyértelmű eredetű blokkban.

## Hibamódok

Ha a változó állapot a stabil prefixbe kerül, romlik az újrahasználás; ha túl későre kerül, a modell figyelmen kívül hagyhatja.

## Kapcsolatok

A státuszjel tervezésére épül, a cache-stabil kontextuselrendezés a költségoldalt magyarázza.

## Ellenőrzés

Mérd a státuszfrissítés utáni cache-viselkedést és ellenőrizd, hogy a modell minden futásnál ugyanazt az aktuális állapotot idézi-e fel.
