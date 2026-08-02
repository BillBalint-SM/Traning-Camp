---
id: procedure.continual-improvement-release-loop
title: Folyamatos fejlesztési kiadási hurok
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [improvement, release, rollback, learning]
aliases: [continual improvement release, folyamatos fejlesztési kiadás]
relations:
  - type: depends_on
    target: pattern.experience-driven-improvement
---

## Lényeg

Az operatív tapasztalatot diagnózis, jelölés, javítási hipotézis, értékelés, korlátozott kiadás, megfigyelés és visszavonás zárt hurkában alakítsd tartós képességgé.

## Miért működik

Az élő futásokból származó jel önmagában zajos; a kiadási kapu választja el a tanulságot a véletlen, egyszeri vagy veszélyes adaptációtól.

## Mikor alkalmazd

Használd hosszú távon üzemelő agentnél, ahol ismétlődő hiba, új eszközminta vagy felhasználói visszajelzés fejlesztési jel lehet.

## Mikor ne alkalmazd

Ne engedj automatikus, korlátlan önmódosítást olyan rendszerben, ahol nincs mért baseline, kiadási határ és gyors visszavonási lehetőség.

## Döntési szabály

Csak akkor engedj ki változást, ha a hibahipotézishez ellenőrzött javulás, korlátmutató és visszavonható kiadási egység tartozik.

## Hibamódok

A tapasztalat közvetlen szabállyá emelése túlilleszkedést, a sikertelen kiadás utáni tanulság nélküli rollback pedig ismétlődő hibát eredményez.

## Kapcsolatok

Az értékelési hurok, az observability és az ablációs kísérlet együtt döntik el, hogy a tapasztalat valódi fejlesztést jelent-e.

## Ellenőrzés

Minden kiadott javításhoz visszakereshető legyen a kiinduló jel, a mérési eredmény, az érintett kockázat, a kiadási kör és a rollback eredménye.
