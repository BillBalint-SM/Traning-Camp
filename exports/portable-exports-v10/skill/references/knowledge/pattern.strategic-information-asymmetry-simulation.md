---
id: pattern.strategic-information-asymmetry-simulation
title: Stratégiai információaszimmetria-szimuláció
kind: pattern
maturity: reviewed
confidence: medium
language: hu
tags: [strategy, information, simulation]
aliases: [rejtett információs agent játék]
relations:
  - type: supports
    target: concept.agent-society-simulation
---

## Lényeg

Adj eltérő privát információt, célokat és kommunikációs jogokat az agenteknek, majd mérd a következtetést, megtévesztést, koalíciót és kalibrációt.

## Miért működik

A kontrollált rejtett állapot feltárja, hogyan viselkedik a rendszer, amikor a kommunikáció nem azonos az igazsággal.

## Mikor alkalmazd

Használd stratégiai döntés, tárgyalás és bizalmi protokoll kutatására szimulációban.

## Mikor ne alkalmazd

Ne képezd át a megtévesztési stratégiát valós felhasználói interakcióba explicit biztonsági cél nélkül.

## Döntési szabály

A privát állapot, megengedett kommunikáció és értékelési cél előre rögzített legyen, az eredményt több seed igazolja.

## Hibamódok

Meta-jel szivárgás, szerepkeverés, evaluator-torzítás és egyetlen érdekes narratíva túlértékelése jelentkezhet.

## Kapcsolatok

A minta az agenttársadalom-szimuláció egyik kontrollált stratégiai környezete.

## Ellenőrzés

Ellenőrizd a rejtett állapot szeparációját, kommunikációs naplót, seed-stabilitást és baseline stratégiákat.
