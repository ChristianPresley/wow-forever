"""Combine the simulator results into the file the calculator page reads.

Run after re-running either simulator:
    python tools/sim/publish.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KEEP = ("class", "spec", "race", "race_name", "build", "dps_mean", "dps_sd", "ci95",
        "iterations", "fight_seconds", "breakdown", "data_confidence")


def main():
    rows = []
    for name in ("physical", "casters"):
        for r in json.loads((ROOT / "tools/sim/results" / f"{name}.json").read_text(encoding="utf-8")):
            row = {k: r.get(k) for k in KEEP}
            if not isinstance(row["ci95"], list):
                row["ci95"] = [row["dps_mean"] - row["ci95"], row["dps_mean"] + row["ci95"]]
            rows.append(row)
    rows.sort(key=lambda r: -r["dps_mean"])
    out = ROOT / "docs/assets/data/sim-results.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {len(rows)} rows to {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
