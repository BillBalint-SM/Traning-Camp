---
id: pattern.agent-status-representation
title: Agent futási állapot megjelenítése
kind: pattern
maturity: reviewed
confidence: high
language: hu
tags: [agent, state, progress, context]
aliases: [agent status bar, futási állapotsáv]
relations:
  - type: supports
    target: pattern.react-observe-act-loop
---

## Lényeg

Tarts rövid, strukturált állapotképet a célról, az aktuális alfeladatról, a bizonyítékokról, a nyitott kockázatokról és a következő döntési pontról.

## Miért működik

Az állapotkép kis költséggel helyettesíti a teljes előzmény újraolvasását, és csökkenti annak esélyét, hogy az agent elveszítse a feladat irányát.

## Mikor alkalmazd

Használd hosszú futásoknál, átadható munkánál, eszközhibák után vagy akkor, amikor a kontextus tömörítése már szükséges.

## Mikor ne alkalmazd

Ne másold bele a teljes beszélgetést vagy nyers eszközlogot; az állapotkép döntési segédlet, nem archívum.

## Döntési szabály

Csak olyan mezőt őrizz meg, amely a következő műveletet, az engedélyezettséget vagy a sikerellenőrzést ténylegesen befolyásolja.

## Hibamódok

Az elavult státusz félrevezeti a következő iterációt, a túl részletes státusz pedig ugyanúgy felemészti a kontextuskeretet, mint a nyers előzmény.

## Kapcsolatok

A megfigyelés–döntés–cselekvés ciklus állapotát tömöríti, és együttműködik a hierarchikus tömörítéssel.

## Ellenőrzés

Egy új munkamenet az állapotképből azonosítani tudja a célt, az utolsó bizonyítékot és a következő biztonságos lépést.
