# Slotted panel system — spec sheet

Draft v0.13, 2026-10-21 (v0.13, print-tested: accessory leg takes the panel leg profile, taper 4.8 → 5.1 mm, square tip with no lead-in or root relief, leg 5.8 mm with a 0.2 mm tip gap to the hole floor, prong slot end 5.0 mm from the panel slot end along the bar, panel tip chamfer removed, 0.5 mm round on the edges between the flat sides except the stop-to-leg inside corners, thick-stop key variant, tileable-panel margins 2.5 / 5.732 mm, groove trade-off and top-edge groove purpose, open points closed; v0.12: accessory leg taper reduced to 4.9 → 5.1 mm, Ø1.0 mm root reliefs tangent to the stop, prong slot ends 1.0 mm from the stop; v0.11: stop height reduced to 12.0 mm, all crush ribs removed; v0.10: panel leg snug fit with its own taper 4.6 → 5.0, prong slot and crush ribs, 1 mm panel tip chamfer, all crush ribs tapered; v0.9: accessory leg split into two flexing prongs with an oversize tip, tip lead-in chamfer, crush ribs on one flat side; v0.2: groove made optional; v0.3: key can be customised; v0.4: key slips into the panel and press-fits into the accessory; v0.5: key shape fixed with a 1 mm stop, groove values corrected; v0.6: conventions, groove wall, key datum, fit check; v0.7: accessory hole direction (rises into the accessory), depth, floor and placement rules, direction check; v0.8: key side faces flat and flush, accessory-leg taper on the upper and lower faces only). Written from the user's design intent plus measurements of the top cover in `gunpla desk vacuum box.step`. Where the reference model and the intent differ, the intent wins and the difference is noted.

## 1. What it is

A pegboard-style mounting surface. A grid of square sockets is cut into a panel, every socket angled 45° downward into the material. Accessories (trays, tool holders) carry matching angled holes. A separate square key ("stick") passes through the accessory hole into a panel socket. The key is one straight bar, so the accessory hole lies on the same 45° line as the socket but, seen from the accessory's own back face, it **rises** as it goes in (section 7).

Because each socket slopes down as it goes into the panel, the accessory's weight pushes the key deeper. It cannot be pulled straight out; it is removed by lifting and tilting. No clips or screws are needed.

Optionally, a thin angled groove runs between each pair of socket rows. Its main purpose is to hollow out material and, at the same time, increase strength for FDM printing.

## 2. Orientation and terms

- **Face:** the panel surface the accessories hang on, used vertically.
- **Perpendicular:** measured at right angles to the face, into the panel.
- **Vertical:** measured up and down along the face.
- **Along the slope (∥):** measured along the 45° socket axis.
- **Cross-section:** square sizes (socket, key) are measured across the 45° axis, at right angles to it.
- **C–C:** centre to centre. All pitches and hole spacings are C–C.
- A 45° socket that is 5 mm thick perpendicular to its own walls shows on the face, and in any vertical measurement, as 5 × √2 = **7.07 mm** tall.

## 3. Socket (pocket)

| Item | Value | Notes |
|---|---|---|
| Cross-section | 5.0 × 5.0 mm square | width horizontal, thickness perpendicular to the sloped walls |
| Angle | 45° downward into the face | gravity lock |
| Height on the face (vertical) | 7.07 mm | 5 × √2 |
| **Functional depth** | **10.0 mm perpendicular** | the depth the key needs to engage (14.14 mm along the slope) |
| **Modelled depth** | **11.0 mm perpendicular** | functional depth + 1.0 mm relief so the key never bottoms out (15.56 mm along the slope) |
| Floor | flat, parallel to the face | |
| Mouth lead-in | 0.5 mm × 45° chamfer on the side edges; small 22.5° bevel on the lip | as modelled; helps the key find the socket |

Rule: **modelled depth = functional depth + 1 mm**. The panel must be at least modelled depth + skin thick (reference: 11 mm panel on a 1 mm skin).

## 4. Grid layout

The grid is not fixed. It fills whatever area is available.

### 4.1 Columns

| Item | Value |
|---|---|
| Column pitch (horizontal, centre to centre) | 10.0 mm |
| Wall between adjacent sockets | 5.0 mm |
| Outer-wall span of *n* columns | (n − 1) × 10 + 5 mm |
| Number of columns | as many as fit the available width |
| Placement | centred in the width, equal left and right margins |
| Side margin, tileable panel | 2.5 mm each side (half a wall), so panels placed side by side keep the 10.0 mm pitch; panel width = n × 10 mm |

*Reference model:* 18 columns, span 175.0 mm in a 180.5 mm panel. The grid sits 0.25 mm off centre (margins 3.0 / 2.5 mm). The spec calls for centring.

### 4.2 Rows: the 30 mm rule

Design rule: measured vertically, the top wall of a socket to the bottom wall of the socket two rows away is **30.0 mm**.

(Originally rows were spaced 30 mm apart, which proved too far. Two such sets were interleaved, giving the spacing below.)

Let h = vertical socket height = 7.07 mm, and p = row pitch. From row *k* to row *k + 2*: 2p − h = 30, so:

| Item (rows *k* and *k + 1*, vertical) | Formula | Value |
|---|---|---|
| **Row pitch** (centre to centre) | (30 + h) / 2 = 15 + 2.5√2 | **18.536 mm** |
| **Gap** (top wall of row *k* → bottom wall of row *k + 1*) | (30 − h) / 2 = 15 − 2.5√2 | **11.464 mm** |
| **Outer to outer** (bottom wall of row *k* → top wall of row *k + 1*) | (30 + 3h) / 2 | **25.607 mm** |
| Rows *k* → *k + 2*, top wall → bottom wall | 2p − h | **30.000 mm** ✓ |
| Row pitch perpendicular to the socket walls | p × sin 45° | 13.107 mm |
| Solid between adjacent socket tunnels, perpendicular | 13.107 − 5 | 8.107 mm |

*Reference model:* pitch 18.53 mm, gap 11.46 mm, matching the rule.

- Number of rows: as many as fit the available height.
- Placement: centred in the height.
- **Tileable panels** (combined side by side or stacked): margins 2.5 mm left and right and **5.732 mm** top and bottom (= gap / 2 = (30 − h) / 4 = 7.5 − 1.25√2). Two margins then make exactly one wall (5.0 mm) or one row gap (11.464 mm), so column pitch, row pitch and the 30 mm rule carry on across the joint. Panel size: n × 10.0 mm wide, r × 18.536 mm tall. The row gap at a stacked joint is split across two panels, so it gets no groove.
- Every row has the same column positions (no staggering).

## 5. Groove (slot between rows)

The groove is **optional**.

- **Purpose:** mainly to hollow out material and, at the same time, increase strength for FDM printing. Less infill is needed, but the extra walls can make the print take longer.
- **When to include:** ask the user if the groove is required.
- **When to skip:** if the area is small and does not need it (for example a small accessory panel, or a grid with only one row, which has no gap), skip the groove and tell the user it was skipped.

When the groove is used, it follows this table:

| Item | Value | Notes |
|---|---|---|
| Position | one groove in every gap between adjacent socket rows | |
| Vertical placement | centred in the gap | 4.25 mm land above and below |
| Thickness | 2.1 mm perpendicular to its walls (2.97 mm vertical on the face) | |
| Angle | 45° downward, parallel to the sockets | |
| Depth | 8.0 mm perpendicular | |
| Wall to each socket | 3.0 mm perpendicular to the walls | (8.107 − 2.1) / 2; constant along the groove because groove and sockets are parallel |
| Material behind the groove floor | 4.0 mm on a 12 mm panel | 12 − 8 |
| **Length** | **exactly the outer-wall span of the socket grid**: from the outer wall of the leftmost socket to the outer wall of the rightmost | (n − 1) × 10 + 5 mm |
| Ends | square, aligned with the outermost socket walls | |

*Reference model:* the groove is 175.5 mm long (centred) against a 175.0 mm socket span (shifted 0.25 mm), so one end overshoots by 0.5 mm. The spec says the lengths match.

*Also in the reference:* a wider groove along the top edge of the panel (optional). Same purpose: it reinforces the panel for FDM printing and reduces infill, at the cost of a possibly longer print. Take its profile from the reference cover; it is not dimensioned in this spec.

## 6. Key ("stick")

The key connects the accessory interface (section 7) to the panel sockets.

**Shape** (from the reference model, with the stop thinned to 1 mm): one straight 4.6 mm square bar on the 45° socket axis, crossed by a thin vertical stop plate.

**Flat sides:** the two side faces of the key (the vertical faces parallel to the bar axis, left and right when the key is in use) are flat and flush along the whole key: panel leg, stop and accessory leg form one plane on each side, 4.6 mm apart. Only the other pair of faces, the upper and lower faces of the bar (at 45° to the panel face), changes size between the legs and carries the taper. The key then prints lying on one flat side with no overhang step.

- **Panel leg:** the bar from the stop into the panel socket, 10.0 mm perpendicular (the functional depth).
- **Accessory leg:** the bar from the stop into the accessory hole, 5.8 mm perpendicular (v0.13): the 6.0 mm hole depth minus a 0.2 mm tip gap. It continues on the same 45° axis.
- **Stop:** a vertical plate 1.0 mm thick (perpendicular), 4.6 mm wide (flush with the flat sides) and 12.0 mm tall (v0.11, reduced from 15.0), centred on the bar. Its ends are cut at 45°, parallel to the bar. It rests flat on the panel face and sets the insertion depth. It is taller than the 7.07 mm socket mouth, so it cannot enter the socket. The bar crosses the face 6.51 mm tall, so the stop reaches 2.75 mm past the bar above and below.

- **Panel leg:** snug fit (v0.10), still **not a press fit**, so accessories stay quick to move and replace. Across the upper and lower faces the leg widens from 4.6 mm at the root to 5.0 mm at the tip (line-to-line with the socket). A slot splits the outer part into two prongs, like the accessory leg, but the slot stops 3.0 mm (perpendicular) from the panel face, so the leg keeps its full section where the bending load is highest. The tip is square, with no chamfer (v0.13).
- **Accessory leg:** expanding press fit (v0.9), with the same profile as the panel leg (v0.13). A slot along the bar axis splits the leg into two prongs, one at the upper face and one at the lower face. Across the upper and lower faces the leg widens in a straight line from 4.8 mm at the root to an oversize 5.1 mm at the tip (v0.13; v0.12 was 4.9 → 5.1 with root reliefs and a lead-in), so the prongs squeeze together in the 5.0 mm hole and spring back against its walls. The tip is square: no lead-in chamfer and no root relief. The slot runs back toward the stop until its end is 5.0 mm from the panel slot end, measured along the bar, so it ends 0.46 mm (perpendicular) inside the stop. The tip stops 0.2 mm short of the hole floor: zero gap fitted best in test, and 0.2 mm keeps a slightly shallow printed hole from stopping the key before the stop seats. Across the flat sides the leg stays 4.6 mm, flush with the panel leg and stop. No crush ribs on either leg (removed in v0.11): both legs keep 0.2 mm side clearance per side in the 5.0 mm socket and hole. The key stays in the accessory when the accessory is moved.
- **Edge rounds (v0.13):** every edge that runs across the key between the two flat sides has a 0.5 mm round: both leg tips, the slot mouths, the slot ends (full rounds) and the stop ends. The four inside corners where the stop meets the legs stay sharp, so the stop seats flat.
- **Printing:** print the key lying on one flat side. The slot walls are then vertical, so each prong is made of full layers and flexes within the layer plane.
- **Customisable:** if a slotted face is shallower than normal, customise the key to match. Shorten the panel leg so that it engages only the functional depth of that face, and keep the 1 mm relief to the socket floor.

| Item | Value | Notes |
|---|---|---|
| Section, panel leg, at the root (stop end) | 4.6 × 4.6 mm square | 0.2 mm clearance per side in a 5.0 mm socket |
| Section, panel leg, at the tip | 4.6 (flat sides) × 5.0 mm (upper/lower faces) | `panel_bulge`; line-to-line, snug, no interference; taper linear over the leg |
| Panel prong slot | 1.0 mm wide across the axis, from the tip to 3.0 mm (perpendicular) from the panel face, through both flat sides | `panel_prong_gap`, `panel_prong_root` |
| Panel leg tip | square, no chamfer (v0.13) | 0.5 mm edge rounds |
| Width across the flat sides | 4.6 mm, whole key | panel leg, stop and accessory leg flush; one flat face per side; no crush ribs (v0.11) |
| Section, accessory leg, at the root (stop end) | 4.6 (flat sides) × 4.8 mm (upper/lower faces) | `key_root`; 0.1 mm clearance per side in the 5.0 mm hole |
| Section, accessory leg, at the tip (prongs relaxed) | 4.6 × 5.1 mm | `key_bulge`; 0.05 mm interference per side, taken up by the prongs flexing |
| Taper on the accessory leg | linear, 4.8 → 5.1 mm (widens toward the tip; line-to-line at 3.87 mm from the stop, 2/3 of the length), upper and lower faces only | over the full 5.8 mm leg length; the flat sides do not taper |
| Prong slot | 1.0 mm wide across the axis, from the tip to 5.0 mm from the panel slot end measured along the bar (0.46 mm perpendicular inside the stop), through both flat sides | `prong_gap`, `slot_spacing`; `prong_root` is derived (negative = inside the stop); keep `prong_gap` > `key_bulge` − hole size so the prongs never close up |
| Edge rounds | 0.5 mm on every edge between the flat sides (leg tips, slot mouths, slot ends, stop ends); not on the stop-to-leg inside corners | `edge_round` |
| Leg lengths, perpendicular | panel 10.0, accessory 5.8 | measured from the stop faces; accessory = `acc_hole_depth` − `acc_tip_gap` (6.0 − 0.2) |
| Stop | 1.0 thick × 4.6 wide (flush) × 12.0 tall | vertical, ends cut at 45°, flat on the panel face |
| Engagement in the panel | functional depth (10 mm on a standard face), measured from the panel face where the stop rests | the 1 mm relief keeps it off the floor |

**Variant: thick stop (v0.13).** For accessories that must stand farther off the panel face, for example to clear obstructions such as the lip of a cover design. The stop is 3.0 mm thick instead of 1.0 mm; the extra 2.0 mm grows toward the panel side. Everything from the stop's accessory face outward is the same as the standard key: accessory leg 5.8 mm, taper, slot end 0.46 mm inside the stop from its accessory face. The panel leg still engages 10.0 mm from the panel face. Results: the accessory back face sits 3.0 mm from the panel face (1.0 mm standard), the slot ends are 7.83 mm apart along the bar (5.54 mm perpendicular), overall length 18.8 mm perpendicular (16.8 standard). Same 0.5 mm edge rounds. Model: `keys/NSAS key - accessories thick.solidcraft`, with `stop_t` = 3 mm and `prong_root` computed with the standard 1 mm stop. Panels and accessory holes do not change.

*Reference model:* `stick (5mm)` has a 2 mm stop; this spec uses 1 mm. The stick overlaps the tray body by about 115 mm³, which matches the press fit on the accessory side. In a new model, do not copy that overlap; use the tapered accessory leg above in a 5.0 mm hole instead.

## 7. Accessory interface

The holes go in the accessory's **back face**: the flat face that rests against the panel face (vertical in use). The key's stop sits between the two faces.

**Direction (the common mistake).** The key is one straight bar. Its panel leg goes into the panel and **down**; so its accessory leg points out of the panel and **up**. The accessory hole must follow the accessory leg: measured from the accessory's back face, it goes in and **rises 45°** (1 mm up for every 1 mm in). It is the same 45° line as the socket, run the other way. **Never copy the socket's "45° downward into the face" onto the accessory.** A downward hole cannot take a key that is already in the panel.

Gravity lock with this direction: the accessory is pressed onto the rising leg and its weight pulls it down and back along the bar, toward the panel.

| Item | Value | Notes |
|---|---|---|
| Cross-section | 5.0 × 5.0 mm square | 0.1 mm per side over the key's 4.8 mm accessory leg root; the fit is set by the key taper |
| Direction | 45°, **rising** into the accessory from its back face | opposite sense to the panel socket, same line |
| Height on the back face (vertical) | 7.07 mm | 5 × √2 |
| Depth | 6.0 mm perpendicular to the back face | accessory leg 5.8 + 0.2 mm tip gap (8.49 mm along the slope) |
| Floor | flat, parallel to the back face | sits 6.0 mm higher than the mouth |
| Blind or through | blind when the wall is thicker than depth + skin; through only when the wall is thinner than the depth | a through hole must still give the leg its full 5.8 mm |

**Placement.**
- Horizontal hole spacing, centre to centre: a multiple of the 10 mm column pitch. Reference: 2 holes at 40 mm. An accessory n columns wide is n × 10 − clearance wide (1.0 mm total suggested), so accessories hang side by side.
- Vertical hole spacing, centre to centre: a multiple of the 18.536 mm row pitch.
- Because the hole rises, its floor ends **depth higher** than its mouth. The gap from the top of the back face to the top of the upper mouth must be at least depth + skin (6 + 2 = 8 mm suggested).
- Check the wall behind every floor (cavities, slopes, fillets inside the accessory): keep at least 2 mm skin.

Check before finishing: from the back face, each hole goes in and up; a key placed in a panel socket can slide straight into it.

## 8. Open points

None at present. Closed in v0.13: the wide top-edge groove purpose (section 5) and the grid margins for tileable panels (section 4.2).
