---
id: procedure.business-rule-compilation
title: Üzleti szabályok végrehajtható fordítása
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [business-rules, prompt, validation, policy]
aliases: [üzleti szabály fordítás]
relations:
  - type: supports
    target: procedure.prompt-structure-design
---

## Lényeg

Az üzleti mondatokat alakítsd feltétel, ellenőrizhető adat, engedélyezett hatás, kivétel és hibajel formájú szabállyá.

## Miért működik

Az értelmezhető szabályból teszt, eszközvalidáció és auditkérdés is készíthető, ezért nem kizárólag a modell nyelvi értelmezésére épül.

## Mikor alkalmazd

Szabályozott folyamat, szerepkör-alapú döntés vagy visszautasítási logika beépítésekor alkalmazd.

## Mikor ne alkalmazd

Ne fordíts le szó szerint homályos üzleti szándékot; előbb tisztázd a fogalmakat, a felelőst és a kivételkezelést.

## Döntési szabály

Minden szabályhoz legyen eldönthető igaz/hamis feltétel és definiált viselkedés hiányzó vagy ellentmondó adat esetére.

## Hibamódok

A "szükség esetén" vagy "megfelelően" típusú fogalmazás rejtett diszkréciót hagy a modellnek, ezért eltérő futásokban eltérő eredményt ad.

## Kapcsolatok

A promptstruktúrát támogatja, a védőkorlátok az érzékeny szabályok végrehajtási ellenőrzését adják.

## Ellenőrzés

Minden szabályhoz készíts igaz, hamis, hiányzó és kivételes bemenetet, majd igazold a kívánt kimenetet és a naplózott indokot.
