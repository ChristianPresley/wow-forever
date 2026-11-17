"""Tests for classes/paladin.py. Run: python -m unittest discover -s tools/levelsim/classes -p "test_paladin.py" """
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import core  # noqa: E402
import paladin as m  # noqa: E402


def _crafted(mod, spec, race, level, n=10):
    """Simulate in crafted gear, then restore naked mode."""
    core.GEAR.update(mode="crafted", spec=spec)
    try:
        return mod.simulate(spec, race, level, n, 1)
    finally:
        core.GEAR.update(mode="none", spec=None)


class TalentTests(unittest.TestCase):
    def test_points_per_level(self):
        for spec in m.SPECS:
            for lv in range(1, 61):
                self.assertEqual(sum(m.talents_at(spec, lv).values()), max(0, lv - 9), (spec, lv))

    def test_ranks_within_max(self):
        tt = {}
        import json
        rp = Path(r"C:/repos/wow-forever/.research/talents/paladin.json")
        if not rp.exists():
            self.skipTest("research talents not available")
        for tree in json.loads(rp.read_text(encoding="utf-8"))["trees"]:
            for t in tree["talents"]:
                tt[t["name"]] = t["max"]
        for spec in m.SPECS:
            for name, r in m.talents_at(spec, 60).items():
                self.assertIn(name, tt, name)
                self.assertLessEqual(r, tt[name], (spec, name))


class SimTests(unittest.TestCase):
    def test_deterministic(self):
        for spec in m.SPECS:
            a = m.simulate(spec, RACE, 40, 5, 7)
            b = m.simulate(spec, RACE, 40, 5, 7)
            self.assertEqual(a["dps_mean"], b["dps_mean"])
            self.assertIn("inputs", a)

    def test_positive_and_growing(self):
        for spec in m.SPECS:
            d = [m.simulate(spec, RACE, lv, 10, 1)["dps_mean"] for lv in (1, 20, 40, 60)]
            self.assertTrue(all(x > 0 for x in d), (spec, d))
            self.assertLess(d[0], d[-1], (spec, d))
            self.assertLess(d[1], d[-1], (spec, d))

    def test_inputs_tags(self):
        r = m.simulate(list(m.SPECS)[0], RACE, 30, 2, 1)
        for k, v in r["inputs"].items():
            self.assertTrue(v.split()[0] in ("F", "C", "CU", "A"), (k, v))


RACE = "human"


def fight(spec, level, plan, iterations=3, mana=None, gear=None):
    """One seal plan on its own (simulate() reports the best of the plans that apply).
    `mana` replaces the mana pool, `gear` is a core.GEAR mode."""
    def build(sim):
        f = m.Fight(sim, spec, RACE, level, {}, plan)
        if mana:
            f.mana = f.max_mana = mana
        f.start()
    core.GEAR.update(mode=gear or "none", spec=spec if gear else None)
    try:
        return m.core.run_many(build, iterations, 1)
    finally:
        core.GEAR.update(mode="none", spec=None)


def without(talent, spec, level, iterations):
    """Crafted-gear DPS with and without one talent, same seeds (as audit.ablate does)."""
    real = m.talents_at
    full = _crafted(m, spec, RACE, level, iterations)["dps_mean"]
    m.talents_at = lambda s, lv: {k: v for k, v in real(s, lv).items() if k != talent}
    try:
        return full, _crafted(m, spec, RACE, level, iterations)["dps_mean"]
    finally:
        m.talents_at = real


class GatingTests(unittest.TestCase):
    def test_seal_of_command_from_talent(self):
        self.assertNotIn("Seal of Command", fight("retribution", 19, "command")["breakdown"])
        self.assertIn("Seal of Command", fight("retribution", 25, "command")["breakdown"])
        self.assertNotIn("Seal of Command", fight("retribution", 25, "righteousness")["breakdown"])
        self.assertNotIn("Seal of Command", m.simulate("holy", RACE, 60, 3, 1)["breakdown"])

    def test_simulate_reports_the_best_seal_plan(self):
        r = m.simulate("retribution", RACE, 60, 20, 1)
        plans = m.plans_for("retribution", RACE, 60)
        self.assertEqual(set(plans), set(m.PLANS))
        self.assertIn(r["seal_plan"], plans)
        for plan in plans:
            self.assertGreaterEqual(r["dps_mean"], fight("retribution", 60, plan, 20)["dps_mean"])

    def test_hammer_of_wrath_is_cast_in_the_execute_phase(self):
        self.assertIn("Hammer of Wrath", m.simulate("retribution", RACE, 60, 5, 1)["breakdown"])

    def test_holy_shock_only_holy_from_30(self):
        # With mana to spare (Holy Shock is the last spell the mana rule allows).
        rich = 10 ** 6
        self.assertNotIn("Holy Shock", fight("holy", 29, "righteousness", mana=rich)["breakdown"])
        self.assertIn("Holy Shock", fight("holy", 30, "righteousness", mana=rich)["breakdown"])
        self.assertIn("Holy Shock", fight("holy", 60, "righteousness", mana=rich)["breakdown"])
        self.assertNotIn("Holy Shock", fight("retribution", 60, "righteousness", mana=rich)["breakdown"])

    def test_unsealed_wrath_twists_at_40(self):
        # In crafted gear: the naked Retribution Paladin has no mana to spare for the twist.
        self.assertNotIn("Seal of Righteousness", fight("retribution", 39, "command_twist", gear="crafted")["breakdown"])
        self.assertIn("Seal of Righteousness", fight("retribution", 40, "command_twist", gear="crafted")["breakdown"])
        self.assertNotIn("Seal of Righteousness", fight("retribution", 40, "command", gear="crafted")["breakdown"])
        self.assertIn("Seal of Righteousness", fight("retribution", 40, "command_twist", mana=10 ** 6)["breakdown"])

    def test_no_judgement_before_4(self):
        self.assertNotIn("Judgement", m.simulate("retribution", RACE, 3, 3, 1)["breakdown"])


class SealOfFuryTests(unittest.TestCase):
    def test_plan_starts_at_level_10_with_the_unlinked_judgement_ranks(self):
        # Seal ranks 1 and 2 name Judgement of Fury 1311650 and 1311655, which no trainer lists.
        self.assertNotIn("fury", m.plans_for("protection", RACE, 9))
        self.assertIsNone(m.Fight(None, "protection", RACE, 9, {}, "fury").sof)
        self.assertIn("fury", m.plans_for("protection", RACE, 10))
        for level, spell_id in ((10, 1311650), (17, 1311650), (18, 1311655), (25, 1311655), (26, 20183)):
            f = m.Fight(None, "protection", RACE, level, {}, "fury")
            self.assertEqual(f.jof["id"], spell_id, level)
            self.assertIs(f.jof, m._judgement_of(f.sof))
        # Rank 1 (23 + 1.71 per level) stops growing at its maximum level 16.
        at = lambda level: m.Fight(None, "protection", RACE, level, {}, "fury").judge_range("SoF")
        self.assertAlmostEqual(sum(at(12)[:2]) / 2, 23 + 2 * 1.71)
        self.assertEqual(at(17), at(16))
        self.assertIn("Seal of Fury", fight("protection", 12, "fury")["breakdown"])

    def test_fury_plan_uses_the_seal_and_its_judgement(self):
        r = fight("protection", 60, "fury")
        self.assertIn("Seal of Fury", r["breakdown"])
        self.assertIn("Judgement", r["breakdown"])
        self.assertNotIn("Seal of Righteousness", r["breakdown"])
        f = m.Fight(None, "protection", RACE, 60, {}, "fury")
        e = f.jof["effects"][0]  # rank 7 (level 58), two levels of growth
        lo, hi, coef = f.judge_range("SoF")
        self.assertAlmostEqual((lo + hi) / 2, e["EffectBasePointsF"] + 2 * e["EffectRealPointsPerLevel"])
        self.assertEqual(coef, e["EffectBonusCoefficient"])

    def test_plan_runs_only_when_its_hit_is_the_larger_one(self):
        for spec, gear in (("holy", "crafted"), ("retribution", "crafted"), ("retribution", "none")):
            core.GEAR.update(mode=gear, spec=spec)
            try:
                for level in (30, 45, 60):
                    f = m.Fight(None, spec, RACE, level, {}, "fury")
                    self.assertEqual("fury" in m.plans_for(spec, RACE, level), f.fury_hit() > f.sor_hit(), (spec, gear, level))
            finally:
                core.GEAR.update(mode="none", spec=None)

    def test_hammer_of_the_righteous_is_never_cast(self):
        for spec in m.SPECS:
            self.assertNotIn("Hammer of the Righteous", _crafted(m, spec, RACE, 60, 3)["breakdown"])


class ManaTests(unittest.TestCase):
    def test_judgement_of_command_is_the_rank_the_talent_seal_names(self):
        # Seal 20375 -> dummy 20425 -> damage spell 20467 (rank 1), also at level 60.
        for level in (20, 60):
            f = m.Fight(None, "retribution", RACE, level, {}, "command")
            self.assertEqual(f.soc["id"], 20375)
            self.assertEqual(f.joc["id"], 20467)
        self.assertIs(m._judgement_of(f.soc), core.unlinked("paladin", 20467))

    def test_judgement_of_command_follows_the_client_row(self):
        at = lambda level: m.Fight(None, "retribution", RACE, level, {}, "command").judge_range("SoC")
        lo, hi, coef = at(20)
        self.assertAlmostEqual((lo + hi) / 2, 48.5)
        lo, hi, coef = at(28)
        self.assertAlmostEqual((lo + hi) / 2, 70.9)
        self.assertEqual((round(lo), round(hi)), (68, 74))  # tooltip: 136 to 148 stunned, half otherwise
        self.assertEqual(at(60), at(28))
        self.assertEqual(coef, 0.429)

    def test_consecration_comes_from_the_tick_spells(self):
        totals = {}
        for level in (20, 30, 40, 50, 60):
            f = m.Fight(None, "holy", RACE, level, {}, "righteousness")
            base, coef = m.consecration_tick(f.consec)
            self.assertEqual(f.consec_tick, (base, coef))
            self.assertAlmostEqual(coef, 0.042)
            self.assertEqual((f.consec_ticks, f.consec_period, f.consec_cd), (8, 1.0, 8.0))
            totals[level] = base * f.consec_ticks
            # The second effect is the bonus for the first 4 enemies (effect 3 of the rank).
            self.assertEqual([e["EffectBasePointsF"] for e in f.consec["effects"] if e["EffectIndex"] == 2], [4])
        self.assertEqual(totals, {20: 48, 30: 80, 40: 136, 50: 224, 60: 312})
        ids = [int(m.re.search(r"\$(\d+)m1", s["desc"]).group(1)) for s in core.ranks("paladin", "Consecration")]
        self.assertEqual(ids, [1280345, 1280346, 1280347, 1280348, 1280349])
        self.assertEqual(m.simulate("holy", RACE, 30, 2, 1)["inputs"]["consecration_damage"], "F")
        self.assertIsNone(m.Fight(None, "holy", RACE, 19, {}, "righteousness").consec)

    def test_holy_shock_cost_and_damage_follow_the_rank(self):
        self.assertIsNone(m._holy_shock(29))
        seen = {}
        for level in (30, 39, 40, 47, 48, 55, 56, 60):
            cast, dmg = m._holy_shock(level)
            self.assertEqual(cast["base_level"], dmg["base_level"])
            seen[level] = (core.cost(cast, 0)[1], core.damage_effect(dmg)["EffectBasePointsF"])
        self.assertEqual(seen, {30: (160, 134), 39: (160, 134), 40: (225, 182), 47: (225, 182),
                                48: (275, 258), 55: (275, 258), 56: (325, 348), 60: (325, 348)})
        f = m.Fight(None, "holy", RACE, 60, {}, "righteousness")
        self.assertAlmostEqual(f.hshock_cost(), 325 * (1 - f.tv("Benediction") / 100))
        self.assertEqual(f.hshock_cd(), 10.0)
        self.assertFalse(m.Fight(None, "retribution", RACE, 60, {}, "righteousness").hshock)

    def test_optional_spells_are_ranked_by_damage_per_mana(self):
        f = m.Fight(None, "holy", RACE, 60, {}, "righteousness")
        self.assertEqual(set(f.order), {"judgement", "how", "hshock", "consec"})
        self.assertEqual(f.order, sorted(f.order, key=lambda k: -f.per_mana[k]))
        self.assertEqual(f.order[0], "judgement")
        f = m.Fight(None, "retribution", RACE, 60, {}, "command_twist")
        self.assertIn("twist", f.order)
        self.assertGreater(f.judge_net, 0)  # 60% of Seal of Command's 65 mana is less than Judgement costs
        f = m.Fight(None, "retribution", RACE, 60, {}, "righteousness")
        self.assertLessEqual(f.judge_net, 0)  # 60% of Seal of Righteousness returns more than it costs
        self.assertTrue(f.may("judgement", 1.0))

    def test_reserve_keeps_mana_for_the_better_spells(self):
        f = m.Fight(m.core.Sim(1), "holy", RACE, 60, {}, "righteousness")
        r = [f.reserve(k) for k in f.order]
        self.assertEqual(r, sorted(r))
        self.assertGreater(r[-1], r[0])
        f.sim.t = f.sim.end  # nothing left to keep mana for
        self.assertEqual(f.reserve(f.order[-1]), 0.0)

    def test_short_of_mana_holy_shock_is_not_cast(self):
        self.assertNotIn("Holy Shock", _crafted(m, "holy", RACE, 60, 5)["breakdown"])

    def test_no_talent_costs_dps(self):
        # The audit found Holy Shock (-2.4%) and Improved Judgement (-1.2% Holy, -0.7% Protection).
        for spec, talent in (("holy", "Holy Shock"), ("holy", "Improved Judgement"), ("protection", "Improved Judgement")):
            full, less = without(talent, spec, 60, 60)
            self.assertGreaterEqual(full, less * 0.99, (spec, talent, full, less))


class GearTests(unittest.TestCase):
    def test_crafted_beats_naked_and_rises(self):
        for spec in m.SPECS:
            vals = [_crafted(m, spec, "human", lv)["dps_mean"] for lv in (20, 40, 60)]
            self.assertEqual(vals, sorted(vals), (spec, vals))
            self.assertGreater(vals[-1], m.simulate(spec, "human", 60, 10, 1)["dps_mean"] * 1.3, spec)
            self.assertEqual(_crafted(m, spec, "human", 60, 1)["inputs"]["gear"], "F (crafted items)")


if __name__ == "__main__":
    unittest.main()
