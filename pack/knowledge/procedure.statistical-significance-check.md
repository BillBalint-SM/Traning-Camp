---
id: procedure.statistical-significance-check
title: Statisztikai szignifikancia ellenőrzése
kind: procedure
maturity: reviewed
confidence: high
language: hu
tags: [evaluation, statistics, significance, sample-size]
aliases: [statisztikailag szignifikáns agent javulása]
relations:
  - type: supports
    target: procedure.agent-evaluation-loop
---
## Lényeg
A javulást hatásmérettel, bizonytalansági intervallummal, megfelelő mintaszámmal és párosított feladateredményekkel értékeld.
## Miért működik
Elválasztja a valós változást a véletlen mintavarianciától, és megmutatja a döntés bizonytalanságát.
## Mikor alkalmazd
Kiadási, modell- vagy promptválasztási döntésnél alkalmazd.
## Mikor ne alkalmazd
Ne tekints alacsony p-értéket önmagában üzletileg jelentős javulásnak.
## Döntési szabály
Előre rögzíts minimális érdemi hatást és szükséges erőt; ugyanazon feladatok páros eredményét használd, amikor lehet.
## Hibamódok
A többszöri próbálkozás, szegmensválogatás és utólagos küszöb hamis pozitív eredményt ad.
## Kapcsolatok
Az agent evaluation loopot támogatja és a baseline természetes varianciáját használja.
## Ellenőrzés
Jelents mintaszámot, hatásméretet, intervallumot, módszert és a sikertelen feladatok eloszlását.
