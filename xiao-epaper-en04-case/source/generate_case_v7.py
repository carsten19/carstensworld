#!/usr/bin/env python3
"""EN04 wall enclosure V7 - the display is retained by the front chassis itself.

V7 changes against V6:
- Rear-cover panel flange removed. It never touched the panel (0.8 mm air gap,
  only foam made contact) and needed support.
- Front chassis: fixed undercut lips on the lower panel edge (both sides of the
  FPC gap) plus two screwed clamp tabs on the upper left/right panel edges.
  Snap hooks were rejected: the hook would sit 2 mm above its root, PLA would
  need >5 % strain for the required deflection.
- Separate part: clamp tab (print 2x).

V6 notes:

V6 changes against V5 (all in the rear cover):
- USB-C opening runs down to the parting line; the thin 1.4 mm web in front
  of the plug is gone.
- Cut-out for the fourth side button SW2 (RESET), missing in V5.
- Counterbores for the four M2 pan-head case screws, so the heads sit below
  the rear face and cannot scratch a table.

Original V5 notes:

V5 uses the measured, actually connected panel/EN04 arrangement as its source
of truth.  The display and EN04 are mounted to the same front chassis; the rear
shell only retains the panel, carries the battery and provides wall mounting.

Coordinate system: view from the BACK. X right, Y up, Z from the visible front
face towards the wall. Dimensions are millimetres.
"""

from pathlib import Path

import numpy as np

import generate_case_v4 as g

OUT = Path(__file__).resolve().parent / "output"

# Physical parts
PANEL_W, PANEL_H, PANEL_T = 91.0, 77.0, 1.9
ACTIVE_W, ACTIVE_H = 84.8, 63.6
ACTIVE_DX, ACTIVE_DY = 3.1, 10.3
FPC_FROM_LEFT, FPC_WIDTH = 46.5, 20.0

BOARD_W, BOARD_H, BOARD_T = 80.0, 41.23, 1.6
KICAD_HOLES = [(2.47, 2.55), (38.68, 2.55), (2.47, 77.46), (38.68, 77.46)]
J2_Y = (22.34, 37.84)
USB_Y = 14.38
BUTTON_Y = [31.59, 40.93, 50.26, 59.60]   # SW3, SW4, SW5, SW2 = RESET (KiCad)
SWITCH_Y = (65.16, 74.16)
COMP_Z_USB, COMP_Z_BTN, COMP_Z_SW = (0.0, 3.4), (0.0, 4.5), (0.0, 3.6)
COMP_MAX_H = 4.5

BAT_W, BAT_H, BAT_T = 34.0, 50.0, 10.0
BAT_CLEARANCE = 0.8

# Enclosure dimensions from Carsten's connected physical mock-up.
WALL, FRONT_T = 2.0, 2.2
CORNER_R = 4.0
BOSS_R, BOSS_H = 3.0, 4.0
PILOT_R, SHANK_R = 0.8, 1.2

# M2 pan-head (Linsenkopf) case screws, DIN 7985: head 4.0 mm, height 1.6 mm.
SCREW_LEN = 16.0
HEAD_D, HEAD_K = 4.0, 1.6
CBORE_R = HEAD_D / 2 + 0.4             # printable clearance
TUBE_R = CBORE_R + 1.4                 # tube wall around the counterbore

CASE_W = 128.0
BOARD_X = 37.0                         # old right edge at x=111, +6 mm symmetric widening
BOARD_Y = 2.0                          # PCB edge just inside lower wall openings
PANEL_X = (CASE_W - PANEL_W) / 2       # 18.5, panel remains centred
PANEL_Y = BOARD_Y + BOARD_H + 14.0     # measured PCB-to-panel gap
CASE_H = PANEL_Y + PANEL_H + 6.0       # same 6 mm upper margin
FPC_X = PANEL_X + FPC_FROM_LEFT        # panel attachment, not the free contact end

J2_CENTER_LOCAL = BOARD_W - ((J2_Y[0] + J2_Y[1]) / 2)
J2_X = BOARD_X + J2_CENTER_LOCAL       # free contact position in connected mock-up
BOARD_HOLES = [(BOARD_X + BOARD_W - ky, BOARD_Y + kx) for kx, ky in KICAD_HOLES]


def flip_x(kicad_y):
    return BOARD_X + BOARD_W - kicad_y


CASE_SCREWS = [(5.0, 5.0), (CASE_W - 5.0, 5.0),
               (5.0, CASE_H - 5.0), (CASE_W - 5.0, CASE_H - 5.0)]

# Z stack. The PCB now rests on posts printed on the front chassis.
Z_PANEL_FRONT = FRONT_T
Z_PANEL_REAR = FRONT_T + PANEL_T
GUIDE_H = PANEL_T + 0.7
Z_BOSS_TOP = FRONT_T + BOSS_H
Z_COMP = 8.0                           # PCB component face; parts project towards -Z
Z_BOARD_REAR = Z_COMP + BOARD_T
Z_REAR_IN = 20.0
Z_REAR_OUT = 22.0
Z_RIM = FRONT_T

# Panel retention in the front chassis.
LIP_OVERLAP, LIP_GAP, LIP_T = 0.8, 0.2, 1.0   # lower lips over the panel edge
CLAMP_T, CLAMP_W, CLAMP_OVER = 1.6, 10.0, 1.5 # clamp tab thickness, width, panel overlap
CLAMP_PRELOAD = 0.1                           # nose reaches 0.1 mm below panel rear
CLAMP_DOME_R = 2.4
CLAMP_DX = 4.5                                # dome centre outside the panel edge
CLAMP_Y = None                                # set after PANEL_Y is known
CLAMP_PILOT_Z0 = 0.8                          # 0.8 mm front skin stays closed

# Screw seat depth: M2x16 tip ends 0.5 mm above the pilot-hole bottom.
Z_PILOT_BOTTOM = FRONT_T - 0.1
Z_SEAT = Z_PILOT_BOTTOM + 0.5 + SCREW_LEN

BAT_X = (CASE_W - BAT_W) / 2
BAT_Y = PANEL_Y + 14.0
KEYHOLE_X = (27.0, CASE_W - 27.0)
KEYHOLE_Y = PANEL_Y + 30.0
CLAMP_Y = PANEL_Y + PANEL_H - 14.0
CLAMPS = [(PANEL_X - CLAMP_DX, CLAMP_Y, +1), (PANEL_X + PANEL_W + CLAMP_DX, CLAMP_Y, -1)]
Z_GUIDE_TOP = FRONT_T + GUIDE_H


def front_chassis():
    body = g.rounded_box(CASE_W, CASE_H, FRONT_T, CORNER_R)
    ax, ay = PANEL_X + ACTIVE_DX, PANEL_Y + ACTIVE_DY
    body = g.difference(body, [g.box(ax - 0.25, ay - 0.25, -0.2,
                                     ACTIVE_W + 0.5, ACTIVE_H + 0.5, FRONT_T + 0.4)])

    # Panel guides. The lower gap covers the complete real FPC side-step from
    # the panel attachment to J2, rather than only the attachment centre.
    gt_thk, cl = 0.8, 0.5
    gl = PANEL_X - cl - gt_thk
    gr = PANEL_X + PANEL_W + cl
    gb = PANEL_Y - cl - gt_thk
    gt = PANEL_Y + PANEL_H + cl
    outer_w = PANEL_W + 2 * (cl + gt_thk)
    gap_x0 = min(FPC_X, J2_X) - FPC_WIDTH / 2 - 4.0
    gap_x1 = max(FPC_X, J2_X) + FPC_WIDTH / 2 + 4.0
    guides = [
        g.box(gl, gt, FRONT_T, outer_w, gt_thk, GUIDE_H),
        g.box(gl, PANEL_Y, FRONT_T, gt_thk, PANEL_H, GUIDE_H),
        g.box(gr, PANEL_Y, FRONT_T, gt_thk, PANEL_H, GUIDE_H),
        g.box(gl, gb, FRONT_T, gap_x0 - gl, gt_thk, GUIDE_H),
        g.box(gap_x1, gb, FRONT_T, gr + gt_thk - gap_x1, gt_thk, GUIDE_H),
    ]

    case_bosses = [g.difference(g.cylinder(x, y, FRONT_T, BOSS_R, BOSS_H),
                                 [g.cylinder(x, y, FRONT_T - 0.1, PILOT_R, BOSS_H + 0.2)])
                   for x, y in CASE_SCREWS]

    # EN04 posts are part of the front chassis. The board is fitted only after
    # the FPC is connected, so no open-book assembly or cable tension is needed.
    post_h = Z_COMP - FRONT_T
    board_posts = [g.difference(g.cylinder(x, y, FRONT_T, 2.2, post_h),
                                [g.cylinder(x, y, FRONT_T - 0.1, PILOT_R, post_h + 0.2)])
                   for x, y in BOARD_HOLES]
    # Lower lips: fixed undercut on both guide segments beside the FPC gap.
    # Insert the panel bottom edge first at a slight angle, then lay it down.
    lz0 = Z_PANEL_REAR + LIP_GAP
    lip_y0 = gb
    lip_len = PANEL_Y + LIP_OVERLAP - lip_y0
    lips = [g.box(gl + gt_thk, lip_y0, lz0, gap_x0 - gl - gt_thk, lip_len, LIP_T),
            g.box(gap_x1, lip_y0, lz0, gr - gap_x1, lip_len, LIP_T),
            # Wall under the lips so they are anchored and printable.
            g.box(gl, gb, FRONT_T, gap_x0 - gl, gt_thk, lz0 + LIP_T - FRONT_T),
            g.box(gap_x1, gb, FRONT_T, gr + gt_thk - gap_x1, gt_thk, lz0 + LIP_T - FRONT_T)]

    # Clamp domes: top flush with the guides, pilot for M2x5 self-tapping.
    clamp_domes = [g.difference(g.cylinder(x, y, FRONT_T, CLAMP_DOME_R, GUIDE_H),
                                [g.cylinder(x, y, CLAMP_PILOT_Z0, PILOT_R,
                                            Z_GUIDE_TOP - CLAMP_PILOT_Z0 + 0.2)])
                   for x, y, _ in CLAMPS]
    return g.union([body, *guides, *lips, *case_bosses, *board_posts, *clamp_domes])


def clamp_tab():
    """Clamp tab in print orientation: flat side on the bed, nose pointing up.

    Installed flipped: the flat side faces the rear cover, the nose presses on
    the panel rear face. X runs from the screw hole towards the panel.
    """
    reach = CLAMP_DX + CLAMP_OVER                  # dome centre to nose tip
    x0 = -CLAMP_DOME_R - 0.5
    body = g.box(x0, -CLAMP_W / 2, 0, reach - x0, CLAMP_W, CLAMP_T)
    # Nose: steps down from guide top to the panel rear face (+ small preload).
    nose_h = Z_GUIDE_TOP - Z_PANEL_REAR + CLAMP_PRELOAD
    guide_outer = CLAMP_DX - 0.5 - 0.8             # x of guide outer face
    nose_x0 = CLAMP_DX - 0.5 + 0.1                 # just inside the guide inner face
    nose = g.box(nose_x0, -CLAMP_W / 2, CLAMP_T - 0.01, reach - nose_x0, CLAMP_W, nose_h + 0.01)
    tab = g.union([body, nose])
    tab = g.difference(tab, [g.cylinder(0, 0, -0.2, 1.2, CLAMP_T + nose_h + 0.4)])
    assert guide_outer > CLAMP_DOME_R, "clamp dome hits guide"
    return tab


def rear_shell():
    outer = g.rounded_box(CASE_W, CASE_H, Z_REAR_OUT - Z_RIM, CORNER_R, z=Z_RIM)
    inner = g.rounded_box(CASE_W - 2 * WALL, CASE_H - 2 * WALL,
                          Z_REAR_IN - Z_RIM, max(1.0, CORNER_R - WALL),
                          z=Z_RIM, x=WALL, y=WALL)
    shell = g.difference(outer, [inner])

    # Bottom-wall access for USB-C, power switch and four buttons.
    def bottom_cut(x0, x1, comp_z, mx=1.0, mz=1.0):
        z_lo = Z_COMP - comp_z[1] - mz
        z_hi = Z_COMP - comp_z[0] + mz
        return g.box(x0 - mx, -0.5, z_lo, (x1 - x0) + 2 * mx, WALL + 1.0, z_hi - z_lo)

    # USB-C: open down to the parting line (Z_RIM); the front chassis closes it.
    usb = bottom_cut(flip_x(USB_Y) - 4.5, flip_x(USB_Y) + 4.5, COMP_Z_USB, mx=1.5)
    usb_z_hi = usb.bounds[1][2]
    usb = g.box(usb.bounds[0][0], -0.5, Z_RIM - 0.5, usb.bounds[1][0] - usb.bounds[0][0],
                WALL + 1.0, usb_z_hi - (Z_RIM - 0.5))
    cuts = [usb,
            bottom_cut(min(flip_x(SWITCH_Y[0]), flip_x(SWITCH_Y[1])),
                       max(flip_x(SWITCH_Y[0]), flip_x(SWITCH_Y[1])), COMP_Z_SW)]
    cuts.extend(bottom_cut(flip_x(by) - 2.25, flip_x(by) + 2.25, COMP_Z_BTN)
                for by in BUTTON_Y)
    shell = g.difference(shell, cuts)

    # Wall keyholes.
    keys = []
    for x in KEYHOLE_X:
        keys.append(g.cylinder(x, KEYHOLE_Y, Z_REAR_IN - 0.2, 4.0, 2.4))
        keys.append(g.box(x - 2.0, KEYHOLE_Y, Z_REAR_IN - 0.2, 4.0, 11.0, 2.4))
    shell = g.difference(shell, keys)

    # Rear-to-front case screw tubes.
    tubes = []
    for x, y in CASE_SCREWS:
        # Slight wall overlap avoids a tangential tube/wall seam in STL export.
        tube = g.cylinder(x, y, Z_BOSS_TOP, TUBE_R, Z_REAR_IN - Z_BOSS_TOP + 0.2)
        tubes.append(g.difference(tube,
                                  [g.cylinder(x, y, Z_BOSS_TOP - 0.2, SHANK_R,
                                              Z_REAR_IN - Z_BOSS_TOP + 0.4)]))
    shell = g.difference(shell,
                         [g.cylinder(x, y, Z_REAR_IN - 0.2, SHANK_R, 2.4)
                          for x, y in CASE_SCREWS])

    # Battery cradle: loose fit, three low rails and optional 10-12 mm strap.
    bw, bh, rt, rh = BAT_W + BAT_CLEARANCE, BAT_H + BAT_CLEARANCE, 1.5, 3.5
    rails = [g.box(BAT_X - rt, BAT_Y - rt, Z_REAR_IN - rh, rt, bh + 2 * rt, rh + 0.2),
             g.box(BAT_X + bw, BAT_Y - rt, Z_REAR_IN - rh, rt, bh + 2 * rt, rh + 0.2),
             g.box(BAT_X, BAT_Y + bh, Z_REAR_IN - rh, bw, rt, rh + 0.2)]

    # Two vertical slots beside the cradle let a reusable strap cross the cell.
    strap_y = BAT_Y + BAT_H / 2 - 6.0
    strap_slots = [g.box(BAT_X - 5.0, strap_y, Z_REAR_IN - 0.2, 2.4, 12.0, 2.4),
                   g.box(BAT_X + bw + 2.6, strap_y, Z_REAR_IN - 0.2, 2.4, 12.0, 2.4)]
    shell = g.difference(shell, strap_slots)
    shell = g.union([shell, *tubes, *rails])
    # Counterbores from the rear face, cut after the tubes are merged so the
    # head seats on solid tube material below the rear plate.
    bores = []
    for x, y in CASE_SCREWS:
        bores.append(g.cylinder(x, y, Z_SEAT, CBORE_R, Z_REAR_OUT - Z_SEAT + 0.3))
        bores.append(g.cylinder(x, y, Z_BOSS_TOP - 0.2, SHANK_R, Z_SEAT - Z_BOSS_TOP + 0.4))
    return g.difference(shell, bores)


def fit_test_coupon():
    """Lower chassis section for a fast physical FPC/PCB fit check."""
    return g.trimesh.boolean.intersection(
        [front_chassis(), g.box(-0.2, -0.2, -0.2, CASE_W + 0.4, 72.0, Z_COMP + 0.4)],
        engine="manifold",
    )


def check():
    assert abs(CASE_W - 128.0) < 1e-6
    assert abs(PANEL_Y - (BOARD_Y + BOARD_H) - 14.0) < 1e-6
    assert abs((BOARD_X + BOARD_W) - (CASE_W - 11.0)) < 1e-6
    assert J2_X > FPC_X, "real FPC side-step must run to the right"
    assert Z_COMP - COMP_MAX_H > FRONT_T + 0.5, "board components hit front chassis"
    assert Z_BOARD_REAR < Z_REAR_IN, "board hits rear plate"
    assert BAT_T <= Z_REAR_IN - Z_BOARD_REAR + 0.5, "battery depth exceeds enclosure"
    assert BAT_X > KEYHOLE_X[0] + 4.5 and BAT_X + BAT_W < KEYHOLE_X[1] - 4.5
    for hx, hy in BOARD_HOLES:
        for sx, sy in CASE_SCREWS:
            d = ((hx - sx) ** 2 + (hy - sy) ** 2) ** 0.5
            assert d > BOSS_R + 2.2 + 0.5, f"board post/case boss collision: {d:.2f} mm"
    assert BOARD_X + BOARD_W <= CASE_SCREWS[1][0] - BOSS_R - 2.0, "right boss clearance lost"
    assert Z_GUIDE_TOP + CLAMP_T + 1.4 < Z_REAR_IN - 3.5, "clamp head hits rear parts"
    for x, y, _ in CLAMPS:
        assert x - CLAMP_DOME_R - 0.5 > WALL + 0.5 and x + CLAMP_DOME_R + 0.5 < CASE_W - WALL - 0.5
        assert y + CLAMP_W / 2 < CASE_SCREWS[2][1] - TUBE_R - 0.5, "clamp hits case screw tube"
    assert Z_GUIDE_TOP - CLAMP_PILOT_Z0 + CLAMP_T >= 5.0, "M2x5 does not fit"
    assert Z_SEAT + HEAD_K <= Z_REAR_OUT - 0.3, "screw head not recessed"
    assert Z_SEAT < Z_REAR_IN, "counterbore must end inside the tube, not in the plate"
    assert Z_BOSS_TOP - (Z_SEAT - SCREW_LEN) >= 3.0, "too little thread engagement"
    # neighbouring side-button openings must not merge
    xs = sorted(flip_x(b) for b in BUTTON_Y)
    assert all(b - a > 4.5 + 2 + 1.5 for a, b in zip(xs, xs[1:])), "button openings merge"
    sw_lo = min(flip_x(SWITCH_Y[0]), flip_x(SWITCH_Y[1])) - 1.0
    sw_hi = max(flip_x(SWITCH_Y[0]), flip_x(SWITCH_Y[1])) + 1.0
    for bx in xs:
        assert bx + 3.25 < sw_lo - 1.0 or bx - 3.25 > sw_hi + 1.0, "button cut hits switch cut"


def export(name, mesh):
    mesh.remove_unreferenced_vertices()
    if not mesh.is_watertight:
        raise RuntimeError(f"{name} is not watertight")
    if mesh.volume <= 0:
        raise RuntimeError(f"{name} has invalid volume")
    if len(mesh.split(only_watertight=False)) != 1:
        raise RuntimeError(f"{name} is not a single body")
    mesh.export(OUT / f"{name}.stl")
    # STL drops indexed topology. Reload it and prove the deliverable, not only
    # the in-memory boolean result.
    reloaded = g.trimesh.load(OUT / f"{name}.stl", process=True)
    if not reloaded.is_watertight or len(reloaded.split(only_watertight=False)) != 1:
        raise RuntimeError(f"{name} STL is not watertight after reload")
    print(f"  {name}: {len(mesh.faces)} faces, {mesh.volume / 1000:.1f} cm3, "
          f"bounds={np.round(mesh.bounds, 2).tolist()}")


def main():
    check()
    print(f"case {CASE_W:.1f} x {CASE_H:.2f} x {Z_REAR_OUT:.1f} mm")
    print(f"panel x={PANEL_X:.2f}..{PANEL_X + PANEL_W:.2f}, y={PANEL_Y:.2f}..{PANEL_Y + PANEL_H:.2f}")
    print(f"board x={BOARD_X:.2f}..{BOARD_X + BOARD_W:.2f}, y={BOARD_Y:.2f}..{BOARD_Y + BOARD_H:.2f}")
    print(f"FPC attachment x={FPC_X:.2f}, physical J2 x={J2_X:.2f}, side-step={J2_X - FPC_X:.2f}")
    print(f"board holes={[(round(x, 2), round(y, 2)) for x, y in BOARD_HOLES]}")
    print(f"buttons x={[round(flip_x(b), 2) for b in BUTTON_Y]} (last = RESET)")
    print(f"screw seat z={Z_SEAT:.2f}, head top z={Z_SEAT + HEAD_K:.2f}, rear face z={Z_REAR_OUT:.1f}, "
          f"engagement={Z_BOSS_TOP - (Z_SEAT - SCREW_LEN):.2f} mm")
    export("en04_front_chassis_v7", front_chassis())
    export("en04_rear_cover_v7", rear_shell())
    export("en04_panel_clamp_v7", clamp_tab())


if __name__ == "__main__":
    main()
