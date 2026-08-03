---
id: procedure.dataset-quality-loop
title: Értékelési adathalmaz minőségi ciklusa
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [evaluation, dataset, quality, iteration]
aliases: [eval dataset minőség]
relations:
  - type: depends_on
    target: pattern.task-distribution-coverage
---
## Lényeg
Az eval adathalmazt hibajelentésekből, lefedettségi résekből és reviewer-elt feladatokból frissítsd, verziózott változtatással és visszaméréssel.
## Miért működik
A valós hibákból származó, kontrollált esetek a rendszer tényleges kockázatát mérik, nem egy statikus mintát optimalizálnak túl.
## Mikor alkalmazd
Minden evaluation ciklus és termelési hibaelemzés után alkalmazd.
## Mikor ne alkalmazd
Ne emelj be automatikusan duplikált, bizonytalan vagy a jelenlegi rendszer outputjára túlillesztett esetet.
## Döntési szabály
Minden jelöltnek legyen képességcímkéje, objektív verifierje, duplikációs ellenőrzése és review-indoka.
## Hibamódok
A tesztadat-szivárgás, mintaarány-eltolódás és hibás címke mesterséges javulást vagy romlást okoz.
## Kapcsolatok
A task distribution coverage-re épül; a benchmark error analysis új eseteket javasol.
## Ellenőrzés
Mérd a verziók közti eloszlást, duplikációt, verifier-egyezést és baseline elmozdulást.
