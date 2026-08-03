---
id: procedure.streaming-turn-detection
title: Streamelt fordulódetektálás
kind: procedure
maturity: reviewed
confidence: medium
language: hu
tags: [turn-taking, streaming, perception]
aliases: [streamelt beszédforduló érzékelés]
relations:
  - type: supports
    target: pattern.streaming-cascaded-voice
---

## Lényeg

A forduló végét akusztikai csend, beszédtartalom, szemantikai befejezettség és interakciós állapot közös jeléből becsüld.

## Miért működik

A többjelű döntés kevésbé vág bele gondolkodási szünetbe, mégsem vár indokolatlanul hosszú fix timeoutot.

## Mikor alkalmazd

Használd természetes, változó tempójú beszélgetésnél.

## Mikor ne alkalmazd

Ne indíts érzékeny műveletet kizárólag valószínű fordulóvég alapján explicit megerősítés nélkül.

## Döntési szabály

Alacsony bizonyosságnál rövid visszakérdezést vagy várakozó állapotot válassz a válasz indítása helyett.

## Hibamódok

Zaj, akcentus, hosszú szünet és háttérbeszéd hamis kezdést vagy véget jelezhet.

## Kapcsolatok

Az eljárás a streamelt hanglánc megszakítási pontját támogatja.

## Ellenőrzés

Mérd a téves közbevágást, késői választ, megszakítás utáni helyreállást és eltérő beszédstílusokat.
