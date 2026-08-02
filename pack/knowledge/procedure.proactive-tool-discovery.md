---
id: procedure.proactive-tool-discovery
title: Proaktív eszközfelfedezés
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [tools, discovery, routing, capabilities]
aliases: [igény szerinti tool discovery]
relations:
  - type: supports
    target: pattern.tool-discovery
---

## Lényeg

A feladat szándékából és várható hatásából előre állíts össze kis képességjelölt-listát, majd csak a kiválasztáshoz szükséges eszközleírásokat töltsd be.

## Miért működik

A kontextus nem telítődik irreleváns sémákkal, miközben az agent képes olyan eszközt is megtalálni, amelyet induláskor nem ismert részletesen.

## Mikor alkalmazd

Nagy, változó vagy távoli eszközkatalógusnál alkalmazd.

## Mikor ne alkalmazd

Ne végezz nyílt végű discoveryt minden lépés előtt, ha a szükséges eszköz már szerződésesen kiválasztott.

## Döntési szabály

Képességkategória alapján keress, szűrj jogosultságra és költségre, töltsd be a minimális sémát, majd cache-eld csak a feladat élettartamára.

## Hibamódok

A túl széles discovery zajt, promptinjekciós felületet és nem indokolt jogosultságkérést hoz létre.

## Kapcsolatok

Az eszközfelfedezést támogatja, az MCP-eszköz kiválasztása a jelöltlista döntési lépése.

## Ellenőrzés

Mérd a releváns eszköz megtalálását, a betöltött sémák számát, a téves kiválasztást és a kontextusköltséget.
