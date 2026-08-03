---
id: decision-guide.sft-or-rl
title: Felügyelt tanítás vagy megerősítéses optimalizálás
kind: decision-guide
maturity: reviewed
confidence: medium
language: hu
tags: [post-training, sft, rl]
aliases: [sft or rl, felügyelt vagy megerősítéses tanítás]
relations:
  - type: depends_on
    target: procedure.agent-evaluation-loop
---

## Lényeg

Felügyelt tanítást válassz, ha jó bemenet–kimenet példák világosan megadhatók; megerősítéses optimalizálást akkor, ha a siker több lépés eredménye és értékelő jelből mérhető.

## Miért működik

A két módszer másfajta visszajelzést hasznosít. A példa gyorsan tanít formát és mintát, a jutalom pedig összetett célok között képes irányt adni.

## Mikor alkalmazd

Használd képességfejlesztési döntés előtt, amikor már van megbízható értékelési környezet és ismert célviselkedés.

## Mikor ne alkalmazd

Ne kezdd megerősítéses optimalizálással, ha nincs stabil mérőjel vagy a környezet nem védi ki a kihasználható kiskapukat.

## Döntési szabály

Ha egy szakértő rövid, helyes példával egyértelműen demonstrálja a kívánt viselkedést, kezdd felügyelt tanítással; ha a minőség csak futtatott eredményből látszik, vizsgáld a jutalom-alapú utat.

## Hibamódok

A rossz jutalom hamis optimalizálást eredményez. A mintákból hiányzó kivételek pedig túl magabiztos, de szűk viselkedést alakítanak ki.

## Kapcsolatok

Az útmutató az értékelési ciklusra épül, mert a módszerválasztást megbízható mérésnek kell megelőznie.

## Ellenőrzés

Készíts ellenpéldákat és váratlan helyzeteket is tartalmazó értékelést; csak akkor fogadd el a javulást, ha ott sem romlik a biztonság vagy a következetesség.
