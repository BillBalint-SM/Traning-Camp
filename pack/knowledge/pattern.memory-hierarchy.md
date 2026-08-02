---
id: pattern.memory-hierarchy
title: Hierarchikus memória
kind: pattern
maturity: reviewed
confidence: high
language: hu
tags: [memory, hierarchy, session, user]
aliases: [memóriaszintek, felhasználóhoz memóriaszinteket]
relations:
  - type: depends_on
    target: procedure.user-memory-lifecycle
---

## Lényeg

Válaszd el a futó lépés munkamemóriáját, a session összefoglalóját, a tartós felhasználói tudást és a külső tudásbázist.

## Miért működik

Minden szintnek más az élettartama, frissítési költsége, jogalapja és hibakockázata, ezért ugyanaz a tárolási szabály nem illik rájuk.

## Mikor alkalmazd

Hosszú interakció, több session, személyre szabás vagy külső dokumentumtár esetén alkalmazd.

## Mikor ne alkalmazd

Ne tárolj tartósan olyan átmeneti állapotot, amely kizárólag egy futó feladat végrehajtásához kell.

## Döntési szabály

Az információt a legrövidebb olyan szintre írd, amely a kívánt viselkedéshez elegendő, és minden magasabb szintű íráshoz adj külön frissítési és törlési szabályt.

## Hibamódok

A szintek összemosása elavult adatot, felesleges személyesítést, drága kontextust és nehezen teljesíthető törlést okoz.

## Kapcsolatok

A memória életciklusára épül; a reprezentációválasztás és a konszolidáció az egyes szinteken történő kezelést részletezi.

## Ellenőrzés

Egy példainformációról meg kell tudni mondani, melyik szinten él, ki írhatja, meddig marad érvényes és hogyan törölhető.
