# IKEA UPPDATERA and VARIERA - NSAS slot in holder

Work in progress. Holds an IKEA UPPDATERA or VARIERA 24 × 17 cm box (10 cm tall): the box's back wall leans on the holder, its bottom edge on the ledge and its rim up in the slot behind the lip. A test print of the first version fits.

Mounting: the flat back face (130.5 × 69 mm) goes against the NSAS panel, with four standard keys in its two rows of holes. It fits current panels and older plates with sockets every second row. Print it with the profile flat on the bed, as tested; no supports are needed.

A side profile from a Fusion sketch, extruded 69 mm. Only the largest region of the sketch is solid; the smaller enclosed regions are notches cut through the full width.

Profile (XY plane, sketch origin at 0, 0; extruded along +Z):

- Base 12.5 mm below Y = 0 (sketch: 10 mm), from X = 5 to the back face.
- Front ledge on Y = 0, 15 mm deep (X = 5 to 20). A notch 8 × 3 mm sits in the ledge, its back on X = 20.
- From X = 20 a wall leans back 5° from vertical (95° to the ledge) up to Y = 102.
- A lip 8 mm thick, parallel to the wall, hangs 10 mm below Y = 102. Its inner face is 3 mm in front of the wall top.
- Notches at the slot mouth: a 1 mm strip on top (Y = 102 to 103, up to 5 mm behind the wall top), and a wedge behind the wall whose back face opens 10° from the wall, from the wall top down to Y ≈ 74.3.

The back face (X = 45) and top face (Y = 118) are not dimensioned in the sketch. They were read off the screenshot; set `RIGHT_X` and `TOP_Y` to the real values.

Optimised after the test print (about 48 % less material than the solid profile):

- Two pockets through the full width: one behind the wall and wedge, one in the top block over the slot. They leave 3 mm walls (`SHELL`), a 3 mm floor and an 8 mm back plate (`BACK_T`) that the NSAS accessory holes pass through. The pockets suit printing with the profile on the bed.
- Six windows through the back plate into the main pocket, in the band between the two hole columns (Z = 21.4 to 49, 3 mm clear of the holes). Each is 12 mm wide along Y with a flat bottom and a 45° pointed top, so printed profile-down none needs a bridge. 7 mm ribs between them (`WINDOW_W`, `WINDOW_RIB`).
- Four windows of the same shape through the leaning wall (the face the box rests on) into the main pocket, cut square to the wall. They run up the wall from 3 mm above its foot to 3 mm under the wedge, with 6.7 mm ribs between them, and leave 8 mm of solid wall at each end (`FRONT_WINDOW_MARGIN`). The box's back wall rests on the ribs and end bands.
- Both sets of windows are split in two along Z (`WINDOW_SETS = 2`), with a 6 mm band between the halves: 12 windows in the back plate, 8 in the leaning wall. The bands lie in XY planes and stiffen the walls in the profile plane. A web across the pocket would be stiffer still, but printed profile-down it would be a floor over open air.
- Fillets on the inner corners: base notch (1 mm), lip root (0.8 mm), pockets (1 mm).
- A 0.8 mm 45° chamfer round the outline of both profile faces (`END_CHAMFER`), the bottom and top as printed: no elephant's foot on the bed, softer ends. It is under 1 mm so it fits the 1 mm strip at the slot mouth. Pocket, window and hole outlines stay square.
- Lead-ins for the box: a 1.5 mm chamfer on the lip's inner bottom edge, a 1 mm round on the ledge's front edge.
- Width 69 mm (7 × 10 − 1), so holders sit side by side on the NSAS 10 mm column pitch.

NSAS accessory holes, in the back face:

- 4 holes: 2 columns 40 mm apart (centred), 2 rows with mouth centres Y = 67.39 and 30.32. They are rows 3 and 5 of a row grid one row pitch (18.536 mm) apart from the top (row 1 at Y = 104.46, 10 mm under the top face), so 37.07 mm (two pitches) apart.
- Two pitches apart, the rows meet sockets on current panels (socket on every row) and on older plates (socket every second row).
- The base is 12.5 mm deep instead of the sketch's 10 mm, so the bottom row keeps 2.2 mm of material under it.
- Each hole is 5 mm square, rises 45° going in, and goes 8 mm deep, through the back plate. Behind it, it opens into a pocket; where no pocket is behind (the top 1 mm of the top row), it ends flat, 2 mm under the top face.
- Printed profile-down (Z = 0 on the bed), each hole is a tunnel bridged on top. The key's tapered faces meet the hole walls that print vertically.
- The bridge is a 30° gable (`NSAS_ROOF_ANGLE`), 1.44 mm high at the ridge, instead of a flat roof, so a sagging bridge (ABS) does not close the hole. It is over a flat side of the key, which has 0.2 mm clearance anyway, so the press fit is unchanged. Keep Z = 0 on the bed, or the gable ends up on the floor of the hole.
- `NSAS_KEEP_ROWS` picks the rows from the grid (`NSAS_ROWS`, `NSAS_ROW_STEP`); `NSAS_COL_STEPS` sets the columns.

## Variants

| Variant | Files | Size | Notes |
|---|---|---|---|
| `flat` | `IKEA UPPDATERA and VARIERA - NSAS slot in holder - flat.step`, `.stl` | 40 × 130.5 × 69 | Mounts straight on an NSAS panel. Everything above. |
| `offset` | `IKEA UPPDATERA and VARIERA - NSAS slot in holder - offset.step`, `.stl` | 40 × 130.5 × 69 | Work in progress: hangs on a NABS base standing vertical, with four standard NSAS keys. See below. |

### Offset variant

Mounts with thick-stop keys on a NABS base (`systems/nabs`) standing vertical (wall mode, hinge edge B down), so the base's two socket rows, 37.071 mm apart, act like an NSAS panel's rows 3 and 5. Differences from `flat`:

- In place of the main pocket, two smaller pockets through the full width, split round the hole tunnels: one below the lower row's tunnel, one between the two tunnels. They keep 2 mm walls round each tunnel (`SLEEVE`), so the keys keep full hole walls, 2 mm behind the stop recesses (`RECESS_SKIN`), and 3 mm (`SHELL`) to the leaning wall.
- Pointed-top windows into those pockets, in the band between the hole columns (Z = 23.3 to 48.7, 3 mm clear of the recesses and hole roofs): three through the X = 37 face and three through the leaning wall, 12 mm wide or narrower, 2 mm in from the pocket edges. No bridges printed profile-down. The offset variant is 95.1 cm³ (133.1 solid).
- An 8 mm rectangle (`OFFSET_W`) is cut from the back, from the bottom up to Y = 99.43, with a 1 mm round in its inner corner. The holder's mounting face is then X = 37, and the block above is an overhang whose underside sits 0.5 mm (`OFFSET_CLEAR`) over the top of the NABS base (its edge-A hinge fingers, at Y = 98.93) when the keys join them; the keys carry the load. `offset_top()` works that height out from the top hole row and the base's row and finger sizes.
- It takes the thick-stop NSAS key (`keys/NSAS key - accessories thick`, 3 mm stop). Round each hole mouth, the X = 37 face has a 3 mm deep recess (`KEY_STOP`) shaped like the stop plate: 4.6 wide and 12 tall, centred on the hole axis, with its ends at 45° parallel to the hole, plus 0.5 mm all round (`STOP_CLEAR`). The stops sit in the recesses, so the holder sits flush on the base. The recess roof (+Z, the top as printed) slopes up at 45° from the recess floor to the face, so it prints without a flat overhang; the opening on the face is 3 mm taller than the stop on that side.
- The NSAS holes run on along their 45° line, through the leaning wall into the slot, and end 0.5 mm past where they break out (`HOLE_EXIT`), clear of the lip. Their mouths on the X = 37 face are at Y = 75.39 and 38.32, the same as the base's socket mouths.

`mockup/slot_in_holder_offset_on_NABS_base.step` shows it on a 10-column NABS base, joined by four `keys/NSAS key - accessories thick` keys, standing Z-up. The keys' stops sit in the recesses and the holder is flush on the base; the base's back face is 2 mm behind the overhang's back (base 10 mm thick, offset 8 mm), and the overhang sits 0.5 mm over its top fingers. For checking only, not for printing. Build it with `src/slot_in_holder_mockup.py`.

## Source

`src/slot_in_holder.py`. `VARIANTS` sets what differs between `flat` and `offset`; both are built on each run. All sketch dimensions are named values at the top of the file.

Rebuild from `src/` (cadgen 0.7.25, Python 3.13):

```
uvx --no-config --python 3.13 --from cadgen==0.7.25 python -I slot_in_holder.py
uvx --no-config --python 3.13 --from cadgen==0.7.25 python -I slot_in_holder_mockup.py
```
