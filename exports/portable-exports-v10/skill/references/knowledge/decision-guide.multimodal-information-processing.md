---
id: decision-guide.multimodal-information-processing
title: Multimodális tudásfeldolgozási stratégia
kind: decision-guide
maturity: reviewed
confidence: high
language: hu
tags: [retrieval, multimodal, documents, tools]
aliases: [multimodális információszerzés]
relations:
  - type: supports
    target: procedure.retrieval-pipeline-design
---
## Lényeg
Szöveggé alakíts, natívan elemezz vagy célzott eszközt hívj a keresett bizonyíték típusától és a veszteségkockázattól függően.
## Miért működik
Nem minden vizuális, hang- vagy táblázatos információ őrizhető meg megbízhatóan egyszerű szövegkinyeréssel.
## Mikor alkalmazd
Vegyes formátumú tudástárnál vagy vizuális bizonyítékot igénylő kérdésnél alkalmazd.
## Mikor ne alkalmazd
Ne használj drága multimodális feldolgozást, ha a szükséges állítás strukturált szövegből igazolható.
## Döntési szabály
Az olcsóbb reprezentációval kezdj, de válts mélyebb érzékelésre, ha az információvesztés a döntést változtatná.
## Hibamódok
A vak szövegkinyerés kihagyhat diagramjelentést, a túl korai mélyelemzés pedig költséget és késleltetést növel.
## Kapcsolatok
A retrieval pipeline-t támogatja; a perception eszközök adják a végrehajtási oldalt.
## Ellenőrzés
Ellenőrizd mintákon, hogy a választott módszer visszaadja-e a döntéshez szükséges attribútumokat.
