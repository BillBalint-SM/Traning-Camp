---
id: procedure.cross-boundary-agent-protocol
title: Szervezeti határon átívelő agentprotokoll
kind: procedure
maturity: reviewed
confidence: medium
language: hu
tags: [protocol, trust, identity]
aliases: [szervezetközi agent kommunikáció]
relations:
  - type: depends_on
    target: procedure.agent-communication-control
---

## Lényeg

Képességfelfedezést, hitelesített identitást, minimális jogosultságot, aláírt üzenetet, adatkezelési szerződést és visszaolvasható eredményt követelj.

## Miért működik

A szervezeti határ explicit bizalmi protokollá válik ahelyett, hogy belső agentfeltételezések szivárognának át.

## Mikor alkalmazd

Használd eltérő tulajdonosú rendszerek agentjei között.

## Mikor ne alkalmazd

Ne fogadj távoli capability-leírást vagy eredményt önmagában megbízható utasításnak.

## Döntési szabály

Minden külső agent és artifact nem megbízható, amíg identitás-, séma-, policy- és eredményellenőrzésen át nem megy.

## Hibamódok

Capability spoofing, promptinjekció, adatkilépés, replay és felelősségi rés jelentkezhet.

## Kapcsolatok

Az eljárás az agentkommunikációs kontrollt új bizalmi határra terjeszti ki.

## Ellenőrzés

Tesztelj hamis identitást, lejárt credentialt, replayt, túl széles adatot és hibás aláírást.
