"""Checks tools/levelsim/base_stats.json covers every class/race pair, levels 1-60, never decreasing."""
import json
from pathlib import Path

from run import CLASS_RACES

DATA = json.loads((Path(__file__).resolve().parent / "base_stats.json").read_text(encoding="utf-8"))
KEYS = ("str", "agi", "sta", "int", "spi")


def test_every_pair_has_levels_1_to_60():
    assert "_source" in DATA
    for cls, races in CLASS_RACES.items():
        for race in races:
            rows = DATA[cls][race]
            assert set(rows) == {str(l) for l in range(1, 61)}, (cls, race)
            for row in rows.values():
                assert set(row) == set(KEYS) and all(row[k] > 0 for k in KEYS)


def test_stats_never_decrease():
    for cls, races in CLASS_RACES.items():
        for race in races:
            rows = DATA[cls][race]
            for l in range(2, 61):
                for k in KEYS:
                    assert rows[str(l)][k] >= rows[str(l - 1)][k], (cls, race, l, k)
