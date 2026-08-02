---
id: decision-guide.multi-agent-topology-selection
title: Több-agent topológia választása
kind: decision-guide
maturity: reviewed
confidence: high
language: hu
tags: [multi-agent, collaboration, topology, delegation]
aliases: [multi agent topology selection, több agent topológia]
relations:
  - type: depends_on
    target: pattern.multi-agent-context-boundaries
---

## Lényeg

Központi koordinátort használj, ha prioritás és felelősség összefogása kell; peer együttműködést, ha független ellenőrzés értékes; átadási láncot, ha a munka természetesen egymásra épül és a határok világosak.

## Miért működik

A topológia határozza meg, ki látja a teljes célt, hogyan jut el az információ a következő szereplőhöz, és hol áll meg a hiba terjedése.

## Mikor alkalmazd

Használd akkor, ha egyetlen agent kontextusa, eszközjogosultsága vagy párhuzamos kapacitása nem elég a feladat biztonságos elvégzéséhez.

## Mikor ne alkalmazd

Ne oszd több agentre az olyan feladatot, amelyet egy agent kevesebb átadással, kevesebb koordinációval és azonos minőségben meg tud oldani.

## Döntési szabály

Előbb a munka szeparálhatóságát, a közös állapot szükségességét, a hiba költségét és az összehangolás terhét mérd fel, utána válassz topológiát.

## Hibamódok

A szerepkör nélküli sokagent-rendszer ismételt munkát, ellentmondó javaslatot és felelősség nélküli átadást termel.

## Kapcsolatok

Az átadási szerződés, a közös állapot konkurenciakezelése és a hibaamplifikáció mind a topológia következményeit kezeli.

## Ellenőrzés

Mérd egy- és több-agent megoldásban a feladat sikerét, az átadások számát, a hibák felismerési idejét és az összköltséget ugyanazon munkán.
