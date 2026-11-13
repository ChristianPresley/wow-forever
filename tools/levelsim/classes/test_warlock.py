"""Tests for the Warlock level sim. Run: python -m pytest tools/levelsim/classes/test_warlock.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from classes import warlock as W  # noqa: E402
import core  # noqa: E402


def _crafted(mod, spec, race, level, n=10):
    """Simulate in crafted gear, then restore naked mode."""
    core.GEAR.update(mode="crafted", spec=spec)
    try:
        return mod.simulate(spec, race, level, n, 1)
    finally:
        core.GEAR.update(mode="none", spec=None)

RAID = {
    "affliction": {"Improved Life Tap": 2, "Suppression": 5, "Improved Corruption": 5, "Amplify Curse": 1, "Pandemic": 3,
                   "Malevolence": 5, "Nightfall": 2, "Siphon Life": 1, "Soul Siphon": 3, "Shadow Mastery": 5, "Wrack": 1,
                   "Improved Shadow Bolt": 5, "Bane": 5, "Cataclysm": 3, "Ruin": 5},
}


def test_points_per_level():
    for spec in W.SPECS:
        for lv in range(1, 61):
            assert sum(W.talents_at(spec, lv).values()) == max(0, lv - 9)


def test_raid_builds():
    assert W.talents_at("affliction", 60) == RAID["affliction"]
    assert W.talents_at("affliction", 40).get("Wrack") == 1
    assert "Wrack" not in W.talents_at("affliction", 39)
    demo = W.talents_at("demonology", 60)
    assert demo["Demonic Pact"] == 1 and demo["Demonic Sacrifice"] == 1 and demo["Master Demonologist"] == 5
    destro = W.talents_at("destruction", 60)
    assert destro["Incinerate"] == 1 and destro["Shadow and Flame"] == 5 and destro["Unholy Power"] == 4


def test_pets():
    assert W.pet_for("affliction", 1) == ("imp", None)
    assert W.pet_for("affliction", 10) == ("voidwalker", None)
    assert W.pet_for("affliction", 20) == ("succubus", None)
    assert W.pet_for("demonology", 40) == ("imp", "succubus")


def test_deterministic_and_gated():
    a = W.simulate("affliction", "human", 30, 5, 3)
    b = W.simulate("affliction", "human", 30, 5, 3)
    assert a["dps_mean"] == b["dps_mean"]
    assert "Wrack" not in a["breakdown"]
    assert "Wrack" in W.simulate("affliction", "human", 40, 5, 3)["breakdown"]
    assert "Incinerate" not in W.simulate("destruction", "orc", 39, 5, 1)["breakdown"]
    assert all(k in a["inputs"] for k in ("base_stats", "pet"))


def test_dps_grows_with_level():
    for spec in W.SPECS:
        d = [W.simulate(spec, "undead", lv, 10, 1)["dps_mean"] for lv in (5, 20, 40, 60)]
        assert d == sorted(d), (spec, d)


def test_crafted_beats_naked_and_rises():
    # From 30: gear.select fails for casters at 10-20 (see report / gear.py caster layout).
    for spec in W.SPECS:
        vals = [_crafted(W, spec, "human", lv)["dps_mean"] for lv in (30, 45, 60)]
        assert vals == sorted(vals), (spec, vals)
        assert vals[-1] > W.simulate(spec, "human", 60, 10, 1)["dps_mean"] * 1.2, spec
    assert _crafted(W, "affliction", "human", 60, 1)["inputs"]["gear"] == "F (crafted items)"
