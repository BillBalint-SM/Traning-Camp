---
id: experiment.task-success-baseline
title: Feladatsiker baseline kísérlet
kind: experiment
maturity: reviewed
confidence: high
language: hu
tags: [evaluation, baseline, task-success, experiment]
aliases: [agent baseline mérés]
relations:
  - type: validated_by
    target: procedure.agent-evaluation-loop
---
## Lényeg
Rögzíts változtatás előtti, reprezentatív feladatsiker-baseline-t ugyanazzal a környezettel, adathalmazzal és futási költségkerettel.
## Miért működik
Baseline nélkül a későbbi különbség nem választható el a feladatmix, környezet vagy véletlen ingadozás hatásától.
## Mikor alkalmazd
Modell-, prompt-, tool- vagy orchestration-változás előtt alkalmazd.
## Mikor ne alkalmazd
Ne hasonlíts eltérő környezeti állapotú vagy eltérően pontozott futásokat.
## Döntési szabály
A baseline protokollja legyen fagyasztott, verziózott és újrafuttatható a változtatott rendszerrel.
## Hibamódok
A túl kicsi vagy könnyű minta hamis javulást mutat, a változó környezet pedig összekeveri az okokat.
## Kapcsolatok
Az agent evaluation loop validálja; a statisztikai ellenőrzés értelmezi az eltérést.
## Ellenőrzés
Ismételt baseline futásokból mérd a természetes varianciát és igazold a reprodukálható pontozást.
