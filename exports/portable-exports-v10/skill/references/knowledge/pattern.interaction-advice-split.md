---
id: pattern.interaction-advice-split
title: Interakciós és tanácsadó ág szétválasztása
kind: pattern
maturity: reviewed
confidence: medium
language: hu
tags: [interaction, advice, dual-process]
aliases: [gyors interakció lassú tanács]
relations:
  - type: supports
    target: decision-guide.reasoning-expression-coupling
---

## Lényeg

A gyors ág kezeli a fordulót, tisztázást és érzelmi visszajelzést, a lassú ág pedig a tényszerű tanácsot és eszközhasználatot.

## Miért működik

Az eltérő célok külön modellezhetők, miközben egy explicit állapotinterfész összeköti őket.

## Mikor alkalmazd

Használd hosszabb elemzést igénylő, de folyamatos jelenlétet kívánó beszélgetésben.

## Mikor ne alkalmazd

Ne engedd a gyors ágnak a lassú ág jóváhagyását igénylő tény vagy művelet kimondását.

## Döntési szabály

A gyors ág csak interakciós szándékot, a lassú ág pedig ellenőrzött tartalmi állapotot írhat.

## Hibamódok

Eltérő személyiség, állapotverseny és egymást felülíró válasz zavaros felhasználói élményt okoz.

## Kapcsolatok

A minta a gondolkodás–kifejezés coupling egyik szerepalapú megoldása.

## Ellenőrzés

Teszteld az állapotátadást, ellentmondást, időtúllépést és azt, hogy csak egy ág ad végső tanácsot.
