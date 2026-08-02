---
id: pattern.tool-discovery
title: Eszközfelfedezés feladathoz kötve
kind: pattern
maturity: reviewed
confidence: medium
language: hu
tags: [tools, discovery, capability]
aliases: [tool discovery, eszközfelfedezés]
relations:
  - type: depends_on
    target: procedure.tool-contract-design
---

## Lényeg

Az agent ne minden elérhető eszközt kapjon meg, hanem a feladathoz illő képességeket fedezze fel egy leírt katalógusból.

## Miért működik

A kisebb eszköztér csökkenti a rossz választás és a szükségtelen jogosultság esélyét. A képességleírás a művelet célját választja el a konkrét implementációtól.

## Mikor alkalmazd

Alkalmazd nagy eszközkészletnél, több környezetnél vagy eltérő jogosultságú felhasználóknál.

## Mikor ne alkalmazd

Ne vezesd be, ha néhány rögzített eszköz egyértelműen lefedi az összes feladatot és a katalógus csak többletterhet jelentene.

## Döntési szabály

Először a szükséges képességet azonosítsd, majd csak olyan eszközt ajánlj, amelynek szerződése és jogosultsági szintje megfelel a feladatnak.

## Hibamódok

A puszta név alapú keresés hasonló hangzású, de más hatású eszközt választhat. A túl részletes katalógus visszahozza a teljes eszköztér zaját.

## Kapcsolatok

A minta az eszközszerződésre épül, és a routing réteghez hasonló fokozatos feltárást használ.

## Ellenőrzés

Mérd külön, hogy ismert és új feladatoknál a kiválasztott eszköz szerződése megfelel-e a szükséges képességnek.
