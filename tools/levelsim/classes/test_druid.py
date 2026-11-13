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
        self.assertIn("Maul", m.simulate("feral", RACE, 15, 3, 1)["breakdown"])
        b = m.simulate("feral", RACE, 60, 3, 1)["breakdown"]
        for k in ("Shred", "Rip", "Rake"):
            self.assertIn(k, b)
        self.assertNotIn("Ferocious Bite", m.simulate("feral", RACE, 23, 3, 1)["breakdown"])

    def test_balance_spells(self):
        self.assertNotIn("Starfire", m.simulate("balance", RACE, 19, 3, 1)["breakdown"])
        self.assertIn("Insect Swarm", m.simulate("balance", RACE, 25, 3, 1)["breakdown"])
        self.assertNotIn("Insect Swarm", m.simulate("restoration", RACE, 60, 3, 1)["breakdown"])


if __name__ == "__main__":
    unittest.main()
