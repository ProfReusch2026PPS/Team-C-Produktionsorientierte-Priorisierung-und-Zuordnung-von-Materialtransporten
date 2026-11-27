"""Zuordnungsregeln: Welche bereitstehende Lieferung übernimmt welches freie Fahrzeug?

Jede Regel bekommt den zum Entscheidungszeitpunkt bekannten Zustand und gibt eine
Liste von (fahrzeug_id, lieferung) zurück. Die Regeln kennen die Simulation nicht,
sie sind also auch unabhängig davon aufrufbar und testbar.
"""
from itertools import permutations


def leerfahrt(fz_pos, lieferung, fahrzeit):
    return fahrzeit(fz_pos, lieferung["abholort"])


def regel_fifo(freie, offene, fahrzeit, jetzt, zustand=None):
    """Referenzregel 1: Lieferungen in Eingangsfolge, jeweils freies Fahrzeug mit kürzester Leerfahrt."""
    freie = dict(freie)  # {fz_id: position}
    zuordnung = []
    for lf in sorted(offene, key=lambda l: (l["bereit"], l["id"])):
        if not freie:
            break
        fz = min(freie, key=lambda f: (leerfahrt(freie[f], lf, fahrzeit), f))  # Gleichstand: kleinere ID
        zuordnung.append((fz, lf))
        del freie[fz]
    return zuordnung


def regel_gesamt(freie, offene, fahrzeit, jetzt, zustand=None, max_kandidaten=7):
    """Referenzregel 2: gemeinsame Zuordnung mit minimaler gesamter Leerfahrtdauer.

    Vollständige Enumeration aller Zuordnungen. Das ist nur für kleine Fälle machbar;
    deshalb werden höchstens max_kandidaten (älteste) Lieferungen betrachtet.
    Für größere Fälle wäre z. B. die Ungarische Methode passend (scipy.optimize.linear_sum_assignment).
    """
    fz_ids = sorted(f for f, _ in freie)
    pos = dict(freie)
    kandidaten = sorted(offene, key=lambda l: (l["bereit"], l["id"]))[:max_kandidaten]
    k = min(len(fz_ids), len(kandidaten))
    if k == 0:
        return []
    beste, beste_kosten = None, float("inf")
    for fz_auswahl in permutations(fz_ids, k):
        for lf_auswahl in permutations(kandidaten, k):
            kosten = sum(leerfahrt(pos[f], l, fahrzeit) for f, l in zip(fz_auswahl, lf_auswahl))
            if kosten < beste_kosten:
                beste, beste_kosten = list(zip(fz_auswahl, lf_auswahl)), kosten
    return beste


def regel_produktion(freie, offene, fahrzeit, jetzt, zustand=None):
    """Eigene Regel: Auswahl nach erwarteter Produktionswirkung.

    TODO (Team C): Sobald Werkstückankünfte und Montagebedarf modelliert sind, z. B.:
      - Vorrang für Lieferungen, die eine anstehende Bearbeitung ermöglichen
      - Dringlichkeit = nächste Werkstückankunft an Zielstation - (Leerfahrt + Lastfahrt)
      - Leerfahrt als Tiebreaker, Aging-Regel gegen dauerhaft wartende Lieferungen
    Bis dahin: Platzhalter, verhält sich wie Regel 1.
    """
    return regel_fifo(freie, offene, fahrzeit, jetzt, zustand)


REGELN = {"fifo": regel_fifo, "gesamt": regel_gesamt, "produktion": regel_produktion}
