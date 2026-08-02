---
id: decision-guide.workflow-or-autonomy
title: Workflow vagy autonóm döntés
kind: decision-guide
maturity: reviewed
confidence: high
language: hu
tags: [workflow, autonomy, orchestration]
aliases: [workflow vagy autonómia, determinisztikus vagy autonóm]
relations:
  - type: depends_on
    target: principle.harness-engineering
---

## Lényeg

Workflow akkor előnyös, ha a lépések és átmenetek előre ismertek; autonóm döntés akkor indokolt, ha a következő hasznos lépés a futás közben feltárt helyzettől függ.

## Miért működik

A két mód külön kezeli a kiszámíthatóságot és az alkalmazkodást, ezért nem fizetsz autonóm bizonytalanságért ott, ahol a sorrend valójában szabályba írható.

## Mikor alkalmazd

Válassz workflow-t jóváhagyási, adatfeldolgozási és ismétlődő üzleti folyamatokhoz; válassz autonómiát nyitott kutatáshoz, diagnózishoz vagy feltáró eszközhasználathoz.

## Mikor ne alkalmazd

Ne címkézz autonómnak egy olyan folyamatot, amelynek egyetlen várt útja van, és ne merevíts workflow-vá olyan helyzetet, amelyben a döntéshez hiányzik a szükséges információ.

## Döntési szabály

Ha a következő lépés legalább kilencven százalékban előre megmondható és eltéréskor egyértelmű a kivételkezelés, workflow-t használj; egyébként engedj korlátozott autonóm döntést.

## Hibamódok

A túl merev folyamat kikerüli a valós kivételeket, a túl szabad autonómia pedig költséges, nehezen auditálható kitérőket nyit.

## Kapcsolatok

Az agent feladatszerződése határozza meg a választás felelősségi és jogosultsági korlátait.

## Ellenőrzés

Mérd külön a normál út, a kivételes út, a kézi beavatkozás és a visszafordítás arányát mindkét megközelítésben.
