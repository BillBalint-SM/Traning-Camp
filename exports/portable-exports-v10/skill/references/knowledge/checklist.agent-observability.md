---
id: checklist.agent-observability
title: Agent megfigyelhetőség ellenőrzőlista
kind: checklist
maturity: reviewed
confidence: high
language: hu
tags: [evaluation, observability, traces, metrics, agent]
aliases: [agent observability, agent megfigyelhetőség]
relations:
  - type: supports
    target: procedure.agent-evaluation-loop
---

## Lényeg

Gyűjts célazonosítót, kontextusméretet, modell- és eszközválasztást, hívási időt, költséget, hibakategóriát, eredménybizonyítékot és emberi beavatkozási pontot.

## Miért működik

Az agent hibája legtöbbször egy döntési láncban keletkezik; trace nélkül csak a végső rossz válasz látszik, az ok nem.

## Mikor alkalmazd

Használd minden éles vagy értékes kísérleti agentnél, különösen eszközhívás, hosszú futás és autonóm iteráció esetén.

## Mikor ne alkalmazd

Ne naplózz érzékeny nyers tartalmat, titkot vagy személyes adatot diagnosztikai címkével; az observability adatkezelési határ is.

## Döntési szabály

Minden jelhez határozd meg, milyen döntést fog támogatni, meddig őrzöd, ki fér hozzá és hogyan távolítod el vagy anonimizálod.

## Hibamódok

A csak token- és késleltetésmérés nem mutatja a helytelen eszközválasztást, a teljes nyers log pedig adatvédelmi kockázatot és zajt teremt.

## Kapcsolatok

Az értékelési hurok és az ablakos kísérlet elemzéséhez ad bizonyítékot.

## Ellenőrzés

Egy hibás futásból a trace alapján megkülönböztethető legyen a rossz kontextus, a rossz modellválasztás, a rossz eszközhívás és a rossz sikerellenőrzés.
