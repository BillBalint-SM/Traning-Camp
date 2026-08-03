---
id: concept.three-stage-model-development
title: Háromlépcsős modellfejlesztés
kind: concept
maturity: reviewed
confidence: medium
language: hu
tags: [pretraining, sft, rl]
aliases: [előtanítás felügyelt tanítás megerősítés]
relations:
  - type: supports
    target: decision-guide.sft-or-rl
---

## Lényeg

A modellfejlesztés három eltérő célt választ szét: általános mintázatok elsajátítása, kívánt viselkedés demonstrálása és mérhető eredményre optimalizálás.

## Miért működik

Az egyes szakaszok más adatot és visszajelzést használnak, ezért a hibák oka és a következő beavatkozás tisztábban azonosítható.

## Mikor alkalmazd

Használd képességfejlesztési program tervezésekor, amikor el kell dönteni, hogy tudás-, viselkedés- vagy céloptimalizálási hiány áll fenn.

## Mikor ne alkalmazd

Ne kezeld merev kötelező sorrendként, ha a szükséges képesség kontextussal, eszközzel vagy tudásmodullal olcsóbban és biztonságosabban megadható.

## Döntési szabály

Először nevezd meg a hiány típusát, majd csak azt a szakaszt válaszd, amelynek visszajelzési formája közvetlenül méri ezt a hiányt.

## Hibamódok

A szakaszok összemosása felesleges tanítást, rossz mérőjelet és nehezen visszafejthető regressziót okoz.

## Kapcsolatok

A fogalom az SFT és RL közötti döntést támasztja alá.

## Ellenőrzés

Minden tanítási jelölthöz rögzítsd a célképességet, a visszajelzés típusát, a baseline-t és a megállási feltételt.
