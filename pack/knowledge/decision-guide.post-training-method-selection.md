---
id: decision-guide.post-training-method-selection
title: Utótanítási módszer kiválasztása
kind: decision-guide
maturity: reviewed
confidence: medium
language: hu
tags: [post-training, selection, evidence]
aliases: [utótanítási módszerválasztás]
relations:
  - type: supports
    target: decision-guide.sft-or-rl
---

## Lényeg

A módszert a rendelkezésre álló tanulási jel, a feladat időhorizontja, a környezet ellenőrizhetősége és a kockázati keret alapján válaszd.

## Miért működik

A döntés így a tényleges bizonyítékhoz igazodik, nem az algoritmus divatjához vagy névleges képességéhez.

## Mikor alkalmazd

Használd minden súlymódosító kezdeményezés tervezési kapujaként.

## Mikor ne alkalmazd

Ne indíts utótanítást, ha a hiba a harnessben, a tudásfrissességben, az eszközszerződésben vagy a kontextusban javítható.

## Döntési szabály

Demonstrációhoz SFT-t, összehasonlító preferenciához preferenciatanulást, végrehajtható célhoz RL-t válassz; bizonytalan mérőjelnél előbb az értékelést javítsd.

## Hibamódok

Az eszköz nélküli módszerválasztás drága tréninget, mérhetetlen eredményt és visszafordíthatatlan regressziót okozhat.

## Kapcsolatok

Az útmutató az SFT–RL alapszétválasztást részletezi.

## Ellenőrzés

Készíts döntési jegyzőkönyvet az alternatívákról, költségről, mérőjelről, rollbackről és leállítási kritériumról.
