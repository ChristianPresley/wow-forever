"""Coverage checks for the level simulator (see audit.py). Run from tools/levelsim:

    python -m unittest test_audit        # or: python -m pytest test_audit.py

The matrix and ability checks read results/levels*.json, so run `python run.py` first.
"""
import unittest

import audit
import classes  # noqa: F401
import core
import run


class Matrix(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = audit.load_rows()

    def test_expected_matrix_size(self):
        cells = run.expected_cells()
        self.assertEqual(len(cells), 20160)  # 168 spec and race pairs x 2 gear modes x 60 levels
        self.assertEqual(len({c[:2] for c in cells}), 27)
        self.assertEqual(len({(c[0], c[2]) for c in cells}), 56)

    def test_no_cell_is_missing_and_all_deal_damage(self):
        m = audit.matrix(self.rows)
        self.assertEqual(m["missing"], [])
        self.assertEqual(m["not_positive"], [])
        self.assertEqual(m["cells_present"], m["cells_expected"])

    def test_every_damaging_spell_is_accounted_for(self):
        doc = audit.abilities(self.rows)
        loose = [f"{c}: {s['name']}" for c, v in doc.items() for s in v["spells"] if s["status"] == "unaccounted"]
        self.assertEqual(loose, [], "add the spell to a rotation or to audit.EXCLUDED with a reason")

    def test_exclusions_are_current(self):
        """A spell that a rotation now uses must leave the exclusion list."""
        doc = audit.abilities(self.rows)
        for cls, v in doc.items():
            used = {s["name"] for s in v["spells"] if s["status"] == "used"}
            stale = used & set(audit.EXCLUDED.get(cls, {}))
            self.assertEqual(stale, set(), f"{cls}: used spells still listed as excluded")
        for cls, names in audit.EXCLUDED.items():
            for reason in names.values():
                self.assertIn(reason, audit.REASONS)


class Builds(unittest.TestCase):
    def test_every_build_follows_its_tree_at_every_level(self):
        self.assertEqual(audit.build_checks(), [])


class Racials(unittest.TestCase):
    def test_every_race_lists_four_racials_with_a_status(self):
        races = {r for rs in run.CLASS_RACES.values() for r in rs}
        self.assertEqual(set(core.RACIAL_STATUS), races)
        for race, items in core.RACIAL_STATUS.items():
            self.assertEqual(len(items), 4, race)
            for _, status, note in items:
                self.assertIn(status, ("modelled", "partial", "none"))
                self.assertTrue(note)

    def test_human_spirit_and_expansive_mind(self):
        base = core.Character("mage", "human", 60)
        human = core.Character("mage", "human", 60)
        core.apply_passive_racials(human, "human")
        self.assertAlmostEqual(human.spi, base.spi * 1.10)
        plain = core.Character("mage", "gnome", 60)
        gnome = core.Character("mage", "gnome", 60)
        core.apply_passive_racials(gnome, "gnome")
        self.assertAlmostEqual(gnome.mana(), plain.mana() * 1.05)
        self.assertAlmostEqual(gnome.resource_cap(100), 105.0)

    def test_touch_of_the_grave_procs_for_undead_only(self):
        def fight(race):
            ch = core.Character("warrior", race, 60)
            core.apply_passive_racials(ch, race)

            def build(sim):
                for t in range(0, 180, 2):
                    sim.at(float(t), sim.deal, "Melee", 100.0)
                sim.at(1.0, sim.deal, "Pet: melee", 50.0)
            return core.run_many(build, iterations=50, seed=3), ch
        out, ch = fight("undead")
        touch = out["breakdown"].get(core.TOUCH, 0)
        self.assertGreater(touch, 0)
        # at most one proc per 15 s of 5% of health
        self.assertLessEqual(touch, ch.health() * 0.05 / 15 + 1e-6)
        out, _ = fight("orc")
        self.assertNotIn(core.TOUCH, out["breakdown"])


if __name__ == "__main__":
    unittest.main()
