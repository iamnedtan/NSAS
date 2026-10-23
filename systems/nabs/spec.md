# NABS — Ned Angle Base System — spec sheet

Draft v0.1, 2026-10-23. First written spec, measured from the Fusion export `angleslot system.step` (2026-10-23) and the designer's answers. The base itself was designed on 2026-01-31; the history is in [README.md](README.md).

NABS is a separate system that builds on NSAS. Where this spec says "NSAS", it means the [NSAS spec](../../.claude/skills/nsas/spec.md), v0.13 (2026-10-21). NABS takes the NSAS socket (5.0 mm square, 45°) and the NSAS pitches (10.0 mm columns, 18.536 mm rows). It does not take the NSAS key: NABS slot-ins have plain legs (section 6).

The illustrated version is [spec/NABS Spec Sheet.html](<spec/NABS Spec Sheet.html>); keep the two in step.

Values marked *as modelled* are read off the Fusion model and are not yet design rules. Values with no mark are design rules.

## 1. What it is

A modular base plate for displays and storage, first made for plastic models. Each base is a flat plate with two rows of 45° sockets on its top face. Slot-in parts (uprights, runner holders, adapters) stand in the sockets on plain square legs.

Bases connect in three ways:

- **Hinge edges:** both long edges carry interleaving hinge fingers. Two bases pinned with a length of 1.75 mm filament lie flat side by side, or one folds up 90° to make a wall (vertical mode).
- **Sides:** the short edges have no fingers. Bases placed side to side are locked by a side joiner in the middle channel, and the socket rows carry on across the joint.
- **NSAS panels:** a stack angle adapter lets a base slot into an NSAS panel like an accessory.

Planned: a display garage made of bases (section 9).

## 2. Orientation and terms

- **Floor mode:** the base lies flat, top face (the face with socket mouths) up. All values in this spec are given in floor mode unless stated.
- **Vertical mode:** the base folded 90° about its hinge to stand as a wall.
- **Column:** one 10.0 mm slice of the base along its length. Each column holds one socket per row, one middle-channel hole and one hinge finger per hinge edge.
- **Length** (*L*): measured along the rows, side to side. *L* = *n* × 10.0 mm for *n* columns.
- **Across:** measured at right angles to the rows, from hinge edge to hinge edge.
- **Sides:** the two short edges, at the ends of the rows. No fingers.
- **Hinge edges:** the two long edges, with fingers. **Hinge edge A** has the wide fingers (4.95 mm), **hinge edge B** the narrow fingers (4.75 mm). Every socket descends toward edge B.
- **Body face:** the flat face of the plate at a hinge edge, from which the fingers stick out.
- **Perpendicular, along the slope, cross-section, C–C:** as in NSAS section 2.
- Across positions are given from the body face at edge A (0.000), toward edge B. Heights are given from the bottom face (0.0).

## 3. Base plate

| Item | Value | Notes |
|---|---|---|
| Thickness | 10.0 mm | |
| Body across (body face A → body face B) | 64.142 mm | 37.071 + 27.071 |
| Overall across, with fingers | 84.142 mm | fingers 10.0 mm past each body face |
| Length | *n* × 10.0 mm | *n* = number of columns, a parameter in the Fusion model |
| Reference model | *n* = 10, 100 × 84.142 × 10 mm | |
| Top edges | 1.0 × 45° chamfer on the body faces | *as modelled* |

The number of columns is a parameter. Every feature that repeats per column (sockets, triangle marks, middle-channel holes, hinge fingers) follows *n*. The top pockets and the underside hollows split by the rule in section 5.

## 4. Sockets and rows

### 4.1 Socket

| Item | Value | Notes |
|---|---|---|
| Cross-section | 5.0 × 5.0 mm square | as NSAS |
| Angle | 45°, descending toward hinge edge B | as NSAS |
| Width on the top face, across | 7.071 mm | 5 × √2 |
| Depth | **through** the 10.0 mm plate (14.14 mm along the slope) | NSAS sockets are blind; NABS keeps them through: no floor to print, debris falls out |
| Mouth lead-in | ≈ 0.7 mm × 45° chamfer on the side edges; 22.5° bevel, 1.0 mm wide on the top face, on the edge-B lip | *as modelled*; same idea as NSAS |

### 4.2 Columns

| Item | Value | Notes |
|---|---|---|
| Column pitch, C–C | 10.0 mm | as NSAS |
| Socket centre from the side | 5.0 mm, then every 10.0 mm | side margin 2.5 mm, the NSAS tileable margin; bases side to side keep the 10.0 mm pitch |
| Wall between sockets | 5.0 mm | |

### 4.3 Rows

Each base has two rows. They are NSAS rows *k* and *k* + 2: two row pitches apart, with no row between them.

| Item | Value | Notes |
|---|---|---|
| Row 1 mouth, across | 10.000 → 17.071 mm | |
| Row 2 mouth, across | 47.071 → 54.142 mm | |
| **Row pitch, C–C** | **37.071 mm** | 2 × 18.536 (NSAS row pitch) |
| Row 1 mouth, edge-B side → row 2 mouth, edge-A side, on the top face | **30.000 mm** | 2 × 18.536 − 7.071: the original NSAS "30 mm rule" (history in the README) |
| Base pitch across, two bases pinned flat | 74.142 mm | 2 × 37.071; the rows carry on at 37.071 across the hinge |

### 4.4 Triangle marks

| Item | Value | Notes |
|---|---|---|
| Shape | equilateral triangle, 4.0 mm side | |
| Depth | 0.6 mm, cut into the top face | |
| Direction | points toward hinge edge B | the way the sockets descend |
| Position, along | between every pair of adjacent sockets (on the column boundaries), so *n* − 1 per row | design rule |
| Position, across | row 1: 4.000 → 7.464 mm; row 2: 43.571 → 47.035 mm | *as modelled* |

The marks have two purposes: they show which way the sockets slope, and they are decoration.

## 5. Middle channel, pockets and hollows

### 5.1 Middle channel

A channel runs the full length of the base between the two rows. It takes the side joiner, the stack angle adapter and the M3 screws.

| Item | Value | Notes |
|---|---|---|
| Across | 33.071 → 41.071 mm (8.0 mm wide) | |
| Floor | 5.0 mm above the bottom face (floor 5.0 mm thick) | channel 5.0 mm deep |
| Top edges | 1.5 × 45° chamfer | from 8.5 mm to the top face |
| Holes | one per column, 8.0 (across, full channel width) × 5.0 mm (along), through the floor | centred on the socket columns; 5.0 mm webs between |

### 5.2 Top pockets

One lightening pocket runs beside each row, along the length: on row 1 between the row and the middle channel, on row 2 between the row and body face B. Their walls follow the 45° socket slope.

**Split rule** (design rule):

- Pockets per row = ⌈*n* / 5⌉: one pocket for up to 5 columns, a new pocket for each further 5 columns or part of 5.
- All pockets in a row are the same length, with a 4.0 mm rib between them and a 2.5 mm end margin at each side.
- Pocket length = (*L* − 5.0 − 4.0 × (*k* − 1)) / *k*, for *k* pockets.
- Examples: *n* = 4: 1 pocket; *n* = 7: 2 pockets (3.5 columns each); *n* = 10: 2 pockets, 45.5 mm each; *n* = 12: 3 pockets, 35.67 mm each (about 4 columns).

Profile: *as modelled* (take it from the STEP). Inner corners are 1.0 mm rounds.

### 5.3 Underside hollows

Each row has a hollow open to the bottom face, on the edge-A side of the socket tunnel. It leaves a 2.0 mm roof (hollow height 8.0 mm) and a 2.0 mm wall to the socket, parallel to the slope. The hollows split with the top pockets (*as modelled*: 2.0 mm rib at *n* = 10). There are also small 1 × 1 mm relief grooves along the bottom face. Profile: *as modelled*.

## 6. Hinge

| Item | Value | Notes |
|---|---|---|
| Finger length, across | 10.0 mm past the body face | both edges |
| Edge A fingers | 4.95 mm wide, at 0 → 4.95 mm in each column, measured from the side | |
| Edge B fingers | 4.75 mm wide, at 5.15 → 9.90 mm in each column | |
| Clearance between interleaved fingers | 0.20 mm and 0.25 mm | |
| Pin hole | Ø2.5 mm, along the full length, 5.0 mm above the bottom face (mid-thickness) | |
| Pin hole position, across | mid-finger: 5.0 mm from the finger tip and from the body face, both edges | so the holes line up when edge-A fingers of one base sit in the edge-B finger gaps of the next |
| Pin | a length of 1.75 mm filament | 0.75 mm diametral clearance in Ø2.5: the hinge turns freely |
| Finger chamfers | 1.0 × 45°: edge A on the top and bottom tip edges, edge B on the top tip edge | *as modelled* |

Uses:

- **Flat:** two bases pinned side by side, at a 74.142 mm base pitch. The socket rows continue across the hinge at 37.071 mm.
- **Folded (vertical mode):** one base turned 90° about the pin stands as a wall, sockets facing inward. With side walls, this makes the floor-and-wall corners of a display garage.

## 7. Sides

The sides are flat, with no fingers. Two bases placed side to side keep the 10.0 mm column pitch (2.5 + 2.5 mm side margins). A side joiner (section 8.4) in the middle channel bridges the joint and locks them.

## 8. Parts

All slot-in legs are plain, with no stop plate, split prongs or taper. The body of the part rests on the base's top face and sets the depth.

### 8.1 Slot-in leg (all slot-ins)

| Item | Value | Notes |
|---|---|---|
| Section | 4.6 × 4.6 mm square | standard; 0.2 mm clearance per side in the 5.0 mm socket |
| Section, loose fit | 4.4 × 4.4 mm | 0.3 mm per side; for tight printers or quicker swapping |
| Angle | 45°, on the socket axis, centred in the socket | |
| Depth | 9.5 mm perpendicular below the top face | ends 0.5 mm above the bottom face |
| Tip | flat, parallel to the top face | |
| Leg spacing between rows | 37.071 mm | one leg per row |

### 8.2 Standard slot in

A template: the reference shape to build other slot-in parts from.

| Item | Value | Notes |
|---|---|---|
| Body | 64.142 long (across) × 4.6 thick × 9.0 mm tall above the top face | spans both rows; ends flush with the body faces |
| Underside relief | 20.0 mm long × 4.0 mm high, across 22.071 → 42.071 mm | *as modelled*; clears the row-1 pocket and the middle channel |
| Legs | 2, one per row, standard 4.6 mm | |

### 8.3 Runner slot in

Holds a gunpla runner, and holds two bases at right angles.

| Item | Value | Notes |
|---|---|---|
| Shape | L: a floor arm and a wall arm, each 73.642 mm long, 4.6 mm thick | |
| Floor arm | 2 legs down into the rows of a floor base | |
| Wall arm | 2 legs sideways into the rows of a folded wall base, 37.071 mm apart | |
| Arm height | 8.0 mm at the edges, 6.7 mm at the bottom of the groove | |
| Runner groove | 90° V-groove along the top of the arm, ≈ 1.6 mm deep | *as modelled* |
| Fixing | lay the runner along the arm, then tape it or cable-tie it round the arm | no tie slots |
| Legs | 4.6 mm standard; loose-fit variant 4.4 mm | 4.6 is the standard |

Second use: with legs in both a floor base and a wall base, it holds the two bases at 90°.

### 8.4 Side joiner

Fusion name: *base to base side joiner*.

| Item | Value | Notes |
|---|---|---|
| Plug | 7.9 (across) × 14.6 (along) × 3.5 mm tall | sits on the channel floor; top 1.5 mm below the top face; 0.1 mm clearance across the 8.0 mm channel |
| Legs | 2, each 7.9 × 4.6 × 5.0 mm, 10.0 mm C–C, straight down | into the channel holes; flush with the bottom face |
| Use | across a side joint: one leg in the last channel hole of one base, one in the first hole of the next | locks bases side to side |

### 8.5 Stack angle adapter

Fusion name: *base to base stack angle adapter*. Lets a base slot into an NSAS panel like an accessory.

| Item | Value | Notes |
|---|---|---|
| Plug | as the side joiner: 7.9 × 14.6 mm, top 1.5 mm below the top face | 2.0 × 45° chamfer on its lower edge-B edge |
| Legs | 2, 4.6 mm square, 10.0 mm C–C (the NSAS column pitch) | through two adjacent channel holes of one base |
| Leg below the base | 45°, descending toward edge B, 9.5 mm perpendicular below the bottom face | into the sockets of one NSAS panel row |

In use, the base's bottom face rests on the NSAS panel face with edge B down. The base's own sockets then also slope down into the base, so parts in them gravity-lock as on NSAS.

### 8.6 Base, M3 mount variant

Screws a base to a desk, shelf or board.

| Item | Value | Notes |
|---|---|---|
| Pad | 15.0 mm long, full channel width, 2.0 mm above the channel floor (top at 7.0 mm) | covers one channel hole |
| Hole | Ø3.0 mm through, Ø6.0 mm counterbore 2.8 mm deep from the pad top | the M3 screw goes in from above |
| Count and position | one per top pocket, centred on the pocket's length | design rule; *n* = 10: 2 holes, 25 mm from each side |

## 9. Display garage (roadmap)

Not yet designed. Planned layouts, built from bases and slot-ins:

- Floor with a back wall: a base with a second base folded up on its hinge.
- Side walls: more folded bases, giving a box-like garage.
- Stacked levels: garages on garages.
- Wall-hung: garages hung on an NSAS panel with stack angle adapters.

## 10. Files

| File | Part |
|---|---|
| `parts/NABS base.step`, `.stl` | Base, *n* = 10 |
| `parts/NABS base - M3 mount.step`, `.stl` | Base with M3 mount |
| `parts/NABS standard slot in.step`, `.stl` | Standard slot in (template) |
| `parts/NABS runner slot in.step`, `.stl` | Runner slot in, 4.6 mm legs |
| `parts/NABS runner slot in - loose fit.step`, `.stl` | Runner slot in, 4.4 mm legs |
| `parts/NABS side joiner.step`, `.stl` | Side joiner |
| `parts/NABS stack angle adapter.step`, `.stl` | Stack angle adapter |

The Fusion model is the source. These files were split from its export, one part each, moved so that the bounding box starts at the origin. Fusion's "base piece in vertical mode" is the same part as the base, turned, so it has no file of its own.

## 11. Open points

- Print orientation and supports for each part are not yet written down.
- The as-modelled profiles (pockets, hollows, relief grooves, mouth lead-in) have not yet been turned into design rules.
