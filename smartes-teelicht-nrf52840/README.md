# Smartes Teelicht mit XIAO nRF52840 (ESPHome + Thread)

Ein akkubetriebenes LED-Teelicht, das in Home Assistant als normales Licht
mit Farbe, Helligkeit und Kerzen-Flackereffekt erscheint. Funkweg ist Thread,
geladen wird über einen magnetischen Pogo-Pin-Anschluss im Sockel. Alles ist
fliegend verdrahtet, eine eigene Platine ist nicht nötig.

## Video

Folgt mit der Veröffentlichung auf dem Kanal
[Carsten's World](https://www.youtube.com/@carstensworld).
Die Idee kam aus einem Kommentar unter
[30 Jahre Akkulaufzeit? Dieser ESPHome-Sensor braucht nur 10 µA](https://youtu.be/a9gEFRlPrB0).

## Dateien

| Datei | Inhalt |
|---|---|
| `teelicht.yaml` | ESPHome-Konfiguration |
| `secrets.example.yaml` | benötigte Secrets mit Platzhaltern |
| `gehaeuse/*.stl` | druckfertige Gehäuseteile |
| `gehaeuse/*.step` | dieselben Teile als STEP zum Weiterkonstruieren |
| `gehaeuse/source/teelicht.py` | parametrische CadQuery-Quelle aller Teile |

## Hardware

- Seeed Studio XIAO nRF52840 (XIAO BLE, ohne Sense)
- RGB-LED 5 mm, **gemeinsame Anode**, 4 Pins
- Widerstände: 1 × 330 Ω (Rot), 2 × 100 Ω (Grün, Blau)
- LiPo-Akku 3,7 V, ca. 200 mAh, **mit Schutzschaltung** (Tiefentladeschutz)
- magnetisches Pogo-Pin-Paar, 2-polig, Raster 2,54 mm
- Schottky-Diode, z. B. SS14 oder 1N5817
- USB-Kabel zum Abschneiden (für den Ladesockel)

## Verdrahtung

| XIAO | Verbindung |
|---|---|
| D1 / P0.03 | 330 Ω → LED Rot (zweitlängstes Beinchen) |
| D4 / P0.04 | 100 Ω → LED Grün |
| D5 / P0.05 | 100 Ω → LED Blau |
| 3V3 | LED-Anode (längstes Beinchen), direkt |
| 5V / VUSB | Schottky-Diode, Ring zum XIAO → Pogo-Buchse Plus |
| GND | Pogo-Buchse Minus |
| BAT+ / BAT− (Unterseite) | Akku Plus / Minus |

- D2 und D3 bleiben frei, weil die Widerstände sonst an die Akku-Pads stoßen.
- Die Pogo-Buchse kommt an **5V/VUSB**, nicht an BAT. Nur so lädt der
  eingebaute Lader des XIAO den Akku.
- Die Polarität des Pogo-Paars vor dem Löten im zusammengesteckten Zustand mit
  dem Durchgangsprüfer bestimmen, die Aderfarben sind kein Beleg.
- Im Sockel kommt ein abgeschnittenes USB-Kabel an das Pogo-Gegenstück
  (Plus/Minus vorher messen).

## Gehäuse

| Teil | Zweck | Druck |
|---|---|---|
| Korpus | nimmt Akku und Pogo-Buchse auf (Rasthaken) | Boden aufs Bett, ohne Stützen |
| Deckel | Klemmring, LED-Loch 6,2 mm | Platte aufs Bett, Ring nach oben |
| Flamme | Lichtstreuer | transluzent, Vasenmodus, **0 Bodenschichten** |
| Sockel | Ladestation mit Pogo-Gegenstück | Oberseite aufs Bett |
| Sockel-Boden | Klemmdeckel für den Sockel | Außenseite aufs Bett |

Der Korpus ist für einen Akku bis ca. 32 × 20 × 6 mm ausgelegt. Die LED wird
im Deckel eingeklebt und hält dort auch den XIAO. Passmaße hängen von Drucker
und Material ab; die Parameter stehen oben in `gehaeuse/source/teelicht.py`.

## Installation

1. `teelicht.yaml` im ESPHome Device Builder als neues Gerät anlegen.
2. `api_encryption_key` und `openthread_tlv` in die eigene `secrets.yaml`
   eintragen (siehe `secrets.example.yaml`).
3. Einmal per USB flashen (UF2 nach Doppel-Reset), danach in Home Assistant
   über die ESPHome-Integration hinzufügen.
4. Für OTA-Updates `poll_period` vorübergehend auf `0s` setzen.

## Einstellungen zum Anpassen

- `name` / `friendly_name` bei mehreren Kerzen je Gerät eindeutig wählen.
- Die Farbe kommt aus Home Assistant und bleibt beim Effekt erhalten. Flackern über die Werte `0.06f`
  (Häufigkeit des Einknickens), `0.35f` (Weichheit) und `0.85f` (Grundhelligkeit).
- Unterspannungsabschaltung bei `3.3` V im Akkusensor.
- Akkuteiler `multiply: 2.961` und Kalibrierung `3.20 → 0 %`, `4.14 → 100 %`
  ggf. an den eigenen Aufbau anpassen.

## Gemessener Stromverbrauch

Nordic PPK2, 16 Minuten, 200-mAh-Akku:

- Standby (Licht aus, Thread verbunden): **Ø 0,06 mA**, rechnerisch ca. 4 Monate
- Kerze an: **Ø 3,0 mA**, rechnerisch gut 2 Tage

## Voraussetzungen

- ESPHome **2026.10.2** (kompiliert)
- Thread Border Router in Home Assistant
- externe Komponente `nrf52_low_power` aus
  [`carsten19/esphome-bthome`](https://github.com/carsten19/esphome-bthome),
  Tag `v0.4.1-nrf52`; schaltet USB/UART für niedrigen Ruhestrom ab, Laden
  über USB/Pogo funktioniert weiter
