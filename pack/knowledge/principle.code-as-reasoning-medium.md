---
id: principle.code-as-reasoning-medium
title: A kód mint gondolkodási közeg
kind: principle
maturity: reviewed
confidence: high
language: hu
tags: [code, reasoning, computation, verification]
aliases: [kóddal végzett gondolkodás]
relations:
  - type: supports
    target: principle.code-as-meta-capability
---

## Lényeg

Használj kódot számítás, állapotkövetés, keresés és ellenőrzés külső munkafelületeként, amikor a puszta nyelvi következtetés nehezen auditálható.

## Miért működik

A program explicit lépésekre bontja a problémát, ismételhető eredményt ad és tesztelhetővé teszi a köztes feltételezéseket.

## Mikor alkalmazd

Nagy adathalmaz, kombinatorikus döntés, pontos számítás vagy komplex transzformáció esetén alkalmazd.

## Mikor ne alkalmazd

Ne helyettesíts vele nem formalizálható értékítéletet vagy hiányzó üzleti döntést.

## Döntési szabály

Ha a következtetés ellenőrizhető algoritmusra és bemenetre bontható, futtasd kódként és őrizd meg az eredmény bizonyítékát.

## Hibamódok

A helytelen formalizálás pontosan ismétli a rossz feltevést, ezért a kód futása önmagában nem bizonyít helyes modellt.

## Kapcsolatok

A kód metaképességét támogatja; az executable business rules a korlátozó alkalmazása.

## Ellenőrzés

Kézi mintán, független számítással vagy invariánssal ellenőrizd a formalizálást és a program eredményét.
