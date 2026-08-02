---
id: pattern.two-layer-feature-flags
title: Kétrétegű feature flag rendszer
kind: pattern
maturity: reviewed
confidence: high
language: hu
tags: [release, feature-flags, experiments, rollback]
aliases: [kétrétegű feature flag]
relations:
  - type: supports
    target: procedure.continual-improvement-release-loop
---
## Lényeg
Válaszd szét a mechanizmust aktiváló technikai flaget és a felhasználói vagy kísérleti célcsoportot kijelölő policy-réteget.
## Miért működik
Ugyanaz a képesség biztonságosan kiadható, mérhető és visszavonható anélkül, hogy a mechanizmust újra kellene telepíteni.
## Mikor alkalmazd
Fokozatos agent-, prompt-, tool- vagy modellváltoztatásnál alkalmazd.
## Mikor ne alkalmazd
Ne hagyj korlátlan ideig tulajdonos és eltávolítási dátum nélküli flaget.
## Döntési szabály
A technikai flag legyen gyors kill switch; a policy legyen verziózott, auditálható célzás.
## Hibamódok
Az összekevert réteg nehezen visszavonható állapotot és értelmezhetetlen kísérleti csoportot okoz.
## Kapcsolatok
A continual improvement release loopot támogatja és az ablation eredményét termelési kontrollá alakítja.
## Ellenőrzés
Teszteld a bekapcsolást, célzást, ütközést, kill switch-et és teljes eltávolítást.
