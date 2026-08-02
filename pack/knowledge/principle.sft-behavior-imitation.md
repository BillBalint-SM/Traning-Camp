---
id: principle.sft-behavior-imitation
title: Az SFT viselkedésmintát tanít
kind: principle
maturity: reviewed
confidence: medium
language: hu
tags: [sft, demonstrations, behavior]
aliases: [sft viselkedésutánzás]
relations:
  - type: supports
    target: pattern.sft-rl-learning-boundary
---

## Lényeg

A felügyelt finomhangolás a bemutatott válaszok eloszlását tanulja meg, ezért elsősorban formát, stílust és demonstrálható eljárást rögzít.

## Miért működik

A célválasz közvetlen tokenenkénti jelzést ad, így kevésbé ritka és stabilabb tanulási jelet biztosít, mint egy késői összesített jutalom.

## Mikor alkalmazd

Használd, ha szakértői példával egyértelműen megmutatható a kívánt válasz vagy eszközhasználati minta.

## Mikor ne alkalmazd

Ne várj tőle megbízható céloptimalizálást olyan helyzetben, ahol több eltérő út is helyes és csak a végrehajtott eredmény értékelhető.

## Döntési szabály

Ha a helyes viselkedés teljes trajektóriája olcsón és következetesen demonstrálható, az SFT legyen az első súlymódosító beavatkozás.

## Hibamódok

Gyenge demonstrációk lemásoltatják a hibákat; túl szűk példakészlet felületi utánzást és rossz általánosítást eredményez.

## Kapcsolatok

Az elv pontosítja a felügyelt és jutalom-alapú tanulás határát.

## Ellenőrzés

Mérd külön a formátumkövetést, a feladat sikerét és az eloszláson kívüli eseteket.
