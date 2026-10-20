---
name: nsas
description: Ned Slotted Angle System (NSAS) — the user's own pegboard-style mounting grid of 45° downward-angled 5 mm square sockets with optional angled grooves between rows, used with a square key (one straight 45° bar with a 1 mm stop, snug split-prong leg into the panel (4.6 → 5.0 mm), expanding split-prong leg into the accessory (5.0 root → 5.3 mm oversize tip on the upper/lower faces, crush ribs on one side face), side faces flat and flush) so accessories gravity-lock. Use whenever the user says "NSAS", "use NSAS", "add NSAS", "Ned Slotted Angle System", or asks to add their slotted/angled socket grid to any panel, lid, wall or accessory in any CAD design (SolidCraft, cadgen/text-to-cad, or other).
---

# Ned Slotted Angle System (NSAS)

When the user says "use NSAS" (or "add NSAS to …"), they mean: put this socket-and-groove grid on the named surface, sized to fill it, following the spec exactly. Accessories meant to hang on an NSAS panel get matching angled holes on the same grid.

The full spec, with derivations and the reference-model notes, is in [spec.md](spec.md). Read it before modelling. The rules below are the working summary.

## Core rules

**Socket**
- 5.0 × 5.0 mm square section, angled **45° downward into the face**. When the panel hangs vertically, each socket descends as it goes in.
- On the face it shows 7.07 mm tall (5 × √2).
- **Functional depth 10.0 mm perpendicular. Modelled depth 11.0 mm perpendicular** (functional + 1 mm, so the key never bottoms out). Rule: modelled = functional + 1 mm.
- Flat floor parallel to the face.
- Mouth lead-in: 0.5 mm × 45° chamfer on the side edges, small 22.5° bevel on the lip.
- The panel must be at least modelled depth + skin thick (reference: 11 mm raised panel on a 1 mm skin). If the surface is thinner, add a local raised panel, or use a shallower face with a customised key, or ask the user.

**Grid**
- Column pitch 10.0 mm (5 mm socket, 5 mm wall).
- Row rule: measured vertically, the top wall of row k to the bottom wall of row k+2 is **30.0 mm** (two interleaved 30 mm sets). For adjacent rows this gives:
  - row pitch **18.536 mm** (= 15 + 2.5√2)
  - gap, top wall of row k to bottom wall of row k+1: **11.464 mm**
  - outer to outer across rows k and k+1: **25.607 mm**
- **Not a fixed size:** as many columns and rows as fit the available area. Centre the grid in both directions so opposite margins are equal. No staggering between rows.
- Outer-wall span of n columns: (n − 1) × 10 + 5 mm.

**Groove (optional)**
- Main purpose: hollow out material and, at the same time, increase strength for FDM printing.
- Ask the user if the groove is required. If the area is small and does not need it (for example a small accessory panel, or a single row with no gap), skip it without asking and tell the user it was skipped.
- When used: one groove in every gap between adjacent socket rows, centred vertically in the gap (4.25 mm land above and below).
- 2.1 mm thick perpendicular to its walls (2.97 mm on the face), 45° downward parallel to the sockets, 8.0 mm deep perpendicular. This leaves a 3.0 mm wall to each socket and 4.0 mm behind the groove floor on a 12 mm panel.
- **Length = exactly the outer-wall span of the socket grid**, from the outer wall of the leftmost socket to the outer wall of the rightmost. Square ends aligned with those walls.

**Key ("stick")**
- Connects the accessory interface to the panel sockets.
- Shape: one straight square bar on the 45° socket axis, crossed by a vertical stop plate 1.0 mm thick (perpendicular), 4.6 mm wide, 15.0 mm tall, ends cut at 45°. The stop rests flat on the panel face and sets the insertion depth.
- Panel leg: 10.0 mm perpendicular from the stop. Accessory leg: 5.0 mm perpendicular from the stop, on the same axis.
- **Panel leg: snug fit, not a press fit** (v0.10). This keeps accessories quick to move and replace. 4.6 × 4.6 mm at the root (0.2 mm clearance per side). The upper and lower faces widen to 5.0 mm at the tip (line-to-line). A 1.0 mm slot splits it into two prongs from the tip to 3.0 mm (perpendicular) from the panel face; the solid part keeps the bending strength. Two crush ribs (0.6 wide, 0.45 high = socket − 4.6 + 0.05 crush) sit on the same flat side as the accessory ribs. 1.0 mm chamfer on the upper tip edge.
- **All crush ribs taper:** height drops 0.15 mm (`rib_taper`) from the root end to the tip end of each rib.
- **Flat sides:** the two side faces (vertical, parallel to the bar axis) are flat and flush along the whole key: panel leg, stop and accessory leg all 4.6 mm wide, one plane per side. The key prints lying on one flat side.
- **Accessory leg: expanding press fit** (v0.9; the plain 4.8→5.0 taper proved loose). Only the upper and lower faces (at 45° to the panel face) taper, linearly over the full length, from 5.0 mm at the root (line-to-line with the 5.0 mm hole) to an oversize 5.3 mm at the tip. A 1.0 mm slot along the axis splits the leg into two prongs, from the tip to 0.5 mm (perpendicular) in front of the accessory back face, through both flat sides. The prongs squeeze together in the hole and spring back against its walls. A 0.6 mm lead-in cuts both prong tip corners. Across the flat sides the leg stays 4.6 mm, except two crush ribs (one per prong, 0.6 mm wide, 0.55 mm high = hole − 4.6 + 0.15 crush) on **one** side face only, ending 1.0 mm (along the slope) short of the tip. Keep the slot wider than tip − hole. Keep the accessory hole at 5.0 mm; the fit is set by the key only.
- **Print the key** lying on the side face without ribs: ribs on top, slot walls vertical, each prong flexes within its layers.
- Reference model: `nsas holders/NSAS key - accessories.solidcraft` (parameters `key_root`, `key_bulge`, `prong_gap`, `prong_root`, `lead_in`, `rib_crush`, `rib_h`, `rib_w`, `rib_lead`, `acc_hole`, `rib_taper`, `panel_socket`, `panel_bulge`, `panel_prong_gap`, `panel_prong_root`, `panel_rib_crush`, `panel_rib_h`, `panel_tip_chamfer`). Slots, ribs, lead-ins and the panel tip chamfer are boxes tilted 45° (or the lead-in angles) with parameter expressions and cut or joined by body name, so nothing depends on picked edges.
- Customisable: on a slotted face shallower than normal, shorten the panel leg to that face's functional depth and keep the 1 mm relief.

**Accessories**
- Holes go in the accessory's back face (the flat face that rests on the panel). Grid: 10 mm horizontal, 18.536 mm vertical. Reference: 2 holes, 40 mm apart.
- **Direction: the hole RISES 45° going into the accessory** (from its back face: 1 mm up per 1 mm in). It is on the same line as the panel socket but runs the other way, because the key is one straight bar: panel leg in and down, accessory leg out and up. **Never copy the socket's "downward into the face" onto the accessory.**
- 5.0 × 5.0 mm square (7.07 mm tall on the face). Depth 6.0 mm perpendicular (leg 5 + 1 relief). Flat floor parallel to the back face. Blind, unless the wall is thinner than the depth.
- The floor ends 6 mm higher than the mouth. Keep top-of-face to top-of-upper-mouth ≥ depth + skin (8 mm). Keep ≥ 2 mm skin behind every floor.
- Accessory width for side-by-side hanging: n × 10 mm − clearance (1.0 mm total suggested).
- SolidCraft method that works: sketch the 5 × 7.07 mm mouth rectangle on the back-face plane, sweep-cut it (orientation parallel) along a 45° line going in and up, then a rectangular feature pattern with parameter spacings.

## Making it parametric

Expose at least: functional depth (10), relief (1), socket size (5), key accessory-leg root and tip widths (5.0, 5.3), prong slot width and root land (1.0, 0.5), tip lead-in (0.6), rib crush, width and tip gap (0.15, 0.6, 1.0), rib taper (0.15), panel-leg tip width, slot root land, rib crush and tip chamfer (5.0, 3.0, 0.05, 1.0), key stop thickness (1.0), column pitch (10), the row rule distance (30), groove thickness (2.1) and depth (8), and the panel area or margins. Derive the counts, row pitch and groove length from those, not as fixed numbers. In SolidCraft, avoid sketch planes whose origin is an expression, and avoid edges picked by fixed points (both break on resize). Also avoid sketch chamfers held by point-to-corner distances: the solver can flip a chamfer point past the corner on a large parameter change. Prefer primitives or extrudes driven by parameters, with patterns or mirrors for repetition.

## Before finishing

- Check: socket depth, row pitch, the k→k+2 = 30 mm rule, groove length = outer socket span (if grooves are used), grid centring, and the key sizes (panel leg 4.6 mm root to 5.0 mm tip × 10 mm, slot, ribs, 1 mm tip chamfer; accessory leg 4.6 mm flat sides, 5.0 mm root to 5.3 mm tip on the upper/lower faces, × 5 mm, prong slot present, ribs on one side only, one solid body; stop 1 mm; flat sides one face each apart from the ribs), measured from the model.
- Accessory holes: confirm from the model that each hole floor is higher than its mouth (rises going in), the depth is 6 mm, and no floor breaks into a cavity or the top face.
- Keep full precision in CAD; round only displayed values. Square sizes are measured across the 45° axis; pitches and spacings are centre to centre.
- Suggest a fit check before a full accessory: one key plus a small block with one 5.0 mm hole.
- Tell the user the resulting row and column counts, the margins, and whether grooves were included or skipped.

## Open points (ask if they matter for the design)

- Purpose and profile of the wider groove along the top edge seen in the reference cover.
- Minimum margin around the grid (reference: about 2.5–3 mm horizontally).

## Source

Derived from the user's top cover in `E:\Dev\RunnerCollector Ned\reference\gunpla desk vacuum box.step`. The spec was written on 2026-10-18 (v0.7, 2026-10-19: accessory hole direction fixed; v0.8, 2026-10-19: key flat flush sides, taper on upper/lower faces only; v0.9, 2026-10-20: expanding split-prong accessory leg with crush ribs; v0.10, 2026-10-20: snug split-prong panel leg, tapered ribs, panel tip chamfer); [spec.md](spec.md) is the only text copy (edit it there), and the illustrated sheet is `reference/NSAS Spec Sheet.html`.
