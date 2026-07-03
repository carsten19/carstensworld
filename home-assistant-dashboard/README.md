# Home Assistant Dashboard

Anonymisierte Lovelace-Beispielkonfiguration für den Home-Tab des Home-Assistant-Dashboards aus dem Video.

## Datei

- `dashboard.example.yaml` - anonymisierter Export des Home-Tabs

## Vor der Nutzung anpassen

Ersetze die Beispiel-Entity-IDs durch deine eigenen Home-Assistant-Entitäten, insbesondere:

- Energie/PV/Batterie: `sensor.solar_*`, `sensor.grid_*`, `sensor.home_battery_*`
- Wallbox/Auto: `sensor.ev_*`, `sensor.wallbox_*`, `select.wallbox_charging_mode`
- Wetter: `sensor.outdoor_temperature`, `sensor.rain_rate`, `sensor.local_weather_warning_level`
- User-Sichtbarkeit: `USER_ID_ADMIN`, `USER_ID_TABLET`, `USER_ID_FAMILY_1`, `USER_ID_FAMILY_2`
- Hintergrundbild: `/local/dashboard/background.png`

## Benötigte Custom Cards

Das Dashboard nutzt unter anderem:

- `card-mod`
- `battery-card`
- `dual-ev-battery-card`
- `power-flow-card-plus`

Je nach Installation müssen diese Karten über HACS oder manuell ergänzt werden.
