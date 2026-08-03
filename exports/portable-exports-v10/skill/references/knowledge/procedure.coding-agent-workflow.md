---
id: procedure.coding-agent-workflow
title: Coding-agent munkafolyamat
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [coding-agent, workflow, tests, repository]
aliases: [coding agent workflow]
relations:
  - type: depends_on
    target: pattern.react-observe-act-loop
---

## Lényeg

A coding agent ciklusa: állapotfelmérés, elvárt viselkedés, reprodukció, kis módosítás, célzott ellenőrzés, teljes gate és diff-review.

## Miért működik

Minden lépés új bizonyítékot ad, így a következő döntés nem feltételezésből, hanem megfigyelt repository-állapotból születik.

## Mikor alkalmazd

Funkció, hibajavítás, refaktor vagy konfigurációs változás esetén alkalmazd.

## Mikor ne alkalmazd

Ne ugorj implementációra, ha az elvárt viselkedés vagy a hiba oka még nem bizonyított.

## Döntési szabály

Mindig a legszűkebb reprodukálható viselkedést változtasd meg, majd szélesítsd az ellenőrzést a kockázat szerint.

## Hibamódok

A kontextus nélküli javítás tünetet fed el, a túl nagy diff pedig lehetetlenné teszi, hogy tudd, melyik változás hatott.

## Kapcsolatok

A megfigyelés–döntés–cselekvés ciklusra épül; a search, editing és error recovery eljárások szakosítják.

## Ellenőrzés

A végső diffből és tesztkimenetből legyen egyértelmű az eredeti hiba, a változtatás és a bizonyított új viselkedés.
