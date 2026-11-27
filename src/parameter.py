"""Parametertabelle für die Simulation, jeweils mit Herkunft.

Herkunftstypen wie im README von Team C: MES-Wert, Ableitung, Beobachtung, Szenarioannahme.

Aufruf:
  python -m src.parameter "../MES_database_snapschots/DB_Export_2026.11.09_1557_production_finished.sql"
Ergebnis: ergebnisse/parametertabelle.csv
"""
import argparse
import csv
from pathlib import Path

import pandas as pd

from .db import PROJEKT
from .dump_zu_sqlite import lade_dump

ZIEL = PROJEKT / "ergebnisse" / "parametertabelle.csv"
PROXY = PROJEKT / "ergebnisse" / "lieferzeit_proxy_kommissionierauftraege.csv"
RASS = {2: "RASS1", 4: "RASS2", 6: "RASS3"}
MONTAGE_OPS = [320, 321, 322, 323, 324, 325, 420]   # ohne 215 (Boxbuchung) und Demontage (326-330)
MAX_SCHRITT = 3600                                   # Befundregister: Schritte > 1 h als Ausreißer
PRODUKT_WPNO = 1000                                  # Produkt des Testlaufs 09.11. (Aufträge 9176, 9178)


def tabelle(schema, daten, name):
    return pd.DataFrame(daten[name], columns=schema[name])


def zeile(parameter, wert, einheit, q1, q3, n, typ, quelle, bereinigung, hinweis=""):
    return {"parameter": parameter, "wert": wert, "einheit": einheit,
            "q1": q1, "q3": q3, "n": n, "herkunft": typ, "quelle": quelle,
            "bereinigung": bereinigung, "hinweis": hinweis}


def q(s):
    return round(s.median()), round(s.quantile(.25)), round(s.quantile(.75)), len(s)


def berechne(dump):
    schema, daten = lade_dump(dump)
    st = tabelle(schema, daten, "tblfinstep")
    st = st[st.Start.notna() & st.End.notna() & (st.Start != "") & (st.End != "")].copy()
    st["s"], st["e"] = pd.to_datetime(st.Start), pd.to_datetime(st.End)
    st["dauer"] = (st.e - st.s).dt.total_seconds()
    st = st[(st.dauer >= 0) & (st.dauer <= MAX_SCHRITT)]
    zeitraum = f"{st.s.min():%d.%m.%Y} bis {st.s.max():%d.%m.%Y}"
    out = []

    # Montagedauer je Werkstück und Station
    m = st[st.ResourceID.isin(RASS) & st.OpNo.isin(MONTAGE_OPS) & (st.WPNo == PRODUKT_WPNO)]
    g = m.groupby(["ONo", "OPos", "ResourceID"]).agg(
        s=("s", "min"), e=("e", "max"),
        p=("OpNo", lambda x: (x == 320).any()), v=("OpNo", lambda x: (x == 321).any())).reset_index()
    g = g[g.p & g.v]
    g["dauer"] = (g.e - g.s).dt.total_seconds()
    for rid, name in RASS.items():
        d = g[g.ResourceID == rid].dauer
        w, a, b, n = q(d)
        out.append(zeile(f"montagedauer_{name}", w, "s", a, b, n, "Ableitung",
                         f"tblfinstep, ResourceID {rid}, nur WPNo {PRODUKT_WPNO}: 'place cover' bis Ende 'move part to pallet', {zeitraum}",
                         f"andere Arbeitsplanvarianten ausgeschlossen; Schritte < 0 oder > 1 h entfernt; "
                         f"{int((d > 300).sum())} Durchläufe > 300 s (einzelne lange Schritte, vermutlich Störungen) im Median enthalten",
                         "Median robust gegen Ausreißer; Q3 als obere Variante nutzbar"))

    # Kommissionierung
    k = st[st.OpNo == 220]
    w, a, b, n = q(k.dauer)
    out.append(zeile("kommissionierzeit_je_position", w, "s", a, b, n, "MES-Wert",
                     f"tblfinstep OpNo 220 'prepare a box for comming orders', Ist-Dauer, {zeitraum}",
                     "Schritte > 1 h entfernt",
                     "reine Bearbeitungszeit; zwischen den Positionen liegen Wartezeiten (z. B. auf Quellboxen). Für die Lieferbereitschaft daher anlage_bis_box_bereit verwenden, nicht Positionen × Wert"))
    fo = tabelle(schema, daten, "tblfinorder").set_index("ONo")
    ka = k.groupby("ONo").agg(e=("e", "max")).join(fo[["PlannedStart"]])
    ka["d"] = (ka.e - pd.to_datetime(ka.PlannedStart)).dt.total_seconds()
    w, a, b, n = q(ka.d)
    out.append(zeile("anlage_bis_box_bereit", w, "s", a, b, n, "Ableitung",
                     "tblfinorder PlannedStart bis letztes Ende OpNo 220 je Kommissionierauftrag",
                     "keine", "Lieferbereitschaft; hängt an der Auftragsfreigabe (Thema Team A)"))

    # Lieferzeit / Fahrzeit
    p = pd.read_csv(PROXY)
    for rid, name in RASS.items():
        w, a, b, n = q(p[p.res == rid].liefer_s)
        out.append(zeile(f"fahrzeit_PICKSORT_{name}", w, "s", a, b, n, "Szenarioannahme",
                         "Ableitung aus lieferzeit_proxy_kommissionierauftraege.csv: Box fertig (OpNo 220) bis gebucht (OpNo 215)",
                         "keine; Median statt Mittelwert wegen Ausreißern bis 7477 s",
                         "enthält Warten auf Fahrzeug und Übergabe -> Obergrenze der Fahrt; symmetrisch auch als Leerfahrt"))
    w, a, b, n = q(p.liefer_s)
    out.append(zeile("fahrzeit_sensitivitaet", w, "s", a, b, n, "Szenarioannahme",
                     "wie oben, alle Stationen", "keine", "für die Sensitivitätsanalyse: Q1 und Q3 als untere/obere Variante"))
    out.append(zeile("beladen_entladen", 0, "s", "", "", "", "Szenarioannahme",
                     "'store box to target' hat im Median 0 s (nur Buchung)", "", "in der Fahrzeit enthalten"))

    # Robotinos und Übergabeplätze
    res = tabelle(schema, daten, "tblresource")
    rob = res[res.Description.str.contains("Robotino", na=False)]
    out.append(zeile("robotinos_registriert", len(rob), "Stück", "", "", "", "MES-Wert",
                     f"tblresource, IDs {', '.join(map(str, rob.ResourceID))}", "", "Stammdaten, nicht alle im Einsatz"))
    out.append(zeile("robotinos_aktiv", 2, "Stück", "", "", "", "Beobachtung",
                     "tblmachinereport 09.11.2026: nur 24 und 25 mit laufenden Meldungen", "",
                     "vom Team am 25.11.2026 als plausibel bewertet (2 von 6 gefahren); README verlangt mind. 2 Fahrzeuge"))
    buf = tabelle(schema, daten, "tblbuffer")
    for rid, name in RASS.items():
        b = buf[(buf.ResourceId == rid) & (buf.Description == "Box")].iloc[0]
        out.append(zeile(f"boxplaetze_{name}", int(b.Rows) * int(b.Columns), "Plätze", "", "", "", "MES-Wert",
                         f"tblbuffer ResourceId {rid} 'Box': Rows {b.Rows} × Columns {b.Columns}", "",
                         "Übergabekapazität laut Stammdaten; vom Team am 25.11.2026 als korrekt bewertet"))

    with open(ZIEL, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]), delimiter=";")
        w.writeheader()
        w.writerows(out)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("dump", type=Path)
    for z in berechne(ap.parse_args().dump):
        print(f"{z['parameter']:32s} {str(z['wert']):>5} {z['einheit']:6s} [{z['q1']}–{z['q3']}] n={z['n']}  {z['herkunft']}")
