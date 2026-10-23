"""IKEA UPPDATERA and VARIERA - NSAS slot in holder.

A side profile from a Fusion sketch, extruded EXTRUDE mm. The profile (XY plane, mm) is the largest region of the sketch. The
smaller enclosed regions of the sketch are notches, cut through:
  - a 8 x 3 notch in the top of the base, behind the front ledge;
  - a 1 mm strip on top of the slot mouth (Y = SLOT_TOP .. +1);
  - a wedge behind the leaning wall, opening 10 deg from it.

Shape, front (-X) to back (+X):
  base, Y = -BASE_H .. 0, X = LEFT_X .. RIGHT_X; its top is a ledge
  from LEFT_X to WALL_X0, then a wall leans back at WALL_ANGLE from
  vertical up to SLOT_TOP. Above the wall, a lip LIP_T thick (parallel
  to the wall) hangs LIP_DROP below SLOT_TOP, its inner face SLOT_GAP
  in front of the wall top. The body runs up to TOP_Y.

Coordinates: profile in XY with the sketch origin at (0, 0), extruded
along +Z from Z = 0.
"""
from __future__ import annotations

import math

from cadgen import build123d as bd
from cadgen import step, stl

EXTRUDE = 70.0

# Dimensioned in the sketch.
WALL_X0 = 20.0  # foot of the leaning wall, on Y = 0
LEDGE_W = 15.0  # front ledge, ending at the wall foot
BASE_H = 10.0  # base below Y = 0
WALL_ANGLE = 5.0  # wall lean from vertical (95 deg to the ledge)
SLOT_TOP = 102.0  # top of the wall
SLOT_GAP = 3.0  # lip inner face to wall top, horizontal
LIP_T = 8.0  # lip thickness, square to its faces
LIP_DROP = 10.0  # lip bottom below SLOT_TOP
STRIP_H = 1.0  # notch strip on top of the slot mouth
WEDGE_W = 5.0  # wedge width at SLOT_TOP, behind the wall top
WEDGE_ANGLE = 10.0  # wedge back face, from the wall
BASE_NOTCH_W = 8.0  # notch in the base top, its back on WALL_X0
BASE_NOTCH_H = 3.0

# Not dimensioned in the sketch (free lines); read off the screenshot.
RIGHT_X = 45.0  # back face
TOP_Y = 118.0  # top face

LEFT_X = WALL_X0 - LEDGE_W


def _wall_x(y):
    return WALL_X0 + y * math.tan(math.radians(WALL_ANGLE))


def profile_points():
    """Outer boundary of the profile, counter-clockwise."""
    t = math.tan(math.radians(WALL_ANGLE))
    wall_top = _wall_x(SLOT_TOP)
    in_x_top = wall_top - SLOT_GAP  # lip inner face at SLOT_TOP + STRIP_H

    def lip_in(y):
        return in_x_top + (y - SLOT_TOP - STRIP_H) * t

    def lip_out(y):
        return lip_in(y) - LIP_T / math.cos(math.radians(WALL_ANGLE))

    lip_bot = SLOT_TOP - LIP_DROP
    return [
        (LEFT_X, -BASE_H),
        (RIGHT_X, -BASE_H),
        (RIGHT_X, TOP_Y),
        (lip_out(TOP_Y), TOP_Y),
        (lip_out(lip_bot), lip_bot),
        (lip_in(lip_bot), lip_bot),
        (lip_in(SLOT_TOP), SLOT_TOP),
        (wall_top, SLOT_TOP),
        (WALL_X0, 0.0),
        (LEFT_X, 0.0),
    ]


def notch_polygons():
    t = math.tan(math.radians(WALL_ANGLE))
    wall_top = _wall_x(SLOT_TOP)
    in_x_top = wall_top - SLOT_GAP
    wedge_x = wall_top + WEDGE_W
    # Wedge back face, WALL_ANGLE + WEDGE_ANGLE from vertical, meets the
    # wall where both lines cross.
    tb = math.tan(math.radians(WALL_ANGLE + WEDGE_ANGLE))
    y_meet = (WALL_X0 - wedge_x + SLOT_TOP * tb) / (tb - t)
    base = [
        (WALL_X0 - BASE_NOTCH_W, -BASE_NOTCH_H),
        (WALL_X0, -BASE_NOTCH_H),
        (WALL_X0, 0.0),
        (WALL_X0 - BASE_NOTCH_W, 0.0),
    ]
    strip = [
        (in_x_top - STRIP_H * t, SLOT_TOP),
        (wedge_x, SLOT_TOP),
        (wedge_x, SLOT_TOP + STRIP_H),
        (in_x_top, SLOT_TOP + STRIP_H),
    ]
    wedge = [(_wall_x(y_meet), y_meet), (wedge_x, SLOT_TOP), (wall_top, SLOT_TOP)]
    return [base, strip, wedge]


def slot_in_holder_shape():
    face = bd.Polygon(*profile_points(), align=None)
    for pts in notch_polygons():
        face = face - bd.Polygon(*pts, align=None)
    return bd.extrude(face, EXTRUDE).clean()


@stl(out="../IKEA UPPDATERA and VARIERA - NSAS slot in holder.stl")
@step(out="../IKEA UPPDATERA and VARIERA - NSAS slot in holder.step")
def slot_in_holder():
    body = slot_in_holder_shape()
    body.label = "slot_in_holder"
    return body


if __name__ == "__main__":
    slot_in_holder()
