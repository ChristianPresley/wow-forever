"""Compact results/levels.json into docs/assets/data/level-sim.json for the wiki page.

    python tools/levelsim/publish.py
"""
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "results" / "levels.json"
OUT = HERE.parent.parent / "docs" / "assets" / "data" / "level-sim.json"


def main():
    rows = json.loads(SRC.read_text(encoding="utf-8"))
    levels = sorted({r["level"] for r in rows})
    groups = defaultdict(dict)
    meta = {}
    for r in rows:
        k = (r["class"], r["spec"], r["race"])
        groups[k][r["level"]] = r
        meta[k] = r
    out = []
    for k, by in groups.items():
        top = by[max(by)]
        tags = list((top.get("inputs") or {}).values())
        out.append({
            "class": k[0], "spec": k[1], "spec_name": meta[k]["spec_name"], "race": k[2],
            "dps": [round(by[lv]["dps_mean"], 1) if lv in by else None for lv in levels],
            "ci": [round((by[lv]["ci95"][1] - by[lv]["ci95"][0]) / 2, 1) if lv in by else None for lv in levels],
            "breakdown": {a: round(v, 1) for a, v in top["breakdown"].items()},
            "forever_share": round(sum(t == "F" for t in tags) / len(tags), 2) if tags else None,
        })
    it = rows[0].get("iterations") if rows else None
    fight = rows[0].get("fight_seconds") if rows else None
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"levels": levels, "iterations": it, "fight_seconds": fight, "rows": out},
                              separators=(",", ":")), encoding="utf-8")
    print(f"wrote {len(out)} series x {len(levels)} levels to {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
