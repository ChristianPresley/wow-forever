"""Value of every talent, ability and stat of the four healer classes.

    python tools/healsim/ledger.py [--classes druid] [--dps-iterations 40] [--jobs N]

For each class it takes a reference healer (REFERENCE build, first race, best craftable
healing gear) and works out:

- talents: every talent of all three trees. Value = result with the talent at its maximum
  rank minus result without it, everything else as in the reference build (tree rules are
  ignored for this one comparison). Healing comes from model.solve, damage from the level
  simulator through model.off_dps. `heal` / `dmg` say whether the healing model or the damage
  simulator reads the talent at all; a talent neither reads has no throughput effect there.
- abilities: every castable rank of every healing spell with cast time, mana, healing per
  cast on one target and on a party, and in which optimal mixes it appears; every other
  trained ability is listed as damage (used by the damage simulator) or utility.
- stats: the healing gained per point of healing power, Intellect, Spirit, crit, mana per
  5 seconds, haste and mana (model.BONUS).

Writes tools/healsim/results/ledger.json and docs/assets/data/heal-ledger.json.
Needs .research/talents (local only) for the talent trees and tooltips.
"""
import argparse
import json
import os
import re
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parent.parent

import builds as B  # noqa: E402
import model  # noqa: E402

REFERENCE = {"priest": "holy-pom", "paladin": "holy-crit", "druid": "resto-splendor", "shaman": "resto-deep"}
STATS = [  # key, label, step used, unit of one point
    ("healing", "Healing power", 10, "point"), ("int", "Intellect", 10, "point"), ("spi", "Spirit", 10, "point"),
    ("crit", "Spell crit", 1, "1%"), ("mp5", "Mana per 5 seconds", 5, "point"), ("haste", "Haste", 1, "1%"),
    ("mana", "Maximum mana", 100, "point"),
]
RANK = re.compile(r" \(Rank \d+\)")
OUT = HERE / "results" / "ledger.json"
PUBLISHED = ROOT / "docs" / "assets" / "data" / "heal-ledger.json"


def reference(cls):
    return B.flat(next(b for b in B.BUILDS[cls] if b[0] == REFERENCE[cls])[4]), B.RACES[cls][0]


def healing(cls, race, talents):
    return {sc: [model.solve(cls, race, talents, "crafted", sc, m)["hps"] for m in model.MODES] for sc in model.SCENARIOS}


def diff(a, b):
    return {sc: [round(x - y, 1) for x, y in zip(a[sc], b[sc])] for sc in a}


def talent_job(job):
    cls, tree, t, dps_iter = job
    ref, race = reference(cls)
    with_t, without = dict(ref), dict(ref)
    with_t[t["name"]] = t["max"]
    without.pop(t["name"], None)
    d = diff(healing(cls, race, with_t), healing(cls, race, without))
    dps = None
    if dps_iter:
        a = model.off_dps(cls, race, with_t, "crafted", dps_iter)["dps"]
        b = model.off_dps(cls, race, without, "crafted", dps_iter)["dps"]
        dps = round(a - b, 1)
    text = t.get("rankmax") or t.get("rank1") or (t.get("text") or [""])[-1]     # for an active talent: the description, not its cost line
    return {"tree": tree, "name": t["name"], "max": t["max"], "row": t["row"], "ref": ref.get(t["name"], 0),
            "text": text.encode("ascii", "replace").decode().replace("?", "-") if "�" in text else text, "d": d, "dps": dps}


def abilities(cls):
    ref, race = reference(cls)
    used = {}
    for sc in model.SCENARIOS:
        for m in model.MODES:
            for x in model.solve(cls, race, ref, "crafted", sc, m)["mix"]:
                used.setdefault(x["name"], set()).add(f"{sc}/{m}")
    rows = {}
    for sc, n in model.SCENARIOS.items():
        for m in ("fight", "max"):   # max adds the abilities that only make sense with mana ignored
            st = model.Stats(cls, race, ref, "crafted")
            U = model.uses(m)
            model.apply_racials(st, U)
            for a in model.KITS[cls](st, {}, n, U, m).actions:
                r = rows.setdefault(a.name, {"name": a.name, "spell": a.spell, "time": round(a.time, 2), "cost": round(a.cost, 1),
                                             "cap": round(a.cap * 60, 2) if a.cap is not None else None, "used": sorted(used.get(a.name, []))})
                r[sc] = round(a.heal, 1)
    return list(rows.values())


def other_abilities(cls, healing_spells):
    src = (model.LEVELSIM / "classes" / f"{cls}.py").read_text(encoding="utf-8")
    if cls == "priest":
        src += (model.LEVELSIM / "classes" / "mage.py").read_text(encoding="utf-8")
    hsrc = (HERE / "model.py").read_text(encoding="utf-8")
    names = sorted({s["name"] for s in model.core.data()["classes"][cls]["spells"] if 0 < s["base_level"] <= model.LEVEL})
    out = {"healing_support": [], "damage": [], "utility": []}
    for n in names:
        if n in healing_spells:
            continue
        if f'"{n}"' in hsrc:
            out["healing_support"].append(n)
        elif f'"{n}"' in src or f"'{n}'" in src:
            out["damage"].append(n)
        else:
            out["utility"].append(n)
    return out


def stat_weights(cls):
    ref, race = reference(cls)
    base = healing(cls, race, ref)
    out = []
    for key, name, step, unit in STATS:
        model.BONUS.clear()
        model.BONUS[key] = step
        try:
            d = healing(cls, race, ref)
        finally:
            model.BONUS.clear()
        out.append({"key": key, "label": name, "unit": unit,
                    "d": {sc: [round((x - y) / step, 3) for x, y in zip(d[sc], base[sc])] for sc in base}})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--classes", default="")
    ap.add_argument("--dps-iterations", type=int, default=30)     # the same runs as run.py, so the numbers agree
    ap.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    a = ap.parse_args()
    wanted = set(filter(None, a.classes.split(","))) or set(B.BUILDS)
    hsrc = (HERE / "model.py").read_text(encoding="utf-8")
    doc, jobs = {}, []
    for cls in B.BUILDS:
        if cls not in wanted:
            continue
        ref, race = reference(cls)
        trees = json.loads((B.RESEARCH / f"{cls}.json").read_text(encoding="utf-8", errors="replace"))["trees"]
        jobs += [(cls, tr["name"], t, a.dps_iterations) for tr in trees for t in tr["talents"]]
        acts = abilities(cls)
        dsrc = (model.LEVELSIM / "classes" / f"{cls}.py").read_text(encoding="utf-8")
        st = model.solve(cls, race, ref, "crafted", "tank", "fight")
        bdef = next(b for b in B.BUILDS[cls] if b[0] == REFERENCE[cls])
        doc[cls] = {"build": REFERENCE[cls], "build_name": bdef[1], "note": bdef[3], "points": B.points(bdef[4]), "race": race, "base": healing(cls, race, ref), "stats": st["stats"],
                    "armor_buff": {m: model.solve(cls, race, ref, "crafted", "tank", m).get("armor_buff") for m in model.MODES},
                    "dps": model.off_dps(cls, race, ref, "crafted", a.dps_iterations)["dps"] if a.dps_iterations else None,
                    "abilities": acts, "other": other_abilities(cls, {x["spell"] for x in acts}),
                    "weights": stat_weights(cls), "talents": [], "_dsrc": dsrc}
    with ProcessPoolExecutor(a.jobs) as ex:
        for job, res in zip(jobs, ex.map(talent_job, jobs, chunksize=2)):
            c = doc[job[0]]
            name = res["name"]
            res["heal"] = f'"{name}"' in hsrc
            res["dmg"] = f'"{name}"' in c["_dsrc"] or f"'{name}'" in c["_dsrc"]
            c["talents"].append(res)
    for c in doc.values():
        del c["_dsrc"]
    out = {"modes": list(model.MODES), "scenarios": model.SCENARIOS, "fight_seconds": model.FIGHT,
           "assumptions": {k: [v[1], v[2]] for k, v in model.CU_VALUES.items()}, "classes": doc}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1), encoding="utf-8")
    PUBLISHED.write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    for cls, c in doc.items():
        ts = c["talents"]
        print(f"{cls:8} {len(ts)} talents ({sum(t['heal'] for t in ts)} healing, {sum(t['dmg'] for t in ts)} damage, "
              f"{sum(not t['heal'] and not t['dmg'] for t in ts)} neither), {len(c['abilities'])} healing actions, "
              f"{sum(len(v) for v in c['other'].values())} other abilities")
    print(f"wrote {OUT} and {PUBLISHED} ({PUBLISHED.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
