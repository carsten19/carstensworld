# ESPHome Configs

ESPHome Konfigurationen für meine Smart Home Projekte aus dem YouTube Kanal **Carsten's World**.

## 📁 Projekte

### Dashboard Timer (HA Voice PE + Waveshare 7" Display)
- **Hardware:** Home Assistant Voice Preview Edition + Waveshare ESP32-S3 7" LCD Development Board
- **Video:** https://www.youtube.com/watch?v=UrlC64jcwt4
- **Files:** `dashboard-timer/`
- **Beschreibung:** ESPHome-Konfiguration für die HA Voice PE (Timer-Sensor-Export via Lambda) und das Waveshare 7"-Dashboard (LVGL Timer-Widget mit Fortschrittsbalken).

### E-Ink Display (Xiao 7.5")
- **Hardware:** Seeed Studio Xiao ESP32 + 7.5" E-Paper Display
- **Video:** https://youtu.be/-BWdE85hcqw
- **Files:** `eink-display/`

### M5Stack Atom Echo IR Proxy
- **Hardware:** M5Stack Atom Echo
- **Video:** TODO - Link zum Video ergänzen
- **Files:** `ir-proxy/`
- **ESPHome:** 2026.1.0 oder neuer
- **Beschreibung:** ESPHome-Konfiguration für einen kompakten IR-Proxy mit Home-Assistant-Actions zum Senden von Pronto-, NEC-, Panasonic- und Sony-IR-Codes.

### Xiao ESP32-C6 SHTC3 Gehäuse
- **Hardware:** Seeed Studio Xiao ESP32-C6 + SHTC3 Temperatur-/Feuchtigkeitssensor
- **Video:** https://youtu.be/xsSsGEaRrT0
- **Files:** `xiao-esp32-c6-shtc3-case/`
- **Beschreibung:** STL-Datei für ein 3D-druckbares Gehäuse zum ESP32-Temperatursensor-Projekt.

### Home Assistant Battery Card
- **Typ:** Lovelace Custom Card für Batterie-SOC mit Lade-/Entladebalken
- **Video:** https://youtube.com/shorts/lcRq-HvQT7c
- **Files:** `home-assistant/battery-card/`

## 🚀 Quick Start

1. **Repository klonen:**
   ```bash
   git clone https://github.com/carsten19/carstensworld.git
   cd carstensworld
   ```

2. **Secrets einrichten:**
   ```bash
   cp <projekt>/secrets.example.yaml <projekt>/secrets.yaml
   # Bearbeite secrets.yaml mit deinen Werten
   ```

3. **In ESPHome einbinden:**
   - ESPHome Dashboard → New Device → Import existing YAML
   - Oder per CLI: `esphome run <projekt>/<config>.yaml`

4. **Auf ESP32 flashen:**
   - USB anschließen
   - In ESPHome Dashboard auf "Install" klicken

## 🔒 Secrets

Die Datei `secrets.yaml` enthält sensible Daten (WiFi, API Keys) und ist in `.gitignore` eingetragen. **Niemals committen!**

Verwende `secrets.example.yaml` als Template mit Platzhaltern.

## 📺 YouTube Kanal

Besuche [Carsten's World](https://youtube.com/@carstensworld) für Videos zu:
- Home Assistant Integrationen
- ESPHome Projekte
- Smart Home Automation mit AI

## 📄 Lizenz

MIT License - Siehe [LICENSE](LICENSE)

---

**Happy Hacking! 🤖**
