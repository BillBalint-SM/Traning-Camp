---
id: decision-guide.single-or-multi-agent
title: Egy agent vagy több agent
kind: decision-guide
maturity: reviewed
confidence: medium
language: hu
tags: [single-agent, multi-agent, complexity]
aliases: [mikor jobb több agent]
relations:
  - type: depends_on
    target: concept.multi-agent-classification-matrix
---

## Lényeg

Több agent csak akkor indokolt, ha a részfeladatok valóban párhuzamosak, eltérő kontextust igényelnek, vagy független ellenőrzésük többet ér a koordinációs költségnél.

## Miért működik

A döntés megakadályozza, hogy az architekturális látványosság felülírja az egyszerűbb egy-agent harness előnyeit.

## Mikor alkalmazd

Használd minden multi-agent javaslat első kapujaként.

## Mikor ne alkalmazd

Ne válassz több agentet pusztán hosszú feladat, szerepnevek vagy nagy kontextus miatt.

## Döntési szabály

Készíts egy-agent baseline-t; multi-agent csak mérhető minőség-, idő- vagy izolációnyereséggel maradhat.

## Hibamódok

Kommunikációs overhead, hibafelerősítés, redundáns munka és kontextusszinkronizáció ronthatja az eredményt.

## Kapcsolatok

A döntés az osztályozási mátrix explicit dimenzióira épül.

## Ellenőrzés

Azonos modellen és budgeten hasonlítsd össze a sikert, költséget, késleltetést és hibamódokat.
