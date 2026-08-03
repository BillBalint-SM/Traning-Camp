---
id: checklist.agent-task-contract
title: Agent feladatszerződés ellenőrzőlista
kind: checklist
maturity: reviewed
confidence: high
language: hu
tags: [agent, task, contract, scope]
aliases: [agent feladatszerződés, feladatindítási szerződés]
relations:
  - type: supports
    target: decision-guide.workflow-or-autonomy
---

## Lényeg

Indítás előtt rögzítsd a célt, a megengedett bemeneteket, az elérhető eszközöket, a módosítási jogot, a sikerfeltételt, a költségkeretet és az átadási formát.

## Miért működik

A szerződés a homályos szándékot megfigyelhető döntési határokká alakítja, ezért az agent nem kénytelen jogosultságot vagy kész állapotot kitalálni.

## Mikor alkalmazd

Használd minden külső állapotot olvasó vagy módosító, illetve több lépésben végrehajtott feladat elején.

## Mikor ne alkalmazd

Egyszerű, ember által közvetlenül felügyelt beszélgetésnél ne készíts túl részletes szerződést, ha az növeli a munkát, de nem csökkenti a kockázatot.

## Döntési szabály

Ha nem tudod egy mondatban kimondani, mi számít sikernek és mi tilos, a feladatot még tisztázni kell, nem elindítani.

## Hibamódok

A nyitott cél, a rejtett költségkeret és az implicit módosítási jog hatáskörtúllépést vagy korai sikerjelentést okoz.

## Kapcsolatok

A workflow vagy autonómia döntését konkretizálja, és összekapcsolódik az eszközszerződés részletes korlátaival.

## Ellenőrzés

Az indítási rekordból egy független ellenőr meg tudja mondani, milyen eredmény elfogadható és melyik eszközművelet tiltott.
