---
id: principle.harness-engineering
title: Agent keretrendszer-tervezés
kind: principle
maturity: reviewed
confidence: high
language: hu
tags: [agent, orchestration, harness]
aliases: [harness engineering, agent keretrendszer]
relations:
  - type: supports
    target: principle.agent-operating-model
---

## Lényeg

Az agent megbízhatóságát elsősorban a modell körüli futtatási keret adja: az állapot, a kontextus, az eszközök, az ellenőrzések és a leállítási feltételek közös rendszere.

## Miért működik

A keret teszi ismételhetővé azt, amit a modell önmagában csak valószínűsíteni tud: mikor gyűjtsön adatot, mikor hajtson végre, mit rögzítsen és mikor kérjen segítséget.

## Mikor alkalmazd

Használd több lépéses, eszközhasználó vagy állapotot öröklő feladatnál, ahol a jó válasz mellett a végrehajtási út is számít.

## Mikor ne alkalmazd

Ne növeld teljes agent keretté az egyszeri, visszafordítható szövegfeladatot, ha a determinisztikus feldolgozás rövidebb és ellenőrizhetőbb.

## Döntési szabály

Előbb rajzold fel a megfigyelés, döntés, végrehajtás és ellenőrzés határait; ha egy lépés tulajdonosa vagy kimenete nem egyértelmű, a keret még hiányos.

## Hibamódok

A láthatatlan állapot, a szabadon növekvő eszközlista és a sikerkritérium nélküli iteráció olyan hibát eredményez, amelyet utólag sem lehet megmagyarázni.

## Kapcsolatok

Az agent működési modelljét konkretizálja, és alapot ad a workflow vagy autonómia választásához.

## Ellenőrzés

Egy futás naplója külön azonosítja a bemenetet, a kiválasztott eszközt, az állapotváltozást, az eredményt és a leállítás okát.
