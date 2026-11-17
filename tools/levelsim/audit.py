"""Coverage audit of the level simulator: what is simulated, what is tested and what is left out.

    python tools/levelsim/audit.py [--iterations 300] [--jobs N] [--no-talents | --keep-talents]

Reads results/levels.json and results/levels_crafted.json (written by run.py) and writes
docs/assets/data/level-audit.json for the wiki page. It answers five questions:

1. Matrix: is every class, spec, race, gear mode and level cell present, with a positive DPS?
2. Abilities: for every damaging class spell in the Forever client, is it used by some spec,
   tested as an option and not chosen, or left out for a stated reason?
3. Talents: does every build follow its tree (known talents, legal ranks, level - 9 points)?
   What does each talent of each level 60 build add? Each one is removed in turn and the
   fight is run again (same seeds), so a talent with no modelled effect shows up as 0.
4. Racials: what does the simulator do with each of the 40 racials?
5. Trajectory: where does DPS fall from one level to the next by more than the noise?

What the audit cannot make complete: the simulator runs one talent build and one priority
list per spec. Other talent allocations and other rotations are not enumerated. The page
says so next to the numbers.

`test_audit.py` fails when a cell is missing, a damaging spell is unaccounted for, or a
build breaks its tree.
"""
import argparse
import importlib
import json
import math
import os
import sys
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parent.parent
OUT = ROOT / "docs" / "assets" / "data" / "level-audit.json"
TREES = HERE.parent / "talents" / "trees"
RESULTS = {"none": HERE / "results" / "levels.json", "crafted": HERE / "results" / "levels_crafted.json"}

import core  # noqa: E402
import run  # noqa: E402

# Why a damaging class spell is not part of any rotation. Categories:
REASONS = {
    "tested": "An option in the rotation. The simulator compares it with the alternatives and it is not chosen.",
    "starved": "In the rotation, but the character has no mana left when it becomes usable, so it is never cast.",
    "multi": "Built for several targets or close range. The fight has one target.",
    "reactive": "Needs the target to attack, cast or be attacked. The training target does nothing.",
    "kill": "Needs a killing blow. The target does not die.",
    "type": "Works on some creature types only. The training target has none.",
    "utility": "Control, threat or movement tool with little damage. Not tested as a damage option.",
    "talent": "Needs a talent that no simulated build takes.",
    "form": "Needs a form, stance or weapon the simulated build does not use.",
    "untested": "Could add single-target damage. It is not in the rotation and has not been tested.",
}
EXCLUDED = {
    "warrior": {
        "Cleave": "multi", "Hamstring": "utility", "Intercept": "utility", "Mocking Blow": "utility",
        "Pummel": "utility", "Revenge": "reactive", "Shield Bash": "utility", "Spearing Strike": "talent",
        "Victory Rush": "kill",
    },
    "paladin": {
        "Exorcism": "type", "Holy Wrath": "type", "Eye for an Eye": "reactive",
        "Hammer of the Righteous": "tested",
    },
    "hunter": {
        "Counterattack": "reactive", "Explosive Trap": "tested", "Raptor Strike": "form", "Wing Clip": "form",
    },
    "rogue": {"Gouge": "utility", "Kick": "utility"},
    "priest": {
        "Chastise": "type", "Shadowguard": "reactive", "Touch of Weakness": "reactive",
    },
    "shaman": {},
    "mage": {
        "Arcane Explosion": "multi", "Blast Wave": "multi", "Cone of Cold": "multi", "Flamestrike": "multi",
        "Frost Nova": "multi", "Frostfire Bolt": "tested",
    },
    "warlock": {
        "Drain Soul": "tested", "Health Funnel": "utility", "Hellfire": "multi", "Hellfire Effect": "multi",
    },
    "druid": {
        "Entangling Roots": "utility", "Lacerate": "form", "Nature's Grasp": "reactive", "Pounce": "tested",
        "Primal Bite": "form", "Swipe": "multi",
    },
}
# Client spells that a rotation uses under another damage source name.
ALIASES = {
    "paladin": {"Judgement of Righteousness": "Judgement", "Righteous Judgement": "Judgement",
                "Judgement of Fury": "Judgement"},
}
WEAPON_EFFECTS = {core.WEAPON_DAMAGE_NOSCHOOL, core.WEAPON_PERCENT_DAMAGE, core.NORMALIZED_WEAPON_DMG, core.WEAPON_DAMAGE}


def load_rows():
    rows = []
    for mode, src in RESULTS.items():
        if src.exists():
            for r in json.loads(src.read_text(encoding="utf-8")):
                r["gear"] = mode
                rows.append(r)
    return rows


# ---------- 1. matrix ----------

def matrix(rows):
    have = {(r["class"], r["spec"], r["race"], r["gear"], r["level"]): r for r in rows}
    want = run.expected_cells()
    missing = [c for c in want if c not in have]
    bad = [c for c in want if c in have and not (have[c]["dps_mean"] > 0 and math.isfinite(have[c]["dps_mean"]))]
    series = {c[:4] for c in want}
    return {"cells_expected": len(want), "cells_present": len(want) - len(missing), "series": len(series),
            "classes": len({c[0] for c in want}), "specs": len({c[:2] for c in want}),
            "class_race_pairs": len({(c[0], c[2]) for c in want}), "levels": len(run.LEVELS),
            "gear_modes": run.GEAR_MODES, "missing": [list(c) for c in missing[:50]],
            "not_positive": [list(c) for c in bad[:50]],
            "iterations": rows[0].get("iterations") if rows else None}


# ---------- 2. abilities ----------

def damaging_spells(cls):
    """Trained class spells with a damage effect: {name: first level}."""
    out = {}
    for s in core.data()["classes"][cls]["spells"]:
        if s["base_level"] <= 0:
            continue
        if core.damage_effect(s) or any(e["Effect"] in WEAPON_EFFECTS for e in s["effects"]):
            out[s["name"]] = min(out.get(s["name"], 99), s["base_level"])
    return out


def abilities(rows):
    used = defaultdict(dict)  # class -> source name -> {"level": first level, "specs": set}
    for r in rows:
        names = set(r["breakdown"]) | {k for k, v in (r.get("casts_per_min") or {}).items() if v > 0}
        for n in names:
            u = used[r["class"]].setdefault(n, {"level": r["level"], "specs": set()})
            u["level"] = min(u["level"], r["level"])
            u["specs"].add(r["spec_name"])
    out = {}
    for cls in sorted(used):
        spells, listed = damaging_spells(cls), []
        for name, lvl in sorted(spells.items(), key=lambda kv: (kv[1], kv[0])):
            src = ALIASES.get(cls, {}).get(name, name)
            hits = [u for n, u in used[cls].items() if n == src or n.startswith(src + " (") or n.endswith(": " + src)]
            if hits:
                listed.append({"name": name, "learned": lvl, "status": "used",
                               "first_used": min(h["level"] for h in hits),
                               "specs": sorted(set().union(*(h["specs"] for h in hits)))})
            elif name in EXCLUDED.get(cls, {}):
                listed.append({"name": name, "learned": lvl, "status": EXCLUDED[cls][name]})
            else:
                listed.append({"name": name, "learned": lvl, "status": "unaccounted"})
        other = sorted(n for n in used[cls] if not any(n == s or n.startswith(s + " (") or n.endswith(": " + s) for s in spells))
        out[cls] = {"spells": listed, "other_sources": other}
    return out


# ---------- 3. talents ----------

def trees(cls):
    t = json.loads((TREES / f"{cls}.json").read_text(encoding="utf-8"))
    return {x["name"]: {"tree": tr["name"], "max": x["max"]} for tr in t["trees"] for x in tr["talents"]}


def build_checks():
    """Every build at every level: known talents, legal ranks, level - 9 points."""
    problems = []
    for name in run.class_modules():
        mod = importlib.import_module(f"classes.{name}")
        tr = trees(mod.CLASS)
        for spec in mod.SPECS:
            for lv in run.LEVELS:
                tal = mod.talents_at(spec, lv)
                pts = sum(tal.values())
                if pts != max(0, lv - 9):
                    problems.append(f"{mod.CLASS} {spec} level {lv}: {pts} points, expected {max(0, lv - 9)}")
                for n, r in tal.items():
                    if n not in tr:
                        problems.append(f"{mod.CLASS} {spec} level {lv}: {n} is not in the talent tree")
                    elif r > tr[n]["max"]:
                        problems.append(f"{mod.CLASS} {spec} level {lv}: {n} rank {r} above max {tr[n]['max']}")
    return problems


def ablate(task):
    """Level 60 DPS of one spec with each talent of its build removed in turn. Worker process."""
    name, spec, race, iterations, seed = task
    import classes  # noqa: F401
    mod = importlib.import_module(f"classes.{name}")
    core.GEAR["mode"], core.GEAR["spec"] = "crafted", spec
    real = mod.talents_at
    full = real(spec, 60)
    base = mod.simulate(spec, race, 60, iterations, seed)
    half = (base["ci95"][1] - base["ci95"][0]) / 2
    out = []
    for talent in full:
        def without(s, lv, talent=talent):
            t = dict(real(s, lv))
            t.pop(talent, None)
            return t
        mod.talents_at = without
        try:
            d = mod.simulate(spec, race, 60, iterations, seed)["dps_mean"]
            delta = (base["dps_mean"] - d) / base["dps_mean"] * 100
            out.append({"talent": talent, "rank": full[talent], "adds_pct": round(delta, 2),
                        "measurable": abs(base["dps_mean"] - d) > 2 * half})
        except Exception as exc:  # a module that cannot run without the talent
            out.append({"talent": talent, "rank": full[talent], "adds_pct": None, "measurable": False,
                        "error": type(exc).__name__})
        finally:
            mod.talents_at = real
    return {"class": mod.CLASS, "spec": spec, "spec_name": mod.SPECS[spec], "race": race,
            "dps": base["dps_mean"], "ci": round(half, 2), "talents": out}


def talents(iterations, jobs, seed=1):
    tasks = []
    for name in run.class_modules():
        mod = importlib.import_module(f"classes.{name}")
        for spec in mod.SPECS:
            tasks.append((name, spec, run.CLASS_RACES[mod.CLASS][0], iterations, seed))
    with ProcessPoolExecutor(max_workers=jobs) as pool:
        specs = list(pool.map(ablate, tasks))
    out = {}
    for s in specs:
        tr = trees(s["class"])
        for t in s["talents"]:
            t["tree"] = tr.get(t["talent"], {}).get("tree", "?")
        c = out.setdefault(s["class"], {"specs": [], "tree_size": len(tr)})
        c["specs"].append(s)
    for cls, c in out.items():
        taken = {t["talent"] for s in c["specs"] for t in s["talents"]}
        c["never_taken"] = sorted(set(trees(cls)) - taken)
    return out


# ---------- 5. trajectory ----------

def dips(rows, threshold=0.05):
    """Level-to-level falls larger than `threshold` and larger than the two confidence intervals."""
    series = defaultdict(dict)
    for r in rows:
        series[(r["class"], r["spec_name"], r["race"], r["gear"])][r["level"]] = r
    found = defaultdict(list)
    for (cls, spec, race, gear), by in series.items():
        for lv in sorted(by)[1:]:
            a, b = by.get(lv - 1), by[lv]
            if not a or a["dps_mean"] <= 0:
                continue
            noise = (a["ci95"][1] - a["ci95"][0]) / 2 + (b["ci95"][1] - b["ci95"][0]) / 2
            fall = a["dps_mean"] - b["dps_mean"]
            if fall > threshold * a["dps_mean"] and fall > noise:
                found[(cls, spec, gear, lv)].append((race, round(-fall / a["dps_mean"] * 100, 1)))
    out = []
    for (cls, spec, gear, lv), races in sorted(found.items()):
        out.append({"class": cls, "spec": spec, "gear": gear, "level": lv, "races": len(races),
                    "worst_pct": min(p for _, p in races)})
    return out


def gear_cover():
    import gear as gear_mod
    out = []
    for name in run.class_modules():
        mod = importlib.import_module(f"classes.{name}")
        for spec in mod.SPECS:
            filled = [len(gear_mod.select(mod.CLASS, spec, lv)["items"]) for lv in run.LEVELS]
            first_weapon = next((lv for lv in run.LEVELS if gear_mod.select(mod.CLASS, spec, lv)["mh"]), None)
            out.append({"class": mod.CLASS, "spec": mod.SPECS[spec], "slots_at_1": filled[0], "slots_at_30": filled[29],
                        "slots_at_60": filled[-1], "first_weapon_level": first_weapon})
    return out


def audit(iterations=300, jobs=None, with_talents=True):
    import classes  # noqa: F401
    rows = load_rows()
    doc = {
        "matrix": matrix(rows),
        "abilities": abilities(rows),
        "reasons": REASONS,
        "build_problems": build_checks(),
        "racials": {race: [{"name": n, "status": s, "note": note} for n, s, note in items]
                    for race, items in core.RACIAL_STATUS.items()},
        "dips": dips(rows),
        "gear": gear_cover(),
    }
    if with_talents:
        doc["talents"] = talents(iterations, jobs or max(1, (os.cpu_count() or 2) - 1))
        doc["talent_iterations"] = iterations
    return doc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iterations", type=int, default=300)
    ap.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument("--no-talents", action="store_true")
    ap.add_argument("--keep-talents", action="store_true",
                    help="keep the talent tests of the existing audit file (valid only if no class module changed since)")
    a = ap.parse_args()
    doc = audit(a.iterations, a.jobs, not (a.no_talents or a.keep_talents))
    if a.keep_talents and OUT.exists():
        old = json.loads(OUT.read_text(encoding="utf-8"))
        for k in ("talents", "talent_iterations"):
            if k in old:
                doc[k] = old[k]
    OUT.write_text(json.dumps(doc, separators=(",", ":")), encoding="utf-8")
    m = doc["matrix"]
    un = [f"{c}: {s['name']}" for c, v in doc["abilities"].items() for s in v["spells"] if s["status"] == "unaccounted"]
    print(f"cells {m['cells_present']}/{m['cells_expected']}, missing {len(m['missing'])}, not positive {len(m['not_positive'])}")
    print(f"unaccounted spells: {un or 'none'}")
    print(f"build problems: {doc['build_problems'][:5] or 'none'}")
    print(f"dips: {len(doc['dips'])}")
    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
