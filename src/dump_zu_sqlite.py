"""Wandelt MES4-Datenbank-Dumps (.sql aus mysqldump/MariaDB) in SQLite-Dateien und CSVs um.

So braucht ihr keinen MariaDB-Server: SQLite ist in Python eingebaut.
Die Rohdaten (.sql) werden nicht verändert.

Aufruf:
  python -m src.dump_zu_sqlite <dump.sql | Ordner mit Dumps> [--csv]

Ergebnis je Dump: data/processed/snapshots/<dumpname>.sqlite
                  (mit --csv zusätzlich data/processed/snapshots/<dumpname>/<tabelle>.csv)
"""
import argparse
import csv
import re
import sqlite3
from pathlib import Path

from .db import PROJEKT

CREATE_RE = re.compile(r"CREATE TABLE `([^`]+)` \((.*?)\n\)[^;]*;", re.S)
COL_RE = re.compile(r"^\s*`([^`]+)`\s", re.M)
INSERT_RE = re.compile(r"INSERT INTO `([^`]+)`(?: \(([^)]*)\))? VALUES ", re.S)
ESC = {"0": "\0", "n": "\n", "r": "\r", "t": "\t", "Z": "\x1a", "b": "\b"}


def parse_values(s, i):
    """Liest Tupel ab Position i bis zum abschließenden ';'. Gibt (zeilen, neue_pos) zurück."""
    zeilen, n = [], len(s)
    while i < n:
        while s[i] in " \n\r\t,":
            i += 1
        if s[i] == ";":
            return zeilen, i + 1
        assert s[i] == "(", f"Unerwartetes Zeichen {s[i]!r} bei {i}"
        i += 1
        zeile = []
        while True:
            while s[i] == " ":
                i += 1
            if s[i] == "'":
                i += 1
                buf = []
                while True:
                    c = s[i]
                    if c == "\\":
                        buf.append(ESC.get(s[i + 1], s[i + 1]))
                        i += 2
                    elif c == "'":
                        if s[i + 1] == "'":
                            buf.append("'")
                            i += 2
                        else:
                            i += 1
                            break
                    else:
                        j = i
                        while s[j] not in "\\'":
                            j += 1
                        buf.append(s[i:j])
                        i = j
                zeile.append("".join(buf))
            else:
                j = i
                while s[j] not in ",)":
                    j += 1
                tok = s[i:j].strip()
                i = j
                if tok.upper() == "NULL":
                    zeile.append(None)
                else:
                    try:
                        zeile.append(int(tok))
                    except ValueError:
                        try:
                            zeile.append(float(tok))
                        except ValueError:
                            zeile.append(tok)
            if s[i] == ",":
                i += 1
                continue
            if s[i] == ")":
                i += 1
                break
        zeilen.append(zeile)
    return zeilen, i


def lade_dump(pfad):
    text = Path(pfad).read_text(encoding="utf-8-sig", errors="replace")
    schema = {}
    for m in CREATE_RE.finditer(text):
        schema[m.group(1)] = COL_RE.findall(m.group(2))
    daten = {t: [] for t in schema}
    pos = 0
    while True:
        m = INSERT_RE.search(text, pos)
        if not m:
            break
        zeilen, pos = parse_values(text, m.end())
        daten.setdefault(m.group(1), []).extend(zeilen)
    return schema, daten


def schreibe_sqlite(schema, daten, ziel):
    ziel.parent.mkdir(parents=True, exist_ok=True)
    if ziel.exists():
        ziel.unlink()
    con = sqlite3.connect(ziel)
    for t, cols in schema.items():
        con.execute(f'CREATE TABLE "{t}" ({", ".join(f"[{c}]" for c in cols)})')
        if daten.get(t):
            con.executemany(f'INSERT INTO "{t}" VALUES ({",".join("?" * len(cols))})', daten[t])
    con.commit()
    con.close()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("quelle", type=Path)
    p.add_argument("--csv", action="store_true")
    args = p.parse_args()
    dumps = sorted(args.quelle.glob("*.sql")) if args.quelle.is_dir() else [args.quelle]
    for d in dumps:
        schema, daten = lade_dump(d)
        name = re.sub(r"[^\w.-]+", "_", d.stem)
        ziel = PROJEKT / "data" / "processed" / "snapshots" / f"{name}.sqlite"
        schreibe_sqlite(schema, daten, ziel)
        if args.csv:
            ordner = ziel.with_suffix("")
            ordner.mkdir(exist_ok=True)
            for t, cols in schema.items():
                with open(ordner / f"{t}.csv", "w", newline="", encoding="utf-8") as f:
                    w = csv.writer(f, delimiter=";")
                    w.writerow(cols)
                    w.writerows(daten.get(t, []))
        nichtleer = sum(1 for t in schema if daten.get(t))
        print(f"{d.name}: {len(schema)} Tabellen ({nichtleer} mit Daten) -> {ziel.name}")


if __name__ == "__main__":
    main()
