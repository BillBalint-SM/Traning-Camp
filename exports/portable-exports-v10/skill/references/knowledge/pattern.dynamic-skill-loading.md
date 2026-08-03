---
id: pattern.dynamic-skill-loading
title: Dinamikus skill-betöltés
kind: pattern
maturity: reviewed
confidence: high
language: hu
tags: [skills, context-engineering, capability, routing]
aliases: [dinamikus skill betöltés, igény szerinti képességbetöltés]
relations:
  - type: supports
    target: procedure.system-prompt-architecture
---

## Lényeg

A ritkán szükséges domainutasításokat és eljárásokat kis, kereshető skill-egységekben tartsd, és csak a feladat releváns pontján töltsd be őket.

## Miért működik

Így a modell kontextusa rövid marad, miközben a részletes szakmai eljárás akkor jelenik meg, amikor ténylegesen befolyásolja a döntést.

## Mikor alkalmazd

Használd több domainnel, sok eszközzel vagy változó üzleti folyamattal dolgozó agentnél.

## Mikor ne alkalmazd

Ne bonts szét olyan rövid, mindig szükséges alapelveket, amelyek betöltési késleltetése vagy elvesztése nagyobb kárt okozna, mint a megtakarított kontextus.

## Döntési szabály

Egy skill akkor legyen dinamikus, ha önálló aktiváló jel, világos cél, szűk bemenet és ellenőrizhető kimenet tartozik hozzá.

## Hibamódok

A homályos név, az átfedő alias és a túl nagy skill-egység rossz betöltést vagy felesleges kontextusnövekedést okoz.

## Kapcsolatok

A kontextus-gyorsítótár és a tudásrouting együtt határozza meg a betöltés helyét és költségét.

## Ellenőrzés

Mérd, hogy a skill nélküli, a releváns skillt betöltő és a túl sok skillt betöltő futás közül melyik ad helyes, rövid és stabil eredményt.
