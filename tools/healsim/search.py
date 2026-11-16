"""Search for better talent allocations than the builds in builds.py.

    python tools/healsim/search.py [--classes druid] [--starts 2] [--jobs N]

For every class, scenario and mode it starts from the best builds in builds.py and climbs:
each step tries moving one talent point from any talent to any talent the model reads, keeps
the tree rules (5 points per row, prerequisites, maximum ranks) and takes the move that raises
healing the most. It stops when no move gains more than 0.1%. This is a local search, not an
exhaustive one: it shows how far a listed build is from the nearest better allocation.
Writes tools/healsim/results/search.json. Needs .research/talents (local only).
"""
import argparse
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import builds as B  # noqa: E402
import model  # noqa: E402

OUT = HERE / "results" / "search.json"
_TREES = {}


def trees(cls):
    """talent -> (tree, row, max rank, prerequisites) from the live Forever trees."""
    if cls not in _TREES:
        d = json.loads((B.RESEARCH / f"{cls}.json").read_text(encoding="utf-8", errors="replace"))
        _TREES[cls] = {t["name"]: (tr["name"], t["row"], t["max"], t.get("requires", []))
                       for tr in d["trees"] for t in tr["talents"]}
    return _TREES[cls]


def valid(cls, tal):
    T = trees(cls)
    below = {}
    for name, pts in tal.items():
        tree, row, mx, req = T[name]
        if pts > mx or any(tal.get(r, 0) < T[r][2] for r in req):
            return False
        below.setdefault(tree, {})[row] = below.get(tree, {}).get(row, 0) + pts
    for name in tal:
        tree, row, _, _ = T[name]
        if sum(p for r, p in below[tree].items() if r < row) < 5 * (row - 1):
            return False
    return True


def modelled(cls):
    src = (HERE / "model.py").read_text(encoding="utf-8")
    return [n for n in trees(cls) if f'"{n}"' in src]


def climb(job):
    cls, race, scenario, mode, start_id, start = job
    score = lambda t: model.solve(cls, race, t, "crafted", scenario, mode, iterations=30)["hps"]  # noqa: E731
    tal, best, targets, steps = dict(start), score(start), modelled(cls), []
    T = trees(cls)
    for _ in range(60):
        pick = None
        for src in list(tal):
            for dst in targets:
                if dst == src or tal.get(dst, 0) >= T[dst][2]:
                    continue
                cand = dict(tal)
                cand[src] -= 1
                if not cand[src]:
                    del cand[src]
                cand[dst] = cand.get(dst, 0) + 1
                if not valid(cls, cand):
                    continue
                v = score(cand)
                if v > (pick[0] if pick else best * 1.001):
                    pick = (v, cand, f"{src} -> {dst}")
        if not pick:
            break
        best, tal = pick[0], pick[1]
        steps.append(pick[2])
    points = {}
    for name, pts in tal.items():
        points[T[name][0]] = points.get(T[name][0], 0) + pts
    return {"class": cls, "race": race, "scenario": scenario, "mode": mode, "start": start_id, "start_hps": score(start),
            "hps": best, "moves": steps, "points": points, "talents": dict(sorted(tal.items()))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--classes", default="")
    ap.add_argument("--starts", type=int, default=2)
    ap.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    a = ap.parse_args()
    wanted = set(filter(None, a.classes.split(",")))
    jobs = []
    for cls, bs in B.BUILDS.items():
        if wanted and cls not in wanted:
            continue
        race = B.RACES[cls][0]
        for sc in model.SCENARIOS:
            for m in model.MODES:
                ranked = sorted(bs, key=lambda b: -model.solve(cls, race, B.flat(b[4]), "crafted", sc, m)["hps"])
                jobs += [(cls, race, sc, m, b[0], B.flat(b[4])) for b in ranked[:a.starts]]
    with ProcessPoolExecutor(a.jobs) as ex:
        res = list(ex.map(climb, jobs))
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(res, indent=1), encoding="utf-8")
    seen = {}
    for r in res:
        k = (r["class"], r["scenario"], r["mode"])
        if k not in seen or r["hps"] > seen[k]["hps"]:
            seen[k] = r
    listed = {k: max(r["start_hps"] for r in res if (r["class"], r["scenario"], r["mode"]) == k) for k in seen}
    for k, r in seen.items():
        gain = (r["hps"] / listed[k] - 1) * 100
        print(f"{k[0]:8} {k[1]:5} {k[2]:7} listed {listed[k]:7.1f}  found {r['hps']:7.1f}  +{gain:4.1f}%  "
              f"{'/'.join(str(v) for v in r['points'].values())} from {r['start']} in {len(r['moves'])} moves")


if __name__ == "__main__":
    main()
