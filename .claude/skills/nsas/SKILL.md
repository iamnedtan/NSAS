---
name: nsas
description: Ned Slotted Angle System (NSAS) — the user's own pegboard-style mounting grid of 45° downward-angled 5 mm square sockets with optional angled grooves between rows, used with a square key (one straight 45° bar with a 1 mm stop, snug split-prong leg into the panel (4.6 → 5.0 mm), expanding split-prong leg into the accessory (4.8 root → 5.1 mm oversize tip on the upper/lower faces, 5.8 mm long, square tip), 0.5 mm edge rounds, no crush ribs, side faces flat and flush) so accessories gravity-lock. Use whenever the user says "NSAS", "use NSAS", "add NSAS", "Ned Slotted Angle System", or asks to add their slotted/angled socket grid to any panel, lid, wall or accessory in any CAD design (SolidCraft, cadgen/text-to-cad, or other).
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
- **Tileable panels** (combined side by side or stacked): margins 2.5 mm left/right and 5.732 mm top/bottom (= (30 − h) / 4), so pitches and the 30 mm rule carry across the joint. Panel = n × 10 mm wide, r × 18.536 mm tall. No groove in the gap at a stacked joint.
- Outer-wall span of n columns: (n − 1) × 10 + 5 mm.

**Groove (optional)**
- Main purpose: hollow out material and, at the same time, increase strength for FDM printing. Less infill, but possibly longer print time. The wide top-edge groove in the reference cover has the same purpose; take its profile from the reference.
- Ask the user if the groove is required. If the area is small and does not need it (for example a small accessory panel, or a single row with no gap), skip it without asking and tell the user it was skipped.
- When used: one groove in every gap between adjacent socket rows, centred vertically in the gap (4.25 mm land above and below).
- 2.1 mm thick perpendicular to its walls (2.97 mm on the face), 45° downward parallel to the sockets, 8.0 mm deep perpendicular. This leaves a 3.0 mm wall to each socket and 4.0 mm behind the groove floor on a 12 mm panel.
- **Length = exactly the outer-wall span of the socket grid**, from the outer wall of the leftmost socket to the outer wall of the rightmost. Square ends aligned with those walls.

**Key ("stick")**
- Connects the accessory interface to the panel sockets.
- Shape: one straight square bar on the 45° socket axis, crossed by a vertical stop plate 1.0 mm thick (perpendicular), 4.6 mm wide, 12.0 mm tall (v0.11), ends cut at 45°. The stop rests flat on the panel face and sets the insertion depth. It reaches 2.75 mm past the bar above and below.
- Panel leg: 10.0 mm perpendicular from the stop. Accessory leg: 5.8 mm perpendicular from the stop (6.0 hole depth − 0.2 mm tip gap, v0.13), on the same axis.
- **Panel leg: snug fit, not a press fit** (v0.10). This keeps accessories quick to move and replace. 4.6 × 4.6 mm at the root (0.2 mm clearance per side). The upper and lower faces widen to 5.0 mm at the tip (line-to-line). A 1.0 mm slot splits it into two prongs from the tip to 3.0 mm (perpendicular) from the panel face; the solid part keeps the bending strength. Square tip, no chamfer (v0.13).
- **No crush ribs** on either leg (removed in v0.11). Both legs keep 0.2 mm side clearance per side across the flat sides.
- **Flat sides:** the two side faces (vertical, parallel to the bar axis) are flat and flush along the whole key: panel leg, stop and accessory leg all 4.6 mm wide, one plane per side. The key prints lying on one flat side.
- **Accessory leg: expanding press fit** (v0.9), same profile as the panel leg (v0.13, print-tested). Only the upper and lower faces (at 45° to the panel face) taper, in a straight line over the full length, from 4.8 mm at the root (0.1 mm clearance per side in the 5.0 mm hole) to an oversize 5.1 mm at the tip. Square tip: no lead-in, no root relief. A 1.0 mm slot along the axis splits the leg into two prongs, through both flat sides, from the tip back to 5.0 mm from the panel slot end measured along the bar (it ends 0.46 mm perpendicular inside the stop). The prongs squeeze together in the hole and spring back against its walls. The tip stops 0.2 mm short of the hole floor. Across the flat sides the leg stays 4.6 mm. Keep the slot wider than tip − hole. Keep the accessory hole at 5.0 mm; the fit is set by the key only.
- **Edge rounds:** 0.5 mm on every edge between the two flat sides (leg tips, slot mouths, slot ends, stop ends). Not on the four stop-to-leg inside corners, so the stop seats flat.
- **Thick-stop variant:** stop 3.0 mm instead of 1.0, grown toward the panel side; the accessory side and panel leg are unchanged, so the accessory back face stands 3.0 mm off the panel (to clear obstructions such as the lip of a cover design). Model: `keys/NSAS key - accessories thick.solidcraft`.
- **Print the key** lying on one flat side: slot walls vertical, each prong flexes within its layers.
- Reference model: `keys/NSAS key - accessories.solidcraft` (v0.13; parameters `key_w`, `key_root`, `key_bulge`, `stop_t`, `stop_h`, `prong_gap`, `slot_spacing`, `prong_root` (derived), `acc_hole_depth`, `acc_tip_gap`, `acc_leg` (derived), `edge_round`, `acc_hole`, `panel_socket`, `panel_bulge`, `panel_prong_gap`, `panel_prong_root`). Slots are boxes tilted 45° with parameter expressions and cut by body name. The edge rounds are one fillet (`Fillet1`) on edges picked by point: after a size change, re-pick its tip edges.
- Customisable: on a slotted face shallower than normal, shorten the panel leg to that face's functional depth and keep the 1 mm relief.

**Accessories**
- Holes go in the accessory's back face (the flat face that rests on the panel). Grid: 10 mm horizontal, 18.536 mm vertical. Reference: 2 holes, 40 mm apart.
- **Direction: the hole RISES 45° going into the accessory** (from its back face: 1 mm up per 1 mm in). It is on the same line as the panel socket but runs the other way, because the key is one straight bar: panel leg in and down, accessory leg out and up. **Never copy the socket's "downward into the face" onto the accessory.**
- 5.0 × 5.0 mm square (7.07 mm tall on the face). Depth 6.0 mm perpendicular (leg 5.8 + 0.2 tip gap). Flat floor parallel to the back face. Blind, unless the wall is thinner than the depth.
- The floor ends 6 mm higher than the mouth. Keep top-of-face to top-of-upper-mouth ≥ depth + skin (8 mm). Keep ≥ 2 mm skin behind every floor.
- Accessory width for side-by-side hanging: n × 10 mm − clearance (1.0 mm total suggested).
- SolidCraft method that works: sketch the 5 × 7.07 mm mouth rectangle on the back-face plane, sweep-cut it (orientation parallel) along a 45° line going in and up, then a rectangular feature pattern with parameter spacings.

## Making it parametric

Expose at least: functional depth (10), relief (1), socket size (5), key accessory-leg root and tip widths (4.8, 5.1), accessory tip gap (0.2), prong slot width and slot spacing (1.0, 5.0), edge round (0.5), panel-leg tip width and slot root land (5.0, 3.0), key stop thickness and height (1.0, 12.0), column pitch (10), the row rule distance (30), groove thickness (2.1) and depth (8), and the panel area or margins. Derive the counts, row pitch and groove length from those, not as fixed numbers. In SolidCraft, avoid sketch planes whose origin is an expression, and avoid edges picked by fixed points (both break on resize). Also avoid sketch chamfers held by point-to-corner distances: the solver can flip a chamfer point past the corner on a large parameter change. Prefer primitives or extrudes driven by parameters, with patterns or mirrors for repetition.

## Before finishing

- Check: socket depth, row pitch, the k→k+2 = 30 mm rule, groove length = outer socket span (if grooves are used), grid centring, and the key sizes (panel leg 4.6 mm root to 5.0 mm tip × 10 mm, slot, square tip; accessory leg 4.6 mm flat sides, 4.8 mm root to 5.1 mm tip on the upper/lower faces, × 5.8 mm, prong slot ends 5.0 mm from the panel slot end along the bar, 0.5 mm edge rounds, sharp stop-to-leg corners, one solid body; stop 1 × 4.6 × 12 mm; no crush ribs; flat sides one face each), measured from the model.
- Accessory holes: confirm from the model that each hole floor is higher than its mouth (rises going in), the depth is 6 mm, and no floor breaks into a cavity or the top face.
- Keep full precision in CAD; round only displayed values. Square sizes are measured across the 45° axis; pitches and spacings are centre to centre.
- Suggest a fit check before a full accessory: one key plus a small block with one 5.0 mm hole.
- Tell the user the resulting row and column counts, the margins, and whether grooves were included or skipped.

## Open points

None at present.

## Source

Derived from the top cover of the user's gunpla desk vacuum box (`reference/gunpla desk vacuum box.step` in the [RunnerCollector](https://github.com/iamnedtan/RunnerCollector) repo). Repository: [iamnedtan/NSAS](https://github.com/iamnedtan/NSAS); model and sheet paths in this skill are relative to its root (local clone: `E:\GIT\NSAS`). The spec was written on 2026-10-18 (v0.7, 2026-10-19: accessory hole direction fixed; v0.8, 2026-10-19: key flat flush sides, taper on upper/lower faces only; v0.9, 2026-10-20: expanding split-prong accessory leg with crush ribs; v0.10, 2026-10-20: snug split-prong panel leg, tapered ribs, panel tip chamfer; v0.11, 2026-10-20: stop height 12 mm, crush ribs removed; v0.12, 2026-10-20: accessory leg 4.9 → 5.1, root reliefs, slot to 1.0 mm from the stop; v0.13, 2026-10-21: accessory leg takes the panel leg profile, 4.8 → 5.1, 5.8 mm long with 0.2 mm tip gap, slot ends 5.0 mm apart along the bar, panel tip chamfer removed, 0.5 mm edge rounds, thick-stop variant, tileable margins 2.5 / 5.732 mm, open points closed); [spec.md](spec.md) is the only text copy (edit it there), and the illustrated sheet is `spec/NSAS Spec Sheet.html`.
