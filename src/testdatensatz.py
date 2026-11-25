"""Erstellt den Testdatensatz "Testlauf 09.11.2026" aus dem letzten MES-Snapshot.

Ergebnis (data/testdaten/testlauf_2026-11-09/):
  lieferungen.csv        3 Boxlieferungen PICKSORT -> RASS1/2/3 (Eingabe für Planer und Simulation)
  werkstueckbedarf.csv   wann jedes Werkstück an RASS1/2/3 Material braucht, plus Ist-Montagezeiten
  fahrzeuge.csv          aktive Robotinos und Startposition
  fahrzeiten.csv         Fahrzeiten PICKSORT <-> RASS (Szenarioannahme, NICHT aus dem MES)
  ist_referenz.csv       tatsächliche Zeitpunkte zum Vergleich mit der Simulation

Alle Zeiten in Sekunden ab t0 = Freigabe des ersten Werkstücks (09.11.2026 15:07:48).
Die Datei enthält keine Passwörter oder Benutzerdaten und darf ins Repository.

Aufruf:
  python -m src.testdatensatz "../MES_database_snapschots/DB_Export_2026.11.09_1557_production_finished.sql"
In Python:
  from src.testdatensatz import lade_testdatensatz
  fahrzeuge, fahrzeit, lieferungen, bedarf = lade_testdatensatz()
"""
import argparse
import csv
from datetime import datetime
from pathlib import Path

from .db import PROJEKT

ZIEL = PROJEKT / "data" / "testdaten" / "testlauf_2026-11-09"
PRODUKTION = (9176, 9178)
KOMMISSIONIERUNG = {9177: "RASS1", 9179: "RASS2", 9180: "RASS3"}
STATION_ID = {"RASS1": 2, "RASS2": 4, "RASS3": 6}
# Schritt direkt VOR der jeweiligen RASS laut Arbeitsplan (tblfinstep, StepNo)
VORSCHRITT = {"RASS1": 10, "RASS2": 80, "RASS3": 140}
ERSTER_SCHRITT = {"RASS1": 20, "RASS2": 90, "RASS3": 150}
LETZTER_SCHRITT = {"RASS1": 70, "RASS2": 120, "RASS3": 170}

# Szenarioannahme: Median "Box fertig kommissioniert -> Box an Station gebucht" aus 229
# Kommissionieraufträgen (ergebnisse/lieferzeit_proxy_kommissionierauftraege.csv).
# Enthält Warten auf ein Fahrzeug, Fahrt und Übergabe -> eher Obergrenze für die reine Fahrt.
FAHRZEIT_ANNAHME = {"RASS1": 123, "RASS2": 132, "RASS3": 141}
FMT = "%Y-%m-%d %H:%M:%S"


def _ts(s):
    return datetime.strptime(s, FMT)


def erstelle(dump):
    from .dump_zu_sqlite import lade_dump
    schema, daten = lade_dump(dump)
    cols = schema["tblfinstep"]
    schritte = [dict(zip(cols, z)) for z in daten["tblfinstep"]
                if z[cols.index("ONo")] in (*PRODUKTION, *KOMMISSIONIERUNG) and z[cols.index("Start")]]
    ocols = schema["tblfinorder"]
    auftraege = {z[ocols.index("ONo")]: dict(zip(ocols, z)) for z in daten["tblfinorder"]}

    t0 = min(_ts(s["Start"]) for s in schritte)
    sek = lambda s: int((_ts(s) - t0).total_seconds())

    lieferungen, referenz = [], []
    for ono, station in KOMMISSIONIERUNG.items():
        eigene = [s for s in schritte if s["ONo"] == ono]
        prep = [s for s in eigene if s["OpNo"] == 220]       # prepare a box for comming orders
        store = [s for s in eigene if s["OpNo"] == 215]      # store box to target
        bereit = max(sek(s["End"]) for s in prep)
        gebucht = min(sek(s["Start"]) for s in store)
        lieferungen.append({
            "id": f"L{ono}", "auftrag": ono, "bereit": bereit, "abholort": "PICKSORT", "ziel": station,
            "positionen": len(prep), "auftrag_angelegt": sek(auftraege[ono]["PlannedStart"]),
            "quelle": "tblfinstep OpNo 220 (letztes Ende) / tblfinorder PlannedStart"})
        referenz.append({"objekt": f"L{ono}", "ereignis": "material_an_station", "zeit": gebucht,
                         "uhrzeit": _ts(min(s["Start"] for s in store)).strftime("%H:%M:%S"),
                         "quelle": "tblfinstep OpNo 215 (erste Buchung)"})

    bedarf = []
    for ono in PRODUKTION:
        for opos in sorted({s["OPos"] for s in schritte if s["ONo"] == ono}):
            ws = {s["StepNo"]: s for s in schritte if s["ONo"] == ono and s["OPos"] == opos}
            for station in STATION_ID:
                ab = sek(ws[VORSCHRITT[station]]["End"])
                start = sek(ws[ERSTER_SCHRITT[station]]["Start"])
                ende = sek(ws[LETZTER_SCHRITT[station]]["End"])
                bedarf.append({"werkstueck": f"{ono}.{opos}", "station": station, "bedarf_ab": ab,
                               "ist_montage_start": start, "ist_montage_ende": ende,
                               "montage_dauer": ende - start, "warten_bis_start": start - ab,
                               "quelle": f"tblfinstep StepNo {VORSCHRITT[station]} Ende / "
                                         f"{ERSTER_SCHRITT[station]} Start / {LETZTER_SCHRITT[station]} Ende"})
                referenz.append({"objekt": f"{ono}.{opos}", "ereignis": f"montage_start_{station}",
                                 "zeit": start, "uhrzeit": ws[ERSTER_SCHRITT[station]]["Start"][11:],
                                 "quelle": "tblfinstep"})
    bedarf.sort(key=lambda b: (b["station"], b["bedarf_ab"]))
    referenz.sort(key=lambda r: r["zeit"])

    fahrzeuge = [{"id": f"R{r}", "resource_id": r, "start": "PICKSORT",
                  "quelle": "tblmachinereport: nur 24 und 25 mit Meldungen am 09.11.; Startposition = Annahme"}
                 for r in (24, 25)]
    fahrzeiten = [{"von": "PICKSORT", "nach": st, "sekunden": s,
                   "quelle": "ANNAHME: Median Lieferzeit-Proxy (229 Kommissionieraufträge), symmetrisch"}
                  for st, s in FAHRZEIT_ANNAHME.items()]

    ZIEL.mkdir(parents=True, exist_ok=True)
    for name, zeilen in [("lieferungen", lieferungen), ("werkstueckbedarf", bedarf), ("fahrzeuge", fahrzeuge),
                         ("fahrzeiten", fahrzeiten), ("ist_referenz", referenz)]:
        with open(ZIEL / f"{name}.csv", "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(zeilen[0]), delimiter=";")
            w.writeheader()
            w.writerows(zeilen)
    print(f"t0 = {t0}  ->  {ZIEL}")
    return t0


def _lies(name, ordner):
    with open(ordner / f"{name}.csv", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f, delimiter=";"))


def lade_testdatensatz(ordner=ZIEL):
    """Gibt (fahrzeuge, fahrzeit, lieferungen, bedarf) im Format von planer.py / simulation.py zurück."""
    fahrzeuge = {z["id"]: z["start"] for z in _lies("fahrzeuge", ordner)}
    tab = {}
    for z in _lies("fahrzeiten", ordner):
        tab[(z["von"], z["nach"])] = tab[(z["nach"], z["von"])] = int(z["sekunden"])

    def fahrzeit(a, b):
        if a == b:
            return 0
        if (a, b) in tab:
            return tab[(a, b)]
        raise KeyError(f"Keine Fahrzeit {a} -> {b} im Testdatensatz (nicht angenommen, bitte ergänzen)")

    lieferungen = [{**z, "bereit": int(z["bereit"]), "auftrag": int(z["auftrag"])} for z in _lies("lieferungen", ordner)]
    bedarf = [{**z, **{k: int(z[k]) for k in ("bedarf_ab", "ist_montage_start", "ist_montage_ende",
                                               "montage_dauer", "warten_bis_start")}}
              for z in _lies("werkstueckbedarf", ordner)]
    return fahrzeuge, fahrzeit, lieferungen, bedarf


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("dump", type=Path, help="letzter Snapshot (.sql), z. B. ..._1557_production_finished.sql")
    erstelle(p.parse_args().dump)
