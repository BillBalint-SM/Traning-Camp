---
id: decision-guide.shared-or-isolated-context
title: Megosztott vagy izolált agentkontextus
kind: decision-guide
maturity: reviewed
confidence: medium
language: hu
tags: [context, isolation, collaboration]
aliases: [megosztott vagy izolált kontextust kapjanak az agentek]
relations:
  - type: supports
    target: pattern.multi-agent-context-boundaries
---

## Lényeg

Megosztott kontextust válassz gyors szerepváltáshoz, izoláltat független gondolkodáshoz, adatminimalizáláshoz és ellenőrizhető átadáshoz.

## Miért működik

A döntés egyensúlyozza a koordinációs költséget a torzítás-, szivárgás- és kontextusterhelési kockázattal.

## Mikor alkalmazd

Használd minden több-agent feladat kontextusarchitektúrája előtt.

## Mikor ne alkalmazd

Ne ossz meg mindent alapértelmezetten, és ne izolálj úgy, hogy a szükséges feladatállapot elveszjen.

## Döntési szabály

Csak a közös döntéshez szükséges kanonikus állapot legyen megosztott; a munkakontextus maradjon szerepkörönként izolált.

## Hibamódok

Közös torzítás, promptinjekció-terjedés, duplikált keresés és hiányos handoff jelentkezhet.

## Kapcsolatok

Az útmutató a multi-agent kontextushatárok gyakorlati választását adja.

## Ellenőrzés

Tesztelj érzékeny mezőt, elavult közös állapotot, hiányos átadást és független megoldási sokféleséget.
