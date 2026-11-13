"""Unit tests: python -m unittest discover -s tools/sim/physical"""
import os
import random
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from engine import (CRIT, DODGE, GLANCE, HIT, MISS, TAGS, Data, Dot, Sim, Swing,  # noqa: E402
                    armor_multiplier, iter_leaves, ppm_chance, rage_from_damage, roll_white,
                    roll_yellow, white_table_shares)
import specs  # noqa: E402

D = Data.load()


def make(cls, race="human", fight=180.0, seed=1):
    sim = Sim(fight, random.Random(seed))
    return sim, cls(sim, D.fresh(), race)


class DataFile(unittest.TestCase):
    def test_every_leaf_is_tagged_with_a_source(self):
        n = 0
        for path, leaf in iter_leaves(D.raw):
            n += 1
            self.assertIsInstance(leaf, list, path)
            self.assertEqual(len(leaf), 3, path)
            self.assertIn(leaf[1], TAGS, path)
            self.assertTrue(isinstance(leaf[2], str) and leaf[2].strip(), path)
        self.assertGreater(n, 150)

    def test_confidence_is_share_of_forever_tags(self):
        d = D.fresh()
        d("buffs", "might")       # F
        d("model", "boss_armor")  # CU
        self.assertAlmostEqual(d.confidence(), 0.5)


class AttackTable(unittest.TestCase):
    def test_white_boundaries(self):
        args = (8, 6.5, 40, 20)  # miss, dodge, glance, crit
        self.assertEqual(roll_white(0, *args), MISS)
        self.assertEqual(roll_white(7.99, *args), MISS)
        self.assertEqual(roll_white(8.0, *args), DODGE)
        self.assertEqual(roll_white(14.49, *args), DODGE)
        self.assertEqual(roll_white(14.5, *args), GLANCE)
        self.assertEqual(roll_white(54.5, *args), CRIT)
        self.assertEqual(roll_white(74.5, *args), HIT)

    def test_white_crit_is_pushed_off_the_table(self):
        s = white_table_shares(27, 6.5, 40, 40)
        self.assertAlmostEqual(s[CRIT], 0.265)
        self.assertAlmostEqual(s[HIT], 0.0)
        self.assertAlmostEqual(sum(s.values()), 1.0)

    def test_white_distribution_matches_shares(self):
        rng = random.Random(3)
        args = (27, 6.5, 40, 20)
        n = 200_000
        counts = {}
        for _ in range(n):
            o = roll_white(rng.random() * 100, *args)
            counts[o] = counts.get(o, 0) + 1
        for k, v in white_table_shares(*args).items():
            self.assertAlmostEqual(counts.get(k, 0) / n, v, delta=0.004, msg=k)

    def test_yellow_is_two_roll(self):
        rng = random.Random(4)
        n = 200_000
        crits = landed = 0
        for _ in range(n):
            o = roll_yellow(rng.random() * 100, rng.random() * 100, 8, 6.5, 30)
            if o in (HIT, CRIT):
                landed += 1
                crits += o == CRIT
        self.assertAlmostEqual(landed / n, 0.855, delta=0.004)
        self.assertAlmostEqual(crits / landed, 0.30, delta=0.004)

    def test_negative_miss_is_clamped(self):
        self.assertEqual(roll_yellow(0.0, 50, -1, 6.5, 0), DODGE)

    def test_armor(self):
        self.assertEqual(armor_multiplier(-500, 5500), 1.0)
        self.assertAlmostEqual(armor_multiplier(5500, 5500), 0.5)

    def test_player_miss_uses_dw_penalty_and_hit(self):
        _, p = make(specs.Fury)
        hit = p.hit
        self.assertAlmostEqual(p.miss_chance("mh", True), max(0, 8 + 19 - hit))
        self.assertAlmostEqual(p.miss_chance("oh", True), max(0, 8 + 19 - hit - 10))
        self.assertAlmostEqual(p.miss_chance("mh", False), max(0, 8 - hit))


class Resources(unittest.TestCase):
    def test_classic_rage(self):
        d = D.fresh()
        d.raw = dict(D.raw, rage=dict(D.raw["rage"], model=["classic", "A", "test"]))
        self.assertAlmostEqual(rage_from_damage(d, 230.6, 3.3, False, False), 7.5)
        self.assertAlmostEqual(rage_from_damage(d, 230.6, 3.3, False, True), 7.5 * 1.75)

    def test_forever_speed_rage(self):
        c = 230.6
        r = rage_from_damage(D, 600, 3.3, False, False)
        self.assertAlmostEqual(r, 3.75 * 600 / c + 3.5 * 3.3 / 2)
        oh = rage_from_damage(D, 600, 2.4, True, False)
        self.assertAlmostEqual(oh, 3.75 * 600 / c + 1.75 * 2.4 / 2)
        self.assertAlmostEqual(rage_from_damage(D, 600, 3.3, False, True), r * 1.75)
        self.assertAlmostEqual(rage_from_damage(D, 10, 3.3, False, False), 15 * 10 / c)  # cap
        self.assertEqual(rage_from_damage(D, 0, 3.3, False, False), 0)

    def test_rage_caps_at_100(self):
        _, p = make(specs.Fury)
        p.gain(150)
        self.assertEqual(p.rage, 100)

    def test_unbridled_wrath_average(self):
        _, p = make(specs.Fury)
        n = 20_000
        for _ in range(n):
            p.rage = 0
            p.on_landed("mh", HIT, "x", True)
            p.totg_ready = 1e9
            p._uw = getattr(p, "_uw", 0) + p.rage
        self.assertAlmostEqual(p._uw / n, 0.60, delta=0.015)

    def test_energy_regen(self):
        sim, p = make(specs.Combat, fight=5.0)
        p.think = lambda: None
        p.swing = lambda hand: None
        p.energy = 0
        sim.run(p)
        # 20 per 2 s with a random first-tick phase: 2 or 3 ticks in 5 s
        self.assertIn(p.energy, (40, 60))
        p.energy = 105
        p._energy_tick()
        self.assertEqual(p.energy, p.max_energy)

    def test_gnome_energy_cap(self):
        _, g = make(specs.Combat, race="gnome")
        _, h = make(specs.Combat, race="human")
        self.assertAlmostEqual(g.max_energy, h.max_energy * 1.05)

    def test_adrenaline_rush_doubles_ticks(self):
        sim, p = make(specs.Combat, fight=2.5)
        p.think = lambda: None
        p.swing = lambda hand: None
        p.energy = 0
        p.buff("adrenaline_rush", 15)
        sim.run(p)
        self.assertIn(p.energy, (40, 80))  # 1 or 2 ticks of 40 instead of 20


class Procs(unittest.TestCase):
    def test_ppm(self):
        self.assertAlmostEqual(ppm_chance(7, 3.3), 0.385)

    def test_seal_of_command_rate(self):
        sim, p = make(specs.Retribution)
        p.setup()
        p.uses_wf_totem = lambda: False
        n = 20_000
        for _ in range(n):
            p.weapon_procs("mh", False)
        procs = sim.counts["Seal of Command"]
        landed_share = 1 - max(0, 8 - p.hit) / 100 - 0.065
        self.assertAlmostEqual(procs / n, 0.385 * landed_share, delta=0.01)

    def test_windfury_totem_rate(self):
        sim, p = make(specs.Arms)
        p.white_attack = lambda *a, **k: sim.counts.__setitem__("wf", sim.counts["wf"] + 1)
        n = 20_000
        for _ in range(n):
            p.weapon_procs("mh", False)
        self.assertAlmostEqual(sim.counts["wf"] / n, 0.20, delta=0.01)
        sim.counts["wf"] = 0
        for _ in range(1000):
            p.weapon_procs("mh", True)  # extra attacks do not chain
            p.weapon_procs("oh", False)
        self.assertEqual(sim.counts["wf"], 0)

    def test_windfury_weapon_two_attacks(self):
        sim, p = make(specs.Enhancement)
        p.white_attack = lambda *a, **k: sim.counts.__setitem__("wf", sim.counts["wf"] + 1)
        n = 20_000
        for _ in range(n):
            p.weapon_procs("mh", False)
        self.assertAlmostEqual(sim.counts["wf"] / n, 0.40, delta=0.02)

    def test_instant_poison_rate(self):
        sim, p = make(specs.Combat)
        p.uses_wf_totem = lambda: False
        p.sword_extra = lambda: 0.0
        n = 20_000
        for _ in range(n):
            p.weapon_procs("mh", False)
        hit = (83 + p.hit) / 100
        self.assertAlmostEqual(sim.counts["Instant Poison"] / n, 0.20 * hit, delta=0.01)

    def test_flurry_charges_and_haste(self):
        sim, p = make(specs.Fury)
        base = p.haste("mh")
        p.on_crit("mh", "Melee")
        self.assertEqual(p.flurry, 3)
        self.assertAlmostEqual(p.haste("mh"), base * 1.3)
        for _ in range(3):
            p.haste("mh", consume=True)
        self.assertEqual(p.flurry, 0)
        self.assertAlmostEqual(p.haste("mh"), base)

    def test_deep_wounds_total(self):
        sim, p = make(specs.Arms, fight=30.0)
        p.think = lambda: None
        p.swing = lambda hand: None
        p.phys_mult = lambda name: 1.0
        avg = p.avg_weapon_dmg("mh")
        sim.at(0.0, p.on_crit, "mh", "Melee")
        sim.run(p)
        self.assertAlmostEqual(sim.dmg["Deep Wounds"], 0.6 * avg, delta=1e-6)

    def test_dot_refresh_keeps_ticking(self):
        sim = Sim(30.0, random.Random(1))

        class P:
            pass
        p = P()
        p.sim = sim
        p.deal = lambda name, amt, school, periodic=False: sim.dmg.__setitem__(name, sim.dmg[name] + amt)
        dot = Dot(p, "x", "physical")
        for i in range(12):
            sim.at(float(i), dot.apply, 10.0, 4, 3.0)
        sim.run(type("S", (), {"start": lambda self: None})())
        # refreshed every second for 12 s, then runs out 12 s after the last refresh: ticks at 3,6,...,21
        self.assertAlmostEqual(sim.dmg["x"], 70.0)

    def test_swing_rescales_on_haste(self):
        sim, p = make(specs.Arms, fight=10.0)
        p.think = lambda: None
        times = []
        p.swing = lambda hand: times.append(sim.t)
        p.mh_swing = Swing(p, "mh", 3.3, p.swing)
        p.swings = [p.mh_swing]
        sim.at(0.0, p.mh_swing.start, 0.0)
        sim.at(1.65, p.buff, "berserking", 60, True)
        p.race = "troll"
        sim.run(type("S", (), {"start": lambda self: None})())
        self.assertAlmostEqual(times[0], 0.0)
        self.assertAlmostEqual(times[1], 1.65 + 1.65 / 1.1)
        self.assertAlmostEqual(times[2] - times[1], 3.3 / 1.1)


class EndToEnd(unittest.TestCase):
    def test_every_spec_runs_and_is_deterministic(self):
        import run
        for spec in specs.SPECS:
            race = D("class_races", spec.cls)[0]
            a = run.simulate(spec.__name__, race, 3, 60.0, 5)
            b = run.simulate(spec.__name__, race, 3, 60.0, 5)
            self.assertEqual(a["dps_mean"], b["dps_mean"], spec.spec)
            self.assertGreater(a["dps_mean"], 100, spec.spec)
            self.assertAlmostEqual(sum(a["breakdown"].values()), a["dps_mean"], delta=1.0)
            self.assertTrue(0 < a["data_confidence"] < 1)


if __name__ == "__main__":
    unittest.main()
