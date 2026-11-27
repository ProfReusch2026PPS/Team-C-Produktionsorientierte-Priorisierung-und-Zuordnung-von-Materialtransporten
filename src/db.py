"""Datenbankverbindung zur MES4-Datenbank. Zugangsdaten kommen aus der Datei .env."""
from pathlib import Path

PROJEKT = Path(__file__).resolve().parent.parent


def lade_env(pfad=PROJEKT / ".env"):
    werte = {}
    if not pfad.exists():
        raise FileNotFoundError(
            "Keine .env gefunden. Kopiere .env.example nach .env und trage die Zugangsdaten ein.")
    for zeile in pfad.read_text(encoding="utf-8").splitlines():
        zeile = zeile.strip()
        if zeile and not zeile.startswith("#") and "=" in zeile:
            k, v = zeile.split("=", 1)
            werte[k.strip()] = v.strip()
    return werte


def verbinden():
    import mariadb  # erst hier importieren, damit andere Module ohne mariadb laufen
    env = lade_env()
    return mariadb.connect(user=env["DB_USER"], password=env["DB_PASSWORD"],
                           host=env["DB_HOST"], database=env["DB_NAME"])
