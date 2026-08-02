---
id: procedure.real-time-latency-budget
title: Valós idejű késleltetés budgetelése
kind: procedure
maturity: reviewed
confidence: medium
language: hu
tags: [latency, realtime, budget]
aliases: [valós idejű latency budget]
relations:
  - type: supports
    target: pattern.fast-slow-interaction-loop
---

## Lényeg

Bontsd fel a végponti késleltetést érzékelésre, hálózatra, sorban állásra, következtetésre, eszközre, szintézisre és felhasználói visszacsatolásra.

## Miért működik

A komponensbudget megmutatja a valódi szűk keresztmetszetet és elválasztja az átlagot a faroklatenciától.

## Mikor alkalmazd

Használd hang-, GUI- és fizikai vezérlés teljesítménytervezésénél.

## Mikor ne alkalmazd

Ne optimalizáld a mediánt, ha a ritka lassú esetek megszakítják a vezérlést vagy biztonsági kockázatot okoznak.

## Döntési szabály

Minden komponensnek legyen p50/p95/p99 budgetje, timeoutja és degradációs viselkedése.

## Hibamódok

Queueing, hidegindítás, hálózati jitter és blokkos eszköz egyetlen átlagérték mögött rejtve marad.

## Kapcsolatok

Az eljárás a gyors–lassú ciklus időbeli szerződését teszi mérhetővé.

## Ellenőrzés

Mérj végponttól végpontig és komponensenként terhelés, megszakítás és hibás dependency alatt.
