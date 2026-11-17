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
    assert "Arcane Blast" in arc
    # Arcane Wrath is known at 60. The client only has its level 25 talent rank, so it can do
    # less damage per second of cast time than Fireball; the rotation casts it only when it pays.
    talents = mage.talents_at("arcane", 60)
    known = mage.MageSim(core.Sim(1), mage.make_character("human", 60, talents), "arcane", 60, talents, {}).sp_
    assert "Arcane Wrath" in known
    assert "Arcane Wrath" not in mage.MageSim(core.Sim(1), mage.make_character("human", 60, mage.talents_at("fire", 60)),
                                               "fire", 60, mage.talents_at("fire", 60), {}).sp_
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


def test_mana_price_plans_within_the_mana():
    # two fillers (strong and costly, weak and cheap), one cooldown spell, and rest
    acts = [(100.0, 50.0, 1.0), (40.0, 10.0, 1.0), (300.0, 60.0, 0.1), (5.0, -8.0, 1.0)]
    price, x = mage.mana_price(acts, 1000.0)
    assert price == 0.0 and abs(sum(x) - 1) < 1e-6 and x[2] == 0.1 and x[0] > 0.89  # mana is free: best damage
    price, x = mage.mana_price(acts, 12.0)
    assert price > 0 and abs(sum(x) - 1) < 1e-6
    assert abs(sum(xi * a[1] for xi, a in zip(x, acts)) - 12.0) < 0.05  # the plan uses exactly the mana
    assert x[2] == 0.1  # the cooldown spell has the best damage per mana and stays in


def test_simulate_reports_the_better_mana_policy():
    core.GEAR.update(mode="none", spec="arcane")
    best = mage.simulate("arcane", "human", 40, 6, 1)
    talents = mage.talents_at("arcane", 40)
    assert best["mana_policy"] in mage.policies_for(talents)
    for mode in mage.policies_for(talents):
        mage.POLICY["mode"] = mode
        try:
            def build(sim):
                mage.MageSim(sim, mage.make_character("human", 40, talents), "arcane", 40, talents, {}).start()
            assert core.run_many(build, 6, 1)["dps_mean"] <= best["dps_mean"] + 1e-9
        finally:
            mage.POLICY["mode"] = "plan"


def _sim(spec, level, race="human"):
    talents = mage.talents_at(spec, level)
    return mage.MageSim(core.Sim(1), mage.make_character(race, level, talents), spec, level, talents, {})


def test_planner_counts_what_a_cast_sets_off():
    # Fingers of Frost: a Frostbolt's value includes the Ice Lance against a Frozen target
    m = _sim("frost", 60)
    bolt, lance = m.ranks_["Frostbolt"][0], m.sp_["Ice Lance"]
    assert m.exp_damage(lance, frozen=True) > 3 * m.exp_damage(lance)
    opt = m.option(bolt)
    assert opt[1] > m.exp_damage(bolt) + 0.1 * m.exp_damage(lance, frozen=True)
    assert opt[2] > m.exec_time(bolt)
    # Arcane Wrath: spell damage from maximum mana, as in the fight
    a = _sim("arcane", 60)
    aw = a.sp_["Arcane Wrath"]
    assert a.exp_damage(aw) > aw.avg_direct + 0.9 * a.max_mana * a.aw_pct / 100 * aw.direct[2]
    assert "Arcane Wrath" in _crafted_dps("arcane", 60, n=3)["breakdown"]
    # a DoT cast back to back is cut short by the next cast
    f = _sim("fire", 30)
    py = f.sp_["Pyroblast"]
    assert f.exp_damage(py) < f.exp_damage(py, spam=False)


def test_scorch_debuff_is_priced():
    f = _sim("fire", 60)
    sc = f.sp_["Scorch"]
    f.plan_rate = 100.0
    start = f.scorch_bonus(sc)
    f.sim.t = f.sim.end - 1.0
    assert start > f.scorch_bonus(sc) > 0
    f.scorch_stacks, f.scorch_end = 5, f.sim.end + 10  # five stacks that outlast the fight
    assert f.scorch_bonus(sc) == 0


def test_a_level_does_not_lower_dps():
    # the three drops this fixed: a level must not cost more than the noise
    core.GEAR.update(mode="none", spec=None)
    for spec, race, lv in (("frost", "human", 54), ("fire", "undead", 31), ("fire", "gnome", 24)):
        a = mage.simulate(spec, race, lv, 30, 1)["dps_mean"]
        b = mage.simulate(spec, race, lv + 1, 30, 1)["dps_mean"]
        assert b > 0.97 * a, (spec, race, lv, a, b)
    core.GEAR.update(mode="crafted", spec="fire")
    try:
        a = mage.simulate("fire", "gnome", 29, 30, 1)["dps_mean"]
        b = mage.simulate("fire", "gnome", 30, 30, 1)["dps_mean"]
    finally:
        core.GEAR.update(mode="none", spec=None)
    assert b > 0.97 * a, (a, b)


def test_improved_fire_blast_can_keep_the_base_cooldown():
    assert mage.policies_for(mage.talents_at("fire", 28)) == mage.POLICIES
    with_talent = mage.policies_for(mage.talents_at("fire", 29))
    assert with_talent == mage.POLICIES + ("plan+basecd",)
    assert mage.policies_for(mage.talents_at("frost", 60)) == mage.POLICIES
    assert mage.policies_for(mage.talents_at("arcane", 60)) == mage.POLICIES + ("plan+nowrath",)
    assert mage.policies_for(mage.talents_at("arcane", 9)) == mage.POLICIES
    # level 29 no longer loses to 28 (orc, no gear: the drop was 3%)
    core.GEAR.update(mode="none", spec=None)
    a = mage.simulate("fire", "orc", 28, 100, 1)
    b = mage.simulate("fire", "orc", 29, 100, 1)
    assert b["dps_mean"] > 0.985 * a["dps_mean"], (a["dps_mean"], b["dps_mean"])
    assert b["mana_policy"] == "plan+basecd" and mage.POLICY["mode"] == "plan"


def test_arcane_can_leave_out_arcane_wrath():
    # without gear near 60 the rotation without Arcane Wrath is the better one; in crafted
    # gear Arcane Wrath stays in
    core.GEAR.update(mode="none", spec=None)
    out = mage.simulate("arcane", "human", 59, 40, 1)
    assert out["mana_policy"] == "plan+nowrath" and "Arcane Wrath" not in out["breakdown"]
    assert "Arcane Wrath" in _crafted_dps("arcane", 60, n=20)["breakdown"]
