---
id: pattern.code-system-adapter
title: Kód mint rendszeradapter
kind: pattern
maturity: reviewed
confidence: high
language: hu
tags: [code, adapter, integration, contracts]
aliases: [rendszeradapter kóddal]
relations:
  - type: supports
    target: procedure.tool-contract-design
---

## Lényeg

Használj kicsi adaptert eltérő adatformátum, protokoll vagy rendszerhatár összeillesztésére, explicit bemeneti és kimeneti szerződéssel.

## Miért működik

Az adapter lokalizálja a kompatibilitási logikát, így a domainfolyamat nem telítődik szolgáltatásspecifikus részletekkel.

## Mikor alkalmazd

API, CLI, fájlformátum vagy régi rendszer integrációjakor alkalmazd.

## Mikor ne alkalmazd

Ne építs általános frameworköt egyetlen stabil leképezéshez.

## Döntési szabály

Az adapter egy irányt és felelősséget kezeljen, validálja a határt, és őrizze meg a paraméterek jelentését.

## Hibamódok

A túl okos adapter elrejti az adatvesztést, a retry-t és a szolgáltatás hibáját a hívó elől.

## Kapcsolatok

A tool szerződést támogatja és a tool-interface hűség elvét követi.

## Ellenőrzés

Valós integrációs mintákon ellenőrizd a sikeres, hibás és részleges válasz leképezését.
