---
id: decision-guide.collaboration-topology
title: Kollaborációs topológia kiválasztása
kind: decision-guide
maturity: reviewed
confidence: medium
language: hu
tags: [topology, coordination, ownership]
aliases: [manager peer decentralizált topológia]
relations:
  - type: supports
    target: decision-guide.multi-agent-topology-selection
---

## Lényeg

Manager topológiát válassz központi prioritáshoz, peer review-t kölcsönös ellenőrzéshez, decentralizált átadást pedig helyi autonómiához és skálázáshoz.

## Miért működik

A topológia a döntési jogot és hibaterjedési utat a feladat függőségeihez igazítja.

## Mikor alkalmazd

Használd összetett munka felbontása és felelősségkiosztása előtt.

## Mikor ne alkalmazd

Ne növeld az agentek számát, ha a munka nem párhuzamosítható vagy az integráció drágább a részfeladatnál.

## Döntési szabály

A legkevesebb koordinációs éllel rendelkező topológiát válaszd, amely még biztosítja a szükséges kontrollt.

## Hibamódok

Manager-szűk keresztmetszet, peer végtelen vita és decentralizált felelősségvesztés jelenhet meg.

## Kapcsolatok

Az útmutató a meglévő topológiaválasztást konkrét működési határokkal bővíti.

## Ellenőrzés

Mérd a kritikus út hosszát, handoffok számát, duplikációt, blokkolást és integrációs hibát.
