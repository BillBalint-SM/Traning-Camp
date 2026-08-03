---
id: pattern.offline-consolidation-cycle
title: Offline konszolidációs ciklus
kind: pattern
maturity: reviewed
confidence: medium
language: hu
tags: [offline, consolidation, forgetting]
aliases: [alvási tanulási ciklus]
relations:
  - type: depends_on
    target: procedure.knowledge-consolidation-from-experience
---

## Lényeg

Az online futástól elkülönített időablakban csoportosítsd a tapasztalatokat, oldd fel a konfliktusokat, felejtsd el az elavult jeleket, és mérd újra a megtartandó képességeket.

## Miért működik

Az offline szakasz csökkenti a futás közbeni instabilitást, kötegelt review-t tesz lehetővé és kontrolláltan kezeli a tudástár növekedését.

## Mikor alkalmazd

Használd nagy mennyiségű operatív tapasztalatnál, amelyet nem kell azonnal beépíteni.

## Mikor ne alkalmazd

Ne várj a ciklusra sürgős biztonsági visszavonással vagy kritikus, bizonyított hibajavítással.

## Döntési szabály

Azonnal csak kritikus és igazolt korrekciót adj ki; minden más jelölt menjen verziózott offline konszolidációba.

## Hibamódok

Korlátlan felhalmozás, ellenőrizetlen felejtés, konfliktusok felülírása és képességregresszió csendes minőségromlást okoz.

## Kapcsolatok

A minta a tapasztalat tudássá konszolidálására épül.

## Ellenőrzés

Mérd ciklusonként a tudásméretet, konfliktusokat, törléseket, frissességet és a képességmegőrzési regressziós készletet.
