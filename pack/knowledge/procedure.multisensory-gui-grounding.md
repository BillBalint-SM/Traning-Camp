---
id: procedure.multisensory-gui-grounding
title: Többérzékű GUI-földelés
kind: procedure
maturity: reviewed
confidence: medium
language: hu
tags: [gui, audio, temporal]
aliases: [animációt és hangot érzékelő gui]
relations:
  - type: supports
    target: procedure.gui-action-grounding
---

## Lényeg

Az állóképet időbeli képsorral, hanggal és strukturált UI-állapottal igazítsd össze közös időbélyegen, majd csak konzisztens jelből cselekedj.

## Miért működik

Animáció, hangjelzés és késleltetett állapotváltozás nem veszik el egyetlen screenshotban.

## Mikor alkalmazd

Használd videólejátszó, játék, távoli asztal vagy hanggal visszajelző alkalmazás esetén.

## Mikor ne alkalmazd

Ne gyűjts mikrofont vagy folyamatos képet a szükségesnél tovább és explicit adatkezelési határ nélkül.

## Döntési szabály

Minden modalitásnak legyen célhoz kötött szerepe, időablaka és elutasítási bizonytalansága.

## Hibamódok

Időbeli elcsúszás, háttérhang, frame drop és modalitáskonfliktus hibás földelést okoz.

## Kapcsolatok

Az eljárás a GUI-akciók vizuális földelését több időbeli jelre bővíti.

## Ellenőrzés

Tesztelj késleltetett hangot, kimaradó képet, konfliktusos jelet és adatminimalizálást.
