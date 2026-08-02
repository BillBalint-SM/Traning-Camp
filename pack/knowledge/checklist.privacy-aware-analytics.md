---
id: checklist.privacy-aware-analytics
title: Adatvédelmi tudatos analitika
kind: checklist
maturity: reviewed
confidence: high
language: hu
tags: [analytics, privacy, observability, retention]
aliases: [privacy-aware agent analytics]
relations:
  - type: supports
    target: checklist.agent-observability
---
## Lényeg
Analitikai jel gyűjtése előtt rögzítsd a célt, szükséges granularitást, érzékeny mezők kezelését, hozzáférést, megőrzést és törlést.
## Miért működik
A rendszer csak a fejlesztési döntéshez szükséges bizonyítékot tartja meg, nem korlátlan nyers interakciót.
## Mikor alkalmazd
Trace, prompt-, tool-, felhasználói vagy hibaanalitika tervezésekor alkalmazd.
## Mikor ne alkalmazd
Ne gyűjts nyers személyes tartalmat, ha aggregált esemény vagy anonimizált jellemző elegendő.
## Döntési szabály
A legkisebb szükséges adatot gyűjtsd rövid megőrzéssel, külön jogosultsággal és dokumentált felhasználással.
## Hibamódok
A teljes trace később más célra használva újraazonosítást, titokszivárgást és bizalomvesztést okozhat.
## Kapcsolatok
Az agent observabilityt támogatja és a memory privacy sanitization elvét alkalmazza.
## Ellenőrzés
Auditáld a mezőket, hozzáféréseket, lejáratot, törlést és azt, hogy a célmetrika nyers tartalom nélkül is számítható.
