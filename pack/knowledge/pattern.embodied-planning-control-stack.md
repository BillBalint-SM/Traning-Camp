---
id: pattern.embodied-planning-control-stack
title: Testet öltött tervezési és vezérlési stack
kind: pattern
maturity: reviewed
confidence: medium
language: hu
tags: [robotics, planning, control]
aliases: [robot tervezés vezérlés két réteg]
relations:
  - type: supports
    target: principle.planning-control-separation
---

## Lényeg

A lassú szemantikai tervező célokat és alfeladatokat ad, a gyors vezérlő pedig zárt szenzorhurokban hajt végre, explicit átadási és vészleállítási szerződéssel.

## Miért működik

A két időskála egyszerre kezeli a hosszú horizontú szándékot és a fizikai rendszer gyors korrekcióját.

## Mikor alkalmazd

Használd robotikai vagy más valós idejű fizikai agentnél.

## Mikor ne alkalmazd

Ne engedd a nyelvi tervezőt közvetlen, korlátlan alacsony szintű aktuátorvezérléshez.

## Döntési szabály

A tervező csak ellenőrizhető célállapotot adhat; a vezérlő felel az invariánsokért és a biztonságos leállásért.

## Hibamódok

Időskála-keverés, elavult terv, rossz állapotbecslés és átadási verseny veszélyes mozgást okozhat.

## Kapcsolatok

A minta a tervezés és vezérlés általános szétválasztását alkalmazza fizikai rendszerre.

## Ellenőrzés

Tesztelj szenzorhibát, késést, célváltást, megszakítást, határállapotot és vészleállítást szimulációban.
