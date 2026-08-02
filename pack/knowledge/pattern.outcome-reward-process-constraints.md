---
id: pattern.outcome-reward-process-constraints
title: Eredményjutalom folyamatkorlátokkal
kind: pattern
maturity: reviewed
confidence: medium
language: hu
tags: [reward, constraints, safety]
aliases: [eredményt jutalmazd folyamatot korlátozd]
relations:
  - type: supports
    target: decision-guide.process-or-outcome-reward
---

## Lényeg

A hasznosságot a végállapot jutalma vezérelje, míg a folyamat kritikus biztonsági és érvényességi szabályait kemény korlátok vagy részleges kredit védje.

## Miért működik

A minta megtartja a stratégiai szabadságot, de kizárja azokat az utakat, amelyek jó végpontot tiltott vagy megbízhatatlan módon érnek el.

## Mikor alkalmazd

Használd eszközhasználatnál, kódvégrehajtásnál és jogosultságot érintő többfordulós feladatnál.

## Mikor ne alkalmazd

Ne kódolj preferenciát kemény korláttá, ha több legitim folyamatváltozatot nem tudsz előre felsorolni.

## Döntési szabály

Csak invariáns biztonsági és szerződéses szabály legyen kemény; minden másnál a bizonyított végsiker döntsön.

## Hibamódok

Túl sok korlát bénítja a feltárást, hiányos korlát pedig optimalizálható rést hagy a jutalom és a valódi cél között.

## Kapcsolatok

A minta a folyamat- és eredményjutalom döntés gyakorlati kombinációja.

## Ellenőrzés

Generálj szándékos kiskapu-próbákat, és ellenőrizd, hogy a korlát elutasítja őket anélkül, hogy helyes alternatívákat blokkolna.
