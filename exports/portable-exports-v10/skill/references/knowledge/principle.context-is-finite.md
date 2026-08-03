---
id: principle.context-is-finite
title: A kontextus véges erőforrás
kind: principle
maturity: validated
confidence: high
language: hu
tags: [context, token-budget, relevance]
aliases: [finite context, véges kontextus]
relations:
  - type: supports
    target: pattern.context-budget-allocation
---

## Lényeg

A kontextuskeret nem tárhely, hanem korlátozott figyelmi költségvetés: minden bekerülő elem versenyez a feladat szempontjából fontos bizonyítékokkal.

## Miért működik

A rövidebb, relevánsabb bemenet csökkenti az egymásnak ellentmondó utasítások és az elvesző kulcsfeltételek esélyét. A keret tudatos kiosztása a válasz minőségét is stabilizálja.

## Mikor alkalmazd

Alkalmazd hosszú beszélgetések, sok dokumentum, több eszközeredmény vagy ismétlődő agent körök esetén.

## Mikor ne alkalmazd

Ne rövidíts mechanikusan olyan adatot, amelynek minden sora jogi, pénzügyi vagy biztonsági döntést befolyásolhat.

## Döntési szabály

Minden új kontextuselemet csak akkor tarts meg, ha közvetlenül változtathatja a következő döntést, a korlátot vagy az ellenőrzést.

## Hibamódok

A teljes előzmény változatlan továbbadása zajt és régi feltételeket örökít. A túl agresszív rövidítés ezzel szemben elveszítheti a kivételeket.

## Kapcsolatok

Ez az elv támasztja alá a kontextuskeret elosztását és a kontextustömörítést.

## Ellenőrzés

Mérd meg, hogy az adott kontextus nélkül vagy helyett rövidebb, releváns kivonattal ugyanaz a döntés születik-e.
