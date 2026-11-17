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
    # Talent spells are known by the right spec. Whether the rotation casts them depends on
    # their damage per mana against the other spells (the mana plan), so check what is known.

    def known(spec, level=60):
        talents = priest.talents_at(spec, level)
        ch = core.Character(priest.CLASS, "human", level, talents)
        core.apply_passive_racials(ch, "human")
        return priest.PriestSim(core.Sim(1), ch, spec, level, talents, {}).S
    assert "Penance" in known("discipline") and "Penance" not in known("shadow")
    assert "Holy Fire" in known("holy") and "Mind Flay" in known("shadow")
    assert "Penance" not in priest.simulate("shadow", "human", 60, 3, 1)["breakdown"]


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


def _sim(spec, level, race="human"):
    talents = priest.talents_at(spec, level)
    ch = core.Character(priest.CLASS, race, level, talents)
    core.apply_passive_racials(ch, race)
    return priest.PriestSim(core.Sim(1), ch, spec, level, talents, {})


def test_starshards_is_night_elf_only():
    assert "Starshards" in _sim("shadow", 10, "nelf").S
    assert "Starshards" not in _sim("shadow", 9, "nelf").S
    assert "Starshards" not in _sim("shadow", 60, "human").S
    out = priest.simulate("holy", "nelf", 20, 3, 1)
    assert "Starshards" in out["breakdown"] and out["inputs"]["race_lock:Starshards"] == "F"
    # the lock is the client's race mask, not a name in the module
    row = core.best_rank("priest", "Starshards", 60)
    assert [r for r in priest.RACE_BIT if priest.race_open(row, r)] == ["nelf"]
    assert not priest.race_open(row, "sho") and priest.race_open(core.best_rank("priest", "Smite", 60), "sho")
    assert priest.race_open(core.best_rank("priest", "Devouring Plague", 60), "human")
    assert "Starshards" not in priest.simulate("holy", "human", 20, 3, 1)["breakdown"]


def test_holy_fire_value_counts_free_holy_nova():
    p = _sim("holy", 60)
    hf = p.S["Holy Fire"]
    opt = p.option(hf)
    assert opt[1] > p.exp_damage(hf) and opt[2] > p.exec_time(hf)
    assert "Holy Fire" in _crafted_dps("holy", 60, n=3)["breakdown"]  # ungeared it seldom pays


def test_inner_focus_goes_to_the_spell_that_gains_most():
    p = _sim("holy", 60)
    p.plan([p.option(r) for rs in p.ranks_.values() for r in rs])
    cands = [p.S[n] for n in ("Shadow Word: Pain", "Devouring Plague", "Shadow Word: Death")]
    p.if_on = True
    pick = p.focus_target(cands)
    assert pick in cands and p.if_on
    assert p.cost_of(pick) == 0
    out = priest.simulate("holy", "human", 60, 3, 1)
    assert out["inputs"]["talent:Inner Focus"] == "F"
    # Discipline keeps the older rule: no Devouring Plague, which only a free cast pays for
    assert "discipline" in priest.FOCUS_FIRST_SPELL
    assert "Devouring Plague" not in priest.simulate("discipline", "human", 60, 3, 1)["breakdown"]


def test_mana_is_kept_for_the_better_spell():
    p = _sim("discipline", 54, "nelf")
    p.plan([p.option(r) for rs in p.ranks_.values() for r in rs])
    swp, stars = p.S["Shadow Word: Pain"], p.S["Starshards"]
    assert p.option(stars)[1] / p.cost_of(stars) > p.option(swp)[1] / p.cost_of(swp)
    p.lam = 1.0
    p.mana = p.cost_of(swp) + 5           # enough for Pain, then nothing left for Starshards
    assert p.held(swp) and not p.held(stars)
    p.mana = p.max_mana
    assert not p.held(swp)
    # a DoT cast near the end of the fight only counts the ticks that still land
    full = p.exp_damage(stars)
    p.sim.t = p.sim.end - 2.0
    assert 0 < p.exp_damage(stars) < 0.5 * full


def test_swing_policy_credits_a_cast_between_swings():
    assert "plan+swing" in priest.POLICIES
    p = _sim("discipline", 40)
    w = p.ch.weapon("mh")[1] / p.haste()
    assert abs(p.swing_overlap(w) - w / 2) < 1e-9 and abs(p.swing_overlap(10 * w) - w / 2) < 1e-9
    assert 0 < p.swing_overlap(w / 2) < w / 2
    swd = p.S["Shadow Word: Death"]
    plain = p.option(swd)[1]
    p.idle = 1.0
    assert p.option(swd)[1] == plain          # the plain plan gives no credit
    priest.POLICY["mode"] = "plan+swing"
    try:
        q = _sim("discipline", 40)
    finally:
        priest.POLICY["mode"] = "plan"
    q.idle = 1.0
    assert abs(q.option(swd)[1] - plain - q.melee_dps() * q.swing_overlap(1.5)) < 1e-6
    smite = q.ranks_["Smite"][0]
    assert q.option(smite)[1] == p.option(smite)[1]   # fillers get none
    out = _crafted_dps("discipline", 36, n=6)
    assert out["mana_policy"] in priest.POLICIES and priest.POLICY["mode"] == "plan"


def test_wand_first_policy_fixes_the_level_38_drop():
    assert "plan+wand" in priest.POLICIES
    # at 38 the gear's Holy spell power makes rank 6 Smite just beat the wand in the plan;
    # wanding between the cooldown spells is the better rotation and the level no longer loses
    a, b = _crafted_dps("discipline", 37, n=30), _crafted_dps("discipline", 38, n=30)
    assert b["dps_mean"] > a["dps_mean"], (a["dps_mean"], b["dps_mean"])
    assert b["mana_policy"] == "plan+wand"
