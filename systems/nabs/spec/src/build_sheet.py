"""Build the NABS spec sheet (../NABS Spec Sheet.html).

The drawings are cut from the Fusion export with OCP, so they are true to the model.
The styles are those of the NSAS spec sheet (spec/NSAS Spec Sheet.html).

Run with the cadgen venv Python (OCP is needed, build123d is not):

    python -I build_sheet.py "D:/OneDrive/Stay Home Geek 3d Design/angleslot system.step"
"""

import html
import math
import re
import sys
from pathlib import Path

from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_Transform
from OCP.BRepTools import BRepTools_WireExplorer
from OCP.GeomAbs import GeomAbs_Line
from OCP.gp import gp_Dir, gp_Pln, gp_Pnt, gp_Trsf, gp_Vec
from OCP.STEPControl import STEPControl_Reader
from OCP.TopAbs import TopAbs_FACE, TopAbs_REVERSED, TopAbs_SOLID, TopAbs_WIRE
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "NABS Spec Sheet.html"
NSAS_SHEET = HERE.parents[3] / "spec" / "NSAS Spec Sheet.html"

# Body order in the Fusion export "angleslot system.step".
BASE, BASE_V, SLOT_IN, RUNNER, BASE_M3, RUNNER_LOOSE, ADAPTER, JOINER = range(8)

ROW_PITCH = 37.071   # 2 x 18.536
BASE_PITCH = 74.142  # two bases pinned flat
PIN = 69.142         # pin axis, across: 5.0 past body face B, mid-finger


# ── geometry ────────────────────────────────────────────────────────────

def load_solids(path):
    r = STEPControl_Reader()
    r.ReadFile(str(path))
    r.TransferRoots()
    out, ex = [], TopExp_Explorer(r.OneShape(), TopAbs_SOLID)
    while ex.More():
        out.append(TopoDS.Solid_s(ex.Current()))
        ex.Next()
    return out


def moved(shape, dx=0.0, dy=0.0, dz=0.0):
    t = gp_Trsf()
    t.SetTranslation(gp_Vec(dx, dy, dz))
    return BRepBuilderAPI_Transform(shape, t, True).Shape()


# Each view maps model (x, y, z) to drawing (u, v), v pointing down the page.
VIEWS = {
    "y": lambda p: (p[0], -p[2]),   # section across the base, looking along the rows
    "z": lambda p: (p[1], p[0]),    # plan from above, rows running left to right, edge A at the top
    "x": lambda p: (p[1], -p[2]),   # section along the middle channel
}


def section(shape, axis, value, view=None):
    """Cut shape with a plane; return a list of faces, each a list of loops of (u, v) points."""
    d = {"x": gp_Dir(1, 0, 0), "y": gp_Dir(0, 1, 0), "z": gp_Dir(0, 0, 1)}[axis]
    p = gp_Pnt(*(value if a == axis else 0.0 for a in "xyz"))
    plane = BRepBuilderAPI_MakeFace(gp_Pln(p, d), -1000, 1000, -1000, 1000).Face()
    op = BRepAlgoAPI_Common(shape, plane)
    op.Build()
    to_uv = view or VIEWS[axis]
    faces = []
    fe = TopExp_Explorer(op.Shape(), TopAbs_FACE)
    while fe.More():
        face = TopoDS.Face_s(fe.Current())
        loops = []
        we = TopExp_Explorer(face, TopAbs_WIRE)
        while we.More():
            wire = TopoDS.Wire_s(we.Current())
            pts = []
            ed = BRepTools_WireExplorer(wire, face)
            while ed.More():
                edge = ed.Current()
                c = BRepAdaptor_Curve(edge)
                n = 1 if c.GetType() == GeomAbs_Line else 24
                t0, t1 = c.FirstParameter(), c.LastParameter()
                ts = [t0 + (t1 - t0) * i / n for i in range(n + 1)]
                if edge.Orientation() == TopAbs_REVERSED:
                    ts.reverse()
                for t in ts[:-1]:
                    q = c.Value(t)
                    pts.append(to_uv((q.X(), q.Y(), q.Z())))
                ed.Next()
            loops.append(pts)
            we.Next()
        faces.append(loops)
        fe.Next()
    return faces


def bbox(loop):
    us = [p[0] for p in loop]
    vs = [p[1] for p in loop]
    return min(us), min(vs), max(us), max(vs)


def area(loop):
    a = 0.0
    for (x1, y1), (x2, y2) in zip(loop, loop[1:] + loop[:1]):
        a += x1 * y2 - x2 * y1
    return abs(a) / 2


# ── SVG ─────────────────────────────────────────────────────────────────

def f(x):
    s = f"{x:.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def path_d(loops):
    return " ".join("M" + " L".join(f"{f(u)},{f(v)}" for u, v in loop) + " Z" for loop in loops)


class Fig:
    def __init__(self, box, fs, hatch_id, hatch=0.6):
        self.box = box  # (u0, v0, w, h)
        self.fs = fs
        self.hatch_id = hatch_id
        self.hatch = hatch
        self.items = []

    def add(self, s):
        self.items.append(s)

    def cut(self, faces, cls="cut"):
        """Hatched section of a panel or base; cut2 hatches the other way, for a second body."""
        pattern = self.hatch_id + ("b" if cls == "cut2" else "")
        for loops in faces:
            d = path_d(loops)
            self.add(f'<path class="{cls}" fill-rule="evenodd" fill="url(#{pattern})" d="{d}"/>')
            self.add(f'<path class="part" fill-rule="evenodd" d="{d}"/>')

    def key(self, faces):
        """Shaded section of a slot-in part."""
        for loops in faces:
            self.add(f'<path class="key" fill-rule="evenodd" d="{path_d(loops)}"/>')

    def poly(self, pts, cls, closed=True):
        tag = "polygon" if closed else "polyline"
        self.add(f'<{tag} class="{cls}" points="{" ".join(f"{f(u)},{f(v)}" for u, v in pts)}"/>')

    def line(self, a, b, cls):
        self.add(f'<line class="{cls}" x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(b[0])}" y2="{f(b[1])}"/>')

    def text(self, p, s, cls="note", anchor="start", rot=0):
        tr = f' transform="rotate({f(rot)} {f(p[0])} {f(p[1])})"' if rot else ""
        self.add(f'<text class="{cls}" x="{f(p[0])}" y="{f(p[1])}" font-size="{f(self.fs)}" '
                 f'text-anchor="{anchor}" dominant-baseline="middle"{tr}>{html.escape(s)}</text>')

    def arrow(self, tip, direction, cls="arrow"):
        ux, uy = direction
        n = math.hypot(ux, uy)
        ux, uy = ux / n, uy / n
        L, W = 0.6 * self.fs, 0.19 * self.fs
        bx, by = tip[0] - ux * L, tip[1] - uy * L
        self.poly([tip, (bx - uy * W, by + ux * W), (bx + uy * W, by - ux * W)], cls)

    def dim(self, p1, p2, off, label, text_side=1):
        """Aligned dimension between p1 and p2, dimension line offset by off (signed, to the left of p1→p2)."""
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        nx, ny = uy, -ux  # left normal on screen (v down)
        a = (p1[0] + nx * off, p1[1] + ny * off)
        b = (p2[0] + nx * off, p2[1] + ny * off)
        g = 0.15 * self.fs * (1 if off > 0 else -1)
        e = 0.35 * self.fs * (1 if off > 0 else -1)
        self.line((p1[0] + nx * g, p1[1] + ny * g), (a[0] + nx * e, a[1] + ny * e), "ext")
        self.line((p2[0] + nx * g, p2[1] + ny * g), (b[0] + nx * e, b[1] + ny * e), "ext")
        inside = L > 1.6 * self.fs
        if inside:
            self.line(a, b, "dim")
            self.arrow(a, (-ux, -uy))
            self.arrow(b, (ux, uy))
        else:
            o = 0.9 * self.fs
            self.line((a[0] - ux * o, a[1] - uy * o), (b[0] + ux * o, b[1] + uy * o), "dim")
            self.arrow(a, (ux, uy))
            self.arrow(b, (-ux, -uy))
        ang = math.degrees(math.atan2(dy, dx))
        if ang > 90.01 or ang < -89.99:
            ang -= 180 if ang > 0 else -180
        s = 0.6 * self.fs * text_side * (1 if off > 0 else -1)
        m = ((a[0] + b[0]) / 2 + nx * s, (a[1] + b[1]) / 2 + ny * s)
        self.text(m, label, "dimt", "middle", ang)

    def lead(self, at, to, lines, right=None):
        self.line(at, to, "lead")
        self.add(f'<circle class="dot" cx="{f(at[0])}" cy="{f(at[1])}" r="{f(0.17 * self.fs)}"/>')
        if right is None:
            right = to[0] >= at[0]
        x = to[0] + (0.25 if right else -0.25) * self.fs
        for i, s in enumerate(lines):
            self.text((x, to[1] + i * 1.25 * self.fs), s, "note", "start" if right else "end")

    def svg(self, label, max_w, min_w):
        u0, v0, w, h = self.box
        hp = self.hatch
        return (f'<svg class="dwg" viewBox="{f(u0)} {f(v0)} {f(w)} {f(h)}" style="max-width:{max_w}px;min-width:{min_w}px" '
                f'role="img" aria-label="{html.escape(label)}" xmlns="http://www.w3.org/2000/svg"><defs>'
                f'<pattern id="{self.hatch_id}" patternUnits="userSpaceOnUse" width="{f(hp)}" height="{f(hp)}" '
                f'patternTransform="rotate(45)"><line class="hatchl" x1="0" y1="0" x2="0" y2="{f(hp)}"/></pattern>'
                f'<pattern id="{self.hatch_id}b" patternUnits="userSpaceOnUse" width="{f(hp)}" height="{f(hp)}" '
                f'patternTransform="rotate(-45)"><line class="hatchl" x1="0" y1="0" x2="0" y2="{f(hp)}"/></pattern>'
                f'</defs>\n' + "\n".join(self.items) + "</svg>")


def clip(fig, box_id, rect, inner):
    """Wrap items added by inner() in a clip rectangle."""
    u, v, w, h = rect
    fig.add(f'<defs><clipPath id="{box_id}"><rect x="{f(u)}" y="{f(v)}" width="{f(w)}" height="{f(h)}"/></clipPath></defs>')
    start = len(fig.items)
    inner()
    body = fig.items[start:]
    del fig.items[start:]
    fig.add(f'<g clip-path="url(#{box_id})">' + "\n".join(body) + "</g>")


# ── figures ─────────────────────────────────────────────────────────────

def fig_section(S):
    """View A: section across the base through a socket column, edge A on the left."""
    fig = Fig((-31, -31, 119, 47), 1.6, "hA", 0.7)
    fig.cut(section(S[BASE], "y", 4.0))
    for c in (13.536, 50.607):  # socket axes
        fig.line((c - 3, -13), (c + 13.2, 3.2), "ctr")
    top = -10
    fig.dim((0, top), (10, top), 4.0, "10.000")
    fig.dim((10, top), (17.071, top), 4.0, "7.071")
    fig.dim((17.071, top), (47.071, top), 4.0, "30.000")
    fig.dim((47.071, top), (54.142, top), 4.0, "7.071")
    fig.dim((13.536, top), (50.607, top), 9.0, "37.071 row pitch = 2 × 18.536")
    fig.dim((-10, 0), (0, 0), -4.2, "10.0")
    fig.dim((0, 0), (64.142, 0), -4.2, "64.142 body")
    fig.dim((33.071, 0), (41.071, 0), -8.8, "8.0 channel")
    fig.dim((64.142, 0), (64.142, -10), -4.0, "10.0")
    fig.dim((25.0, -5.0), (21.465, -8.535), 6.2, "5.00 ⊥")
    r, cx = 5.5, 20.0
    fig.add(f'<path class="dimarc" d="M{f(cx - r)},0 A{f(r)},{f(r)} 0 0 1 {f(cx - r * math.cos(math.pi / 4))},{f(-r * math.sin(math.pi / 4))}"/>')
    fig.text((cx - r - 0.8, -2.4), "45°", "dimt", "end")
    fig.lead((-5.6, -5.6), (-14, -16), ["pin hole Ø2.5,", "1.75 filament"])
    fig.lead((24.0, -3.5), (17, 7.5), ["through socket"])
    fig.lead((6.0, -4.0), (-2, 11.5), ["underside hollow"])
    fig.lead((37.0, -2.5), (46, 7.5), ["channel hole (floor 5.0", "between holes)"])
    fig.lead((28.5, -8.0), (32, -24.8), ["top pocket"])
    fig.text((-10, -28.5), "EDGE A", "lbl", "start")
    fig.text((74.142, -28.5), "EDGE B", "lbl", "end")
    fig.text((86, 14), "SOCKETS DESCEND TOWARD EDGE B", "lbl", "end")
    return fig.svg("Section across the base through one socket column", 920, 540)


def fig_plan(S):
    """View B: plan of the base, rows running left to right."""
    fig = Fig((-27, -27, 146, 125), 1.75, "hB", 0.8)
    top = section(S[BASE], "z", 9.95)
    low = section(S[BASE], "z", 2.5)
    fig.add('<rect class="groovef" x="0" y="33.071" width="100" height="8"/>')
    for loops in low:
        for lp in loops[1:]:
            u0, v0, u1, v1 = bbox(lp)
            if 33 < v0 and v1 < 41.2:
                fig.poly(lp, "holef")
    for loops in top:
        fig.add(f'<path class="sheetfill" fill-rule="evenodd" d="{path_d(loops)}"/>')
        for lp in loops[1:]:
            u0, v0, u1, v1 = bbox(lp)
            w, h = u1 - u0, v1 - v0
            if w > 20:
                fig.poly(lp, "groovef")          # top pocket
            elif w < 4.5 and h < 4.0:
                fig.poly(lp, "part")             # triangle mark
            else:
                fig.poly(lp, "holef")            # socket mouth
    fig.dim((5, -10), (15, -10), 5.4, "10.00 pitch")
    fig.dim((0, -10), (5, -10), 1.8, "5.0")
    fig.dim((0, 74.142), (100, 74.142), -4.6, "L = n × 10.0 (n = 10)")
    fig.dim((2.5, 74.142), (48.0, 74.142), -9.6, "45.5 pocket")
    fig.dim((48.0, 74.142), (52.0, 74.142), -9.6, "4.0")
    fig.dim((100, -10), (100, 74.142), 4.6, "84.142 overall")
    fig.lead((20, 5.73), (24, -22), ["triangle mark, points to edge B"])
    fig.lead((55, 13.5), (62, -22), ["socket mouth 5.0 × 7.071"])
    fig.lead((85, 25), (91, -17), ["top pocket,", "⌈n/5⌉ per row"])
    fig.lead((65, 37.07), (72, 93.5), ["channel hole 8.0 × 5.0,", "one per column"])
    fig.lead((27.5, 79), (36, 93.5), ["edge-B finger 4.75"])
    fig.lead((2.5, -7), (-3, -22), ["edge-A finger 4.95"])
    fig.text((-24, -6), "EDGE A", "lbl", "end", -90)
    fig.text((-24, 80), "EDGE B", "lbl", "start", -90)
    fig.text((0, 96.5), "SIDE", "lbl", "start")
    fig.text((100, 96.5), "SIDE", "lbl", "end")
    return fig.svg("Plan of a 10-column base", 940, 560)


def fig_hinge(S):
    """View C: two bases pinned flat, plan at mid-finger height (cut above the pin)."""
    fig = Fig((-4, 47, 54, 42), 1.25, "hC", 0.55)
    a = section(S[BASE], "z", 7.5)
    b = section(moved(S[BASE], dx=BASE_PITCH), "z", 7.5)

    def body():
        fig.cut(a)
        fig.cut(b, "cut2")
    clip(fig, "clipC", (0, 57.5, 30, 22), body)
    for v in (PIN - 1.25, PIN + 1.25):
        fig.line((0, v), (30, v), "holeline")
    fig.line((-1.5, PIN), (31.5, PIN), "ctr")
    fig.dim((0, 64.142), (4.95, 64.142), 9.0, "4.95")
    fig.dim((4.95, 64.142), (5.15, 64.142), 5.6, "0.20")
    fig.dim((5.15, 74.142), (9.9, 74.142), -9.0, "4.75")
    fig.dim((30, 64.142), (30, 74.142), 3.2, "10.0")
    fig.dim((30, 64.142), (30, PIN), 7.4, "5.0")
    fig.lead((22, PIN), (16, 86), ["pin hole Ø2.5, full length"])
    fig.text((40.5, 60.5), "BASE 1", "lbl", "start")
    fig.text((40.5, 77.5), "BASE 2", "lbl", "start")
    return fig.svg("Hinge fingers of two bases pinned flat", 460, 320)


def fig_finger(S):
    """View C2: section through an edge-A finger and the pin."""
    fig = Fig((-17, -17, 36, 27), 1.25, "hC2", 0.55)
    faces = section(S[BASE], "y", 2.5)

    def body():
        fig.cut(faces)
    clip(fig, "clipC2", (-11, -11.5, 18, 12.2), body)
    fig.add('<circle class="key" cx="-5" cy="-5" r="0.875"/>')
    fig.line((-5, -8.2), (-5, -1.8), "ctr")
    fig.line((-8.2, -5), (-1.8, -5), "ctr")
    fig.dim((-10, -10), (-5, -10), 2.4, "5.0")
    fig.dim((-10, -10), (0, -10), 5.2, "10.0 finger")
    fig.dim((-10, 0), (-10, -5), -2.8, "5.0")
    fig.lead((-4.4, -4.4), (1.5, 4.5), ["Ø2.5 hole, Ø1.75 pin"])
    fig.text((7, -6), "BODY", "lbl", "start")
    return fig.svg("Section through a hinge finger and its pin", 420, 280)


def fig_slot_in(S):
    """View D1: standard slot in seated in a base."""
    fig = Fig((-5, -33, 81, 50), 2.4, "hD", 0.7)
    fig.key(section(S[SLOT_IN], "y", 15.0))
    fig.cut(section(S[BASE], "y", 15.0))
    fig.dim((64.142, -10), (64.142, -19), -3.6, "9.0")
    fig.dim((0, -19), (64.142, -19), 4.0, "64.142")
    fig.lead((23.0, -3.6), (30, 9.0), ["leg 4.6 square, 9.5 ⊥ deep,", "0.5 above the bottom"])
    fig.lead((10, -14.5), (16, -27.5), ["body rests on the top face"])
    return fig.svg("Standard slot in seated in a base", 620, 380)


def fig_runner(S):
    """View D2: runner slot in holding a floor base and a folded wall base."""
    fig = Fig((-6, -92, 98, 106), 2.6, "hD2", 0.8)
    fig.key(section(S[RUNNER], "y", 5.0))
    fig.cut(section(S[BASE], "y", 5.0))
    fig.cut(section(S[BASE_V], "y", 5.0))
    fig.lead((15, -14), (-4, 7.5), ["floor arm: runner taped or", "cable-tied along the V-groove"], right=True)
    fig.lead((60.5, -45), (28, -64), ["wall arm"])
    fig.dim((64.142, -23.536), (64.142, -60.607), 12.0, "37.071")
    fig.text((-4, -86), "FLOOR BASE + FOLDED WALL BASE", "lbl", "start")
    return fig.svg("Runner slot in holding a floor base and a wall base", 620, 380)


def fig_joiner(S):
    """View E: side joiner across the joint between two bases, section along the middle channel."""
    fig = Fig((79, -26, 46, 38), 1.5, "hE", 0.6)
    a = section(S[BASE], "x", 37.0)
    b = section(moved(S[BASE], dy=100.0), "x", 37.0)
    j = section(moved(S[JOINER], dy=-150.0), "x", 37.0)

    def body():
        fig.key(j)
        fig.cut(a)
        fig.cut(b, "cut2")
    clip(fig, "clipE", (82, -12, 36, 14), body)
    fig.line((100, -20), (100, 4), "ctr")
    fig.dim((95, -8.5), (105, -8.5), 6.0, "10.0 C–C")
    fig.dim((92.7, -8.5), (107.3, -8.5), 11.0, "14.6")
    fig.dim((118, -10), (118, -8.5), -3.0, "1.5")
    fig.text((89, 5.5), "BASE 1", "lbl", "middle")
    fig.text((111, 5.5), "BASE 2", "lbl", "middle")
    fig.text((100, 10), "SIDE JOINT", "lbl", "middle")
    return fig.svg("Side joiner across the joint between two bases", 560, 360)


def fig_adapter(S):
    """View F: stack angle adapter, base hung on an NSAS panel. Panel face vertical, edge B down."""
    view = lambda p: (-p[2], p[0])  # base left of the panel face, panel right; edge B down
    fig = Fig((-32, 12, 60, 54), 1.9, "hF", 0.6)
    base = section(S[BASE_M3], "y", 205.0, view)
    adp = section(S[ADAPTER], "y", 205.0, view)

    def body():
        fig.cut(base)
    clip(fig, "clipF", (-10.6, 20, 11.2, 40), body)
    # NSAS panel, schematic: 12 thick, socket 5.0 square, 11.0 deep, centred on the leg axis x + z = c
    c = 36.3235
    h = 2.5 * math.sqrt(2)
    outer = [(0, 20), (12, 20), (12, 60), (0, 60)]
    sock = [(0, c - h), (11, c - h + 11), (11, c + h + 11), (0, c + h)]
    d = path_d([outer, sock])
    fig.add(f'<path class="cut2" fill-rule="evenodd" fill="url(#hFb)" d="{d}"/>')
    fig.add(f'<path class="part" fill-rule="evenodd" d="{d}"/>')
    fig.key(adp)
    for v in (19.4, 60.6):
        fig.line((0, v), (12, v), "brk")
    fig.line((-10.6, 20), (-10.6, 60), "brk")
    fig.dim((0, 60), (9.5, 60), -3.0, "9.5 ⊥")
    fig.lead((-7.5, 37.5), (-15, 26.5), ["plug in the", "middle channel"])
    fig.lead((5.0, 41.2), (14, 52.5), ["leg 4.6, 45°"])
    fig.text((-1.5, 16.5), "NABS BASE", "lbl", "end")
    fig.text((1.5, 16.5), "NSAS PANEL", "lbl", "start")
    fig.text((-27, 63), "DOWN", "lbl", "middle")
    fig.line((-27, 53), (-27, 58.6), "ctrs")
    fig.arrow((-27, 60), (0, 1), "arrowm")
    return fig.svg("Stack angle adapter hanging a base on an NSAS panel", 560, 360)


# ── page ────────────────────────────────────────────────────────────────

def nsas_css():
    """Reuse the NSAS sheet styles, with the NABS labels."""
    text = NSAS_SHEET.read_text(encoding="utf-8")
    css = re.search(r"<style>\n/\* Layout.*?</style>", text, re.S).group(0)
    css = css.replace('"NSAS  /  ENGINEERING SYSTEMS"', '"NSAS  /  NABS  /  ENGINEERING SYSTEMS"')
    css = css.replace('"SYSTEM / 001"', '"SYSTEM / 002"')
    css = css.replace('"NSAS / SECTION"', '"NABS / SECTION"')
    return css + "\n<style>.dwg .cut2 { stroke: none; } .pair td.num { white-space: normal; }</style>"


def build(step):
    S = load_solids(step)
    figs = {
        "A": fig_section(S), "B": fig_plan(S), "C": fig_hinge(S), "C2": fig_finger(S),
        "D1": fig_slot_in(S), "D2": fig_runner(S), "E": fig_joiner(S), "F": fig_adapter(S),
    }
    page = PAGE
    for k, v in figs.items():
        page = page.replace("{{FIG_" + k + "}}", v)
    head = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<title>NABS Spec Sheet</title>'
            '<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700'
            '&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&family=Noto+Sans+JP:wght@700;900'
            '&family=Noto+Serif+JP:wght@700;900&display=swap">\n')
    OUT.write_text(head + nsas_css() + "\n</head><body>\n" + page + "\n</body></html>\n", encoding="utf-8")
    print("wrote", OUT)


PAGE = (HERE / "page.html").read_text(encoding="utf-8")

if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "D:/OneDrive/Stay Home Geek 3d Design/angleslot system.step")
