---
id: principle.tool-interface-fidelity
title: Eszközfelület jelentéshűsége
kind: principle
maturity: reviewed
confidence: high
language: hu
tags: [tools, contracts, parameters, fidelity]
aliases: [tool paraméterhűség]
relations:
  - type: supports
    target: procedure.tool-contract-design
---

## Lényeg

Az eszközfelület őrizze meg a felhasználói szándék, a paraméterek, az előfeltételek és az eredmény jelentését minden átalakítási rétegen keresztül.

## Miért működik

A pontos típus, mértékegység, hatókör és alapértelmezés megakadályozza, hogy egy helyes modell-döntés hibás végrehajtássá torzuljon.

## Mikor alkalmazd

API-adapter, parancssori wrapper, MCP-eszköz vagy több szolgáltatáson átívelő művelet tervezésekor alkalmazd.

## Mikor ne alkalmazd

Ne vezess be kényelmi átalakítást, ha az elveszíti a felhasználó által megadott pontosságot vagy jogosultsági határt.

## Döntési szabály

Minden mezőhöz rögzíts típust, egységet, kötelezőséget, megengedett tartományt és a célrendszerbe történő pontos leképezést.

## Hibamódok

A csendes kerekítés, automatikus kitöltés vagy mezőátnevezés látszólag sikeres, de üzletileg hibás műveletet okozhat.

## Kapcsolatok

Az eszközszerződést támogatja, az eredményellenőrzés pedig a visszaút jelentéshűségét vizsgálja.

## Ellenőrzés

Határértékes és negatív integrációs tesztekben hasonlítsd össze a bemeneti szándékot a célrendszer ténylegesen fogadott paramétereivel.
