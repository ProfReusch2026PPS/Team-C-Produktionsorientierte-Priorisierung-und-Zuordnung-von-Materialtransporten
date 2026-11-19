"""Exportiert alle MES4-Tabellen unverändert als CSV nach data/raw/<Datum_Uhrzeit>/.

Aufruf:  python -m src.export_mes4 [--limit N] [--nur tabelle1 tabelle2]
"""
import argparse
import csv
import datetime as dt

from .db import PROJEKT, verbinden


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=None, help="max. Zeilen je Tabelle")
    p.add_argument("--nur", nargs="*", default=None, help="nur diese Tabellen")
    args = p.parse_args()

    stempel = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    ziel = PROJEKT / "data" / "raw" / stempel
    ziel.mkdir(parents=True, exist_ok=True)

    conn = verbinden()
    cur = conn.cursor()
    cur.execute("SHOW TABLES;")
    tabellen = [r[0] for r in cur.fetchall()]
    if args.nur:
        gewuenscht = {t.lower() for t in args.nur}
        tabellen = [t for t in tabellen if t.lower() in gewuenscht]

    uebersicht = [f"# MES4 Schema-Übersicht", f"Export: {stempel}"
                  + (f", Limit {args.limit} Zeilen/Tabelle" if args.limit else ""), "",
                  "| Tabelle | Zeilen in DB |", "|---|---|"]
    details = []
    for t in tabellen:
        cur.execute(f"SELECT COUNT(*) FROM `{t}`;")
        n = cur.fetchone()[0]
        uebersicht.append(f"| {t} | {n} |")

        cur.execute(f"DESCRIBE `{t}`;")
        details += [f"\n## {t} ({n} Zeilen)\n", "| Spalte | Typ | NULL | Schlüssel | Default |",
                    "|---|---|---|---|---|"]
        details += [f"| {c[0]} | {c[1]} | {c[2]} | {c[3]} | {c[4]} |" for c in cur.fetchall()]

        sql = f"SELECT * FROM `{t}`" + (f" LIMIT {int(args.limit)}" if args.limit else "")
        cur.execute(sql)
        zeilen = cur.fetchall()
        with open(ziel / f"{t}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow([d[0] for d in cur.description])
            w.writerows(zeilen)
        print(f"{t:35s} {n:>8} in DB, {len(zeilen):>8} exportiert")

    (ziel / "schema_uebersicht.md").write_text("\n".join(uebersicht + details) + "\n", encoding="utf-8")
    cur.close()
    conn.close()
    print(f"\nFertig: {ziel}")


if __name__ == "__main__":
    main()
