---
id: pattern.isolated-context-collaboration
title: Izolált kontextusú együttműködés
kind: pattern
maturity: reviewed
confidence: medium
language: hu
tags: [isolation, collaboration, artifact]
aliases: [külön kontextusú agentek]
relations:
  - type: depends_on
    target: decision-guide.shared-or-isolated-context
---

## Lényeg

Az agentek saját munkakontextusban dolgoznak, és csak verziózott, sémás artifactokon keresztül kommunikálnak.

## Miért működik

Megőrzi a független gondolkodást, minimalizálja az adatszivárgást és auditálhatóvá teszi az átadást.

## Mikor alkalmazd

Használd párhuzamos kutatásnál, biztonsági izolációnál vagy nagy, eltérő kontextusoknál.

## Mikor ne alkalmazd

Ne használd nagyon szoros, alacsony késleltetésű közös döntéshez túl nehéz handoff-sémával.

## Döntési szabály

Az artifact legyen a közös igazság; az agent privát munkamenete ne legyen implicit dependency.

## Hibamódok

Elavult artifact, verziókonfliktus, rejtett előfeltétel és rossz séma blokkolhatja az integrációt.

## Kapcsolatok

A minta az izolált kontextus választásának végrehajtási formája.

## Ellenőrzés

Indíts új agentet csak az artifactból, és ellenőrizd, hogy képes-e helyesen folytatni.
