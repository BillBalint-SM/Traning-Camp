---
id: procedure.human-escalation-design
title: Emberi eszkaláció tervezése
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [human-in-the-loop, escalation, approval, safety]
aliases: [emberi jóváhagyási pont]
relations:
  - type: depends_on
    target: procedure.guardrail-design
---

## Lényeg

Az emberi eszkaláció ne általános segítségkérés legyen, hanem hatáskörrel, bizonytalansággal, döntési lehetőségekkel és visszaadott kontrollal rendelkező állapotátadás.

## Miért működik

Az ember gyorsan akkor tud jóváhagyni vagy korrigálni, ha a rendszer világosan elválasztja a tényeket, a kockázatot és a javasolt hatást.

## Mikor alkalmazd

Bizonytalan identitás, ellentmondó szabály, magas hatás, kivételes jogosultság vagy visszafordíthatatlan lépés előtt alkalmazd.

## Mikor ne alkalmazd

Ne kérj jóváhagyást minden alacsony kockázatú, teljesen ellenőrizhető olvasási vagy számítási lépéshez.

## Döntési szabály

Az eszkalációs csomag tartalmazza a célt, az előzményt, a blokkoló feltételt, a választható műveleteket, az alapértelmezett biztonságos utat és a határidőt.

## Hibamódok

A kontextus nélküli "megerősíted?" kérdés rossz döntést, lassú válaszidőt vagy megtévesztő automatikus folytatást okoz.

## Kapcsolatok

A védőkorlát tervezésére épül, és a feladat-szerződésben rögzített megállási feltételeket használja.

## Ellenőrzés

Szimulált kivételben mérd, hogy a jóváhagyó a szükséges információból egyértelműen választ tud-e adni, és elutasításkor a rendszer biztonságosan zár-e.
