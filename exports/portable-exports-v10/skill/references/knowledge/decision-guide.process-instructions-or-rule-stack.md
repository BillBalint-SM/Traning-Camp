---
id: decision-guide.process-instructions-or-rule-stack
title: Folyamatutasítás vagy szabályhalmaz
kind: decision-guide
maturity: reviewed
confidence: high
language: hu
tags: [prompt, process, rules, orchestration]
aliases: [folyamat vagy szabálylista]
relations:
  - type: depends_on
    target: procedure.prompt-structure-design
---

## Lényeg

Ismétlődő, állapotfüggő munkához lépéses folyamatutasítást, ritka és egymástól független korlátozáshoz rövid szabályhalmazt használj.

## Miért működik

A folyamat a döntések sorrendjét adja meg, míg a szabályhalmaz a tiltott vagy kötelező határokat rögzíti; a kettő más hibát előz meg.

## Mikor alkalmazd

Prompt egyszerűsítésekor vagy olyan hibánál, amikor a modell tudja a szabályt, de rossz sorrendben jár el.

## Mikor ne alkalmazd

Ne írj hosszú folyamatot egylépéses korlátozáshoz, és ne próbálj többállapotú munkafolyamatot egymásra rakott tiltásokból vezetni.

## Döntési szabály

Ha a következő lépés az előző eredményétől függ, írj folyamatot; ha a döntés bármely pontján ugyanaz a korlát érvényes, írj szabályt.

## Hibamódok

Szabályhalmazból a modell kihagyhat köztes ellenőrzést, túl merev folyamatból pedig nem tud kezelni legitim kivételt.

## Kapcsolatok

A promptstruktúrára épül, az üzleti szabályok fordítása pedig a szabályok gépileg követhető formáját adja.

## Ellenőrzés

Tesztelj normál, kivételes és tiltott útvonalat; a folyamatnak a helyes sorrendet, a szabályoknak a helyes határt kell érvényesíteniük.
