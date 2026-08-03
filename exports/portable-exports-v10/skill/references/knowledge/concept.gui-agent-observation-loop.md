---
id: concept.gui-agent-observation-loop
title: GUI agent megfigyelési hurka
kind: concept
maturity: reviewed
confidence: medium
language: hu
tags: [gui, observation, action]
aliases: [gui megfigyelés cselekvés]
relations:
  - type: supports
    target: procedure.gui-action-grounding
---

## Lényeg

A GUI agent képernyő- és strukturált állapotot figyel meg, célhoz kötött műveletet választ, végrehajt, majd függetlenül visszaolvassa a változást.

## Miért működik

A zárt hurok megakadályozza, hogy a rendszer a kattintási szándékot sikernek tekintse.

## Mikor alkalmazd

Használd olyan felületen, ahol nincs stabilabb API és a vizuális állapot a szerződés része.

## Mikor ne alkalmazd

Ne válaszd API helyett puszta kényelemből nagy hatású vagy tömeges művelethez.

## Döntési szabály

Minden akciót új megfigyelés és elvárt állapot-invariáns kövessen.

## Hibamódok

Elavult screenshot, animáció, fókuszvesztés és felugró ablak téves koordinátát vagy állapotot okoz.

## Kapcsolatok

A fogalom a GUI-cselekvés földelését zárt végrehajtási körbe helyezi.

## Ellenőrzés

Mérd a művelet utáni állapotegyezést, téves kattintást és helyreállítási arányt.
