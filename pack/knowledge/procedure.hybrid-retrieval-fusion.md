---
id: procedure.hybrid-retrieval-fusion
title: Hibrid visszakeresési fúzió
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [retrieval, hybrid, ranking]
aliases: [sűrű és ritka keresés egyesítése]
relations:
  - type: depends_on
    target: decision-guide.retrieval-strategy-selection
---
## Lényeg
Egyesítsd a lexikális és szemantikus jel találatait, majd közös, mérhető rangsorral válassz kontextust.
## Miért működik
Az egyik jel a pontos formát, a másik a jelentésbeli változatot fedi le.
## Mikor alkalmazd
Vegyes dokumentumtárnál és bizonytalan lekérdezésformánál alkalmazd.
## Mikor ne alkalmazd
Ne kombinálj jeleket, ha nincs relevanciaadat a súlyok ellenőrzésére.
## Döntési szabály
Normalizáld a rangokat, tartsd meg az egyedi jel erős találatait, és csak utána újrarendezz.
## Hibamódok
A rossz súlyozás zajt emel előre vagy elrejti a pontos azonosítót.
## Kapcsolatok
A retrieval stratégia választására épül, a kontextuális retrieval tovább javíthatja.
## Ellenőrzés
Hasonlítsd össze a külön és egyesített keresők top-k relevanciáját, késleltetését és költségét.
