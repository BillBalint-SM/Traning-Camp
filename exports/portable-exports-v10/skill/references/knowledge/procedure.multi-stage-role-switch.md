---
id: procedure.multi-stage-role-switch
title: Többlépcsős szerepváltás
kind: procedure
maturity: reviewed
confidence: medium
language: hu
tags: [roles, stages, handoff]
aliases: [többlépcsős agent szerepváltás]
relations:
  - type: supports
    target: pattern.shared-context-role-switching
---

## Lényeg

Minden fázishoz rögzíts belépési feltételt, szerepcélt, írható mezőket, kimeneti szerződést és következő fázis kapuját.

## Miért működik

A fázisok így ellenőrizhető állapotgéppé válnak, nem puszta egymás utáni promptokká.

## Mikor alkalmazd

Használd kutatás–tervezés–megvalósítás–review jellegű lineáris folyamatban.

## Mikor ne alkalmazd

Ne engedj szerepet saját kimenetének végső jóváhagyójává válni magas kockázatnál.

## Döntési szabály

Következő fázis csak sémaérvényes és kapuval ellenőrzött artifactot fogadhat.

## Hibamódok

Hiányos átadás, nem idempotens újrapróbálás és visszafelé írás felborítja a folyamatot.

## Kapcsolatok

Az eljárás a közös kontextusú szerepváltást teszi végrehajthatóvá.

## Ellenőrzés

Tesztelj hiányzó mezőt, fázisismétlést, elutasítást és megszakítás utáni folytatást.
