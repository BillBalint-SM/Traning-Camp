---
id: pattern.react-observe-act-loop
title: Megfigyelés–döntés–cselekvés ciklus
kind: pattern
maturity: reviewed
confidence: high
language: hu
tags: [agent, observation, action, loop]
aliases: [observe act loop, megfigyelés cselekvés ciklus]
relations:
  - type: depends_on
    target: principle.agent-operating-model
---

## Lényeg

Az agent minden külső hatású lépés előtt friss megfigyelésből dönt, végrehajtja a legkisebb indokolt műveletet, majd az eredményt új megfigyelésként visszaírja a helyzetbe.

## Miért működik

A ciklus nem engedi, hogy a rendszer régi feltételezésre építsen, és az eszközeredményeket bizonyítékként kezeli a következő döntéshez.

## Mikor alkalmazd

Használd akkor, ha a környezet változhat, az eszköz hibázhat, vagy a következő lépés csak az előző eredménye után választható ki.

## Mikor ne alkalmazd

Ne használd szükségtelenül zárt, előre kiszámítható transzformációra, ahol egyetlen determinisztikus művelet elég.

## Döntési szabály

Minden iterációban mondd ki, milyen megfigyelés hiányzik, milyen művelet csökkenti a bizonytalanságot, és milyen eredmény állítja le a ciklust.

## Hibamódok

Az ismétlődő, új információt nem hozó cselekvés végtelen körhöz, a nem ellenőrzött eszközkimenet pedig hamis előrehaladáshoz vezet.

## Kapcsolatok

Az állapotreprezentáció támaszkodik rá, a futtatási keret pedig korlátot ad neki.

## Ellenőrzés

Egy visszajátszható futásban minden akcióhoz egy előtte rögzített megfigyelés és egy utána rögzített eredmény tartozik.
