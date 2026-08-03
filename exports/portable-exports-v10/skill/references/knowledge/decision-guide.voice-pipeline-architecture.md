---
id: decision-guide.voice-pipeline-architecture
title: Voice pipeline architektúra kiválasztása
kind: decision-guide
maturity: reviewed
confidence: medium
language: hu
tags: [voice, pipeline, architecture]
aliases: [voice pipeline architektúrát]
relations:
  - type: supports
    target: decision-guide.voice-architecture-selection
---

## Lényeg

Kaszkádolt pipeline-t válassz kontrollálhatósághoz, omnimodális modellt jelgazdag egységességhez, full-duplex modellt pedig folyamatos kétirányú beszélgetéshez.

## Miért működik

A három paradigma másképp osztja el a megfigyelhetőséget, késleltetést, cserélhetőséget és természetességet.

## Mikor alkalmazd

Használd hangos rendszer műszaki alapdöntése előtt.

## Mikor ne alkalmazd

Ne csak demótermészetesség alapján válassz mérhető feladat-, adatvédelmi és üzemeltetési követelmény nélkül.

## Döntési szabály

Ha komponensenkénti audit és csere kell, kaszkád; ha a nem szöveges jel kritikus, omni; ha átfedő beszéd kell, duplex.

## Hibamódok

Rejtett komponenshiba, túl nagy végponti késleltetés vagy ellenőrizhetetlen end-to-end viselkedés jelentkezhet.

## Kapcsolatok

Az útmutató a meglévő hangarchitektúra-választást operatív paradigmákra bontja.

## Ellenőrzés

Ugyanazon beszélgetési készleten mérd a késleltetést, megszakítást, átírási hibát, feladatsikert és költséget.
