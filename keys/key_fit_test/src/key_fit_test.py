"""NSAS key fit test: accessory-leg variants of the v0.12 key, a matching
test block and print plates (handoff 2026-10-20, spec v0.12 unchanged).

The key's flat sides are flat and flush, so the whole key is a side-view
profile extruded 4.6 mm. That profile is drawn in XY and extruded in +Z,
which is also the print orientation (lying on one flat side).

Key frame (same as `NSAS key - accessories.solidcraft`):
- X: perpendicular to the panel face. Panel face at X = 0, panel leg toward
  -X (into the panel), stop X = 0..STOP_T, accessory leg toward +X.
- Y: vertical in use. The bar axis is the line Y = X (out of the panel and up).
- Z: across the flat sides, 0..KEY_W.
Widths are measured across the 45 deg axis; leg lengths and positions are
perpendicular to the panel face (X), as in the spec.

Test block: printed with its back face on the bed (Z = 0). Each hole is
the v0.12 accessory hole: 5.0 square, rises 45 deg (+Y) going in (+Z),
6.0 deep perpendicular, flat floor.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, replace
from pathlib import Path

from cadgen import build123d as bd
from cadgen import stl

HERE = Path(__file__).resolve().parent
R2 = math.sqrt(2.0)

# Baseline key, v0.12 (names follow the SolidCraft parameters)
KEY_W = 4.6  # across the flat sides, whole key
STOP_T = 1.0
STOP_H = 12.0
PANEL_LEN = 10.0  # functional depth
ACC_LEN = 5.0
PANEL_ROOT = 4.6
PANEL_BULGE = 5.0
PANEL_PRONG_GAP = 1.0
PANEL_PRONG_ROOT = 3.0
PANEL_TIP_CHAMFER = 1.0
KEY_ROOT = 4.9
KEY_BULGE = 5.1
PRONG_GAP = 1.0
PRONG_ROOT = 1.0
RELIEF_D = 1.0
LEAD_IN = 0.6

# Barbs (B1/B2): ramp toward the tip, steep face toward the root
BARB_X = (2.5, 4.5)  # steep faces, perpendicular from the panel face (stop root at 1.0)
BARB_RAMP = 0.8  # ramp length along the axis

# Label, debossed into the top flat side at the panel-leg root (no fit effect)
LABEL_H = 2.0
LABEL_DEPTH = 0.4
FONT = "DejaVu Sans"

# Test block
ACC_HOLE = 5.0
ACC_DEPTH = 6.0
HOLE_PITCH = 10.0
BLOCK_T = 10.0  # 6 deep + 4 skin behind the floor
MOUTH_Y0 = 3.0  # bottom of the hole mouth on the back face
BLOCK_H = 24.0  # 13.9 above the top of the mouth (>= depth + skin)
BLOCK_LABEL_H = 3.0


@dataclass(frozen=True)
class Key:
    name: str
    acc_root: float = KEY_ROOT  # accessory leg, upper/lower faces, at the stop
    acc_tip: float = KEY_BULGE  # same, at the tip (prongs relaxed)
    relief_d: float = RELIEF_D
    barb_h: float = 0.0
    panel_tip: float = PANEL_BULGE
    note: str = ""


P1 = Key("P1", 5.05, 5.05, note="parallel 5.05")
VARIANTS = [
    Key("V0", note="baseline v0.12, 4.9 -> 5.1"),
    P1,
    replace(P1, name="P2", acc_root=5.10, acc_tip=5.10, note="parallel 5.10"),
    replace(P1, name="P3", acc_root=5.15, acc_tip=5.15, note="parallel 5.15"),
    Key("F1", 5.08, 4.95, note="flipped taper 5.08 -> 4.95"),
    replace(P1, name="B1", barb_h=0.10, note="P1 + 0.10 barbs"),
    replace(P1, name="B2", barb_h=0.15, note="P1 + 0.15 barbs"),
    replace(P1, name="R1", relief_d=0.6, note="P1 + 0.6 relief"),
    replace(P1, name="L1", panel_tip=4.90, note="P1 + panel tip 4.90"),
]
BY_NAME = {k.name: k for k in VARIANTS}

# Test rounds: V0 is the control in every round, P1 is the base of B/R/L
ROUNDS = {
    "A": ["V0", "P1", "P2", "P3"],
    "B": ["V0", "P1", "F1", "B1", "B2"],
    "C": ["V0", "P1", "R1", "L1"],
}


def _pt(u, v):
    """Key frame point from axis coordinates: u along the bar axis (toward
    the accessory tip), v across it (toward the upper face)."""
    return ((u - v) / R2, (u + v) / R2)


def _edge_y(x, w, side):
    """Y of the upper (side = 1) or lower (side = -1) face at X for width w."""
    return x + side * w / R2


def _prism(points, z0=-1.0, h=KEY_W + 2.0):
    """Extrude an XY outline in +Z whatever its winding."""
    wire = bd.Wire.make_polygon([(x, y, z0) for x, y in points], close=True)
    return bd.Solid.extrude(bd.Face(wire), bd.Vector(0, 0, h))


def _lerp(a, b, t):
    return a + (b - a) * t


def key_shape(k: Key):
    x0 = STOP_T  # accessory leg root
    x1 = STOP_T + ACC_LEN  # accessory tip

    def acc_w(x):
        return _lerp(k.acc_root, k.acc_tip, (x - x0) / ACC_LEN)

    # Panel leg, X = 0 .. -PANEL_LEN, width PANEL_ROOT -> panel_tip
    xp = -PANEL_LEN
    panel = [
        (0.0, _edge_y(0.0, PANEL_ROOT, -1)),
        (xp, _edge_y(xp, k.panel_tip, -1)),
        (xp, _edge_y(xp, k.panel_tip, 1)),
        (0.0, _edge_y(0.0, PANEL_ROOT, 1)),
    ]
    stop = [(0, -STOP_H / 2), (STOP_T, STOP_T - STOP_H / 2), (STOP_T, STOP_T + STOP_H / 2), (0, STOP_H / 2)]
    acc = [
        (x0 - 0.01, _edge_y(x0 - 0.01, acc_w(x0), -1)),
        (x1, _edge_y(x1, acc_w(x1), -1)),
        (x1, _edge_y(x1, acc_w(x1), 1)),
        (x0 - 0.01, _edge_y(x0 - 0.01, acc_w(x0), 1)),
    ]
    body = _prism(panel, 0, KEY_W) + _prism(stop, 0, KEY_W) + _prism(acc, 0, KEY_W)

    # Barbs on both tapered faces (built on a parallel leg)
    if k.barb_h > 0:
        for xb in BARB_X:
            for side in (1, -1):
                v = side * acc_w(xb) / 2
                u0 = xb * R2 + v  # steep face meets the leg edge at X = xb
                h = side * k.barb_h
                eps = -side * 0.02
                body += _prism([_pt(u0, v + eps), _pt(u0, v + h), _pt(u0 + BARB_RAMP, v + eps)], 0, KEY_W)

    cuts = []
    # Accessory prong slot: tip to PRONG_ROOT from the stop, square end
    ua = (x0 + PRONG_ROOT) * R2
    cuts.append(_prism([_pt(ua, -PRONG_GAP / 2), _pt(ua + 20, -PRONG_GAP / 2),
                        _pt(ua + 20, PRONG_GAP / 2), _pt(ua, PRONG_GAP / 2)]))
    # Panel prong slot: tip to PANEL_PRONG_ROOT from the panel face
    up = -PANEL_PRONG_ROOT * R2
    cuts.append(_prism([_pt(up - 20, -PANEL_PRONG_GAP / 2), _pt(up, -PANEL_PRONG_GAP / 2),
                        _pt(up, PANEL_PRONG_GAP / 2), _pt(up - 20, PANEL_PRONG_GAP / 2)]))
    # Tip lead-ins: LEAD_IN along the end face and along the leg edge
    c = LEAD_IN / R2
    for side in (1, -1):
        yc = _edge_y(x1, acc_w(x1), side)
        cuts.append(_prism([(x1, yc - side * LEAD_IN), (x1 + 1, yc - side * LEAD_IN),
                            (x1 + 1, yc + side * 2), (x1 - c, yc + side * 2),
                            (x1 - c, yc - side * c)]))
    # Panel tip chamfer, upper edge only
    yc = _edge_y(xp, k.panel_tip, 1)
    pc = PANEL_TIP_CHAMFER / R2
    cuts.append(_prism([(xp, yc - PANEL_TIP_CHAMFER), (xp + pc, yc + pc), (xp + pc, yc + 3),
                        (xp - 1, yc + 3), (xp - 1, yc - PANEL_TIP_CHAMFER)]))
    for cut in cuts:
        body = body - cut

    # Root reliefs: tangent to the stop's accessory face, centre on the leg edge
    r = k.relief_d / 2
    for side in (1, -1):
        xr = x0 + r
        cyl = bd.Cylinder(r, KEY_W + 2).moved(bd.Location((xr, _edge_y(xr, acc_w(x0), side), KEY_W / 2)))
        body = body - cyl

    # Label on the top flat side, along the panel-leg root
    txt = bd.Text(k.name, LABEL_H, font=FONT)
    txt = bd.extrude(txt, LABEL_DEPTH + 0.5)
    cx, cy = _pt(-2.1, 0.0)
    txt = txt.rotate(bd.Axis.Z, 45).moved(bd.Location((cx, cy, KEY_W - LABEL_DEPTH)))
    body = (body - txt).clean()
    body.label = f"key_{k.name}"
    return body


def block_shape(names):
    n = len(names)
    w = n * HOLE_PITCH
    body = bd.Box(w, BLOCK_H, BLOCK_T, align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))
    yc = MOUTH_Y0 + ACC_HOLE * R2 / 2  # mouth centre on the back face
    for i, name in enumerate(names):
        x = (i + 0.5) * HOLE_PITCH
        bar = bd.Box(ACC_HOLE, ACC_HOLE, 40).rotate(bd.Axis.X, -45).moved(bd.Location((x, yc, 0)))
        slab = bd.Box(w + 2, 200, ACC_DEPTH + 1, align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.MIN)).moved(
            bd.Location((-1, 0, -1))
        )
        body = body - (bar & slab)
        txt = bd.extrude(bd.Text(name, BLOCK_LABEL_H, font=FONT), LABEL_DEPTH + 0.5)
        body = body - txt.moved(bd.Location((x, BLOCK_H - 3.5, BLOCK_T - LABEL_DEPTH)))
    body = body.clean()
    body.label = "test_block"
    return body


def plate_shape(names, with_block=True):
    parts = []
    for i, name in enumerate(names):
        k = key_shape(BY_NAME[name]).moved(bd.Location((i * 20.0, 0, 0)))
        parts.append(k)
    if with_block:
        parts.append(block_shape(names).moved(bd.Location((-10.0, -50.0, 0))))
    out = bd.Compound(children=parts)
    out.label = "plate"
    return out


@stl(out="../STL/key_V0.stl")
def key_V0():
    return key_shape(BY_NAME["V0"])


@stl(out="../STL/key_P1.stl")
def key_P1():
    return key_shape(BY_NAME["P1"])


@stl(out="../STL/key_P2.stl")
def key_P2():
    return key_shape(BY_NAME["P2"])


@stl(out="../STL/key_P3.stl")
def key_P3():
    return key_shape(BY_NAME["P3"])


@stl(out="../STL/key_F1.stl")
def key_F1():
    return key_shape(BY_NAME["F1"])


@stl(out="../STL/key_B1.stl")
def key_B1():
    return key_shape(BY_NAME["B1"])


@stl(out="../STL/key_B2.stl")
def key_B2():
    return key_shape(BY_NAME["B2"])


@stl(out="../STL/key_R1.stl")
def key_R1():
    return key_shape(BY_NAME["R1"])


@stl(out="../STL/key_L1.stl")
def key_L1():
    return key_shape(BY_NAME["L1"])


@stl(out="../STL/test_block.stl")
def test_block():
    return block_shape([k.name for k in VARIANTS])


@stl(out="../STL/plate_all.stl")
def plate_all():
    return plate_shape([k.name for k in VARIANTS])


@stl(out="../STL/plate_round_A.stl")
def plate_round_A():
    return plate_shape(ROUNDS["A"])


@stl(out="../STL/plate_round_B.stl")
def plate_round_B():
    return plate_shape(ROUNDS["B"])


@stl(out="../STL/plate_round_C.stl")
def plate_round_C():
    return plate_shape(ROUNDS["C"])


if __name__ == "__main__":
    for model in (key_V0, key_P1, key_P2, key_P3, key_F1, key_B1, key_B2, key_R1, key_L1,
                  test_block, plate_all, plate_round_A, plate_round_B, plate_round_C):
        model()
