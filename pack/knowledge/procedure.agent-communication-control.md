---
id: procedure.agent-communication-control
title: Agentkommunikáció és vezérlés
kind: procedure
maturity: reviewed
confidence: medium
language: hu
tags: [communication, control, protocol]
aliases: [agentek közti kommunikáció vezérlés]
relations:
  - type: supports
    target: procedure.multi-agent-handoff-contract
---

## Lényeg

Az üzenet tartalmazzon feladattípust, korrelációs azonosítót, verziót, határidőt, jogosultságot, várt választ és idempotenciakulcsot.

## Miért működik

A vezérlési metaadat különválasztja a tartalmat a futáskoordinációtól és lehetővé teszi az újrapróbálást.

## Mikor alkalmazd

Használd aszinkron, izolált vagy több gépen futó agentek között.

## Mikor ne alkalmazd

Ne bízz szabad szöveges „kész” üzenetben állapot-visszaolvasás nélkül.

## Döntési szabály

Minden állapotmódosító kérés legyen hitelesített, idempotens vagy explicit egyszeri, és legyen terminális válasza.

## Hibamódok

Duplikált üzenet, sorrendcsere, elveszett válasz és jogosulatlan feladó hibás végrehajtást okoz.

## Kapcsolatok

Az eljárás a handoff-szerződés kommunikációs transportját részletezi.

## Ellenőrzés

Tesztelj késést, duplikációt, kiesést, újraindítást, lejárt jogosultságot és idempotens visszajátszást.
