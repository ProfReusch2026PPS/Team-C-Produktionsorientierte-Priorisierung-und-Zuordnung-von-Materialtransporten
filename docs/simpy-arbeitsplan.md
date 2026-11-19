# Arbeitspaket C · SimPy-Modell und Versuchsläufe

**Verantwortlich:** Moritz Spieker  
**Fester Termin:** Abschlusspräsentation am **16.12.2026**

Die Meilensteine folgen der fachlichen Reihenfolge. Die Checklisten zeigen, welche Ergebnisse und Nachweise jeweils vorliegen müssen.

## Meilensteine

- [ ] **M1 · In SimPy einarbeiten.** Ein eigenständiges Übungsmodell mit frei erfundenen Daten ausführen. Zwei Aufträge teilen sich ein Fahrzeug. Start, Ende und Wartezeit sind im Protokoll nachvollziehbar. Die Tests E1 und E2 sind erfüllt.
- [ ] **M2 · Testdaten und Schnittstellen abstimmen.** Viola stellt einen kleinen Projektdatensatz mit zwei Robotinos und zwei konkurrierenden Stationen bereit. Mit Orkun und Viola sind die Eingaben des Planers, das Format der Fahrzeugzuordnung und die Pflichtfelder des Ereignisprotokolls abgestimmt. Das Protokoll enthält mindestens Zeit in Sekunden, Ereignis, Identität, Ressource und Zustandsänderung.
- [ ] **M3 · Ersten Projektablauf simulieren.** Die erste Referenzregel läuft von der Lieferbereitschaft über Zuordnung, Transport und Übergabe bis zum Montageende. Je ein protokollierter Lauf zeigt die rechtzeitige und die verspätete Lieferung (T1 und T2). Fahrzeugpositionen werden für nachfolgende Zuordnungen fortgeschrieben.
- [ ] **M4 · Alle drei Transportregeln integrieren und testen.** Orkuns Regeln sind über dieselbe Schnittstelle aufrufbar. Die Modelltests T3 bis T7 sind durchgeführt. Viola kann die Ereignisprotokolle mit ihrer getrennt aufrufbaren Prüfung kontrollieren.
- [ ] **M5 · Versuchsläufe abschließen und Präsentation vorbereiten.** Basisfall, beide Stressfälle und Sensitivitätsanalyse sind ausgeführt, geprüft und ausgewertet. Eingaben, Parameter und Protokolle stehen Viola zur Prüfung und Orkun zur Auswertung zur Verfügung. Ein kurzer Ablauf für die Präsentation zeigt die Wirkung einer Zuordnung auf die Montage.
- [ ] **M6 · Abschlusspräsentation am 16.12.2026.** Das Team stellt das Simulationsmodell, die Vergleichsergebnisse und die daraus abgeleitete Empfehlung vor.
- [ ] **M7 · Abgabe fertigstellen.** Ein Teammitglied kann die dokumentierten Versuchsläufe aus einem frischen Stand des Repos reproduzieren. Abhängigkeiten, Beispielaufrufe, Eingabedaten, Parameter und erwartete Ausgaben sind nachvollziehbar dokumentiert.

## Einarbeitung mit frei erfundenen Daten

Das Übungsmodell verwendet ein Fahrzeug mit Kapazität eins. Alle Aufträge und Zeiten sind frei gewählt.

| Test | Aufbau | Erwartetes Ergebnis |
| --- | --- | --- |
| **E1 · Simulationszeit** | Auftrag 1 startet bei 0 s und beansprucht das Fahrzeug 10 s. | Das Protokoll zeigt den Start bei 0 s und das Ende bei 10 s. |
| **E2 · Warteschlange und Freigabe** | Auftrag 1 läuft wie in E1. Auftrag 2 wird bei 2 s bereit, benötigt dasselbe Fahrzeug und dauert 5 s. | Auftrag 2 wartet 8 s, startet bei 10 s und endet bei 15 s. Das Fahrzeug bearbeitet höchstens einen Auftrag gleichzeitig. |

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
