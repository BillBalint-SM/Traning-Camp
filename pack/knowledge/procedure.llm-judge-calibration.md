---
id: procedure.llm-judge-calibration
title: LLM-bíró kalibrálása
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [evaluation, llm-judge, calibration, rubric]
aliases: [LLM-as-a-judge értékelést kalibráljam]
relations:
  - type: depends_on
    target: decision-guide.metric-selection
---
## Lényeg
Az LLM-bírót explicit rubrikával, vak emberi mintával, sorrendcserével és ismételt futással kalibráld.
## Miért működik
Láthatóvá válik a pozíció-, stílus-, hossz- és modellrokonsági torzítás, valamint a bíró természetes varianciája.
## Mikor alkalmazd
Nem teljesen formalizálható minőség automatikus pontozásakor alkalmazd.
## Mikor ne alkalmazd
Ne használd objektív állapot vagy teszt helyett, ha determinisztikus verifier elérhető.
## Döntési szabály
Csak olyan dimenziót bízz rá, amelyhez példákkal rögzített rubrika és mért emberi egyezés tartozik.
## Hibamódok
A bíró jutalmazhat meggyőző stílust, saját válaszmintát vagy a bemutatási sorrendet.
## Kapcsolatok
A metric selectionre épül; a pairwise ranking gyakori fogyasztója.
## Ellenőrzés
Mérd a bíró–ember egyezést, önkonzisztenciát, sorrendérzékenységet és ismert hibák felismerését.
