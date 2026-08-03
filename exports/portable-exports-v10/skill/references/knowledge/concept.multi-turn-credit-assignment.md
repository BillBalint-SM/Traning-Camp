---
id: concept.multi-turn-credit-assignment
title: Többlépéses kredit-hozzárendelés
kind: concept
maturity: reviewed
confidence: medium
language: hu
tags: [multi-turn, credit, reward]
aliases: [kredit hozzárendelés több lépéshez]
relations:
  - type: supports
    target: procedure.agent-evaluation-loop
---

## Lényeg

A kredit-hozzárendelés azt dönti el, hogy egy későbbi siker vagy kudarc jelét mely korábbi döntésekhez és milyen erősséggel rendeljük.

## Miért működik

A különválasztás segít megtanulni a hosszú távon hasznos előkészítő lépéseket anélkül, hogy minden köztes műveletet azonosan jutalmazna.

## Mikor alkalmazd

Használd hosszú eszközláncoknál, keresési stratégiánál és késleltetett üzleti eredménynél.

## Mikor ne alkalmazd

Ne vezess be összetett kreditmodellt, ha minden lépés közvetlenül és objektíven ellenőrizhető.

## Döntési szabály

A legritkább összesített jel mellé csak olyan köztes jelet adj, amely bizonyítottan korrelál a valódi végcéllal és nem írja felül azt.

## Hibamódok

Túl sűrű proxyjutalom rövidlátó viselkedést, túl ritka végjutalom nagy varianciát és lassú tanulást okoz.

## Kapcsolatok

A fogalom az agentértékelés lépés- és eredményszintű mérését támogatja.

## Ellenőrzés

Ablációval mérd, hogy minden köztes jel valóban javítja-e a holdout végsikert és nem csak a proxyértéket.
