#!/usr/bin/env python3
"""EN04 wall enclosure V4 - two parts, EN04 component side facing the display.

Why V4 exists
-------------
V1-V3 used a three-part stack (bezel / carrier / back cover) with the EN04
mounted component side towards the REAR cover. J2, the 24-pin FPC connector,
sits on the component side (KiCad layer F). With the component side facing the
rear, the panel FPC had to pass through the carrier slot to the back and then
wrap around the board's top edge to reach the contacts - two 180 degree folds in
3.4 mm of space. No slot position can fix that; the concept itself was wrong.

V4 turns the board over about the global Y axis so the component side, and with
it J2, faces the display. The FPC now runs from the panel rear in a single gentle
S-bend straight into J2. The carrier plate disappears entirely - there is no
longer anything between panel and board, so no FPC slot is needed at all.

Flipping about Y mirrors the board in global X while J2 keeps pointing towards
+Y (up, at the panel) and the user controls stay on the bottom edge:

    hole/feature X = BOARD_X + BOARD_W - kicad_y      (was BOARD_X + kicad_y)
    hole/feature Y = BOARD_Y + kicad_x                (unchanged)

That shift moves the board left. To keep all four board posts clear of the case
screw bosses the enclosure grows from 110 to 116 mm wide and the panel is
centred, which also makes the whole design symmetric about X - so a mirrored
assembly can no longer introduce an offset.

Coordinate system: view from the BACK. X right, Y up, Z from the bezel's front
face towards the wall. All dimensions in millimetres.
"""

from pathlib import Path

import numpy as np
import trimesh

OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)

# --- Panel (GDEY042T81, landscape, FPC on the bottom edge) ----------------------
PANEL_W, PANEL_H, PANEL_T = 91.0, 77.0, 1.9
ACTIVE_W, ACTIVE_H = 84.8, 63.6
ACTIVE_DX, ACTIVE_DY = 3.1, 10.3        # side margin / FPC-edge margin
FPC_FROM_LEFT = 46.5                     # confirmed by Carsten: measured from the left edge
FPC_WIDTH = 20.0

# --- EN04 V1.2 (from ref/en04_layout_from_kicad.md) ----------------------------
BOARD_W, BOARD_H, BOARD_T = 80.0, 41.23, 1.6   # KiCad y -> X, KiCad x -> Y
KICAD_HOLES = [(2.47, 2.55), (38.68, 2.55), (2.47, 77.46), (38.68, 77.46)]
J2_Y = (22.34, 37.84)
USB_Y = 14.38
BUTTON_Y = [31.59, 40.93, 50.26]
SWITCH_Y = (65.16, 74.16)
COMP_Z_USB, COMP_Z_BTN, COMP_Z_SW = (0.0, 3.4), (0.0, 4.5), (0.0, 3.6)
COMP_MAX_H = 4.5                          # tallest part on the component side

BAT_W, BAT_H, BAT_T = 34.0, 50.0, 10.0
BAT_CLEARANCE = 0.6

# --- Enclosure -----------------------------------------------------------------
WALL, FRONT_T = 2.0, 2.2
CORNER_R = 4.0
BOSS_R, BOSS_H = 3.0, 4.0                 # bezel screw bosses, 4 mm thread engagement
PILOT_R, SHANK_R = 0.8, 1.2

CASE_W = 116.0
PANEL_X = (CASE_W - PANEL_W) / 2          # 12.5 -> panel centred, design symmetric in X
FPC_X = PANEL_X + FPC_FROM_LEFT           # 59.0
BOARD_Y = WALL + 0.2                      # connectors just inside the bottom wall
PANEL_Y = BOARD_Y + BOARD_H + 3.4         # 3.4 mm for the FPC S-bend
CASE_H = PANEL_Y + PANEL_H + 6.0

J2_CENTER = (J2_Y[0] + J2_Y[1]) / 2
BOARD_X = FPC_X - (BOARD_W - J2_CENTER)   # flipped mapping aligns J2 with the FPC
BOARD_HOLES = [(BOARD_X + BOARD_W - ky, BOARD_Y + kx) for kx, ky in KICAD_HOLES]


def flip_x(kicad_y):
    """Global X of a board feature after the 180 degree flip about Y."""
    return BOARD_X + BOARD_W - kicad_y


CASE_SCREWS = [(5.0, 5.0), (CASE_W - 5.0, 5.0), (5.0, CASE_H - 5.0), (CASE_W - 5.0, CASE_H - 5.0)]

# --- Z stack -------------------------------------------------------------------
Z_PANEL_FRONT = FRONT_T                   # 2.20
Z_PANEL_REAR = FRONT_T + PANEL_T          # 4.10
GUIDE_H = PANEL_T + 0.7
Z_GUIDE_TOP = FRONT_T + GUIDE_H           # 4.80
Z_BOSS_TOP = FRONT_T + BOSS_H             # 6.20
Z_COMP = 8.0                              # board component face, components point at -Z
Z_BOARD_REAR = Z_COMP + BOARD_T           # 9.60
Z_REAR_IN = 20.0
Z_REAR_OUT = Z_REAR_IN + 2.0              # 22.0 total depth
Z_RIM = FRONT_T                           # shell seam sits on the bezel's inner face

FLANGE_Z0, FLANGE_Z1 = 4.9, 7.3           # panel retainer, clears the bezel guides
FLANGE_OVERLAP = 2.0                      # how far it reaches over the panel border

BAT_X = (CASE_W - BAT_W) / 2
BAT_Y = PANEL_Y + 14.0
KEYHOLE_X = (25.0, CASE_W - 25.0)
KEYHOLE_Y = PANEL_Y + 30.0


# --- primitives ----------------------------------------------------------------
def moved(mesh, xyz):
    mesh = mesh.copy()
    mesh.apply_translation(xyz)
    return mesh


def box(x, y, z, sx, sy, sz):
    return moved(trimesh.creation.box((sx, sy, sz)), (x + sx / 2, y + sy / 2, z + sz / 2))


def cylinder(x, y, z, radius, height, sections=48):
    return moved(trimesh.creation.cylinder(radius=radius, height=height, sections=sections),
                 (x, y, z + height / 2))


def union(items):
    return trimesh.boolean.union([i for i in items if i is not None], engine="manifold")


def difference(base, cutters):
    return trimesh.boolean.difference([base, *[c for c in cutters if c is not None]], engine="manifold")


def rounded_box(w, h, d, radius, z=0.0, x=0.0, y=0.0):
    parts = [box(x + radius, y, z, w - 2 * radius, h, d),
             box(x, y + radius, z, w, h - 2 * radius, d)]
    for cx in (x + radius, x + w - radius):
        for cy in (y + radius, y + h - radius):
            parts.append(cylinder(cx, cy, z, radius, d))
    return union(parts)


# --- part 1: front bezel -------------------------------------------------------
def front_bezel():
    body = rounded_box(CASE_W, CASE_H, FRONT_T, CORNER_R)
    ax, ay = PANEL_X + ACTIVE_DX, PANEL_Y + ACTIVE_DY
    body = difference(body, [box(ax - 0.25, ay - 0.25, -0.2, ACTIVE_W + 0.5, ACTIVE_H + 0.5, FRONT_T + 0.4)])

    gt_thk, cl = 0.8, 0.5
    gl = PANEL_X - cl - gt_thk
    gr = PANEL_X + PANEL_W + cl
    gb = PANEL_Y - cl - gt_thk
    gt = PANEL_Y + PANEL_H + cl
    outer_w = PANEL_W + 2 * (cl + gt_thk)
    gap = (FPC_X - FPC_WIDTH / 2 - 4.0, FPC_X + FPC_WIDTH / 2 + 4.0)   # 28 mm, generous
    guides = [
        box(gl, gt, FRONT_T, outer_w, gt_thk, GUIDE_H),
        box(gl, PANEL_Y, FRONT_T, gt_thk, PANEL_H, GUIDE_H),
        box(gr, PANEL_Y, FRONT_T, gt_thk, PANEL_H, GUIDE_H),
        box(gl, gb, FRONT_T, gap[0] - gl, gt_thk, GUIDE_H),
        box(gap[1], gb, FRONT_T, gr + gt_thk - gap[1], gt_thk, GUIDE_H),
    ]
    bosses = [difference(cylinder(x, y, FRONT_T, BOSS_R, BOSS_H),
                         [cylinder(x, y, FRONT_T - 0.1, PILOT_R, BOSS_H + 0.2)])
              for x, y in CASE_SCREWS]
    return union([body, *guides, *bosses])


# --- part 2: back shell (carrier + back cover merged) --------------------------
def back_shell():
    outer = rounded_box(CASE_W, CASE_H, Z_REAR_OUT - Z_RIM, CORNER_R, z=Z_RIM)
    inner = rounded_box(CASE_W - 2 * WALL, CASE_H - 2 * WALL, Z_REAR_IN - Z_RIM,
                        max(1.0, CORNER_R - WALL), z=Z_RIM, x=WALL, y=WALL)
    shell = difference(outer, [inner])

    # Panel retainer: frame on three sides. The bottom stays open for the FPC.
    px0, px1 = PANEL_X, PANEL_X + PANEL_W
    py1 = PANEL_Y + PANEL_H
    fz = FLANGE_Z1 - FLANGE_Z0
    flange = union([
        box(WALL, PANEL_Y, FLANGE_Z0, px0 + FLANGE_OVERLAP - WALL, PANEL_H, fz),
        box(px1 - FLANGE_OVERLAP, PANEL_Y, FLANGE_Z0, CASE_W - WALL - (px1 - FLANGE_OVERLAP), PANEL_H, fz),
        box(WALL, py1 - FLANGE_OVERLAP, FLANGE_Z0, CASE_W - 2 * WALL, CASE_H - WALL - (py1 - FLANGE_OVERLAP), fz),
    ])
    flange = difference(flange, [cylinder(x, y, FLANGE_Z0 - 0.2, BOSS_R + 0.3, fz + 0.4)
                                 for x, y in CASE_SCREWS])
    shell = union([shell, flange])

    # Bottom-wall openings. Components sit on the board's display-facing side, so
    # they occupy Z from Z_COMP towards -Z.
    def bottom_cut(x0, x1, comp_z, mx=1.0, mz=1.0):
        z_lo = Z_COMP - comp_z[1] - mz
        z_hi = Z_COMP - comp_z[0] + mz
        return box(x0 - mx, -0.5, z_lo, (x1 - x0) + 2 * mx, WALL + 1.0, z_hi - z_lo)

    cuts = [bottom_cut(flip_x(USB_Y) - 4.5, flip_x(USB_Y) + 4.5, COMP_Z_USB, mx=1.5),
            bottom_cut(min(flip_x(SWITCH_Y[0]), flip_x(SWITCH_Y[1])),
                       max(flip_x(SWITCH_Y[0]), flip_x(SWITCH_Y[1])), COMP_Z_SW)]
    for by in BUTTON_Y:
        cuts.append(bottom_cut(flip_x(by) - 2.25, flip_x(by) + 2.25, COMP_Z_BTN))
    shell = difference(shell, cuts)

    # Keyholes in the rear plate.
    keys = []
    for x in KEYHOLE_X:
        keys.append(cylinder(x, KEYHOLE_Y, Z_REAR_IN - 0.2, 4.0, 2.4))
        keys.append(box(x - 2.0, KEYHOLE_Y, Z_REAR_IN - 0.2, 4.0, 11.0, 2.4))
    shell = difference(shell, keys)

    # Case screw tubes: run from the rear plate forward onto the bezel bosses.
    tubes = []
    for x, y in CASE_SCREWS:
        tube = cylinder(x, y, Z_BOSS_TOP, BOSS_R, Z_REAR_IN - Z_BOSS_TOP)
        tubes.append(difference(tube, [cylinder(x, y, Z_BOSS_TOP - 0.2, SHANK_R, Z_REAR_IN - Z_BOSS_TOP + 0.4)]))
    shell = difference(shell, [cylinder(x, y, Z_REAR_IN - 0.2, SHANK_R, 2.4) for x, y in CASE_SCREWS])

    # EN04 posts: board rests on them, component side towards the display.
    posts = []
    post_h = Z_REAR_IN - Z_BOARD_REAR
    for x, y in BOARD_HOLES:
        # 3.8 mm flare deliberately merges with the nearby case screw tube
        # (centres 6.64 mm apart) instead of leaving an unprintable 0.14 mm gap.
        stack = union([cylinder(x, y, Z_BOARD_REAR, 2.0, post_h),
                       cylinder(x, y, Z_REAR_IN - 6.0, 3.8, 6.0)])
        posts.append(difference(stack, [cylinder(x, y, Z_BOARD_REAR - 0.1, PILOT_R, 8.0)]))

    # Battery cradle on the rear plate, behind the panel and clear of the keyholes.
    bw, bh, rt, rh = BAT_W + BAT_CLEARANCE, BAT_H + BAT_CLEARANCE, 1.5, 3.5
    rails = [box(BAT_X - rt, BAT_Y - rt, Z_REAR_IN - rh, rt, bh + 2 * rt, rh),
             box(BAT_X + bw, BAT_Y - rt, Z_REAR_IN - rh, rt, bh + 2 * rt, rh),
             box(BAT_X, BAT_Y + bh, Z_REAR_IN - rh, bw, rt, rh)]
    return union([shell, *tubes, *posts, *rails])


# --- checks and export ---------------------------------------------------------
def check():
    assert abs((BOARD_X + BOARD_W - J2_CENTER) - FPC_X) < 1e-6, "J2 not aligned with the FPC"
    assert abs(PANEL_X - (CASE_W - PANEL_W - PANEL_X)) < 1e-6, "panel not centred"
    left_boss = CASE_SCREWS[0][0] + BOSS_R
    assert BOARD_X > left_boss + 0.5, f"board {BOARD_X:.2f} clashes with left boss {left_boss:.2f}"
    assert BOARD_X + BOARD_W < CASE_SCREWS[1][0] - BOSS_R - 0.5, "board clashes with right boss"
    assert BOARD_Y + BOARD_H < PANEL_Y, "board overlaps the panel"
    assert Z_COMP - COMP_MAX_H > FRONT_T + 0.5, "components hit the bezel face"
    assert Z_BOARD_REAR + BAT_T <= Z_REAR_IN, "battery does not fit behind the board plane"
    assert BAT_X > KEYHOLE_X[0] + 4.5 and BAT_X + BAT_W < KEYHOLE_X[1] - 4.5, "battery overlaps keyholes"
    for hx, hy in BOARD_HOLES:
        for sx, sy in CASE_SCREWS:
            d = ((hx - sx) ** 2 + (hy - sy) ** 2) ** 0.5
            assert d > 2 * BOSS_R + 0.5, f"board post at ({hx:.2f},{hy:.2f}) too close to case boss ({sx},{sy}): {d:.2f} mm"


def export(name, mesh):
    mesh.remove_unreferenced_vertices()
    if not mesh.is_watertight:
        raise RuntimeError(f"{name} is not watertight")
    if mesh.volume <= 0:
        raise RuntimeError(f"{name} has invalid volume")
    if len(mesh.split(only_watertight=False)) != 1:
        raise RuntimeError(f"{name} is not a single body")
    mesh.export(OUT / f"{name}.stl")
    print(f"  {name}: {len(mesh.faces)} faces, {mesh.volume / 1000:.1f} cm^3, "
          f"bounds={np.round(mesh.bounds, 2).tolist()}")


def main():
    check()
    print(f"case {CASE_W} x {CASE_H:.2f} mm, total depth {Z_REAR_OUT:.1f} mm")
    print(f"panel X {PANEL_X:.2f}..{PANEL_X + PANEL_W:.2f} (centred), FPC centre X {FPC_X:.2f}")
    print(f"board X {BOARD_X:.2f}..{BOARD_X + BOARD_W:.2f}, Y {BOARD_Y:.2f}..{BOARD_Y + BOARD_H:.2f}")
    print(f"J2 centre X {BOARD_X + BOARD_W - J2_CENTER:.2f}  (= FPC centre)")
    print(f"USB-C X {flip_x(USB_Y):.2f}; buttons X {[round(flip_x(b), 2) for b in BUTTON_Y]}; "
          f"switch X {flip_x(SWITCH_Y[1]):.2f}..{flip_x(SWITCH_Y[0]):.2f}")
    print(f"board posts {[(round(x, 2), round(y, 2)) for x, y in BOARD_HOLES]}")
    export("en04_front_bezel_v4", front_bezel())
    export("en04_back_shell_v4", back_shell())


if __name__ == "__main__":
    main()
