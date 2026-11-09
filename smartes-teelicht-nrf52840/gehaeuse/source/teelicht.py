#!/usr/bin/env python3
"""Parametrisches Gehäuse für das Smart-Teelicht: Korpus, Deckel, Flamme, Ladesockel."""
from pathlib import Path
import cadquery as cq

# Bauteile (mm)
BAT = (31.0, 20.0, 5.0)       # LiPo gemessen
BAT_CABLE_CORNER = (1, 1)     # Ecke ohne Anschlag: +X-Stirnseite, Seite der Pogo-Buchse
BAT_EXTRA_L = 1.0             # Akkuhalterung in Längsrichtung länger, nach Testeinbau
XIAO = (21.0, 17.5, 1.2)      # PCB
XIAO_H = 3.6                  # PCB + USB-C, angesetzt
POGO_W, POGO_H, POGO_D = 14.5, 4.0, 4.0  # Buchse gemessen, Breite über die Flanschohren
POGO_FRONT_W = 12.5           # schmaler Kontaktteil (Stadion), gemessen
POGO_FRONT_D = 2.2            # Länge des Kontaktteils bis Flansch, gemessen
SNAP_T, SNAP_HOOK = 0.9, 0.5    # Rastarm-Dicke, Hakenüberstand über die Ohren
POGO_Y = -13.0                # Seite gegenüber dem Akkukabel, Litzen laufen neben dem Akku hoch
CLEAR = 0.3                   # Spiel gesamt je Maß
FOAM = 1.0                    # Klebepad Akku/XIAO

# Korpus
OD, WALL, FLOOR = 45.0, 1.6, 1.2
ID = OD - 2 * WALL
SHELF_Z = 5.0                 # Akku-Unterkante, darunter Pogo + Lötstellen
LID_PLUG, LID_T = 2.0, 1.5
BODY_H = 23.0

# Deckel/Flamme
LID_RING_H, LID_RIB = 3.0, 0.10  # Klemmring: Höhe, radiales Übermaß der Rippen
LED_D = 6.2
FLAME_D, FLAME_H, GROOVE = 12.0, 24.0, 0.8

# Sockel
BASE_OD, BASE_H, BASE_TOP = 52.0, 9.0, 1.2
BASE_WALL = 2.0
CABLE_D = 4.2                 # USB-Kabel, ANGESETZT, bitte messen


def cyl(d, h, z=0):
    return cq.Workplane("XY").workplane(offset=z).circle(d / 2).extrude(h)


def box(x, y, z0, z1, cx=0, cy=0):
    return (cq.Workplane("XY").workplane(offset=z0).center(cx, cy)
            .rect(x, y).extrude(z1 - z0))


def pogo_cut(top):
    """Außen schmaler Stadion-Schlitz, innen Tasche; der Flansch liegt auf der Stufe."""
    slot = (cq.Workplane("XY").workplane(offset=-1).center(0, POGO_Y)
            .slot2D(POGO_FRONT_W + CLEAR, POGO_H + CLEAR).extrude(POGO_FRONT_D + 1))
    return slot.union(box(POGO_W + CLEAR, POGO_H + CLEAR, POGO_FRONT_D, top, cy=POGO_Y))


def body():
    b = cyl(OD, BODY_H).cut(cyl(ID, BODY_H, FLOOR))
    b = b.faces("<Z").edges().chamfer(0.5)
    inner = cyl(ID + 0.2, BODY_H)
    # Pogo-Rahmen führt die Buchse beim Einkleben
    frame = box(POGO_W + 3.3, POGO_H + 3.3, FLOOR, POGO_D + 0.2, cy=POGO_Y)
    frame = frame.cut(box(POGO_W + 3.4, 4.2, FLOOR + 0.01, BODY_H, cy=POGO_Y)).union(
        frame.intersect(box(POGO_W + CLEAR, POGO_H + 3.4, 0, BODY_H, cy=POGO_Y)))
    # Zwei Auflageschienen und Eckanschläge für den Akku
    bx, by = BAT[0] + CLEAR * 2 + BAT_EXTRA_L, BAT[1] + CLEAR * 2
    rails = (box(bx - 2, 2.5, FLOOR, SHELF_Z, cy=7.75)
             .union(box(bx - 2, 2.5, FLOOR, SHELF_Z, cy=-7.75)))
    stops = cq.Workplane("XY")
    first = True
    for sx in (-1, 1):
        for sy in (-1, 1):
            s = box(5, 5, FLOOR, SHELF_Z, sx * (bx / 2 - 1.5), sy * (by / 2 - 1.5))
            if (sx, sy) != BAT_CABLE_CORNER:  # dort läuft das Akkukabel heraus
                s = s.union(box(4, 4, FLOOR, SHELF_Z + BAT[2] - 1,
                                sx * (bx / 2 - 1.2), sy * (by / 2 - 1.2)))
            s = s.cut(box(bx, by, SHELF_Z, BODY_H))
            stops = s if first else stops.union(s)
            first = False
    inside = frame.union(rails).union(stops).intersect(inner)
    # Litzenkanal quer durch die Schienen
    b = b.union(inside)
    b = b.cut(box(5, 40, FLOOR + 0.0, SHELF_Z - 1.5))
    b = b.cut(pogo_cut(BODY_H))
    return b.union(pogo_snaps())


def pogo_snaps():
    """Zwei Rasthaken an den Stirnseiten, greifen über die Flanschohren."""
    edge = (POGO_W + CLEAR) / 2
    t, w, top = SNAP_T, 3.0, POGO_D + 2.0
    out = None
    for sx in (-1, 1):
        # Rahmen-Stirnwand entfernen, damit der Arm frei federn kann
        arm = box(t, w, FLOOR, top, sx * (edge + t / 2), POGO_Y)
        hook = (cq.Workplane("XZ").polyline([
            (edge, POGO_D + 0.05), (edge - SNAP_HOOK, POGO_D + 0.05),
            (edge - SNAP_HOOK, POGO_D + 0.45), (edge, top)]).close()
            .extrude(w / 2, both=True).translate((0, POGO_Y, 0)))
        if sx < 0:
            hook = hook.mirror("YZ")
        s = arm.union(hook)
        out = s if out is None else out.union(s)
    return out


def lid():
    """v11: geschlitzter Klemmring, passend zum unveränderten Korpus."""
    plate = cyl(OD, LID_T).faces(">Z").edges().fillet(0.6)
    h = LID_RING_H
    ring = cyl(ID - 0.3, h, -h).cut(cyl(ID - 2.3, h, -h))
    for angle in range(0, 360, 60):
        ring = ring.cut(box(5, 1.2, -h - 0.1, 0.01, ID / 2, 0).rotate((0, 0, 0), (0, 0, 1), angle))
    # Klemmrippen mit Einführschräge, Übermaß separat einstellbar
    for angle in range(30, 360, 60):
        rib = (cq.Workplane("XZ").polyline([
            (ID / 2 - 0.3, -h + 0.3), (ID / 2 - 0.15, -h + 0.3),
            (ID / 2 + LID_RIB, -h + 1.5), (ID / 2 + LID_RIB, -h + 2.2),
            (ID / 2 - 0.15, -h + 2.7), (ID / 2 - 0.3, -h + 2.7)]).close()
            .revolve(16, (0, 0, 0), (0, 1, 0))
            .rotate((0, 0, 0), (0, 0, 1), angle - 8))
        ring = ring.union(rib)
    l = plate.union(ring).cut(cyl(LED_D, LID_T + 1, -0.5))
    groove = cyl(FLAME_D + 0.5, GROOVE, LID_T - GROOVE).cut(
        cyl(FLAME_D - 1.5, GROOVE, LID_T - GROOVE))
    return l.cut(groove)


def flame():
    r = FLAME_D / 2
    pts = [(r - 0.1, 3), (r + 0.5, 7), (r - 1.0, 14), (1.6, 21)]
    prof = (cq.Workplane("XZ").moveTo(0, 0).lineTo(r, 0).lineTo(r, 1.0)
            .spline(pts, includeCurrent=True).lineTo(0.2, FLAME_H).lineTo(0, FLAME_H).close())
    return prof.revolve(360, (0, 0, 0), (0, 1, 0))


def base():
    """Gedruckt mit der Oberseite aufs Bett (z=0 ist die Standfläche der Kerze)."""
    h, w = BASE_H, BASE_WALL
    b = cyl(BASE_OD, h).cut(cyl(BASE_OD - 2 * w, h, BASE_TOP))
    b = b.faces("<Z").edges().chamfer(0.5)
    b = b.union(box(POGO_W + 3.3, POGO_H + 3.3, BASE_TOP, POGO_D + 0.2, cy=POGO_Y))
    b = b.cut(pogo_cut(POGO_D + 1))
    # Kabel wird von unten in die Kerbe gelegt, Zugentlastung per Kabelbinder um die Stege
    x_wall = -(BASE_OD / 2 - w)
    posts = (box(3, 2.5, BASE_TOP, h - 1.5, x_wall + 7, CABLE_D / 2 + 2.5)
             .union(box(3, 2.5, BASE_TOP, h - 1.5, x_wall + 7, -CABLE_D / 2 - 2.5)))
    b = b.union(posts)
    return b.cut(cable_notch(h))


def cable_notch(top):
    d = CABLE_D
    r = (cq.Workplane("XY").workplane(offset=top - d / 2).center(-BASE_OD / 2, 0)
         .rect(BASE_WALL * 2 + 2, d).extrude(d / 2 + 1))
    c = (cq.Workplane("YZ").workplane(offset=-BASE_OD / 2 - BASE_WALL)
         .center(0, top - d / 2).circle(d / 2).extrude(BASE_WALL * 2 + 1))
    return r.union(c)


def base_cover():
    """v10: geschlitzter Klemmring, passend zum unveränderten v9-Sockel."""
    d = BASE_OD - 2 * BASE_WALL
    p = cyl(BASE_OD, 1.2)
    # Sechs voneinander getrennte Segmente, nur an der Bodenplatte verbunden.
    ring = cyl(d - 0.3, 3.0, -3.0).cut(cyl(d - 2.3, 3.0, -3.0))
    for angle in range(0, 360, 60):
        slit = box(5, 1.2, -3.1, 0.01, d / 2, 0).rotate((0,0,0),(0,0,1),angle)
        ring = ring.cut(slit)
    # Kurze Klemmrippen mit Einführschräge: 0,10 mm radiales Übermaß.
    for angle in range(30, 360, 60):
        rib = (cq.Workplane("XZ").polyline([
            (d/2-0.3,-2.7), (d/2-0.15,-2.7),
            (d/2+0.10,-1.5), (d/2+0.10,-0.8),
            (d/2-0.15,-0.3), (d/2-0.3,-0.3)]).close()
            .revolve(16,(0,0,0),(0,1,0))
            .rotate((0,0,0),(0,0,1),angle-8))
        ring = ring.union(rib)
    ring = ring.cut(box(8, CABLE_D + 0.6, -3.1, 0.01, -d / 2, 0))
    return p.union(ring)


PARTS = {"korpus": body, "deckel": lid, "flamme": flame, "sockel": base,
         "sockel-boden": base_cover}

if __name__ == "__main__":
    out = Path(__file__).parent / "out"
    out.mkdir(exist_ok=True)
    for name, fn in PARTS.items():
        s = fn()
        cq.exporters.export(s, str(out / f"teelicht-{name}.stl"), tolerance=0.02, angularTolerance=0.1)
        cq.exporters.export(s, str(out / f"teelicht-{name}.step"))
        v = s.val()
        bb = v.BoundingBox()
        print(f"{name:13} valid={v.isValid()} solids={len(s.solids().vals())} "
              f"{bb.xlen:.1f}x{bb.ylen:.1f}x{bb.zlen:.1f} vol={v.Volume():.0f}")
