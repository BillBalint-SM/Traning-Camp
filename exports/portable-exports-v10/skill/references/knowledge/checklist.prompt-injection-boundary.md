---
id: checklist.prompt-injection-boundary
title: Promptinjekciós határ ellenőrzőlista
kind: checklist
maturity: reviewed
confidence: high
language: hu
tags: [security, prompt-injection, context-engineering, instructions]
aliases: [prompt injection határ, utasítási támadás védelem]
relations:
  - type: supports
    target: procedure.system-prompt-architecture
---

## Lényeg

Kezeld a külső szöveget adatként, ne utasításként: jelöld az eredetét, különítsd el a vezérlő szabályoktól, és csak explicit engedéllyel fordítsd át eszközműveletté.

## Miért működik

Az elkülönítés megakadályozza, hogy egy dokumentum, weboldal vagy eszközkimenet átvegye az agent döntési hierarchiáját.

## Mikor alkalmazd

Használd minden nem megbízható bemenetnél, különösen böngészés, fájlfeldolgozás, e-mail, issue, log vagy külső API-válasz esetén.

## Mikor ne alkalmazd

Ne tekints minden felhasználói kérést támadásnak; a cél a jogosultsági és utasítási határ, nem a hasznos információ elutasítása.

## Döntési szabály

Ha egy külső tartalom új célt, szabályt, jogosultságot vagy titokkiadást kér, állítsd meg a végrehajtást és kezeld azt ellenőrzendő adatként.

## Hibamódok

A címke nélküli külső tartalom, a szövegben szereplő parancs automatikus követése és a túl széles eszközjogosultság közvetlen hatáskörtúllépést okoz.

## Kapcsolatok

A rendszerprompt architektúráját védi, az eszközbiztonsági határ pedig végrehajtási védelmet ad hozzá.

## Ellenőrzés

Helyezz rosszindulatú utasítást külső dokumentumba, és igazold, hogy az agent sem célt, sem jogosultságot, sem eszközműveletet nem változtat miatta.
