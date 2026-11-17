"""Run every class module for every spec, race, level and gear mode.

    python tools/levelsim/run.py [--iterations N] [--levels 1-60] [--classes warrior,mage]
                                 [--gear none,crafted] [--jobs N] [--no-specs]

One pass writes both outputs:
- tools/levelsim/results/levels.json (no gear) and levels_crafted.json: one row per class,
  spec, race and level with the mean DPS, its confidence interval, the damage by source,
  casts per minute, talents and input tags.
- docs/assets/data/specs/<class>-<spec>-<gear>.json: the build panel data of the wiki page
  (see spec_export.py for the shape). Skipped with --no-specs or a partial --levels run.

The matrix is the full product CLASS_RACES x SPECS x levels x gear modes; `audit.py` checks
that no cell is missing. Work is split by class, spec, gear and race over --jobs processes.
The seed of a cell does not depend on the split, so results are reproducible.
"""
import argparse
import importlib
import json
import os
import pkgutil
import sys
from concurrent.futures import ProcessPoolExecutor
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
GEAR_MODES = ["none", "crafted"]
LEVELS = list(range(1, 61))


def parse_levels(text):
    out = set()
    for part in text.split(","):
        a, _, b = part.partition("-")
        out.update(range(int(a), int(b or a) + 1))
    return sorted(out)


def class_modules(wanted=()):
    """Names of the class modules in classes/, optionally limited to `wanted`."""
    return [m.name for m in pkgutil.iter_modules([str(HERE / "classes")])
            if not m.name.startswith("test_") and (not wanted or m.name in wanted)]


def expected_cells(classes=None):
    """Every (class, spec, race, gear, level) cell the simulator must produce."""
    out = []
    for name in class_modules(classes or ()):
        mod = importlib.import_module(f"classes.{name}")
        for spec in mod.SPECS:
            for race in CLASS_RACES[mod.CLASS]:
                for gear in GEAR_MODES:
                    for lv in LEVELS:
                        out.append((mod.CLASS, spec, race, gear, lv))
    return out


def simulate_series(task):
    """One class, spec, gear mode and race across the levels. Runs in a worker process."""
    name, spec, gear, race, levels, iterations, seed = task
    import classes  # noqa: F401
    import core
    mod = importlib.import_module(f"classes.{name}")
    core.GEAR["mode"], core.GEAR["spec"] = gear, spec
    core.TRACE["on"] = True
    rows = []
    for lv in levels:
        r = mod.simulate(spec, race, lv, iterations, seed)
        for racial, status, _ in core.RACIAL_STATUS[race]:
            if status != "none":  # Touch of the Grave's proc chance and health base are assumptions
                r["inputs"][f"racial:{racial}"] = "A" if racial == core.TOUCH else "F"
        rows.append({"class": mod.CLASS, "spec": spec, "spec_name": mod.SPECS[spec], "race": race,
                     "level": lv, "gear": gear, "talents": mod.talents_at(spec, lv), **r})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iterations", type=int, default=100)
    ap.add_argument("--levels", default="1-60")
    ap.add_argument("--classes", default="")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--gear", default="none,crafted")
    ap.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument("--no-specs", action="store_true", help="do not rewrite the wiki build panel files")
    a = ap.parse_args()
    levels = parse_levels(a.levels)
    wanted = set(filter(None, a.classes.split(",")))
    modes = [g for g in a.gear.split(",") if g]
    import classes  # noqa: F401
    tasks = []
    for name in class_modules(wanted):
        mod = importlib.import_module(f"classes.{name}")
        for spec in mod.SPECS:
            for gear in modes:
                for race in CLASS_RACES[mod.CLASS]:
                    tasks.append((name, spec, gear, race, levels, a.iterations, a.seed))
    # longest series first, so the pool stays busy to the end
    tasks.sort(key=lambda t: t[0] not in ("mage", "priest", "druid", "shaman"))
    rows = []
    with ProcessPoolExecutor(max_workers=a.jobs) as pool:
        for i, part in enumerate(pool.map(simulate_series, tasks), 1):
            rows.extend(part)
            t = tasks[i - 1]
            print(f"[{i}/{len(tasks)}] {t[0]:8} {t[1]:14} {t[2]:7} {t[3]:7} done", flush=True)
    order = {c: i for i, c in enumerate(class_modules())}
    rows.sort(key=lambda r: (order.get(r["class"], 99), r["spec"], r["race"], r["level"]))
    (HERE / "results").mkdir(exist_ok=True)
    for mode in modes:
        out = HERE / "results" / ("levels.json" if mode == "none" else f"levels_{mode}.json")
        part = [{k: v for k, v in r.items() if k != "timeline"} for r in rows if r["gear"] == mode]
        if wanted or levels != LEVELS:  # partial run: merge into the existing file
            old = json.loads(out.read_text(encoding="utf-8")) if out.exists() else []
            key = lambda r: (r["class"], r["spec"], r["race"], r["level"])
            new = {key(r) for r in part}
            part = sorted([r for r in old if key(r) not in new] + part,
                          key=lambda r: (order.get(r["class"], 99), r["spec"], r["race"], r["level"]))
        out.write_text(json.dumps(part, separators=(",", ":")), encoding="utf-8")
        print(f"wrote {len(part)} rows to {out}")
    if not a.no_specs and levels == LEVELS:
        import spec_export
        spec_export.write_docs(rows, a.iterations)


if __name__ == "__main__":
    main()
