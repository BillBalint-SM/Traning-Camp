---
id: procedure.failure-diagnosis-to-improvement
title: Hibadiagnózistól javítási jelöltig
kind: procedure
maturity: reviewed
confidence: medium
language: hu
tags: [diagnosis, hypothesis, improvement]
aliases: [hibából javítási jelölt]
relations:
  - type: depends_on
    target: procedure.benchmark-error-analysis
---

## Lényeg

Reprodukálj, kategorizálj, keresd meg a legkorábbi hibás döntést, fogalmazz meg egyetlen okhipotézist, majd készíts legkisebb visszafordítható javítási jelöltet.

## Miért működik

Az ok és a javítás összekapcsolása megakadályozza, hogy tüneti promptfoltozás vagy több egyidejű módosítás elfedje a valódi hatást.

## Mikor alkalmazd

Használd minden ismétlődő vagy nagy hatású operatív hiba után.

## Mikor ne alkalmazd

Ne készíts általános fejlesztést egyszeri, nem reprodukálható és külső rendszerhibából.

## Döntési szabály

Egy jelölt egy diagnosztizált okot célozzon, és legyen hozzá pozitív reprodukció, negatív kontroll és regressziós környezet.

## Hibamódok

Utólagos narratíva, összecsomagolt változtatások és nem reprezentatív reprodukció téves ok-okozatot sugall.

## Kapcsolatok

Az eljárás a strukturált benchmark-hibaanalízisre épül.

## Ellenőrzés

Mutasd meg, hogy a jelölt megszünteti az eredeti hibát, nem változtatja meg a negatív kontrollt, és nem rontja a releváns eloszlást.
