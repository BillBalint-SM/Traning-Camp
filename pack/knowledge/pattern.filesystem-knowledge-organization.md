---
id: pattern.filesystem-knowledge-organization
title: Fájlrendszer-alapú tudásszervezés
kind: pattern
maturity: reviewed
confidence: high
language: hu
tags: [knowledge, filesystem, indexes, governance]
aliases: [mappaalapú tudásrendezés]
relations:
  - type: supports
    target: concept.structured-knowledge-index
---
## Lényeg
Szervezd a tudást stabil útvonalakkal, kis önálló egységekkel és géppel olvasható indexszel, hogy ember és agent ugyanazt a szerkezetet használja.
## Miért működik
A fájlrendszer egyszerűen verziózható, ellenőrizhető és eszközfüggetlen, ha az identitás nem az elhelyezéstől függ.
## Mikor alkalmazd
Helyi, hordozható vagy auditálható tudástárnál alkalmazd.
## Mikor ne alkalmazd
Ne tekintsd a mappanevet jogosultsági vagy üzleti szemantikának külön kontroll nélkül.
## Döntési szabály
Azonosítót adj a modulnak, útvonalat a navigációhoz, indexet a kereséshez és manifestet az integritáshoz.
## Hibamódok
A csak mappanévre épített tudás átrendezéskor törik, a túl mély hierarchia pedig elrejti a releváns anyagot.
## Kapcsolatok
A strukturált tudásindexet támogatja, a frissességi governance tartja karban.
## Ellenőrzés
Áthelyezés után is legyen érvényes azonosító, keresési találat és hivatkozás.
