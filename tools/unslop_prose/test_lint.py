"""Unit tests for unslop-prose.

    python -m unittest discover -s tools/unslop_prose -p "test_*.py"
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import lint  # noqa: E402


def rules(text):
    return sorted({rule for _line, rule, _msg in lint.check_text(text)})


class Rules(unittest.TestCase):
    def test_clean_text_has_no_findings(self):
        self.assertEqual(rules("Train Frost Nova at level 10. It roots each enemy near you for 8 seconds."), [])

    def test_each_rule_fires(self):
        self.assertEqual(rules("Buy the mount; it is fast."), ["semicolon"])
        self.assertEqual(rules("You should buy the mount."), ["modal"])
        self.assertEqual(rules("You can utilize the mount."), ["word"])
        self.assertEqual(rules("You find out the price in the city."), ["phrasal"])
        self.assertEqual(rules("There are three trainers in the city."), ["number-word"])
        self.assertEqual(rules("The mount is a robust option."), ["filler"])
        self.assertEqual(rules(" ".join(["word"] * 26) + "."), ["long-sentence"])
        self.assertEqual(rules(" ".join(["This is a sentence."] * 7)), ["long-paragraph"])

    def test_sentence_limit_is_25_words(self):
        self.assertEqual(rules(" ".join(["word"] * 25) + "."), [])

    def test_month_may_and_names_are_not_flagged(self):
        self.assertEqual(rules("The patch is due on 5 May 2027."), [])
        self.assertEqual(rules("Go to Three Corners. Equip a two-handed mace."), [])


class Scope(unittest.TestCase):
    def test_code_markup_quotes_and_headings_are_skipped(self):
        self.assertEqual(rules("```\nyou should; utilize\n```"), [])
        self.assertEqual(rules("Run `should; utilize` in the shell."), [])
        self.assertEqual(rules("## You should utilize three things"), [])
        self.assertEqual(rules('The tooltip says "you should utilize three things".'), [])
        self.assertEqual(rules("See the [guide](https://example.com/a;b) first."), [])
        self.assertEqual(rules("Tom &amp; Jerry is a name."), [])

    def test_front_matter_description_is_checked_for_words_not_length(self):
        long_ok = "---\ndescription: " + " ".join(["word"] * 40) + "\ntags:\n  - should\n---\n\nText."
        self.assertEqual(rules(long_ok), [])
        self.assertEqual(rules("---\ndescription: You should read it.\n---\n\nText."), ["modal"])

    def test_lists_of_names_are_not_long_sentences(self):
        self.assertEqual(rules("Discipline (33): " + " · ".join(f"Talent Name {i} 5/5" for i in range(12))), [])
        self.assertEqual(rules(", ".join(f"{i} Bolt of Runecloth" for i in range(1, 9))), [])
        self.assertEqual(rules(" ".join("**Spell Name**{ .pill .pill--new }" for _ in range(14))), [])

    def test_table_cells_with_a_sentence_are_checked(self):
        self.assertEqual(rules("| A | B |\n|---|---|\n| Mount | You should buy this mount when you reach the level 40 trainer. |"), ["modal"])
        self.assertEqual(rules("| A | B |\n|---|---|\n| should | may |"), [])

    def test_off_and_on_comments(self):
        text = "<!-- unslop-prose: off -->\nYou should utilize it.\n<!-- unslop-prose: on -->\n\nYou should stop."
        self.assertEqual([(line, rule) for line, rule, _ in lint.check_text(text)], [(5, "modal")])

    def test_each_list_item_is_its_own_paragraph(self):
        self.assertEqual(rules("\n".join("- This is a sentence." for _ in range(12))), [])


class Wiki(unittest.TestCase):
    def test_the_wiki_is_within_its_baseline(self):
        found = lint.counts(lint.lint_files(sorted(lint.DOCS.rglob("*.md"))))
        import json
        base = json.loads(lint.BASELINE.read_text(encoding="utf-8")) if lint.BASELINE.exists() else {}
        over = {f: r for f, r in found.items() if any(n > base.get(f, {}).get(rule, 0) for rule, n in r.items())}
        self.assertEqual(over, {})


if __name__ == "__main__":
    unittest.main()
