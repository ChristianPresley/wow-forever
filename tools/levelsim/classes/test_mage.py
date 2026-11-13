"""Tests for classes/mage.py. Run: python -m pytest tools/levelsim/classes/test_mage.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from classes import mage  # noqa: E402
import core  # noqa: E402


def test_talent_points_per_level():
    for spec in mage.SPECS:
        assert mage.talents_at(spec, 9) == {}
        for lv in range(10, 61):
            assert sum(mage.talents_at(spec, lv).values()) == lv - 9


def test_level60_builds():
    def split(spec):
        t = mage.talents_at(spec, 60)
        return t
    assert split("fire")["Combustion"] == 1 and split("fire")["Missile Barrage"] == 2
    assert split("arcane")["Arcane Power"] == 1 and split("arcane")["Precision"] == 3
    assert split("frost")["Ice Barrier"] == 1 and split("frost")["Incineration"] == 5


def test_runs_and_deterministic():
    for spec in mage.SPECS:
        for lv in (1, 20, 40, 60):
            a = mage.simulate(spec, "gnome", lv, 5, 7)
            b = mage.simulate(spec, "gnome", lv, 5, 7)
            assert a["dps_mean"] == b["dps_mean"] > 0
            assert a["inputs"]


def test_spells_gated_by_level_and_talent():
    lv1 = mage.simulate("arcane", "human", 1, 3, 1)["breakdown"]
    assert set(lv1) - {"Melee (unarmed)"} == {"Fireball"}
    early = mage.simulate("frost", "human", 15, 3, 1)["breakdown"]
    assert "Ice Lance" not in early and "Arcane Blast" not in early
    fire = mage.simulate("fire", "human", 60, 3, 1)["breakdown"]
    assert "Ignite" in fire and "Pyroblast" in fire
    # Arcane Blast's stacking cost makes it a burst spell: used in a short fight, while
    # the mana-aware rotation drops it for cheaper damage per mana over 180 s
    arc = _dps_at(30, lambda: mage.simulate("arcane", "human", 60, 3, 1)["breakdown"])
    assert "Arcane Blast" in arc and "Arcane Wrath" in arc
    assert "Arcane Wrath" in mage.simulate("arcane", "human", 60, 3, 1)["breakdown"]
    frost = mage.simulate("frost", "human", 60, 3, 1)["breakdown"]
    assert "Ice Lance" in frost


def test_dps_grows_with_level():
    for spec in mage.SPECS:
        d = [mage.simulate(spec, "human", lv, 10, 1)["dps_mean"] for lv in (1, 20, 40, 60)]
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
    # 180 s DPS is lower than 30 s DPS but well above the old ~1/3 collapse
    for spec in mage.SPECS:
        short = _dps_at(30, lambda: mage.simulate(spec, "human", 60, 6, 1)["dps_mean"])
        long_ = _dps_at(180, lambda: mage.simulate(spec, "human", 60, 6, 1)["dps_mean"])
        assert 0.5 * short < long_ < 1.05 * short, (spec, short, long_)


def test_plan_options_downranks_and_rests():
    # (key, damage, seconds, cost, affordable)
    opts = [("r1", 30, 1.5, 15, True), ("r9", 300, 3.0, 300, True)]
    # plenty of mana for the fight: top rank, cast all the time
    key, f, ok, need, lam = mage.plan_options(opts, 10000, 0, 30, 0, 20, 10)
    assert key == "r9" and f == 1.0
    # little mana, long fight, top rank only a bit stronger per mana: cheap rank sustained
    opts2 = [("r1", 30, 1.5, 15, True), ("r9", 45, 1.5, 40, True)]
    key, f, ok, need, lam = mage.plan_options(opts2, 2000, 0, 180, 0, 5, 1)
    assert key == "r1" and f == 1.0 and lam > 0
    # efficient top rank: cast part of the time, rest (melee) the rest
    key, f, ok, need, lam = mage.plan_options(opts, 500, 0, 180, 0, 20, 10)
    assert key == "r9" and 0 < f < 1 and lam > 0


def test_oom_falls_back_to_melee():
    b = _dps_at(180, lambda: mage.simulate("fire", "human", 40, 3, 1)["breakdown"])
    assert b.get("Melee (unarmed)", 0) > 0
    assert mage.simulate("fire", "human", 40, 2, 1)["inputs"]["oom_unarmed_melee"] == "A"


def _crafted_dps(spec, level, fight=None, n=8):
    """Simulate in crafted gear (core.GEAR), then restore naked mode."""
    core.GEAR.update(mode="crafted", spec=spec)
    try:
        return mage.simulate(spec, "human", level, n, 1)
    finally:
        core.GEAR.update(mode="none", spec=None)


def test_crafted_gear_beats_naked_and_rises():
    for spec in mage.SPECS:
        vals = [_crafted_dps(spec, lv)["dps_mean"] for lv in (20, 40, 60)]
        assert vals == sorted(vals), (spec, vals)
        for lv, v in zip((20, 40, 60), vals):
            assert v > mage.simulate(spec, "human", lv, 8, 1)["dps_mean"], (spec, lv)
    out = _crafted_dps(next(iter(mage.SPECS)), 60, n=1)
    assert out["inputs"]["gear"] == "F (crafted items)"
    assert "gear" not in mage.simulate(next(iter(mage.SPECS)), "human", 60, 1, 1)["inputs"]


def test_crafted_wand_replaces_unarmed_melee():
    out = _crafted_dps("fire", 20, n=3)
    assert "Wand" in out["breakdown"] and not any("unarmed" in k for k in out["breakdown"])
    assert "Wand" not in mage.simulate("fire", "human", 20, 3, 1)["breakdown"]
