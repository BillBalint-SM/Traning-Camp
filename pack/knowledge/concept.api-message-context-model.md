---
id: concept.api-message-context-model
title: Üzenetalapú kontextusmodell
kind: concept
maturity: reviewed
confidence: high
language: hu
tags: [context, messages, api, tools]
aliases: [API üzenetkontextus]
relations:
  - type: supports
    target: procedure.system-prompt-architecture
---

## Lényeg

Az agent kontextusa nem egyetlen szöveg, hanem szerep, cél, előzmény, eszközhívás és eszközeredmény szerint tagolt üzenetfolyam.

## Miért működik

A szerepek és események megőrzik, hogy egy állítás utasítás, felhasználói igény, megfigyelés vagy végrehajtási eredmény-e.

## Mikor alkalmazd

Többfordulós, eszközhasználó vagy auditálható futás tervezésekor használd alapmodellként.

## Mikor ne alkalmazd

Ne keverd a megbízhatatlan külső tartalmat a rendszerszintű szabályok közé csak azért, mert ugyanabban a promptban utazik.

## Döntési szabály

Minden új információt a legalacsonyabb indokolt jogosultságú szerephez rendelj, és őrizd meg az eszközeredmény eredetét és időpontját.

## Hibamódok

Az összefűzött, címke nélküli szövegben a modell utasításnak értelmezhet adatot, vagy adatnak korábbi döntést.

## Kapcsolatok

A rendszerprompt architektúrát támogatja; a prompt-injection határ választja el a szabályt az idegen tartalomtól.

## Ellenőrzés

Egy futási naplóban vissza kell vezethetőnek lennie minden modellválasznak a szerepeltetett üzenetekre és eszközeredményekre.
