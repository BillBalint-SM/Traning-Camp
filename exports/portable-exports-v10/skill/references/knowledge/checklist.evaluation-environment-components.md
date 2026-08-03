---
id: checklist.evaluation-environment-components
title: Értékelési környezet komponensei
kind: checklist
maturity: reviewed
confidence: high
language: hu
tags: [evaluation, environment, verifier, reset]
aliases: [eval környezet komponenslista]
relations:
  - type: supports
    target: procedure.evaluation-environment-design
---
## Lényeg
Az értékelési környezet tartalmazzon inicializálást, feladatbemenetet, engedélyezett műveleteket, megfigyelést, állapot-resetet, verifiert és futási naplót.
## Miért működik
Ezek együtt választják el a rendszer képességét a tesztkörnyezet véletlen állapotától.
## Mikor alkalmazd
Új benchmark vagy belső eval harness tervezésekor alkalmazd.
## Mikor ne alkalmazd
Ne tekintsd teljesnek a környezetet pusztán azért, mert egy végső szöveges választ pontozni tud.
## Döntési szabály
Minden feladathoz legyen ismert kezdőállapot, megengedett hatás, objektív végállapot és reprodukálható reset.
## Hibamódok
A szivárgó állapot, nem determinisztikus fixture vagy hiányzó verifier torz eredményt ad.
## Kapcsolatok
Az evaluation environment designot támogatja; a tool- és HCI-környezet szakosítja.
## Ellenőrzés
Futtass ugyanazon feladaton reset–run–verify ciklust többször, és hasonlítsd az induló és végállapotot.
