---
id: decision-guide.reasoning-expression-coupling
title: Gondolkodás és kifejezés összekapcsolása
kind: decision-guide
maturity: reviewed
confidence: medium
language: hu
tags: [reasoning, expression, latency]
aliases: [gondolkodás kifejezés szétválasztása]
relations:
  - type: supports
    target: pattern.fast-slow-interaction-loop
---

## Lényeg

Válaszd szét a gyors interakciós jelzést a lassú tartalmi döntéstől, kivéve ha az egységes modell bizonyítottan jobban kezeli az időzítést és a tartalmat.

## Miért működik

A szétválasztás alacsony reakcióidőt ad anélkül, hogy a rendszer elhamarkodná a végső választ.

## Mikor alkalmazd

Használd komplex tanácsadás, keresés vagy eszközhasználat melletti beszélgetésnél.

## Mikor ne alkalmazd

Ne generálj tölteléket, amely állításnak, beleegyezésnek vagy kész eredménynek hangzik.

## Döntési szabály

Ha a tartalmi válasz késik, csak visszavonható interakciós jelet adj; végállítást csak ellenőrzött lassú ágból.

## Hibamódok

Ellentmondó gyors és lassú ág, túlbeszélés vagy félrevezető magabiztosság csökkenti a bizalmat.

## Kapcsolatok

Az útmutató a gyors–lassú interakciós ciklust konkretizálja.

## Ellenőrzés

Mérd külön az első reakciót, végső válasz idejét, ellentmondásokat és megszakítás utáni konzisztenciát.
