# IKEA UPPDATERA and VARIERA - NSAS slot in holder

Work in progress. Holds an IKEA UPPDATERA or VARIERA 24 × 17 cm box (10 cm tall): the box's back wall leans on the holder, its bottom edge on the ledge and its rim up in the slot behind the lip. A test print of the first version fits.

Mounting: the flat back face (130.5 × 69 mm) goes against the NSAS panel, with standard keys in the top and bottom rows of holes. It fits current panels and older plates with sockets every second row. Print it with the profile flat on the bed, as tested; no supports are needed.

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
- Fillets on the inner corners: base notch (1 mm), wedge tip (0.5 mm), lip root (0.8 mm), pockets (1 mm).
- Lead-ins for the box: a 1.5 mm chamfer on the lip's inner bottom edge, a 1 mm round on the ledge's front edge.
- Width 69 mm (7 × 10 − 1), so holders sit side by side on the NSAS 10 mm column pitch.

NSAS accessory holes, in the back face:

- 14 holes: 2 columns 40 mm apart (centred), 7 rows one row pitch (18.536 mm) apart, mouth centres Y = 104.46 (10 mm under the top face), 85.93, 67.39, 48.86, 30.32, 11.79 and −6.75.
- Rows 1, 3, 5, 7 (every second row) meet sockets on current panels (socket on every row) and on older plates (socket every second row). Rows 2, 4, 6 are extra, for the test print; drop them with `NSAS_ROWS = 4`, `NSAS_ROW_STEP = 2`.
- The box hangs in front, so its weight tries to pull the top of the holder off the panel. Key the top and bottom rows (111.2 mm apart).
- The base is 12.5 mm deep instead of the sketch's 10 mm, so the bottom row keeps 2.2 mm of material under it.
- Each hole is 5 mm square, rises 45° going in, and goes 8 mm deep, through the back plate. Behind it, it opens into a pocket; where no pocket is behind (the top 1 mm of the top row), it ends flat, 2 mm under the top face.
- Printed profile-down (Z = 0 on the bed), each hole is a tunnel bridged on top. The key's tapered faces meet the hole walls that print vertically.
- The bridge is a 30° gable (`NSAS_ROOF_ANGLE`), 1.44 mm high at the ridge, instead of a flat roof, so a sagging bridge (ABS) does not close the hole. It is over a flat side of the key, which has 0.2 mm clearance anyway, so the press fit is unchanged. Keep Z = 0 on the bed, or the gable ends up on the floor of the hole.
- `NSAS_ROWS`, `NSAS_ROW_STEP` and `NSAS_COL_STEPS` set the layout.

| File | Size |
|---|---|
| `IKEA UPPDATERA and VARIERA - NSAS slot in holder.step`, `.stl` | 40 × 130.5 × 69 |

## Source

`src/slot_in_holder.py`. All sketch dimensions are named values at the top of the file.

Rebuild from `src/` (cadgen 0.7.25, Python 3.13):

```
uvx --no-config --python 3.13 --from cadgen==0.7.25 python -I slot_in_holder.py
```
