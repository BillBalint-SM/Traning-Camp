---
id: failure-mode.unvalidated-autonomy
title: Ellenőrizetlen önállóság
kind: failure-mode
maturity: validated
confidence: high
language: hu
tags: [autonomy, safety, verification]
aliases: [unvalidated autonomy, ellenőrzés nélküli végrehajtás]
relations: []
---

## Lényeg

Az ellenőrizetlen önállóság akkor jelenik meg, amikor az agent bizonytalan értelmezésből, hiányos jogosultsággal vagy visszaolvasás nélkül indít mellékhatást.

## Miért működik

A hiba gyakran azért marad rejtve, mert a rendszer azonnal hasznosnak tűnő választ ad. A tényleges hatás és a szándék közötti eltérést csak külső ellenőrzés tárja fel.

## Mikor alkalmazd

Használd kockázatértékelési szempontrendszerként, amikor az agent nemcsak javasol, hanem eszközökkel változtat is.

## Mikor ne alkalmazd

Ne tekints minden önálló lépésre hibaként; alacsony kockázatú, visszafordítható művelet lehet automatizálható, ha szerződés és mérés védi.

## Döntési szabály

Minél nagyobb a mellékhatás és minél gyengébb a bizonyíték, annál erősebb előzetes jóváhagyás és utólagos visszaolvasás szükséges.

## Hibamódok

Jellemző tünet a kitalált siker, a rossz célobjektum módosítása, a jogosultság átugrása és az ismételt automatikus hívás.

## Kapcsolatok

Az eszközbiztonsági határlista, a kontextustömörítés és a több-agent határok mind ezt a hibamódot mérséklik.

## Ellenőrzés

Szimulálj félreérthető célt és sikertelen műveletet; a rendszernek meg kell állnia, jeleznie kell a bizonytalanságot, és nem állíthat sikeres végrehajtást bizonyíték nélkül.
