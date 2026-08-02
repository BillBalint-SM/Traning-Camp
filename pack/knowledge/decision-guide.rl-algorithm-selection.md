---
id: decision-guide.rl-algorithm-selection
title: RL algoritmus kiválasztása
kind: decision-guide
maturity: reviewed
confidence: medium
language: hu
tags: [rl, algorithm, stability]
aliases: [rl algoritmusválasztás]
relations:
  - type: depends_on
    target: concept.agent-environment-learning-loop
---

## Lényeg

Az RL algoritmust a politika frissessége, a minták újrahasznosíthatósága, a jutalom varianciája, a memóriaigény és a stabilitási korlát alapján válaszd.

## Miért működik

Az algoritmus csak a már meghatározott környezet–adat–jutalom szerződésen belül optimalizál, ezért a megfelelő illeszkedés fontosabb a névnél.

## Mikor alkalmazd

Használd, amikor a környezet és a jutalom már validált, de több optimalizálási megközelítés reális.

## Mikor ne alkalmazd

Ne algoritmusváltással próbáld elfedni a zajos jutalmat, hibás környezetet vagy gyenge mintavételt.

## Döntési szabály

Válaszd a legegyszerűbb módszert, amely a szükséges mintahatékonyságot és stabilitást bizonyítottan eléri a saját feladatodon.

## Hibamódok

Elavult trajektóriák, túl nagy frissítés, gyenge referencia-korlát és instabil értékbecslés teljesítmény-összeomlást okozhat.

## Kapcsolatok

A döntés az agent–környezet tanulási hurok pontos definíciójától függ.

## Ellenőrzés

Azonos adaton, budgeten és seed-készleten hasonlítsd össze a tanulási görbét, varianciát, költséget és regressziót.
