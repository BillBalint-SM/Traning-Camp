---
id: procedure.code-driven-media-generation
title: Kódvezérelt médiagenerálás
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [code, media, generation, reproducibility]
aliases: [média generálása kóddal]
relations:
  - type: applies_to
    target: principle.code-as-meta-capability
---

## Lényeg

Médiát deklaratív adatokból és verziózott renderelő kódból generálj, hogy a tartalom, elrendezés és export megismételhető legyen.

## Miért működik

A forrásadat és a transzformáció külön review-zható, a kimenet pedig ugyanabból a bemenetből újraépíthető.

## Mikor alkalmazd

Diagram, riport, prezentáció, képkompozíció vagy tömeges vizuális változat készítésekor alkalmazd.

## Mikor ne alkalmazd

Ne válassz programozott generálást egyszeri, erősen művészi módosításhoz, ha nincs ismételhetőségi igény.

## Döntési szabály

Rögzíts bemeneti sémát, determinisztikus renderelést, licencelt asset-határt és vizuális ellenőrzési lépést.

## Hibamódok

A helyes build is adhat olvashatatlan, levágott vagy vizuálisan félrevezető kimenetet.

## Kapcsolatok

A kód metaképességét alkalmazza; az értékelési környezet a vizuális minőség külön gate-jeit adhatja.

## Ellenőrzés

Ellenőrizd a reprodukálhatóságot, méretet, olvashatóságot, asset-eredetet és legalább egy renderelt mintát vizuálisan.
