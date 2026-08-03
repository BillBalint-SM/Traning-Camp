---
id: procedure.hci-evaluation-environment
title: Ember–gép interakciós értékelési környezet
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [evaluation, hci, gui, interaction]
aliases: [HCI eval környezet]
relations:
  - type: depends_on
    target: procedure.evaluation-environment-design
---
## Lényeg
Interaktív agentet vizuális állapottal, eseménysorral, időzítéssel, felhasználói visszajelzéssel és végállapot-verifierrel értékelj.
## Miért működik
A helyes végállapot mellett a kezelési út, a téves kattintás, a megszakítás és a kommunikáció minősége is számít.
## Mikor alkalmazd
GUI-, hang-, mobil- vagy valós idejű agentnél alkalmazd.
## Mikor ne alkalmazd
Ne pontozd csak képernyőkép-hasonlósággal a funkcionális és hozzáférhetőségi viselkedést.
## Döntési szabály
Válaszd szét a feladatsikert, interakciós költséget, hibahatást és felhasználói kontrollt.
## Hibamódok
A törékeny koordináta, változó animáció vagy nem stabil UI-állapot hamis regressziót okoz.
## Kapcsolatok
Az evaluation environment designra épül és a GUI-grounding viselkedését méri.
## Ellenőrzés
Stabil azonosítókkal és állapot-reset után futtasd a normál, megszakított és hibás interakciós utat.
