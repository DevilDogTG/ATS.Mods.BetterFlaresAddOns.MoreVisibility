"""
Pins shared by the generators: this repo is the ATS twin of ETS2 MoreVisibility
(ADR-0001), generated from the ATS extraction of Better Flares 4.9.1 and
checked against the ATS 1.62 base game. Running it for the wrong game, or on
another Better Flares or base-game version, fails here instead of building a
mod from the wrong reference.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# This host's extracted-reference root for the game, from the scs-mod-developer host config.
sys.path.insert(0, str(Path.home() / ".agent-brains/profiles/scs-mod-developer/skills/megapack/scripts"))
from megapack import base_dir, ref_list, reference_root, repo_game  # noqa: E402,F401

GAME = "ats"
BASE_VERSION = "1.62"
BF_VERSION = "4.9.1"
BF_ROOT = reference_root(GAME) / "local" / "better-flares" / BF_VERSION

VERSION_RE = re.compile(r'^\s*package_version:\s*"([^"]+)"', re.MULTILINE)
GAME_VERSION_RE = re.compile(r"^- game_version:\s*(\S+)", re.MULTILINE)


def fail(msg):
    raise SystemExit(f"error: {msg}")


def check_game():
    if repo_game(ROOT) != GAME:
        fail(f"these generators are for {GAME}; pack.config.json says {repo_game(ROOT)!r}")


def check_bf(*packs):
    """Every Better Flares pack read must be the pinned version (its manifest says so)."""
    for pack in packs:
        manifest = Path(pack) / "manifest.sii"
        if not manifest.is_file():
            fail(f"{pack} missing - extract Better Flares {BF_VERSION} for {GAME}")
        m = VERSION_RE.search(manifest.read_text(encoding="utf-8", errors="replace"))
        if not m or m.group(1) != BF_VERSION:
            fail(f"{pack} is Better Flares {m.group(1) if m else '?'}, generators pin {BF_VERSION}")


def base_game():
    """The pinned base-game extraction (for the truck coverage check)."""
    base = base_dir(reference_root(GAME), BASE_VERSION)
    meta = base / "_extract-meta.md"
    if not meta.is_file():
        fail(f"{base} has no extraction - run extract-reference for {GAME} {BASE_VERSION}")
    m = GAME_VERSION_RE.search(meta.read_text(encoding="utf-8"))
    if not m or not m.group(1).startswith(BASE_VERSION + "."):
        fail(f"base extraction is {m.group(1) if m else '?'}, generators pin {BASE_VERSION}")
    return base
