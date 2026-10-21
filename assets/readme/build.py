"""Build the README art from the spec sheet, in the spec sheet's style.

GitHub strips CSS from README files, so the sheet's title block, section
numbers and drawings are rendered as standalone SVG files here:

- title-block.svg: sheet header (system strip, title block, revision data).
- footer.svg: sheet footer strip.
- n01.svg ... n10.svg: section number badges (壱 ... 拾).
- fig-*.svg: drawings copied from the spec sheet, with the sheet's drawing
  styles inlined in light-theme colours.

Revision and date are read from the sheet's title block. Run after changing
the spec sheet:  python assets/readme/build.py
"""
from __future__ import annotations

import html
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHEET = HERE.parent.parent / "spec" / "NSAS Spec Sheet.html"

# Spec sheet light-theme colours
PAPER = "#e7e9e7"
SHEET_BG = "#ffffff"
INK = "#20262b"
MUTED = "#626d75"
RULE = "#c4cbd0"
DIM = "#a82c26"
HATCH = "#929ba1"
KEYFILL = "#e5ebef"
PANEL_EDGE = "#aab3b9"
ARMOR_RED = "#d82f25"
ARMOR_GOLD = "#c99a3d"
GUNMETAL = "#30383e"

# Web fonts do not load in SVG images, so each stack ends in system fonts.
DISPLAY = "'Barlow Condensed', 'Arial Narrow', 'Roboto Condensed', 'Helvetica Neue', Arial, sans-serif"
BODY = "'IBM Plex Sans', 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'IBM Plex Mono', 'Cascadia Mono', Consolas, 'Courier New', monospace"
SERIF_JP = "'Noto Serif JP', 'Yu Mincho', 'Hiragino Mincho ProN', 'MS Mincho', serif"
SANS_JP = "'Noto Sans JP', 'Yu Gothic', 'Hiragino Sans', Meiryo, sans-serif"

NUMERALS = "壱弐参肆伍陸漆捌玖拾"

# Drawing styles from the sheet, with var() resolved to the light theme.
DWG_CSS = f"""
.part {{ fill: none; stroke: {INK}; stroke-width: 1.4px; vector-effect: non-scaling-stroke; stroke-linejoin: round; }}
.cut, .cut2 {{ stroke: none; }}
.hatchl {{ stroke: {HATCH}; stroke-width: 0.9px; vector-effect: non-scaling-stroke; }}
.brk {{ stroke: {INK}; stroke-width: 0.8px; stroke-dasharray: 10 3 2 3; vector-effect: non-scaling-stroke; }}
.func {{ stroke: {DIM}; stroke-width: 1.2px; stroke-dasharray: 5 3; vector-effect: non-scaling-stroke; }}
.ctr {{ stroke: {MUTED}; stroke-width: 0.8px; stroke-dasharray: 12 3 2 3; vector-effect: non-scaling-stroke; }}
.ctrs {{ stroke: {MUTED}; stroke-width: 1.4px; vector-effect: non-scaling-stroke; }}
.dim, .ext, .dimarc {{ stroke: {DIM}; stroke-width: 0.9px; fill: none; vector-effect: non-scaling-stroke; }}
.ext {{ stroke-width: 0.6px; }}
.lead {{ stroke: {MUTED}; stroke-width: 0.8px; vector-effect: non-scaling-stroke; }}
.dot {{ fill: {MUTED}; }}
.arrow {{ fill: {DIM}; stroke: none; }}
.arrowm {{ fill: {MUTED}; stroke: none; }}
text {{ font-family: {MONO}; }}
.dimt {{ fill: {DIM}; }}
.note {{ fill: {INK}; }}
.lbl {{ fill: {MUTED}; letter-spacing: 0.08em; }}
.big {{ fill: {INK}; font-weight: 500; }}
.sheetfill {{ fill: {SHEET_BG}; stroke: {INK}; stroke-width: 1.4px; vector-effect: non-scaling-stroke; }}
.holef {{ fill: {INK}; stroke: none; }}
.groovef {{ fill: {HATCH}; stroke: {INK}; stroke-width: 0.8px; vector-effect: non-scaling-stroke; }}
.key, .keysec {{ fill: {KEYFILL}; stroke: {DIM}; stroke-width: 1.4px; vector-effect: non-scaling-stroke; stroke-linejoin: round; }}
.holeline {{ fill: none; stroke: {INK}; stroke-width: 1px; stroke-dasharray: 4 3; vector-effect: non-scaling-stroke; }}
"""

# README figures: output name, the drawing's aria-label in the sheet, caption strip text.
FIGURES = [
    ("fig-key.svg", "Key seated in a panel socket and an accessory wall", "FIG / KEY SEATED · SECTION"),
    ("fig-grid.svg", "Face view of a 5 by 3 grid", "FIG / GRID · FACE VIEW"),
    ("fig-socket.svg", "Section through one socket", "FIG / SOCKET · SECTION"),
]
FIG_W = 720  # rendered drawing width in px
# Side room for labels: system mono fonts run wider than IBM Plex Mono, so
# text near the drawing edge would be clipped at the sheet's viewBox.
FIG_SIDE = 90


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def title_block(revision: str, date: str) -> str:
    w = 1080
    strip_h = 26
    tb_y = strip_h + 3
    row_h = 58
    tb_h = 2 * row_h
    h = tb_y + tb_h + 3
    name_w = 470
    cell_w = (w - name_w) / 3
    cells = [
        ("Document", "NSAS-SPEC"), ("Revision", revision), ("Date", date),
        ("Units", "mm, degrees"), ("Views", "to scale, per view"), ("Process", "FDM"),
    ]
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
        f'aria-label="NSAS spec sheet title block: Ned Slotted Angle System, {esc(revision)}, {esc(date)}">',
        f'<rect width="{w}" height="{h}" fill="{SHEET_BG}"/>',
        # Diagonal panel tint on the right of the title block
        f'<polygon points="{w * 0.68},{tb_y} {w},{tb_y} {w},{tb_y + tb_h} {w * 0.68 - 40},{tb_y + tb_h}" fill="#828c93" fill-opacity="0.07"/>',
        # System strip
        f'<rect width="{w}" height="{strip_h}" fill="{GUNMETAL}"/>',
        f'<rect y="{strip_h}" width="{w}" height="3" fill="{ARMOR_RED}"/>',
        f'<text x="28" y="17" fill="#f4f5f5" font-family="{esc(MONO)}" font-size="10" font-weight="500" letter-spacing="1.9">NSAS  /  ENGINEERING SYSTEMS</text>',
        # Name cell
        f'<rect x="0" y="{tb_y}" width="{name_w}" height="{tb_h}" fill="#879198" fill-opacity="0.08"/>',
        f'<rect x="0" y="{tb_y}" width="5" height="{tb_h}" fill="{ARMOR_RED}"/>',
        f'<text x="25" y="{tb_y + 22}" fill="{MUTED}" font-family="{esc(MONO)}" font-size="10" letter-spacing="1.5">SPECIFICATION</text>',
        f'<text x="24" y="{tb_y + 60}" fill="{INK}" font-family="{esc(DISPLAY)}" font-size="40" font-weight="700" '
        f'textLength="{name_w - 50}" lengthAdjust="spacingAndGlyphs">NED SLOTTED ANGLE SYSTEM</text>',
        f'<text x="25" y="{tb_y + 82}" fill="{MUTED}" font-family="{esc(BODY)}" font-size="13">45° gravity-lock socket grid for FDM-printed panels and accessories</text>',
        f'<text x="25" y="{tb_y + 103}" fill="{ARMOR_GOLD}" font-family="{esc(MONO)}" font-size="10" font-weight="500" letter-spacing="1.7">SYSTEM / 001</text>',
    ]
    for i, (k, v) in enumerate(cells):
        col, row = i % 3, i // 3
        x = name_w + col * cell_w
        y = tb_y + row * row_h
        out.append(f'<text x="{x + 16:.1f}" y="{y + 22}" fill="{MUTED}" font-family="{esc(MONO)}" font-size="10" letter-spacing="1.5">{esc(k.upper())}</text>')
        out.append(f'<text x="{x + 16:.1f}" y="{y + 42}" fill="{INK}" font-family="{esc(MONO)}" font-size="13">{esc(v)}</text>')
    # Cell rules
    for col in range(3):
        x = name_w + col * cell_w
        out.append(f'<line x1="{x:.1f}" y1="{tb_y}" x2="{x:.1f}" y2="{tb_y + tb_h}" stroke="{RULE}"/>')
    out.append(f'<line x1="{name_w}" y1="{tb_y + row_h}" x2="{w}" y2="{tb_y + row_h}" stroke="{RULE}"/>')
    out.append(f'<rect y="{h - 3}" width="{w}" height="3" fill="{GUNMETAL}"/>')
    out.append(f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" fill="none" stroke="{PANEL_EDGE}"/>')
    out.append("</svg>")
    return "\n".join(out)


def footer() -> str:
    w, h = 1080, 34
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Technical design, FDM fabrication">',
        f'<rect width="{w}" height="{h}" fill="{SHEET_BG}"/>',
        f'<rect width="{w}" height="3" fill="{GUNMETAL}"/>',
        f'<rect width="54" height="3" fill="{ARMOR_RED}"/>',
        f'<text x="28" y="22" fill="{MUTED}" font-family="{esc(MONO)}" font-size="9" font-weight="500" letter-spacing="1.35">TECHNICAL DESIGN • FDM FABRICATION</text>',
        f'<text x="{w - 28}" y="22" text-anchor="end" fill="{MUTED}" font-family="{esc(MONO)}" font-size="9" letter-spacing="1.35">NSAS / ENGINEERING SYSTEMS</text>',
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" fill="none" stroke="{PANEL_EDGE}"/>',
        "</svg>",
    ])


def badge(n: int) -> str:
    """Section number badge: cut-corner plate, kanji numeral, 第 mark."""
    s = 58
    i = n - 1
    # Colour cycle of the sheet's sections: red, gunmetal, gold.
    bg, fg, mark = [(ARMOR_RED, "#f8f8f5", "#e7b75b"), ("#252b30", "#f8f8f5", "#e7b75b"),
                    (ARMOR_GOLD, INK, "#fffaf0")][i % 3]
    pts = f"0,0 {s * 0.78:.1f},0 {s},{s * 0.22:.1f} {s},{s} {s * 0.18:.1f},{s} 0,{s * 0.82:.1f}"
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 {s} {s}" role="img" aria-label="Section {n}">',
        f'<polygon points="{pts}" fill="{bg}"/>',
        f'<text x="{s / 2}" y="{s / 2 + 11}" text-anchor="middle" fill="{fg}" font-family="{esc(SERIF_JP)}" font-size="31" font-weight="900">{NUMERALS[i]}</text>',
        f'<text x="4" y="12" fill="{mark}" font-family="{esc(SANS_JP)}" font-size="9" font-weight="800">第</text>',
        f'<text x="{s - 4}" y="{s - 4}" text-anchor="end" fill="#c8cdd0" font-family="{esc(MONO)}" font-size="5" letter-spacing="0.2">NSAS / SECTION</text>',
        "</svg>",
    ])


def figure(src: str, label: str, caption: str) -> str:
    m = re.search(r'<svg class="dwg" viewBox="([^"]+)"[^>]*aria-label="' + re.escape(label) + r'"[^>]*>(.*?)</svg>', src, re.S)
    if not m:
        raise SystemExit(f"figure not found in spec sheet: {label}")
    vx, vy, vw, vh = (float(v) for v in m.group(1).split())
    body = m.group(2)
    draw_h = FIG_W * vh / vw
    pad, strip = 14, 22
    w = FIG_W + 2 * (pad + FIG_SIDE)
    h = strip + draw_h + 2 * pad
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}" role="img" aria-label="{esc(label)}">',
        f'<rect width="{w:.0f}" height="{h:.0f}" fill="{SHEET_BG}"/>',
        f'<rect width="{w:.0f}" height="3" fill="{GUNMETAL}"/>',
        f'<text x="{w - 10:.0f}" y="16" text-anchor="end" fill="{MUTED}" fill-opacity="0.75" font-family="{esc(MONO)}" font-size="9" letter-spacing="1.1">{esc(caption)}</text>',
        f'<rect x="0.5" y="0.5" width="{w - 1:.0f}" height="{h - 1:.0f}" fill="none" stroke="{PANEL_EDGE}"/>',
        f'<svg x="{pad + FIG_SIDE}" y="{strip + pad}" width="{FIG_W}" height="{draw_h:.1f}" viewBox="{m.group(1)}" overflow="visible">',
        f"<style>{DWG_CSS}</style>",
        body.strip(),
        "</svg>",
        "</svg>",
    ])


def main():
    src = SHEET.read_text(encoding="utf-8")
    rev = re.search(r'<span class="k">Revision</span><span class="v">([^<]+)</span>', src).group(1)
    date = re.search(r'<span class="k">Date</span><span class="v">([^<]+)</span>', src).group(1)
    files = {"title-block.svg": title_block(rev, date), "footer.svg": footer()}
    for n in range(1, len(NUMERALS) + 1):
        files[f"n{n:02d}.svg"] = badge(n)
    for name, label, caption in FIGURES:
        files[name] = figure(src, label, caption)
    for name, text in files.items():
        (HERE / name).write_text(text + "\n", encoding="utf-8", newline="\n")
        print("wrote", name)


if __name__ == "__main__":
    main()
