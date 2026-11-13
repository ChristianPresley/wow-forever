"""Unit tests for the caster simulator: python -m unittest discover -s tools/sim/casters"""
from __future__ import annotations

import heapq
import json
import random
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from engine import Caster, Data  # noqa: E402
import specs  # noqa: E402
from run import simulate  # noqa: E402

DATA = Data()


class Dummy(Caster):
    """Minimal caster for mechanics tests (mage class tables, no talents)."""
    cls = "mage"
    spec = "Dummy"

    def setup(self):
        self.reg("bolt", "fire", label="Bolt")
        self.reg("dot", "fire", True, "Dot")


def dummy(seed=1, fight=180.0, race="undead"):
    return Dummy(race, DATA, random.Random(seed), fight)


class DataTests(unittest.TestCase):
    def test_every_leaf_is_tagged(self):
        tags = {"F", "FE", "C", "CU", "A"}

        def walk(node, path):
            if isinstance(node, dict):
                for k, v in node.items():
                    if not k.startswith("_"):
                        walk(v, f"{path}.{k}")
            elif isinstance(node, list) and node and isinstance(node[0], (int, float)) and not isinstance(node[0], bool):
                self.assertEqual(len(node), 3, path)
                self.assertIn(node[1], tags, path)
                self.assertTrue(isinstance(node[2], str) and node[2].strip(), path)
        walk(json.loads((HERE / "data.json").read_text(encoding="utf-8")), "")

    def test_confidence_counts_forever_share(self):
        d = Data()
        d.get("spells.shadow_bolt.coef")      # F
        d.get("spells.frostbolt.coef")        # C
        self.assertAlmostEqual(d.confidence(), 0.5)


class HitCritTests(unittest.TestCase):
    def test_hit_and_crit_rates(self):
        s = dummy(7)
        s.hit = 90.0
        s.crit = 20.0
        n, hits, crits = 40000, 0, 0
        for _ in range(n):
            r = s.direct("bolt", 100, 0.0)
            if r is not None:
                hits += 1
                crits += r[0]
        self.assertAlmostEqual(hits / n, 0.90, delta=0.01)
        self.assertAlmostEqual(crits / hits, 0.20, delta=0.01)

    def test_hit_cap(self):
        s = dummy()
        s.hit = 120.0
        self.assertAlmostEqual(s.hit_p("bolt"), 0.99)

    def test_crit_multiplier_and_debuff(self):
        s = dummy()
        s.hit, s.crit, s.sp = 99.0, 100.0, 0.0
        r = None
        while r is None:
            r = s.direct("bolt", 100, 0.0)
        # 100 base x 1.10 Curse of the Elements x 1.5 spell crit
        self.assertAlmostEqual(r[1], 100 * 1.10 * 1.5)

    def test_spell_power_coefficient(self):
        s = dummy()
        s.hit, s.crit, s.sp = 99.0, -100.0, 200.0
        r = None
        while r is None:
            r = s.direct("bolt", 100, 0.5)
        self.assertAlmostEqual(r[1], (100 + 0.5 * 200) * 1.10)


class DotTests(unittest.TestCase):
    def test_ticks_and_total(self):
        s = dummy()
        s.crit = -100.0
        s.apply_dot("dot", 50.0, 6, 3.0, True)
        while s._q:
            t, _q, fn, args = heapq.heappop(s._q)
            s.t = t
            fn(*args)
        self.assertAlmostEqual(s.dmg["Dot"], 6 * 50 * 1.10)
        self.assertAlmostEqual(s.t, 18.0)

    def test_refresh_restarts_and_drops_old_ticks(self):
        s = dummy()
        s.crit = -100.0
        s.apply_dot("dot", 10.0, 4, 2.0, False)
        s.at(3.0, lambda: s.apply_dot("dot", 10.0, 4, 2.0, False))
        while s._q:
            t, _q, fn, args = heapq.heappop(s._q)
            s.t = t
            fn(*args)
        # one tick at 2 s, then the refresh at 3 s gives 4 ticks (5, 7, 9, 11)
        self.assertAlmostEqual(s.dmg["Dot"], 5 * 10 * 1.10)
        self.assertAlmostEqual(s.t, 11.0)

    def test_dot_crit_uses_periodic_multiplier(self):
        lock = specs.Affliction("undead", DATA, random.Random(1))
        self.assertAlmostEqual(lock.crit_mult("corruption", True), 2.0)    # Pandemic 3/3
        self.assertAlmostEqual(lock.crit_mult("shadow_bolt", False), 2.0)  # Ruin 5/5


class ManaTests(unittest.TestCase):
    def test_max_mana_formula(self):
        s = dummy()
        i = s.int
        self.assertAlmostEqual(s.max_mana, 1213 + 20 + 15 * (i - 20))

    def test_five_second_rule(self):
        s = dummy()
        s.mana = 0.0
        s.last_spend = 0.0
        s.t = 1.0
        s._regen_tick()
        self.assertAlmostEqual(s.mana, s.mp2)            # casting: only mp5 sources
        s.t = 7.0
        before = s.mana
        s._regen_tick()
        self.assertAlmostEqual(s.mana - before, s.regen + s.mp2)

    def test_regen_while_casting_talent(self):
        s = specs.Arcane("undead", DATA, random.Random(1))
        s.mana, s.last_spend, s.t = 0.0, 0.0, 1.0
        s._regen_tick()
        self.assertAlmostEqual(s.mana, 0.5 * s.regen + s.mp2)

    def test_life_tap_scales_with_spirit(self):
        lock = specs.Affliction("human", DATA, random.Random(1))
        lock.mana = 0.0
        lock.life_tap()
        self.assertAlmostEqual(lock.mana, (424 + lock.spirit) * 1.2)

    def test_potion_used_on_deficit(self):
        s = dummy()
        s.t = 10.0
        s.mana = s.max_mana - 3000
        s._off_gcd()
        self.assertGreaterEqual(s.mana, s.max_mana - 3000 + 1350)
        self.assertFalse(s.cd_ready("potion"))

    def test_clearcasting_makes_next_spell_free(self):
        s = dummy()
        s.buffs["cc"] = 100.0
        self.assertEqual(s.cost("bolt", 400), 0.0)
        self.assertEqual(s.cost("bolt", 400), 400)


class ProcTests(unittest.TestCase):
    def test_ignite_rolls_and_refreshes(self):
        f = specs.Fire("undead", DATA, random.Random(1))
        f.add_ignite(100.0)
        f.t = 1.0
        f.add_ignite(60.0)   # pool 160, two new ticks at 3 s and 5 s
        while f._q:
            t, _q, fn, args = heapq.heappop(f._q)
            if fn.__name__ != "_ignite_tick":
                continue
            f.t = t
            fn(*args)
        self.assertAlmostEqual(f.dmg["Ignite"], 160.0)
        self.assertAlmostEqual(f.t, 5.0)

    def test_overload_rate(self):
        e = specs.Elemental("tauren", DATA, random.Random(3))
        e.hit, n = 99.0, 20000
        for _ in range(n):
            e.bolt("lightning_bolt", 100, 0.0)
        ratio = e.dmg["Lightning Overload"] / e.dmg["Lightning Bolt"]
        # 30% chance x half damage => overload damage about 15% of bolt damage
        self.assertAlmostEqual(ratio, 0.15, delta=0.01)

    def test_shadow_weaving_caps_at_five(self):
        p = specs.Shadow("undead", DATA, random.Random(1))
        for _ in range(9):
            p.add_weave()
        self.assertEqual(p.weave_n, 5)
        base = (1 + 0.10) * (1 + 0.10)
        self.assertAlmostEqual(p.spec_mult("mind_blast", False), base * 1.10)

    def test_improved_scorch_stacks(self):
        f = specs.Fire("undead", DATA, random.Random(2))
        f.hit = 99.0
        f.mana = 1e9
        for _ in range(7):
            f.cast_scorch()
            f.t = f.busy_until + 0.1
            while f._q and f._q[0][0] <= f.t:
                t, _q, fn, args = heapq.heappop(f._q)
                if fn.__name__ == "ready":
                    continue
                fn(*args)  # resolved at the later f.t; timing does not matter here
        self.assertEqual(f.scorch_stacks, 5)

    def test_nightfall_proc_rate(self):
        lock = specs.Affliction("undead", DATA, random.Random(5))
        n = 50000
        hits = 0
        for _ in range(n):
            lock.buffs.pop("nightfall", None)
            lock.roll_nightfall()
            hits += lock.up("nightfall")
        self.assertAlmostEqual(hits / n, 0.04, delta=0.004)

    def test_eclipse_charges(self):
        b = specs.Balance("tauren", DATA, random.Random(1))
        b.mana = 1e9
        b.cast_wrath()
        while b._q:
            t, _q, fn, args = heapq.heappop(b._q)
            if fn.__name__ == "ready":
                continue
            b.t = t
            fn(*args)
            if b.charges:
                break
        self.assertEqual(b.charges, 2)


class EndToEnd(unittest.TestCase):
    def test_every_pair_runs_and_is_reproducible(self):
        races = DATA.raw["class_races"]
        for cls in specs.SPECS:
            race = races[cls.cls][0]
            a = simulate(cls.spec, race, 5, 60.0, 11)
            b = simulate(cls.spec, race, 5, 60.0, 11)
            self.assertEqual(a["dps_mean"], b["dps_mean"], cls.spec)
            self.assertGreater(a["dps_mean"], 100, cls.spec)
            self.assertAlmostEqual(sum(a["breakdown"].values()), a["dps_mean"], delta=2.0)
            self.assertTrue(0 < a["data_confidence"] <= 1)


if __name__ == "__main__":
    unittest.main()
