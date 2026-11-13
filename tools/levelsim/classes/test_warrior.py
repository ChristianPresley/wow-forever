"""Tests for the Warrior level simulator module. Run: python -m pytest tools/levelsim/classes"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import core  # noqa: E402
import warrior as W  # noqa: E402


def _crafted(mod, spec, race, level, n=10):
    """Simulate in crafted gear, then restore naked mode."""
    core.GEAR.update(mode="crafted", spec=spec)
    try:
        return mod.simulate(spec, race, level, n, 1)
    finally:
        core.GEAR.update(mode="none", spec=None)


class TalentTests(unittest.TestCase):
    def test_points_per_level(self):
        for spec in W.SPECS:
            for lv in range(1, 61):
                self.assertEqual(sum(W.talents_at(spec, lv).values()), max(0, lv - 9), (spec, lv))

    def test_ranks_within_tooltip_max(self):
        for spec in W.SPECS:
            for name, r in W.talents_at(spec, 60).items():
                if name in W.TOOLTIP:
                    self.assertLessEqual(r, W.TOOLTIP[name][1], name)

    def test_capstones_at_40(self):
        self.assertEqual(W.talents_at("arms", 40).get("Mortal Strike"), 1)
        self.assertEqual(W.talents_at("fury", 40).get("Bloodthirst"), 1)
        self.assertEqual(W.talents_at("protection", 40).get("Shield Slam"), 1)

    def test_tooltip_overrides_wrong_linear_fallback(self):
        # Client rank 1 of Cruelty already holds 5; linear scaling would give 25.
        v, tag = core.talent_points("warrior", "Cruelty", 5)
        self.assertEqual(tag, "A")
        self.assertNotEqual(v, 5)
        self.assertEqual(W.tal({"Cruelty": 5}, "Cruelty"), 5)
        self.assertEqual(W.tal({"Improved Rend": 3}, "Improved Rend"), 35)
        # Where the client agrees, the tooltip value matches.
        self.assertEqual(core.talent_points("warrior", "Impale", 2)[0], W.tal({"Impale": 2}, "Impale"))


class SimTests(unittest.TestCase):
    def test_deterministic(self):
        a = W.simulate("fury", "orc", 45, 5, 7)
        b = W.simulate("fury", "orc", 45, 5, 7)
        self.assertEqual(a["dps_mean"], b["dps_mean"])

    def test_dps_rises_with_level(self):
        for spec in W.SPECS:
            vals = [W.simulate(spec, "human", lv, 20, 1)["dps_mean"] for lv in (1, 10, 20, 30, 40, 50, 60)]
            self.assertEqual(vals, sorted(vals), (spec, vals))

    def test_level_60_plausible(self):
        for spec, lo, hi in (("arms", 80, 400), ("fury", 80, 400), ("protection", 40, 300)):
            d = W.simulate(spec, "human", 60, 20, 1)["dps_mean"]
            self.assertTrue(lo < d < hi, (spec, d))

    def test_only_known_abilities(self):
        r = W.simulate("arms", "human", 39, 5, 1)
        self.assertNotIn("Mortal Strike", r["breakdown"])
        r = W.simulate("fury", "human", 35, 5, 1)
        self.assertNotIn("Whirlwind", r["breakdown"])
        self.assertNotIn("Bloodthirst", r["breakdown"])
        r = W.simulate("fury", "human", 60, 5, 1)
        self.assertIn("Bloodthirst", r["breakdown"])

    def test_inputs_tagged(self):
        r = W.simulate("arms", "dwarf", 60, 2, 1)
        for k, tag in r["inputs"].items():
            self.assertTrue(tag.split("(")[0] in ("F", "C", "CU", "A"), (k, tag))


class GearTests(unittest.TestCase):
    def test_crafted_beats_naked_and_rises(self):
        for spec in W.SPECS:
            vals = [_crafted(W, spec, "human", lv)["dps_mean"] for lv in (20, 40, 60)]
            self.assertEqual(vals, sorted(vals), (spec, vals))
            self.assertGreater(vals[-1], W.simulate(spec, "human", 60, 10, 1)["dps_mean"] * 1.3, spec)

    def test_fury_dual_wields_in_gear_only(self):
        self.assertIn("Melee (off hand)", _crafted(W, "fury", "human", 60)["breakdown"])
        self.assertNotIn("Melee (off hand)", W.simulate("fury", "human", 60, 5, 1)["breakdown"])
        self.assertNotIn("Melee (off hand)", _crafted(W, "arms", "human", 60)["breakdown"])

    def test_gear_tagged(self):
        r = _crafted(W, "arms", "human", 60, 2)
        self.assertEqual(r["inputs"]["gear"], "F (crafted items)")
        self.assertNotIn("gear", W.simulate("arms", "human", 60, 2, 1)["inputs"])


if __name__ == "__main__":
    unittest.main()
