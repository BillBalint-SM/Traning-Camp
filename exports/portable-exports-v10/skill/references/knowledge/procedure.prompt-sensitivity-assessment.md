---
id: procedure.prompt-sensitivity-assessment
title: Promptérzékenység vizsgálata
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [evaluation, prompt, sensitivity, robustness]
aliases: [prompt érzékenységi teszt]
relations:
  - type: supports
    target: procedure.ablation-and-experiment-loop
---
## Lényeg
Mérd, mennyire változik a viselkedés jelentést megtartó szóhasználat-, sorrend-, formátum- és példamódosításokra.
## Miért működik
Feltárja, ha a rendszer valódi feladatmegértés helyett törékeny promptfelszínhez kötődik.
## Mikor alkalmazd
Promptkiadás, modellcsere vagy váratlan regresszió előtt alkalmazd.
## Mikor ne alkalmazd
Ne keverd össze a jelentést változtató követelménymódosítást érzékenységi perturbációval.
## Döntési szabály
Készíts előre definiált, szemantikailag ekvivalens változatcsaládot és mérd az eredmények szórását.
## Hibamódok
A túl kevés variáns vagy utólag kiválasztott példa hamis stabilitást mutat.
## Kapcsolatok
Az ablation loopot támogatja; a system prompt architecture jelöli a vizsgált rétegeket.
## Ellenőrzés
Jelents feladatsiker-, tool- és format-varianciát változatcsoportonként, valamint a legrosszabb esetet.
