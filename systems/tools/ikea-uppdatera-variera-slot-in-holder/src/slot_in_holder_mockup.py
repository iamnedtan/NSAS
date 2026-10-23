"""Mockup: the offset variant on a NABS base standing vertical (wall
mode), joined by four thick-stop NSAS keys. Not for printing.

The NABS base (systems/nabs, 10 columns) stands with edge B down, its top
face (socket mouths) toward the holder, so its sockets run in and down
like an NSAS panel's. Its two rows are 37.071 mm apart, the same as the
holder's rows 3 and 5. Each key's panel leg sits in a base socket and its
accessory leg in a holder hole; the key's 1 mm stop sits between the
base's top face and the floor of a recess in the holder's offset face,
so the holder sits flush on the base.

Built in the holder's coordinates (X toward the base, Y up, Z along the
width), then turned 90 deg about X so the output stands Z-up.
"""
from __future__ import annotations

import sys
from pathlib import Path

from cadgen import build123d as bd
from cadgen import step

sys.path.insert(0, str(Path(__file__).resolve().parent))  # run with python -I
import slot_in_holder as sh  # noqa: E402

REPO = Path(__file__).resolve().parents[4]
NABS_BASE = REPO / "systems/nabs/parts/NABS base.step"
KEY = REPO / "keys/NSAS key - accessories thick.step"

KEY_STOP = sh.KEY_STOP
NABS_T = 10.0  # base thickness
NABS_FINGER = sh.NABS_FINGER
NABS_ROW1_MOUTH = sh.NABS_ROW1_MOUTH
NABS_COL0 = 5.0  # first socket centre, along from the side


def placements():
    """Base face X, and the key mouth points (Y, Z) on that face."""
    face_x = sh.base_face_x()
    # Each hole axis runs x + y = RIGHT_X + y_mouth; where it meets the
    # base face is the socket mouth centre.
    mouths = [
        (y + (sh.RIGHT_X - face_x), z) for y, z in sh.nsas_hole_centres()
    ]
    return face_x, mouths


def mockup():
    face_x, mouths = placements()
    holder = sh.slot_in_holder_shape("offset")
    holder.label = "slot_in_holder_offset"

    # NABS frame: X across (body face A at X = 10), Y along, Z up from the
    # bottom face. Across -> down, Z -> toward the holder, along -> width.
    y_top_mouth = max(y for y, _ in mouths)
    z_first = min(z for _, z in mouths)
    base_plane = bd.Plane(
        origin=(
            face_x + NABS_T,
            y_top_mouth + NABS_ROW1_MOUTH + NABS_FINGER,
            z_first - (NABS_COL0 + 10.0),  # holder column 1 on base column 2
        ),
        x_dir=(0, -1, 0),
        z_dir=(-1, 0, 0),
    )
    base = bd.import_step(NABS_BASE).moved(bd.Location(base_plane))
    base.label = "NABS_base"

    # Key frame: X out of the panel (panel face at X = 0), Z up, axis
    # through the origin.
    key0 = bd.import_step(KEY)
    keys = []
    for i, (y, z) in enumerate(mouths):
        plane = bd.Plane(origin=(face_x, y, z), x_dir=(-1, 0, 0), z_dir=(0, 1, 0))
        key = key0.moved(bd.Location(plane))
        key.label = f"NSAS_key_{i + 1}"
        keys.append(key)

    # Stand it up for viewing: the holder's Y (up in use) becomes Z.
    up = bd.Location((0, 0, 0), (1, 0, 0), 90)
    parts = [p.moved(up) for p in [holder, base] + keys]
    for p, src in zip(parts, [holder, base] + keys):
        p.label = src.label
    asm = bd.Compound(children=parts)
    asm.label = "slot_in_holder_offset_on_NABS_base"
    return asm


@step(out="../mockup/slot_in_holder_offset_on_NABS_base.step")
def slot_in_holder_offset_mockup():
    return mockup()


if __name__ == "__main__":
    slot_in_holder_offset_mockup()
