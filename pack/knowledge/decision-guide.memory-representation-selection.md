---
id: decision-guide.memory-representation-selection
title: Memóriaábrázolás választása
kind: decision-guide
maturity: reviewed
confidence: high
language: hu
tags: [memory, representation, structured-data]
aliases: [memóriaformátum választás]
relations:
  - type: depends_on
    target: pattern.memory-hierarchy
---

## Lényeg

Az emléket a használati módhoz válaszd: rövid tényhez mező, összetett indokhoz jegyzet, ismétlődő döntéshez szabály vagy program.

## Miért működik

A forma meghatározza a kereshetőséget, a frissíthetőséget, az auditot és azt, mennyire könnyű hibás általánosítást javítani.

## Mikor alkalmazd

Új tartós emléktípus vagy felhasználói profilmező tervezésekor alkalmazd.

## Mikor ne alkalmazd

Ne kódolj programba változékony, bizonytalan vagy emberi jóváhagyást igénylő szabályt.

## Döntési szabály

Válaszd a legegyszerűbb reprezentációt, amely támogatja a szükséges lekérdezést, frissítést, törlést és eredetvizsgálatot.

## Hibamódok

A szabad szövegbe rejtett kritikus mező nem ellenőrizhető; a túl merev séma elveszíti a kivételhez szükséges jelentést.

## Kapcsolatok

A memóriahierarchiára épül, a konszolidáció tölti fel és a privacy ellenőrzőlista korlátozza.

## Ellenőrzés

Mintapéldákon igazold, hogy a memória visszakereshető, célzottan módosítható és teljesen törölhető.
