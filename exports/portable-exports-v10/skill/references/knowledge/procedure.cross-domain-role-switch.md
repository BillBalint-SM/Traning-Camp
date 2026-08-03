---
id: procedure.cross-domain-role-switch
title: Szakterületek közötti szerepváltás
kind: procedure
maturity: reviewed
confidence: medium
language: hu
tags: [roles, domain, translation]
aliases: [szakterületek közti agent átadás]
relations:
  - type: depends_on
    target: procedure.multi-agent-handoff-contract
---

## Lényeg

A domainváltásnál közös fogalomtárat, bizonyítéklistát, feltételezéseket, nyitott kérdéseket és a fogadó szerep döntési határát add át.

## Miért működik

A strukturált fordítás csökkenti, hogy ugyanaz a szó eltérő jelentéssel vagy a következtetés tényként kerüljön tovább.

## Mikor alkalmazd

Használd például jogi, műszaki, üzleti és biztonsági szerepek egymásra épülő munkájánál.

## Mikor ne alkalmazd

Ne engedd a küldő szerepnek a fogadó domain szakmai döntését előre lezárni.

## Döntési szabály

Állítás, bizonyíték, feltételezés és ajánlás külön mezőben menjen át.

## Hibamódok

Terminológiai sodródás, hatáskörtúllépés és elveszett bizonytalanság hibás integrációt okoz.

## Kapcsolatok

Az eljárás az általános agent-handoff szerződésre épül.

## Ellenőrzés

A fogadó szerep olvassa vissza saját szavaival a célt, határt és bizonytalanságot a munka előtt.
