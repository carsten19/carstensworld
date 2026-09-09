# BLE-Helligkeitssensor mit XIAO nRF52840

Ein sehr sparsamer Helligkeitssensor aus einem **Seeed Studio XIAO nRF52840**
und einem **OPT3001**. Luxwert, Akkuspannung und Akkustand werden als
[BTHome-v2](https://bthome.io/)-Advertisements per Bluetooth Low Energy an
Home Assistant gesendet. WLAN, ESPHome-API und ein eigener BLE-Decoder sind
nicht erforderlich.

## Video

**TODO:** Link zum Video auf Carsten's World ergänzen.

## Gemessener Stromverbrauch

Am vollständigen Aufbau wurden vor der Aktivierung der echten
TX-Power-Steuerung folgende Werte angezeigt. Der Funkcontroller sendete dabei
mit seiner Standardleistung von 0 dBm:

- etwa **10 µA** im Ruhezustand
- kurz etwa **15 µA** bei sichtbarer BLE-Aktivität
- kurz mehr als **80 µA** bei einer OPT3001-Messung

Ein normales Multimeter mittelt die sehr kurzen Funkspitzen. Die Werte sind
daher Praxiswerte für diesen Aufbau, keine hochauflösende Funkmessung. Bei
einem 5.000-mAh-Akku wird die reale Laufzeit eher durch Selbstentladung,
Schutzschaltung und Alterung als durch den rechnerischen Sensorverbrauch
begrenzt.

Der entscheidende Low-Power-Schritt ist `disable_usb_uart: true`. Ohne diese
Option lag derselbe Aufbau bei rund **0,55 mA**. Das Abschalten betrifft nur die
laufende Zephyr-Anwendung; USB-Stromversorgung und Akkuladung arbeiten
hardwareseitig weiter.

## Hardware

- Seeed Studio XIAO nRF52840
- OPT3001-Modul, im Aufbau CJMCU-3001
- LiPo-Akku, im Aufbau 5.000 mAh
- vier Verbindungsleitungen

## Verkabelung

| XIAO nRF52840 | OPT3001 | Funktion |
|---|---|---|
| 3V3 | VCC | Versorgung |
| GND | GND | Masse |
| D4 / P0.04 | SDA | I²C-Daten |
| D5 / P0.05 | SCL | I²C-Takt |

`INT` und `ADD` des OPT3001 werden in diesem Projekt nicht angeschlossen.

## Voraussetzungen

- ESPHome **2026.8.1** oder kompatible neuere Version mit nRF52/Zephyr-Support
- Home Assistant mit Bluetooth-Adapter oder einem Bluetooth-Proxy in Reichweite
- der fest referenzierte Fork
  [`carsten19/esphome-bthome`](https://github.com/carsten19/esphome-bthome)
  in Version `v0.4.0-nrf52`

Das Projekt verwendet keine Secrets, da der Sensor ausschließlich per BLE
sendet. Die Datei `secrets.example.yaml` dokumentiert das ausdrücklich.

## Installation

1. [`ble-lumi-nrf.yaml`](ble-lumi-nrf.yaml) in ESPHome importieren.
2. Bei einer zuvor kompilierten Variante einmal **Clean Build Files** ausführen.
3. Die Firmware kompilieren und als UF2-Datei herunterladen.
4. Den Reset-Taster des XIAO zweimal kurz drücken.
5. Die UF2-Datei auf das eingebundene Bootloader-Laufwerk kopieren.
6. Nach dem automatischen Neustart USB trennen und den Sensor per Akku betreiben.

Mit `disable_usb_uart: true` stehen in der laufenden Firmware kein USB-CDC-Log
und kein UART0 zur Verfügung. Der separate UF2-Bootloader per Doppel-Reset sowie
das Laden des Akkus über USB funktionieren weiterhin. Deshalb darf kein
`logger:`-Block ergänzt werden.

## Funktionsweise

- Der OPT3001 misst die Beleuchtungsstärke alle fünf Minuten.
- Die Akkuspannung wird alle 30 Minuten erfasst.
- BTHome sendet die zuletzt bekannten Werte alle fünf bis zehn Sekunden.
- `App.set_loop_interval(1000)` reduziert unnötige ESPHome-Loop-Aufrufe; das
  BLE-Advertising läuft unabhängig im Controller weiter.
- Der nRF52-Low-Power-Helfer versetzt den ungenutzten externen QSPI-Flash in
  den Schlafmodus und deaktiviert USB/UART in der Anwendung.

Home Assistant erkennt das unverschlüsselte BTHome-Gerät normalerweise
automatisch und bietet die drei Messwerte als neue Entitäten an.

## Einstellungen anpassen

- `tx_power`: `v0.4.0-nrf52` setzt diesen Wert tatsächlich am
  nRF52840-Funkcontroller. Die enthaltenen `8` dBm wurden für den Außensensor
  gewählt, weil zwischen Sensor und Bluetooth-Proxy eine Wand liegt. Niedrigere
  Werte sparen während der kurzen Funkimpulse Strom, reduzieren aber die
  Verbindungsreserve.
- `min_interval` / `max_interval`: Abstand der BLE-Advertisements.
- `update_interval` beim OPT3001 und ADC: Messintervalle.
- `3.20 -> 0` und `4.14 -> 100`: einfache Akkuprozent-Kalibrierung für den
  verwendeten LiPo. Die Spannungskurve eines LiPo ist nicht linear; diese
  Anzeige ist daher nur eine Näherung.

Der interne Batteriespannungsteiler des XIAO wird über P0.14 aktiviert. Die
enthaltene Schalterkonfiguration hält P0.14 physisch auf LOW, damit der
ADC-Eingang P0.31 auch während des USB-Ladens geschützt bleibt.

## Dateien

- `ble-lumi-nrf.yaml` – vollständige ESPHome-Konfiguration
- `secrets.example.yaml` – Hinweis, dass keine Secrets erforderlich sind

## Lizenz

Dieses Projekt steht wie das Hauptrepository unter der MIT-Lizenz.
