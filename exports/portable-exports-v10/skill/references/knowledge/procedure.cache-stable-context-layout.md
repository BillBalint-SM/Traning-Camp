---
id: procedure.cache-stable-context-layout
title: Cache-stabil kontextuselrendezés
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [context, cache, prompt, latency]
aliases: [stabil cache kontextus]
relations:
  - type: depends_on
    target: concept.context-cache-architecture
---

## Lényeg

A ritkán változó utasítást, eszközleírást és hosszú távú szabályt a kontextus stabil elejére, a fordulónként változó adatot pedig elkülönített késői szakaszba helyezd.

## Miért működik

A stabil prefix újrahasználható, így kevesebb ismételt feldolgozást, alacsonyabb késleltetést és kiszámíthatóbb költséget eredményez.

## Mikor alkalmazd

Hosszú rendszerutasítás, nagy eszközséma vagy sokfordulós session esetén alkalmazd.

## Mikor ne alkalmazd

Ne fagyassz olyan adatot a stabil részbe, amely jogosultság, feladat vagy felhasználói állapot szerint gyakran változik.

## Döntési szabály

Minden kontextusdarabról döntsd el, hogy session-szintű, feladat-szintű vagy lépés-szintű; a stabilitási osztály határozza meg a helyét.

## Hibamódok

Egy korán beszúrt dinamikus dátum, azonosító vagy státusz megbonthatja az újrahasználást, a rossz helyre tett szabály pedig elavulhat.

## Kapcsolatok

A cache architektúrára épül; a szerkeszthető kontextusjegyzetek kontrollált kivételt adnak a stabil törzs mellett.

## Ellenőrzés

Mérd külön a stabil prefix arányát, a cache-találatot, a kontextus építési idejét és a válaszminőséget változó terhelés mellett.
