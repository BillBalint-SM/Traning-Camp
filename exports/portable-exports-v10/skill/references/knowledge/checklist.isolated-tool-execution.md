---
id: checklist.isolated-tool-execution
title: Izolált eszközvégrehajtás
kind: checklist
maturity: reviewed
confidence: high
language: hu
tags: [tools, isolation, sandbox, safety]
aliases: [sandboxolt tool futtatás]
relations:
  - type: supports
    target: checklist.tool-safety-boundary
---

## Lényeg

Kockázatos végrehajtás előtt korlátozd a fájlrendszert, hálózatot, hitelesítő adatokat, erőforrást, futási időt és továbbadható eredményt.

## Miért működik

Az izoláció a hibás vagy ellenséges művelet hatását a deklarált munkatérre és időablakra szűkíti.

## Mikor alkalmazd

Idegen kód, shell, böngésző, konverter vagy nem megbízható dokumentumfeldolgozó futtatásakor alkalmazd.

## Mikor ne alkalmazd

Ne tekintsd az izolációt a bemenet-, jogosultság- és eredményellenőrzés helyettesítőjének.

## Döntési szabály

Csak a feladathoz szükséges útvonalat, végpontot, titkot és erőforrást add át, majd a kimenetet külön validáld, mielőtt magasabb bizalmi szintre kerül.

## Hibamódok

A host könyvtár, teljes környezeti változók vagy korlátlan hálózat átadása megszünteti az izoláció valódi védelmét.

## Kapcsolatok

Az eszközbiztonsági határt támogatja; a tool-interface hűség és eredményellenőrzés zárja a végrehajtási láncot.

## Ellenőrzés

Negatív tesztben próbálj kilépni a munkatérből, hálózati tiltást megkerülni és erőforráskorlátot túllépni; mindnek kontrolláltan kell leállnia.
