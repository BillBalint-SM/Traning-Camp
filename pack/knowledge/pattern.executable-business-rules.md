---
id: pattern.executable-business-rules
title: Végrehajtható üzleti szabályok
kind: pattern
maturity: reviewed
confidence: high
language: hu
tags: [code, business-rules, validation, policy]
aliases: [üzleti szabály kódban]
relations:
  - type: supports
    target: procedure.business-rule-compilation
---

## Lényeg

A kritikus, eldönthető üzleti szabályt kódolt validációként érvényesítsd, miközben a modell a szükséges adatok felismerését és a magyarázatot végzi.

## Miért működik

A determinisztikus ellenőrzés minden futásban ugyanazt a határt tartja, és független tesztekkel bizonyítható.

## Mikor alkalmazd

Jogosultság, limit, állapotátmenet, számítás vagy tiltott kombináció esetén alkalmazd.

## Mikor ne alkalmazd

Ne kódolj mereven bizonytalan, kontextuális vagy gyakran változó döntést megfelelő tulajdonos és verziózás nélkül.

## Döntési szabály

A modell állítson elő strukturált jelöltet, a kód validáljon és csak siker után engedjen hatást.

## Hibamódok

A promptban maradt kritikus szabály ingadozhat, a kódban rejtett üzleti döntés pedig review nélkül elavulhat.

## Kapcsolatok

Az üzleti szabály fordítását támogatja, a tool szerződés a végrehajtási határt adja.

## Ellenőrzés

Táblázatos pozitív, negatív, hiányzó és határértékes tesztekkel bizonyítsd a szabályt.
