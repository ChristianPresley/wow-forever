"""Tests for classes/priest.py. Run: python -m pytest tools/levelsim/classes/test_priest.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from classes import priest  # noqa: E402


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
    assert set(priest.simulate("shadow", "human", 1, 3, 1)["breakdown"]) == {"Smite"}
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
