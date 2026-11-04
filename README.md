# Team C: Produktionsorientierte Priorisierung und Zuordnung von Materialtransporten

Prüfungsprojekt **Operations Management in der IoT Factory**

## Team

- Moritz Spieker
- Orkun Yavas
- Viola Fürer

## Projektstatus und fachliche Grundlage

**Es gibt noch keine Implementierung. Das Referenzpaket steht noch aus.** Dieses README beschreibt den vorgesehenen Arbeitsumfang und die Anforderungen; es dokumentiert keine bereits erzielten Ergebnisse, bestandenen Prüfungen oder bestätigten Leistungsverbesserungen.

Fachliche Grundlage ist `Pruefungsprojekte_IoT_Factory_Studierende(1).pdf`, Stand 30. Oktober 2026: Team C auf Seiten 4–5, gemeinsame Anforderungen und Abgaben auf Seiten 6–7 sowie Arbeitsrahmen und Zwischenstände auf Seite 1.

Das angekündigte Referenzpaket soll Daten, Formate, Produktionsabschnitt, feste Umgebungsregeln und ein kleines SimPy-Grundgerüst bereitstellen. Konkrete Datenfelder, Parameter, Stationszahl und Anlagenregeln werden nach dessen Bereitstellung geprüft. Das fachliche Simulationsmodell entwickelt das Team selbst. Ergebnisse oder Code anderer Teams werden nicht benötigt.

Aktuell wird ausschließlich diese `README.md` im Repository-Hauptverzeichnis angelegt. Weitere Dateien, Verzeichnisse, Installationsanweisungen oder ausführbare Beispielaufrufe sind noch nicht vorhanden.

## Projektziel und Abgrenzung

Entwickelt werden soll ein Python-Verfahren, das entscheidet, **welche bereits kommissionierte, bereitstehende Lieferung welches zulässige Robotino-Fahrzeug als Nächstes übernimmt**. Ziel ist, anstehende Bearbeitungsmöglichkeiten der Montage rechtzeitig mit Material zu versorgen. Eine kurze Leerfahrt allein genügt dafür nicht.

Fehlt Material, fährt das Werkstück gemäß Anlagenlogik weiter. Eine Bearbeitungsmöglichkeit kann dadurch entfallen und erst bei einer späteren Wiederkehr erneut entstehen. Die Transportentscheidung muss deshalb an Werkstückankünfte, Vorgängerabschlüsse, Stationsbelegung und verfügbare vollständige Materialsätze gekoppelt werden.

Der Schwerpunkt liegt auf Bedienreihenfolge und Fahrzeugzuordnung. Dabei gelten:

- Boxinhalt, Liefermenge und Bereitstellungszeitpunkt sind vorgegeben und erfüllen bestätigte Satz- und Boxregeln.
- Team C bildet keine Chargen und verändert keine Produktionsfreigaben oder Montageprioritäten.
- Reservierungen, bereits freigegebene Aufträge, begonnene Vorgänge und beauftragte Transporte bleiben bindend.
- Fahrzeugverfügbarkeit und begrenzte Übergabekapazitäten sind einzuhalten.
- Navigation, Kollisionsvermeidung und Ladungsbergung bei Ausfällen gehören nicht zum Umfang.
- Die Bearbeitung erfolgt offline; Änderungen am produktiven System sind nicht vorgesehen.

Aussagen gelten ausschließlich für den dokumentierten Produktionsabschnitt. Änderungen bestätigter Modellgrenzen sind fachlich zu begründen und mit der Lehrperson abzustimmen.

## Datengrundlage und Datenqualität

Jede Lieferung muss zu Produktionsauftrag, Position, Arbeitsschritt, vollständigem Materialsatz und Zielstation nachvollziehbar verknüpft werden. Zu untersuchen sind die relevanten MES-Tabellen und Felder sowie verfügbare Bestands-, Zeit- und Fahrzeugdaten. Eine feste Versorgungsliste enthält die Produktionsreferenzen.

### Vorgesehene Datenprüfung

Geprüft werden Bedeutung, Einheiten und Zeitbezug, fehlende Werte, doppelte Schlüssel, widersprüchliche Statusangaben, Mengen- und Zeitplausibilität sowie fehlende Referenzen und Mehrfachzählungen bei Verknüpfungen.

Jeder Befund wird mit folgenden Angaben dokumentiert:

| Angabe | Inhalt |
| --- | --- |
| Prüfregel | Fachliche und ausführbare Bedingung |
| Umfang | Anzahl geprüfter Datensätze |
| Auffälligkeiten | Anzahl und Anteil auffälliger Datensätze |
| Beispiel | Nachvollziehbare Datensatzreferenz |
| Behandlung | Bereinigung, Ausschluss oder begründete Übernahme |
| Modellfolge | Auswirkung auf Planung, Simulation und Aussagekraft |

Ausführbare Prüfungen und mindestens eine manuelle Datenstichprobe sind vorgesehen. Bereinigungen und Ausschlüsse müssen reproduzierbar sein; Rohdaten bleiben unverändert.

MES-Werte, abgeleitete Werte, ergänzende Beobachtungen und Szenarioannahmen werden klar getrennt. Ein Exportzustand belegt keine historische Bestands- oder Bewegungsfolge. Historische Fahrzeugpositionen und Bewegungen werden nur aus geeigneten Aufzeichnungen rekonstruiert. Zeitstempeldifferenzen sind nicht automatisch reine Fahr- oder Bearbeitungszeiten; Luftlinienentfernungen werden nicht ungeprüft als Fahrdauern verwendet. Datenlücken bleiben auch bei ergänzenden Szenariodaten ausdrücklich dokumentiert.

## Planungsverfahren

Die folgenden drei Regeln werden unter vergleichbaren Bedingungen untersucht:

| Verfahren | Entscheidung |
| --- | --- |
| Referenz 1: Eingangsreihenfolge | Anforderungen in Eingangsreihenfolge bedienen und jeweils das zulässige Fahrzeug mit der kürzesten Leerfahrtdauer zuordnen. |
| Referenz 2: Gemeinsame Zuordnung | Lieferungen und Fahrzeuge gemeinsam mit möglichst geringer gesamter Leerfahrtdauer zuordnen. |
| Eigene produktionsorientierte Regel | Lieferungen und Fahrzeuge anhand ihrer erwarteten Produktionswirkung auswählen und zuordnen. |

Für die eigene Regel soll insbesondere unterschieden werden, ob eine Lieferung eine bevorstehende Bearbeitung ermöglicht oder zunächst nur Vorrat erhöht. Unbegründete Dringlichkeitspunkte ersetzen diesen Produktionsbezug nicht.

Entscheidungsgrößen, zulässige Alternativen, Nebenbedingungen und Entscheidungshorizont werden formal definiert. Als zu begründende Zielhierarchie ist vorgesehen: zuerst geringe materialbedingte Montageverzögerung, anschließend geringer Transportaufwand. Regeln für Gleichstände und lange wartende Lieferungen werden ausdrücklich festgelegt. Die konkrete Ausgestaltung folgt der Daten- und Systemanalyse.

Für einen kleinen Fall werden alle zulässigen Alternativen vollständig enumeriert und mit dem Verfahren verglichen. Eine optimale Einzelentscheidung belegt keinen insgesamt optimalen Anlagenablauf.

## Simulationsanforderungen

Vorgesehen ist eine eigene ereignisdiskrete **SimPy-Simulation** mit mindestens zwei Fahrzeugen und den Montagestationen des vorgegebenen Produktionsabschnitts. Mindestens zwei Stationen konkurrieren um Transportkapazität; die konkrete Stationszahl folgt dem Referenzpaket.

### Produktions- und Transportablauf

Abzubilden sind:

1. Werkstückankünfte, technische Vorgängerbeziehungen, Stationsbelegung, Bearbeitungsdauern und Komponentenbedarfe.
2. Lieferbereitschaft, Zuordnung und Fahrzeugbindung.
3. Leerfahrt, Beladung, Lastfahrt, Entladung und Materialzugang.
4. Montagebeginn, Komponentenverbrauch und Montageende.
5. Weiterfahrt und Wiederkehr bei fehlendem Material nach der vorgegebenen Anlagenlogik.

Montage setzt einen vollständigen Materialsatz in einer zulässigen Box voraus. Fahrzeugpositionen werden fortgeschrieben. Fahrzeuge, Übergabeplätze und weitere Ressourcen bleiben während ihrer Nutzung gebunden.

Bei Materialmangel wird die verpasste Bearbeitungsmöglichkeit protokolliert. Es entsteht dadurch **nicht automatisch ein vor der Station wartendes Werkstück**. Eine verspätete Lieferung muss Montagebeginn und Montageabschluss tatsächlich beeinflussen können. Laufende Vorgängerarbeit und eine belegte Station sind als andere Verzögerungsursachen zu unterscheiden.

Übergabeplätze haben endliche Kapazitäten. Gegebenenfalls vorgegebene Sperrfenster ergänzen diese Grenzen. Lade- und Parkregeln bleiben vorgegeben oder werden ausdrücklich ausgeblendet. Ein zeitweiliger Fahrzeugentzug darf nur im freien Zustand beginnen.

### Ereignisse und Ausführung

Neu geplant wird bei Lieferbereitschaft, Fahrzeugfreigabe sowie relevanten Änderungen von Produktionsbedarf oder Verfügbarkeit, jeweils mit dem dann bekannten Zustand. Beauftragte Transporte bleiben bindend.

Planung, Simulation und Ergebnisprüfung müssen getrennt aufrufbar sein. Die Simulation ermittelt tatsächliche Wartezeiten, Zustandsänderungen und Abschlüsse; sie übernimmt keine geplanten Fertigstellungen als Simulationsergebnis.

Zeitangaben erfolgen in Sekunden. Für gleichzeitige Ereignisse werden eindeutige Regeln festgelegt. Das Ereignisprotokoll enthält Zeit, Ereignis, Identität, Ressource und Zustandsänderung und stellt insbesondere Lieferungen, Werkstückankünfte, Weiterfahrten und Montage gegenüber. Eine Animation ist nicht erforderlich.

Endkriterium und maximale Laufzeit werden vorab definiert. Offene Arbeit, ihr Zustand und Stillstände ohne Fortschritt werden berichtet. Unzulässige Doppelbindungen werden nicht stillschweigend repariert.

## Unabhängige Prüfungen

Die Ergebnisprüfung soll unabhängig vom Planer und getrennt von der Simulation folgende Regeln kontrollieren:

- Mengenbilanz und nachvollziehbarer Komponentenverbrauch.
- Vollständigkeit der Materialsätze und Einhaltung zulässiger Boxinhalte.
- Technische Vorgängerfolge vor Montagebeginn.
- Ressourcen- und Übergabekapazitäten sowie Verfügbarkeitsgrenzen.
- Eindeutige Aufgaben- und Fahrzeugbindung ohne Doppelzuordnung.
- Einhaltung bindender Transporte und Zustandsübergänge einschließlich Weiterfahrt und Wiederkehr.

Absichtlich fehlerhafte Ergebnisse müssen zeigen, dass die Prüfungen Verstöße erkennen. Die Angemessenheit der Modellregeln wird anhand der MES-Unterlagen und bestätigten Anlagenabläufe begründet.

## Vergleichsversuche und Sensitivität

| Versuch | Anforderung |
| --- | --- |
| Basisfall | Gleichmäßiger Produktionsbedarf |
| Stressfall 1 | Gleichzeitig versorgungsbedürftige Stationen mit unterschiedlichen bevorstehenden Bearbeitungsmöglichkeiten |
| Stressfall 2 | Zeitweiliger Fahrzeugentzug; Entzug nur eines freien Fahrzeugs |
| Sensitivitätsanalyse | Unsichere Fahrdauern oder Werkstückankunftszeiten; Bezug zu einer wesentlichen Datenunsicherheit oder Bereinigungsentscheidung der Datenanalyse |

Innerhalb jedes Vergleichs bleiben Eingangsdaten, Abläufe und Ressourcen gleich; geändert werden nur die Entscheidungsregel und ausdrücklich ausgewiesene Parameter. Parameterwahl und abschließende Prüfung erfolgen auf getrennten Szenarien.

Der Hauptvergleich verwendet feste Dauern. Zufällige Dauern sind optional. Werden sie eingesetzt, sind Verteilungen zu belegen oder als Szenarioannahmen zu kennzeichnen; mehrere Wiederholungen und Unsicherheitsangaben sind erforderlich. Die Regeln werden dann mit denselben vorab erzeugten Eingangs- und Dauerverläufen verglichen.

## Kennzahlen und Auswertung

| Bereich | Kennzahlen bzw. Nachweise |
| --- | --- |
| Produktionswirkung | Materialbedingt verpasste Bearbeitungsmöglichkeiten; Verzögerungen von Montagebeginn und Montageabschluss |
| Erledigungsstand | Erledigte und offene Montagevorgänge einschließlich Zustand offener Einheiten |
| Transportaufwand | Leerfahrtdauer, Transportwartezeiten und Fahrzeugbelegung |
| Stationswirkung | Tatsächliche materialbedingte Stationsstillstände, gesondert ausgewiesen |
| Nachvollziehbarkeit | Gemeinsames Zeitprotokoll von Lieferung, Werkstückankunft, Weiterfahrt und Montage |

Reguläres Warten, verpasste Bearbeitungsmöglichkeiten und Verletzungen fester Plantermine werden unterschieden. Verzögerungen werden mit Ursache ausgewiesen. Werkstückverzögerungen sind nicht mit tatsächlichem Stationsstillstand gleichzusetzen. Definitionen, Bezugspunkte und Auswertungszeitraum der Kennzahlen werden dokumentiert.

Eine Verbesserung im Modell belegt keine Verbesserung der realen Anlage. Auch ein Ergebnis ohne nachgewiesene Verbesserung kann bei sauberem Vorgehen methodisch überzeugend sein.

## Meilensteine

Die Aufgabenstellung sieht acht Wochen Bearbeitungszeit vor. Kalendertermine werden nach Bestätigung des Projektstarts ergänzt.

| Zeitpunkt | Geplanter Zwischenstand |
| --- | --- |
| Ende Woche 2 | Erste Datenqualitätsanalyse, Modellabgrenzung, Parameterherkunft und Arbeitsplan; gemeinsamer Aufwandsabgleich und verbindliche Umfangsbestätigung |
| Ende Woche 4 | Lauffähiger Referenzplaner mit Simulation und Ereignisprotokoll |
| Wochen 5–8 | Eigene Verbesserung, Vergleichsversuche, Sensitivitätsanalyse, Ergebnisprüfung und Ausarbeitung |

Erkenntnisse aus Prüfung und Auswertung können erneute Datenanalysen oder Modelländerungen erfordern. Solche Überarbeitungen werden dokumentiert und begründet.

## Vorgesehene Abgaben

- **Hausarbeit:** Datenqualitätsanalyse, Entscheidungsmodell mit Definition aller Größen, begründete Verfahren, Simulationsmodell, Ergebnisse und Handlungsempfehlung einschließlich Gültigkeitsbedingungen.
- **Lauffähiger Python-Code:** Planung, SimPy-Simulation und unabhängige Prüfung mit dokumentierten Ein- und Ausgaben, Abhängigkeiten und Beispielaufruf.
- **Reproduzierbare Nachweise:** Datenherkunft und Aufbereitung, Befundregister, Parameter, Ereignisprotokolle, Basis- und Stressvergleiche sowie Sensitivitätsanalyse.

Diese Abgaben sind geplant und noch nicht vorhanden. Der nächste fachliche Schritt ist die Prüfung des ausstehenden Referenzpakets und die darauf aufbauende Bestätigung von Datenbasis, Parametern und Modellgrenzen.
