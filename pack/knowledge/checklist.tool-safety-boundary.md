---
id: checklist.tool-safety-boundary
title: Eszközbiztonsági határlista
kind: checklist
maturity: validated
confidence: high
language: hu
tags: [tools, safety, authorization]
aliases: [tool safety boundary, eszközbiztonsági határ]
relations:
  - type: prevents
    target: failure-mode.unvalidated-autonomy
---

## Lényeg

Eszközművelet előtt ellenőrizd a célt, jogosultságot, célobjektumot, visszafordíthatóságot, naplózást és az utólagos ellenőrzés lehetőségét.

## Miért működik

A lista a veszélyes döntéseket a végrehajtás elé helyezi. Így a rendszer nem a modell jó szándékára, hanem ismételhető korlátokra támaszkodik.

## Mikor alkalmazd

Minden adatot módosító, megosztó, pénzügyi, jogosultsági vagy külső kommunikációs eszközhívásnál alkalmazd.

## Mikor ne alkalmazd

Ne egyszerűsítsd el a listát csak azért, mert egy művelet gyakori; a gyakoriság nem csökkenti a hatást.

## Döntési szabály

Ha a célobjektum, a jogosultság vagy a visszaolvasási bizonyíték nem egyértelmű, ne hívd meg az eszközt.

## Hibamódok

Veszélyes minta a széles célkijelölés, az implicit megerősítés, a nem naplózott módosítás és a hibából automatikusan következő újrapróbálkozás.

## Kapcsolatok

A lista az eszközszerződésre épül, és közvetlenül védi a rendszert az ellenőrizetlen önállóságtól.

## Ellenőrzés

Készíts negatív próbát minden tiltott műveletre; a futtatónak a hívás előtt kell elutasítania, nem utána kompenzálnia.
