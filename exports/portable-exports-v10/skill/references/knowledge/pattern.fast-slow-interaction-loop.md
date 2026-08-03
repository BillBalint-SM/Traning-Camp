---
id: pattern.fast-slow-interaction-loop
title: Gyors–lassú interakciós hurok
kind: pattern
maturity: reviewed
confidence: high
language: hu
tags: [interaction, realtime, latency, voice]
aliases: [fast slow interaction loop, gyors lassú interakció]
relations:
  - type: supports
    target: decision-guide.voice-architecture-selection
---

## Lényeg

Válaszd szét a gyors kapcsolatfenntartó reakciót és a lassabb, nagyobb bizonyosságot igénylő döntést; a gyors réteg soha ne ígérjen vagy hajtson végre olyat, amit a lassú réteg még nem validált.

## Miért működik

Az interakció folytonos marad, miközben az összetett válaszhoz, eszközhíváshoz vagy kockázatos döntéshez továbbra is elegendő idő és ellenőrzés jut.

## Mikor alkalmazd

Használd valós idejű hang- vagy GUI-interakciónál, ahol a felhasználó gyors visszajelzést vár, de a tartalmi válasz bonyolult lehet.

## Mikor ne alkalmazd

Ne hozz létre két döntéshozó réteget egyszerű, azonnal ellenőrizhető kérdés-válasznál, ha ez csak további inkonzisztenciát okozna.

## Döntési szabály

A gyors réteg csak állapotot jelezhet, pontosíthat vagy biztonságos várakozást kommunikálhat; minden külső hatású vagy tartalmi következtetés a lassú réteghez tartozik.

## Hibamódok

A gyors réteg túlzott magabiztossága és a két réteg eltérő állapotképe félrevezető ígéretet vagy ismételt műveletet okozhat.

## Kapcsolatok

A hangarchitektúra választását támogatja, és a státuszmegjelenítéssel közös futási képet igényel.

## Ellenőrzés

Szimulálj lassú háttérdöntést és felhasználói megszakítást, majd igazold, hogy a gyors visszajelzés nem mond ellent a végső, validált eredménynek.
