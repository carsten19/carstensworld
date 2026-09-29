# XIAO ePaper Display Board EN04 – Wandgehäuse (V7)

3D-druckbares Zwei-Teile-Gehäuse für das Seeed Studio XIAO ePaper Display Board EN04 (nRF52840) mit 4,2"-Monochrom-E-Paper und LiPo-Akku. Display und EN04 sitzen untereinander auf dem Frontchassis, das Display wird von festen Lippen und zwei verschraubten Klemmlaschen gehalten, wie das Display-FPC direkt ohne Verlängerung verläuft. Der Rückdeckel trägt Akku und Wandaufhängung.

## Video

- YouTube: https://youtu.be/oomAC2TNEEU

## Dateien

- `en04-front-chassis.stl` – Front mit Displayfenster, Displayführung und Domen für das EN04
- `en04-rear-cover.stl` – Rückdeckel mit Akkufach, Gurtschlitzen, Schlüssellöchern und Öffnungen für USB-C, Taster und Schalter
- `en04-panel-clamp.stl` – Klemmlasche fürs Display, **2× drucken**, Nase nach oben
- `details.png` – Unterkante und Schnitt durch eine Gehäuseschraube
- `source/` – parametrische Python-Quelle (`generate_case_v7.py`, nutzt Hilfsfunktionen aus `generate_case_v4.py`)

## Maße

- Außen: 128 × 140,2 × 22 mm
- Display: 4,2" Seeed Monochrome ePaper (91 × 77 mm)
- Akku: bis 50 × 34 × 10 mm (z. B. LiPo 2000 mAh), JST-PH-2.0

## Material

- 4× M2×6, selbstschneidend für Kunststoff (EN04)
- 2× M2×5, selbstschneidend (Klemmlaschen)
- 4× M2×16 Linsenkopf, Kopf max. Ø 4,0 mm (Gehäuse; Köpfe liegen versenkt)
- 10–12 mm Klettband für den Akku
- Für die Wand: zwei Schrauben mit 6–7 mm Kopf

## Montage

1. Frontchassis mit der Sichtseite auf ein weiches Tuch legen. Display schräg mit der Unterkante unter die beiden Lippen schieben und flach ablegen.
2. Die beiden Klemmlaschen mit der Nase zum Display auflegen und mit M2×5 anschrauben. Nur anziehen, bis die Lasche aufliegt – das Glas nicht verspannen.
3. Das Display-FPC ohne Verdrehen in den 24-poligen Anschluss des EN04 stecken (Jumper auf „24 PIN“).
4. EN04 mit der Bauteilseite zum Display auf die Dome schrauben.
5. Akku einlegen und mit Klettband sichern. **Polung vorher prüfen** – viele Akkus haben die Kabel am JST-Stecker gegenüber dem EN04 vertauscht.
6. Rückdeckel aufsetzen und mit den vier M2×16 verschrauben.

## Druck

- PETG bevorzugt, PLA für innen möglich
- 0,2 mm Schichthöhe, 3 Perimeter, 15–20 % Infill
- Alle Teile mit der großen flachen Seite aufs Druckbett, supportfrei druckbar

## Änderungen gegenüber V5/V6

- Display wird vom Frontchassis gehalten (Lippen unten, zwei Klemmlaschen oben), kein Panelrahmen und kein Schaumstoff mehr nötig

- USB-C-Öffnung reicht bis zur Trennfuge, der schmale Steg davor ist entfallen
- Ausschnitt für den RESET-Taster ergänzt
- Senkungen für die Gehäuseschrauben, die Köpfe stehen nicht mehr über
