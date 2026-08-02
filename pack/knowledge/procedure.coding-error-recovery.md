---
id: procedure.coding-error-recovery
title: Coding-agent hibavisszaállítás
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [coding-agent, recovery, debugging, git]
aliases: [coding agent hibás módosítás után]
relations:
  - type: depends_on
    target: procedure.coding-agent-workflow
---

## Lényeg

Hiba után állj meg, őrizd meg a kimenetet, határozd meg az első hibás állapotátmenetet, majd a legkisebb visszafordítható korrekcióból indulj újra.

## Miért működik

A bizonyíték megtartása és a gyökérok izolálása megakadályozza, hogy egymásra rakott próbálkozások tovább rontsák a repository állapotát.

## Mikor alkalmazd

Teszt-, build-, dependency-, merge- vagy futási hiba esetén alkalmazd.

## Mikor ne alkalmazd

Ne töröld a felhasználó változását, ne resetelj széles állapotot és ne gyengíts tesztet pusztán a zöld eredményért.

## Döntési szabály

Reprodukálj, hasonlíts működő mintához, fogalmazz egy hipotézist, teszteld minimálisan, majd csak igazolás után javíts.

## Hibamódok

A vak retry, catch-all fallback vagy széles visszaállítás elfedi az okot és elveszíthet értékes munkát.

## Kapcsolatok

A coding workflow-ra épül; a sessionless állapot és a Git-bizonyíték teszi folytathatóvá.

## Ellenőrzés

Az eredeti hibát a regressziós tesztnek a javítás nélkül elő kell idéznie, a javítással pedig meg kell szüntetnie.
