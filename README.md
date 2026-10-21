# NSAS - Ned Slotted Angle System

A pegboard-style mounting grid for 3D-printed panels and accessories. Panels carry a grid of 5 mm square sockets angled 45° downward, with optional angled grooves between rows. A square key joins panel and accessory: one straight 45° bar with a 1 mm stop, a snug split-prong leg into the panel and an expanding split-prong leg into the accessory. Accessories gravity-lock and lift off without tools.

Current spec: **v0.13** (2026-10-21).

## Contents

| Path | What |
|---|---|
| [spec/NSAS Spec Sheet.html](<spec/NSAS Spec Sheet.html>) | Illustrated spec sheet (open in a browser) |
| [.claude/skills/nsas/spec.md](.claude/skills/nsas/spec.md) | Full text spec, the only text copy |
| [.claude/skills/nsas/SKILL.md](.claude/skills/nsas/SKILL.md) | Claude Code skill: working summary used when adding NSAS to a design |
| `keys/NSAS key - accessories.*` | Standard key (1 mm stop): SolidCraft source, STEP, STL |
| `keys/NSAS key - accessories thick.*` | Thick-stop key (3 mm stop), for accessories that must stand off the panel |
| [keys/key_fit_test/](keys/key_fit_test/) | Accessory-leg fit test: variant keys, test block and print plates |
| [systems/](systems/) | Created systems: accessory sets built on NSAS, one folder per hobby or use (first: [modelling-gunpla](systems/modelling-gunpla/)) |

## Printing the keys

Print keys as exported, lying on a flat side, without supports. See the [fit test README](keys/key_fit_test/README.md) for tuning the accessory-leg fit to your printer.

## Using the skill

The `nsas` skill lets Claude Code add the grid to any panel or accessory ("use NSAS on the lid"). To use it outside this repo, link the skill folder into your user skills:

```powershell
New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\nsas" -Target "E:\GIT\NSAS\.claude\skills\nsas"
```

## History

Ned ([iamnedtan](https://github.com/iamnedtan)) invented NSAS in 2026 as part of a project to remodel a plastic modelling trolley. The aim is a quick way to reconfigure and move items around, similar to a pegboard system.

The design work was first done alongside [RunnerCollector](https://github.com/iamnedtan/RunnerCollector), the first project to use NSAS. On 2026-10-21 the NSAS files moved to this repo with their git history, so the early commits here carry RunnerCollector commit messages. RunnerCollector keeps its own NSAS-based parts (the boxes and the socket broach that repairs early box prints). The nipper holder and the sanding block were copied from it into [systems/modelling-gunpla](systems/modelling-gunpla/).

## License

[CC BY-SA 4.0](LICENSE)
