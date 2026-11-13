"""Tests for the Hunter level sim. Run: python -m pytest tools/levelsim/classes/test_hunter.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from classes import hunter as H  # noqa: E402


def test_points_per_level():
    for spec in H.SPECS:
        for lv in range(1, 61):
            assert sum(H.talents_at(spec, lv).values()) == max(0, lv - 9)


def test_raid_builds():
    bm = H.talents_at("beast_mastery", 60)
    assert bm["Bestial Wrath"] == 1 and bm["Summon Hawk"] == 1 and bm["Mortal Shots"] == 5
    mm = H.talents_at("marksmanship", 60)
    assert mm["Lone Wolf"] == 1 and mm["Sniper Shot"] == 1 and mm["Deadly Aspects"] == 5 and "Efficiency" not in mm
    sv = H.talents_at("survival", 60)
    assert sv["Lacerating Strikes"] == 1 and sv["Survivalist"] == 4 and sv["Survivalist's Discipline"] == 2


def test_no_ranged_abilities_and_pet_from_10():
    r = H.simulate("beast_mastery", "orc", 9, 5, 1)
    assert r["pet"] is False
    r = H.simulate("beast_mastery", "orc", 30, 5, 1)
    assert r["pet"] is True and "Hawk: dive" in r["breakdown"]
    for k in ("Auto Shot", "Arcane Shot", "Serpent Sting", "Raptor Strike"):
        assert k not in r["breakdown"]
    assert "Hawk: dive" not in H.simulate("beast_mastery", "orc", 24, 5, 1)["breakdown"]


def test_deterministic():
    assert H.simulate("survival", "troll", 45, 5, 7)["dps_mean"] == H.simulate("survival", "troll", 45, 5, 7)["dps_mean"]


def test_dps_grows_with_level():
    for spec in H.SPECS:
        d = [H.simulate(spec, "human", lv, 10, 1)["dps_mean"] for lv in (5, 20, 40, 60)]
        assert d == sorted(d), (spec, d)
