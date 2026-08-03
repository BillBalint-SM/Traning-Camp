---
id: checklist.memory-privacy-sanitization
title: Memória adatvédelmi tisztítása
kind: checklist
maturity: reviewed
confidence: high
language: hu
tags: [memory, privacy, logs, retention]
aliases: [memória privacy ellenőrzés]
relations:
  - type: supports
    target: procedure.user-memory-lifecycle
---

## Lényeg

Mielőtt tartós emléket vagy naplót írsz, vizsgáld meg a célhoz kötöttséget, az érzékenységet, a minimalizálást, a megőrzést és a törölhetőséget.

## Miért működik

A korai tisztítás megelőzi, hogy egy hasznosnak tűnő futási nyom később kontrollálatlan személyes adattá váljon.

## Mikor alkalmazd

Profil, beszélgetési kivonat, hibajegy, eszközválasz vagy megfigyelési adat tartósítása előtt alkalmazd.

## Mikor ne alkalmazd

Ne tekintsd a maszkolást egyedüli védelemnek, ha az adatkombinációból azonosítható következtetés marad.

## Döntési szabály

Csak azt őrizd meg, ami meghatározott viselkedéshez kell, és rendelj hozzá tulajdonost, lejáratot, hozzáférési határt és törlési utat.

## Hibamódok

A teljes nyers napló, az örök megőrzés és a nem tesztelt törlési folyamat rejtett adatvédelmi és bizalmi kockázatot teremt.

## Kapcsolatok

A memóriaéletciklust támogatja, az értékelés pedig méri a hibás vagy tiltott felidézést.

## Ellenőrzés

Próbálj jogosultság nélküli lekérdezést, lejárt rekordot és törlési kérést; mindháromnak ellenőrizhető, biztonságos eredményt kell adnia.
