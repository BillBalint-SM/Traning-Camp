---
id: decision-guide.agent-model-selection
title: Agent modellválasztás
kind: decision-guide
maturity: reviewed
confidence: high
language: hu
tags: [agent, model-selection, cost, latency, tools]
aliases: [modellválasztás agenthez]
relations:
  - type: depends_on
    target: principle.harness-engineering
---

## Lényeg

Modellt a feladat sikerfeltétele, a kontextus- és eszközszerződés, a késleltetési cél és a teljes futási költség alapján válassz, ne általános rangsor alapján.

## Miért működik

Az agent teljesítménye a modell és a futtatási keret együttműködéséből áll; az erősebb modell nem javítja ki a hiányzó állapotot vagy rossz eszközhívást.

## Mikor alkalmazd

Új feladatkör, szolgáltató, modellverzió vagy költségkeret bevezetésekor használd.

## Mikor ne alkalmazd

Ne cserélj modellt mérés nélkül, ha a hiba valójában eszköz-, prompt-, adat- vagy orchestration-probléma.

## Döntési szabály

Először rögzíts reprezentatív feladatkészletet és minimumküszöböt, majd csak azokat a modelleket hasonlítsd, amelyek a szerződéses kontextust és eszközöket ténylegesen kezelik.

## Hibamódok

A benchmarkhoz optimalizált, de rossz késleltetésű vagy bizonytalan eszközhasználatú modell termelési környezetben gyengébb lehet.

## Kapcsolatok

A harness tervezésétől függ, az értékelési környezet és a metrikaválasztás adja a bizonyítékot.

## Ellenőrzés

Mérd külön a feladatsikert, az eszközhibát, a késleltetést, a token- és külső szolgáltatási költséget, majd dokumentáld a választási küszöböt.
