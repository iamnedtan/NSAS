"""Coffee cup holder: one mini instant-coffee cup on an NSAS panel.

An open ring whose bore follows the cup's own taper. The cup drops in from
the top and wedges in the taper, held over the full HOLDER_H. No floor: the
lower part of the cup hangs out below the ring. The ring top sits LIP_GAP
under the cup lip. A back plate carries NSAS accessory holes in one row.
The brand name is engraved in the top face of the back plate, readable
from the front.

Only the cup body is measured; the lid is ignored. Each brand is one
entry in VARIANTS:
  top_d   cup diameter just below the lip
  bot_d   cup bottom diameter
  slant   bottom to under the lip, measured along the slanted side
  label   text engraved on the top face (None for no text)

Coordinates: base on Z = 0 (print this way up, no supports), back face on
Y = 0 facing -Y (toward the panel), cup axis on X = 0. In use, +Z is up.
"""
from __future__ import annotations

import math

from cadgen import build123d as bd
from cadgen import step, stl

VARIANTS = {
    "starbucks": dict(top_d=30.9, bot_d=24.0, slant=37.0, label="STARBUCKS"),
    "luckin": dict(top_d=29.7, bot_d=20.0, slant=28.6, label="LUCKIN"),
}

HOLDER_H = 22.0  # cup held over this length; >= 20 asked
LIP_GAP = 1.5  # cup lip underside to ring top, at line-to-line fit
# Radial bore offset from the cup surface. The cup seats where the bore
# meets it, so every +0.1 mm here drops the cup 0.1 / tan(taper): about
# 1.1 mm for Starbucks (5.3 deg), 0.6 mm for Luckin (9.8 deg).
# 0 = line-to-line; raise it if the print comes out tight.
FIT = 0.0
WALL = 2.0  # ring wall at the top of the bore
LEAD_IN = 0.5  # 45 deg chamfer at the bore mouth
PLATE_T = 8.0  # back plate: 6 mm hole + 2 mm skin behind the floor
PLATE_R = 2.0  # vertical outer corners of the back plate
HOLDER_W = 39.0  # 4 x 10 - 1, so holders hang side by side

# Engraved label on the top face, in the land between the back face and
# the bore (8 mm deep at the centre).
LABEL_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
LABEL_W = 30.0  # maximum text width, mm
LABEL_H = 3.5  # maximum text height, mm; the font size fits both
LABEL_Y = 4.0  # text centre, from the back face
LABEL_DEPTH = 0.6

# NSAS accessory holes in the back face, one row. They rise 45 deg toward
# +Z going in (+Y). Blind, 6 mm deep perpendicular, flat floor.
NSAS_HOLE = 5.0  # square, across the 45 deg axis
NSAS_DEPTH = 6.0  # perpendicular
NSAS_COLS = 2  # 2 to 4 fit across HOLDER_W
NSAS_COL_PITCH = 10.0
NSAS_SPACING = 2  # in column pitches between neighbouring holes
NSAS_FACE_H = NSAS_HOLE * math.sqrt(2)  # 7.07 tall on the face
NSAS_TOP_SKIN = 8.0  # top face to top of the mouth (= depth + 2 mm skin)
NSAS_BOTTOM_MIN = 2.0  # minimum, bottom face to bottom of the mouth


def cup_height(top_d, bot_d, slant):
    return math.sqrt(slant**2 - ((top_d - bot_d) / 2) ** 2)


def _nsas_holes(height):
    """Accessory holes in the Y = 0 face, rising toward +Z going in (+Y)."""
    # Mouth centre as high as the top skin allows, so the floor stays clear.
    zc = height - NSAS_TOP_SKIN - NSAS_FACE_H / 2
    assert zc - NSAS_FACE_H / 2 >= NSAS_BOTTOM_MIN
    step_x = NSAS_SPACING * NSAS_COL_PITCH
    holes = []
    for i in range(NSAS_COLS):
        x = (i - (NSAS_COLS - 1) / 2) * step_x
        # Bar along Z, turned -45 deg about X: its axis becomes (0, 1, 1).
        bar = bd.Box(NSAS_HOLE, NSAS_HOLE, 40.0).rotate(bd.Axis.X, -45)
        bar = bar.moved(bd.Location((x, 0, zc)))
        # Flat floor parallel to the back face, NSAS_DEPTH in.
        slab = bd.Box(HOLDER_W + 2, NSAS_DEPTH + 1, 3 * height).moved(
            bd.Location((0, (NSAS_DEPTH - 1) / 2, zc))
        )
        holes.append(bar & slab)
    return holes


def _label_cut(text):
    """Text sunk LABEL_DEPTH into the top face, reading from the front."""
    probe = bd.Text(text, 10.0, font_path=LABEL_FONT)
    pb = probe.bounding_box().size
    size = 10.0 * min(LABEL_W / pb.X, LABEL_H / pb.Y)
    sk = bd.Text(text, size, font_path=LABEL_FONT)  # centred on the origin
    cut = bd.extrude(sk, LABEL_DEPTH + 1)
    # Seen from the front (+Y, looking at the panel) the reader's right is
    # -X and text "up" points to the panel: turn 180 deg about Z.
    cut = cut.rotate(bd.Axis.Z, 180)
    return cut.moved(bd.Location((0, LABEL_Y, HOLDER_H - LABEL_DEPTH)))


def bore_fit(top_d, bot_d, slant, label=None):
    """Bore radii at the ring base and top, the cup axis Y, and the Z of
    the cup bottom (below the ring base, so negative)."""
    h_cup = cup_height(top_d, bot_d, slant)
    k = (top_d - bot_d) / 2 / h_cup  # radius gain per mm of height

    def r(z):  # cup radius at z above its bottom
        return bot_d / 2 + k * z

    z_top = h_cup - LIP_GAP
    z_base = z_top - HOLDER_H
    assert z_base > 0, "ring taller than the cup"
    rb, rt = r(z_base) + FIT, r(z_top) + FIT
    axis_y = PLATE_T + rt  # bore keeps PLATE_T clear of the back face
    return rb, rt, axis_y, -z_base


def cup_holder_shape(top_d, bot_d, slant, label=None):
    rb, rt, axis_y, _ = bore_fit(top_d, bot_d, slant)
    r_out = rt + WALL
    up = (bd.Align.CENTER,) * 2 + (bd.Align.MIN,)

    ring = bd.Cylinder(r_out, HOLDER_H, align=up)
    ring = ring.moved(bd.Location((0, axis_y, 0)))
    plate = bd.extrude(bd.RectangleRounded(HOLDER_W, axis_y, PLATE_R), HOLDER_H)
    plate = plate.moved(bd.Location((0, axis_y / 2, 0)))
    body = ring + plate

    # Extend the bore cone 1 mm past both faces so the cuts are clean.
    k = (rt - rb) / HOLDER_H
    bore = bd.Cone(rb - k, rt + k, HOLDER_H + 2, align=up).moved(
        bd.Location((0, axis_y, -1))
    )
    lead = bd.Cone(rt, rt + LEAD_IN + 0.5, LEAD_IN + 0.5, align=up).moved(
        bd.Location((0, axis_y, HOLDER_H - LEAD_IN))
    )
    body = body - bore - lead
    for hole in _nsas_holes(HOLDER_H):
        body = body - hole
    if label:
        body = body - _label_cut(label)
    body = body.clean()
    return body


def _variant(name):
    body = cup_holder_shape(**VARIANTS[name])
    body.label = f"cup_holder_{name}"
    return body


@stl(out="../cup_holder_starbucks.stl")
@step(out="../cup_holder_starbucks.step")
def cup_holder_starbucks():
    return _variant("starbucks")


@stl(out="../cup_holder_luckin.stl")
@step(out="../cup_holder_luckin.step")
def cup_holder_luckin():
    return _variant("luckin")


if __name__ == "__main__":
    cup_holder_starbucks()
    cup_holder_luckin()
