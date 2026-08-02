---
id: procedure.sft-data-pipeline
title: SFT adatfolyamat kialakítása
kind: procedure
maturity: reviewed
confidence: medium
language: hu
tags: [sft, dataset, validation]
aliases: [sft adatfolyamat]
relations:
  - type: depends_on
    target: procedure.dataset-quality-loop
---

## Lényeg

Az SFT adatfolyamat a célképességből mintavételi szabályt, demonstrációt, tisztítást, szeparált ellenőrzőkészletet és verziózott kiadást készít.

## Miért működik

A reprodukálható adatút lehetővé teszi, hogy a modellváltozás oka visszavezethető legyen konkrét példákra és minőségi döntésekre.

## Mikor alkalmazd

Használd minden ismételhető finomhangolás előtt, különösen több annotátor vagy több adatforrás esetén.

## Mikor ne alkalmazd

Ne taníts addig, amíg a célválaszok minősége, jogosultsága és értékelési szeparációja nem bizonyított.

## Döntési szabály

Csak olyan adatkészletet adj tanításhoz, amelynek minden rekordja megfelel a séma-, minőség-, duplikáció- és adatvédelmi kapunak.

## Hibamódok

Train–test szivárgás, rejtett duplikáció, hibás szerepformátum és licenc nélküli adat hamis javulást vagy kockázatot okoz.

## Kapcsolatok

Az eljárás az általános adatkészlet-minőségi hurokra épül.

## Ellenőrzés

Rögzítsd a verziót, tartalmi hash-t, szeparációs szabályt, elutasítási arányt és mintavételes emberi auditot.
