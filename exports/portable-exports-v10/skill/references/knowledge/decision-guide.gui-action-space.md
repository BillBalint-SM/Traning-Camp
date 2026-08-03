---
id: decision-guide.gui-action-space
title: GUI agent action space tervezése
kind: decision-guide
maturity: reviewed
confidence: medium
language: hu
tags: [gui, action-space, safety]
aliases: [gui agent action space-ét]
relations:
  - type: depends_on
    target: concept.gui-agent-observation-loop
---

## Lényeg

Az akcióteret a lehető legszűkebb szemantikus műveletekből építsd, koordinátás vezérlést csak stabil elemhorgony hiányában engedj.

## Miért működik

A kisebb, típusos akciótér javítja a tanulhatóságot, auditálhatóságot és jogosultsági kontrollt.

## Mikor alkalmazd

Használd GUI-automatizálási harness és értékelési környezet tervezésekor.

## Mikor ne alkalmazd

Ne adj általános shellt, vágólapot vagy korlátlan billentyűzetet, ha a feladat szűk műveletekkel megoldható.

## Döntési szabály

Stabil azonosító előbb, accessibility-fa másodszor, vizuális horgony harmadszor, nyers koordináta utoljára.

## Hibamódok

Túl nagy akciótér, felbontásfüggés és rejtett mellékhatás növeli a téves végrehajtást.

## Kapcsolatok

A döntés a GUI megfigyelés–végrehajtás zárt hurkára épül.

## Ellenőrzés

Tesztelj átméretezést, lokalizációt, fókuszváltást, tiltott műveletet és állapot-visszaolvasást.
