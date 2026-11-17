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


def test_drain_soul_is_a_filler_option_that_never_wins():
    # Best case for Drain Soul: all three Soul Siphon effects up, the other fillers with none.
    for mode in ("none", "crafted"):
        for spec in W.SPECS:
            core.GEAR.update(mode=mode, spec=spec)
            try:
                for lv in range(10, 61):
                    w = W.Warlock(core.Sim(1), spec, "human", lv)
                    others = max(w.filler_value(n)[1] for n in ("Shadow Bolt", "Searing Pain", "Incinerate", "Drain Life"))
                    w.dots = {k: {"end": 99.0} for k in ("Corruption", "Siphon Life", "Bane of Agony")}
                    s, v = w.filler_value("Drain Soul")
                    assert s and 0 < v < 0.95 * others, (mode, spec, lv, v, others)
            finally:
                core.GEAR.update(mode="none", spec=None)
    assert "Drain Soul" not in W.simulate("affliction", "human", 60, 5, 1)["breakdown"]


def test_resisted_channel_costs_only_the_global_cooldown():
    class Miss:
        def chance(self, pct):
            return False

        def uniform(self, lo, hi):
            return lo

    sim = core.Sim(1)
    w = W.Warlock(sim, "affliction", "human", 60)
    sim.rng = Miss()
    w.choose = lambda: ("Wrack", w.spell("Wrack"))
    w.act()
    assert w.wrack_until < 0
    assert [t for t, _, fn, _ in sim.q if fn == w.act] == [w.gcd()]


def test_shadow_bolt_value_counts_improved_shadow_bolt():
    core.GEAR.update(mode="crafted", spec="affliction")
    try:
        w = W.Warlock(core.Sim(1), "affliction", "human", 60)
        fresh = w.filler_value("Shadow Bolt")[1]
        w.buffs["isb"] = 100.0  # debuff already up for longer than a new crit would give
        held = w.filler_value("Shadow Bolt")[1] / (1 + 5 * W.TT["Improved Shadow Bolt"])
        assert fresh > held
        w.t_.pop("Improved Shadow Bolt")
        assert abs(w.filler_value("Shadow Bolt")[1] - held) < 1e-6
    finally:
        core.GEAR.update(mode="none", spec=None)


def test_wrack_doubles_tick_speed_and_keeps_the_duration():
    # Blizzard note, 10 November 2026 hotfixes: a 1 s Wrack channel during a 3 s Corruption tick
    # advances that tick by 2 s, the time gained is kept, and the DoT lasts as long as before.
    sim = core.Sim(1)
    w = W.Warlock(sim, "affliction", "human", 60)
    s = w.spell("Corruption")
    w.apply_dot("Corruption", s, core.damage_effect(s), "shadow")
    d = w.dots["Corruption"]
    assert (d["next"], d["end"]) == (3.0, 18.0)
    sim.t = 1.0
    w.wrack_until = 2.0
    w.wrack_speed(0.5)
    assert d["next"] == 2.0
    sim.t = 2.0
    w.wrack_end()
    assert d["next"] == 2.0 and d["end"] == 18.0  # the tick lands 1 s early, the duration is unchanged


def test_corruption_gains_ticks_under_wrack():
    def ticks(wrack):
        sim = core.Sim(1)
        w = W.Warlock(sim, "affliction", "human", 60)
        n = []
        sim.deal = lambda source, amount: n.append(sim.t)
        s = w.spell("Corruption")
        w.apply_dot("Corruption", s, core.damage_effect(s), "shadow")
        if wrack:
            w.wrack_until = 6.0
            w.wrack_speed(0.5)
            sim.at(6.0, w.wrack_end)
        sim.run()
        return n

    assert ticks(False) == [3.0, 6.0, 9.0, 12.0, 15.0, 18.0]
    assert ticks(True) == [1.5, 3.0, 4.5, 6.0, 9.0, 12.0, 15.0, 18.0]


def test_dot_ending_early_in_a_channel_is_recast_first():
    core.GEAR.update(mode="crafted", spec="affliction")
    try:
        sim = core.Sim(1)
        w = W.Warlock(sim, "affliction", "human", 60)
        w.racial = None
        w.cds.update({"Death Coil": 999.0, "Soul Fire": 999.0})
        for name in ("Bane of Agony", "Corruption", "Siphon Life", "Immolate"):
            s = w.spell(name)
            w.apply_dot(name, s, core.damage_effect(s), w.school(s))
        assert w.choose()[0] == "Wrack"
        w.dots["Corruption"]["end"] = 2.0  # under half of the 6 s channel: cut it off and recast
        assert w.choose()[0] == "Corruption"
        w.dots["Corruption"]["end"] = 4.0  # over half: let it run
        assert w.choose()[0] != "Corruption"
    finally:
        core.GEAR.update(mode="none", spec=None)


def test_immolate_is_cast_only_when_it_beats_the_filler():
    core.GEAR.update(mode="crafted", spec="affliction")
    try:
        sim = core.Sim(1)
        w = W.Warlock(sim, "affliction", "human", 50)
        w.racial = None
        w.cds.update({"Death Coil": 999.0, "Soul Fire": 999.0})
        for name in ("Bane of Agony", "Corruption", "Siphon Life"):
            s = w.spell(name)
            w.apply_dot(name, s, core.damage_effect(s), w.school(s))
        assert w.immolate_value() < w.best_filler()[1]  # Wrack with three DoTs to speed up
        assert w.choose()[0] == "Wrack"
        w.t_.pop("Wrack")
        assert w.immolate_value() > w.best_filler()[1]  # Shadow Bolt as filler
        assert w.choose()[0] == "Immolate"
    finally:
        core.GEAR.update(mode="none", spec=None)
    # Destruction needs Immolate for Conflagrate whatever the filler is worth.
    assert "Immolate" in W.simulate("destruction", "human", 60, 5, 1)["breakdown"]


def test_soul_fire_is_cast_only_when_it_beats_the_filler():
    core.GEAR.update(mode="crafted", spec="affliction")
    try:
        w = W.Warlock(core.Sim(1), "affliction", "human", 50)
        w.racial = None
        w.cds["Death Coil"] = 999.0
        for name in ("Bane of Agony", "Corruption", "Siphon Life"):
            s = w.spell(name)
            w.apply_dot(name, s, core.damage_effect(s), w.school(s))
        assert w.ready("Soul Fire") and w.filler_value("Soul Fire")[1] < w.best_filler()[1]
        assert w.choose()[0] == "Wrack"
        w.t_.pop("Wrack")
        assert w.choose()[0] in ("Immolate", "Soul Fire")  # both beat a hard-cast Shadow Bolt
    finally:
        core.GEAR.update(mode="none", spec=None)
