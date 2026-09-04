# Seeed Studio reTerminal E1004 Picture Frame

Konfiguration aus dem Video zum Seeed Studio reTerminal E1004:

https://youtu.be/B2D3pNJRpu8

Das Projekt zeigt drei Seiten auf dem 13,3-Zoll-Sechsfarben-E-Paper:

- generiertes KI-Bild
- Wetter-Dashboard mit Sieben-Tage-Vorhersage
- Erklärung zum KI-Bild

Die drei Hardwaretasten wechseln direkt zu diesen Seiten und wecken das Gerät aus dem Deep Sleep. Wetter und Erklärung werden mit LVGL aufgebaut. Das große Bild wird wegen Speicher- und Watchdog-Grenzen blockweise direkt in den E-Paper-Framebuffer geschrieben.

## Dateien

- `esphome.yaml`: vollständige ESPHome-Konfiguration für das E1004
- `home-assistant-templates.yaml`: kompakte Wetter- und Forecast-Sensoren für die ESPHome-Seiten
- `secrets.example.yaml`: Vorlage für WLAN, API, OTA und Bild-URL

## Voraussetzungen

- ESPHome 2026.7.0 oder neuer
- Home Assistant
- Seeed Studio reTerminal E1004
- ein per HTTP erreichbares JPEG für die Bildseite
- optional ein `input_text.ai_daily_picture_description` für die Bilderklärung

## Einrichtung

1. Ordner in das ESPHome-Konfigurationsverzeichnis kopieren.
2. `secrets.example.yaml` als `secrets.yaml` kopieren und alle Platzhalter ersetzen.
3. `home-assistant-templates.yaml` als Package einbinden oder den `template:`-Block in die Home-Assistant-Konfiguration übernehmen.
4. In `home-assistant-templates.yaml` diese Beispiel-Entity-IDs an das eigene System anpassen:
   - `weather.home`
   - `sensor.outdoor_temperature`
   - `sensor.rain_today`
   - `sensor.sun_next_rising`
   - `sensor.sun_next_setting`
5. Falls die Bilderklärung anders heißt, `input_text.ai_daily_picture_description` in `esphome.yaml` ersetzen.
6. Home Assistant neu laden bzw. neu starten und anschließend `esphome.yaml` installieren.

## Bildformat und Speichergrenze

Die Konfiguration lädt das Bild als JPEG/RGB565 mit `1520x1140` Pixeln. Ein Vollbild mit 1600x1200 benötigt einen zusammenhängenden RGB565-Puffer von 3.840.000 Byte. Auf dem getesteten Gerät war der größte freie PSRAM-Block kleiner. Das reduzierte 4:3-Bild benötigt 3.465.600 Byte und wird mit einem schmalen weißen Rand zentriert.

Die Bild-URL muss direkt auf eine JPEG-Datei zeigen. Dateiendung, tatsächlicher MIME-Typ und `format: JPEG` müssen zusammenpassen.

## Tastenbelegung

- GPIO3 / rechte Pfeiltaste: Bilderklärung
- GPIO4 / linke Pfeiltaste: Wetter-Dashboard
- GPIO5 / Refresh-Taste: KI-Bild neu laden

Alle drei Tasten können das Gerät aus dem vierstündigen Deep-Sleep-Zyklus wecken.

## Anpassungshinweise

- Die Akku-Kalibrierwerte sind Erfahrungswerte und sollten bei Bedarf gegen ein Multimeter geprüft werden.
- Das Wetter-Template erwartet mindestens sieben Tage in der Antwort von `weather.get_forecasts`.
- Die Template-Sensoren müssen exakt die in `esphome.yaml` importierten Namen erzeugen.
- Für andere Bildquellen oder Dateiformate die `online_image`-Konfiguration entsprechend anpassen.
