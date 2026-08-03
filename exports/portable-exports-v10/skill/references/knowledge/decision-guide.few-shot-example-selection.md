---
id: decision-guide.few-shot-example-selection
title: Kevés példás minta kiválasztása
kind: decision-guide
maturity: reviewed
confidence: high
language: hu
tags: [few-shot, prompt, examples, generalization]
aliases: [few-shot példaválasztás]
relations:
  - type: supports
    target: procedure.system-prompt-architecture
---

## Lényeg

Kevés példát akkor adj, ha a kívánt formátumot, döntési határt vagy eszközhasználati mintát röviden pontosabban lehet megmutatni, mint leírni.

## Miért működik

A reprezentatív példa a szabály alkalmazását és nem csak a szabály megfogalmazását teszi láthatóvá.

## Mikor alkalmazd

Strukturált kimenet, nehezen verbalizálható stílus, határeset vagy eszközhívási sorrend stabilizálására alkalmazd.

## Mikor ne alkalmazd

Ne töltsd tele a kontextust ismétlődő példákkal, és ne használj olyan példát, amely érzékeny vagy véletlenül egyedi adatra tanít.

## Döntési szabály

Válassz kevés, egymást kiegészítő példát: egy tipikus pozitív esetet, egy releváns határesetet és szükség esetén egy elutasítási mintát.

## Hibamódok

A túl szűk vagy hibás példa utánzásra késztet, és rontja a korábban általánosítható feladatmegoldást.

## Kapcsolatok

A rendszerprompt architektúrát támogatja; a folyamatutasítás dönti el, hogy a példa mely lépéshez tartozik.

## Ellenőrzés

Hasonlítsd össze a szabály-only és példával kiegészített változatot nem látott, de releváns feladatokon; a példa csak akkor maradjon, ha javítja a mért eredményt.
