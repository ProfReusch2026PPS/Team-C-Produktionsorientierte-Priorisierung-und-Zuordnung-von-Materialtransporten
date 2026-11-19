"""Automatische Grundprüfungen der Datenqualität für einen Export.

Schreibt ein Befundregister (ergebnisse/befundregister_<export>.csv) mit den Feldern,
die die Aufgabenstellung verlangt: Prüfregel, geprüfte Datensätze, Anzahl und Anteil
auffälliger Datensätze, Beispielreferenz. Behandlung und Modellfolge tragt ihr von Hand ein.

Das sind nur generische Prüfungen. Fachliche Prüfungen (Zeitplausibilität, fehlende
Referenzen zwischen Tabellen, widersprüchliche Status) ergänzt ihr unten in
FACHLICHE_PRUEFUNGEN, sobald ihr wisst, welche Tabellen und Felder relevant sind.

Aufruf:  python -m src.datenqualitaet [--export data/raw/<Ordner>]
"""
import argparse
from pathlib import Path

import pandas as pd

from .db import PROJEKT


def neuester_export():
    ordner = sorted(p for p in (PROJEKT / "data" / "raw").iterdir() if p.is_dir())
    if not ordner:
        raise SystemExit("Kein Export in data/raw gefunden. Erst python -m src.export_mes4 ausführen.")
    return ordner[-1]


def befund(tabelle, regel, n, auffaellig, beispiel=""):
    return {"Tabelle": tabelle, "Prüfregel": regel, "geprüfte Datensätze": n,
            "auffällig": auffaellig, "Anteil": round(auffaellig / n, 4) if n else 0,
            "Beispielreferenz": beispiel, "Behandlung": "", "Modellfolge": ""}


def generische_pruefungen(name, df):
    out = []
    n = len(df)
    if n == 0:
        return [befund(name, "Tabelle leer", 0, 0)]
    dup = df.duplicated()
    out.append(befund(name, "vollständig doppelte Zeilen", n, int(dup.sum()),
                      str(df[dup].index[0]) if dup.any() else ""))
    erste = df.columns[0]  # Annahme: erste Spalte ist oft der Schlüssel -> prüfen!
    dupk = df[erste].duplicated(keep=False)
    out.append(befund(name, f"doppelter Wert in erster Spalte '{erste}' (Schlüssel?)", n,
                      int(dupk.sum()), str(df.loc[dupk, erste].iloc[0]) if dupk.any() else ""))
    for col in df.columns:
        leer = df[col].isna() | (df[col].astype(str).str.strip() == "")
        if leer.any():
            out.append(befund(name, f"fehlender Wert in '{col}'", n, int(leer.sum()),
                              f"Zeile {df[leer].index[0]}"))
    return out


# Hier fachliche Prüfungen ergänzen, z. B.:
# def pruefe_endzeit_nach_startzeit(tabellen): ...
FACHLICHE_PRUEFUNGEN = []


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--export", type=Path, default=None)
    args = p.parse_args()
    exp = args.export or neuester_export()

    tabellen = {f.stem: pd.read_csv(f, sep=";", low_memory=False) for f in sorted(exp.glob("*.csv"))}
    register = []
    for name, df in tabellen.items():
        register += generische_pruefungen(name, df)
    for pruefung in FACHLICHE_PRUEFUNGEN:
        register += pruefung(tabellen)

    ziel = PROJEKT / "ergebnisse" / f"befundregister_{exp.name}.csv"
    pd.DataFrame(register).to_csv(ziel, sep=";", index=False, encoding="utf-8-sig")
    print(f"{len(tabellen)} Tabellen geprüft, {len(register)} Befunde -> {ziel}")


if __name__ == "__main__":
    main()
