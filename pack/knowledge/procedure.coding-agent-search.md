---
id: procedure.coding-agent-search
title: Coding-agent keresési eljárás
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [coding-agent, search, codebase, evidence]
aliases: [kódbázis keresés agenttel]
relations:
  - type: supports
    target: procedure.coding-agent-workflow
---

## Lényeg

Kereséskor az azonosítótól és hibaüzenettől haladj a definíció, hívó, teszt, konfiguráció és futási adatfolyam felé.

## Miért működik

A célzott keresés gyorsan feltárja a repository saját mintáit és azokat a határokat, ahol az adat vagy állapot megváltozik.

## Mikor alkalmazd

Ismeretlen kódbázis, regresszió, duplikált logika vagy módosítási pont keresésekor alkalmazd.

## Mikor ne alkalmazd

Ne olvass végig teljes könyvtárakat, ha egy pontos azonosító vagy teszt néhány releváns fájlra szűkíthet.

## Döntési szabály

Először fájlt és szimbólumot keress, majd csak a releváns környezetet olvasd; minden következtetéshez jelölj konkrét kódbizonyítékot.

## Hibamódok

A felszíni szövegegyezés téves módosítási pontra vihet, a hívási lánc kihagyása pedig rejtett fogyasztót törhet el.

## Kapcsolatok

A coding workflow-t támogatja; a safe editing csak a bizonyított módosítási pont után következik.

## Ellenőrzés

A kiválasztott fájlról legyen igazolható, hogy tartalmazza a viselkedés tulajdonosát, a tesztet és az érintett fogyasztókat.
