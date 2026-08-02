---
id: pattern.peer-to-peer-handoff
title: Peer-to-peer agentátadás
kind: pattern
maturity: reviewed
confidence: medium
language: hu
tags: [peer-to-peer, handoff, decentralization]
aliases: [decentralizált peer handoff]
relations:
  - type: depends_on
    target: procedure.multi-agent-handoff-contract
---

## Lényeg

Az aktuális agent a feladatállapot és képességigény alapján közvetlenül választ következő felelőst, központi manager nélkül.

## Miért működik

Csökkenti a központi szűk keresztmetszetet és helyi döntéssel skálázhatja a munkafolyamatot.

## Mikor alkalmazd

Használd stabil képességregiszterrel és jól típusos handoffokkal rendelkező hálózatban.

## Mikor ne alkalmazd

Ne használd globális prioritás, szigorú audit vagy erős tranzakciós koordináció nélkül.

## Döntési szabály

Minden átadás előtt ellenőrizd a fogadó képességét, jogosultságát, terhelését és elfogadási válaszát.

## Hibamódok

Körkörös delegálás, gazdátlan feladat, duplikált tulajdon és jogosultsági sodródás jelentkezhet.

## Kapcsolatok

A minta az explicit handoff-szerződés decentralizált alkalmazása.

## Ellenőrzés

Tesztelj ciklust, fogadó elutasítást, timeoutot, kapacitáshiányt és terminális felelőst.
