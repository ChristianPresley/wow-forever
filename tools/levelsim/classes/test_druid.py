"""Tests for classes/druid.py. Run: python -m unittest discover -s tools/levelsim/classes -p "test_druid.py" """
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import core  # noqa: E402
import druid as m  # noqa: E402


class TalentTests(unittest.TestCase):
    def test_points_per_level(self):
        for spec in m.SPECS:
            for lv in range(1, 61):
                self.assertEqual(sum(m.talents_at(spec, lv).values()), max(0, lv - 9), (spec, lv))

    def test_ranks_within_max(self):
        tt = {}
        import json
        rp = Path(r"C:/repos/wow-forever/.research/talents/druid.json")
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


RACE = "nelf"


class GatingTests(unittest.TestCase):
    def test_feral_forms(self):
        self.assertIn("Wrath", m.simulate("feral", RACE, 9, 3, 1)["breakdown"])
        bear = core.run_many(lambda sim: m.Fight(sim, "feral", RACE, 15, {}).start(), 3, 1)
        self.assertIn("Maul", bear["breakdown"])
        b = core.run_many(lambda sim: m.Fight(sim, "feral", RACE, 60, {}).start(), 3, 1)["breakdown"]
        for k in ("Shred", "Rip", "Rake"):
            self.assertIn(k, b)
        self.assertNotIn("Ferocious Bite", m.simulate("feral", RACE, 23, 3, 1)["breakdown"])

    def test_feral_reports_the_better_form_and_builder(self):
        """Levels 10-19: Bear Form or the caster rotation; from 46: Shred or Claw."""
        for lv, knob, value in ((12, "low_form", "caster"), (46, "builder", "Claw")):
            best = m.simulate("feral", RACE, lv, 6, 3)
            first = core.run_many(lambda sim: m.Fight(sim, "feral", RACE, lv, {}).start(), 6, 3)
            self.assertGreaterEqual(best["dps_mean"], first["dps_mean"])
            self.assertEqual(m.FERAL, {"builder": None, "low_form": "bear"})
            if best.get("feral_" + knob) == "Claw":
                self.assertNotIn("Shred", best["breakdown"])
            if best.get("feral_" + knob) == "caster":
                self.assertIn("Wrath", best["breakdown"])

    def test_balance_spells(self):
        self.assertNotIn("Starfire", m.simulate("balance", RACE, 19, 3, 1)["breakdown"])
        self.assertIn("Insect Swarm", m.simulate("balance", RACE, 25, 3, 1)["breakdown"])
        self.assertNotIn("Insect Swarm", m.simulate("restoration", RACE, 60, 3, 1)["breakdown"])


class ManaTests(unittest.TestCase):
    def _at(self, fight, fn):
        old = core.ASSUMPTIONS["fight_seconds"]
        core.ASSUMPTIONS["fight_seconds"] = (fight, old[1], old[2])
        try:
            return fn()
        finally:
            core.ASSUMPTIONS["fight_seconds"] = old

    def test_sustained_long_fight(self):
        # 180 s DPS is lower than 30 s DPS but not the old ~1/3 collapse
        for spec in ('balance', 'restoration'):
            short = self._at(30, lambda: m.simulate(spec, "nelf", 60, 6, 1)["dps_mean"])
            long_ = self._at(180, lambda: m.simulate(spec, "nelf", 60, 6, 1)["dps_mean"])
            self.assertTrue(0.4 * short < long_ < 1.05 * short, (spec, short, long_))

    def test_oom_melee_and_downranks(self):
        b = self._at(180, lambda: m.simulate("balance", "nelf", 60, 3, 1)["breakdown"])
        self.assertGreater(b.get("Melee (unarmed)", 0), 0)


if __name__ == "__main__":
    unittest.main()


def _crafted_dps(spec, level, fight=None, n=8):
    """Simulate in crafted gear (core.GEAR), then restore naked mode."""
    core.GEAR.update(mode="crafted", spec=spec)
    try:
        return m.simulate(spec, "nelf", level, n, 1)
    finally:
        core.GEAR.update(mode="none", spec=None)


def test_crafted_gear_beats_naked_and_rises():
    for spec in m.SPECS:
        vals = [_crafted_dps(spec, lv)["dps_mean"] for lv in (20, 40, 60)]
        assert vals == sorted(vals), (spec, vals)
        for lv, v in zip((20, 40, 60), vals):
            assert v > m.simulate(spec, "nelf", lv, 8, 1)["dps_mean"], (spec, lv)
    out = _crafted_dps(next(iter(m.SPECS)), 60, n=1)
    assert out["inputs"]["gear"] == "F (crafted items)"
    assert "gear" not in m.simulate(next(iter(m.SPECS)), "nelf", 60, 1, 1)["inputs"]


def test_ravage_opens_the_cat_fight_once():
    core.TRACE["on"] = True
    try:
        r = m.simulate("feral", "nelf", 40, 4, 1)
        early = m.simulate("feral", "nelf", 31, 4, 1)
    finally:
        core.TRACE["on"] = False
    assert r["breakdown"].get("Ravage", 0) > 0
    assert abs(r["casts_per_min"]["Ravage"] - 60 / core.A("fight_seconds")) < 0.01  # one per fight
    assert [name for _, name in r["timeline"] if name != "Tiger's Fury"][0] == "Ravage"
    assert r["inputs"]["prowl_opener"] == "A"
    assert "Ravage" not in early["breakdown"]  # trained at 32
    assert "Pounce" not in r["casts_per_min"]  # tested, not chosen (module docstring)


def test_caster_reports_the_better_mana_policy():
    for spec, lv in (("balance", 40), ("restoration", 30)):
        best = m.simulate(spec, "nelf", lv, 6, 3)
        assert best["mana_policy"] in m.POLICIES
        assert best["inputs"]["mana_policy_best_of"] == "A"
        each = {}
        for mode in m.POLICIES:
            m.POLICY["mode"] = mode
            try:
                each[mode] = core.run_many(lambda sim: m.Fight(sim, spec, "nelf", lv, {}).start(), 6, 3)["dps_mean"]
            finally:
                m.POLICY["mode"] = "simple"
        assert best["dps_mean"] == max(each.values()), (spec, each)
    assert "mana_policy" not in m.simulate("feral", "nelf", 40, 2, 1)


def test_table_policy_fixes_the_level_13_drop():
    # in crafted gear the plan may value swings by the attack table; a Feral Tauren at 13
    # then no longer loses 3.4% against 12
    assert 0.9 < core.melee_expect(core.Character(m.CLASS, "tauren", 13, {})) < 1.1
    core.GEAR.update(mode="crafted", spec="feral")
    try:
        a = m.simulate("feral", "tauren", 12, 60, 1)
        b = m.simulate("feral", "tauren", 13, 60, 1)
    finally:
        core.GEAR.update(mode="none", spec=None)
    assert b["dps_mean"] > 0.99 * a["dps_mean"], (a["dps_mean"], b["dps_mean"])
    assert b["mana_policy"] in m.POLICIES + m.TABLE_POLICIES
    assert m.simulate("feral", "tauren", 13, 4, 1)["mana_policy"] in m.POLICIES  # no gear: not tried
