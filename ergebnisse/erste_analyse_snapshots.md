# Erste Analyse der MES-Snapshots vom 09.11.2026 (Team C)

Quelle: Ordner `MES_database_snapschots` (6 MariaDB-Dumps, 15:16 bis 15:57 Uhr, plus Readme).
Umwandlung ohne Datenbankserver: `python -m src.dump_zu_sqlite <Ordner> --csv`
→ `data/processed/snapshots/*.sqlite` und CSVs. Rohdaten bleiben unverändert.

Stand: erster Durchgang, noch nicht von einer zweiten Person geprüft.

## Was im Testlauf passiert ist

| Auftrag | Art | Inhalt | Start → Ende |
|---|---|---|---|
| 9176 | Produktion (WPNo 1000) | 1 Produkt | 15:07:48 → 15:54:32 |
| 9178 | Produktion (WPNo 1000) | 2 Produkte | 15:08:29 → 15:55:34 |
| 9177 | Kommissionierung RASS1 | 6 Positionen (Main PCB + Display, je 3×) | 15:09:15 → 15:17:47 |
| 9179 | Kommissionierung RASS2 | 6 Positionen (Analog + Gyroscope, je 3×) | 15:24:23 → 15:34:58 |
| 9180 | Kommissionierung RASS3 | 3 Positionen (Front Cover, 3×) | 15:39:34 → 15:45:09 |

Route je Produkt (aus `tblfinstep`): ASRS32 (1) → **RASS1** (2) → Messen (3) → **RASS2** (4) →
Kamera-Check (5) → **RASS3** (6) → Funktionstest (7) → Label (14) → Ausgabe (11) → ASRS32 (1).

## Befunde, die für Team C wichtig sind

1. **Die Montage wartet sichtbar auf Material.** Jede Montagestation beginnt erst wenige
   Sekunden nach „store box to target“ für ihre Box:
   - RASS1: Box gebucht 15:17:44 → erste Montage 15:17:56
   - RASS2: Box gebucht 15:34:58 → erste Montage 15:35:31 (Produkt 9176 war seit 15:22:52 mit dem Messen fertig)
   - RASS3: Box gebucht 15:45:09 → erste Montage 15:46:07
   Von den rund 47 Minuten Durchlaufzeit je Produkt ist nur ein kleiner Teil Bearbeitung.
   *Vorsicht:* Ob die Werkstücke in dieser Zeit weitergefahren sind oder gewartet haben, ist in `tblfinstep` nicht sichtbar.

2. **Die Kommissionierung läuft nacheinander.** Der Kommissionierauftrag für die nächste
   Station wird erst angelegt, wenn der vorherige fertig gebucht ist: 9179 um 15:17:57,
   10 s nach dem Ende von 9177; 9180 um 15:35:05, 7 s nach dem Ende von 9179.
   Das ist eine mögliche Hauptursache der Wartezeiten. Die Kommissionierung selbst ist eher Thema von Team A, beeinflusst aber unsere Lieferbereitschaft.

3. **Pro Station wird eine Zielbox geliefert, nicht eine Box pro Bauteil.** Beispiel 9179:
   Zielbox 18 hat 6 reservierte Fächer (O9179.1 bis .6). Die Bauteile werden aus Quellboxen
   (3, 4, 21, 26) umgepackt. Ablauf: Boxlager ASRS20 (17) → Robotino →
   Kommissionierplatz PICKSORT (19) → Robotino → Boxpuffer der RASS (2/4/6).

4. **Robotinos:** Die Stammdaten (`tblresource`) enthalten 6 Robotinos (ID 20 bis 25). Am 09.11.
   haben nur **24 und 25** Statusmeldungen geliefert (`tblmachinereport`: Busy, Auto/Manuell, Fehler).
   20 bis 23 haben nur einen Eintrag um 11:33. Wahrscheinlich waren also 2 Fahrzeuge aktiv; bitte im Labor bestätigen.

## Datenlücken (für das Befundregister)

| Befund | Quelle | Folge fürs Modell |
|---|---|---|
| `TransportTime` ist in allen 838 Schrittdefinitionen 0 | `tblstepdef` | Fahrzeiten sind nicht im MES hinterlegt → Messung oder Szenarioannahme |
| „store box to target“ hat Start = Ende (Dauer 0 s) | `tblfinstep` | Das ist nur eine Buchung; die Fahrt selbst wird nicht protokolliert |
| Kein Robotino in den Schritten: `ResourceID` = Zielstation | `tblfinstep` | Welches Fahrzeug welche Lieferung gefahren hat, ist nicht direkt ablesbar |
| Robotino-Status nur als Busy/Idle-Wechsel, ohne Auftrag und Position | `tblmachinereport` | Fahrdauern lassen sich höchstens grob abschätzen |
| Boxstandorte nur als Momentaufnahme (auch Box auf Robotino, z. B. Box 3 auf 25 um 15:21:46) | `tblbufferpos` | Laut Readme werden Änderungen nicht gespeichert → keine Bewegungshistorie |
| Wartende/umlaufende Werkstücke nicht protokolliert | `tblfinstep`, `tblcarrier` | Ob ein Werkstück wegen Materialmangel weitergefahren ist, bleibt offen |

## Offene Fragen an das Labor

- Waren am 09.11. nur die Robotinos 24 und 25 im Einsatz?
- Gibt es Fahrzeiten oder Robotino-Logs außerhalb des MES, z. B. in der Fleet-Software?
- Wie viele Boxplätze hat der Puffer je RASS? In `tblbuffer` ist je Station ein Puffer vom Typ „Box“ hinterlegt.
- Haben die Werkstücke vor RASS2 und RASS3 gewartet oder sind sie im Kreis gefahren?
