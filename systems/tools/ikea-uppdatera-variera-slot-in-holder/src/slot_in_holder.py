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

Optimised from the tested print:
  - two pockets through the body, one behind the wall and wedge and one
    in the top block over the slot, leaving SHELL walls, a FLOOR_T floor
    and a BACK_T back plate (kept solid for the NSAS accessory holes
    still to come);
  - fillets on the inner corners of the base notch, the wedge tip, the
    lip root and the pocket;
  - a LIP_LEAD chamfer on the lip's inner bottom edge and a LEDGE_R round
    on the ledge's front edge, so the box rim finds the slot;
  - EXTRUDE 69 mm (7 x 10 - 1), so holders sit side by side on the
    NSAS 10 mm column pitch.

Mounting: the back face (X = RIGHT_X) goes against the NSAS panel, Y up.
NSAS accessory holes in it, 2 columns 40 mm apart and 4 rows two row
pitches (37.07 mm) apart, so it fits current panels and older plates
with sockets every second row. Key the top and bottom rows: the box
hangs in front, so its weight pulls the top of the holder off the panel.
Print with the profile on the bed.

Coordinates: profile in XY with the sketch origin at (0, 0), extruded
along +Z from Z = 0.
"""
from __future__ import annotations

import math

from cadgen import build123d as bd
from cadgen import step, stl

EXTRUDE = 69.0  # 7 x 10 - 1, NSAS column pitch

# Dimensioned in the sketch.
WALL_X0 = 20.0  # foot of the leaning wall, on Y = 0
LEDGE_W = 15.0  # front ledge, ending at the wall foot
BASE_H = 10.5  # base below Y = 0; sketch 10, +0.5 for 2 mm under the 4th NSAS row
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

# Optimisation.
SHELL = 3.0  # wall left between the pocket and the slot / wedge faces
FLOOR_T = 3.0  # under the pocket
BACK_T = 10.0  # solid back plate, reserved for the NSAS accessory holes
POCKET_R = 1.0  # pocket corner fillets
NOTCH_R = 1.0  # base notch inner corners
WEDGE_TIP_R = 0.5  # 10 deg tip at the bottom of the wedge
LIP_ROOT_R = 0.8  # lip inner face to strip roof; < STRIP_H
LIP_LEAD = 1.5  # 45 deg lead-in on the lip's inner bottom edge
LEDGE_R = 1.0  # ledge front top edge

# NSAS accessory holes in the back face (X = RIGHT_X, against the panel).
# Blind, they go in (-X) and rise 45 deg (+Y); flat floor parallel to the
# back face. Square 5 mm across the axis, one pair of faces normal to Z,
# so printed profile-down the hole is a tunnel with a flat 5 mm bridge.
NSAS_HOLE = 5.0
NSAS_DEPTH = 6.0  # perpendicular to the back face
NSAS_FACE_H = NSAS_HOLE * math.sqrt(2)  # 7.07 tall on the face
NSAS_TOP_SKIN = 8.0  # top face to top of the upper mouth (depth + 2)
NSAS_ROW_PITCH = 15 + 2.5 * math.sqrt(2)  # 18.536
# Rows NSAS_ROW_STEP pitches apart from the top down. Every second row
# fits both current panels (sockets on every row) and older plates
# (sockets every second row).
NSAS_ROWS = 4
NSAS_ROW_STEP = 2
# Printed profile-down (Z = 0 on the bed), each hole's +Z face is a 5 mm
# bridge. A gable over it, NSAS_ROOF_ANGLE from flat on both sides, gives
# room for an ABS bridge that sags. It sits on a face against a flat side
# of the key, which has 0.2 mm clearance, so the press fit is unchanged.
NSAS_ROOF_ANGLE = 30.0
NSAS_COL_PITCH = 10.0
NSAS_COL_STEPS = 2  # columns this many pitches either side of centre


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


def pocket_points():
    """Lightening pocket behind the wall and wedge, SHELL from both."""
    t5 = math.tan(math.radians(WALL_ANGLE))
    a15 = math.radians(WALL_ANGLE + WEDGE_ANGLE)
    t15 = math.tan(a15)
    wedge_x = _wall_x(SLOT_TOP) + WEDGE_W
    # Pocket front: the wall face and the wedge back face, each offset
    # SHELL square to itself.
    x0w = WALL_X0 + SHELL / math.cos(math.radians(WALL_ANGLE))
    x0e = wedge_x + SHELL / math.cos(a15) - SLOT_TOP * t15

    def front_wall(y):
        return x0w + y * t5

    y_kink = (x0w - x0e) / (t15 - t5)  # the two offset lines cross
    x_back = RIGHT_X - BACK_T
    y_top = (x_back - x0e) / t15  # wedge offset meets the back plate
    y_bot = -BASE_H + FLOOR_T
    assert y_bot < y_kink < y_top < SLOT_TOP
    return [
        (front_wall(y_bot), y_bot),
        (x_back, y_bot),
        (x_back, y_top),
        (front_wall(y_kink), y_kink),
    ]


def upper_pocket_points():
    """Second pocket in the top block, over the strip, SHELL from the
    lip's outer face, the top face, the strip roof and the back plate."""
    t5 = math.tan(math.radians(WALL_ANGLE))
    lip_out = profile_points()[3][0]  # lip outer face at TOP_Y
    dx = SHELL / math.cos(math.radians(WALL_ANGLE))
    y0, y1 = SLOT_TOP + STRIP_H + SHELL, TOP_Y - SHELL
    x_back = RIGHT_X - BACK_T

    def left(y):
        return lip_out + dx - (TOP_Y - y) * t5

    return [(left(y0), y0), (x_back, y0), (x_back, y1), (left(y1), y1)]


def nsas_hole_centres():
    """Mouth centres (Y, Z) on the back face: NSAS_ROWS x 2 columns."""
    y_top = TOP_Y - NSAS_TOP_SKIN - NSAS_FACE_H / 2
    step = NSAS_ROW_STEP * NSAS_ROW_PITCH
    rows = [y_top - k * step for k in range(NSAS_ROWS)]
    assert rows[-1] - NSAS_FACE_H / 2 >= -BASE_H + 2.0, "bottom skin < 2 mm"
    dz = NSAS_COL_STEPS * NSAS_COL_PITCH
    return [(y, EXTRUDE / 2 + s * dz) for y in rows for s in (-1, 1)]


def _nsas_holes():
    h = NSAS_HOLE / 2
    rise = h * math.tan(math.radians(NSAS_ROOF_ANGLE))
    holes = []
    for y, z in nsas_hole_centres():
        # Bar along X turned -45 deg about Z: axis along (1, -1), so going
        # in (-X) it rises (+Y).
        bar = bd.Box(40.0, NSAS_HOLE, NSAS_HOLE).rotate(bd.Axis.Z, -45)
        bar = bar.moved(bd.Location((RIGHT_X, y, z)))
        # Gable on the +Z face: sketch plane square to the hole axis,
        # local x across the hole in XY, local y = -Z.
        plane = bd.Plane(
            origin=(RIGHT_X, y, z), x_dir=(1, 1, 0), z_dir=(-1, 1, 0)
        )
        tri = plane * bd.Polygon((-h, -h), (h, -h), (0, -h - rise), align=None)
        roof = bd.extrude(tri, 20.0, both=True)
        slab = bd.Box(NSAS_DEPTH + 1, 3 * TOP_Y, EXTRUDE + 2).moved(
            bd.Location((RIGHT_X - (NSAS_DEPTH - 1) / 2, y, z))
        )
        holes.append((bar + roof) & slab)
    return holes


def _z_edges_near(body, points, tol=0.05):
    """Edges parallel to Z whose XY passes through any of `points`."""
    found = []
    for e in body.edges().filter_by(bd.Axis.Z):
        c = e.center()
        if any(abs(c.X - x) < tol and abs(c.Y - y) < tol for x, y in points):
            found.append(e)
    assert len(found) == len(points), (len(found), points)
    return found


def slot_in_holder_shape():
    base, strip, wedge = notch_polygons()
    face = bd.Polygon(*profile_points(), align=None)
    pockets = [pocket_points(), upper_pocket_points()]
    for pts in [base, strip, wedge] + pockets:
        face = face - bd.Polygon(*pts, align=None)
    body = bd.extrude(face, EXTRUDE).clean()

    # Inner corners: base notch floor, wedge tip, pockets.
    body = body.fillet(NOTCH_R, _z_edges_near(body, base[:2]))
    body = body.fillet(WEDGE_TIP_R, _z_edges_near(body, wedge[:1]))
    for pts in pockets:
        body = body.fillet(POCKET_R, _z_edges_near(body, pts))
    # Lip root: lip inner face meets the strip roof.
    body = body.fillet(LIP_ROOT_R, _z_edges_near(body, strip[3:]))
    # Lead-ins: lip inner bottom edge, ledge front top edge.
    lip = profile_points()[5]
    body = body.chamfer(LIP_LEAD, None, _z_edges_near(body, [lip]))
    body = body.fillet(LEDGE_R, _z_edges_near(body, [profile_points()[-1]]))
    for hole in _nsas_holes():
        body = body - hole
    return body.clean()


@stl(out="../IKEA UPPDATERA and VARIERA - NSAS slot in holder.stl")
@step(out="../IKEA UPPDATERA and VARIERA - NSAS slot in holder.step")
def slot_in_holder():
    body = slot_in_holder_shape()
    body.label = "slot_in_holder"
    return body


if __name__ == "__main__":
    slot_in_holder()
