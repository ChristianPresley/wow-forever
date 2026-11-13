"""Tests for the Rogue level simulator module. Run: python -m pytest tools/levelsim/classes"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import core  # noqa: E402
import rogue as R  # noqa: E402


def _crafted(mod, spec, race, level, n=10):
    """Simulate in crafted gear, then restore naked mode."""
    core.GEAR.update(mode="crafted", spec=spec)
    try:
        return mod.simulate(spec, race, level, n, 1)
    finally:
        core.GEAR.update(mode="none", spec=None)


class TalentTests(unittest.TestCase):
    def test_points_per_level(self):
        for spec in R.SPECS:
            for lv in range(1, 61):
                self.assertEqual(sum(R.talents_at(spec, lv).values()), max(0, lv - 9), (spec, lv))

    def test_ranks_within_tooltip_max(self):
        for spec in R.SPECS:
            for name, r in R.talents_at(spec, 60).items():
                if name in R.TOOLTIP:
                    self.assertLessEqual(r, R.TOOLTIP[name][1], name)

    def test_capstones(self):
        self.assertEqual(R.talents_at("assassination", 40).get("Mutilate"), 1)
        self.assertNotIn("Mutilate", R.talents_at("assassination", 39))
        self.assertEqual(R.talents_at("combat", 40).get("Adrenaline Rush"), 1)
        self.assertEqual(R.talents_at("subtlety", 40).get("Death Mark"), 1)

    def test_tooltip_overrides_wrong_linear_fallback(self):
        self.assertNotEqual(core.talent_points("rogue", "Malice", 5)[0], 5)
        self.assertEqual(R.tal({"Malice": 5}, "Malice"), 5)
        self.assertEqual(R.tal({"Ruthlessness": 3}, "Ruthlessness"), 60)
        self.assertEqual(R.tal({"Opportunity": 5}, "Opportunity"), 20)


class SimTests(unittest.TestCase):
    def test_deterministic(self):
        a = R.simulate("combat", "human", 45, 5, 3)
        b = R.simulate("combat", "human", 45, 5, 3)
        self.assertEqual(a["dps_mean"], b["dps_mean"])

    def test_dps_rises_with_level(self):
        for spec in R.SPECS:
            vals = [R.simulate(spec, "human", lv, 20, 1)["dps_mean"] for lv in (1, 10, 20, 30, 45, 60)]
            self.assertEqual(vals, sorted(vals), (spec, vals))

    def test_level_60_plausible(self):
        for spec in R.SPECS:
            d = R.simulate(spec, "human", 60, 20, 1)["dps_mean"]
            self.assertTrue(80 < d < 500, (spec, d))

    def test_mutilate_is_castable_spell(self):
        p = R.setup("assassination", "human", 40)
        self.assertTrue(p["ab"]["mut"]["costs"])
        r = R.simulate("assassination", "human", 40, 5, 1)
        self.assertIn("Mutilate", r["breakdown"])
        self.assertIn("Deadly Poison", r["breakdown"])

    def test_only_known_abilities(self):
        r = R.simulate("combat", "human", 19, 5, 1)
        self.assertNotIn("Instant Poison", r["breakdown"])
        self.assertNotIn("Shank", r["breakdown"])
        r = R.simulate("subtlety", "human", 60, 5, 1)
        self.assertIn("Death Mark", r["breakdown"])

    def test_inputs_tagged(self):
        r = R.simulate("subtlety", "orc", 60, 2, 1)
        for k, tag in r["inputs"].items():
            self.assertTrue(tag.split("(")[0] in ("F", "C", "CU", "A"), (k, tag))


class GearTests(unittest.TestCase):
    def test_crafted_beats_naked_and_rises(self):
        for spec in R.SPECS:
            vals = [_crafted(R, spec, "human", lv)["dps_mean"] for lv in (20, 40, 60)]
            self.assertEqual(vals, sorted(vals), (spec, vals))
            self.assertGreater(vals[-1], R.simulate(spec, "human", 60, 10, 1)["dps_mean"] * 1.3, spec)

    def test_weapon_requirements_in_gear(self):
        r = _crafted(R, "assassination", "human", 60)
        self.assertIn("Mutilate", r["breakdown"])
        self.assertIn("Melee (off hand)", r["breakdown"])
        self.assertEqual(r["inputs"]["weapon_requirements"], "C")
        r = _crafted(R, "combat", "human", 60, 3)
        self.assertNotIn("Backstab", r["breakdown"])
        self.assertNotIn("Ambush", r["breakdown"])


if __name__ == "__main__":
    unittest.main()
