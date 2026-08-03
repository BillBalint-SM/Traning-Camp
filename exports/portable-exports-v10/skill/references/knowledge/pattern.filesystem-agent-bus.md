---
id: pattern.filesystem-agent-bus
title: Fájlrendszer mint agent üzenetbusz
kind: pattern
maturity: reviewed
confidence: medium
language: hu
tags: [filesystem, artifacts, coordination]
aliases: [fájlrendszer agent kommunikációhoz]
relations:
  - type: depends_on
    target: pattern.isolated-context-collaboration
---

## Lényeg

Verziózott fájlok és könyvtárak hordozzák a feladatot, állapotot és eredményt, explicit tulajdonosi, atomikus írási és készültségi szabállyal.

## Miért működik

A fájlrendszer egyszerű, visszaolvasható és eszközfüggetlen közös artifact-határt ad.

## Mikor alkalmazd

Használd helyi vagy repository-alapú izolált agentmunkánál.

## Mikor ne alkalmazd

Ne használd tranzakció és zárolás nélkül nagy konkurenciájú vagy távoli elosztott koordinációhoz.

## Döntési szabály

Egy artifactnak egyszerre egy írója legyen; publikálás atomikus csere és érvényesítés után történjen.

## Hibamódok

Részleges írás, névütközés, elavult olvasás és véletlen titokpublikálás jelentkezhet.

## Kapcsolatok

A minta az izolált kontextusú artifact-együttműködésre épül.

## Ellenőrzés

Tesztelj párhuzamos írót, megszakadt írást, verzióütközést, sémát és érzékeny fájlkizárást.
