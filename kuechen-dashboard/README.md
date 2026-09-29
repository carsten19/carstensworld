# Küchen-Dashboard (Waveshare 7" + ESPHome + LVGL)

ESPHome-Konfiguration für mein Küchen-Dashboard auf dem Waveshare ESP32-S3-Touch-LCD-7 (800 × 480). Angezeigt werden Uhrzeit mit Sekunden, Innen- und Außentemperatur, Sonnenauf-/-untergang, der nächste Kalendertermin oder die laufende Musik, ein Timer der Home Assistant Voice PE und der nächste Müll-Abholtermin.

## Video

- YouTube: TODO – Link zum Video ergänzen
- Vorgängervideo zum Dashboard: https://youtu.be/v1UE3SAf5vI

## Hardware

- Waveshare ESP32-S3-Touch-LCD-7 (800 × 480): https://link.amazon/B0i6uTKOs *(Affiliate-Link)*
- Gehäuse: https://makerworld.com/de/models/1858825-waveshare-esp32-s3-lcd-touch-7-case#profileId-1987829
- Optional: Home Assistant Voice Preview Edition für den Timer

## Dateien

- `kuechen-dashboard.yaml` – komplette ESPHome-Konfiguration
- `images/` – Hintergrundbild und Boot-Logo (werden beim Kompilieren direkt aus diesem Repo geladen)

## Installation

1. ESPHome Device Builder öffnen → **New Device** → **Import from File** bzw. neues Gerät anlegen und den Inhalt von `kuechen-dashboard.yaml` hineinkopieren.
2. In deiner `secrets.yaml` müssen `wifi_ssid` und `wifi_password` stehen (im ESPHome Device Builder ist das Standard).
3. Den Block `substitutions` ganz oben anpassen (siehe unten).
4. Kompilieren und beim ersten Mal per USB flashen, danach per OTA.
5. Das Gerät in Home Assistant über die ESPHome-Integration hinzufügen.

Die Konfiguration wurde mit ESPHome 2026.9 validiert (`esphome config`).

## Was du anpassen musst

Alles steht im Block `substitutions` am Anfang der YAML:

| Substitution | Bedeutung |
|---|---|
| `name`, `friendly_name` | Gerätename in ESPHome/Home Assistant |
| `latitude`, `longitude` | Dein Standort für Sonnenauf-/-untergang (Dezimalgrad) |
| `timezone` | Zeitzone, z. B. `Europe/Berlin` |
| `entity_temp_indoor` | Sensor für die Innentemperatur |
| `entity_temp_outdoor` | Sensor für die Außentemperatur |
| `entity_timer` | Timer-Sensor der Voice PE (Restsekunden), siehe [`dashboard-timer/`](../dashboard-timer/) |
| `entity_media_player` | Media Player in der Küche (Titel, Interpret und Cover werden angezeigt) |
| `entity_calendar` | Template-Sensor mit dem Attribut `next_event` |
| `entity_date` | Template-Sensor mit dem Datum als Text |
| `entity_tts_timer` | Timer-Helfer, der während TTS-Ansagen läuft |
| `entity_trash` | Text-Sensor mit dem nächsten Abholtermin |

Optional: `wallpaper_url` und `boot_logo_url`, wenn du eigene Bilder verwenden willst (URL oder lokaler Pfad).

Weitere optionale Punkte in der YAML:
- `api:` – Verschlüsselung ist auskommentiert. Empfohlen: Schlüssel erzeugen und als `api_encryption_key` in `secrets.yaml` eintragen.
- `bluetooth_proxy:` – kann entfernt werden, wenn du keinen Bluetooth-Proxy brauchst.
- Anti-Burn-in läuft nachts zwischen 1 und 5 Uhr jeweils 15 Minuten (`time:` → `on_time`).

## Benötigte Helfer in Home Assistant

### Müll-Abholtermin
Mit der HACS-Integration [Waste Collection Schedule](https://github.com/mampfes/hacs_waste_collection_schedule). Der Text muss mit „Heute“ oder „Morgen“ beginnen, damit die Kachel rot bzw. hell eingefärbt wird:

```yaml
sensor:
  - platform: waste_collection_schedule
    name: Müll nächste Abholung
    value_template: >-
      {% if value.daysTo == 0 %}Heute{% elif value.daysTo == 1 %}Morgen{% else %}In {{ value.daysTo }} Tagen{% endif %}
      {{ value.types | join(", ") }}
```

### Nächster Kalendertermin
Trigger-basierter Template-Sensor (Kalender-Entität anpassen):

```yaml
template:
  - trigger:
      - trigger: time_pattern
        minutes: /5
      - trigger: homeassistant
        event: start
    action:
      - action: calendar.get_events
        target:
          entity_id: calendar.familie
        data:
          duration:
            hours: 48
        response_variable: kalender
    sensor:
      - name: Dashboard Calendar Events
        state: "{{ kalender['calendar.familie'].events | count }}"
        attributes:
          next_event: >-
            {% set e = kalender['calendar.familie'].events | first %}
            {% if e %}{{ as_datetime(e.start).strftime('%H:%M') }} - {{ as_datetime(e.end).strftime('%H:%M') }}: {{ e.summary }}{% endif %}
```

### Datum als Text

```yaml
template:
  - sensor:
      - name: Datum
        state: >-
          {% set tage = ['Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag'] %}
          {% set monate = ['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'] %}
          {{ tage[now().weekday()] }}, {{ now().day }}. {{ monate[now().month - 1] }}
```

### TTS-Sperre (optional)
Ein Timer-Helfer (z. B. `timer.tts_active`, Dauer 5 s), den deine TTS-Automation vor jeder Ansage startet. Solange er läuft, zeigt das Dashboard statt der Ansage weiter den Kalender an und schaltet erst wieder auf die Musik um, wenn die Wiedergabe beendet ist. Ohne diesen Helfer die Substitution auf eine beliebige, nie aktive Timer-Entität setzen.

## Hinweise

- Die Material-Design-Icons und die Roboto-Schrift werden beim Kompilieren automatisch heruntergeladen.
- Der Touchscreen weckt das Display wieder auf, wenn die Hintergrundbeleuchtung aus ist.
