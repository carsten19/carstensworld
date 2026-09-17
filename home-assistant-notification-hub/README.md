# Home Assistant Notification Hub

Ein zentraler Benachrichtigungs-Router für Home Assistant. Eine Automation ruft
nur noch ein Skript auf; das Skript kümmert sich abhängig von der Meldungsstufe
um Dashboard, Push-Nachrichten, Messenger und optionales TTS.

Entstanden als generische, anonymisierte Version des Skripts **„Information“**
aus dem Video:

▶️ [Home Assistant Notifications Effectively: From Info to Alert](https://youtu.be/EfXObDNgm7k)

## Funktionen

- drei Meldungsstufen: `info`, `warning`, `critical`
- vollständiger Meldungstext plus optionaler Dashboard-Kurztext
- frei konfigurierbare Aktionen für jede Meldungsstufe
- Dashboard-Ausgabe über zwei `input_text`-Helfer
- automatische Rücksetzung über einen Timer
- optionales TTS direkt über `tts.speak`
- optionaler Urlaubs-/Abwesenheitsmodus für normales TTS
- `tts_force` für Meldungen, die trotzdem gesprochen werden sollen
- warteschlangenfähiger Skriptmodus für gleichzeitig eintreffende Meldungen

Es gibt bewusst **keine fest eingebauten Geräte oder Messenger**. Push,
Telegram, Matrix oder andere Ziele werden als normale Home-Assistant-Aktionen
beim Erstellen des Skripts konfiguriert.

## Dateien

| Datei | Zweck |
| --- | --- |
| [`blueprints/script/carsten19/notification_hub.yaml`](blueprints/script/carsten19/notification_hub.yaml) | wiederverwendbarer Skript-Blueprint |
| [`packages/notification_hub_helpers.yaml`](packages/notification_hub_helpers.yaml) | Dashboard-Helfer, Timer und Reset-Automation |
| [`examples/script_instance.yaml`](examples/script_instance.yaml) | vollständige Beispielkonfiguration mit Push und direktem TTS |
| [`examples/automation_calls.yaml`](examples/automation_calls.yaml) | Aufrufe für Info, Warnung und kritische Meldung |
| [`examples/dashboard_cards.yaml`](examples/dashboard_cards.yaml) | einfache Dashboard-Karten |

## Installation

### 1. Helfer-Paket installieren

Kopiere `packages/notification_hub_helpers.yaml` nach:

```text
/config/packages/notification_hub_helpers.yaml
```

Falls Packages noch nicht aktiviert sind, ergänze in `configuration.yaml`:

```yaml
homeassistant:
  packages: !include_dir_named packages
```

Anschließend Home Assistant neu starten. Dadurch entstehen:

- `input_text.notification_hub_info`
- `input_text.notification_hub_warning`
- `timer.notification_hub_reset`
- eine Automation zum Leeren der Texte

### 2. Blueprint importieren

Importiere folgende URL unter **Einstellungen → Automationen & Szenen →
Blueprints → Blueprint importieren**:

```text
https://github.com/carsten19/carstensworld/blob/main/home-assistant-notification-hub/blueprints/script/carsten19/notification_hub.yaml
```

Erstelle daraus ein Skript und wähle die drei oben erzeugten Helfer aus.

### 3. Zustellwege konfigurieren

Die Aktionsfelder akzeptieren normale Home-Assistant-Aktionen. Darin sind diese
Template-Variablen verfügbar:

- `notification_message` – vollständiger Meldungstext
- `display_message` – Kurztext oder ersatzweise der vollständige Text
- `notification_title` – übergebener oder automatisch erzeugter Titel
- `notification_level` – `info`, `warning` oder `critical`

Beispiel für die Companion App:

```yaml
- action: notify.mobile_app_your_phone
  data:
    title: "{{ notification_title }}"
    message: "{{ notification_message }}"
```

Beispiel für eine moderne Notify-Entität:

```yaml
- action: notify.send_message
  target:
    entity_id: notify.your_messenger
  data:
    title: "{{ notification_title }}"
    message: "{{ notification_message }}"
```

### 4. TTS konfigurieren

```yaml
- action: tts.speak
  target:
    entity_id: tts.your_tts_engine
  data:
    media_player_entity_id: media_player.your_speaker
    message: "{{ notification_message }}"
    cache: false
```

Die TTS-Aktionen laufen nur, wenn beim Skriptaufruf `tts: true` oder
`tts_force: true` gesetzt ist. Ein optionaler `input_boolean` kann normales TTS
bei Abwesenheit sperren; `tts_force` umgeht diese Sperre.

## Verwendung

```yaml
- action: script.notification_hub
  data:
    level: warning
    title: Fenster offen
    message: Das Wohnzimmerfenster ist seit 15 Minuten geöffnet.
    short_message: Wohnzimmerfenster offen
    duration_minutes: 15
    tts: true
```

Weitere Beispiele stehen in
[`examples/automation_calls.yaml`](examples/automation_calls.yaml).

## Hinweise

- `input_text` ist auf 255 Zeichen begrenzt. Verwende für längere Meldungen den
  vollständigen Benachrichtigungskanal und einen kurzen `short_message`.
- Das Projekt liefert nur den Router. Die jeweiligen Integrationen für Push,
  Messenger, TTS und Media Player müssen bereits eingerichtet sein.
- Teste kritische Meldungen zunächst mit harmlosen Beispielautomationen.

## Lizenz

[MIT](LICENSE)
