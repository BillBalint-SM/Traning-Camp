---
id: pattern.hierarchical-context-compression
title: Hierarchikus kontextustömörítés
kind: pattern
maturity: reviewed
confidence: high
language: hu
tags: [context-engineering, compression, hierarchy, state]
aliases: [hierarchikus kontextustömörítés, többszintű tömörítés]
relations:
  - type: depends_on
    target: pattern.context-compression
---

## Lényeg

Tömöríts több szinten: a friss munkamenet részletes marad, a lezárt szakaszok döntési összefoglalót kapnak, a hosszú távú állapot pedig csak stabil tényeket és nyitott kötelezettségeket őriz.

## Miért működik

A különböző időtávok eltérő pontosságot igényelnek, ezért nem kell minden korábbi részletet ugyanazzal a felbontással megtartani.

## Mikor alkalmazd

Használd hosszú párbeszédnél, kutatási vagy fejlesztési ciklusnál, illetve több agent közötti átadás előtt.

## Mikor ne alkalmazd

Ne tömöríts bizonyítékot, számot, engedélyt vagy függőben lévő kockázatot úgy, hogy az ellenőrizhetetlen következtetéssé váljon.

## Döntési szabály

Előbb jelöld ki, mely információt kell pontosan visszaidézni, melyet elég döntési szabállyá alakítani, és melyet lehet biztonságosan elengedni.

## Hibamódok

A túl korai tömörítés elveszíti a kivételt, a csak rövid összefoglalóra támaszkodó futás pedig tévesen biztosnak tekintheti a hiányzó részletet.

## Kapcsolatok

Az állapotmegjelenítés táplálja, a véges kontextus és a visszakeresési folyamat szabja meg, mikor kell újra részletet betölteni.

## Ellenőrzés

Egy tömörített munkamenetből ellenőrizhetően vissza kell állnia a célnak, a döntések indokának, a nyitott kérdéseknek és a releváns bizonyítékhoz vezető útnak.
