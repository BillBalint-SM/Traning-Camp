---
id: procedure.agent-evaluation-loop
title: Agent értékelési ciklus
kind: procedure
maturity: validated
confidence: high
language: hu
tags: [evaluation, metrics, regression]
aliases: [agent evaluation loop, agent értékelés]
relations:
  - type: supports
    target: pattern.experience-driven-improvement
  - type: supports
    target: decision-guide.sft-or-rl
---

## Lényeg

Az agent minőségét rögzített feladatsor, világos sikerjel, hibakategória és ismételhető összehasonlítás alapján fejleszd.

## Miért működik

Az értékelési ciklus a benyomást mérhető visszajelzéssé alakítja. Így a prompt, eszköz vagy modell változása összehasonlítható marad.

## Mikor alkalmazd

Használd minden olyan képességnél, amelyet kiadsz, skálázol vagy több megoldás között választasz.

## Mikor ne alkalmazd

Ne vonj le következtetést egyetlen látványos példából vagy olyan mérőszámból, amely nem tükrözi a valódi feladathatást.

## Döntési szabály

Előbb írd le a környezetet és a siker feltételét, csak utána optimalizálj. Ha a hiba nem osztályozható, bővítsd az értékelési megfigyelést.

## Hibamódok

A túl szűk tesztkészlet megtanítja a rendszert a bemutatóra. A kizárólag átlagos pontszám elfedi a biztonsági vagy szélsőérték hibákat.

## Kapcsolatok

Az eljárás az élményalapú fejlesztést és az utótanítási döntést egyaránt támogatja.

## Ellenőrzés

Minden változtatás előtt és után futtasd ugyanazt a rögzített feladatsort, és bontsd a különbséget sikerre, hibára, költségre és időre.
