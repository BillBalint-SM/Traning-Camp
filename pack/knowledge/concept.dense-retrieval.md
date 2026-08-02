---
id: concept.dense-retrieval
title: Szemantikus visszakeresés
kind: concept
maturity: reviewed
confidence: high
language: hu
tags: [retrieval, semantic-search, embeddings, similarity]
aliases: [dense retrieval]
relations:
  - type: supports
    target: decision-guide.retrieval-strategy-selection
---

## Lényeg

A szemantikus visszakeresés a kérdés és a tudásegység jelentésbeli hasonlóságát használja akkor is, ha a szavak eltérnek.

## Miért működik

Azonos fogalom sokféle megfogalmazását képes egymáshoz közelíteni, ezért javítja az átfogalmazott kérdések felidézését.

## Mikor alkalmazd

Fogalmi, természetes nyelvű vagy szinonimákkal teli kérdéseknél alkalmazd.

## Mikor ne alkalmazd

Ne várj tőle pontos azonosító-, verzió-, kód- vagy névillesztést önmagában.

## Döntési szabály

Ha a kérdés jelentésben gazdag, de a szóalak bizonytalan, indulj szemantikus jellel, és adj hozzá szűrőt vagy hibrid jelet, ha pontos mező is fontos.

## Hibamódok

A fogalmi közelség relevánsnak tűnő, de hibás találatot emelhet az első helyre.

## Kapcsolatok

A retrieval stratégia választását támogatja, a hibrid fúzió a lexikális jelével kombinálja.

## Ellenőrzés

Mérd külön az átfogalmazott kérdések recallját és a top találatok tényleges válaszhasznát emberi vagy szabályalapú bírálattal.
