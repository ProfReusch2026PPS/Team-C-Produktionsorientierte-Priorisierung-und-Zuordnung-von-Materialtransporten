"""Unabhängige Prüfung eines Ereignisprotokolls. Nutzt nur das Protokoll, nicht die Simulation.

Prüfregeln (Gerüst, erweitern!):
  P1  Jede Lieferung wird höchstens einmal zugeordnet.
  P2  Kein Fahrzeug ist zwei Lieferungen gleichzeitig zugeordnet (Doppelbindung).
  P3  Material erreicht die Station erst nach der Zuordnung.
  P4  Zuordnung erst, nachdem die Lieferung bereit ist.
TODO: Übergabekapazitäten, Mengenbilanz, Vorgängerfolge, Montage nur mit vollständigem Satz.

Aufruf:  python -m src.pruefung [--protokoll pfad] | --selbsttest
"""
import argparse
import csv
from collections import defaultdict

from .db import PROJEKT


def pruefe(log):
    fehler = []
    bereit, zugeordnet, geliefert = {}, defaultdict(list), {}
    belegt = {}  # fahrzeug -> lieferung, die es gerade fährt
    for e in sorted(log, key=lambda e: float(e["zeit"])):
        t, ev, i, r = float(e["zeit"]), e["ereignis"], e["id"], e["ressource"]
        if ev == "lieferbereit":
            bereit[i] = t
        elif ev == "zuordnung":
            zugeordnet[i].append(r)
            if i not in bereit or bereit[i] > t:
                fehler.append(f"P4: {i} zugeordnet bei t={t}, aber nicht bereit")
            if r in belegt:
                fehler.append(f"P2: {r} bei t={t} doppelt gebunden ({belegt[r]} und {i})")
            belegt[r] = i
        elif ev == "material_an_station":
            geliefert[i] = t
            if not zugeordnet.get(i):
                fehler.append(f"P3: {i} geliefert ohne Zuordnung")
        elif ev == "fahrzeug_frei":
            belegt.pop(r, None)
    for i, fz in zugeordnet.items():
        if len(fz) > 1:
            fehler.append(f"P1: {i} mehrfach zugeordnet ({fz})")
    return fehler


def selbsttest():
    """Absichtlich fehlerhafte Protokolle: Die Prüfung muss jeden Fehler erkennen."""
    ok = [
        {"zeit": 0, "ereignis": "lieferbereit", "id": "L1", "ressource": ""},
        {"zeit": 0, "ereignis": "zuordnung", "id": "L1", "ressource": "R1"},
        {"zeit": 50, "ereignis": "material_an_station", "id": "L1", "ressource": "R1"},
        {"zeit": 50, "ereignis": "fahrzeug_frei", "id": "R1", "ressource": "R1"},
    ]
    faelle = {
        "korrekt": (ok, None),
        "Doppelbindung": (ok[:2] + [{"zeit": 1, "ereignis": "lieferbereit", "id": "L2", "ressource": ""},
                                    {"zeit": 1, "ereignis": "zuordnung", "id": "L2", "ressource": "R1"}], "P2"),
        "Zuordnung vor Bereitschaft": ([{"zeit": 0, "ereignis": "zuordnung", "id": "L1", "ressource": "R1"},
                                        {"zeit": 5, "ereignis": "lieferbereit", "id": "L1", "ressource": ""}], "P4"),
        "Lieferung ohne Zuordnung": ([{"zeit": 0, "ereignis": "lieferbereit", "id": "L1", "ressource": ""},
                                      {"zeit": 9, "ereignis": "material_an_station", "id": "L1", "ressource": "R1"}], "P3"),
    }
    alles_ok = True
    for name, (log, erwartet) in faelle.items():
        f = pruefe(log)
        erkannt = (not f) if erwartet is None else any(x.startswith(erwartet) for x in f)
        alles_ok &= erkannt
        print(f"{'OK ' if erkannt else 'FEHLER'}  {name:28s} {f or 'keine Verstöße'}")
    print("\nSelbsttest bestanden." if alles_ok else "\nSelbsttest NICHT bestanden.")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--protokoll", default=str(PROJEKT / "ergebnisse" / "ereignisprotokoll_fifo.csv"))
    p.add_argument("--selbsttest", action="store_true")
    args = p.parse_args()
    if args.selbsttest:
        return selbsttest()
    with open(args.protokoll, encoding="utf-8-sig") as f:
        log = list(csv.DictReader(f, delimiter=";"))
    fehler = pruefe(log)
    print("\n".join(fehler) if fehler else f"Keine Verstöße in {args.protokoll}")


if __name__ == "__main__":
    main()
