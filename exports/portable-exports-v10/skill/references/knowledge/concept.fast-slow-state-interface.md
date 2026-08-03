---
id: concept.fast-slow-state-interface
title: Gyors–lassú ág állapotinterfésze
kind: concept
maturity: reviewed
confidence: medium
language: hu
tags: [state, interface, realtime]
aliases: [gyors lassú állapotátadás]
relations:
  - type: supports
    target: pattern.fast-slow-interaction-loop
---

## Lényeg

Az ágak szöveg mellett szándékot, bizonytalanságot, megszakítási pontot, felhasznált megfigyelést és engedélyezett következő műveletet adjanak át.

## Miért működik

A strukturált állapot csökkenti a félreértést és megőrzi a beszélgetés időbeli kontextusát.

## Mikor alkalmazd

Használd több komponensből álló valós idejű interakcióban.

## Mikor ne alkalmazd

Ne ossz meg belső állapotot korlátlanul, ha érzékeny adatot vagy nem stabil következtetést tartalmaz.

## Döntési szabály

Csak a következő döntéshez szükséges, típusos és verziózott állapot lépheti át az ághatárt.

## Hibamódok

Elavult verzió, hiányzó megszakítási jel és szabad szöveges implicit állapot versenyhelyzetet okoz.

## Kapcsolatok

A fogalom a gyors–lassú interakciós hurok szerződését részletezi.

## Ellenőrzés

Végezz séma-, sorrend-, duplikáció- és elavult állapot teszteket.
