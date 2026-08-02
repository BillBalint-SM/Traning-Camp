---
id: procedure.shared-workspace-concurrency
title: Közös munkatér konkurenciakezelése
kind: procedure
maturity: reviewed
confidence: medium
language: hu
tags: [concurrency, workspace, ownership]
aliases: [agentek közös fájljainak ütközése]
relations:
  - type: depends_on
    target: checklist.shared-state-concurrency-control
---

## Lényeg

Oszd fel a tulajdont, használj izolált branchet vagy munkateret, verzióellenőrzött integrációt, atomikus publikálást és konfliktus esetén explicit feloldást.

## Miért működik

Az írók nem írják felül csendben egymást, az integráció pedig auditálható ponton történik.

## Mikor alkalmazd

Használd több agent közös repository-, fájl- vagy állapotmódosításánál.

## Mikor ne alkalmazd

Ne használj utolsó írás nyer szabályt olyan artifactnál, ahol mindkét módosítás értékes lehet.

## Döntési szabály

Egy fájlnak egy szeletben egy elsődleges írója legyen; átfedésnél koordinálj az írás előtt.

## Hibamódok

Elveszett frissítés, fél merge, generált zaj és régi alapra épített publikálás jelentkezhet.

## Kapcsolatok

Az eljárás a közös állapot konkurenciakontrollját repository-szintre konkretizálja.

## Ellenőrzés

Tesztelj két párhuzamos írót, elavult bázist, konfliktust, megszakított integrációt és visszaolvasást.
