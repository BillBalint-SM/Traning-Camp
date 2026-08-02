---
id: procedure.safe-file-editing
title: Biztonságos fájlszerkesztés
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [coding-agent, editing, patch, scope]
aliases: [biztonságosan fájlokat coding agent]
relations:
  - type: supports
    target: procedure.coding-agent-workflow
---

## Lényeg

Szerkesztés előtt olvasd a célfájlt és instrukcióit, majd kis, explicit patchben változtass, megőrizve az idegen módosításokat és a fájl formátumát.

## Miért működik

A patch láthatóvá teszi a szándékot, szűkíti a felülírási felületet és könnyen review-zható.

## Mikor alkalmazd

Minden kézi vagy agent által végzett forrás-, teszt-, konfiguráció- és dokumentációmódosításnál alkalmazd.

## Mikor ne alkalmazd

Ne használj teljes fájlt újrageneráló megoldást kis változáshoz, ha az elveszítheti a felhasználó párhuzamos munkáját.

## Döntési szabály

A legkisebb kohézív diffet készítsd, majd olvasd vissza a célrészt, futtasd a formátum- és viselkedési ellenőrzést.

## Hibamódok

A vak felülírás, széles keresés-csere, rossz encoding vagy nem ellenőrzött generátor zajt és adatvesztést okoz.

## Kapcsolatok

A coding workflow-t támogatja; a search bizonyítja a helyet, a recovery kezeli a sikertelen módosítást.

## Ellenőrzés

A diff kizárólag a szükséges sorokat érintse, legyen formailag tiszta, és a célzott teszt igazolja az új viselkedést.
