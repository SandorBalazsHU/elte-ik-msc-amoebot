# 🧠 Amoebot Simuláció – Hálózati Algoritmusok Projekt

Ez a projekt az **Eötvös Loránd Tudományegyetem** Informatikai Karának **Programtervező Informatikus MSc** képzésében, a **Hálózati Algoritmusok** tárgy keretében készült. A cél egy **amoebot modell alapú szimulációs környezet** megvalósítása, amelyben az egyszerű robotok (ún. **amoebotok**) különböző viselkedési szabályok alapján mozognak és együttműködnek.

## 🎯 Célkitűzés

A projekt célja, hogy vizsgálható legyen a **decentralizált, lokális szabályokon alapuló robotrendszerek** viselkedése egy diszkrét térben. A szimuláció támogatja:

- különféle mozgásmodellek kipróbálását (pl. random, követéses, kígyó alakú mozgás),
- kapcsolatokon alapuló együttmozgást,
- vizuális megjelenítést és elemzést.

## 🧬 Fő fogalmak

### 🔹 Amoebot modell
Az **Amoebot** modell egy elméleti keretrendszer, melyben az **egyszerű robotok** egy **diszkrét rácson** helyezkednek el (jelen esetben háromszög alapú grid), és:
- csak **lokális információval rendelkeznek** (nem látják a teljes hálózatot),
- **bővülnek és összehúzódnak** a mozgás érdekében,
- **állapotokat** és **irányokat** tárolnak,
- képesek egymással **kommunikálni és kapcsolódni**.

### 🔹 Állapotok
Minden amoebot az alábbi állapotok valamelyikében lehet:
- `ACTIVE`: képes döntést hozni és mozogni,
- `PASSIVE`: nem mozog, csak követ,
- `INACTIVE`: tétlen, nincs viselkedése,
- `ONE_STEP`: egyszeri lépés után passzívvá válik.

### 🔹 Viselkedések
A viselkedést a `BehaviorType` határozza meg:
- `RANDOM`: véletlenszerű mozgás szabad irányba,
- `TO_HEADING`: mozgás egy adott irányba,
- `STAY`: nem mozog,
- `INTELLIGENT`: egyedi, intelligens logika alapján dönt (pl. kígyófej és -test mozgása).

### 🔹 Snake behavior (kígyómozgás)
Az egyik megvalósított intelligens viselkedés egy **kígyó-szerű mozgás**, ahol:
- az első amoebot a „fej”, amely önállóan mozog,
- a többi amoebot a fej előző pozícióit követi időben eltolva,
- vizuálisan egy hullámzó lánc jön létre.

## 🖥️ Futtatás

### 🔧 Szükséges környezet
- Python 3.8+
- `pygame` a grafikus megjelenítéshez

📁 src/
 ├─ amoebot.py           # Az amoebot osztály és működése<br\>
 ├─ triangle_map.py      # Háromszög alapú rács és mozgáslogika<br\>
 ├─ behaviors.py         # Viselkedés típusok és függvények<br\>
 ├─ simulation.py        # A szimulációs motor<br\>
 ├─ config.py            # Paraméterek, sebesség, méretek, stb.<br\>
 └─ ...<br\>