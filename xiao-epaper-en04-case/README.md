# XIAO ePaper Display Board EN04 – Wandgehäuse (V6)

3D-druckbares Zwei-Teile-Gehäuse für das Seeed Studio XIAO ePaper Display Board EN04 (nRF52840) mit 4,2"-Monochrom-E-Paper und LiPo-Akku. Display und EN04 sitzen untereinander auf dem Frontchassis, wie das Display-FPC direkt ohne Verlängerung verläuft. Der Rückdeckel trägt Akku und Wandaufhängung.

## Video

- YouTube: TODO – Link zum Video ergänzen

## Dateien

- `en04-front-chassis.stl` – Front mit Displayfenster, Displayführung und Domen für das EN04
- `en04-rear-cover.stl` – Rückdeckel mit Panelhalter, Akkufach, Gurtschlitzen, Schlüssellöchern und Öffnungen für USB-C, Taster und Schalter
- `details.png` – Unterkante und Schnitt durch eine Gehäuseschraube
- `source/` – parametrische Python-Quelle (`generate_case_v6.py`, nutzt Hilfsfunktionen aus `generate_case_v4.py`)

## Maße

- Außen: 128 × 140,2 × 22 mm
- Display: 4,2" Seeed Monochrome ePaper (91 × 77 mm)
- Akku: bis 50 × 34 × 10 mm (z. B. LiPo 2000 mAh), JST-PH-2.0

## Material

- 4× M2×6, selbstschneidend für Kunststoff (EN04)
- 4× M2×16 Linsenkopf, Kopf max. Ø 4,0 mm (Gehäuse; Köpfe liegen versenkt)
- 10–12 mm Klettband für den Akku
- 0,8–1,0 mm Schaumklebeband als Vorspannung für das Display
- Für die Wand: zwei Schrauben mit 6–7 mm Kopf

## Montage

1. Frontchassis mit der Sichtseite auf ein weiches Tuch legen und das Display einlegen.
2. Das Display-FPC ohne Verdrehen in den 24-poligen Anschluss des EN04 stecken (Jumper auf „24 PIN“).
3. EN04 mit der Bauteilseite zum Display auf die Dome schrauben.
4. Akku einlegen und mit Klettband sichern. **Polung vorher prüfen** – viele Akkus haben die Kabel am JST-Stecker gegenüber dem EN04 vertauscht.
5. Schaumband auf den Displayrand, Rückdeckel aufsetzen und mit den vier M2×16 verschrauben.

## Druck

- PETG bevorzugt, PLA für innen möglich
- 0,2 mm Schichthöhe, 3 Perimeter, 15–20 % Infill
- Beide Teile mit der großen flachen Seite aufs Druckbett

## Änderungen gegenüber V5

- USB-C-Öffnung reicht bis zur Trennfuge, der schmale Steg davor ist entfallen
- Ausschnitt für den RESET-Taster ergänzt
- Senkungen für die Gehäuseschrauben, die Köpfe stehen nicht mehr über
