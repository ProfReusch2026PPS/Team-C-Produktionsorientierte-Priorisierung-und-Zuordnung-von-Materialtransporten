# Code und Projektstruktur – Team C

Prüfungsprojekt IoT Factory, PPS. Offline-Bearbeitung: Das Projekt liest nur
exportierte MES-Daten und verändert nichts an der Anlage.

## Ordnerstruktur

```
team-c-iot-factory/
├── data/
│   ├── raw/          Rohdaten-Export aus MES4 (unverändert, je Export ein Datumsordner)
│   ├── processed/    bereinigte / abgeleitete Daten (reproduzierbar aus raw erzeugt)
│   └── testdaten/    gemeinsame Testdatensätze (konkurrenz_2rass, testlauf_2026-11-09)
├── docs/             Erläuterungen, u. a. parameter-und-testdaten.md
├── ergebnisse/       Befundregister, Parametertabelle, Ereignisprotokolle, Auswertungen
├── src/
│   ├── db.py             Datenbankverbindung (Zugangsdaten aus .env)
│   ├── export_mes4.py    Export aller MES4-Tabellen nach data/raw/<Datum>/
│   ├── dump_zu_sqlite.py MES-Dumps (.sql) ohne DB-Server nach SQLite/CSV umwandeln
│   ├── datenqualitaet.py automatische Grundprüfungen -> Befundregister
│   ├── parameter.py      Parametertabelle mit Herkunft aus dem letzten Snapshot
│   ├── testdatensatz.py  Testdatensätze erzeugen und laden (lade_testdatensatz)
│   ├── planer.py         Zuordnungsregeln (Regel 1, Regel 2, eigene Regel)
│   ├── simulation.py     SimPy-Simulation mit Ereignisprotokoll
│   └── pruefung.py       unabhängige Prüfung des Ereignisprotokolls
├── .env.example      Vorlage für Zugangsdaten
└── requirements.txt
```

Planung, Simulation und Prüfung sind getrennt aufrufbar (Vorgabe der Aufgabenstellung).

## Einrichtung (einmalig)

Im VS-Code-Terminal im Projektordner:

```
python -m venv .venv
.venv\Scripts\activate          (Windows)
source .venv/bin/activate       (Mac/Linux)
pip install -r requirements.txt
```

Dann `.env.example` kopieren, in `.env` umbenennen und die Zugangsdaten eintragen.
Die `.env` wird nicht mit Git hochgeladen.

## Aufrufe

Alle Befehle aus dem Projektordner, mit aktivierter `.venv`:

```
python -m src.export_mes4 --limit 100    # Verbindungstest (VPN nötig)
python -m src.export_mes4                # kompletter Export
python -m src.dump_zu_sqlite <Ordner mit .sql-Dumps> --csv   # Snapshots umwandeln
python -m src.datenqualitaet             # Befundregister zum neuesten Export
python -m src.parameter <Snapshot .sql>  # Parametertabelle neu erzeugen (zuerst)
python -m src.testdatensatz [<Snapshot .sql>]  # Testdatensätze neu erzeugen (danach)
python -m src.simulation --regel fifo    # Demo-Simulation (fifo | gesamt | produktion)
python -m src.pruefung                   # prüft das letzte Ereignisprotokoll
python -m src.pruefung --selbsttest      # zeigt, dass die Prüfung Fehler erkennt
```

## Stand

- [x] Projektgerüst, Export, Grundprüfungen Datenqualität
- [x] Referenzregeln 1 und 2 (Regel 2 per Enumeration für kleine Fälle)
- [x] Simulationsgerüst Transporte + Ereignisprotokoll, Prüfgerüst
- [x] Testdatensätze und Parametertabelle aus den MES-Daten (siehe docs/parameter-und-testdaten.md)
- [ ] Demo-Daten in simulation.py durch Testdatensatz / Referenzpaket ersetzen
- [ ] Werkstückankünfte, Montage, Weiterfahrt bei Materialmangel modellieren
- [ ] Eigene produktionsorientierte Regel
- [ ] Basisfall, zwei Stressfälle, Sensitivitätsanalyse

Testdaten in Python laden (ohne Rohdaten, direkt aus dem Repo):

```python
from src.testdatensatz import lade_testdatensatz, KONKURRENZ
fahrzeuge, fahrzeit, lieferungen, bedarf = lade_testdatensatz(KONKURRENZ)
```

## Hinweis zu Rohdaten

Die MES-Datenbankabzüge (`.sql`) und daraus erzeugte SQLite-Dateien werden nicht hochgeladen,
weil sie Passwörter enthalten (Tabelle `tblusercontrol`). Jede Person legt sie lokal unter `data/raw/` ab.
