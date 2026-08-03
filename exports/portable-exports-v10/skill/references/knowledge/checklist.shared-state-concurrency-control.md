---
id: checklist.shared-state-concurrency-control
title: Közös állapot konkurenciakezelési ellenőrzőlista
kind: checklist
maturity: reviewed
confidence: high
language: hu
tags: [multi-agent, concurrency, state, coordination]
aliases: [shared state concurrency control, közös állapot zárolás]
relations:
  - type: prevents
    target: failure-mode.multi-agent-error-amplification
---

## Lényeg

Közös fájl, adatbázis vagy feladatlista módosítása előtt tisztázd a tulajdonost, a zárolást vagy verziót, az idempotenciát, az ütközésfeloldást és az utólagos visszaolvasást.

## Miért működik

Párhuzamos agentek ugyanazt a valóságot módosíthatják eltérő feltételezésből; a konkurenciakezelés teszi az átadást és a végrehajtást összeegyeztethetővé.

## Mikor alkalmazd

Használd minden megosztott munkaelem, fájl, konfiguráció, készlet vagy külső tranzakció esetén.

## Mikor ne alkalmazd

Ne vezess be globális zárolást teljesen független, csak olvasási vagy külön névtérben futó feladatra.

## Döntési szabály

Ha két agent ugyanazt az erőforrást módosíthatja, legyen egyértelmű sorosítás, optimista verzióellenőrzés vagy tulajdonosi felosztás.

## Hibamódok

Az utolsó író győz alapértelmezés, a nem idempotens újrapróbálás és a tulajdonos nélküli konfliktus csendes adatvesztést vagy hibasokszorozást okoz.

## Kapcsolatok

Az átadási szerződéshez tartozik, és közvetlenül csökkenti a több-agent hibaamplifikáció esélyét.

## Ellenőrzés

Futtass ugyanarra az erőforrásra párhuzamos, késleltetett és újrapróbált műveletet, majd igazold, hogy a végállapot és az auditnyom determinisztikus.
