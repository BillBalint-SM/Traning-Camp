---
id: checklist.knowledge-freshness-governance
title: Tudásfrissességi governance
kind: checklist
maturity: reviewed
confidence: high
language: hu
tags: [knowledge, freshness, governance, review]
aliases: [tudás frissesség ellenőrzés]
relations:
  - type: supports
    target: concept.structured-knowledge-index
---
## Lényeg
Minden döntést befolyásoló tudásegységhez rendelj tulajdonost, érvényességi jelzést, felülvizsgálati ritmust és visszavonási utat.
## Miért működik
A kereshető tudás csak akkor megbízható, ha az agent felismeri az elavult vagy vitatott anyagot.
## Mikor alkalmazd
Gyorsan változó szabály, rendszer vagy működési útmutató esetén alkalmazd.
## Mikor ne alkalmazd
Ne frissíts automatikusan megbízhatósági besorolást pusztán egy fájl módosítási ideje alapján.
## Döntési szabály
A kockázattal arányos review-ciklust és lejárati viselkedést rögzítsd a modul életciklusában.
## Hibamódok
Tulajdonos nélküli tudás elavul, a csendes felülírás pedig elveszíti a döntés indokát.
## Kapcsolatok
A strukturált indexet támogatja; a manifest az integritást, nem a tartalmi frissességet bizonyítja.
## Ellenőrzés
Válassz lejárt és aktív mintát, majd igazold a megfelelő jelzést, routingot és visszavonást.
