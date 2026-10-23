# IKEA UPPDATERA and VARIERA - NSAS slot in holder

Work in progress. A side profile from a Fusion sketch, extruded 70 mm. Only the largest region of the sketch is solid; the smaller enclosed regions are notches cut through the full 70 mm.

Profile (XY plane, sketch origin at 0, 0; extruded along +Z):

- Base 10 mm below Y = 0, from X = 5 to the back face.
- Front ledge on Y = 0, 15 mm deep (X = 5 to 20). A notch 8 × 3 mm sits in the ledge, its back on X = 20.
- From X = 20 a wall leans back 5° from vertical (95° to the ledge) up to Y = 102.
- A lip 8 mm thick, parallel to the wall, hangs 10 mm below Y = 102. Its inner face is 3 mm in front of the wall top.
- Notches at the slot mouth: a 1 mm strip on top (Y = 102 to 103, up to 5 mm behind the wall top), and a wedge behind the wall whose back face opens 10° from the wall, from the wall top down to Y ≈ 74.3.

The back face (X = 45) and top face (Y = 118) are not dimensioned in the sketch. They were read off the screenshot; set `RIGHT_X` and `TOP_Y` to the real values.

| File | Size |
|---|---|
| `IKEA UPPDATERA and VARIERA - NSAS slot in holder.step`, `.stl` | 40 × 128 × 70 |

## Source

`src/slot_in_holder.py`. All sketch dimensions are named values at the top of the file.

Rebuild from `src/` (cadgen 0.7.25, Python 3.13):

```
uvx --no-config --python 3.13 --from cadgen==0.7.25 python -I slot_in_holder.py
```
