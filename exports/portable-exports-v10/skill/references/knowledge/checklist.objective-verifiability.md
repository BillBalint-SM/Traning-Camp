---
id: checklist.objective-verifiability
title: Objektív ellenőrizhetőség
kind: checklist
maturity: reviewed
confidence: high
language: hu
tags: [evaluation, verifier, objectivity, tasks]
aliases: [objektív eval verifier]
relations:
  - type: supports
    target: procedure.evaluation-task-specification
---
## Lényeg
A sikerkritérium legyen megfigyelhető, független az agent önbevallásától, stabilan mérhető és a nem kívánt mellékhatásra is érzékeny.
## Miért működik
Az objektív verifier ugyanazt a futást következetesen pontozza és nem jutalmaz puszta meggyőző szöveget.
## Mikor alkalmazd
Feladat és pontozó review-jánál alkalmazd.
## Mikor ne alkalmazd
Ne kényszeríts bináris verifiert valóban szubjektív minőségre; ott kalibrált többdimenziós bírálat kell.
## Döntési szabály
Először állapotból, tesztből vagy adatbázisból mérj; bíró modellt csak a nem formalizálható maradékra használj.
## Hibamódok
A kulcsszó-, formátum- vagy önbevallás-alapú pontozás könnyen kijátszható.
## Kapcsolatok
Az evaluation task specificationt támogatja; az LLM judge kalibráció a szubjektív részt kezeli.
## Ellenőrzés
Készíts tudatosan csaló, részleges és mellékhatásos eredményt, és igazold, hogy a verifier nem ad teljes sikert.
