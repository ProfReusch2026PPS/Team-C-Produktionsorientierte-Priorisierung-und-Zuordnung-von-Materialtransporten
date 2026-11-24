# Arbeitspaket C · SimPy-Modell und Versuchsläufe

**Verantwortlich:** Moritz Spieker  
**Fester Termin:** Abschlusspräsentation am **16.12.2026**

Die Meilensteine folgen der fachlichen Reihenfolge. Die Checklisten zeigen, welche Ergebnisse und Nachweise jeweils vorliegen müssen.

## Meilensteine

- [x] **M1 · In SimPy einarbeiten.** Abgeschlossen am 24.11.2026. Die lokalen Läufe E1 und E2 zeigen Transportbeginn, Ankunft, Wartezeit und Fahrzeugfreigabe.
- [ ] **M2 · Testdaten und Schnittstellen abstimmen (nächster Meilenstein).** Viola stellt einen kleinen Projektdatensatz mit zwei Robotinos und zwei konkurrierenden Stationen bereit. Mit Orkun und Viola sind die Eingaben des Planers, das Format der Fahrzeugzuordnung und die Pflichtfelder des Ereignisprotokolls abgestimmt. Das Protokoll enthält mindestens Zeit in Sekunden, Ereignis, Identität, Ressource und Zustandsänderung.
- [ ] **M3 · Ersten Projektablauf simulieren.** Die erste Referenzregel läuft von der Lieferbereitschaft über Zuordnung, Transport und Übergabe bis zum Montageende. Je ein protokollierter Lauf zeigt die rechtzeitige und die verspätete Lieferung (T1 und T2). Fahrzeugpositionen werden für nachfolgende Zuordnungen fortgeschrieben.
- [ ] **M4 · Alle drei Transportregeln integrieren und testen.** Orkuns Regeln sind über dieselbe Schnittstelle aufrufbar. Die Modelltests T3 bis T7 sind durchgeführt. Viola kann die Ereignisprotokolle mit ihrer getrennt aufrufbaren Prüfung kontrollieren.
- [ ] **M5 · Versuchsläufe abschließen und Präsentation vorbereiten.** Basisfall, beide Stressfälle und Sensitivitätsanalyse sind ausgeführt, geprüft und ausgewertet. Eingaben, Parameter und Protokolle stehen Viola zur Prüfung und Orkun zur Auswertung zur Verfügung. Ein kurzer Ablauf für die Präsentation zeigt die Wirkung einer Zuordnung auf die Montage.
- [ ] **M6 · Abschlusspräsentation am 16.12.2026.** Das Team stellt das Simulationsmodell, die Vergleichsergebnisse und die daraus abgeleitete Empfehlung vor.
- [ ] **M7 · Abgabe fertigstellen.** Ein Teammitglied kann die dokumentierten Versuchsläufe aus einem frischen Stand des Repos reproduzieren. Abhängigkeiten, Beispielaufrufe, Eingabedaten, Parameter und erwartete Ausgaben sind nachvollziehbar dokumentiert.

## Einarbeitung mit frei erfundenen Daten

Die lokalen Testläufe am 24.11.2026 verwendeten SimPy 4.1.2 und frei gewählte Zeiten. Ein Transport dauerte im Grundfall 42 s (10 s Leerfahrt, 12 s Beladen und 20 s Lastfahrt).

| Test | Aufbau | Beobachtung im Konsolenprotokoll |
| --- | --- | --- |
| **E1 · Simulationszeit** | Ein Robotino fährt bei 0 s los. | Das Beladen beginnt bei 10 s, die Lastfahrt bei 22 s. Die Box erreicht die Station bei 42 s. |
| **E2 · Warteschlange und Freigabe** | Ein Robotino bedient A, B und C nach FIFO. Die Aufträge sind bei 0 s, 15 s und 20 s bereit. | A fährt von 0 bis 42 s. B startet bei 42 s nach 27 s Wartezeit. C startet bei 84 s nach 64 s Wartezeit und kommt bei 126 s an. |

### Weitere Übungstests

| Versuch | Beobachtung |
| --- | --- |
| **FIFO und feste Priorität** | Bei gleicher Freigabe wie in E2 fährt mit Vorrang für C zuerst A, dann C und zuletzt B. C kommt bei 84 s an, unter FIFO bei 126 s. Wird C erst bei 41 s bereit, greift der Vorrang bei der Vergabe bei 42 s ebenfalls. Bei Freigabe von C bei 43 s fährt B bereits. C erreicht die Station dann erst bei 126 s. |
| **Zwei Robotinos** | A und B starten bei 0 s und 15 s. C wird bei 20 s bereit, wartet bis zur Freigabe des ersten Fahrzeugs bei 42 s und kommt bei 84 s an. |
| **Längere Beladung** | Mit einem Robotino, Vorrang für C und 20 s Beladezeit für C erreicht C die Station bei 92 s. Der angenommene Termin bei 90 s wird um 2 s verfehlt. B kommt bei 134 s an. |
| **Leerlauf** | Bei Freigaben von 0 s, 50 s und 100 s starten alle Aufträge sofort. Der Robotino ist von 42 bis 50 s und von 92 bis 100 s frei. Das ergibt 16 s Leerlauf und 126 s Belegung in 142 s Simulationszeit. |

## Projekttests für das SimPy-Modell

Die angegebenen Sekundenwerte dienen als Testeingaben. Für die Versuchsläufe werden bestätigte Anlagenregeln und dokumentierte Zeitparameter verwendet. Zu jedem Test werden der Szenarioaufruf, der relevante Protokollauszug und das Prüfergebnis festgehalten.

| Test | Aufbau | Erwartetes Ergebnis |
| --- | --- | --- |
| **T1 · Rechtzeitige Lieferung** | Der vollständige Materialsatz ist bei 15 s an Station 1. Das Werkstück kommt bei 20 s an. Die Station ist frei und die Vorgänger sind abgeschlossen. | Die Montage beginnt bei 20 s. Der Materialsatz wird genau einmal verbraucht. |
| **T2 · Verspätete Lieferung** | Wie T1, mit Materialankunft bei 25 s und einer Wiederkehr bei 40 s als Testvorgabe. | Bei 20 s werden eine verpasste Bearbeitungsmöglichkeit und die Weiterfahrt protokolliert. Bei 25 s findet kein Montagestart statt. Bei der Wiederkehr um 40 s startet die Montage, wenn ihre Voraussetzungen erfüllt sind. |
| **T3 · Gleichzeitige Ereignisse** | Werkstück und vollständiger Materialsatz kommen beide bei 20 s an. | Die fachlich abgestimmte Ereignisreihenfolge bestimmt eindeutig, ob die Montage bei 20 s beginnen kann. Wiederholungen ergeben denselben Ablauf. |
| **T4 · Fahrzeugbindung** | Zwei Lieferungen werden gleichzeitig bereit, während nur ein Robotino frei ist. | Der Robotino übernimmt jeweils höchstens eine Lieferung. Die andere bleibt bis zur nächsten zulässigen Zuordnung verfügbar. |
| **T5 · Voller Übergabeplatz** | Ein Robotino erreicht einen vollständig belegten Übergabeplatz. | Die Materialbuchung erfolgt erst nach der vorgesehenen Übergaberegel. Die Kapazität wird zu keinem Zeitpunkt überschritten. |
| **T6 · Montagevoraussetzungen** | In zwei getrennten Läufen fehlt bei der Werkstückankunft einmal eine Komponente und einmal der Abschluss eines technischen Vorgängers. | Beim ersten Ankunftsereignis beginnt keine Montage. Die Ursache geht aus dem Protokoll hervor. Ein späterer Montagestart setzt eine zulässige Bearbeitungsmöglichkeit und erfüllte Voraussetzungen voraus. |
| **T7 · Zeitweiser Fahrzeugentzug** | Der Entzug eines Robotinos wird während eines laufenden Transports angefordert. | Der Transport wird abgeschlossen. Der Entzug beginnt erst im freien Zustand. Während der Sperre erhält der Robotino keine neue Lieferung. |
| **T8 · Vergleich und Wiederholbarkeit** | Alle drei Regeln laufen im Basisfall und in beiden Stressfällen. In der Sensitivitätsanalyse werden die Fahrdauern gezielt variiert. Ein Lauf wird mit identischer Konfiguration wiederholt. | Innerhalb jedes Vergleichs gelten dieselben Eingaben und Ressourcen. Wiederholungen mit identischer Konfiguration erzeugen dieselben Ereignisse und Kennzahlen. |

## Versuchsplan und Übergaben

| Versuch | Bedingung |
| --- | --- |
| **Basisfall** | Gleichmäßiger Produktionsbedarf. |
| **Stressfall 1** | Mehrere Stationen benötigen gleichzeitig Material und haben unterschiedlich dringende Bearbeitungsmöglichkeiten. |
| **Stressfall 2** | Ein Robotino wird zeitweise entzogen, sobald er frei ist. |
| **Sensitivitätsanalyse** | Fahrdauern anhand einer dokumentierten Datenunsicherheit variieren. |

Der Hauptvergleich verwendet feste Dauern. Die Szenarien für die Parameterwahl werden von den abschließenden Prüfszenarien getrennt. Je Lauf werden Konfiguration, Transportregel, Ereignisprotokoll und der Zustand offener Vorgänge am Laufende festgehalten.

Moritz führt die Modelltests und Versuchsläufe durch. Viola prüft die erzeugten Protokolle unabhängig, insbesondere auf Mengen- und Kapazitätsverstöße, Vorgängerfolgen und Doppelbindungen. Orkun wertet die Vergleichsläufe aus. Für die Präsentation stehen materialbedingt verpasste Bearbeitungsmöglichkeiten, Montageverzögerungen und Leerfahrtdauer im Vordergrund.
