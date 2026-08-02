---
id: failure-mode.unsafe-tool-expansion
title: Nem biztonságos eszközbővítés
kind: failure-mode
maturity: reviewed
confidence: high
language: hu
tags: [tools, safety, capability, failure-mode]
aliases: [unsafe tool expansion, nem biztonságos eszközbővítés]
relations:
  - type: contrasts_with
    target: decision-guide.tool-granularity
---

## Lényeg

Hiba, ha új eszköz vagy új paraméter úgy kerül az agenthez, hogy nincs hozzá jogosultsági modell, bemenetséma, hibakezelés, auditnyom és visszavonási terv.

## Miért működik

Az új képesség nem csak több funkció: új támadási felületet és új, korábban nem létező mellékhatást is bevezet.

## Mikor alkalmazd

Vizsgáld ezt minden integráció, plugin, MCP-szerver vagy általános végrehajtó hozzáadása előtt.

## Mikor ne alkalmazd

Ne akadályozd a biztonságos, csak olvasási képesség bővítését fölösleges jóváhagyási folyamattal, ha a kockázati elemzés ezt nem indokolja.

## Döntési szabály

Új eszköz csak akkor léphet be az alapértelmezett készletbe, ha a legkisebb szükséges jogosultság, a tesztelt szerződés és az eredményellenőrzés együtt rendelkezésre áll.

## Hibamódok

A rejtett alapértelmezés, a túl széles scope és a nem auditált paraméter hatáskörtúllépéshez vagy későn felismerhető adatvesztéshez vezet.

## Kapcsolatok

Az eszköz-granularitás döntési korlátja, az eszközbiztonsági határ pedig a bevezetés operatív ellenőrzése.

## Ellenőrzés

Új képességhez futtasd végig a tiltott bemenet, a jogosulatlan hívás, a hibás válasz és a részleges siker forgatókönyvét is.
