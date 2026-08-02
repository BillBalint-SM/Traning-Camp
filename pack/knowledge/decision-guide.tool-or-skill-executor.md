---
id: decision-guide.tool-or-skill-executor
title: Dedikált eszköz vagy skill végrehajtó
kind: decision-guide
maturity: reviewed
confidence: high
language: hu
tags: [tools, skills, execution, design]
aliases: [dedikált eszköz vagy skill]
relations:
  - type: depends_on
    target: concept.tool-capability-taxonomy
---
## Lényeg
Dedikált eszközt válassz szűk, stabil és erősen ellenőrizhető művelethez; skill plusz általános végrehajtót változatos, leíró tudást igénylő munkához.
## Miért működik
Az eszköz szerződést és korlátot ad, a skill pedig anélkül bővíti a működést, hogy minden változathoz új API kellene.
## Mikor alkalmazd
Új képesség kifejezési formájának tervezésekor alkalmazd.
## Mikor ne alkalmazd
Ne rejts nagy hatású írási műveletet általános végrehajtó mögé szűk validáció nélkül.
## Döntési szabály
Ha a paraméterek és eredmények stabilan sémázhatók, készíts eszközt; ha az eljárás sok kontextusos tudást igényel, adj skillt ellenőrzött végrehajtóval.
## Hibamódok
A túl általános executor túl széles jogosultságot, a túl sok mikroeszköz pedig rossz kiválasztást okoz.
## Kapcsolatok
A képességtaxonómiára épül, a tool szerződés és biztonsági határ konkretizálja.
## Ellenőrzés
Mérd a helyes kiválasztást, a paraméterhibát, a jogosultsági hatókört és a karbantartási költséget mindkét formánál.
