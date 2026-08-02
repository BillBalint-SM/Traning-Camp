---
id: procedure.tool-evaluation-environment
title: Eszközhívási értékelési környezet
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [evaluation, tools, environment, contracts]
aliases: [tool calling eval környezet]
relations:
  - type: depends_on
    target: procedure.evaluation-environment-design
---
## Lényeg
Eszközhívást valós szerződéssel, kontrollált állapottal és független utólagos állapotellenőrzéssel értékelj.
## Miért működik
Nemcsak a hívás alakját, hanem a választott eszközt, paramétert, sorrendet és tényleges hatást méri.
## Mikor alkalmazd
API-, MCP-, adatbázis- vagy fájlműveletet végző agentnél alkalmazd.
## Mikor ne alkalmazd
Ne használj olyan fake toolt, amely sikeres választ ad állapotváltozás nélkül.
## Döntési szabály
A verifier a környezet független állapotából döntsön, ne az agent által jelentett eredményből.
## Hibamódok
A mock-alapú siker elfedi a hibás paramétert, idempotenciát és részleges végrehajtást.
## Kapcsolatok
Az evaluation environment designra épül és a tool result verification szerződését méri.
## Ellenőrzés
Tesztelj helyes, tiltott, hiányos, ismételt és részben sikertelen hívást valós állapotváltozással.
