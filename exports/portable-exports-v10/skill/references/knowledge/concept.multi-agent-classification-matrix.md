---
id: concept.multi-agent-classification-matrix
title: Multi-agent osztályozási mátrix
kind: concept
maturity: reviewed
confidence: medium
language: hu
tags: [multi-agent, context, topology]
aliases: [multi agent osztályozási keret]
relations:
  - type: supports
    target: decision-guide.multi-agent-topology-selection
---

## Lényeg

A kollaborációt legalább a kontextus megosztása, a vezérlési topológia, a szerepek, az állapot tulajdonosa és az átadási szerződés szerint osztályozd.

## Miért működik

A mátrix az agentek számánál fontosabb működési különbségeket teszi láthatóvá.

## Mikor alkalmazd

Használd multi-agent architektúra tervezése vagy összehasonlítása előtt.

## Mikor ne alkalmazd

Ne nevezd több-agent rendszernek a puszta párhuzamos modellhívást önálló felelősség és koordináció nélkül.

## Döntési szabály

Minden agenthez rögzíts bemenetet, döntési jogot, írható állapotot, kimenetet és felelőst.

## Hibamódok

Implicit kontextus, kettős tulajdon és homályos topológia duplikációt vagy versenyhelyzetet okoz.

## Kapcsolatok

A fogalom a topológiaválasztás dimenzióit rendszerezi.

## Ellenőrzés

Rajzold fel a kommunikációs és állapotírási éleket, majd keress tulajdonos nélküli vagy többtulajdonosú csomópontot.
