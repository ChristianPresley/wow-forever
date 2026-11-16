"""Run every healer build for every race and gear set, and publish the wiki data.

    python tools/healsim/run.py [--classes priest,druid] [--dps-iterations 30] [--no-dps] [--jobs N]

Writes tools/healsim/results/healers.json (full detail) and
docs/assets/data/heal-sim.json (compact, read by docs/javascripts/heal-calc.js).
"""
import argparse
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parent.parent
RESULTS = HERE / "results" / "healers.json"
PUBLISHED = ROOT / "docs" / "assets" / "data" / "heal-sim.json"
GEAR_MODES = ("crafted", "none")

import builds as B  # noqa: E402
import model  # noqa: E402


def one(job):
    cls, bid, race, gear, dps_iter, seed = job
    spec = next(b for b in B.BUILDS[cls] if b[0] == bid)[4]
    talents = B.flat(spec)
    res = model.evaluate(cls, race, talents, gear)
    top = {sc: {m: model.solve(cls, race, talents, gear, sc, m, top_only=True)["hps"] for m in model.MODES}
           for sc in model.SCENARIOS}
    dps = model.off_dps(cls, race, talents, gear, dps_iter, seed) if dps_iter else None
    return {"class": cls, "build": bid, "race": race, "gear": gear, "results": res, "top_rank_only": top, "dps": dps}


def compact(rows):
    """Small JSON for the page: names are indexed, each mix entry is [name, casts/min, hps]."""
    names = []

    def ix(n):
        if n not in names:
            names.append(n)
        return names.index(n)

    out = []
    for r in rows:
        first = r["results"]["tank"]["fight"]
        tags = list(first["inputs"].values())
        row = {"class": r["class"], "build": r["build"], "race": r["race"], "gear": r["gear"], "stats": first["stats"],
               "share": round(sum(t == "F" for t in tags) / len(tags), 2), "r": {}, "top": {}}
        for sc, modes in r["results"].items():
            row["r"][sc] = {}
            row["top"][sc] = [r["top_rank_only"][sc][m] for m in model.MODES]
            for m, o in modes.items():
                row["r"][sc][m] = {"hps": o["hps"], "rest": o["rest"], "oom": o["oom_seconds"], "hpm": o["hpm"],
                                   "spend": o["mana_spent_ps"], "regen": o["mana_regen_ps"],
                                   "mix": [[ix(x["name"]), x["cpm"], x["hps"]] for x in o["mix"]],
                                   "src": [[ix(k), v] for k, v in o["breakdown"].items()]}
        if r["dps"]:
            d = r["dps"]
            row["dps"] = {"dps": d["dps"], "rot": d["rotation"], "src": [[ix(k), v] for k, v in d["breakdown"].items()]}
        out.append(row)
    return names, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--classes", default="")
    ap.add_argument("--dps-iterations", type=int, default=30)
    ap.add_argument("--no-dps", action="store_true")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    a = ap.parse_args()
    problems = B.validate()
    if problems:
        sys.exit("invalid builds:\n" + "\n".join(problems))
    wanted = set(filter(None, a.classes.split(",")))
    dps_iter = 0 if a.no_dps else a.dps_iterations
    jobs = [(cls, b[0], race, gear, dps_iter, a.seed)
            for cls, bs in B.BUILDS.items() if not wanted or cls in wanted
            for b in bs for race in B.RACES[cls] for gear in GEAR_MODES]
    if a.jobs > 1:
        with ProcessPoolExecutor(a.jobs) as ex:
            rows = list(ex.map(one, jobs, chunksize=2))
    else:
        rows = [one(j) for j in jobs]
    RESULTS.parent.mkdir(exist_ok=True)
    RESULTS.write_text(json.dumps(rows, separators=(",", ":")), encoding="utf-8")
    names, out = compact(rows)
    doc = {
        "level": model.LEVEL, "fight_seconds": model.FIGHT, "dps_fight_seconds": 180, "dps_iterations": dps_iter,
        "scenarios": model.SCENARIOS, "modes": list(model.MODES), "names": names,
        "builds": [{"class": cls, "id": b[0], "name": b[1], "role": b[2], "note": b[3], "points": B.points(b[4]),
                    "talents": {tree: _merge(order) for tree, order in b[4].items()}}
                   for cls, bs in B.BUILDS.items() if not wanted or cls in wanted for b in bs],
        "gear": {cls: model.gear_set(cls, "crafted") for cls in B.BUILDS if not wanted or cls in wanted},
        "assumptions": {k: [v[1], v[2]] for k, v in model.CU_VALUES.items()},
        "rows": out,
    }
    PUBLISHED.parent.mkdir(parents=True, exist_ok=True)
    PUBLISHED.write_text(json.dumps(doc, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {len(rows)} rows: {RESULTS} and {PUBLISHED} ({PUBLISHED.stat().st_size // 1024} KB)")
    best = {}
    for r in rows:
        if r["gear"] != "crafted":
            continue
        for sc in model.SCENARIOS:
            for m in model.MODES:
                v = r["results"][sc][m]["hps"]
                if v > best.get((sc, m), (0,))[0]:
                    best[(sc, m)] = (v, r["class"], r["build"], r["race"])
    for (sc, m), (v, cls, bid, race) in best.items():
        print(f"best {sc:5} {m:7}: {v:7.1f} HPS  {cls} {bid} ({race})")


def _merge(order):
    out = {}
    for name, pts in order:
        out[name] = out.get(name, 0) + pts
    return out


if __name__ == "__main__":
    main()
