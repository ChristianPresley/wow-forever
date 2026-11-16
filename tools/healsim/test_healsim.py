"""Unit tests for the healer model.

    python -m unittest discover -s tools/healsim -p "test_*.py"
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import builds as B  # noqa: E402
import model  # noqa: E402


def talents(cls, bid):
    return B.flat(next(b for b in B.BUILDS[cls] if b[0] == bid)[4])


class LinearProgram(unittest.TestCase):
    def test_known_optimum(self):
        # maximise 3x + 2y with x + y <= 4, x + 3y <= 6, x <= 3  ->  x = 3, y = 1, value 11
        x, obj = model.lp_max([3, 2], [[1, 1], [1, 3], [1, 0]], [4, 6, 3])
        self.assertAlmostEqual(obj, 11)
        self.assertAlmostEqual(x[0], 3)
        self.assertAlmostEqual(x[1], 1)

    def test_zero_budget(self):
        x, obj = model.lp_max([5], [[1]], [0])
        self.assertEqual(obj, 0)


class Builds(unittest.TestCase):
    def test_builds_are_valid(self):
        self.assertEqual(B.validate(), [])

    def test_every_build_has_51_points_and_unique_id(self):
        for cls, bs in B.BUILDS.items():
            self.assertEqual(len({b[0] for b in bs}), len(bs))
            for b in bs:
                self.assertEqual(sum(B.points(b[4]).values()), 51, f"{cls}/{b[0]}")
                self.assertIn(b[2], ("healer", "hybrid"))


class Data(unittest.TestCase):
    def test_low_level_penalty(self):
        r1 = model.trained("priest", "Lesser Heal")[0]            # learned at level 1
        top = model.trained("priest", "Greater Heal")[-1]
        self.assertAlmostEqual(model.coef(r1, model.eff(r1, "direct")), 0.429 * (1 - 0.0375 * 19), places=4)
        self.assertAlmostEqual(model.coef(top, model.eff(top, "direct")), 0.857, places=3)

    def test_every_class_has_ranked_heals(self):
        for cls, name in (("priest", "Flash Heal"), ("paladin", "Holy Light"), ("druid", "Healing Touch"), ("shaman", "Healing Wave")):
            rows = model.trained(cls, name)
            self.assertGreater(len(rows), 5)
            self.assertTrue(all(model.mana_cost(s, 1000) > 0 for s in rows))


class Solve(unittest.TestCase):
    CASES = [("priest", "holy-pom", "human"), ("paladin", "holy-crit", "dwarf"),
             ("druid", "resto-splendor", "tauren"), ("shaman", "resto-deep", "troll")]

    def test_modes_are_ordered(self):
        for cls, bid, race in self.CASES:
            for sc in model.SCENARIOS:
                r = {m: model.solve(cls, race, talents(cls, bid), "crafted", sc, m) for m in model.MODES}
                self.assertGreater(r["max"]["hps"], r["fight"]["hps"], f"{cls} {sc}")
                self.assertGreater(r["fight"]["hps"], r["endless"]["hps"], f"{cls} {sc}")
                self.assertGreater(r["endless"]["hps"], 0)

    def test_time_and_mana_budgets_hold(self):
        for cls, bid, race in self.CASES:
            for sc in model.SCENARIOS:
                o = model.solve(cls, race, talents(cls, bid), "crafted", sc, "fight")
                self.assertLessEqual(sum(x["time"] for x in o["mix"]) + o["rest"], 1.001)
                pool = o["stats"]["mana"]
                self.assertLessEqual(o["mana_spent_ps"] * model.FIGHT, pool + o["mana_regen_ps"] * model.FIGHT + 5)
                e = model.solve(cls, race, talents(cls, bid), "crafted", sc, "endless")
                self.assertLessEqual(e["mana_spent_ps"], e["mana_regen_ps"] + 0.01)
                self.assertIsNone(e["oom_seconds"])

    def test_max_mode_runs_out_of_mana(self):
        for cls, bid, race in self.CASES:
            o = model.solve(cls, race, talents(cls, bid), "crafted", "tank", "max")
            self.assertIsNotNone(o["oom_seconds"])
            self.assertLess(o["oom_seconds"], model.FIGHT)
            self.assertEqual(o["rest"], 0)

    def test_downranking_never_hurts(self):
        for cls, bid, race in self.CASES:
            for m in ("fight", "endless"):
                free = model.solve(cls, race, talents(cls, bid), "crafted", "tank", m)["hps"]
                top = model.solve(cls, race, talents(cls, bid), "crafted", "tank", m, top_only=True)["hps"]
                self.assertGreaterEqual(free, top * 0.98)

    def test_hot_limit_per_target(self):
        o = model.solve("priest", "human", talents("priest", "holy-pom"), "crafted", "tank", "max")
        renew = sum(x["cpm"] for x in o["mix"] if x["name"].startswith("Renew"))
        self.assertLessEqual(renew, 60 / 15 + 0.01)                 # one Renew per 15 s on one target

    def test_group_heals_scale_with_targets(self):
        tank = model.solve("priest", "human", talents("priest", "holy-pom"), "crafted", "tank", "max")["hps"]
        group = model.solve("priest", "human", talents("priest", "holy-pom"), "crafted", "group", "max")["hps"]
        self.assertGreater(group, tank * 1.3)

    def test_gear_and_talents_matter(self):
        geared = model.solve("druid", "nelf", talents("druid", "resto-deep"), "crafted", "tank", "fight")["hps"]
        naked = model.solve("druid", "nelf", talents("druid", "resto-deep"), "none", "tank", "fight")["hps"]
        untalented = model.solve("druid", "nelf", {}, "crafted", "tank", "fight")["hps"]
        self.assertGreater(geared, naked)
        self.assertGreater(geared, untalented)

    def test_deterministic(self):
        a = model.solve("shaman", "orc", talents("shaman", "resto-deep"), "crafted", "group", "fight")
        b = model.solve("shaman", "orc", talents("shaman", "resto-deep"), "crafted", "group", "fight")
        self.assertEqual(a, b)

    def test_talent_only_spells_need_the_talent(self):
        o = model.solve("priest", "human", {}, "crafted", "group", "max")
        names = " ".join(x["name"] for x in o["mix"])
        self.assertNotIn("Prayer of Mending", names)
        self.assertNotIn("Penance", names)


class Coverage(unittest.TestCase):
    def test_results_cover_every_build_race_gear_scenario_and_mode(self):
        import json
        path = Path(__file__).resolve().parent / "results" / "healers.json"
        if not path.exists():
            self.skipTest("run tools/healsim/run.py first")
        rows = json.loads(path.read_text(encoding="utf-8"))
        want = {(c, b[0], r, g) for c, bs in B.BUILDS.items() for b in bs for r in B.RACES[c] for g in ("crafted", "none")}
        self.assertEqual({(r["class"], r["build"], r["race"], r["gear"]) for r in rows}, want)
        for r in rows:
            for sc in model.SCENARIOS:
                for m in model.MODES:
                    self.assertGreater(r["results"][sc][m]["hps"], 0)
                    self.assertTrue(r["results"][sc][m]["mix"])
            self.assertGreater(r["dps"]["dps"], 0)
            self.assertNotIn("error", r["dps"])

    def test_shield_respects_its_cooldown(self):
        t = talents("priest", "holy-pom")                       # no Soul Warding: 4 s cooldown
        st = model.Stats("priest", "human", t, "crafted")
        model.apply_racials(st, model.uses("max"))
        k = model.priest(st, {}, 5, model.uses("max"), "max")
        self.assertAlmostEqual(k.groups["Weakened Soul"], 1 / 4)


class Extras(unittest.TestCase):
    def test_every_stat_has_a_weight_and_none_hurts(self):
        t = talents("druid", "resto-splendor")
        base = model.solve("druid", "nelf", t, "crafted", "tank", "fight")["hps"]
        for key, step in (("healing", 10), ("int", 10), ("spi", 10), ("crit", 1), ("mp5", 5), ("haste", 1), ("mana", 100)):
            model.BONUS[key] = step
            try:
                self.assertGreater(model.solve("druid", "nelf", t, "crafted", "tank", "fight")["hps"], base, key)
            finally:
                model.BONUS.clear()

    def test_lay_on_hands_only_when_mana_is_ignored(self):
        t = talents("paladin", "holy-crit")
        names = lambda m: {x["name"] for x in model.solve("paladin", "human", t, "crafted", "tank", m)["mix"]}  # noqa: E731
        self.assertIn("Lay on Hands", names("max"))
        self.assertNotIn("Lay on Hands", names("fight"))

    def test_self_and_party_only_spells_stay_out_of_tank_healing(self):
        t = talents("priest", "holy-pom")
        for m in model.MODES:
            names = " ".join(x["name"] for x in model.solve("priest", "human", t, "crafted", "tank", m)["mix"])
            self.assertNotIn("Lightwell", names)
            self.assertNotIn("Desperate Prayer", names)

    def test_power_infusion_never_lowers_healing(self):
        t = talents("priest", "disc-pi")
        without = dict(t)
        del without["Power Infusion"]
        for sc in model.SCENARIOS:
            for m in model.MODES:
                self.assertGreaterEqual(model.solve("priest", "human", t, "crafted", sc, m)["hps"],
                                        model.solve("priest", "human", without, "crafted", sc, m)["hps"] - 0.05)

    def test_armor_buff_uptime_is_reported_for_the_tank(self):
        o = model.solve("shaman", "troll", talents("shaman", "resto-deep"), "crafted", "tank", "fight")
        self.assertEqual(o["armor_buff"]["talent"], "Ancestral Healing")
        self.assertTrue(0 < o["armor_buff"]["uptime"] < 1)


class OffDps(unittest.TestCase):
    def test_off_dps_uses_the_build_and_restores_the_module(self):
        import classes.shaman as sh
        before = sh.talents_at
        healer = model.off_dps("shaman", "orc", talents("shaman", "resto-deep"), "crafted", iterations=5)
        hybrid = model.off_dps("shaman", "orc", talents("shaman", "enh-healer"), "crafted", iterations=5)
        self.assertIs(sh.talents_at, before)
        self.assertGreater(healer["dps"], 0)
        self.assertGreater(hybrid["dps"], healer["dps"])


if __name__ == "__main__":
    unittest.main()
