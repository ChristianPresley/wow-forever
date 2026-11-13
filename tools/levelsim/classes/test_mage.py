"""Tests for classes/mage.py. Run: python -m pytest tools/levelsim/classes/test_mage.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from classes import mage  # noqa: E402


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
    assert set(lv1) == {"Fireball"}
    early = mage.simulate("frost", "human", 15, 3, 1)["breakdown"]
    assert "Ice Lance" not in early and "Arcane Blast" not in early
    fire = mage.simulate("fire", "human", 60, 3, 1)["breakdown"]
    assert "Ignite" in fire and "Pyroblast" in fire
    arc = mage.simulate("arcane", "human", 60, 3, 1)["breakdown"]
    assert "Arcane Blast" in arc and "Arcane Wrath" in arc
    frost = mage.simulate("frost", "human", 60, 3, 1)["breakdown"]
    assert "Ice Lance" in frost


def test_dps_grows_with_level():
    for spec in mage.SPECS:
        d = [mage.simulate(spec, "human", lv, 10, 1)["dps_mean"] for lv in (1, 20, 40, 60)]
        assert d == sorted(d)
