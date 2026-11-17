"""Build panel data for the wiki: one file per class, spec and gear mode.

`run.py` calls `write_docs` with the rows of a full run, so the panel shows the same fights
as the table. Running this file is the same as `python tools/levelsim/run.py`.

docs/assets/data/specs/<class>-<spec>-<gear>.json:

    {"class", "spec", "spec_name", "gear", "iterations", "fight_seconds", "levels": {"60": {
        "talents": {"Arms": {"Deep Wounds": 3, ...}, ...},     # talent tree -> talent -> rank
        "points": {"Arms": 31, ...},
        "gear": {"items": {slot: {...}}, "enchants": [...], "stats": {...}} | null,
        "races": {"orc": {"dps", "ci", "tl": [t*10, name index, ...],
                          "cpm": {name index: casts per minute}, "dmg": {name index: DPS}}}}},
     "names": [ability or damage source, ...]}

`tl` is the first fight's cast sequence (up to core.TRACE["max_events"] casts), so it shows
the opener and the priority in action. `cpm`, `dmg`, `dps` and `ci` (half of the 95%
confidence interval) are averaged over the iterations. Every level from 1 to 60 is present,
so the page can chart damage by source across levels for one race.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
OUT = HERE.parent.parent / "docs" / "assets" / "data" / "specs"

import core  # noqa: E402
import gear as gear_mod  # noqa: E402

RESEARCH = HERE.parent.parent / ".research" / "talents"
TREES = HERE.parent / "talents" / "trees"
_TREE = {}


def tree_of(cls, name):
    """Talent tree name: the live Forever trees (tools/talents/trees, or .research), else the client."""
    if cls not in _TREE:
        _TREE[cls] = {}
        for p in (RESEARCH / f"{cls}.json", TREES / f"{cls}.json"):
            if p.exists():
                for tree in json.loads(p.read_text(encoding="utf-8"))["trees"]:
                    for t in tree["talents"]:
                        _TREE[cls].setdefault(t["name"], tree["name"])
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


def write_docs(rows, iterations):
    """Write one build panel file per class, spec and gear mode from run.py rows."""
    groups = defaultdict(list)
    for r in rows:
        groups[(r["class"], r["spec"], r["gear"])].append(r)
    OUT.mkdir(parents=True, exist_ok=True)
    for (cls, spec, mode), part in sorted(groups.items()):
        names = []

        def ix(n, names=names):
            if n not in names:
                names.append(n)
            return names.index(n)
        doc = {"class": cls, "spec": spec, "spec_name": part[0]["spec_name"], "gear": mode,
               "iterations": iterations, "fight_seconds": core.A("fight_seconds"), "levels": {}}
        by_level = defaultdict(list)
        for r in part:
            by_level[r["level"]].append(r)
        for lv in sorted(by_level):
            trees, points = talents_by_tree(cls, by_level[lv][0]["talents"])
            g = None
            if mode == "crafted":
                sel = gear_mod.select(cls, spec, lv)
                g = {"items": sel["items"], "enchants": sel["enchants"],
                     "stats": {k: v for k, v in sel["stats"].items() if v and not k.startswith("res_")}}
            races = {}
            for r in by_level[lv]:
                tl = []
                for t, name in r.get("timeline") or []:
                    tl += [round(t * 10), ix(name)]
                races[r["race"]] = {
                    "dps": round(r["dps_mean"], 1), "ci": round((r["ci95"][1] - r["ci95"][0]) / 2, 1), "tl": tl,
                    "cpm": {ix(k): round(v, 1) for k, v in (r.get("casts_per_min") or {}).items() if v >= 0.05},
                    "dmg": {ix(k): round(v, 1) for k, v in r["breakdown"].items() if v >= 0.05}}
            doc["levels"][str(lv)] = {"talents": trees, "points": points, "gear": g, "races": races}
        doc["names"] = names
        path = OUT / f"{cls}-{spec}-{mode}.json"
        path.write_text(json.dumps(doc, separators=(",", ":")), encoding="utf-8")
        print(f"{path.name}: {path.stat().st_size // 1024} KB", flush=True)


if __name__ == "__main__":
    import run
    run.main()
