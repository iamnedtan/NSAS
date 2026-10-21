"""Sanding block: box for sanding sticks with NSAS accessory holes.

Extracted on 2026-10-21 from RunnerCollector mini/src/mini_under_bins.py
(sanding_block_shape and _nsas_holes, commit 193ac88), where it is one of
the lift-out bins under the tray of the mini box. Same geometry; the
footprint and height that came from the mini box envelope are fixed values
here.

Closed box with one open end and a 45 deg cut across that end, so the
inside shows from above. Sanding sticks slide in lengthwise. The floor
carries NSAS accessory holes, so the block hangs on an NSAS panel open end
up (its floor is then its back face).

Coordinates: base on Z = 0, centred in XY, long side along Y, open end at
-Y. On a panel, "up" is -Y.
"""
from __future__ import annotations

import math

from cadgen import build123d as bd
from cadgen import step, stl

# Outside size
BLOCK_X = 68.4  # 66 inside
BLOCK_Y = 82.7  # open end to back face
BLOCK_H = 34.0

WALL = 1.2
OUTER_R = 6.0  # vertical outer corners at the closed end
INNER_R = OUTER_R - WALL
SAND_FLOOR = 5.0  # floor thickness (NSAS accessory side)
SAND_CUT = 20.0  # 45 deg cut at the open end: drops this much at the open face

# NSAS accessory holes in the floor. The holes rise 45 deg toward -Y going
# in (+Z) and punch through the 5 mm floor.
NSAS_HOLE = 5.0  # square, across the 45 deg axis
NSAS_COL_PITCH = 10.0
NSAS_ROW_RULE = 30.0  # top wall of row k to bottom wall of row k + 2
NSAS_FACE_H = NSAS_HOLE * math.sqrt(2)  # 7.07 tall on the face
NSAS_ROW_PITCH = (NSAS_ROW_RULE + NSAS_FACE_H) / 2  # 18.536
NSAS_MARGIN = 6.0  # minimum, face edge to hole mouth

Y0, Y1 = -BLOCK_Y / 2, BLOCK_Y / 2


def _rbox(x, y, h, r):
    """Box with rounded vertical edges, base on Z = 0, centred in XY."""
    sk = bd.RectangleRounded(x, y, r) if r > 0 else bd.Rectangle(x, y)
    return bd.extrude(sk, h)


def _cut(x0, x1, y0, y1, z0, z1, r=0):
    return _rbox(x1 - x0, y1 - y0, z1 - z0, r).moved(
        bd.Location(((x0 + x1) / 2, (y0 + y1) / 2, z0))
    )


def _at_y(shape, y0, y1):
    return shape.moved(bd.Location((0, (y0 + y1) / 2, 0)))


def _nsas_holes(face_x, y0, y1):
    """Accessory holes in the Z = 0 face, rising toward -Y going in (+Z)."""
    ncol = int((face_x - 2 * NSAS_MARGIN - NSAS_HOLE) // NSAS_COL_PITCH) + 1
    nrow = int((y1 - y0 - 2 * NSAS_MARGIN - NSAS_FACE_H) // NSAS_ROW_PITCH) + 1
    xs = [(i - (ncol - 1) / 2) * NSAS_COL_PITCH for i in range(ncol)]
    yc = (y0 + y1) / 2
    ys = [yc + (j - (nrow - 1) / 2) * NSAS_ROW_PITCH for j in range(nrow)]
    holes = []
    for x in xs:
        for y in ys:
            # Bar along Z, turned 45 deg about X: its axis becomes (0, -1, 1).
            bar = bd.Box(NSAS_HOLE, NSAS_HOLE, 20.0)
            bar = bar.rotate(bd.Axis.X, 45).moved(bd.Location((x, y, 0)))
            holes.append(bar)
    return holes


def sanding_block_shape():
    """Closed box open on its -Y end, base Z = 0, centred in XY."""
    length = Y1 - Y0
    # Rounded corners at the +Y end only; the open -Y end stays square so
    # the 1.2 mm side walls run straight to the opening.
    body = _rbox(BLOCK_X, length, BLOCK_H, OUTER_R)
    body = body + _at_y(_rbox(BLOCK_X, length / 2, BLOCK_H, 0), Y0, Y0 + length / 2)
    ix0, ix1 = -BLOCK_X / 2 + WALL, BLOCK_X / 2 - WALL
    cavity = _cut(ix0, ix1, Y0 - 1.0, Y1 - WALL, SAND_FLOOR, BLOCK_H - WALL)
    # Round the back corners to follow the R6 outside with a full WALL.
    inner = _at_y(
        _rbox(BLOCK_X - 2 * WALL, length + 10.0, BLOCK_H, INNER_R),
        Y0 - 10.0 - WALL,
        Y1 - WALL,
    )
    body = body - (cavity & inner)
    # 45 deg cut across the open end: the plane runs from
    # Z = BLOCK_H - SAND_CUT at the open face up to the top, SAND_CUT back
    # from it.
    zc = BLOCK_H - SAND_CUT
    wedge = bd.Plane.YZ * bd.Polygon(
        (Y0 - 1.0, zc - 1.0),
        (Y0 - 1.0, BLOCK_H + 1.0),
        (Y0 + SAND_CUT + 1.0, BLOCK_H + 1.0),
        align=None,
    )
    body = body - bd.extrude(wedge, BLOCK_X, both=True)
    for h in _nsas_holes(BLOCK_X, Y0, Y1):
        body = body - h
    body = body.clean()
    body.label = "sanding_block"
    return body


@stl(out="../sanding_block.stl")
@step(out="../sanding_block.step")
def sanding_block():
    return sanding_block_shape()


if __name__ == "__main__":
    sanding_block()
