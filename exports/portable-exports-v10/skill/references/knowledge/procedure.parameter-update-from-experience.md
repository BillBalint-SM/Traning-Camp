---
id: procedure.parameter-update-from-experience
title: Paraméterfrissítés tapasztalatból
kind: procedure
maturity: reviewed
confidence: medium
language: hu
tags: [parameters, experience, training]
aliases: [tapasztalat súlyfrissítésbe]
relations:
  - type: depends_on
    target: checklist.post-training-readiness
---

## Lényeg

Operatív tapasztalatból csak kurált, deduplikált, hozzájárulás- és adatvédelmi szempontból tiszta, függetlenül értékelt készlet után készíts súlyfrissítést.

## Miért működik

A szigorú kapu megakadályozza, hogy zajos egyedi esemény vagy érzékeny adat tartósan és nehezen törölhetően beépüljön a modellbe.

## Mikor alkalmazd

Használd, ha ugyanaz a viselkedési hiány sok helyzetben jelentkezik és külső réteggel nem kezelhető megbízhatóan.

## Mikor ne alkalmazd

Ne használj paraméterfrissítést friss tény, egyedi felhasználói preferencia, gyorsan változó szabály vagy kevés eset alapján.

## Döntési szabály

Csak akkor lépj súlyszintre, ha a tudás-, instrukció- és programréteg kontrollált kísérletben elégtelennek bizonyult.

## Hibamódok

Katasztrofális felejtés, adatmemorizálás, nehezen lokalizálható regresszió és törlési kötelezettség sérülése jelentkezhet.

## Kapcsolatok

Az eljárás a teljes utótanítási készenléti kaputól függ.

## Ellenőrzés

Futtass privacy auditot, kanári regressziókat, képességmegőrzési teszteket és verziózott összehasonlítást a korábbi súlyokkal.
