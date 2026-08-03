---
id: failure-mode.model-only-system-design
title: Csak modellre épített rendszerhiba
kind: failure-mode
maturity: reviewed
confidence: high
language: hu
tags: [agent, model, failure-mode, architecture]
aliases: [modellközpontú rendszerhiba, csak modell tervezés]
relations:
  - type: contrasts_with
    target: principle.harness-engineering
---

## Lényeg

Hiba, ha a rendszer minden feladat-, állapot-, jogosultság- és ellenőrzési döntését a modell szabad szövegű válaszára bízza.

## Miért működik

A modell erős értelmező, de nem stabil tranzakciókezelő, jogosultsági motor vagy bizonyítéknyilvántartás; ezekhez explicit rendszerhatár kell.

## Mikor alkalmazd

Vizsgáld ezt a hibamódot, amikor egy agent magabiztosan válaszol, de a végrehajtás okai, az adatok eredete vagy a változás visszavonhatósága nem látható.

## Mikor ne alkalmazd

Ne tekintsd hibának, ha a modell csak ajánlást ad, és egy determinisztikus réteg végzi a tényleges szabályérvényesítést.

## Döntési szabály

Minden biztonsági, pénzügyi, jogosultsági vagy állapotmódosító döntéshez nevezd meg a nem nyelvi ellenőrző mechanizmust.

## Hibamódok

Tipikus következmény a prompttól függő viselkedés, a nem reprodukálható módosítás, az elhallgatott hiba és a nem bizonyítható siker.

## Kapcsolatok

A keretrendszer-tervezés megelőzi ezt a hibát, az eszközszerződés pedig konkrét végrehajtási korlátot ad.

## Ellenőrzés

Egy kritikus műveletnél a modell válaszának megváltoztatása nélkül is ellenőrizhető legyen a jogosultság, a bemenet és a kimenet érvényessége.
