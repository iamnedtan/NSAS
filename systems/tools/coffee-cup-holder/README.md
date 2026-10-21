# Coffee cup holder

Holds one mini cup of freeze-dried instant coffee on an NSAS panel. Each brand gets its own variant, because the cup sizes differ. Only the cup body is measured; the lid is ignored.

The holder is an open ring whose bore follows the cup's own taper. The cup drops in from the top and wedges in the taper over the full 22 mm ring height. There is no floor: the lower part of the cup hangs out below the ring (13.3 mm for Starbucks, 5.0 mm for Luckin). The ring top sits 1.5 mm under the cup lip. The 8 mm back plate carries one row of 2 NSAS accessory holes, 20 mm apart, so the holder hangs on two standard keys. The plate is 39 mm wide (4 × 10 − 1), so holders hang side by side on 40 mm centres. The brand name is engraved 0.6 mm deep in the top face of the back plate, at most 30 mm wide and 3.5 mm tall, reading from the front (DejaVu Sans Bold).

The bore is line-to-line with the cup (`FIT = 0`). Because the cup seats on its taper, the fit sets the height: every 0.1 mm of radial `FIT` drops the cup about 1.1 mm (Starbucks) or 1.2 mm (Luckin). If a print holds the cup too high (lip gap over 2 mm), raise `FIT` a little and rebuild.

Print standing on its base, as exported. No supports are needed.

## Variants

| Variant | Files | Cup diameter, top / bottom | Slant length | Cup height | Bore diameter, base / top | Holder size | Label |
|---|---|---|---|---|---|---|---|
| `starbucks` | `cup_holder_starbucks.step`, `.stl` | 30.9 / 24.0 | 37.0 | 36.84 | 26.50 / 30.62 | 39 × 40.6 × 22 | STARBUCKS |
| `luckin` | `cup_holder_luckin.step`, `.stl` | 24.7 / 20.0 | 28.6 | 28.50 | 20.83 / 24.45 | 39 × 34.5 × 22 | LUCKIN |

Cup values: diameter just below the lip, bottom diameter, and the length from the bottom to under the lip measured along the slanted side. The cup height (ground to under the lip) is derived from them. All in mm.

## Source

`src/cup_holder.py`. Add a variant to `VARIANTS` (its `label` is the engraved text) and an export function for it. The label font is read from `LABEL_FONT`, a system font path; change it if that file is missing. Tunable values at the top of the file: `HOLDER_H`, `LIP_GAP`, `FIT`, `WALL`, `LABEL_W`, `LABEL_DEPTH`, `NSAS_COLS` (2 to 4) and `NSAS_SPACING`.

`src/cup_holder_mockup.py` builds `mockup/`: each holder with its cup seated in it, whole and cut in half. For checking only, not for printing.

Rebuild from `src/` (cadgen 0.7.25, Python 3.13):

```
uvx --no-config --python 3.13 --from cadgen==0.7.25 python -I cup_holder.py
uvx --no-config --python 3.13 --from cadgen==0.7.25 python -I cup_holder_mockup.py
```
