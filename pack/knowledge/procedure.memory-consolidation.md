---
id: procedure.memory-consolidation
title: Memóriakonszolidáció
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [memory, consolidation, review, lifecycle]
aliases: [emlék konszolidáció]
relations:
  - type: depends_on
    target: pattern.memory-hierarchy
---

## Lényeg

A futási tapasztalatot csak kiválasztás, tömörítés, bizonyítékellenőrzés és explicit megőrzési döntés után emeld tartós memóriába.

## Miért működik

Az esemény és a hosszú távú tudás elválasztása csökkenti a zajt és a véletlen, egyszeri helyzetek beégetését.

## Mikor alkalmazd

Session lezárásakor, visszatérő hiba után vagy jóváhagyott preferencia módosításakor alkalmazd.

## Mikor ne alkalmazd

Ne konszolidálj pusztán azért, mert egy adat friss; egyszeri kérdés vagy ellenőrizetlen modellkövetkeztetés nem emlékjelölt.

## Döntési szabály

Csak ismétlődő, releváns, igazolt és engedélyezett jelet írj tartós szintre, a többit hagyd a rövid élettartamú állapotban.

## Hibamódok

A nyers előzmény automatikus felhalmozása elavult, ellentmondó és személyes adatokkal telített memóriát hoz létre.

## Kapcsolatok

A memóriahierarchiára épül; a reprezentációválasztás határozza meg a tartós rekord formáját.

## Ellenőrzés

Auditmintán kövesd végig, hogy a tartós rekordhoz milyen bizonyíték, jóváhagyás és lejárati szabály tartozik.
