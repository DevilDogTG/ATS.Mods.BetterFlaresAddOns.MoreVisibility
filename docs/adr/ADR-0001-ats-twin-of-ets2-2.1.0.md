# ADR-0001: ATS twin of ETS2 MoreVisibility 2.1.0

- Status: accepted
- Date: 2026-11-24
- Origin: World ATS plan `bf-addons-ats-port` (exploration report `reports/2026-11-24-exploration.md`, decisions
  D1-D7, maintainer 2026-11-24)

## Context
ETS2 MoreVisibility 2.1.0 (`DevilDogTG/ETS2.Mods.BetterFlaresAddOns.MoreVisibility` `4ee3ce1`) overrides Better
Flares v4.9's shared `def/vehicle/_common/color.sui` and the two headlight flare units with generated copies, and
ships six sharpened low-beam masks (its ADR-0002). An ATS version was wanted.

The exploration found:
- Better Flares 4.9 / 4.9.1 archives are byte-identical for ETS2 and ATS, all but the Traffic Addon
  (`bf_ta_ats_v4.9.scs` vs `bf_ta_ets2_v4.9.1.scs`), which this mod does not read.
- The ETS2 generators, run on the ATS extraction, reproduce ETS2 2.1.0's `src/def`, `src/unit` and masks
  byte-for-byte.
- Better Flares Headlights.1 covers all 19 ATS 1.62 trucks (27 `head_light` defs at the base game's paths), and
  every one includes `/def/vehicle/_common/color.sui`.

## Decision
- A separate public repo with the same package name (`drivedog_bf_morevisibility_dot7500`) and display name as the
  ETS2 mod; the game is set by `pack.config.json` (`ats`), which also gives the cover its red ATS badge.
- Copy the ETS2 generators from `4ee3ce1` unchanged in design and values (ETS2 2.1.0 levers, D3); retune only if
  ATS playtesting needs it (US lamp heights, wider roads), logged in `docs/tuning.md`.
- Pin the generators (`tools/pins.py`): fail unless the repo's game is `ats`, every Better Flares pack read is
  `4.9.1`, and the base-game extraction is ATS `1.62`.
- Add an ATS coverage check to `generate_headlights.py`: every base-game
  `def/vehicle/truck/*/head_light/*.sii` must exist, including `color.sui`, in every Headlights.1 pack. A miss is a
  warning naming the truck, not a failure: the mod still works for every other truck.
- Version starts at `1.0.0-dev.1`; first release `1.0.0`.

## Consequences
- Load order: this mod above every Better Flares headlight pack and the ATS Traffic Addon, below DriveDogs BF City
  Lights. Requires BF Base 4.9.1, one Headlights.1 and Headlights.2 7500K LED.
- A Better Flares or ATS update needs a re-extraction and a pin bump before the generators run again; a new truck
  Better Flares does not cover shows up as a coverage warning.
- The two repos share their generator design; a change to the ETS2 generators should be ported here (and back).
- The masks are modified Better Flares textures: GitHub release notes only, no `.scs` and no Workshop upload until
  Avelium grants permission.
