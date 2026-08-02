---
id: pattern.generative-ui
title: Generatív felhasználói felület
kind: pattern
maturity: reviewed
confidence: high
language: hu
tags: [code, ui, generation, interaction]
aliases: [generált UI kóddal]
relations:
  - type: applies_to
    target: principle.code-as-meta-capability
---

## Lényeg

Az agent feladatspecifikus felületet generálhat strukturált adatból, de a komponensek, események és jogosultságok engedélyezett készletből származzanak.

## Miért működik

A felület a feladat információigényéhez igazítható anélkül, hogy tetszőleges kód korlátlanul futna a felhasználó környezetében.

## Mikor alkalmazd

Dinamikus dashboard, konfigurátor vagy egyszeri döntéstámogató nézet esetén alkalmazd.

## Mikor ne alkalmazd

Ne generálj kritikus tranzakciós UI-t validált komponens- és eseményszerződés nélkül.

## Döntési szabály

A modell deklaratív UI-sémát állítson elő, a host pedig validálja és kontrollált komponensekből renderelje.

## Hibamódok

A tetszőleges script, nem stabil mezőazonosító vagy rejtett állapot manipulálható és nem tesztelhető felülethez vezet.

## Kapcsolatok

A kód metaképességét alkalmazza; a multimodális interakciós határ és GUI-grounding korlátozza.

## Ellenőrzés

Teszteld a sémavalidációt, hozzáférhetőséget, eseményhatást és tiltott komponens elutasítását.
