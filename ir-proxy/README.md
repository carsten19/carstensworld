# M5Stack Atom Echo IR Proxy

ESPHome Beispielkonfiguration für einen M5Stack Atom Echo als Infrarot-Proxy in Home Assistant.

## Video

- YouTube: TODO - Link zum Video ergänzen

## Hardware

- M5Stack Atom Echo
- IR-Transmitter auf `GPIO26`
- IR-Receiver auf `GPIO32`
- interne Status-LED auf `GPIO27`

## Dateien

- `m5stack-atom-echo-ir-proxy.yaml` - ESPHome-Konfiguration
- `secrets.example.yaml` - Beispiel für die benötigten ESPHome-Secrets

## Home-Assistant-Actions

Die Konfiguration stellt über die native ESPHome-API mehrere Actions bereit:

- `send_pronto`
- `send_nec`
- `send_panasonic`
- `send_sony`

Damit können IR-Codes aus Home Assistant heraus an Geräte wie Fernseher, Receiver, Klimaanlagen oder andere IR-Geräte gesendet werden.

## Nutzung

1. `secrets.example.yaml` als Vorlage für deine ESPHome-Secrets verwenden.
2. YAML in ESPHome importieren.
3. Gerät per USB flashen.
4. In Home Assistant den neuen ESPHome-Knoten hinzufügen.
5. IR-Codes über den Receiver anlernen oder bekannte Codes über die Actions senden.

## Hinweise

- `remote_receiver.dump: all` ist zum Anlernen praktisch, erzeugt aber viele Logs. Für den Dauerbetrieb kann man gezielt nur die benötigten Protokolle dumpen oder das Dumping reduzieren.
- Die `infrared`-Plattform mit `ir_rf_proxy` muss von deiner ESPHome-Installation unterstützt werden. Falls die Konfiguration nicht kompiliert, prüfe zuerst ESPHome-Version und benötigte Komponenten.
- Der M5Stack Atom Echo ist hier als kompakter IR-Proxy gedacht. Für hohe Reichweite oder schwierige Räume kann eine externe IR-LED bzw. ein stärkerer Sender nötig sein.
