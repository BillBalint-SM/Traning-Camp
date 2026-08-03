---
id: procedure.guardrail-design
title: Védőkorlát tervezése
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [safety, guardrail, policy, tools]
aliases: [guardrail tervezés]
relations:
  - type: supports
    target: checklist.tool-safety-boundary
---

## Lényeg

A védőkorlátokat a kockázatos átmenetek köré tervezd: bemenet elfogadása, jogosultságadományozás, külső művelet, adatkiadás és véglegesítés.

## Miért működik

A döntés előtti, szerződéses ellenőrzés megakadályozza, hogy a modellnek kelljen biztonsági szabályt megbízhatóan felidéznie.

## Mikor alkalmazd

Írási, pénzügyi, személyes adatot érintő, rendszeradminisztrációs vagy visszafordíthatatlan hatású eszköznél kötelezően használd.

## Mikor ne alkalmazd

Ne blokkolj veszélytelen olvasási lépéseket ugyanazzal a súrlódással, mint egy külső állapotváltoztatást.

## Döntési szabály

Kockázati szintenként határozz meg tiltást, automatikus engedélyt, megerősítést vagy emberi jóváhagyást; a default legyen a legkisebb jogosultság.

## Hibamódok

A kizárólag szöveges tiltás megkerülhető utasítással, a túl széles blokkolás pedig használhatatlanná teszi az agentet.

## Kapcsolatok

Az eszközbiztonsági határt támogatja, az emberi eszkaláció a nem automatizálható döntések folytatása.

## Ellenőrzés

Negatív tesztekben próbálj jogosulatlan paramétert, túl széles hatókört, ismételt végrehajtást és félrevezető bemenetet; mindnek egyértelműen meg kell állnia.
