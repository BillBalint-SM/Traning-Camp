---
id: pattern.manager-worker-coordination
title: Manager–worker koordináció
kind: pattern
maturity: reviewed
confidence: medium
language: hu
tags: [manager, worker, coordination]
aliases: [manager agent több worker agentet]
relations:
  - type: depends_on
    target: decision-guide.collaboration-topology
---

## Lényeg

A manager bontja a célt független szerződésekre, kiosztja a workereket, követi a függőségeket, majd validált artifactokból integrál.

## Miért működik

Központi prioritást és egységes integrációs felelőst ad sok párhuzamos részfeladathoz.

## Mikor alkalmazd

Használd jól bontható munkánál, ahol a részfeladatok kimeneti szerződése előre megadható.

## Mikor ne alkalmazd

Ne válassz managert, ha ő válik minden döntés, kontextus és review szűk keresztmetszetévé.

## Döntési szabály

A manager ne végezze el újra a worker munkáját; szerződést, prioritást és integrációt birtokoljon.

## Hibamódok

Túl finom felbontás, rejtett függőség, elveszett worker és ellenőrizetlen összefésülés ronthatja az eredményt.

## Kapcsolatok

A minta a centralizált kollaborációs topológiára épül.

## Ellenőrzés

Tesztelj worker-kiesést, késést, inkompatibilis artifactot és manager nélküli újraindíthatóságot.
