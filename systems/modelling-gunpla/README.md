# Modelling / Gunpla

NSAS accessories for plastic model (gunpla) tools. Both parts hang on any NSAS panel with standard keys.

These are copies taken on 2026-10-21 from [RunnerCollector](https://github.com/iamnedtan/RunnerCollector), where the designs started as part of the desk setup and where the originals stay. The two copies are not kept in sync.

## Nipper holder (`nipper-holder/`)

`nipper holder - NSAS.solidcraft` (SolidCraft source), `.step`, `.stl`. Holds a pair of nippers. 3 mm NSAS back plate with accessory holes on a 2.5 mm bottom land. RunnerCollector source: `nsas holders/`, last changed in f9b0ef2 (2026-10-20).

## Sanding block (`sanding-block/`)

`sanding_block.step`, `.stl`, source `src/sanding_block.py`. Box for sanding sticks, 68.4 × 82.7 × 34 mm, open at one end with a 45° cut. Its 5 mm floor carries 24 NSAS accessory holes (6 × 4), so it hangs on a panel open end up. It was sized to fit under the tray of the RunnerCollector mini box.

The script was extracted from RunnerCollector `mini/src/mini_under_bins.py` (commit 193ac88), where it is built together with the other under-tray bins. The size that came from the mini box is fixed here (`BLOCK_X`, `BLOCK_Y`, `BLOCK_H`). Its export matches RunnerCollector's `mini_under_sanding_block.step`: same volume, area, bounding box and 112 faces, and no difference in a boolean comparison.

Rebuild from `src/` (cadgen 0.7.25, Python 3.13):

```
uvx --no-config --python 3.13 --from cadgen==0.7.25 python -I sanding_block.py
```

Print both as exported.
