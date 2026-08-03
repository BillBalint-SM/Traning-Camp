---
id: procedure.programmatic-skill-evolution
title: Programozott képességfejlesztés
kind: procedure
maturity: reviewed
confidence: medium
language: hu
tags: [program, skill, evolution]
aliases: [tapasztalat programba]
relations:
  - type: supports
    target: principle.agent-tool-bootstrapping
---

## Lényeg

Az ismételhető, determinisztikus és tesztelhető tapasztalatot kis célfüggvénnyé, validátorrá vagy eszközzé alakítsd explicit szerződéssel.

## Miért működik

A program leveszi a modellről a pontos ismétlés terhét, végrehajtható szabályt ad és hagyományos tesztekkel ellenőrizhető.

## Mikor alkalmazd

Használd stabil adatátalakítás, ellenőrzés, számítás vagy ismétlődő rendszerintegráció esetén.

## Mikor ne alkalmazd

Ne generálj és engedj automatikusan kódot jogosultság, sandbox, review és valós viselkedési teszt nélkül.

## Döntési szabály

Ha a javítás tiszta bemenet–kimenet szerződéssel és determinisztikus invariánsokkal leírható, program legyen az első jelölt.

## Hibamódok

Túl széles jogosultság, rejtett mellékhatás, függőségi kockázat és rossz hibakezelés új támadási felületet hoz létre.

## Kapcsolatok

Az eljárás az agent új eszköz létrehozására képes meta-képességét támogatja.

## Ellenőrzés

Futtass pozitív, negatív, határ- és jogosultsági tesztet, majd hasonlítsd össze a programos és modell-only végrehajtás eredményét.
