"""Erstellt den Testdatensatz "Testlauf 09.11.2026" aus dem letzten MES-Snapshot.

Ergebnis (data/testdaten/testlauf_2026-11-09/):
  lieferungen.csv        3 Boxlieferungen PICKSORT -> RASS1/2/3 (Eingabe für Planer und Simulation)
  werkstueckbedarf.csv   wann jedes Werkstück an RASS1/2/3 Material braucht, plus Ist-Montagezeiten
  fahrzeuge.csv          aktive Robotinos und Startposition
  fahrzeiten.csv         Fahrzeiten PICKSORT <-> RASS (Szenarioannahme, NICHT aus dem MES)
  ist_referenz.csv       tatsächliche Zeitpunkte zum Vergleich mit der Simulation

Zusätzlich (data/testdaten/konkurrenz_2rass/): kleiner Projektdatensatz mit 2 Robotinos und
2 konkurrierenden Stationen, abgeleitet aus dem Testlauf (siehe erstelle_konkurrenz).

Alle Zeiten in Sekunden ab t0 = Freigabe des ersten Werkstücks (09.11.2026 15:07:48).
Die Datei enthält keine Passwörter oder Benutzerdaten und darf ins Repository.

Aufruf:
  python -m src.testdatensatz "../MES_database_snapschots/DB_Export_2026.11.09_1557_production_finished.sql"
In Python:
  from src.testdatensatz import lade_testdatensatz
  fahrzeuge, fahrzeit, lieferungen, bedarf = lade_testdatensatz()            # Testlauf 09.11.
  fahrzeuge, fahrzeit, lieferungen, bedarf = lade_testdatensatz(KONKURRENZ)  # Konkurrenzfall
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


KONKURRENZ = PROJEKT / "data" / "testdaten" / "konkurrenz_2rass"


def _schreibe(ordner, name, zeilen):
    ordner.mkdir(parents=True, exist_ok=True)
    with open(ordner / f"{name}.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(zeilen[0]), delimiter=";")
        w.writeheader()
        w.writerows(zeilen)


def erstelle_konkurrenz(quelle=ZIEL, ziel=KONKURRENZ):
    """Kleiner Projektdatensatz: 2 Robotinos, 2 um Transporte konkurrierende Stationen (RASS1, RASS2).

    Dauern stammen aus dem Testlauf 09.11. (Median je Station) bzw. aus derselben Fahrzeit-Annahme.
    Bereitstellungs- und Bedarfszeitpunkte sind SZENARIOANNAHMEN: Sie sind so gesetzt, dass
    zwei Lieferungen gleichzeitig auf ein Fahrzeug warten und nur eine davon eine bevorstehende
    Montage ermöglicht (die andere erhöht nur den Vorrat).
    """
    from statistics import median
    _, _, _, bedarf_ist = lade_testdatensatz(quelle)
    dauer = {st: int(median(b["montage_dauer"] for b in bedarf_ist if b["station"] == st))
             for st in ("RASS1", "RASS2")}
    q_dauer = "Median Ist-Montagedauer Testlauf 09.11. (werkstueckbedarf.csv)"
    q_szen = "SZENARIOANNAHME"

    lieferungen = [
        {"id": "L1", "auftrag": "P1", "bereit": 0, "abholort": "PICKSORT", "ziel": "RASS1", "positionen": 6,
         "zweck": "Materialsatz P1 für RASS1", "quelle": q_szen},
        {"id": "L2", "auftrag": "P2", "bereit": 10, "abholort": "PICKSORT", "ziel": "RASS1", "positionen": 6,
         "zweck": "Materialsatz P2 für RASS1 (wird erst spät gebraucht = Vorrat)", "quelle": q_szen},
        {"id": "L3", "auftrag": "P1", "bereit": 25, "abholort": "PICKSORT", "ziel": "RASS2", "positionen": 6,
         "zweck": "Materialsatz P1 für RASS2 (wird bald gebraucht)", "quelle": q_szen},
        {"id": "L4", "auftrag": "P2", "bereit": 40, "abholort": "PICKSORT", "ziel": "RASS2", "positionen": 6,
         "zweck": "Materialsatz P2 für RASS2", "quelle": q_szen},
    ]
    # Je Produktionsauftrag 3 Werkstücke; Ankunft an RASS2 im Abstand der RASS1-Montagedauer
    ankunft = {("P1", "RASS1"): 130, ("P1", "RASS2"): 300, ("P2", "RASS1"): 1300, ("P2", "RASS2"): 1500}
    bedarf = []
    for (auftrag, st), t in ankunft.items():
        for i in range(3):
            bedarf.append({"werkstueck": f"{auftrag}.{i + 1}", "station": st,
                           "bedarf_ab": t + i * dauer["RASS1"], "montage_dauer": dauer[st],
                           "quelle": f"bedarf_ab: {q_szen}; montage_dauer: {q_dauer}"})
    bedarf.sort(key=lambda b: (b["bedarf_ab"], b["station"]))

    _schreibe(ziel, "lieferungen", lieferungen)
    _schreibe(ziel, "werkstueckbedarf", bedarf)
    _schreibe(ziel, "fahrzeuge", _lies("fahrzeuge", quelle))
    _schreibe(ziel, "fahrzeiten", [z for z in _lies("fahrzeiten", quelle) if z["nach"] in ("RASS1", "RASS2")])
    print(f"Montagedauern {dauer}  ->  {ziel}")


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

    lieferungen = [{**z, "bereit": int(z["bereit"])} for z in _lies("lieferungen", ordner)]
    zahlen = ("bedarf_ab", "ist_montage_start", "ist_montage_ende", "montage_dauer", "warten_bis_start")
    bedarf = [{**z, **{k: int(z[k]) for k in zahlen if z.get(k) not in (None, "")}}
              for z in _lies("werkstueckbedarf", ordner)]
    return fahrzeuge, fahrzeit, lieferungen, bedarf


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("dump", type=Path, nargs="?",
                   help="letzter Snapshot (.sql), z. B. ..._1557_production_finished.sql; "
                        "ohne Angabe wird nur der Konkurrenz-Datensatz aus dem vorhandenen Testlauf erzeugt")
    args = p.parse_args()
    if args.dump:
        erstelle(args.dump)
    erstelle_konkurrenz()
