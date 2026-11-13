"""Run the caster simulator for every spec + race pair and write results JSON.

    python tools/sim/casters/run.py                       # 1000 x 180 s, all pairs
    python tools/sim/casters/run.py -n 200 --fight 300 --seed 7
    python tools/sim/casters/run.py --spec Fire --race troll -v --no-write
"""
from __future__ import annotations

import argparse
import json
import math
import random
import statistics
import sys
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from engine import Data  # noqa: E402
from specs import SPECS  # noqa: E402

DEFAULT_OUT = HERE.parent / "results" / "casters.json"
SPEC_BY_NAME = {c.spec: c for c in SPECS}


def simulate(spec_name: str, race: str, iterations: int, fight: float, seed: int) -> dict:
    cls = SPEC_BY_NAME[spec_name]
    data = Data()
    dps, dmg, casts = [], defaultdict(float), defaultdict(float)
    mana_end = 0.0
    for i in range(iterations):
        rng = random.Random(f"{seed}|{cls.cls}|{cls.spec}|{race}|{i}")
        sim = cls(race, data, rng, fight)
        total = sim.run()
        dps.append(total / fight)
        for k, v in sim.dmg.items():
            dmg[k] += v
        for k, v in sim.casts.items():
            casts[k] += v
        mana_end += sim.mana / sim.max_mana
    mean = statistics.fmean(dps)
    sd = statistics.stdev(dps) if len(dps) > 1 else 0.0
    half = 1.96 * sd / math.sqrt(len(dps))
    breakdown = {k: round(v / (iterations * fight), 1) for k, v in sorted(dmg.items(), key=lambda kv: -kv[1])}
    return {
        "class": cls.cls,
        "spec": cls.spec,
        "race": race,
        "race_name": data.raw["races"][race]["name"],
        "build": cls.build,
        "dps_mean": round(mean, 1),
        "dps_sd": round(sd, 1),
        "ci95": [round(mean - half, 1), round(mean + half, 1)],
        "iterations": iterations,
        "fight_seconds": fight,
        "breakdown": breakdown,
        "data_confidence": round(data.confidence(), 3),
        "casts_per_fight": {k: round(v / iterations, 2) for k, v in sorted(casts.items(), key=lambda kv: -kv[1])},
        "mana_left_pct": round(100 * mana_end / iterations, 1),
    }


def _job(args):
    return simulate(*args)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-n", "--iterations", type=int, default=1000)
    ap.add_argument("--fight", type=float, default=180.0, help="fight length in seconds")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--spec", action="append", help="limit to spec name(s), e.g. Fire")
    ap.add_argument("--race", action="append", help="limit to race id(s), e.g. troll")
    ap.add_argument("--jobs", type=int, default=0, help="worker processes (0 = CPU count, 1 = no pool)")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true", help="print breakdown and casts")
    a = ap.parse_args(argv)

    races_by_class = Data().raw["class_races"]
    jobs = []
    for cls in SPECS:
        if a.spec and cls.spec not in a.spec and cls.spec.split(" ")[0] not in a.spec:
            continue
        for race in races_by_class[cls.cls]:
            if a.race and race not in a.race:
                continue
            jobs.append((cls.spec, race, a.iterations, a.fight, a.seed))
    if not jobs:
        ap.error("no spec/race pair matches")

    t0 = time.time()
    if a.jobs == 1 or len(jobs) == 1:
        results = [_job(j) for j in jobs]
    else:
        with ProcessPoolExecutor(max_workers=a.jobs or None) as ex:
            results = list(ex.map(_job, jobs))
    results.sort(key=lambda r: -r["dps_mean"])

    for r in results:
        print(f"{r['class']:8} {r['spec']:20} {r['race_name']:22} {r['dps_mean']:7.1f} "
              f"sd {r['dps_sd']:6.1f}  ci95 {r['ci95'][0]:.1f}-{r['ci95'][1]:.1f}  conf {r['data_confidence']:.2f}")
        if a.verbose:
            for k, v in r["breakdown"].items():
                print(f"      {k:26} {v:8.1f}")
            print("      casts:", ", ".join(f"{k} {v}" for k, v in r["casts_per_fight"].items()))
            print(f"      mana left at end: {r['mana_left_pct']}%")
    print(f"{len(results)} pairs, {a.iterations} x {a.fight:g} s, seed {a.seed}, {time.time() - t0:.1f} s", file=sys.stderr)

    if not a.no_write:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8")
        print(f"wrote {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
