---
id: principle.planning-control-separation
title: Tervezés és vezérlés szétválasztása
kind: principle
maturity: reviewed
confidence: high
language: hu
tags: [planning, control, robotics, gui, safety]
aliases: [planning control separation, tervezés vezérlés határ]
relations:
  - type: supports
    target: procedure.gui-action-grounding
---

## Lényeg

A magas szintű tervező a célt, a sorrendet és a korlátot választja; az alacsony szintű vezérlő a helyi érzékeléshez igazítja a pontos mozdulatot vagy felületi műveletet.

## Miért működik

Az időtávok és hibák különböznek: a tervhez globális összefüggés kell, a végrehajtáshoz friss, nagy frekvenciájú visszajelzés.

## Mikor alkalmazd

Használd GUI-automatizálásnál, robotikus végrehajtásnál és minden olyan feladatnál, ahol a környezet a terv készítése és a művelet között változhat.

## Mikor ne alkalmazd

Ne építs külön tervezőt és vezérlőt egyetlen, változatlan állapotú, biztonságos eszközhívás köré.

## Döntési szabály

A tervező ne adjon végleges koordinátát vagy képernyőpozíciót, a vezérlő pedig ne írja felül a célt vagy a jogosultsági korlátot.

## Hibamódok

Az összemosott réteg lassú, törékeny és nehezen diagnosztizálható, mert nem derül ki, hogy a rossz cél vagy a rossz végrehajtás okozta a hibát.

## Kapcsolatok

A GUI-grounding és az eseményvezérelt futás is ezt a felelősségi határt használja.

## Ellenőrzés

Változtasd meg a helyi elrendezést a cél megtartása mellett, és igazold, hogy a vezérlő újraigazít, miközben a terv és a jogosultság változatlan marad.
