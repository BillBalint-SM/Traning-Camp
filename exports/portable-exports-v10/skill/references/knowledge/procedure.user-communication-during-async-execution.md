---
id: procedure.user-communication-during-async-execution
title: Felhasználói kommunikáció aszinkron futás közben
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [async, communication, status, interruption]
aliases: [aszinkron futási tájékoztatás]
relations:
  - type: depends_on
    target: pattern.event-driven-agent-execution
---
## Lényeg
Hosszú futás alatt előre mondd meg a célt, a várható eseményeket, a megszakítás módját és csak állapotváltozáskor küldj rövid, igazolható tájékoztatást.
## Miért működik
A felhasználó így kontrollt kap anélkül, hogy a rendszer zajos, félrevezető haladásjelzéseket küldene.
## Mikor alkalmazd
Külső várakozás, több lépés, háttérmunka vagy emberi jóváhagyásra váró folyamat esetén alkalmazd.
## Mikor ne alkalmazd
Ne ígérj bizonytalan befejezési időt, és ne állíts sikert ellenőrizetlen eszközeredmény előtt.
## Döntési szabály
Jelezz induláskor, lényeges fázisváltáskor, blokkoláskor, megszakításkor és lezáráskor; minden üzenethez adj következő választási lehetőséget, ha kell.
## Hibamódok
A néma futás bizalomvesztést, a túl sűrű státusz pedig zajt és téves kész-érzetet okoz.
## Kapcsolatok
Az eseményvezérelt futásra épül; az aszinkron megszakítás és a státuszjel adja a kontrollt.
## Ellenőrzés
Szimulált hosszú futásban igazold a pontos fázisjelzést, a megszakítás visszaigazolását és a hiba érthető közlését.
