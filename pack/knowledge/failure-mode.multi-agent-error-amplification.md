---
id: failure-mode.multi-agent-error-amplification
title: Több-agent hibaamplifikáció
kind: failure-mode
maturity: reviewed
confidence: high
language: hu
tags: [multi-agent, failure-mode, coordination, propagation]
aliases: [multi agent error amplification, több agent hibasokszorozás]
relations:
  - type: contrasts_with
    target: decision-guide.multi-agent-topology-selection
---

## Lényeg

Egy kis kezdeti hiba több agent között felerősödik, ha az átadott állítás bizonyíték nélkül tényként terjed, a szereplők ugyanarra a rossz feltételezésre építenek, vagy a javítás is automatikusan továbbterjed.

## Miért működik

A párhuzamosság a helyes munka mellett a hibát is gyorsítja; a sok független döntés nem jelent független bizonyítékot.

## Mikor alkalmazd

Vizsgáld ezt a hibamódot sokagent-architektúránál, manager mintánál, peer review-nál és közös állapotú munkafolyamatnál.

## Mikor ne alkalmazd

Ne feltételezd automatikusan, hogy a több agent veszélyesebb; jól kialakított független ellenőrzés éppen hogy csökkentheti az egyetlen agent hibáját.

## Döntési szabály

Minden kritikus átadásnál jelöld, mi bizonyított, mi feltételezés, ki ellenőrizte, és melyik agent jogosult a globális állapot módosítására.

## Hibamódok

A közös memória kritikátlan másolása, a ciklikus visszajelzés és a hibás eredmény automatikus újrafelhasználása gyorsan terjeszti a kezdeti tévedést.

## Kapcsolatok

A topológia választása adja a szerkezeti ellensúlyt, a konkurenciakezelés és az átadási szerződés pedig a gyakorlati védelmet.

## Ellenőrzés

Ültess szándékosan hibás, de hihető állítást egy ágba, és mérd, hogy a rendszer felismeri, izolálja és megállítja-e, mielőtt más ágakra vagy külső műveletre jut.
