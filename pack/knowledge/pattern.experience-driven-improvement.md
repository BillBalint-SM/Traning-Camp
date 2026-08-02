---
id: pattern.experience-driven-improvement
title: Tapasztalatból vezérelt fejlesztés
kind: pattern
maturity: validated
confidence: high
language: hu
tags: [improvement, feedback, learning]
aliases: [experience driven improvement, tapasztalat alapú fejlesztés]
relations:
  - type: depends_on
    target: procedure.agent-evaluation-loop
---

## Lényeg

Az agent futásaiból csak strukturált tapasztalatot emelj ki: helyzet, döntés, eszközeredmény, hiba, javítási jelölt és utólagos mérés.

## Miért működik

A strukturált tapasztalat visszakereshető és összehasonlítható. Ez megakadályozza, hogy egyetlen hangos hiba aránytalanul átírja a rendszer működését.

## Mikor alkalmazd

Alkalmazd ismétlődő feladatoknál, ahol valódi futásokból érkezik elég jel a folyamat, prompt vagy eszközszerződés javításához.

## Mikor ne alkalmazd

Ne kezeld automatikus igazságként a nyers futási naplót, különösen akkor, ha nincs ellenőrzött sikerjel vagy az input bizalmas.

## Döntési szabály

Csak olyan tapasztalatot emelj be fejlesztési jelöltnek, amelyhez mérhető eredmény és visszaellenőrizhető hibakategória kapcsolódik.

## Hibamódok

A szelektív naplózás megerősíti a meglévő torzításokat. A közvetlen automatikus promóció regressziót és szivárgást okozhat.

## Kapcsolatok

A minta az értékelési ciklusra épül, mert a tanulságot mindig a mért eredmény hitelesíti.

## Ellenőrzés

Minden bevezetett tanulsághoz őrizd meg a mérési esetet, és futtasd újra a korábbi regressziós készletet.
