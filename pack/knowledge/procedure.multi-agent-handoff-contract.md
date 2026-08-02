---
id: procedure.multi-agent-handoff-contract
title: Több-agent átadási szerződés
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [multi-agent, handoff, contract, collaboration]
aliases: [agent handoff contract, agent átadási szerződés]
relations:
  - type: supports
    target: decision-guide.multi-agent-topology-selection
---

## Lényeg

Minden átadás tartalmazza a célt, a kész és nyitott munkát, a bizonyítékot, a releváns állapotot, az engedélyeket, a következő döntési pontot és a visszaadás feltételét.

## Miért működik

Az átadás nem beszélgetési összefoglaló, hanem felelősségátadás; a szerződés csökkenti a rejtett feltételezést és a korábbi munka ismétlését.

## Mikor alkalmazd

Használd szerepkörváltásnál, szakértői delegálásnál, párhuzamos ágak egyesítésénél és ember–agent együttműködésben.

## Mikor ne alkalmazd

Ne adj át teljes, nyers előzményt vagy titkos adatot csak azért, mert az elérhető; az átvevőnek a legkisebb szükséges, jogosult állapot kell.

## Döntési szabály

Ha az átvevő nem tudja a szerződésből megmondani, mit tehet, mit kell igazolnia és mikor kell visszaadnia a munkát, az átadás hiányos.

## Hibamódok

A bizonyíték nélküli kész állapot, az implicit jogosultság és a tulajdonos nélküli nyitott kérdés későbbi konfliktust vagy ismételt végrehajtást okoz.

## Kapcsolatok

A topológia választását valósítja meg, a közös állapot konkurenciakezelése pedig védi a párhuzamos átadásokat.

## Ellenőrzés

Egy új átvevő csak a szerződést használva végre tudja hajtani a következő biztonságos lépést és képes az eredményt a kijelölt formában visszaadni.
