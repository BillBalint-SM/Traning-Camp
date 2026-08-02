---
id: concept.observation-action-interface
title: Megfigyelési és cselekvési felület
kind: concept
maturity: reviewed
confidence: high
language: hu
tags: [agent, observation, action, interface]
aliases: [megfigyelés és akció tér]
relations:
  - type: supports
    target: principle.agent-operating-model
---

## Lényeg

Az agent csak azon a megfigyelési felületen tud helyzetet értelmezni, és csak azon a cselekvési felületen tud hatni, amelyet a rendszer kifejezetten rendelkezésére bocsát.

## Miért működik

A világ állapotának, az engedélyezett műveleteknek és azok visszajelzésének explicit szerződése csökkenti a félreértést és ellenőrizhetővé teszi a döntést.

## Mikor alkalmazd

Új eszköz, GUI, adatforrás vagy együttműködő szereplő bevonásakor előbb ezt a két felületet határozd meg.

## Mikor ne alkalmazd

Ne adj korlátlan megfigyelést vagy írási jogot csak azért, mert egy jövőbeli feladat esetleg igényelheti.

## Döntési szabály

Minden művelethez nevezd meg a szükséges megfigyelést, az előfeltételt, a hatást és az ellenőrizhető eredményt; amihez ez nem írható le, az még nem érett eszköz.

## Hibamódok

A homályos állapot és a túl széles akciótér találgató lépésekhez, jogosulatlan hatásokhoz és nehezen diagnosztizálható hibákhoz vezet.

## Kapcsolatok

Az agent működési modelljét támogatja, és a tool-szerződés konkretizálja a cselekvési oldalát.

## Ellenőrzés

Végigkövethető tesztesetben igazold, hogy minden döntéshez elérhető megfigyelés, minden művelethez pedig mérhető visszajelzés tartozik.
