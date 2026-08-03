---
id: procedure.mcp-tool-selection
title: MCP-eszköz kiválasztása
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [mcp, tools, discovery, selection]
aliases: [MCP tool választás]
relations:
  - type: depends_on
    target: pattern.tool-discovery
---

## Lényeg

Az MCP-eszközt a szükséges képesség, jogosultság, bemeneti szerződés és várható bizonyíték alapján válaszd, ne pusztán a név hasonlósága szerint.

## Miért működik

A képességalapú szűrés csökkenti a nagy eszközkatalógusokban előforduló téves kiválasztást és a túl széles hozzáférést.

## Mikor alkalmazd

Több szerver, átfedő eszköz vagy dinamikusan betölthető képesség esetén alkalmazd.

## Mikor ne alkalmazd

Ne tölts be teljes eszközkatalógust a kontextusba, ha a feladatból szűk képességcsoport következik.

## Döntési szabály

Előbb osztályozd a kívánt hatást, majd szűrj jogosultságra és szerződésre; csak ezután rangsorolj leírás és korábbi mérés alapján.

## Hibamódok

A névalapú választás összekeverhet olvasó és író eszközt, vagy hasonló nevű, eltérő hatókörű szolgáltatást.

## Kapcsolatok

Az eszközfelfedezésre épül; a proaktív discovery szűkített katalógust készít hozzá.

## Ellenőrzés

Átfedő eszköznevekkel teszteld, hogy a kiválasztás a szerződésesen helyes és legkisebb jogosultságú eszközt adja.
