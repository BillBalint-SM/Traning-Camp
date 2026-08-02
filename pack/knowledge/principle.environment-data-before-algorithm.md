---
id: principle.environment-data-before-algorithm
title: Környezet és adat az algoritmus előtt
kind: principle
maturity: reviewed
confidence: high
language: hu
tags: [post-training, environment, data, evaluation]
aliases: [environment data before algorithm, környezet és adat előbb]
relations:
  - type: supports
    target: pattern.sft-rl-learning-boundary
---

## Lényeg

Agent fejlesztésnél a jó környezet, a tiszta sikerjel és a reprezentatív adat több értéket ad, mint egy összetettebb tanulási algoritmus önmagában.

## Miért működik

A modell csak azt tud optimalizálni, amit a példák és a visszajelzés megkülönböztet; rossz céljel mellett az algoritmus hatékonyan tanulhat rosszat.

## Mikor alkalmazd

Használd minden post-training, önfejlesztési vagy értékelési beruházás priorizálásakor.

## Mikor ne alkalmazd

Ne halogasd végtelenül az algoritmikus problémát, ha a környezet és az adat már mérhetően elég jó, de a választott módszer bizonyítottan nem konvergál.

## Döntési szabály

Mielőtt algoritmust cserélsz, ellenőrizd, hogy a feladatkészlet lefedi-e a valós eseteket, a sikerjel nem manipulálható-e, és a hibás minták visszakereshetők-e.

## Hibamódok

A rossz minőségű adatból épített nagy tréning, a nem valós környezet és a pusztán benchmarkra optimalizált jutalom általánosítási hibát okoz.

## Kapcsolatok

Az SFT–RL határt és az értékelési környezet tervezését is ez a prioritási elv vezeti.

## Ellenőrzés

Mutasd ki, hogy az adatkészlet és a környezet változtatása nagyobb vagy kisebb hatást gyakorol-e a mérőszámokra, mint az algoritmus módosítása.
