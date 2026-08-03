---
id: decision-guide.retrieval-strategy-selection
title: Visszakeresési stratégia választása
kind: decision-guide
maturity: reviewed
confidence: high
language: hu
tags: [retrieval, hybrid-retrieval, search, knowledge]
aliases: [retrieval stratégia választás, hibrid retrieval, hibrid retrievalt visszakereséséhez]
relations:
  - type: depends_on
    target: procedure.retrieval-pipeline-design
---

## Lényeg

Pontos név, azonosító vagy jogszabályjellegű kérdéshez lexikális keresést, jelentésben változatos kérdéshez szemantikus keresést, vegyes helyzethez hibrid visszakeresést válassz.

## Miért működik

A kulcsszavas és szemantikus jel más hibát fed fel: az egyik a pontos egyezést, a másik a megfogalmazási változatokat kezeli jól.

## Mikor alkalmazd

Használd akkor, amikor a tudásbázisban egyszerre vannak kódok, nevek, strukturált mezők és természetes nyelvű magyarázatok.

## Mikor ne alkalmazd

Ne adj össze vakon több keresőt, ha nincs mérésed arra, hogy a második jel milyen hiányt javít és milyen zajt hoz.

## Döntési szabály

Ha a lekérdezésben egyedi azonosító vagy pontos kifejezés van, kezdd lexikálisan; ha a várt válasz fogalmi, indíts szemantikusan; bizonytalanságnál használd a kettőt újrarendezéssel.

## Hibamódok

A kizárólag szemantikus keresés elvétheti az azonosítót, a kizárólag kulcsszavas keresés pedig nem találja meg az átfogalmazott releváns anyagot.

## Kapcsolatok

A visszakeresési folyamat minőségétől függ, és a strukturált index szűrőivel kombinálható.

## Ellenőrzés

Ugyanazon kérdéskészleten hasonlítsd össze a lexikális, szemantikus és hibrid találati arányt, zaját, késleltetését és költségét.
