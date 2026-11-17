"""Tests for classes/shaman.py. Run: python -m unittest discover -s tools/levelsim/classes -p "test_shaman.py" """
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import core  # noqa: E402
import shaman as m  # noqa: E402


class TalentTests(unittest.TestCase):
    def test_points_per_level(self):
        for spec in m.SPECS:
            for lv in range(1, 61):
                self.assertEqual(sum(m.talents_at(spec, lv).values()), max(0, lv - 9), (spec, lv))

    def test_ranks_within_max(self):
        tt = {}
        import json
        rp = Path(r"C:/repos/wow-forever/.research/talents/shaman.json")
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


RACE = "orc"


class GatingTests(unittest.TestCase):
    def test_enhancement_tools(self):
        b29 = m.simulate("enhancement", RACE, 29, 3, 1)["breakdown"]
        self.assertNotIn("Windfury", b29)
        b60 = m.simulate("enhancement", RACE, 60, 3, 1)["breakdown"]
        for k in ("Windfury", "Stormstrike", "Lightning Bolt", "Searing Totem"):
            self.assertIn(k, b60)
        self.assertNotIn("Stormstrike", m.simulate("enhancement", RACE, 24, 3, 1)["breakdown"])

    def test_overload_only_elemental(self):
        self.assertNotIn("Lightning Overload", m.simulate("elemental", RACE, 30, 3, 1)["breakdown"])
        self.assertIn("Lightning Overload", m.simulate("elemental", RACE, 31, 5, 1)["breakdown"])
        self.assertNotIn("Lightning Overload", m.simulate("restoration", RACE, 60, 3, 1)["breakdown"])

    def test_paid_ranks(self):
        self.assertTrue(m._rank("Lightning Bolt", 60)["costs"])
        self.assertFalse(m._rank("Lightning Bolt", 60, False)["costs"])


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
        for spec in ('elemental', 'restoration', 'enhancement'):
            short = self._at(30, lambda: m.simulate(spec, "orc", 60, 6, 1)["dps_mean"])
            long_ = self._at(180, lambda: m.simulate(spec, "orc", 60, 6, 1)["dps_mean"])
            self.assertTrue(0.4 * short < long_ < 1.05 * short, (spec, short, long_))

    def test_oom_melee_and_downranks(self):
        b = self._at(180, lambda: m.simulate("elemental", "orc", 60, 3, 1)["breakdown"])
        self.assertGreater(b.get("Melee (unarmed)", 0), 0)


if __name__ == "__main__":
    unittest.main()


def _crafted_dps(spec, level, fight=None, n=8):
    """Simulate in crafted gear (core.GEAR), then restore naked mode."""
    core.GEAR.update(mode="crafted", spec=spec)
    try:
        return m.simulate(spec, "orc", level, n, 1)
    finally:
        core.GEAR.update(mode="none", spec=None)


def test_crafted_gear_beats_naked_and_rises():
    for spec in m.SPECS:
        vals = [_crafted_dps(spec, lv)["dps_mean"] for lv in (20, 40, 60)]
        assert vals == sorted(vals), (spec, vals)
        for lv, v in zip((20, 40, 60), vals):
            assert v > m.simulate(spec, "orc", lv, 8, 1)["dps_mean"], (spec, lv)
    out = _crafted_dps(next(iter(m.SPECS)), 60, n=1)
    assert out["inputs"]["gear"] == "F (crafted items)"
    assert "gear" not in m.simulate(next(iter(m.SPECS)), "orc", 60, 1, 1)["inputs"]


def _policy_dps(spec, level, mode, n=6, seed=3):
    m.POLICY["mode"] = mode
    try:
        return core.run_many(lambda sim: m.Fight(sim, spec, "orc", level, {}).start(), n, seed)
    finally:
        m.POLICY["mode"] = "simple"


def test_caster_reports_the_best_rotation_policy():
    for spec, lv in (("elemental", 40), ("restoration", 30)):
        best = m.simulate(spec, "orc", lv, 6, 3)
        assert best["mana_policy"] in m.POLICIES
        assert best["inputs"]["mana_policy_best_of"] == "A"
        each = {mode: _policy_dps(spec, lv, mode)["dps_mean"] for mode in m.POLICIES}
        assert best["dps_mean"] == max(each.values()), (spec, each)
    assert "mana_policy" not in m.simulate("enhancement", "orc", 40, 2, 1)


def test_direct_shock_only_in_shock_policies():
    for mode in ("plan", "simple"):
        b = _policy_dps("elemental", 60, mode)["breakdown"]
        assert "Earth Shock" not in b and "Frost Shock" not in b, (mode, b)
    b = _policy_dps("elemental", 60, "simple+shock", n=10)["breakdown"]
    assert b.get("Earth Shock", 0) > 0, b


def test_frost_shock_when_its_rank_is_newer():
    # level 58: Frost Shock rank 4 (58) beats Earth Shock rank 6 (48); level 60: Earth Shock rank 7
    pick = lambda lv: m.Fight(core.Sim(1), "restoration", "orc", lv, {}).direct_shock()[0]
    assert pick(58) == "Frost Shock"
    assert pick(60) == "Earth Shock"
    assert pick(19) == "Earth Shock"  # Frost Shock is trained at 20
    core.GEAR.update(mode="crafted", spec="elemental")
    try:
        b58 = _policy_dps("elemental", 58, "plan+shock", n=10)["breakdown"]
    finally:
        core.GEAR.update(mode="none", spec=None)
    assert b58.get("Frost Shock", 0) > 0 and "Earth Shock" not in b58, b58
    # Enhancement keeps Earth Shock (Frost Shock tested and not chosen, module docstring)
    assert "Frost Shock" not in m.simulate("enhancement", "orc", 58, 5, 1)["breakdown"]
