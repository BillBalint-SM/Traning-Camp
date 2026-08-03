---
id: pattern.editable-context-notes
title: Szerkeszthető kontextusjegyzetek
kind: pattern
maturity: reviewed
confidence: high
language: hu
tags: [context, notes, cache, state]
aliases: [szerkeszthető agent jegyzet]
relations:
  - type: supports
    target: procedure.cache-stable-context-layout
---

## Lényeg

Tarts rövid, strukturált munkajegyzetet a fontos döntésekről, nyitott kérdésekről és ellenőrzött tényekről, amelyet szabályozottan frissíthetsz a teljes előzmény újraépítése nélkül.

## Miért működik

A tömör állapot kifejezi, mi maradt releváns, miközben a stabil kontextust és a részletes előzményt nem kell minden fordulóban újramodellezni.

## Mikor alkalmazd

Hosszú, többeszközös feladatoknál, ahol a döntési állapot fontosabb, mint a teljes beszélgetési szó szerinti előzmény.

## Mikor ne alkalmazd

Ne használd ellenőrizetlen összefoglalóként jogi, pénzügyi vagy nagy pontosságú tények kizárólagos forrásaként.

## Döntési szabály

Csak forrással, időbélyeggel és státusszal rendelkező állítást emelj be; elavult vagy vitatott jegyzetet külön jelölj, ne írd felül csendben.

## Hibamódok

A kontroll nélküli jegyzet egyetlen téves következtetést sok későbbi lépésbe szaporít, és elfedi az eredeti bizonyítékot.

## Kapcsolatok

A cache-stabil elrendezést támogatja, a státuszjelzés pedig a feladat látható haladását egészíti ki.

## Ellenőrzés

Válassz vissza néhány jegyzetállítást az eredeti megfigyelésekhez, és ellenőrizd, hogy frissítéskor a visszavont állítások eltűnnek vagy egyértelműen érvénytelenek maradnak.
