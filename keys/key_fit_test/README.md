# NSAS key fit test (accessory leg, spec v0.12 baseline)

Source: `src/key_fit_test.py` (cadgen / build123d). Run `python src/key_fit_test.py` from this folder's `src`.
All variant values are `Key(...)` entries in `VARIANTS`; baseline values are the v0.12 constants at the top.
Spec sheet is **not** changed until the results are in.

Keys print as exported: lying on a flat side, no supports. Variant name is debossed 0.4 mm into the top flat
side at the panel-leg root (no effect on fit). Test block prints back face down; one 5.00 hole per key,
10 C-C, rising 45°, 6.00 deep, Ø3.5 hang hole under each, name debossed on the front.

| Variant | Accessory leg (upper/lower faces) | Other |
|---|---|---|
| V0 | 4.90 root → 5.10 tip | control, v0.12 |
| P1 | 5.05 parallel | |
| P2 | 5.10 parallel | |
| P3 | 5.15 parallel | |
| F1 | 5.08 root → 4.95 tip | flipped taper |
| B1 | P1 | two barbs per face, 0.10 high, steep faces at 2.5 and 4.5 from the panel face, 0.8 ramp toward the tip |
| B2 | P1 | as B1, 0.15 high |
| R1 | P1 | Ø0.60 root relief (0.3 deep) |
| L1 | P1 | panel leg tip 4.90 (was 5.00) |

## Rounds (one plate each, V0 in every round)

| Round | Plate | Keys |
|---|---|---|
| A: parallel width | `STL/plate_round_A.stl` | V0, P1, P2, P3 |
| B: lock features | `STL/plate_round_B.stl` | V0, P1, F1, B1, B2 |
| C: relief / panel balance | `STL/plate_round_C.stl` | V0, P1, R1, L1 |

`STL/plate_all.stl` has all 9 keys and the 9-hole `test_block.stl`.

## Score sheet

Measured hole size (calipers / gauge pin): ______ × ______ mm. Material: ______

| Variant | Insert 1–5 | 200 g hold | 500 g hold | Play | Pull-out (g) | After 5 cycles | After 24 h | Panel: slides in / holds / lift-tilt out |
|---|---|---|---|---|---|---|---|---|
| V0 | | | | | | | | |
| P1 | | | | | | | | |
| P2 | | | | | | | | |
| P3 | | | | | | | | |
| F1 | | | | | | | | |
| B1 | | | | | | | | |
| B2 | | | | | | | | |
| R1 | | | | | | | | |
| L1 | | | | | | | | |
