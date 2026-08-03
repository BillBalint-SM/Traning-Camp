---
id: procedure.gui-action-grounding
title: GUI-művelet megalapozása
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [gui, computer-use, perception, action]
aliases: [gui action grounding, képernyőművelet megalapozás]
relations:
  - type: depends_on
    target: concept.multimodal-interaction-boundary
---

## Lényeg

Képernyőművelet előtt azonosítsd a célelemet, ellenőrizd az aktuális felületállapotot, végezd el a legkisebb műveletet, majd vizuális vagy strukturált visszajelzésből erősítsd meg az eredményt.

## Miért működik

A vizuális helyzet gyorsan változhat; az akció csak akkor megbízható, ha nem egy régi képre vagy feltételezett koordinátára épül.

## Mikor alkalmazd

Használd böngésző-, asztali- vagy mobilfelület automatizálásánál, különösen navigáció, űrlapkitöltés és állapotmódosítás előtt.

## Mikor ne alkalmazd

Ne kattints kizárólag képi hasonlóság alapján érzékeny vagy visszafordíthatatlan felületen, ha van stabil API, hozzáférési azonosító vagy emberi jóváhagyás.

## Döntési szabály

Ha a célelem azonosítása bizonytalan, előbb szerezz további megfigyelést vagy kérj megerősítést; a bizonytalan grounding nem végrehajtási engedély.

## Hibamódok

Az elcsúszott felület, az animáció, az átfedő elem és a késleltetett visszajelzés rossz célra végzett kattintást okozhat.

## Kapcsolatok

A tervezés–vezérlés szétválasztása a magas szintű szándékot választja el az alacsony szintű GUI-művelettől.

## Ellenőrzés

Minden kritikus GUI-lépés után ellenőrizd a megjelenő állapotot, és tesztelj hibás elrendezést, modális ablakot, késleltetést és eltűnő célelemet.
