---
id: pattern.sessionless-coding-agent
title: Session nélküli coding agent
kind: pattern
maturity: reviewed
confidence: high
language: hu
tags: [coding-agent, sessionless, repository, state]
aliases: [session nélküli coding agentet]
relations:
  - type: depends_on
    target: principle.code-as-meta-capability
---

## Lényeg

A coding agent minden futást a repository aktuális állapotából, instrukcióiból és ellenőrzési bizonyítékaiból rekonstruáljon, ne rejtett beszélgetési memóriára építsen.

## Miért működik

A fájlok, Git-állapot és tesztek megosztható, visszaolvasható állapotot adnak sessionök és modellek között.

## Mikor alkalmazd

Hosszú, megszakítható, több agent által folytatható vagy auditálható fejlesztésnél alkalmazd.

## Mikor ne alkalmazd

Ne tekintsd a repositoryt teljes feladatállapotnak, ha a külső rendszer vagy jóváhagyás aktuális állapota nincs benne.

## Döntési szabály

Induláskor olvasd vissza a branch, HEAD, worktree, instrukció és tesztállapotot; minden fontos döntést tartós artefaktumba vagy commitba rögzíts.

## Hibamódok

A korábbi chatre épülő feltételezés elavult branchből, elveszett indokból vagy megismételt munkából eredő hibát okoz.

## Kapcsolatok

A kód metaképességére épül; a coding workflow és a hibavisszaállítás használja az explicit állapotot.

## Ellenőrzés

Új sessionben, előzmény nélkül legyen rekonstruálható a cél, a változás, a jelenlegi gate és a következő biztonságos lépés.
