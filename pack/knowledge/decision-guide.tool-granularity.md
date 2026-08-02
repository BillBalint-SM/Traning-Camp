---
id: decision-guide.tool-granularity
title: Eszköz-granularitás választása
kind: decision-guide
maturity: reviewed
confidence: high
language: hu
tags: [tools, granularity, contracts, capability]
aliases: [tool granularity, eszköz granularitás]
relations:
  - type: depends_on
    target: concept.tool-capability-taxonomy
---

## Lényeg

Szűk eszközt adj, ha a művelet érzékeny vagy gyakori ellenőrzést igényel; általános végrehajtót csak akkor adj, ha a bemenet korlátozása és a sandbox valóban érvényesíthető.

## Miért működik

A kisebb eszközfelület csökkenti a hibás paraméterezés és a váratlan mellékhatás terét, míg az általános végrehajtó a jól kontrollált, sokféle feladatnál csökkentheti az integrációs költséget.

## Mikor alkalmazd

Használd eszközkatalógus tervezésekor és akkor, amikor egy új képességet skill, dedikált tool vagy általános executor formában kell kifejezni.

## Mikor ne alkalmazd

Ne bonts szét minden apró API-hívást külön eszközzé, ha a túl nagy választék rontja a kiválasztás pontosságát.

## Döntési szabály

Ha egy hibás paraméter visszafordíthatatlan vagy nagy hatású, dedikált, szűk szerződésű eszközt használj; ha a művelet sandboxban teljesen izolált, általános executor is elfogadható.

## Hibamódok

A túl tág eszköz rejtett jogosultságot ad, a túl sok mikroszintű eszköz pedig választási bénulást és hibás hívást okoz.

## Kapcsolatok

Az eszközképesség-osztályozást és a nem biztonságos bővítés hibamódját egyaránt figyelembe veszi.

## Ellenőrzés

Hasonlítsd össze a kiválasztási hibaarányt, a hibás paraméterezést, a jóváhagyási igényt és a sikeres végrehajtást két különböző granularitási terven.
