---
id: procedure.status-signal-design
title: Agent státuszjel tervezése
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [agent, status, state, observability]
aliases: [agent státuszjel]
relations:
  - type: supports
    target: pattern.agent-status-representation
---

## Lényeg

Az agent státuszjele rövid, strukturált nézet legyen a célról, az aktuális fázisról, a nyitott akadályról, az utolsó igazolt eredményről és a következő megengedett lépésről.

## Miért működik

Ez az információ segít a modellnek és az operátornak ugyanazt a futási állapotot látni anélkül, hogy a teljes előzményt kellene újraértelmezni.

## Mikor alkalmazd

Többlépéses, megszakítható, aszinkron vagy több szereplős feladatnál alkalmazd.

## Mikor ne alkalmazd

Ne tükrözd bele a teljes beszélgetést, és ne tárolj benne nem ellenőrzött következtetést tényként.

## Döntési szabály

Csak a következő döntéshez szükséges állapotot tartsd meg, minden mezőnek legyen frissítési tulajdonosa és érvényességi feltétele.

## Hibamódok

Az elavult, túl hosszú vagy kétértelmű státusz hamis folytonosságérzetet ad, és rossz eszközlépést indíthat.

## Kapcsolatok

Az agent állapotábrázolását támogatja; a státuszfrissítés elhelyezése a cache- és kontextusköltséget szabályozza.

## Ellenőrzés

Megszakítás és újraindítás után a státuszból egyértelműen rekonstruálható legyen a biztonságos következő lépés.
