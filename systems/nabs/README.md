# NABS — Ned Angle Base System

A modular base plate system built on [NSAS](../../README.md). Each base is a flat plate with two rows of NSAS 45° sockets. Slot-in parts stand in the sockets on plain square legs. Bases pin together on filament hinges, fold up into walls, join side to side, and slot into NSAS panels.

The [**illustrated spec sheet**](https://iamnedtan.github.io/NSAS/systems/nabs/spec/NABS%20Spec%20Sheet.html) is the reference: views cut from the Fusion model, every value, the history and revisions. Source: [`spec/NABS Spec Sheet.html`](<spec/NABS Spec Sheet.html>), built by [`spec/src/build_sheet.py`](spec/src/build_sheet.py) from `spec/src/page.html` and the Fusion export. The text spec is [spec.md](spec.md) (draft v0.1). Both reference the NSAS spec (v0.13) for the socket and the pitches.

| Key values | | |
|---|---|---|
| Socket | 5.0 square, 45°, through a 10.0 plate | as NSAS, but through |
| Columns | 10.0 pitch, *n* columns, length *n* × 10 | *n* is a parameter |
| Rows | 2 per base, 37.071 C–C (2 × 18.536) | 30.0 between mouths: the original 30 mm rule |
| Base | 64.142 body, 84.142 with hinge fingers, 10.0 thick | pinned flat at 74.142 pitch |
| Hinge pin | 1.75 mm filament in Ø2.5 | flat or folded 90° |
| Slot-in leg | 4.6 square (loose fit 4.4), 9.5 deep | plain, no stop or prongs |

## Parts

All in [`parts/`](parts/), as STEP and STL. The Fusion model is the source.

| Part | What it does |
|---|---|
| NABS base | The base plate, 10 columns (100 mm) |
| NABS base - M3 mount | Base with counterbored M3 holes in the middle channel, to screw it to a surface |
| NABS standard slot in | Template for slot-in parts: a 4.6 mm fin on two legs |
| NABS runner slot in | L-shaped holder: tape or cable-tie a gunpla runner along the arm. It also holds a floor base and a wall base at 90° |
| NABS runner slot in - loose fit | Same, 4.4 mm legs |
| NABS side joiner | Locks two bases side to side, in the middle channel |
| NABS stack angle adapter | Lets a base slot into an NSAS panel like an accessory |

## History

**2026-01-31: the first NSAS part.** Ned ([iamnedtan](https://github.com/iamnedtan)) was remodelling a plastic modelling trolley and wanted a quick way to reconfigure and move items around, similar to a pegboard. For that project he designed this base in Fusion, the first part to use the NSAS socket: 5 mm square, angled 45° so that a part's weight pushes it deeper. The Fusion file was called "angleslot system". It had the base, its vertical (folded) mode, the standard slot in, the runner slot in with a loose-fit version, the M3 mount version, the side joiner and the stack angle adapter.

**The 30 mm rule.** The base's two rows were set 30 mm apart, measured from the inner edge of one socket mouth to the inner edge of the other. This became the NSAS row rule. On NSAS panels 30 mm between rows proved too far, so two sets of rows were interleaved, giving the 18.536 mm NSAS row pitch. The 30 mm rule is still in the NSAS spec, as the spacing from a row to the row two away. The NABS base keeps the original spacing: its rows are NSAS rows *k* and *k* + 2.

**NSAS grows from it.** Later in the same trolley project NSAS grew in its own direction: wall panels, the key with its stop plate and split-prong legs, blind sockets, grooves and tileable margins (see the History section of the [NSAS README](../../README.md) and the spec's revision notes). The NABS base kept its January form: through sockets and plain-legged slot-ins.

**2026-10-23: spec written.** The Fusion model was exported, the parts were split into one file each, and the system got its own name and spec: NABS, Ned Angle Base System, draft v0.1. The spec records the design as modelled, and states as design rules what the designer confirmed (parametric column count, pocket split, triangle marks, M3 hole placement, standard leg fit).

**Next: display garages.** Bases as floors and walls, with side walls, stacked levels and wall-hung garages on NSAS panels, for plastic model display. See spec section 9.
