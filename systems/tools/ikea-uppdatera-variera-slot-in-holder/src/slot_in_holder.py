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
    and a BACK_T back plate that the NSAS accessory holes pass through;
  - fillets on the inner corners of the base notch, the lip root and the
    pockets;
  - an END_CHAMFER round the outline of both profile faces;
  - a LIP_LEAD chamfer on the lip's inner bottom edge and a LEDGE_R round
    on the ledge's front edge, so the box rim finds the slot;
  - EXTRUDE 69 mm (7 x 10 - 1), so holders sit side by side on the
    NSAS 10 mm column pitch.

Mounting: the back face (X = RIGHT_X) goes against the NSAS panel, Y up.
NSAS accessory holes in it, 2 columns 40 mm apart and 2 rows (rows 3
and 5 of the row grid, two row pitches apart), so it fits current
panels and older plates with sockets every second row.
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
BASE_H = 12.5  # base below Y = 0; sketch 10, +2.5 for 2 mm under the 4th NSAS row
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
BACK_T = 8.0  # back plate carrying the NSAS accessory holes
POCKET_R = 1.0  # pocket corner fillets
NOTCH_R = 1.0  # base notch inner corners
LIP_ROOT_R = 0.8  # lip inner face to strip roof; < STRIP_H
LIP_LEAD = 1.5  # 45 deg lead-in on the lip's inner bottom edge
LEDGE_R = 1.0  # ledge front top edge
# 45 deg chamfer round the outline of both profile faces (Z = 0 and
# Z = EXTRUDE, bottom and top as printed): no elephant's foot on the
# bed, and softer ends. Pocket and window outlines are left square.
END_CHAMFER = 0.8  # < STRIP_H, the 1 mm strip at the slot mouth

# Offset variant.
OFFSET_W = 8.0  # cut from the back face, for the NABS base piece
# The overhang's underside sits OFFSET_CLEAR over the top of the NABS base
# (its edge-A hinge fingers) when the keys join them: see offset_top().
KEY_STOP = 3.0  # thick-stop NSAS key: stop plate thickness, and recess depth
NABS_ROW1_MOUTH = 10.0 + 2.5 * math.sqrt(2)  # row 1 mouth centre from body face A
NABS_FINGER = 10.0  # hinge fingers past body face A
OFFSET_CLEAR = 0.5  # gap between the overhang and the top of the base
# Recess for each key's stop plate in the offset face, so the holder sits
# flush on the base. The thick-stop key's stop is KEY_STOP thick (from the
# base face into the holder), STOP_W wide and 2 x STOP_HALF tall, centred
# on the bar, with its ends cut at 45 deg, parallel to the bar.
STOP_W = 4.6
STOP_HALF = 6.0
STOP_CLEAR = 0.5  # recess outline clearance, each side
OFFSET_R = 1.0  # inner corner under the overhang
SLEEVE = 2.0  # wall kept round each hole tunnel by the offset pockets
RECESS_SKIN = 2.0  # wall kept behind the stop recesses by the offset pockets
POCKET_MIN_AREA = 60.0  # smaller offset pocket slivers are left solid
WINDOW_MARGIN = 2.0  # offset windows: in from the pocket edges
WINDOW_IN = 1.0  # offset windows: past the wall into the pocket
HOLE_EXIT = 0.5  # through holes end this far past the break-out

# NSAS accessory holes in the back face (X = RIGHT_X, against the panel).
# They go in (-X) and rise 45 deg (+Y), through the BACK_T back plate:
# open into the pockets, with a flat end parallel to the back face where
# no pocket is behind. Square 5 mm across the axis, one pair of faces
# normal to Z, so printed profile-down the hole is a bridged tunnel.
NSAS_HOLE = 5.0
NSAS_DEPTH = BACK_T  # perpendicular to the back face; key leg needs 6
NSAS_FACE_H = NSAS_HOLE * math.sqrt(2)  # 7.07 tall on the face
NSAS_TOP_SKIN = NSAS_DEPTH + 2  # top face to top of the upper mouth
NSAS_ROW_PITCH = 15 + 2.5 * math.sqrt(2)  # 18.536
# Row grid: one row pitch apart from the top down (row 1 under the top
# skin). Only the NSAS_KEEP_ROWS of it get holes. Rows 3 and 5 are two
# pitches apart, so they fit current panels (sockets on every row) and
# older plates (sockets every second row).
NSAS_ROWS = 7
NSAS_ROW_STEP = 1
NSAS_KEEP_ROWS = (3, 5)  # 1-based, from the top
# Printed profile-down (Z = 0 on the bed), each hole's +Z face is a 5 mm
# bridge. A gable over it, NSAS_ROOF_ANGLE from flat on both sides, gives
# room for an ABS bridge that sags. It sits on a face against a flat side
# of the key, which has 0.2 mm clearance, so the press fit is unchanged.
NSAS_ROOF_ANGLE = 30.0
NSAS_COL_PITCH = 10.0

# Windows through the back plate into the main pocket, in the band
# between the two hole columns. Printed profile-down, Z is up: each
# window has a flat bottom (low Z), straight sides and a 45 deg pointed
# top, so it needs no bridge. Spread along Y, at least WINDOW_RIB apart.
WINDOW_W = 12.0  # along Y
WINDOW_RIB = 6.0  # minimum back-plate rib between windows
# Each window column is split along Z into WINDOW_SETS windows with a
# WINDOW_RIB band between them: bands in XY planes that stiffen the
# walls in the profile plane. (A web across the pocket would do more,
# but printed profile-down it would be a floor over open air.)
WINDOW_SETS = 2
# Same windows through the leaning wall (the face the box rests on) into
# the main pocket, square to the wall, spread up the wall between the
# ledge and the wedge. FRONT_WINDOW_MARGIN of solid wall is left at each
# end (Z = 0 and Z = EXTRUDE).
FRONT_WINDOW_MARGIN = 8.0
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


def pocket_points(x_back=None):
    """Lightening pocket behind the wall and wedge, SHELL from both, back
    to x_back (default: the BACK_T back plate)."""
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
    if x_back is None:
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


def offset_pocket_regions():
    """Offset variant: the main pocket, back to KEY_STOP + RECESS_SKIN
    behind the offset face (clear of the stop recesses), less a SLEEVE band
    round each hole row's 45 deg tunnel, so the key legs keep full hole
    walls. Returns the remaining regions as faces."""
    pocket = bd.Polygon(
        *pocket_points(base_face_x() - KEY_STOP - RECESS_SKIN), align=None
    )
    w = (NSAS_HOLE / 2 + SLEEVE) * math.sqrt(2)  # band half-width in x + y
    for y in sorted({y for y, _ in nsas_hole_centres()}):
        c = RIGHT_X + y  # hole axis: x + y = c
        band = bd.Polygon(
            (-50, c - w + 50), (100, c - w - 100),
            (100, c + w - 100), (-50, c + w + 50), align=None,
        )
        pocket = pocket - band
    return [f for f in pocket.faces() if f.area >= POCKET_MIN_AREA]


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
    """Mouth centres (Y, Z) on the back face: NSAS_KEEP_ROWS x 2 columns."""
    y_top = TOP_Y - NSAS_TOP_SKIN - NSAS_FACE_H / 2
    step = NSAS_ROW_STEP * NSAS_ROW_PITCH
    grid = [y_top - k * step for k in range(NSAS_ROWS)]
    assert grid[-1] - NSAS_FACE_H / 2 >= -BASE_H + 2.0, "bottom skin < 2 mm"
    rows = [grid[r - 1] for r in NSAS_KEEP_ROWS]
    dz = NSAS_COL_STEPS * NSAS_COL_PITCH
    return [(y, EXTRUDE / 2 + s * dz) for y in rows for s in (-1, 1)]


def _front_x(y):
    """X of the profile's front faces the holes can break out through:
    the leaning wall up to the wedge tip, the wedge's back face above."""
    t15 = math.tan(math.radians(WALL_ANGLE + WEDGE_ANGLE))
    y_tip = notch_polygons()[2][0][1]
    if y < y_tip:
        return _wall_x(y)
    return _wall_x(SLOT_TOP) + WEDGE_W - (SLOT_TOP - y) * t15


def hole_end_x(y_mouth):
    """Through holes (offset variant): X where a hole's flat end sits,
    HOLE_EXIT past the point where its lower edge breaks out of the front
    faces into the slot. Its upper edge must stay clear of the lip."""
    h = NSAS_FACE_H / 2

    def lower(x):  # lower edge, vertically under the axis
        return y_mouth + (RIGHT_X - x) - h

    lo, hi = 0.0, RIGHT_X  # x - front_x(lower(x)) is < 0 at lo, > 0 at hi
    for _ in range(60):
        mid = (lo + hi) / 2
        if mid - _front_x(lower(mid)) > 0:
            hi = mid
        else:
            lo = mid
    x_end = hi - HOLE_EXIT
    upper = y_mouth + (RIGHT_X - x_end) + h
    lip_bot = SLOT_TOP - LIP_DROP
    assert upper < lip_bot - HOLE_EXIT, "through hole would hit the lip"
    return x_end


def _nsas_holes(through=False):
    h = NSAS_HOLE / 2
    rise = h * math.tan(math.radians(NSAS_ROOF_ANGLE))
    holes = []
    for y, z in nsas_hole_centres():
        # Bar along X turned -45 deg about Z: axis along (1, -1), so going
        # in (-X) it rises (+Y).
        bar = bd.Box(100.0, NSAS_HOLE, NSAS_HOLE).rotate(bd.Axis.Z, -45)
        bar = bar.moved(bd.Location((RIGHT_X, y, z)))
        # Gable on the +Z face: sketch plane square to the hole axis,
        # local x across the hole in XY, local y = -Z.
        plane = bd.Plane(
            origin=(RIGHT_X, y, z), x_dir=(1, 1, 0), z_dir=(-1, 1, 0)
        )
        tri = plane * bd.Polygon((-h, -h), (h, -h), (0, -h - rise), align=None)
        roof = bd.extrude(tri, 50.0, both=True)
        # Flat end parallel to the back face.
        x_end = hole_end_x(y) if through else RIGHT_X - NSAS_DEPTH
        depth = RIGHT_X - x_end
        slab = bd.Box(depth + 1, 3 * TOP_Y, EXTRUDE + 2).moved(
            bd.Location((RIGHT_X - (depth - 1) / 2, y, z))
        )
        holes.append((bar + roof) & slab)
    return holes


def _window_set(a, b, z0, z1, sets=None):
    """`sets` (default WINDOW_SETS) windows from a to b across, stacked
    from z0 to z1 along Z with WINDOW_RIB between: flat bottom, 45 deg
    pointed top."""
    sets = WINDOW_SETS if sets is None else sets
    w = b - a
    h = (z1 - z0 - (sets - 1) * WINDOW_RIB) / sets
    assert h > w / 2 + 3, "window too short for its pointed top"
    out = []
    for k in range(sets):
        lo = z0 + k * (h + WINDOW_RIB)
        hi = lo + h
        out.append([(a, lo), (b, lo), (b, hi - w / 2), ((a + b) / 2, hi), (a, hi - w / 2)])
    return out


def window_outlines():
    """Window outlines as (Y, Z) points on the back face."""
    h = NSAS_HOLE / 2
    rise = h * math.tan(math.radians(NSAS_ROOF_ANGLE))
    zs = sorted({z for _, z in nsas_hole_centres()})
    z0 = zs[0] + h + rise + SHELL  # above the lower column's gable
    z1 = zs[1] - h - SHELL  # below the upper column's flat side
    # Y span where the main pocket is behind the back plate, clear of its
    # corner fillets and of the slanted top where it narrows.
    pk = pocket_points()
    y_lo, y_hi = pk[1][1] + SHELL / 2, pk[2][1] - SHELL
    n = int((y_hi - y_lo + WINDOW_RIB) // (WINDOW_W + WINDOW_RIB))
    pitch = (y_hi - y_lo - WINDOW_W) / (n - 1)
    out = []
    for i in range(n):
        y = y_lo + WINDOW_W / 2 + i * pitch
        out += _window_set(y - WINDOW_W / 2, y + WINDOW_W / 2, z0, z1)
    return out


def _windows():
    x0 = RIGHT_X - BACK_T - 0.5  # into the pocket
    plane = bd.Plane.YZ.offset(x0)
    return [
        bd.extrude(plane * bd.Polygon(*pts, align=None), BACK_T + 1.0)
        for pts in window_outlines()
    ]


def _wall_plane():
    """Plane on the leaning wall face: origin at its foot, local x up the
    wall, local y = +Z, normal into the body."""
    a = math.radians(WALL_ANGLE)
    return bd.Plane(
        origin=(WALL_X0, 0, 0),
        x_dir=(math.sin(a), math.cos(a), 0),
        z_dir=(math.cos(a), -math.sin(a), 0),
    )


def front_window_outlines():
    """Window outlines as (s, Z) on the wall face, s measured up the wall
    from its foot."""
    a = math.radians(WALL_ANGLE)
    # Up the wall: clear of the base notch below, and below the wedge tip
    # and the pocket's kink above, SHELL from each.
    wedge_tip = notch_polygons()[2][0][1]
    y_kink = pocket_points()[3][1]
    s_lo = SHELL / math.cos(a)
    s_hi = (min(wedge_tip, y_kink) - SHELL) / math.cos(a)
    n = int((s_hi - s_lo + WINDOW_RIB) // (WINDOW_W + WINDOW_RIB))
    pitch = (s_hi - s_lo - WINDOW_W) / (n - 1)
    z0, z1 = FRONT_WINDOW_MARGIN, EXTRUDE - FRONT_WINDOW_MARGIN
    out = []
    for i in range(n):
        s = s_lo + WINDOW_W / 2 + i * pitch
        out += _window_set(s - WINDOW_W / 2, s + WINDOW_W / 2, z0, z1)
    return out


def _front_windows():
    plane = _wall_plane().offset(-1.0)  # start outside the face
    return [
        bd.extrude(plane * bd.Polygon(*pts, align=None), SHELL + 2.0)
        for pts in front_window_outlines()
    ]


def _z_edges_near(body, points, tol=0.05):
    """Edges parallel to Z whose XY passes through any of `points`."""
    found = []
    for e in body.edges().filter_by(bd.Axis.Z):
        c = e.center()
        if any(abs(c.X - x) < tol and abs(c.Y - y) < tol for x, y in points):
            found.append(e)
    assert len(found) == len(points), (len(found), points)
    return found


def base_face_x():
    """X of the NABS base's top face when keyed on: on the offset face,
    since the key stops sit in recesses in it."""
    return RIGHT_X - OFFSET_W


def _stop_recesses():
    """Offset variant: a KEY_STOP deep pocket in the offset face round
    each hole mouth, the stop plate's shape plus STOP_CLEAR: in the
    profile a parallelogram along the hole axis, 2 x STOP_HALF tall.
    Printed profile-down its roof (+Z) would be a flat 3 mm overhang, so
    it slopes up at 45 deg from the recess floor to the face instead."""
    x0 = base_face_x()
    x1 = x0 - KEY_STOP  # recess floor
    hz = STOP_W / 2 + STOP_CLEAR
    hy = STOP_HALF + STOP_CLEAR
    out = []
    for y, z in nsas_hole_centres():

        def axis(x):  # hole axis Y at X
            return y + (RIGHT_X - x)

        xo = x0 + 1.0  # start outside the face
        pts = [
            (x1, axis(x1) - hy),
            (xo, axis(xo) - hy),
            (xo, axis(xo) + hy),
            (x1, axis(x1) + hy),
        ]
        top = z + hz + (xo - x1)  # roof height at xo
        face = bd.Polygon(*pts, align=None).moved(bd.Location((0, 0, z - hz)))
        recess = bd.extrude(face, top - (z - hz), dir=(0, 0, 1))
        # Cut off everything above the roof plane z = z + hz + (x - x1).
        roof = bd.Polygon(
            (x1 - 10, z + hz - 10), (xo + 10, top + 10),
            (xo + 10, top + 50), (x1 - 10, top + 50), align=None,
        )
        above = bd.extrude(
            bd.Plane.XZ * roof, 100, both=True
        ).moved(bd.Location((0, axis(x1), 0)))
        out.append(recess - above)
    return out


def _span_windows(spans, z0, z1):
    """Pointed-top windows along each (lo, hi) span, WINDOW_W wide and
    WINDOW_RIB apart, or one narrower window in a short span."""
    out = []
    for lo, hi in spans:
        length = hi - lo
        if length < 5.0:
            continue
        n = max(1, int((length + WINDOW_RIB) // (WINDOW_W + WINDOW_RIB)))
        w = min(WINDOW_W, length)
        pitch = (length - w) / (n - 1) if n > 1 else 0
        for i in range(n):
            a = lo + i * pitch if n > 1 else lo + (length - w) / 2
            out += _window_set(a, a + w, z0, z1, sets=1)
    return out


def _offset_window_band():
    """Z band between the hole columns, SHELL clear of the stop recesses
    (with their sloped roofs) and the hole gables."""
    zs = sorted({z for _, z in nsas_hole_centres()})
    hz = STOP_W / 2 + STOP_CLEAR
    return zs[0] + hz + KEY_STOP + SHELL, zs[1] - hz - SHELL


def offset_window_spans():
    """Y spans of the offset pockets on the offset face side (at the
    pocket back, X = xb) and on the leaning wall side, WINDOW_MARGIN in from
    the pocket edges; the windows run WINDOW_IN past the pocket wall."""
    t5 = math.tan(math.radians(WALL_ANGLE))
    w = (NSAS_HOLE / 2 + SLEEVE) * math.sqrt(2)
    c_lo, c_hi = sorted(RIGHT_X + y for y in {y for y, _ in nsas_hole_centres()})
    m, d = WINDOW_MARGIN, WINDOW_IN
    pk = pocket_points(base_face_x() - KEY_STOP - RECESS_SKIN)
    xb, y_bot, y_top, y_kink = pk[1][0], pk[0][1], pk[2][1], pk[3][1]
    back = [
        (y_bot + m, c_lo - w - xb - m),
        (c_lo + w - (xb - d) + m, min(c_hi - w - xb, y_top) - m),
    ]
    x0w = WALL_X0 + SHELL / math.cos(math.radians(WALL_ANGLE))  # pocket front
    k = 1 + t5
    front = [
        (y_bot + m, (c_lo - w - x0w - d - m) / k),
        ((c_lo + w + SHELL - x0w + m) / k, min((c_hi - w - x0w - d - m) / k, y_kink - m)),
    ]
    return back, front


def _offset_windows():
    z0, z1 = _offset_window_band()
    back, front = offset_window_spans()
    xb = base_face_x() - KEY_STOP - RECESS_SKIN
    plane = bd.Plane.YZ.offset(xb - WINDOW_IN)
    depth = base_face_x() + 1.0 - (xb - WINDOW_IN)
    out = [
        bd.extrude(plane * bd.Polygon(*pts, align=None), depth)
        for pts in _span_windows(back, z0, z1)
    ]
    # Front: on the wall plane, s up the wall = y / cos(WALL_ANGLE).
    c = math.cos(math.radians(WALL_ANGLE))
    s_spans = [(lo / c, hi / c) for lo, hi in front]
    wall = _wall_plane().offset(-1.0)
    out += [
        bd.extrude(wall * bd.Polygon(*pts, align=None), 1.0 + SHELL + WINDOW_IN)
        for pts in _span_windows(s_spans, z0, z1)
    ]
    return out


def offset_top():
    """Y of the overhang's underside: the top of the NABS base when keyed
    on (its upper row's mouth centre on its face, where the holder's top
    hole axis meets base_face_x(), plus the row's distance from
    body face A and the hinge fingers), plus OFFSET_CLEAR."""
    y_hole = max(y for y, _ in nsas_hole_centres())
    base_top = y_hole + (RIGHT_X - base_face_x()) + NABS_ROW1_MOUTH + NABS_FINGER
    return base_top + OFFSET_CLEAR


def offset_points():
    """Offset variant: rectangle cut from the back, OFFSET_W deep, from
    below the base up to offset_top(); the top block above stays as an
    overhang just over the NABS base."""
    x0, x1 = RIGHT_X - OFFSET_W, RIGHT_X + 1.0
    y0, y1 = -BASE_H - 1.0, offset_top()
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


# Variants:
#   flat    mounts straight on an NSAS panel: main pocket, windows into it.
#   offset  to mount over a NABS base piece (work in progress): the main
#           pocket is split round the hole tunnels, with windows into it; the
#           NSAS holes run on through the wall into the slot; an
#           OFFSET_W rectangle is cut from the back, from the bottom up
#           to offset_top(), so the overhang above sits just over the base;
#           the key stops sit in recesses, so the holder is flush on the base.
VARIANTS = {
    "flat": dict(main_pocket=True, offset=False),
    "offset": dict(main_pocket=False, offset=True),  # own pockets
}


def slot_in_holder_shape(variant="flat"):
    opts = VARIANTS[variant]
    base, strip, wedge = notch_polygons()
    face = bd.Polygon(*profile_points(), align=None)
    pockets = [upper_pocket_points()]
    if opts["main_pocket"]:
        pockets.insert(0, pocket_points())
    elif opts["offset"]:
        pockets = offset_pocket_regions() + pockets
    cuts = [base, strip, wedge] + pockets
    if opts["offset"]:
        cuts.append(offset_points())
    for cut in cuts:
        if not isinstance(cut, bd.Face):
            cut = bd.Polygon(*cut, align=None)
        face = face - cut
    body = bd.extrude(face, EXTRUDE).clean()
    if opts["offset"]:
        # Inner corner where the offset meets the overhang above it.
        corner = offset_points()[3]
        body = body.fillet(OFFSET_R, _z_edges_near(body, [corner]))

    # Inner corners: base notch floor, pockets. (The wedge tip is a 170 deg
    # corner of the slot: no fillet, it would block the end chamfer.)
    body = body.fillet(NOTCH_R, _z_edges_near(body, base[:2]))
    for pts in pockets:
        if isinstance(pts, bd.Face):
            pts = [(v.X, v.Y) for v in pts.vertices()]
        body = body.fillet(POCKET_R, _z_edges_near(body, pts))
    # Lip root: lip inner face meets the strip roof.
    body = body.fillet(LIP_ROOT_R, _z_edges_near(body, strip[3:]))
    # Lead-ins: lip inner bottom edge, ledge front top edge.
    lip = profile_points()[5]
    body = body.chamfer(LIP_LEAD, None, _z_edges_near(body, [lip]))
    body = body.fillet(LEDGE_R, _z_edges_near(body, [profile_points()[-1]]))
    ends = body.faces().filter_by(bd.Axis.Z)
    outline = [e for f in ends for e in f.outer_wire().edges()]
    body = body.chamfer(END_CHAMFER, None, outline)
    for hole in _nsas_holes(through=opts["offset"]):
        body = body - hole
    if opts["offset"]:
        for cut in _stop_recesses() + _offset_windows():
            body = body - cut
    if opts["main_pocket"]:
        for window in _windows() + _front_windows():
            body = body - window
    return body.clean()


NAME = "IKEA UPPDATERA and VARIERA - NSAS slot in holder"


def _variant(name):
    body = slot_in_holder_shape(name)
    body.label = f"slot_in_holder_{name}"
    return body


@stl(out=f"../{NAME} - flat.stl")
@step(out=f"../{NAME} - flat.step")
def slot_in_holder_flat():
    return _variant("flat")


@stl(out=f"../{NAME} - offset.stl")
@step(out=f"../{NAME} - offset.step")
def slot_in_holder_offset():
    return _variant("offset")


if __name__ == "__main__":
    slot_in_holder_flat()
    slot_in_holder_offset()
