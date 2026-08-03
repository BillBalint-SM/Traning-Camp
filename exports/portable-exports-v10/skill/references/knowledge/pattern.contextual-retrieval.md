---
id: pattern.contextual-retrieval
title: Kontextuális visszakeresés
kind: pattern
maturity: reviewed
confidence: high
language: hu
tags: [retrieval, context, ranking, documents]
aliases: [kontextusos keresés]
relations:
  - type: supports
    target: procedure.hybrid-retrieval-fusion
---
## Lényeg
A kereshető részlethez adj rövid, strukturált környezeti leírást, hogy a rangsorolás a részlet helyét és szerepét is értse.
## Miért működik
Ugyanaz a mondat más jelentést kap cím, dokumentumtípus, idő és szomszédos szakasz szerint.
## Mikor alkalmazd
Rövid chunkoknál vagy hasonló nyelvű, eltérő rendeltetésű dokumentumoknál alkalmazd.
## Mikor ne alkalmazd
Ne ismételd minden darabban a teljes dokumentumot, mert zajt és költséget okoz.
## Döntési szabály
Csak olyan kontextust adj hozzá, amely megkülönbözteti a darabot a közeli, de eltérő jelentésű találatoktól.
## Hibamódok
A túl sok metaadat elfedheti a tényleges szöveget, a hiányzó környezet pedig hibás relevanciát eredményez.
## Kapcsolatok
A hibrid fúziót támogatja és a dokumentumdarabolás minőségétől függ.
## Ellenőrzés
Hasonlítsd össze a kontextus nélküli és kontextusos chunkok top-k pontosságát többértelmű kérdéseken.
