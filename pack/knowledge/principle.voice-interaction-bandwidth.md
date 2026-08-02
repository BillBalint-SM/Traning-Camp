---
id: principle.voice-interaction-bandwidth
title: A hang valós idejű kapcsolati csatorna
kind: principle
maturity: reviewed
confidence: medium
language: hu
tags: [voice, realtime, interaction]
aliases: [hangalapú ember gép kapcsolat]
relations:
  - type: supports
    target: decision-guide.voice-architecture-selection
---

## Lényeg

A hang nem puszta szövegátvitel: időzítés, hangsúly, megszakítás, bizonytalanság és érzelmi jel együtt alakítja az interakciót.

## Miért működik

A rendszer így nem veszti el azokat a jeleket, amelyek a szándékot és a beszélgetés ritmusát hordozzák.

## Mikor alkalmazd

Használd valós idejű asszisztens, ügyfélszolgálat vagy kéz nélküli vezérlés tervezésekor.

## Mikor ne alkalmazd

Ne válaszd alapértelmezettnek érzékeny, pontosan visszaolvasható vagy csendet igénylő feladathoz.

## Döntési szabály

Hangot akkor adj elsődleges csatornaként, ha a késleltetés és a turn-taking fontosabb a szerkeszthető pontosságnál.

## Hibamódok

Átiratközpontú tervezés elveszíti a ritmust; túl agresszív automatizmus félbeszakítja vagy félreérti a felhasználót.

## Kapcsolatok

Az elv a hangarchitektúra-választás célfüggvényét pontosítja.

## Ellenőrzés

Mérd a feladat sikerét, első hang idejét, megszakításkezelést és javítási fordulók számát.
