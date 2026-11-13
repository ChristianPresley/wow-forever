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


class GatingTests(unittest.TestCase):
    def test_seal_of_command_from_talent(self):
        self.assertNotIn("Seal of Command", m.simulate("retribution", RACE, 19, 3, 1)["breakdown"])
        self.assertIn("Seal of Command", m.simulate("retribution", RACE, 25, 3, 1)["breakdown"])
        self.assertNotIn("Seal of Command", m.simulate("holy", RACE, 60, 3, 1)["breakdown"])

    def test_holy_shock_only_holy_from_30(self):
        self.assertNotIn("Holy Shock", m.simulate("holy", RACE, 29, 3, 1)["breakdown"])
        self.assertIn("Holy Shock", m.simulate("holy", RACE, 30, 3, 1)["breakdown"])
        self.assertNotIn("Holy Shock", m.simulate("retribution", RACE, 60, 3, 1)["breakdown"])

    def test_unsealed_wrath_twists_at_40(self):
        self.assertNotIn("Seal of Righteousness", m.simulate("retribution", RACE, 39, 3, 1)["breakdown"])
        self.assertIn("Seal of Righteousness", m.simulate("retribution", RACE, 40, 3, 1)["breakdown"])

    def test_no_judgement_before_4(self):
        self.assertNotIn("Judgement", m.simulate("retribution", RACE, 3, 3, 1)["breakdown"])


class GearTests(unittest.TestCase):
    def test_crafted_beats_naked_and_rises(self):
        for spec in m.SPECS:
            vals = [_crafted(m, spec, "human", lv)["dps_mean"] for lv in (20, 40, 60)]
            self.assertEqual(vals, sorted(vals), (spec, vals))
            self.assertGreater(vals[-1], m.simulate(spec, "human", 60, 10, 1)["dps_mean"] * 1.3, spec)
            self.assertEqual(_crafted(m, spec, "human", 60, 1)["inputs"]["gear"], "F (crafted items)")


if __name__ == "__main__":
    unittest.main()
