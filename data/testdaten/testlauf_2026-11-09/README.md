# Testdatensatz „Testlauf 09.11.2026“ (Team C)

Erzeugt mit `python -m src.testdatensatz "../MES_database_snapschots/DB_Export_2026.11.09_1557_production_finished.sql"`
aus dem letzten MES-Snapshot. Rohdaten bleiben unverändert. Enthält keine Passwörter.

**Zeitbasis:** Sekunden ab t0 = 09.11.2026 15:07:48 (Freigabe des ersten Werkstücks, Auftrag 9176).

**Inhalt des Testlaufs:** 3 Werkstücke (9176.1, 9178.1, 9178.2), 3 Boxlieferungen (je eine Zielbox pro RASS).

| Datei | Inhalt | Herkunft |
|---|---|---|
| `lieferungen.csv` | Box fertig an PICKSORT (`bereit`) → Ziel-RASS | MES (tblfinstep OpNo 220, tblfinorder) |
| `werkstueckbedarf.csv` | Ab wann jedes Werkstück an RASS1/2/3 Material braucht, Ist-Montagestart/-dauer | MES (tblfinstep) |
| `fahrzeuge.csv` | Robotinos 24 und 25 | MES (tblmachinereport); Startposition **Annahme** |
| `fahrzeiten.csv` | PICKSORT ↔ RASS1/2/3 | **Annahme**: Median Lieferzeit-Proxy aus 229 Kommissionieraufträgen |
| `ist_referenz.csv` | Tatsächliche Zeitpunkte (Material an Station, Montagestart) | MES – zum Vergleich mit der Simulation |

## Spalten (Auswahl)

- `bereit`: Ende des letzten „prepare a box“-Schritts = Box abholbereit
- `auftrag_angelegt`: PlannedStart des Kommissionierauftrags (≈ Anlage; 9177 liegt vor t0 → negativ)
- `bedarf_ab`: Ende des Arbeitsschritts vor der RASS (RASS1: Auslagern StepNo 10, RASS2: Messen StepNo 80, RASS3: Kamera-Check StepNo 140)
- `warten_bis_start`: Montagestart − `bedarf_ab`. **Enthält auch Bandfahrt und Warten hinter anderen Werkstücken**, ist also nicht nur Materialwartezeit.

## Bekannte Grenzen

- Fahrzeiten stehen nicht im MES (`TransportTime` = 0). Die Annahme enthält auch Warten auf ein Fahrzeug und Übergabe → eher Obergrenze. Für die Sensitivitätsanalyse variieren.
- Nur die Lieferung PICKSORT → RASS ist enthalten. Die Fahrten Boxlager (ASRS20) → PICKSORT und die Quellboxen sind im MES nicht als Ereignisse protokolliert.
- Welcher Robotino welche Box gefahren hat, ist nicht rekonstruierbar.
- Beladen/Entladen: in der Fahrzeit-Annahme enthalten → in der Simulation 0 s setzen oder Fahrzeit entsprechend kürzen.

## In Python laden

```python
from src.testdatensatz import lade_testdatensatz
fahrzeuge, fahrzeit, lieferungen, bedarf = lade_testdatensatz()
```
Das Format passt direkt zu `planer.py` (Felder `id`, `bereit`, `abholort`, `ziel`).
