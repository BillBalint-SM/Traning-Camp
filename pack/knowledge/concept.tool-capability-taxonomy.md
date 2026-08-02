---
id: concept.tool-capability-taxonomy
title: Eszközképességek osztályozása
kind: concept
maturity: reviewed
confidence: high
language: hu
tags: [tools, capability, perception, execution, collaboration]
aliases: [tool capability taxonomy, eszközképesség osztályozás]
relations:
  - type: supports
    target: procedure.tool-contract-design
---

## Lényeg

Az agent eszközeit különítsd el megfigyelő, végrehajtó és együttműködési képességekre; mindegyikhez más jogosultság, bizonyíték és hibakezelés tartozik.

## Miért működik

Az osztályozás megakadályozza, hogy egy adatlekérdezés, egy állapotmódosítás és egy külső üzenet ugyanazzal a kockázati szabállyal fusson.

## Mikor alkalmazd

Használd új eszközkatalógus, MCP-szerver, integráció vagy autonóm munkafolyamat tervezésekor.

## Mikor ne alkalmazd

Ne kategorizálj pusztán név alapján; az eszköz tényleges mellékhatása és az általa kezelt adat határozza meg a csoportját.

## Döntési szabály

Ha egy művelet megváltoztatja a külső világot, végrehajtóként kezeld akkor is, ha a válasza csak rövid szövegnek látszik.

## Hibamódok

A csak olvasásnak címkézett, de rejtett módosítást végző eszköz jogosultsági hibát, a túl általános kategória pedig rossz auditnyomot okoz.

## Kapcsolatok

Az eszköz-granularitás erre épül, az eszközszerződés pedig a kategória konkrét korlátait rögzíti.

## Ellenőrzés

Minden eszközhöz dokumentáld a bemenetet, a külső hatást, a visszafordíthatóságot, a szükséges jóváhagyást és az eredmény ellenőrzését.
