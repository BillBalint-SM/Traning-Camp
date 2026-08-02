---
id: concept.context-isolation-strategy
title: Kontextusizolációs stratégia
kind: concept
maturity: reviewed
confidence: high
language: hu
tags: [context, isolation, subagents, safety]
aliases: [elkülönített kontextus]
relations:
  - type: supports
    target: pattern.hierarchical-context-compression
---

## Lényeg

Ha egy részfeladatnak saját, nagy vagy kockázatos információtere van, külön kontextusban dolgoztasd fel, és csak ellenőrzött eredményt adj vissza a fő futásnak.

## Miért működik

Az izoláció a nem releváns részleteket és az idegen utasításokat nem engedi közvetlenül a fő döntési térbe, ezért gyakran jobb, mint az agresszív tömörítés.

## Mikor alkalmazd

Dokumentumelemzés, kódvizsgálat, több forrás összevetése vagy párhuzamos részfeladat esetén alkalmazd.

## Mikor ne alkalmazd

Ne szigetelj el olyan információt, amelynek közvetlenül és folyamatosan alakítania kell a közös döntést.

## Döntési szabály

Válaszd el a feladatot, ha a bemeneti halmaz nagy, a jogosultság eltérő, vagy a részfeladat kimenete szerződhető rövid eredményre és bizonyítékra.

## Hibamódok

A kontroll nélküli átadás elrejti a bizonytalanságot, a túl sok izolált feladat pedig elveszíti a szükséges közös kontextust.

## Kapcsolatok

A hierarchikus tömörítést támogatja; a több-agent átadási szerződés adja az izolált eredmény biztonságos formáját.

## Ellenőrzés

Hasonlítsd össze a közös és izolált futást relevancia, tokenhasználat, hibaterjedés és az átadott eredmény visszaellenőrizhetősége szerint.
