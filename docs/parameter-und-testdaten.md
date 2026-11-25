# Parameter und Testdaten (Arbeitspaket A, Stand 25.11.2026)

Diese Seite erklärt, woher die Simulationsparameter und Testdatensätze kommen und welche Entscheidungen dabei getroffen wurden. Herkunftstypen wie im README: **MES-Wert, Ableitung, Beobachtung, Szenarioannahme**.

## Dateien

| Datei | Inhalt | Erzeugt mit |
|---|---|---|
| `ergebnisse/parametertabelle.csv` | Simulationsparameter mit Median, Q1–Q3, n, Herkunft, Quelle, Bereinigung | `python -m src.parameter <letzter Snapshot .sql>` |
| `data/testdaten/konkurrenz_2rass/` | Testdatensatz für M2: 2 Robotinos, 2 konkurrierende Stationen, Handrechnung im README | `python -m src.testdatensatz` |
| `data/testdaten/testlauf_2026-11-09/` | Testlauf 09.11. aus dem MES (Datenbasis und Ist-Referenz) | `python -m src.testdatensatz <letzter Snapshot .sql>` |
| `ergebnisse/befundregister_snapshots_2026-11-09.csv` | Datenbefunde inkl. aller Annahmen dieser Seite | von Hand ergänzt |

Datengrundlage ist der letzte MES-Snapshot vom 09.11.2026, 15:57 Uhr (`tblfinstep` enthält alle Durchläufe 06/2025–11/2026). Neuere Daten liegen nicht vor, die Live-Datenbank war aus VPN und Hochschul-WLAN nicht erreichbar.

## Entscheidungen

**Montagedauern nur für das Produkt WPNo 1000.** An RASS1 streuten die Montagedauern stark (Q3 187 s). Ursache waren vor allem andere Arbeitsplanvarianten, z. B. WPNo 1002 mit langen Lücken zwischen den Schritten (Median rund 49 min je Werkstück). Ausgewertet wird daher nur WPNo 1000, das Produkt des Testlaufs (87 Durchläufe je Station). Ergebnis: RASS1 136 s (Q1–Q3 134–156 s), RASS2 121 s, RASS3 63 s.

**Median statt Mittelwert.** Auch bei WPNo 1000 gibt es einzelne sehr lange Schritte (z. B. ONo 8604 Pos 2: 1282 s an RASS1), vermutlich Störungen. Ihre Ursache ist im MES nicht protokolliert, deshalb werden sie nicht herausgefiltert. Der Median ist dagegen robust. Q3 kann als obere Variante in der Sensitivitätsanalyse dienen.

**Fahrzeiten sind eine Szenarioannahme.** `TransportTime` ist im MES überall 0. Verwendet wird der Median der Zeit „Box fertig kommissioniert → Box an Station gebucht“ aus 229 Kommissionieraufträgen: PICKSORT → RASS1/2/3 = 123/132/141 s, symmetrisch auch als Leerfahrt. Darin stecken Warten auf ein Fahrzeug und Übergabe, die reine Fahrt ist also eher kürzer. Für die Sensitivitätsanalyse: Q1–Q3 über alle Stationen = 102–171 s. Be- und Entladen = 0 s, weil in der Fahrzeit enthalten.

**Robotinos und Boxplätze.** Stammdaten: 6 Robotinos (20–25), 2 Boxplätze je RASS. Am 09.11. haben nur 24 und 25 laufend Statusmeldungen geschickt (20–23 nur eine Meldung um 11:33 Uhr, alles 0). Das Team bewertet am 25.11.2026 beides als plausibel: **2 aktive Robotinos, 2 Boxplätze je RASS.**

**Konkurrenzfall.** Im MES gibt es keinen Fall, in dem zwei Stationen gleichzeitig auf ein Fahrzeug warten (am 09.11. kamen die Lieferungen nacheinander). Bereitstellungs- und Ankunftszeiten in `konkurrenz_2rass` sind deshalb gesetzt (Szenarioannahme), die Dauern stammen aus der Parametertabelle. Ergebnisse dieses Falls sind ein Modelltest, keine Aussage über die reale Anlage.

## Nicht abgedeckt

- Transporte Boxlager (ASRS20) → PICKSORT und Quellboxen: im MES nicht als Ereignis protokolliert, daher nicht enthalten.
- Welcher Robotino welche Box gefahren hat, lässt sich nicht rekonstruieren.
- Bandzeiten zwischen den Stationen: Die Zeitstempel enthalten Wartezeiten, eine reine Bandzeit lässt sich daraus nicht sauber ableiten.
