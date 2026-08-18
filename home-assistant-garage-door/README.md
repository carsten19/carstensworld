# Home Assistant Garagentor-Cover

Die Datei `garage-door-cover.yaml` enthält ein anonymisiertes Template-Cover für ein Garagentor mit:

- einem Taster-/Relais-Switch für Öffnen, Schließen und Stoppen,
- zwei Kontaktsensoren für die Endpositionen,
- dynamischem Zustand (`opening`, `closing`, `open`, `closed`),
- dynamischem Garagentor-Icon.

Vor der Verwendung müssen die drei Beispiel-Entity-IDs durch die eigenen Home-Assistant-Entitäten ersetzt werden.

Wenn in der bestehenden `configuration.yaml` bereits ein `template:`-Abschnitt vorhanden ist, darf `template:` nicht ein zweites Mal ergänzt werden. In diesem Fall nur den Block ab `- cover:` in die bestehende Liste übernehmen.
