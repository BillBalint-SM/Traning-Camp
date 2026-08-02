---
id: decision-guide.process-or-outcome-reward
title: Folyamatjutalom vagy eredményjutalom
kind: decision-guide
maturity: reviewed
confidence: medium
language: hu
tags: [process-reward, outcome-reward, multi-turn]
aliases: [folyamatjutalmat vagy eredményjutalmat]
relations:
  - type: depends_on
    target: decision-guide.reward-signal-density
---

## Lényeg

Eredményjutalmat válassz, ha a végállapot megbízhatóan ellenőrizhető; folyamatjutalmat akkor adj, ha a biztonságos vagy helyes köztes lépések önállóan is verifikálhatók.

## Miért működik

A végjel megőrzi a cél szabadságát, a folyamatjel pedig csökkenti a hosszú trajektória bizonytalanságát és kikényszeríthet kritikus invariánsokat.

## Mikor alkalmazd

Használd több lépéses döntések jutalmazási szerződésének tervezésekor.

## Mikor ne alkalmazd

Ne jutalmazz szubjektív gondolatmenetet vagy olyan köztes mintát, amelynek helyessége nem ellenőrizhető függetlenül.

## Döntési szabály

Objektív végállapotnál a végjutalom legyen elsődleges; köztes jelet csak bizonyított biztonsági vagy verifikációs okból adj.

## Hibamódok

A túl szigorú folyamatjutalom elnyomhat új, jó stratégiákat; a puszta végjutalom veszélyes kiskapukat hagyhat nyitva.

## Kapcsolatok

A döntés a jutalomjel sűrűségének megválasztására épül.

## Ellenőrzés

Futtass folyamatjel-ablációt, és ellenőrizd külön a végsikert, szabálykövetést, változatosságot és jutalomkijátszást.
