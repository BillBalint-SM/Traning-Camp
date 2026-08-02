---
id: pattern.context-budget-allocation
title: Kontextuskeret elosztása
kind: pattern
maturity: validated
confidence: high
language: hu
tags: [context-engineering, token-budget, routing]
aliases: [context budget allocation, kontextuskeret elosztása]
relations:
  - type: depends_on
    target: principle.context-is-finite
  - type: supports
    target: pattern.context-compression
---

## Lényeg

A kontextuskeretet előre oszd fel feladatcélra, kötelező korlátokra, friss bizonyítékra, eszközeredményekre és választervre.

## Miért működik

Az explicit keret megakadályozza, hogy egyetlen hosszú mellékág elfoglalja a döntési tér nagy részét. A rendszer így a következő lépéshez szükséges információt részesíti előnyben.

## Mikor alkalmazd

Használd hosszú munkafolyamatban, ahol több dokumentum és több eszközhívás érkezik ugyanabba a döntésbe.

## Mikor ne alkalmazd

Ne kezeld merev kvótaként, ha egyetlen bizonyíték teljes egészében szükséges a biztonságos válaszhoz.

## Döntési szabály

Tarts fenn külön keretet a változhatatlan korlátoknak és a legutóbbi megfigyelésnek; a maradékból csak a következő döntést módosító anyagot töltsd be.

## Hibamódok

Hiba, ha a keret csak dokumentumhosszt mér, relevanciát nem. Hiba az is, ha a korlátozó utasítások összefoglalás közben eltűnnek.

## Kapcsolatok

A minta a véges kontextusból következik, és a tömörítés előtt ad rendezési szempontot.

## Ellenőrzés

Minden körben rögzítsd, melyik kontextuselem melyik következő döntést támogatja; a nem indokolható elemeket távolítsd el.
