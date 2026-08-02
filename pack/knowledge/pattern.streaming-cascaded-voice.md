---
id: pattern.streaming-cascaded-voice
title: Végponttól végpontig streamelt hanglánc
kind: pattern
maturity: reviewed
confidence: medium
language: hu
tags: [streaming, voice, latency]
aliases: [streamelt kaszkádolt hang]
relations:
  - type: depends_on
    target: decision-guide.voice-pipeline-architecture
---

## Lényeg

A beszédfelismerés, gondolkodás és beszédszintézis részleges eredményeit folyamatosan továbbítsd, explicit megszakítási és visszavonási szerződéssel.

## Miért működik

A komponensek átfedő futása csökkenti az első válaszhang idejét anélkül, hogy feladnád a moduláris megfigyelhetőséget.

## Mikor alkalmazd

Használd kaszkádolt hangrendszernél, ahol a teljes mondat megvárása túl lassú.

## Mikor ne alkalmazd

Ne streamelj visszavonhatatlan állítást vagy műveletet, ha a későbbi kontextus megváltoztathatja a jelentést.

## Döntési szabály

Csak stabil részletet adj tovább; bizonytalan részhez tarts visszavonható puffert és verziót.

## Hibamódok

Részleges hipotézis ingadozása, duplikált token, rossz megszakítás és komponensek közti backpressure töredezett választ okoz.

## Kapcsolatok

A minta a kaszkádolt voice pipeline választására épül.

## Ellenőrzés

Mérd komponensenként az első részlet idejét, véglegesítés késését, visszavonásokat és felhasználói megszakítást.
