# DriveDogs: Better Flares More Visibility (7500K LED) — ATS

An American Truck Simulator add-on for **Better Flares v4.9 - Headlights.2 7500K LED** (by Avelium). Truck
headlights spread wider and the low and high beams reach farther for more comfortable night driving, and the
headlamp glow stays readable in bad daytime conditions, while keeping Better Flares' realistic mood.

The ATS twin of [ETS2 MoreVisibility](https://github.com/DevilDogTG/ETS2.Mods.BetterFlaresAddOns.MoreVisibility)
`2.1.0`: same design, same generators, same values (see
[`docs/adr/ADR-0001-ats-twin-of-ets2-2.1.0.md`](docs/adr/ADR-0001-ats-twin-of-ets2-2.1.0.md)).

**Status: `1.0.0-dev.1`** (towards `1.0.0`): low beam 220, x1.3 brighter, sharper cutoff with its left side raised
to the right side's level, high beam 320, front aux lamps 350, 103° on every stage. Better Flares v4.9.1 and ATS 1.62
only; 7500K LED only; any Headlights.1 pattern; all 19 ATS 1.62 trucks.

## Load order
Top = highest priority in Mod Manager:
1. DriveDogs: Better Flares City Lights (optional)
2. DriveDogs: Better Flares More Visibility (7500K LED)
3. Better Flares - Traffic Addon (ATS) (optional)
4. Better Flares - Headlights.2 7500K LED
5. Better Flares - Headlights.1 (any one)
6. Better Flares - City Lights Addon (optional)
7. Better Flares - Base

Headlights.1 and Headlights.2 are both required: every Headlights.1 truck def includes the
`def/vehicle/_common/color.sui` that only Headlights.2 ships.

## How it works
Better Flares v4.9 keeps every beam value for every truck in one file, Headlights.2's
`def/vehicle/_common/color.sui`; Headlights.1 truck defs only set masks and include it. The game replaces whole
files, so this mod ships a complete copy of that file (and of the two headlight flare units) with only the tuned
values changed. Those files are **generated, not hand-edited** (ETS2's ADR-0002 design; Better Flares 4.9.1's
archives are byte-identical for ETS2 and ATS, all but the Traffic Addon).

`tools/generate_headlights.py` reads the extracted upstream pack and applies the tuning levers at the
top of the script:

| Lever (per beam stage: low / hi / front / roof / front_roof) | Field(s) |
|---|---|
| `color_mult` | `*_color`, `*_color_specular`, `*_color_ambient` |
| `range_mult` / `range_set` | `*_range` (relative / absolute) |
| `bias_add` | `*_bias` |
| `angle_add` / `angle_set` | `*_angle` (relative / absolute; vertical FOV scales too unless `aspect_set` compensates) |
| `aspect_set` | `*_aspect` (absolute; horizontal / vertical spread) |
| `refr_fraction_mult` | `*_refracted_color_fraction` |
| `refr_range_mult` | `*_refracted_range` |

| Lever (flare units `vehicle_headl`, `vehicle_high_beam`) | Field |
|---|---|
| `default_scale_mult` | `default_scale` |
| `scale_factor_mult` | `scale_factor` |
| `inner_angle_add` / `outer_angle_add` | `flare_inner_angle` / `flare_outer_angle` |

Released values, per-round (Tx) history and how to run a new tuning round: see
[`docs/tuning.md`](docs/tuning.md).

Aim (`*_rot`) is never touched. Only files a lever actually changes are written. Checks on every run:
- **Pins** (`tools/pins.py`): `pack.config.json` must say `ats`, every Better Flares pack read must be `4.9.1`, and
  the base-game extraction must be ATS `1.62`. Any mismatch fails the run.
- **h1 check**: every Headlights.1 def next to the base pack must include `/def/vehicle/_common/color.sui` and name
  only masks the base pack ships, else the run fails.
- **ATS coverage**: every ATS 1.62 base truck headlight def (`def/vehicle/truck/*/head_light/*.sii`, from the base
  extraction's index) must have a def at the same path, including `color.sui`, in every Headlights.1 pack. Today:
  19 trucks / 27 defs, all covered. A miss is a warning naming the truck (Better Flares hasn't caught up with a new
  truck), not a failure.

```
python tools/generate_headlights.py            # regenerate src/def + src/unit
python tools/generate_headlights.py --all --out <dir>   # emit all three files (identity check with identity levers)
```
Defaults read `local/better-flares/4.9.1/bf_h2_7500K_led_v4.9.1` and `bf_base_v4.9.1` (with the `bf_h1_*` packs
next to it), and `base/1.62` for the coverage check, under this host's ATS extracted-reference root
(`scs-mod-developer` host config); `--source` / `--base` override the Better Flares packs.

`tools/generate_masks.py` writes sharper-cutoff copies of Better Flares Base's six low-beam masks
(`material/custom/bf_<pattern>_norm`) to `src/material/custom/`. Left of the centre step it raises the cutoff to at
most `LEFT_LIFT_GAP` rows below the right side's level (at most `LEFT_LIFT_CAP` rows), so the left of the road is lit
farther. Then, above each column's brightest row, it dims pixels below `EDGE_PROTECT` of the peak by a power curve
(`EDGE_GAMMA`), so the glow over the cutoff fades out faster while the beam itself and the steps stay put. The output
is gitignored and regenerated at `prePack`.

Run the tools with plain `python` (not `python -I`): they import the profile's `megapack` helpers, which need
`yaml` from the user site-packages.

## Building
Requires `scs_packer` (and `scs_extractor`, for verification) on `PATH`, and Python 3 with Pillow and NumPy.
Packing runs `pack.config.json`'s `prePack` (`generate_masks.py`, then `generate_cover.py`, which regenerates
`src/cover.jpg` with the `manifest.sii` version badge and the red ATS badge). Commit the regenerated cover with a
version bump.

- **Local**: the `scs-mod-developer` profile's `pack-mod` skill → versioned `.scs` in `output/local/`.
- **Workshop**: `pack-mod` stages `output/workshop/` for the SCS Workshop Uploader.

## Distribution
The sharpened masks are modified Better Flares textures. Until Avelium grants permission (SCS forum t=326854),
releases are GitHub release notes only: no `.scs` attached and no Workshop upload.

## Updating for a new Better Flares release
1. Extract the new base, every Headlights.1 and the Headlights.2 7500K LED pack into the ATS extracted-reference root.
2. Bump `BF_VERSION` in `tools/pins.py` and regenerate. A failed h1 check means Better Flares changed its design
   again; a coverage warning names a truck Better Flares doesn't cover.
3. Review `git diff src/`, playtest, bump the version.

For a new ATS release, extract the new base and bump `BASE_VERSION` in `tools/pins.py`; the coverage check then
lists any new truck.
