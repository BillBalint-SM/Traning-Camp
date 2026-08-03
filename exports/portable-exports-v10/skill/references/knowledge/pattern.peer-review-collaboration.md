---
id: pattern.peer-review-collaboration
title: Peer review agentkollaboráció
kind: pattern
maturity: reviewed
confidence: medium
language: hu
tags: [peer-review, independence, iteration]
aliases: [agentek kölcsönös ellenőrzése]
relations:
  - type: supports
    target: procedure.ablation-and-experiment-loop
---

## Lényeg

Két vagy több agent előbb független jelöltet készít, majd bizonyítékalapú kritikával és explicit feloldási szabállyal iterál.

## Miért működik

A független első kör növeli a megoldási sokféleséget, a kritika pedig feltárhatja az egyedi vakfoltokat.

## Mikor alkalmazd

Használd bizonytalan, több jó megoldású vagy nagy review-értékű feladatnál.

## Mikor ne alkalmazd

Ne futtass végtelen vitát objektív verifier vagy döntési felelős nélkül.

## Döntési szabály

Előbb vak jelölt, utána kritika; konszenzus helyett előre rögzített mérőjel vagy tulajdonos döntsön.

## Hibamódok

Kölcsönös lehorgonyzás, udvarias egyetértés és ciklikus javítgatás költséget növelhet nyereség nélkül.

## Kapcsolatok

A minta az összehasonlító kísérleti hurkot használja jelöltválasztásra.

## Ellenőrzés

Mérd a vak jelöltek sokféleségét, kritikák találati arányát és a review nélküli baseline-t.
