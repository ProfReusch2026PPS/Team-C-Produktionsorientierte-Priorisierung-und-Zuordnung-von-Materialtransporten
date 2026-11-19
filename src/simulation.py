"""SimPy-Simulation der Materialtransporte mit Ereignisprotokoll.

Aktueller Umfang (Gerüst): Lieferbereitschaft -> Zuordnung -> Leerfahrt -> Beladen ->
Lastfahrt -> Entladen -> Material an Station. Fahrzeugpositionen werden fortgeschrieben.

Noch NICHT enthalten (TODO): Werkstückankünfte, Montage, Komponentenverbrauch,
Weiterfahrt bei Materialmangel, begrenzte Übergabeplätze, Fahrzeugentzug.

ALLE Zahlen in DEMO_* sind erfundene Platzhalter (Szenarioannahmen), keine MES-Werte.

Aufruf:  python -m src.simulation --regel fifo|gesamt|produktion
"""
import argparse
import csv

import simpy

from .db import PROJEKT
from .planer import REGELN

# ---------- Demo-Eingangsdaten (Platzhalter!) ----------
DEMO_FAHRZEUGE = {"R1": "Lager", "R2": "Lager"}
DEMO_FAHRZEITEN = {  # Sekunden, symmetrisch; Platzhalter statt gemessener Fahrzeiten
    ("Lager", "S1"): 40, ("Lager", "S2"): 60, ("S1", "S2"): 30,
}
DEMO_LIEFERUNGEN = [
    {"id": "L1", "bereit": 0, "abholort": "Lager", "ziel": "S1"},
    {"id": "L2", "bereit": 5, "abholort": "Lager", "ziel": "S2"},
    {"id": "L3", "bereit": 10, "abholort": "Lager", "ziel": "S1"},
    {"id": "L4", "bereit": 50, "abholort": "Lager", "ziel": "S2"},
]
BELADEN, ENTLADEN = 10, 10  # Sekunden, Platzhalter


def fahrzeit(a, b):
    if a == b:
        return 0
    return DEMO_FAHRZEITEN.get((a, b), DEMO_FAHRZEITEN.get((b, a)))


class Modell:
    def __init__(self, env, regel, fahrzeuge, lieferungen):
        self.env, self.regel = env, regel
        self.pos = dict(fahrzeuge)
        self.frei = set(fahrzeuge)
        self.offene = []
        self.log = []
        self.trigger = env.event()
        for lf in lieferungen:
            env.process(self.lieferung_bereit(lf))
        env.process(self.dispatcher())

    def protokoll(self, ereignis, identitaet, ressource="", zustand=""):
        self.log.append({"zeit": self.env.now, "ereignis": ereignis, "id": identitaet,
                         "ressource": ressource, "zustand": zustand})

    def anstossen(self):
        if not self.trigger.triggered:
            self.trigger.succeed()

    def lieferung_bereit(self, lf):
        yield self.env.timeout(lf["bereit"])
        self.offene.append(lf)
        self.protokoll("lieferbereit", lf["id"], zustand=f"ziel={lf['ziel']}")
        self.anstossen()

    def dispatcher(self):
        # Neuplanung bei Lieferbereitschaft und Fahrzeugfreigabe (über self.trigger)
        while True:
            yield self.trigger
            self.trigger = self.env.event()
            freie = [(f, self.pos[f]) for f in sorted(self.frei)]
            if not freie or not self.offene:
                continue
            for fz, lf in self.regel(freie, list(self.offene), fahrzeit, self.env.now):
                self.frei.discard(fz)
                self.offene.remove(lf)
                self.protokoll("zuordnung", lf["id"], fz)
                self.env.process(self.transport(fz, lf))

    def transport(self, fz, lf):
        yield self.env.timeout(fahrzeit(self.pos[fz], lf["abholort"]))
        self.pos[fz] = lf["abholort"]
        self.protokoll("ankunft_abholort", lf["id"], fz, f"pos={self.pos[fz]}")
        yield self.env.timeout(BELADEN)
        self.protokoll("beladen", lf["id"], fz)
        yield self.env.timeout(fahrzeit(lf["abholort"], lf["ziel"]))
        self.pos[fz] = lf["ziel"]
        self.protokoll("ankunft_ziel", lf["id"], fz, f"pos={self.pos[fz]}")
        yield self.env.timeout(ENTLADEN)
        self.protokoll("material_an_station", lf["id"], fz, f"station={lf['ziel']}")
        self.frei.add(fz)
        self.protokoll("fahrzeug_frei", fz, fz, f"pos={self.pos[fz]}")
        self.anstossen()


def simuliere(regelname, max_zeit=10_000):
    env = simpy.Environment()
    m = Modell(env, REGELN[regelname], DEMO_FAHRZEUGE, DEMO_LIEFERUNGEN)
    env.run(until=max_zeit)
    return m


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--regel", choices=REGELN, default="fifo")
    args = p.parse_args()
    m = simuliere(args.regel)
    ziel = PROJEKT / "ergebnisse" / f"ereignisprotokoll_{args.regel}.csv"
    with open(ziel, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["zeit", "ereignis", "id", "ressource", "zustand"], delimiter=";")
        w.writeheader()
        w.writerows(m.log)
    for e in m.log:
        print(f"{e['zeit']:>6} s  {e['ereignis']:20s} {e['id']:4s} {e['ressource']:3s} {e['zustand']}")
    print(f"\nOffene Lieferungen am Ende: {len(m.offene)}  ->  Protokoll: {ziel}")


if __name__ == "__main__":
    main()
