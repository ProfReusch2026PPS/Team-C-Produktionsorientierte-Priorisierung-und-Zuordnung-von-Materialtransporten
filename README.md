# Team C: Produktionsorientierte Priorisierung und Zuordnung von Materialtransporten

## Team

- Moritz Spieker
- Orkun Yavas
- Viola Fürer

## Projektstatus und fachliche Grundlage

**Es gibt noch keine Implementierung. Das Referenzpaket steht noch aus.** Dieses README beschreibt den vorgesehenen Arbeitsumfang und die Anforderungen; es dokumentiert keine bereits erzielten Ergebnisse, bestandenen Prüfungen oder bestätigten Leistungsverbesserungen.

Fachliche Grundlage ist `Pruefungsprojekte_IoT_Factory_Studierende(1).pdf`, Stand 30. Oktober 2026: Team C auf Seiten 4–5, gemeinsame Anforderungen und Abgaben auf Seiten 6–7 sowie Arbeitsrahmen und Zwischenstände auf Seite 1.

Das angekündigte Referenzpaket soll Daten, Formate, Produktionsabschnitt, feste Umgebungsregeln und ein kleines SimPy-Grundgerüst bereitstellen. Konkrete Datenfelder, Parameter, Stationszahl und Anlagenregeln werden nach dessen Bereitstellung geprüft. Das fachliche Simulationsmodell entwickelt das Team selbst. Ergebnisse oder Code anderer Teams werden nicht benötigt.

Aktuell wird ausschließlich diese `README.md` im Repository-Hauptverzeichnis angelegt. Weitere Dateien, Verzeichnisse, Installationsanweisungen oder ausführbare Beispielaufrufe sind noch nicht vorhanden.


## Arbeitsüberblick: Vom ersten Laborbesuch bis zur Abgabe

**Planungsstand: 4. November 2026. Erster Laborbesuch: Mittwoch, 11. November 2026.**
Alle folgenden Punkte sind offene Aufgaben. Der Laborbesuch ist nicht automatisch der Beginn der achtwöchigen Bearbeitungsfrist; Projektstart, Abgabetermin und Zuordnung zu den Projektwochen sind mit der Lehrperson zu bestätigen.

### 1. Vor dem Laborbesuch vorbereiten

- [ ] Aufgabenstellung zu Team C und gemeinsame Anforderungen gemeinsam lesen.
- [ ] Die drei zu vergleichenden Transportregeln und die Abgrenzung zu Chargenbildung und Auftragsfreigabe erklären können.
- [ ] Fragen aus der folgenden Laborcheckliste sammeln und priorisieren.
- [ ] Rollen für den Besuch verteilen: Ablauf beobachten, MES-/Datenfragen klären, Protokoll und offene Punkte festhalten. Die Zuordnung im Team erfolgt gemeinsam.
- [ ] Verfügbarkeit des Referenzpakets, Datenzugang und zulässige Dokumentation erfragen.

**Ergebnis:** Gemeinsames Aufgabenverständnis und vorbereitete Fragenliste.

### 2. Im Labor: Anlage und Regeln verstehen

Ziel des ersten Besuchs ist ein fachlich belastbares Prozessbild. Noch nicht bekannte Abläufe werden als offene Fragen festgehalten.

| Thema | Vor Ort beobachten oder erfragen | Festzuhaltender Nachweis |
| --- | --- | --- |
| Produktionsabschnitt | Welche Stationen und Produkte gehören zum Projekt? Wo liegen Start und Ende der Betrachtung? | Einfache Ablaufskizze mit Stationsbezeichnungen |
| Konkreter Montagefall | Einen Vorgang von Werkstückankunft über Materialversorgung bis Montageabschluss nachvollziehen | Beispiel mit Auftrag, Position, Schritt, Lieferung und Zielstation |
| Materialsatz und Box | Welche Komponenten und Mengen müssen gemeinsam vorliegen? Welche Boxinhalte sind zulässig? | Bestätigte Satz- und Boxregeln |
| Materialmangel | Wohin fährt ein unversorgtes Werkstück weiter? Wann und unter welchen Bedingungen kehrt es zurück? | Weiterfahr- und Wiederkehrregel; Beobachtung oder fachliche Bestätigung |
| Montagebereitschaft | Welche Vorgänger müssen beendet sein? Was passiert bei belegter Station? Welche Montagepriorität gilt? | Voraussetzungen einer nutzbaren Bearbeitungsmöglichkeit |
| Lieferbereitschaft | Wann gilt eine Lieferung als kommissioniert und verfügbar? Welche Angaben enthält die Versorgungsliste? | Definition und verfügbare Produktionsreferenzen |
| Robotinos | Welche Fahrzeuge sind zulässig? Welche Positionen, Zustände und Verfügbarkeiten sind bekannt? Ab wann ist ein Transport bindend? | Fahrzeugzustände und Bindungsregel |
| Transportzeiten | Sind Leer- und Lastfahrdauern sowie Be- und Entladezeiten vorhanden? Welche Messungen wären ergänzend möglich? | Parameterquelle, Einheit und Datenlücken |
| Übergabeplätze | Wie viele Plätze gibt es? Was geschieht bei voller Kapazität oder Sperrfenstern? | Kapazitäts-, Warte- und Übergaberegel |
| Lade- und Parkvorgänge | Welche Regeln sind bindend und was darf im Modell ausdrücklich ausgeblendet werden? | Bestätigte Modellabgrenzung |
| MES und Datenbank | Wo liegen Stammdaten, Aufträge, Positionen, Schritte, Bestände, Reservierungen und Historien? | Relevante Tabellen/Felder und Verknüpfungen |
| Zeitbezug | Welche Zeitstempel sind geplant, tatsächlich gemessen oder nur gebucht? Sind Fahrzeugbewegungen historisch aufgezeichnet? | Bedeutung der Zeitfelder und Eignung zur Zeitermittlung |

- [ ] Ein Beispiel möglichst vollständig verfolgen und fehlende Verbindungen notieren.
- [ ] Beobachtete Abläufe von Aussagen der betreuenden Person und eigenen Annahmen unterscheiden.
- [ ] Ungeklärte Regeln mit zuständiger Ansprechperson und nächstem Klärungsschritt festhalten.
- [ ] Referenzpaket, Projektfrist und Umfangsbestätigung ansprechen.
- [ ] Keine Änderungen an der produktiven Anlage vornehmen.

**Ergebnis:** Laborprotokoll mit Prozessskizze, Beispielablauf, bestätigten Regeln, verfügbaren Daten und offenen Fragen. Ein fehlender Materialfall muss nicht künstlich ausgelöst werden; die Anlagenlogik kann fachlich geklärt werden.

### 3. Nach dem Besuch: Daten und Modellgrenze festlegen

- [ ] Beobachtungen zeitnah gemeinsam abgleichen und Widersprüche klären.
- [ ] Referenzpaket prüfen, sobald es vorliegt; Beobachtungen mit den verbindlichen Projektregeln abgleichen.
- [ ] Datenwörterbuch erstellen: Objekt, Feld, Bedeutung, Einheit, Schlüssel, Zeitbezug und Quelle.
- [ ] Lieferung → Auftrag → Position → Arbeitsschritt → Materialsatz → Zielstation anhand eines Beispiels verknüpfen.
- [ ] Datenqualität mit ausführbaren Regeln und mindestens einer manuellen Stichprobe untersuchen.
- [ ] Befunde mit Anzahl, Anteil, Beispiel, Behandlung und Modellfolge erfassen; Rohdaten unverändert lassen.
- [ ] Parameterherkunft trennen: MES-Wert, Ableitung, Beobachtung oder Szenarioannahme.
- [ ] Modellgrenze, Kapazitäten, Ereignisse und Zustandsübergänge dokumentieren und den Umfang abstimmen.

**Ergebnis bis Ende Projektwoche 2:** Erste Datenqualitätsanalyse, abgestimmte Modellabgrenzung, Parameterübersicht und Arbeitsplan. Fehlende historische Fahrdaten werden als Datenlücke ausgewiesen.

### 4. Referenzplanung und Simulation aufbauen

- [ ] Gemeinsame Ein- und Ausgaben für Planer, Simulation und unabhängige Prüfung definieren.
- [ ] Referenz 1 umsetzen: Eingangsreihenfolge mit jeweils kürzester zulässiger Leerfahrtdauer.
- [ ] Referenz 2 umsetzen: gemeinsame Zuordnung mit möglichst geringer gesamter Leerfahrtdauer.
- [ ] SimPy-Modell mit mindestens zwei Fahrzeugen und mindestens zwei um Transporte konkurrierenden Stationen aufbauen; konkrete Stationszahl gemäß Referenzpaket.
- [ ] Transportkette, Fahrzeugpositionen, Übergabekapazitäten und Ressourcenbindung abbilden.
- [ ] Montagevoraussetzungen, Komponentenverbrauch sowie Weiterfahrt und Wiederkehr abbilden.
- [ ] Planung nur zu festgelegten Ereignissen und mit dem dann bekannten Zustand aufrufen.
- [ ] Ereignisprotokoll, Regeln für gleichzeitige Ereignisse, Endkriterium und maximale Laufzeit ergänzen.
- [ ] Einen kleinen Ablauf von Hand durchgehen und mit dem simulierten Zeitprotokoll vergleichen.

**Ergebnis bis Ende Projektwoche 4:** Lauffähiger Referenzplaner mit Simulation und Ereignisprotokoll gemäß Meilenstein. Beide Referenzregeln müssen spätestens für den abschließenden Vergleich verfügbar sein.

### 5. Unabhängige Prüfung und eigene Regel entwickeln

Die Prüfung wird bereits beim Aufbau der Referenzsimulation mitentwickelt.

- [ ] Mengenbilanz, Satzvollständigkeit, Vorgängerfolge, Kapazitäten und eindeutige Aufgaben-/Fahrzeugbindung unabhängig prüfen.
- [ ] Absichtlich fehlerhafte Ergebnisse erzeugen und nachweisen, dass die Prüfung Verstöße erkennt.
- [ ] Produktionsorientierte Regel entwerfen: Welche Zuordnung ermöglicht voraussichtlich eine bevorstehende Montage oder vermeidet eine spätere Fertigstellung?
- [ ] Zielhierarchie, Gleichstände und Umgang mit lange wartenden Lieferungen begründen.
- [ ] Nur zum Entscheidungszeitpunkt bekannte Informationen verwenden.
- [ ] Für einen kleinen Fall alle zulässigen Alternativen vollständig enumerieren und das Verfahren daran bewerten.
- [ ] Einen nachvollziehbaren Fall zeigen, in dem eine verspätete Lieferung den Montageablauf tatsächlich verändert.

**Ergebnis:** Drei vergleichbare Planungsverfahren und eine nachweislich wirksame Regelprüfung. Eine Leistungsverbesserung der eigenen Regel ist zu untersuchen und wird nicht vorausgesetzt.

### 6. Vergleichsversuche durchführen und auswerten

- [ ] Kennzahlen und Bezugspunkte festlegen, insbesondere die Vergleichsbasis für Verzögerungen von Montagebeginn und -abschluss.
- [ ] Basisfall mit gleichmäßigem Produktionsbedarf durchführen.
- [ ] Stressfall mit gleichzeitig versorgungsbedürftigen Stationen und unterschiedlichen Bearbeitungsmöglichkeiten durchführen.
- [ ] Stressfall mit zeitweiligem Entzug eines freien Fahrzeugs durchführen.
- [ ] Alle drei Regeln je Fall mit denselben Eingaben, Abläufen und Ressourcen vergleichen.
- [ ] Hauptvergleich mit festen Dauern durchführen.
- [ ] Eine aus der Datenanalyse begründete Unsicherheit untersuchen, etwa Fahrdauern oder Werkstückankunftszeiten.
- [ ] Parameterwahl und abschließende Prüfung auf getrennten Szenarien durchführen.
- [ ] Verpasste Bearbeitungsmöglichkeiten, Montageverzögerungen, erledigte/offene Montagevorgänge, Leerfahrtdauer, Transportwartezeiten und Fahrzeugbelegung auswerten.
- [ ] Tatsächliche materialbedingte Stationsstillstände separat erfassen und Verzögerungsursachen begründen.
- [ ] Offene Arbeit und Zustände am Laufende sowie Stillstände ohne Fortschritt berichten.

**Ergebnis:** Reproduzierbare Basis- und Stressvergleiche, Sensitivitätsanalyse und begründete Aussage, unter welchen Bedingungen welche Regel vorteilhaft ist.

### 7. Abgabe fertigstellen

- [ ] Hausarbeit fortlaufend aus Datenbefunden, Modellentscheidungen und Versuchsergebnissen aufbauen.
- [ ] Datenherkunft, Aufbereitung, Parameter und alle wesentlichen Annahmen nachvollziehbar dokumentieren.
- [ ] Python-Code mit Abhängigkeiten, Ein-/Ausgaben und Beispielaufrufen beschreiben.
- [ ] Gesamten Ablauf von der Aufbereitung bis zur unabhängigen Prüfung erneut ausführen.
- [ ] Ergebnisse, Grenzen und Handlungsempfehlung gemeinsam prüfen.
- [ ] Abgabeumfang und Termin mit den bestätigten Vorgaben abgleichen.

**Ergebnis bis zum bestätigten Abgabetermin:** Hausarbeit, lauffähiger Code und reproduzierbare Nachweise. Die Aussage bleibt auf den modellierten Produktionsabschnitt begrenzt.

### Zusammenarbeit und nächste Entscheidung

Moritz Spieker, Orkun Yavas und Viola Fürer legen nach dem Laborbesuch gemeinsam Verantwortliche fest. Für jedes Arbeitspaket sollen eine verantwortliche Person, eine prüfende Person, ein Zieltermin und ein prüfbares Ergebnis festgehalten werden. Anlagenverständnis und Ergebnisinterpretation bleiben gemeinsame Aufgaben.

Als theoretische Unterstützung dienen insbesondere die Lehrunterlagen zu Datenverwaltung (Kapitel 02), Reihenfolgeregeln (Kapitel 05), Produktionslogistik (Kapitel 11), MES-Ereignissen (Kapitel 12) und logistischen Zielkonflikten (Kapitel 13). Verbindliche projektspezifische Regeln folgen aus Aufgabenstellung, Referenzpaket und bestätigter Abstimmung.

**Unmittelbar nächster Schritt:** Laborcheckliste im Team durchgehen, Beobachtungsrollen verteilen und am 11. November die offenen Anlagen- und Datenfragen klären.

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
