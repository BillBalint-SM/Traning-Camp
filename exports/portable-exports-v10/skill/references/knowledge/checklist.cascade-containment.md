---
id: checklist.cascade-containment
title: Agenthiba-kaszkád megfékezése
kind: checklist
maturity: reviewed
confidence: medium
language: hu
tags: [cascade, containment, verification]
aliases: [hibák kaszkádos felerősödését agentek között]
relations:
  - type: supports
    target: failure-mode.multi-agent-error-amplification
---

## Lényeg

Legyen bizalmi címke, független verifier, terjedési limit, circuit breaker, budget, jogosultsági szűkítés, korrelációs trace és emberi eszkaláció.

## Miért működik

A hibás kimenet nem válik automatikusan magasabb bizalmú bemenetté minden új agentlépéssel.

## Mikor alkalmazd

Futtasd minden több-agent pipeline és külső műveletet végző kollaboráció előtt.

## Mikor ne alkalmazd

Ne tekintsd az agentek egyetértését független bizonyítéknak, ha ugyanazt a kontextust és modellt használják.

## Döntési szabály

Minden bizalmi vagy hatásnövelő átadás előtt új, független ellenőrzés szükséges.

## Hibamódok

Közös torzítás, hamis konszenzus, retry-vihar és egyre szélesebb jogosultság gyorsan felerősíti a hibát.

## Kapcsolatok

A lista közvetlen containmentet ad a multi-agent hibafelerősítéshez.

## Ellenőrzés

Injektálj korai hibát, és bizonyítsd, hogy a rendszer korlátozott lépésszámon és hatáson belül leáll.
