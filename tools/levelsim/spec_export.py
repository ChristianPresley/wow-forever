"""Export a full character specification for every class, spec, race, gear mode and level.

    python tools/levelsim/spec_export.py [--iterations 10] [--gear none,crafted] [--classes warrior]

For each class, spec and gear mode it writes docs/assets/data/specs/<class>-<spec>-<gear>.json:

    {"class", "spec", "spec_name", "gear", "levels": {"60": {
        "talents": {"Arms": {"Deep Wounds": 3, ...}, ...},     # talent tree -> talent -> rank
        "points": {"Arms": 31, ...},
        "gear": {"items": {slot: {...}}, "enchants": [...], "stats": {...}} | null,
        "races": {"orc": {"dps", "tl": [t*10, name index, ...], "cpm": {name index: casts per minute},
                          "dmg": {name index: DPS}}}}},
     "names": [ability or damage source, ...]}

tl is the timeline is the first fight's cast sequence (up to core.TRACE["max_events"] casts),
so it shows the opener and the priority in action. casts_per_min and breakdown are
averaged over the iterations. The wiki's DPS by level table loads these files when a
row is clicked.
"""
import argparse
import importlib
import json
import pkgutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
OUT = HERE.parent.parent / "docs" / "assets" / "data" / "specs"

import core  # noqa: E402
import gear as gear_mod  # noqa: E402
from run import CLASS_RACES  # noqa: E402


RESEARCH = HERE.parent.parent / ".research" / "talents"
_TREE = {}


def tree_of(cls, name):
    """Talent tree name: the live Forever trees (.research/talents, local only), else the client."""
    if cls not in _TREE:
        _TREE[cls] = {}
        p = RESEARCH / f"{cls}.json"
        if p.exists():
            for tree in json.loads(p.read_text(encoding="utf-8"))["trees"]:
                for t in tree["talents"]:
                    _TREE[cls][t["name"]] = tree["name"]
    if name in _TREE[cls]:
        return _TREE[cls][name]
    try:
        return core.talent(cls, name)["tab"]
    except KeyError:
        return "Other"


def talents_by_tree(cls, talents):
    trees, points = {}, {}
    for name, rank in talents.items():
        tab = tree_of(cls, name)
        trees.setdefault(tab, {})[name] = rank
        points[tab] = points.get(tab, 0) + rank
    return trees, points


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iterations", type=int, default=10)
    ap.add_argument("--gear", default="none,crafted")
    ap.add_argument("--classes", default="")
    ap.add_argument("--levels", default="1-60")
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    from run import parse_levels
    levels = parse_levels(a.levels)
    wanted = set(filter(None, a.classes.split(",")))
    core.TRACE["on"] = True
    OUT.mkdir(parents=True, exist_ok=True)
    import classes  # noqa: F401
    for m in pkgutil.iter_modules([str(HERE / "classes")]):
        if m.name.startswith("test_") or (wanted and m.name not in wanted):
            continue
        mod = importlib.import_module(f"classes.{m.name}")
        for mode in a.gear.split(","):
            core.GEAR["mode"] = mode
            for spec, spec_name in mod.SPECS.items():
                core.GEAR["spec"] = spec
                names = []

                def ix(n, names=names):
                    if n not in names:
                        names.append(n)
                    return names.index(n)
                doc = {"class": mod.CLASS, "spec": spec, "spec_name": spec_name, "gear": mode,
                       "iterations": a.iterations, "fight_seconds": core.A("fight_seconds"), "levels": {}}
                for lv in levels:
                    tal = mod.talents_at(spec, lv)
                    trees, points = talents_by_tree(mod.CLASS, tal)
                    g = None
                    if mode == "crafted":
                        sel = gear_mod.select(mod.CLASS, spec, lv)
                        g = {"items": sel["items"], "enchants": sel["enchants"],
                             "stats": {k: v for k, v in sel["stats"].items() if v and not k.startswith("res_")}}
                    races = {}
                    for race in CLASS_RACES[mod.CLASS]:
                        r = mod.simulate(spec, race, lv, a.iterations, a.seed)
                        tl = []
                        for t, name in r.get("timeline") or []:
                            tl += [round(t * 10), ix(name)]
                        races[race] = {"dps": round(r["dps_mean"], 1), "tl": tl,
                                       "cpm": {ix(k): round(v, 1) for k, v in (r.get("casts_per_min") or {}).items() if v >= 0.05},
                                       "dmg": {ix(k): round(v, 1) for k, v in r["breakdown"].items() if v >= 0.05}}
                    doc["levels"][str(lv)] = {"talents": trees, "points": points, "gear": g, "races": races}
                doc["names"] = names
                path = OUT / f"{mod.CLASS}-{spec}-{mode}.json"
                path.write_text(json.dumps(doc, separators=(",", ":")), encoding="utf-8")
                print(f"{path.name}: {path.stat().st_size // 1024} KB", flush=True)
    core.TRACE["on"] = False


if __name__ == "__main__":
    main()
