---
id: concept.multimodal-interaction-boundary
title: Multimodális interakciós határ
kind: concept
maturity: reviewed
confidence: medium
language: hu
tags: [multimodal, voice, gui]
aliases: [multimodal interaction boundary, multimodális határ]
relations:
  - type: applies_to
    target: procedure.tool-contract-design
---

## Lényeg

Kép, hang, grafikus felület és fizikai jel esetén különítsd el az észlelést, az értelmezést, a bizonytalanságot és a végrehajtási jogosultságot.

## Miért működik

A multimodális bemenet részleges, zajos vagy késleltetett lehet. A határok megnevezése megakadályozza, hogy az agent bizonytalan észlelésből biztos mellékhatást indítson.

## Mikor alkalmazd

Használd képernyővezérlésnél, hangalapú párbeszédnél, képfeldolgozásnál vagy bármely világérzékelő eszköznél.

## Mikor ne alkalmazd

Ne köss közvetlen, nagy hatású műveletet egyetlen nem megerősített vizuális vagy hangjelhez.

## Döntési szabály

Ha az észlelés bizonytalan vagy a művelet visszafordíthatatlan, kérj megerősítést vagy gyűjts második, független megfigyelést.

## Hibamódok

Gyakori hiba a felismert szöveg és a tényleges célobjektum összekeverése, illetve a felhasználói szándék következtetése hiányos hangjelből.

## Kapcsolatok

A fogalom az eszközszerződést alkalmazza olyan csatornákra, ahol az észlelés és a végrehajtás közötti rés különösen nagy.

## Ellenőrzés

Tesztelj zajos, félrevezető és késleltetett bemenetekkel; a rendszernek ilyenkor biztonságos bizonytalanságot kell jeleznie.
