"""Run the physical DPS simulator for every spec + race pair.

    python tools/sim/physical/run.py                       # 1000 x 180 s, writes tools/sim/results/physical.json
    python tools/sim/physical/run.py -n 200 --fight 240 --seed 7
    python tools/sim/physical/run.py --only Fury --race orc -n 50 --out -
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import statistics
import sys
import zlib
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from engine import Data, Sim  # noqa: E402
from specs import CLASS_NAMES, SPECS  # noqa: E402

DEFAULT_OUT = os.path.normpath(os.path.join(HERE, "..", "results", "physical.json"))


def pairs(only=None, race=None, data_path=None):
    d = Data.load(data_path)
    out = []
    for spec in SPECS:
        if only and only.lower() not in spec.spec.lower():
            continue
        for r in d("class_races", spec.cls):
            if race and r != race:
                continue
            out.append((spec.__name__, r))
    return out


def simulate(spec_name: str, race: str, iterations: int, fight: float, seed: int, data_path=None):
    spec = next(s for s in SPECS if s.__name__ == spec_name)
    d = Data.load(data_path)
    base = seed * 1_000_003 + zlib.crc32(f"{spec_name}/{race}".encode())
    dps, breakdown = [], {}
    for i in range(iterations):
        sim = Sim(fight, random.Random(base + i))
        player = spec(sim, d, race)
        dps.append(sim.run(player))
        for k, v in sim.dmg.items():
            breakdown[k] = breakdown.get(k, 0.0) + v / fight
    mean = statistics.fmean(dps)
    sd = statistics.stdev(dps) if len(dps) > 1 else 0.0
    half = 1.96 * sd / math.sqrt(len(dps))
    return {
        "class": spec.cls,
        "class_name": CLASS_NAMES[spec.cls],
        "spec": spec.spec,
        "race": race,
        "race_name": d("races", race, "name"),
        "build": spec.build,
        "faction": d("races", race, "faction"),
        "dps_mean": round(mean, 1),
        "dps_sd": round(sd, 1),
        "ci95": [round(mean - half, 1), round(mean + half, 1)],
        "iterations": iterations,
        "fight_seconds": fight,
        "breakdown": {k: round(v / iterations, 1) for k, v in sorted(breakdown.items(), key=lambda kv: -kv[1])},
        "data_confidence": round(d.confidence(), 3),
        "input_tags": d.tag_counts(),
    }


def _job(args):
    return simulate(*args)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-n", "--iterations", type=int, default=1000)
    ap.add_argument("--fight", type=float, default=180.0, help="fight length in seconds")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--only", help="substring of a spec name, e.g. Fury")
    ap.add_argument("--race", help="race id, e.g. orc")
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 1)
    ap.add_argument("--data", help="alternate data.json (for what-if runs)")
    ap.add_argument("--out", default=DEFAULT_OUT, help="output path, or - for stdout")
    a = ap.parse_args(argv)

    jobs = [(s, r, a.iterations, a.fight, a.seed, a.data) for s, r in pairs(a.only, a.race, a.data)]
    if a.jobs > 1 and len(jobs) > 1:
        with Pool(min(a.jobs, len(jobs))) as pool:
            rows = pool.map(_job, jobs)
    else:
        rows = [_job(j) for j in jobs]
    rows.sort(key=lambda x: (x["class"], x["spec"], -x["dps_mean"]))

    for x in rows:
        print(f"{x['class_name']:8} {x['spec']:26} {x['race_name']:22} {x['dps_mean']:8.1f}  sd {x['dps_sd']:6.1f}  "
              f"ci95 {x['ci95'][0]:.0f}-{x['ci95'][1]:.0f}  conf {x['data_confidence']:.2f}", file=sys.stderr)
    text = json.dumps(rows, indent=2)
    if a.out == "-":
        print(text)
    else:
        os.makedirs(os.path.dirname(a.out), exist_ok=True)
        with open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(text + "\n")
    return rows


if __name__ == "__main__":
    main()
