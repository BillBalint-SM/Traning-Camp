---
id: pattern.multi-agent-context-boundaries
title: Több-agent kontextushatárok
kind: pattern
maturity: reviewed
confidence: medium
language: hu
tags: [multi-agent, context, collaboration]
aliases: [multi agent context boundaries, több agent határai]
relations:
  - type: depends_on
    target: principle.context-is-finite
  - type: supports
    target: failure-mode.unvalidated-autonomy
---

## Lényeg

Több agent között ne teljes beszélgetéseket, hanem célhoz kötött munkaszerződést és minimális állapotot adj át.

## Miért működik

Az elkülönített kontextus csökkenti a szerepzavart és a véletlen utasításátvitelt. Az együttműködés így közös célhoz, nem közös zajhoz kötődik.

## Mikor alkalmazd

Alkalmazd, amikor párhuzamos kutatás, külön jogosultság, független ellenőrzés vagy specializált szerepek indokoltak.

## Mikor ne alkalmazd

Ne bonts szét olyan rövid, egységes feladatot, ahol az átadási költség nagyobb, mint a specializáció nyeresége.

## Döntési szabály

Minden agent átadásában legyen cél, bemenet, tilalom, elvárt eredményformátum és felelős döntési határ; minden más maradjon helyi.

## Hibamódok

A teljes kontextus megosztása elrejti a felelőst. A közös, írási konfliktus nélküli állapot hiánya pedig egymásnak ellentmondó végrehajtást okozhat.

## Kapcsolatok

A minta a véges kontextusra épül, és az ellenőrizetlen önállóság elleni kontrollt erősíti.

## Ellenőrzés

Egy átadás akkor jó, ha a fogadó agent csak abból képes megmondani, mit tehet, mit nem tehet, és milyen eredményt kell visszaadnia.
