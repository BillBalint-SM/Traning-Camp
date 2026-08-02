---
id: checklist.continual-evolution-safety
title: Folyamatos fejlődés biztonsági kapuja
kind: checklist
maturity: reviewed
confidence: medium
language: hu
tags: [safety, evolution, governance]
aliases: [önfejlődés biztonsági határ]
relations:
  - type: supports
    target: procedure.evolution-validation-release-rollback
---

## Lényeg

Követeld meg a jogosultsági határt, adatminimalizálást, elkülönített jelöltkészítést, független validációt, változtatási korlátot, auditot, emberi eszkalációt és rollbacket.

## Miért működik

A több kapu megszakítja azt az utat, amelyen az agent saját hibás visszajelzését önállóan tartós képességgé emelhetné.

## Mikor alkalmazd

Futtasd minden automatikus vagy félautomatikus tudás-, instrukció-, kód- és súlyváltoztatási rendszerben.

## Mikor ne alkalmazd

Ne engedj kivételt gyorsaság miatt magas hatású, személyes adatot vagy külső műveletet érintő változtatásnál.

## Döntési szabály

Az agent javasolhat, de saját változtatását nem validálhatja és nem adhatja ki ugyanazon független kontroll nélkül.

## Hibamódok

Önjóváhagyás, jogosultságnövekedés, naplómérgezés, rejtett perzisztencia és visszagörgethetetlen súlyváltozás súlyos kárt okozhat.

## Kapcsolatok

A kapu a validálási, kiadási és rollback eljárást védi.

## Ellenőrzés

Próbálj meg rosszindulatú trajektóriát, jogosultságbővítést, hamis sikert és rollback-hibát átjuttatni minden kapun.
