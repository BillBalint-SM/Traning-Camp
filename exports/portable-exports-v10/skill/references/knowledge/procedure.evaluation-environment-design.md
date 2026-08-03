---
id: procedure.evaluation-environment-design
title: Agent értékelési környezet tervezése
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [evaluation, environment, tasks, tools]
aliases: [evaluation environment design, értékelési környezet tervezés]
relations:
  - type: supports
    target: procedure.agent-evaluation-loop
---

## Lényeg

Az értékelési környezet tartalmazza a kezdeti állapotot, a feladatot, az elérhető eszközöket, a megfigyelhető sikerfeltételt, az idő- és költségkorlátot, valamint a hibák kezelését.

## Miért működik

Az agent teljesítménye csak akkor hasonlítható össze, ha ugyanazt a helyzetet, jogosultságot és ellenőrzési szabályt kapja.

## Mikor alkalmazd

Használd új agent, modell, prompt, eszköz vagy orchestration változtatás előtt és után.

## Mikor ne alkalmazd

Ne tekints véletlenül sikerült demót értékelésnek, ha a kezdeti állapot vagy a siker megítélése nem reprodukálható.

## Döntési szabály

Előbb a valós célállapotot és az ellenőrzését tervezd meg, utána szűkítsd az eszközöket és a feladatot annyira, hogy a hiba oka megkülönböztethető maradjon.

## Hibamódok

Az instabil környezet, a rejtett kézi segítség és a modell által értékelt saját válasz hamis javulást mutathat.

## Kapcsolatok

A feladat-eloszlás lefedettsége erre épül, az observability pedig a futásbeli diagnózist adja hozzá.

## Ellenőrzés

Ismételd meg ugyanazt az értékelést kontrollált állapotból, és igazold, hogy a siker, a költség és a hibakategória összehasonlítható marad.
