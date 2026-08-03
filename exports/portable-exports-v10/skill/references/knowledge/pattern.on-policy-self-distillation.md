---
id: pattern.on-policy-self-distillation
title: Saját eloszlású öndesztilláció
kind: pattern
maturity: reviewed
confidence: medium
language: hu
tags: [self-distillation, on-policy, filtering]
aliases: [on policy öndesztilláció]
relations:
  - type: supports
    target: pattern.experience-driven-improvement
---

## Lényeg

Erősebb tanár nélkül a modell több saját próbából csak a függetlenül igazolt jobb trajektóriákat emeli vissza tanulási példává.

## Miért működik

A végrehajtható ellenőrzés kiszűrheti a modell véletlenül jó vagy új megoldásait, és sűrűbb tanulási jellé alakíthatja őket.

## Mikor alkalmazd

Használd objektíven verifikálható feladatoknál, ahol több minta generálása olcsóbb, mint külső tanár fenntartása.

## Mikor ne alkalmazd

Ne alkalmazd önértékelésre építve olyan feladatnál, ahol a helyességet ugyanaz a modell ítéli meg.

## Döntési szabály

Csak külső végrehajtás, teszt vagy szabály által igazolt trajektória kerülhet a visszatanítási készletbe.

## Hibamódok

A szelekciós torzítás, könnyű példák túlsúlya és rejtett verifier-hiba önmegerősítő teljesítményromlást okoz.

## Kapcsolatok

A minta az ellenőrzött tapasztalatból vezérelt fejlesztés egyik súlyfrissítő változata.

## Ellenőrzés

Mérd a generált minták lefedettségét, a verifier hamis pozitív arányát és a visszatanítás utáni nehéz holdout eredményt.
