---
id: principle.code-as-meta-capability
title: A kód mint metaképesség
kind: principle
maturity: reviewed
confidence: high
language: hu
tags: [coding-agent, code, tools, automation]
aliases: [kód mint új eszköz]
relations:
  - type: supports
    target: principle.harness-engineering
---

## Lényeg

A kód nem csupán kimenet: az agent új, végrehajtható eszközt, ellenőrzést és adaptert hozhat létre vele egy feladat megoldásához.

## Miért működik

A program pontos, ismételhető állapotátmenetté alakítja a nyelvi szándékot, és futás közben mérhető eredményt ad.

## Mikor alkalmazd

Ismétlődő transzformáció, adatfeldolgozás, integráció vagy új ellenőrzés szükségénél alkalmazd.

## Mikor ne alkalmazd

Ne generálj kódot egyszeri, egyszerű olvasási feladathoz, ha egy meglévő szűk eszköz kisebb kockázattal megoldja.

## Döntési szabály

Csak akkor írj új kódot, ha a kívánt viselkedés tesztelhető szerződéssé alakítható, és a futtatási környezet korlátozható.

## Hibamódok

A nem ellenőrzött generált kód új jogosultságot, rejtett mellékhatást és nehezen auditálható függőséget hozhat létre.

## Kapcsolatok

A harness engineeringet támogatja; az izolált futtatás és a coding-agent biztonság korlátozza.

## Ellenőrzés

Futtass valós bemeneten pozitív, határ- és hibatesztet, majd igazold a létrehozott eszköz hatókörét és megismételhetőségét.
