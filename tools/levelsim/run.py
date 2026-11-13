"""Run every class module for every spec, race and level.

    python tools/levelsim/run.py [--iterations N] [--levels 60] [--classes warrior,mage]

Writes tools/levelsim/results/levels.json.
"""
import argparse
import importlib
import json
import pkgutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

CLASS_RACES = {
    "warrior": ["human", "dwarf", "gnome", "nelf", "sho", "orc", "troll", "tauren", "undead", "sws"],
    "paladin": ["human", "dwarf", "undead"],
    "hunter": ["human", "dwarf", "nelf", "sho", "orc", "troll", "tauren", "sws"],
    "rogue": ["human", "dwarf", "gnome", "nelf", "sho", "orc", "troll", "undead", "sws"],
    "priest": ["human", "dwarf", "gnome", "nelf", "troll", "undead"],
    "shaman": ["dwarf", "orc", "troll", "tauren", "sws"],
    "mage": ["human", "gnome", "sho", "orc", "troll", "undead"],
    "warlock": ["human", "gnome", "orc", "troll", "undead"],
    "druid": ["nelf", "sho", "tauren", "sws"],
}


def parse_levels(text):
    out = set()
    for part in text.split(","):
        a, _, b = part.partition("-")
        out.update(range(int(a), int(b or a) + 1))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iterations", type=int, default=200)
    ap.add_argument("--levels", default="1-60")
    ap.add_argument("--classes", default="")
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    levels = parse_levels(a.levels)
    wanted = set(filter(None, a.classes.split(",")))
    rows = []
    import classes  # noqa: F401
    for m in pkgutil.iter_modules([str(HERE / "classes")]):
        if m.name.startswith("test_") or (wanted and m.name not in wanted):
            continue
        mod = importlib.import_module(f"classes.{m.name}")
        for spec, spec_name in mod.SPECS.items():
            for race in CLASS_RACES[mod.CLASS]:
                for lv in levels:
                    r = mod.simulate(spec, race, lv, a.iterations, a.seed)
                    rows.append({"class": mod.CLASS, "spec": spec, "spec_name": spec_name, "race": race,
                                 "level": lv, "talents": mod.talents_at(spec, lv), **r})
                print(f"{mod.CLASS:8} {spec:14} {race:7} done", flush=True)
    out = HERE / "results" / "levels.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(rows, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {len(rows)} rows to {out}")


if __name__ == "__main__":
    main()
