"""Tests for classes/priest.py. Run: python -m pytest tools/levelsim/classes/test_priest.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from classes import priest  # noqa: E402
import core  # noqa: E402


def test_talent_points_per_level():
    for spec in priest.SPECS:
        assert priest.talents_at(spec, 9) == {}
        for lv in range(10, 61):
            assert sum(priest.talents_at(spec, lv).values()) == lv - 9


def test_level60_builds():
    assert priest.talents_at("shadow", 60)["Shadowform"] == 1
    assert priest.talents_at("discipline", 60)["Penance"] == 1
    assert priest.talents_at("discipline", 60)["Power in Light"] == 5
    assert priest.talents_at("holy", 60)["Searing Light"] == 2


def test_runs_and_deterministic():
    for spec in priest.SPECS:
        for lv in (1, 20, 40, 60):
            a = priest.simulate(spec, "undead", lv, 5, 3)
            b = priest.simulate(spec, "undead", lv, 5, 3)
            assert a["dps_mean"] == b["dps_mean"] > 0


def test_spells_gated():
    assert set(priest.simulate("shadow", "human", 1, 3, 1)["breakdown"]) - {"Melee (unarmed)"} == {"Smite"}
    b31 = priest.simulate("shadow", "human", 31, 3, 1)["breakdown"]
    assert "Shadow Word: Death" not in b31 and "Mind Flay" in b31
    assert "Shadow Word: Death" in priest.simulate("shadow", "human", 32, 3, 1)["breakdown"]
    assert "Penance" in priest.simulate("discipline", "human", 60, 3, 1)["breakdown"]
    assert "Penance" not in priest.simulate("shadow", "human", 60, 3, 1)["breakdown"]
    assert "Holy Fire" in priest.simulate("holy", "human", 60, 3, 1)["breakdown"]


def test_swd_damagepower():
    assert 190 < priest.damagepower(60) < 193


def test_dps_grows_with_level():
    for spec in priest.SPECS:
        d = [priest.simulate(spec, "human", lv, 10, 1)["dps_mean"] for lv in (1, 20, 40, 60)]
        assert d == sorted(d)


def _dps_at(fight, fn):
    import core
    old = core.ASSUMPTIONS["fight_seconds"]
    core.ASSUMPTIONS["fight_seconds"] = (fight, old[1], old[2])
    try:
        return fn()
    finally:
        core.ASSUMPTIONS["fight_seconds"] = old


def test_mana_sustained_over_long_fight():
    # Shadow keeps most of its burst; Smite specs are mana-bound (naked pool) but no
    # longer collapse below a third, and long-fight DPS still rises with level
    short = _dps_at(30, lambda: priest.simulate("shadow", "human", 60, 6, 1)["dps_mean"])
    long_ = _dps_at(180, lambda: priest.simulate("shadow", "human", 60, 6, 1)["dps_mean"])
    assert 0.5 * short < long_ < short
    for spec in priest.SPECS:
        d = _dps_at(180, lambda: [priest.simulate(spec, "human", lv, 6, 1)["dps_mean"] for lv in (20, 40, 60)])
        assert d == sorted(d), (spec, d)


def test_downranks_known():
    import core
    ch = core.Character("priest", "human", 40, priest.talents_at("shadow", 40))
    p = priest.PriestSim(core.Sim(1), ch, "shadow", 40, priest.talents_at("shadow", 40), {})
    assert len(p.ranks_["Smite"]) > 1 and len(p.ranks_["Mind Flay"]) > 1
    assert all(r.raw["base_level"] <= 40 for rs in p.ranks_.values() for r in rs)


def _crafted_dps(spec, level, fight=None, n=8):
    """Simulate in crafted gear (core.GEAR), then restore naked mode."""
    core.GEAR.update(mode="crafted", spec=spec)
    try:
        return priest.simulate(spec, "human", level, n, 1)
    finally:
        core.GEAR.update(mode="none", spec=None)


def test_crafted_gear_beats_naked_and_rises():
    for spec in priest.SPECS:
        vals = [_crafted_dps(spec, lv)["dps_mean"] for lv in (20, 40, 60)]
        assert vals == sorted(vals), (spec, vals)
        for lv, v in zip((20, 40, 60), vals):
            assert v > priest.simulate(spec, "human", lv, 8, 1)["dps_mean"], (spec, lv)
    out = _crafted_dps(next(iter(priest.SPECS)), 60, n=1)
    assert out["inputs"]["gear"] == "F (crafted items)"
    assert "gear" not in priest.simulate(next(iter(priest.SPECS)), "human", 60, 1, 1)["inputs"]
