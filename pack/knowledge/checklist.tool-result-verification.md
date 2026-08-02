---
id: checklist.tool-result-verification
title: Eszközeredmény ellenőrzőlista
kind: checklist
maturity: reviewed
confidence: high
language: hu
tags: [tools, verification, evidence, execution]
aliases: [tool result verification, eszközeredmény ellenőrzés]
relations:
  - type: supports
    target: checklist.tool-safety-boundary
---

## Lényeg

Eszközhívás után ellenőrizd a válasz sémáját, a célobjektumot, a mellékhatást, az időbélyeget, az autorizációt, a visszaolvashatóságot és a hibaállapotot.

## Miért működik

Az eszköz válasza lehet hiányos, elavult vagy csak részben sikeres; az ellenőrzés választja el a tényleges hatást a modell által feltételezett hatástól.

## Mikor alkalmazd

Használd minden állapotmódosító, pénzügyi, jogosultsági, fájl- vagy kommunikációs művelet után.

## Mikor ne alkalmazd

Ne vezess be költséges visszaolvasást alacsony kockázatú, tisztán determinisztikus számításnál, ha a bemenet és a kimenet önmagában teljesen ellenőrizhető.

## Döntési szabály

Minél nagyobb a visszafordíthatatlanság vagy a külső hatás, annál közelebb legyen az ellenőrzés a végrehajtáshoz és annál függetlenebb legyen az eredeti hívástól.

## Hibamódok

A HTTP-siker vagy a természetes nyelvű üzenet önmagában nem bizonyítja, hogy a célállapot valóban megváltozott.

## Kapcsolatok

Az eszközbiztonsági határt erősíti, és az aszinkron megszakítás után szükséges állapot-visszaolvasást adja.

## Ellenőrzés

Készíts olyan negatív esetet, amely sikeres válaszkód mellett hibás vagy hiányzó külső állapotot ad, és igazold, hogy a folyamat ezt nem tekinti sikernek.
