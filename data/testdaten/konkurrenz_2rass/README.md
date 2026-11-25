# Testdatensatz „Konkurrenzfall 2 Robotinos / 2 Stationen“ (Team C)

Kleiner Projektdatensatz für Meilenstein M2 aus `docs/simpy-arbeitsplan.md`: **2 Robotinos, 2 Stationen (RASS1, RASS2), die um Transporte konkurrieren.**
Erzeugt mit `python -m src.testdatensatz` aus dem Testlauf vom 09.11. (`../testlauf_2026-11-09/`). Zeiten in Sekunden ab Szenariostart.

## Was echt und was angenommen ist

| Angabe | Herkunft |
|---|---|
| Montagedauer RASS1 132 s, RASS2 120 s | Median der Ist-Montagedauern im Testlauf 09.11. (MES) |
| Robotinos 24 und 25 | MES (am 09.11. aktiv); Start an PICKSORT = Annahme |
| Fahrzeiten PICKSORT ↔ RASS1 123 s, ↔ RASS2 132 s | Annahme aus Lieferzeit-Proxy (wie im Testlauf-Datensatz) |
| Bereitstellungszeiten der 4 Lieferungen, Ankunftszeiten der Werkstücke | **Szenarioannahme** |
| 2 Produktionsaufträge P1, P2 mit je 3 Werkstücken; je Station eine Box pro Auftrag | **Szenarioannahme**, angelehnt an den Testlauf (dort eine Box je Station für 3 Werkstücke) |

## Idee des Falls

- L1 (RASS1, P1) und L2 (RASS1, P2) sind bei 0 s und 10 s bereit. L2 wird erst ab 1300 s gebraucht, ist also nur **Vorrat**.
- L3 (RASS2, P1) ist bei 25 s bereit und wird **ab 300 s** gebraucht. Zu diesem Zeitpunkt sind beide Robotinos schon unterwegs.
- Damit zeigt der Fall, ob eine Regel eine Lieferung für eine **bevorstehende Montage** einem reinen Vorrat vorzieht.

## Handrechnung FIFO (Referenzregel 1)

Annahmen: Beladen/Entladen 0 s (in der Fahrzeit enthalten), Fahrzeug ist am Ziel wieder frei, Neuplanung bei Lieferbereitschaft und Fahrzeugfreigabe.

| t [s] | Entscheidung | Ankunft |
|---|---|---|
| 0 | L1 → R24 | RASS1 bei 123 |
| 10 | L2 → R25 | RASS1 bei 133 |
| 123 | L3 → R24 (Leerfahrt 123 s) | **RASS2 bei 378** |
| 133 | L4 → R25 (Leerfahrt 123 s) | RASS2 bei 388 |

→ Werkstück P1.1 braucht an RASS2 ab 300 s Material, die Box kommt erst bei 378 s: **78 s materialbedingte Verzögerung.**
Referenzregel 2 (gesamte Leerfahrt minimal) entscheidet hier genauso. Mit `regel_fifo` und `regel_gesamt` aus `src/planer.py` nachgerechnet.

Zum Vergleich (Handrechnung, keine fertige Regel): Hält eine Regel R25 bei 10 s für den Vorrat L2 zurück und gibt ihm bei 25 s L3, ist die Box bei 157 s an RASS2, also rechtzeitig.

## In Python laden

```python
from src.testdatensatz import lade_testdatensatz, KONKURRENZ
fahrzeuge, fahrzeit, lieferungen, bedarf = lade_testdatensatz(KONKURRENZ)
```
