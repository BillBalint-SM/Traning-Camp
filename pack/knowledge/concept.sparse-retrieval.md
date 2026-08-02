---
id: concept.sparse-retrieval
title: Lexikális visszakeresés
kind: concept
maturity: reviewed
confidence: high
language: hu
tags: [retrieval, lexical-search, keywords, bm25]
aliases: [sparse retrieval]
relations:
  - type: supports
    target: decision-guide.retrieval-strategy-selection
---

## Lényeg

A lexikális visszakeresés a lekérdezésben szereplő kifejezések, azonosítók és ritka szavak pontos előfordulását jutalmazza.

## Miért működik

Egyedi név, kód, verzió vagy szakmai kifejezés esetén a szó szerinti egyezés sokszor erősebb jel, mint az általános jelentésbeli hasonlóság.

## Mikor alkalmazd

Pontos hivatkozás, azonosító, parancs, konfigurációs mező vagy megnevezett fogalom keresésekor alkalmazd.

## Mikor ne alkalmazd

Ne várj jó recallt erősen átfogalmazott vagy szinonimákkal kifejezett kérdésnél önmagában.

## Döntési szabály

Ha a lekérdezésben pontos karakterlánc vagy ritka kulcsszó van, kezdj lexikális jelből, majd bővíts szemantikával, ha kevés a találat.

## Hibamódok

A gyakori szavak és a felszíni egyezés irreleváns dokumentumot emelhetnek előre, miközben a valódi jelentés kimarad.

## Kapcsolatok

A retrieval stratégia választását támogatja; a hibrid fúzióban a szemantikus jel ellensúlyozza a szinonimaproblémát.

## Ellenőrzés

Tesztelj azonosító-alapú és átfogalmazott kérdéscsoportot külön, hogy látható legyen a módszer valódi erőssége és vakfoltja.
