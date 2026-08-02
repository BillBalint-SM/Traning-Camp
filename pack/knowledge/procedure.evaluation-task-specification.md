---
id: procedure.evaluation-task-specification
title: Értékelési feladat specifikálása
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [evaluation, tasks, specification, verifier]
aliases: [eval feladatleírás]
relations:
  - type: supports
    target: procedure.evaluation-environment-design
---
## Lényeg
A feladatleírás rögzítse a célt, kezdőállapotot, megengedett és tiltott hatást, sikerfeltételt, idő- és költségkeretet, valamint a verifier nézőpontját.
## Miért működik
Az agent és a pontozó ugyanazt az eredményt célozza, miközben a megoldási út nem lesz indokolatlanul előírva.
## Mikor alkalmazd
Minden új eval eset vagy benchmark-feladat létrehozásakor alkalmazd.
## Mikor ne alkalmazd
Ne írj megoldási receptet, ha a cél az általános problémamegoldó képesség mérése.
## Döntési szabály
A feladat legyen egyértelmű a célban, nyitott a legitim stratégiában és objektív a végállapotban.
## Hibamódok
A homályos cél, rejtett feltétel vagy túl részletes recept más képességet mér, mint amit állít.
## Kapcsolatok
Az evaluation environment designot támogatja; az objektív verifiability ellenőrzőlista vizsgálja.
## Ellenőrzés
Független reviewer ugyanabból a specifikációból ugyanazt a sikerkritériumot és tiltott állapotot azonosítsa.
