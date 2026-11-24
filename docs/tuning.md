# Tuning reference

The tuning levers live at the top of `tools/generate_headlights.py` (`STAGE_LEVERS`, `FLARE_LEVERS`) and
`tools/generate_masks.py` (mask levers). This page records what each round (Tx) controls, the released values, and
how they were reached, so a future round (new Better Flares release, or a retune) starts from known ground.

**Tuning intent:** comfortable night driving first; in bad daytime conditions (rain, fog, overcast) the road stays
readable; keep Better Flares' realistic mood (no arcade glare). The engine limits how visible a lamp can be in
daylight; that ceiling is accepted.

**Starting point (ADR-0001):** ETS2 MoreVisibility 2.1.0's values, carried over unchanged. Its rounds and build
history are in the ETS2 repo's `docs/tuning.md`. Retune only if ATS playtesting needs it: US truck lamp heights
(conventional W900 / 389 vs high-cab VNL / Cascadia) and wider roads.

## Better Flares v4.9 (1.x)

Source: Headlights.2 7500K LED v4.9.1, one shared `def/vehicle/_common/color.sui` for every truck.

| Round | Lever group | Fields | Stock v4.9.1 7500K | Lever | 1.0.0-dev.1 (= ETS2 2.1.0) | Check in-game |
|---|---|---|---|---|---|---|
| T1 | Intensity | `*_color*` | low `(4.15, 4.675, 6.2)` | low beam `color_mult` 1.3 | low `(5.395, 6.0775, 8.06)`; others stock | Road visible at dusk; no whiteout up close at night |
| T2 | Reach | `*_range` | low 140 / hi 240 / front 260 / roof, front_roof 400 | `range_set` 220 low, 320 hi, 350 front | 220 / 320 / 350 / 400 | Low beam, high beam and aux lamps carry farther on interstates and two-lane roads |
| | | `*_bias` | 0.0 | identity | 0.0 | |
| **T3** | Width | `*_angle` | 90° (aspect 2.0 untouched) | `angle_set` 103 (all stages); low beam `aspect_set` 2.289 | 103°; low beam aspect 2.289 | Shoulders and curves; low-beam cutoff not stretched taller |
| **T6** | Cutoff | low-beam mask `bf_<pattern>_norm` | BF's soft glow above the cutoff (10-90% edge 9-46 px of 512) | `EDGE_GAMMA` 2 below `EDGE_PROTECT` 50% of the column peak; left lift `LEFT_LIFT_GAP` 0 / `LEFT_LIFT_CAP` 14 rows | edge 4-32 px; left cutoff 3-14 rows higher | Crisp cutoff line; left of the road lit farther; check on a conventional and a high-cab truck |
| T4 | Near-field | `*_refracted_*` | fraction 0.02, range 60 | identity | stock | |
| **T5** | Lamp glow | `vehicle_headl`: `default_scale` / `scale_factor` | 1.6 / 3.5 | ×1.15 / ×1.1 | 1.84 / 3.85 | Lamp readable in poor daylight |
| | | `vehicle_headl`: `flare_inner_angle` / `flare_outer_angle` | 65° / 80° | +10 / +10 | 75° / 90° | |
| | | `vehicle_high_beam`: `default_scale` / `scale_factor` | 1.8 / 4.0 | ×1.15 / ×1.1 | 2.07 / 4.4 | |
| | | `vehicle_high_beam`: `flare_inner_angle` / `flare_outer_angle` | 65° / 80° | +10 / +10 | 75° / 90° | |

Aim is one value for every truck in v4.9 (`low_beam_left_rot (-0.55, 0, 0)`), not per truck.

| Build | Changed | Verdict |
|---|---|---|
| 1.0.0-dev.1 | ETS2 2.1.0 values on ATS 1.62 (generated files and masks byte-identical to ETS2 2.1.0) | Pending playtest |

## Running a new round

1. Change **one lever group** (two at once only when you can tell their effects apart in-game) and add a
   `# Tn (<version>): ...` note above the levers.
2. Regenerate: `python tools/generate_headlights.py` (and `python tools/generate_masks.py` for T6). Check the
   printed key counts and the ATS coverage line, and diff one file against upstream.
3. Bump `package_version` in `src/manifest.sii` to the next `-dev.N`, run `python tools/generate_cover.py`, and
   commit source and cover together.
4. Pack locally (`pack-mod`), playtest night + bad-weather day on a conventional and a high-cab truck, and add a
   row to the build table above.
5. When a round is kept, update the rounds table's lever and released columns.
