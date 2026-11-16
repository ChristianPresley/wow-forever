# unslop-prose

The prose linter of the Forever Codex. It checks the writing profile in `DESIGN.md` ("Writing: unslop-prose"), which is a profile of ASD-STE100 Simplified Technical English. Python 3.12, standard library only.

```bash
python tools/unslop_prose/lint.py                  # all of docs/, against the baseline (what CI runs)
python tools/unslop_prose/lint.py --all            # every finding, baseline ignored
python tools/unslop_prose/lint.py --summary        # counts by rule
python tools/unslop_prose/lint.py docs/about/faq.md
python tools/unslop_prose/lint.py --update-baseline
npm run lint:prose
```

## Rules

| Rule | It finds | Write |
|---|---|---|
| `semicolon` | A semicolon that joins 2 sentences | 2 sentences. A colon can introduce a list or an explanation |
| `modal` | *should*, *would*, *could*, *might*, *may* | *can*, *must*, or a direct command. Keep a hedge as a hedge: "It is possible that …" |
| `long-sentence` | More than 25 words in a sentence | 2 sentences, or a list |
| `long-paragraph` | More than 6 sentences in a paragraph | 2 paragraphs, or a list for 3 or more parallel items |
| `word` | A word with a simpler approved word: *utilize*, *obtain*, *in order to*, *prior to* | The approved word: *use*, *get*, *to*, *before* |
| `phrasal` | A phrasal verb with a single-verb form: *find out*, *keep on* | *find*, *continue* |
| `number-word` | A number written as a word | The digit |
| `filler` | Filler and hype that gives no fact: *it is worth noting*, *seamless*, *robust* | Remove it, or state the fact |

A line of items with `·` between them ("A 5/5 · B 3/3 · C 1/1") is a list, not a sentence. A `description:` in the front matter is checked for words, not for length.

## What it reads

- **Reads:** body text, list items, callout bodies, HTML lines with text, table cells with 8 or more words, and the `description:` of the front matter.
- **Skips:** code, inline code, markup, attribute lists, link targets, headings, quoted text, and other front matter.
- **Opt out:** put these 2 comments on their own lines around a block that must stay as written.

```markdown
<!-- unslop-prose: off -->
The quoted rule or the deliberate bad example.
<!-- unslop-prose: on -->
```

## Baseline

`baseline.json` holds the number of accepted findings for each file and rule. The check fails only when a file has more findings of a rule than its baseline. New text must be clean. Old text can be cleaned over time.

After you clean a page, run `--update-baseline` and commit the lower numbers. Do not raise a number to make the check pass.

## What it does not check

A program cannot check these rules of the profile. A reviewer checks them.

- One topic for each sentence, and one topic for each paragraph.
- The active voice.
- Noun clusters of more than 3 nouns.
- One term for one thing on every page.
- Facts.

## Use from a generator

`tools/classes/build.py` calls `check_text()` on the guide data. It stops on `semicolon`, `modal` and `long-sentence`.

```python
from unslop_prose import lint
for line, rule, message in lint.check_text(text):
    ...
```
