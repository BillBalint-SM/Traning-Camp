---
id: procedure.system-prompt-architecture
title: Rendszerprompt architektúra
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [context-engineering, system-prompt, instructions, policy]
aliases: [rendszerprompt architektúra, utasításrétegezés]
relations:
  - type: supports
    target: principle.harness-engineering
---

## Lényeg

Szervezd a rendszerpromptot cél, működési folyamat, biztonsági korlát, eszközhasználati szabály és válaszformátum rétegekre, ebben a sorrendben.

## Miért működik

A folyamatra épülő utasítás csökkenti a szabályütközést: a modell nem elszigetelt tiltásokból próbálja kitalálni a következő biztonságos lépést.

## Mikor alkalmazd

Használd minden tartós agent-szerepnél, különösen akkor, ha az agent eszközt hívhat vagy érzékeny üzleti szabályt alkalmaz.

## Mikor ne alkalmazd

Ne zsúfold tele a promptot ritka kivételekkel, teljes kézikönyvekkel vagy olyan adattal, amelyet célzottan vissza lehet keresni.

## Döntési szabály

Ha egy szabály csak egy konkrét folyamatlépéshez tartozik, a lépésnél add meg; ha minden lépésre érvényes, maradjon magasabb rétegben.

## Hibamódok

A szabályhalmozás ellentmondó prioritásokat, az elrejtett formátumkövetelmény pedig nehezen észrevehető kimeneti hibákat okoz.

## Kapcsolatok

A promptinjekciós határ védi, a dinamikus skill-betöltés pedig megakadályozza, hogy minden domainutasítás állandóan jelen legyen.

## Ellenőrzés

Tesztelj normál, hiányos, ellentmondó és rosszindulatú bemenetet úgy, hogy a kívánt folyamatlépés és a tiltott művelet is egyértelműen mérhető legyen.
