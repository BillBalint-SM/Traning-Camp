---
id: procedure.prompt-structure-design
title: Promptstruktúra tervezése
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [prompt, context, instructions, structure]
aliases: [strukturált rendszerprompt]
relations:
  - type: depends_on
    target: procedure.system-prompt-architecture
---

## Lényeg

A rendszerutasítást cél, hatáskör, folyamat, tilalmak, eszközszabályok, kimeneti szerződés és eszkalációs feltételek szerint tagold.

## Miért működik

A világos szerkezet egyszerre segíti a modell következetes viselkedését és az emberi review-t, mert minden szabály szerepe visszakereshető.

## Mikor alkalmazd

Összetett agent vagy új üzleti folyamat bevezetésekor alkalmazd.

## Mikor ne alkalmazd

Ne építs szabálygyűjteményt, ha a tényleges folyamat még nincs megfogalmazva vagy az eszközszerződés hiányzik.

## Döntési szabály

Előbb a kívánt állapotátmeneteket írd le, majd csak azokat a szabályokat tedd be, amelyek egy konkrét átmenetet korlátoznak vagy ellenőriznek.

## Hibamódok

Az ismétlődő, ellentmondó vagy sorrend nélküli szabályok esetén a modell kiszámíthatatlan prioritást alakít ki.

## Kapcsolatok

A rendszerprompt architektúrára épül; a folyamatutasítás és üzleti szabály fordítása részletesíti.

## Ellenőrzés

Minden fontos szabályhoz legyen egy pozitív és egy tiltott példa, amelyből egyértelmű, hogy a struktúra a kívánt viselkedést adja.
