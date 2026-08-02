---
id: decision-guide.experience-encoding-layer
title: Tapasztalat kódolási rétegének kiválasztása
kind: decision-guide
maturity: reviewed
confidence: medium
language: hu
tags: [experience, knowledge, adaptation]
aliases: [tudásba instrukcióba vagy programba kódoljam a tapasztalatot]
relations:
  - type: depends_on
    target: concept.operational-trajectory-learning-signal
---

## Lényeg

A tapasztalatot a legkisebb elégséges rétegbe emeld: tudásba tényként, instrukcióba szabályként, programba determinisztikus eljárásként, paraméterbe csak tartós viselkedésként.

## Miért működik

Az alacsonyabb rétegek gyorsabban ellenőrizhetők, könnyebben visszagörgethetők és kevesebb nem szándékolt képességet módosítanak.

## Mikor alkalmazd

Használd minden bizonyított tapasztalat promóciója előtt.

## Mikor ne alkalmazd

Ne emelj egyedi esetet általános szabállyá és ne válassz súlyfrissítést pusztán tartóssági igény miatt.

## Döntési szabály

Válaszd azt a legkülső, verziózható réteget, amelyben a kívánt javulás determinisztikusan kifejezhető és mérhető.

## Hibamódok

Túl mély kódolás rejtett regressziót, túl sekély kódolás kontextusterhelést vagy következetlen végrehajtást okozhat.

## Kapcsolatok

A döntés csak hiteles operatív trajektóriából származó jelre épülhet.

## Ellenőrzés

Készíts ugyanarra a hibára legalább két rétegalternatívát, és hasonlítsd össze a hatást, költséget, terjedést és rollback-időt.
