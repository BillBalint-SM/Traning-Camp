---
id: concept.context-cache-architecture
title: Kontextus-gyorsítótár architektúra
kind: concept
maturity: reviewed
confidence: high
language: hu
tags: [context-engineering, cache, kv-cache, prompt-cache]
aliases: [kv cache architektúra, prompt cache tervezés]
relations:
  - type: depends_on
    target: principle.context-is-finite
---

## Lényeg

A stabil, gyakran ismételt kontextusrészeket úgy szervezd, hogy azok sorrendje, formája és elhelyezése minél ritkábban változzon, míg a dinamikus állapot elkülönített rétegben maradjon.

## Miért működik

A modelloldali gyorsítótár csak a közös előtagot tudja újrahasználni, ezért a változó információ korai beszúrása növeli a költséget és a késleltetést.

## Mikor alkalmazd

Használd rendszerutasításoknál, állandó szabályoknál, közös eszközleírásoknál és ismétlődő feladatsablonoknál.

## Mikor ne alkalmazd

Ne gyorsítótárazz személyes, rövid életű vagy jogosultságfüggő adatot úgy, hogy az más feladatba vagy felhasználóhoz átkerülhessen.

## Döntési szabály

Először a hosszú életű szabályokat, utána a ritkán változó feladatkeretet, végül a konkrét felhasználói állapotot helyezd el.

## Hibamódok

Az instabil előtag, a kevert felhasználói állapot és a folyamatosan átírt rendszerprompt cache-vesztést és kontextusszivárgást okozhat.

## Kapcsolatok

A rendszerprompt-architektúra és a dinamikus skill-betöltés együtt dönti el, mely elemek maradnak stabilak.

## Ellenőrzés

Mérd külön a stabil előtag arányát, a cache-találatot, a költséget és azt, hogy az ismételt futások válasza nem kever-e idegen állapotot.
