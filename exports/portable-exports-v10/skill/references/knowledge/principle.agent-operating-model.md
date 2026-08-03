---
id: principle.agent-operating-model
title: Agent működési modell
kind: principle
maturity: validated
confidence: high
language: hu
tags: [agent, context, tools]
aliases: [agent operating model, ügynök működési modell]
relations:
  - type: supports
    target: principle.context-is-finite
---

## Lényeg

Egy hasznos agent nem pusztán nyelvi modell: az eredményét a modell, az aktuális kontextus és a végrehajtható eszközök együttese adja.

## Miért működik

A modell az értelmezést végzi, a kontextus kijelöli a helyzetet, az eszköz pedig megfigyelést vagy változtatást tesz lehetővé. E három elem szerződése megszünteti a homályos felelősségi határokat.

## Mikor alkalmazd

Használd minden olyan feladatnál, ahol a válaszon túl ellenőrzésre, adatra vagy külső műveletre is szükség van.

## Mikor ne alkalmazd

Ne építs teljes agent hurkot egyszerű, egyértelmű szövegátalakításra vagy olyan feladatra, amelyhez nincs biztonságos eszközművelet.

## Döntési szabály

Először nevezd meg, mit kell az agentnek tudnia, mit kell látnia, és mit módosíthat; ha bármelyik kérdésre nincs szerződéses válasz, szűkítsd a feladatot.

## Hibamódok

A gyakori hiba az, hogy a modellre bíznak állapotkezelést vagy jogosultsági döntést. Ettől a rendszer magabiztosnak látszhat, miközben nem visszakövethető.

## Kapcsolatok

Az elv a véges kontextus felismerését támogatja, és alapot ad az eszköz- illetve memória-tervezéshez.

## Ellenőrzés

Egy feladatleírás akkor teljes, ha külön felsorolja a szükséges kontextust, az engedélyezett eszközöket és a siker megfigyelhető feltételét.
