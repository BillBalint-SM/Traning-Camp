# Tudáscsomag routing

1. Használat előtt ellenőrizd a `manifest.json` fájllistáját, fájlonkénti hash-eit és a teljes csomag digestjét; nem deklarált vagy eltérő fájllal ne dolgozz.
2. Töltsd be az `indexes/l0.json` fájlt, és a kérdés alapján válassz egyetlen tématerületet.
3. Töltsd be csak a kiválasztott terület L1 indexét, majd az ott megjelölt, legkisebb elegendő L2 modult.
4. Kétértelmű kérdésnél nevezd meg az érintett területeket, és kérj pontosítást vagy töltsd be a két szükséges L1 áttekintést.
5. Ha nincs lefedett terület, mondd ki, hogy a csomagban nincs megbízható útvonal; ne egészítsd ki találgatással.
6. A `candidate` vagy `deprecated` állapotú modulokat ne töltsd be alapértelmezésben.
7. A `graph/canonical.json` fájlt csak egy már kiválasztott modul közvetlen kapcsolatainak bővítésére használd; ne töltsd be alapértelmezett kontextusként a teljes gráfot.
8. Csak a csomag deklarált fájljait olvasd; a csomagon kívüli helyeket ne keresd és ne használd.
