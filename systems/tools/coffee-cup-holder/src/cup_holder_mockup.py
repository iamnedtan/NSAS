"""Mockup: Starbucks cup seated in its holder, to check how it sits.

Not for printing. The cup is a 0.5 mm shell with a simple rolled lip, built
from the measured body values only (no lid). It sits where its taper meets
the bore (line-to-line), on the holder's bore axis, with its lower part
below the ring. A second output cuts both in
half on the YZ plane so the seat in the bore shows.
"""
from __future__ import annotations

import sys
from pathlib import Path

from cadgen import build123d as bd
from cadgen import step

sys.path.insert(0, str(Path(__file__).resolve().parent))  # run with python -I
import cup_holder as ch  # noqa: E402

CUP_SHELL = 0.5
LIP_H = 1.5  # rolled lip above the "under lip" diameter
LIP_OUT = 0.8  # lip overhang, radial


def cup_shape(top_d, bot_d, slant, label=None):
    h = ch.cup_height(top_d, bot_d, slant)
    up = (bd.Align.CENTER,) * 2 + (bd.Align.MIN,)
    outer = bd.Cone(bot_d / 2, top_d / 2, h, align=up)
    inner = bd.Cone(
        bot_d / 2 - CUP_SHELL, top_d / 2 - CUP_SHELL, h, align=up
    ).moved(bd.Location((0, 0, CUP_SHELL)))
    lip = bd.Cylinder(top_d / 2 + LIP_OUT, LIP_H, align=up) - bd.Cylinder(
        top_d / 2 - CUP_SHELL, LIP_H, align=up
    )
    return (outer - inner) + lip.moved(bd.Location((0, 0, h)))


def mockup(half=False):
    v = ch.VARIANTS["starbucks"]
    _, _, axis_y, cup_z = ch.bore_fit(**v)
    holder = ch.cup_holder_shape(**v)
    cup = cup_shape(**v).moved(bd.Location((0, axis_y, cup_z)))
    if half:
        keep = bd.Box(100, 100, 100, align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.MIN))
        keep = keep.moved(bd.Location((0, 0, -30)))
        holder, cup = holder & keep, cup & keep
    holder.label = "holder"
    cup.label = "starbucks_cup"
    return bd.Compound(children=[holder, cup], label="cup_holder_mockup")


@step(out="../mockup/cup_holder_starbucks_mockup.step")
def cup_holder_starbucks_mockup():
    return mockup()


@step(out="../mockup/cup_holder_starbucks_mockup_half.step")
def cup_holder_starbucks_mockup_half():
    return mockup(half=True)


if __name__ == "__main__":
    cup_holder_starbucks_mockup()
    cup_holder_starbucks_mockup_half()
