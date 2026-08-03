---
id: concept.preference-modeling
title: Preferenciamodellezés
kind: concept
maturity: reviewed
confidence: medium
language: hu
tags: [preference, ranking, reward]
aliases: [emberi preferenciapárok]
relations:
  - type: supports
    target: procedure.pairwise-model-ranking
---

## Lényeg

A preferenciamodellezés abszolút címke helyett két vagy több kimenet relatív sorrendjéből tanul minőségi jelet.

## Miért működik

Az összehasonlítás gyakran könnyebb és következetesebb emberi döntés, mint egy összetett válasz pontos pontszámozása.

## Mikor alkalmazd

Használd stílus, hasznosság vagy több szempontú minőség esetén, amikor nincs közvetlen objektív sikerfüggvény.

## Mikor ne alkalmazd

Ne váltsd ki vele az objektív ellenőrzést kód, számítás, jogosultság vagy más géppel verifikálható eredmény esetén.

## Döntési szabály

Preferenciát csak akkor használj tanulási jelként, ha az annotátori egyezés és a vak ellenőrzőpárok stabilak.

## Hibamódok

Pozíciótorzítás, hosszpreferencia, annotátori stílus és eloszlási szűkösség hibás jutalommodellt hozhat létre.

## Kapcsolatok

A fogalom a páronkénti modellrangsorolás értékelési eljárását támogatja.

## Ellenőrzés

Mérd a párok közötti egyezést, cseréld fel a sorrendet kontrollként, és tarts vissza rejtett kalibrációs párokat.
