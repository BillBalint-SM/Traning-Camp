---
id: concept.operational-trajectory-learning-signal
title: Operatív trajektória mint tanulási jel
kind: concept
maturity: reviewed
confidence: medium
language: hu
tags: [trajectory, operations, learning]
aliases: [tanulási jelet az operatív trajektóriákból]
relations:
  - type: supports
    target: pattern.experience-driven-improvement
---

## Lényeg

Egy éles futás csak akkor válik tanulási jellé, ha a helyzet, döntések, eszközeredmények, végállapot, visszajelzés és bizonytalanság együtt visszakereshető.

## Miért működik

A teljes trajektória különválasztja az okot a következménytől, és lehetővé teszi ugyanazon hibaminta összehasonlítását több futás között.

## Mikor alkalmazd

Használd ismétlődő agentfeladatoknál, ahol valódi eredmény és elegendő megfigyelhetőség áll rendelkezésre.

## Mikor ne alkalmazd

Ne alakíts naplót tanulási adattá hozzájárulás, adatminimalizálás, sikerjel vagy megbízható azonosítás nélkül.

## Döntési szabály

Csak olyan trajektória jelölhető fejlesztési bizonyítéknak, amelynek eredménye függetlenül ellenőrizhető és hibakategóriája reprodukálható.

## Hibamódok

Hiányos logging, túlélési torzítás, érzékeny adat és önbevallott siker hamis tanulságot vagy adatvédelmi kockázatot okoz.

## Kapcsolatok

A fogalom az ellenőrzött tapasztalatból vezérelt fejlesztést támasztja alá.

## Ellenőrzés

Mintánként olvasd vissza a teljes eseménysort, reprodukáld a végállapotot, és hasonlítsd össze a független sikerjellel.
