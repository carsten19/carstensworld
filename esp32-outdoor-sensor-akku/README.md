# ESP32-C6 Outdoor-Sensor mit Akku (Thread + MQTT + Deep Sleep)

Batteriebetriebener Außentemperatur-Sensor mit ESP32-C6, DS18B20 und Akkuspannungsmessung. Der Sensor wacht alle 20 Minuten auf, verbindet sich über Thread, sendet Temperatur und Akkustand per MQTT und geht danach wieder in den Deep Sleep.

📺 **Video:** [ESP32 Outdoor-Sensor mit Akku: Deep Sleep, MQTT & Solar richtig planen](https://youtu.be/l48ehZmMlDc)

## Dateien

| Datei | Inhalt |
|---|---|
| `thread-outdoor-sensor.yaml` | ESPHome-Konfiguration |
| `secrets.example.yaml` | Vorlage für `secrets.yaml` (MQTT-Broker, Thread-Datensatz) |

## Voraussetzungen

- ESP32-C6 (z. B. Seeed Studio XIAO ESP32-C6), Framework ESP-IDF
- DS18B20-Temperatursensor (1-Wire) an **GPIO11**
- Akkuspannung über Spannungsteiler an **GPIO4** (ADC)
- Thread-Netzwerk mit Border Router (z. B. Home Assistant mit OpenThread Border Router)
- MQTT-Broker (z. B. Mosquitto) und die MQTT-Integration in Home Assistant
- Getestet mit ESPHome 2026.9

Der Sensor nutzt **MQTT statt der ESPHome-API**. So kann er senden und sofort wieder schlafen, ohne auf den Verbindungsaufbau von Home Assistant zu warten. Die Entitäten erscheinen per MQTT-Discovery automatisch in Home Assistant.

## Installation

1. `secrets.example.yaml` nach `secrets.yaml` kopieren und eigene Werte eintragen:
   - `mqtt_broker`: IP-Adresse oder Hostname des MQTT-Brokers
   - `openthread_tlv`: Active Dataset (TLV) deines Thread-Netzwerks. In Home Assistant unter *Einstellungen → Geräte & Dienste → Thread → Konfigurieren* beim Netzwerk über das (i)-Symbol abrufbar.
2. `thread-outdoor-sensor.yaml` im ESPHome Device Builder anlegen oder einfügen.
3. Beim ersten Mal per USB flashen. Danach sind Updates per OTA möglich (siehe Wartungsmodus).

## Anpassen

- **Pins:** `one_wire` → `pin: GPIO11`, `adc` → `pin: GPIO4`
- **Akkustand:** Die Kalibrierung `0.85 → 0 %` und `1.1 → 100 %` bezieht sich auf die **gemessene ADC-Spannung hinter dem Spannungsteiler**, nicht auf die Akkuspannung selbst. Passe die Werte an deinen Teiler und Akkutyp an.
- **Schlafintervall:** `deep_sleep` → `sleep_duration: 20min`. `run_duration: 60s` ist nur die Obergrenze; normalerweise schläft der Sensor nach wenigen Sekunden wieder ein.
- **Name und MQTT-Topic:** `esphome` → `name` sowie das Topic `helper/thread_outdoor_sensor/keep_awake`
- **Birth/Will-Topics:** `myavailability/birth` bzw. `myavailability/will` nach Bedarf ändern

## Ablauf eines Wachzyklus

1. Nach dem Aufwachen starten Temperatur- und Akkumessung sofort, parallel zum Thread- und MQTT-Verbindungsaufbau.
2. Das Skript `finish_cycle` wartet, bis MQTT verbunden ist, beide Messungen vorliegen und der Wachhalte-Sollzustand empfangen wurde (maximal 60 s).
3. Bei `OFF` lässt eine kooperative Sendepause von einer Sekunde ESPHome die MQTT-Verarbeitung fortsetzen; danach geht der Sensor in den Deep Sleep. Bei `ON` bleibt er für Wartung wach. Bei einem Timeout schläft er sicherheitshalber trotzdem. Die Sendepause ist keine Empfangsquittung des Brokers.
4. Diagnose-Sensoren: **Time to Connected** (Sekunden bis MQTT verbunden) und **Time to Finish** (Sekunden bis Messung und Steuerzustand bereit sind, vor der abschließenden Sendepause).

## Wartungsmodus (OTA)

Ein Sensor im Deep Sleep ist für OTA-Updates fast nie erreichbar. Deshalb gibt es den Schalter **Radio Always On**, gesteuert über ein MQTT-Topic mit Retain:

```bash
# Wach halten (beim nächsten Aufwachen bleibt der Sensor an)
mosquitto_pub -h <broker> -t helper/thread_outdoor_sensor/keep_awake -m ON -r -q 1
# Normalbetrieb
mosquitto_pub -h <broker> -t helper/thread_outdoor_sensor/keep_awake -m OFF -r -q 1
```

Wichtig: Der Sensor wartet bei jedem Aufwachen auf diesen Sollzustand. Die Nachricht deshalb **mit Retain** veröffentlichen, z. B. per Home-Assistant-Aktion `mqtt.publish` mit `retain: true`. Fehlt sie, wartet der Sensor bis zum 60-s-Timeout und verbraucht unnötig Strom.

## Hinweise

- `openthread` → `device_type: MTD`: Der Sensor arbeitet als Endgerät, nicht als Router.
- `network` → `enable_ipv6: true` ist für Thread erforderlich.

## Fehlerkorrektur vom 25.10.2026

Wer eine frühere Fassung übernommen hat, sollte die YAML aktualisieren und neu flashen:

- `control_received` wird ausschließlich beim tatsächlichen MQTT-Empfang von `ON` oder `OFF` gesetzt. Der Template-Schalter führt beim Start standardmäßig seine OFF-Aktion aus; diese darf keinen empfangenen MQTT-Befehl vortäuschen. Andernfalls kann der Sensor schlafen gehen, bevor ein retained `ON` verarbeitet wird, und sich nicht zuverlässig für OTA wachhalten lassen.
- Die aktive `delay: 1s` vor Deep Sleep bleibt erhalten. Messwerte und Diagnosewerte lokal zu publizieren oder `mqtt.connected` zu prüfen, bestätigt noch keine Zustellung beim Broker.
- **Time to Finish** bleibt als Diagnosewert erhalten; er misst nicht die zusätzliche Sendepause.

Die Konfiguration wurde mit dem ESPHome-2026.9.1-Validator geprüft. Ein Hardware-/OTA-Test dieser korrigierten Fassung ist damit nicht ersetzt. Falls die alte Firmware sich nicht mehr wachhalten lässt, kann ein USB-Flash zur Wiederherstellung nötig sein.
