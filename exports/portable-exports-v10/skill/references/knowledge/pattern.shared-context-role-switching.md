---
id: pattern.shared-context-role-switching
title: Szerepváltás közös kontextusban
kind: pattern
maturity: reviewed
confidence: medium
language: hu
tags: [shared-context, roles, state]
aliases: [közös kontextusú szerepváltás]
relations:
  - type: depends_on
    target: decision-guide.shared-or-isolated-context
---

## Lényeg

Egy közös kanonikus állapot fölött külön szereppromptok vagy agentlépések váltják egymást, minden váltásnál explicit cél- és felelősségjelöléssel.

## Miért működik

Elkerüli a teljes kontextus újraküldését, miközben külön nézőpontokat és munkafázisokat ad.

## Mikor alkalmazd

Használd szorosan egymásra épülő, lineáris munkafolyamatban.

## Mikor ne alkalmazd

Ne használd független véleményhez, ha a korábbi szerep gondolatai lehorgonyozzák a következőt.

## Döntési szabály

Szerepváltáskor csak a kanonikus tényállapot maradjon, az előző szerep nem igazolt következtetése ne váljon automatikus ténnyé.

## Hibamódok

Szerepösszemosódás, kontextusduzzadás és korai hipotézis öröklése csökkenti a sokféleséget.

## Kapcsolatok

A minta a megosztott kontextus választására épül.

## Ellenőrzés

Teszteld a szerephatárt, a kanonikus állapot diffjét és vak újraértékelést izolált kontrollal.
