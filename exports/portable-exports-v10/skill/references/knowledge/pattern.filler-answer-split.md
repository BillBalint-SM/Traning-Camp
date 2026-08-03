---
id: pattern.filler-answer-split
title: Töltelékjel és válasz szétválasztása
kind: pattern
maturity: reviewed
confidence: medium
language: hu
tags: [voice, filler, latency]
aliases: [gyors töltelék lassú válasz]
relations:
  - type: depends_on
    target: decision-guide.reasoning-expression-coupling
---

## Lényeg

A gyors ág rövid, tartalommentes jelenlétjelzést ad, miközben a lassú ág elkészíti és ellenőrzi a tényleges választ.

## Miért működik

Csökkenti az érzékelt várakozást úgy, hogy nem kényszeríti korai következtetésre a tartalmi modellt.

## Mikor alkalmazd

Használd ritka, néhány másodperces késés elfedésére természetes beszédben.

## Mikor ne alkalmazd

Ne használd folyamatosan, és ne engedd, hogy a töltelék ígéretet vagy hamis készültséget sugalljon.

## Döntési szabály

Csak semleges, megszakítható és rövid jelzés mehet a gyors ágon.

## Hibamódok

Ismétlődő sablon, kulturálisan rossz tónus és túl hosszú töltelék irritáló vagy megtévesztő lesz.

## Kapcsolatok

A minta a gondolkodás és kifejezés tudatos szétválasztására épül.

## Ellenőrzés

Mérd az érzékelt várakozást, megszakítási arányt, töltelékgyakoriságot és a végválasz konzisztenciáját.
