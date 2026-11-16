"""unslop-prose: the prose linter of the Forever Codex.

    python tools/unslop_prose/lint.py                 # lint docs/**/*.md against the baseline (CI)
    python tools/unslop_prose/lint.py --all           # show every finding, baseline ignored
    python tools/unslop_prose/lint.py --summary       # counts by rule
    python tools/unslop_prose/lint.py --update-baseline
    python tools/unslop_prose/lint.py path/to/file.md

unslop-prose is the writing profile in DESIGN.md ("Writing: unslop-prose"), a Codex profile of
ASD-STE100 Simplified Technical English. This file checks the rules that a program can check:

  semicolon       a semicolon joins two sentences
  modal           should, would, could, might, may (use can, must or a command)
  long-sentence   more than 25 words in a sentence
  long-paragraph  more than 6 sentences in a paragraph
  word            a word with a simpler approved word (utilize -> use)
  phrasal         a phrasal verb with a single-verb form (find out -> find)
  number-word     a number written as a word (three -> 3)
  filler          filler and hype that carries no fact ("it is worth noting", "seamless")

It does not check what needs judgement: one topic per sentence, active voice, noun clusters,
one term for one thing. Reviewers still do that.

What it reads: body text, list items, callout bodies, table cells that hold a sentence and the
`description:` of the front matter. What it skips: code, markup, attribute lists, link targets,
headings, quoted text, and text between `<!-- unslop-prose: off -->` and `<!-- unslop-prose: on -->`.

Baseline: tools/unslop_prose/baseline.json holds, for each file and rule, the number of findings
that existed when the rule was adopted. The check fails only when a file has MORE findings of a
rule than its baseline, so old text can be cleaned over time and new text must be clean.
`check_text(text)` is also used by tools/classes/build.py on the guide data.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
BASELINE = Path(__file__).resolve().parent / "baseline.json"
MAX_SENTENCE, MAX_PARAGRAPH = 25, 6

MODAL = re.compile(r"\b(should|would|could|might|may)\b")
WORDS = {   # not approved -> approved
    r"utili[sz]e[sd]?|utili[sz]ing": "use", r"commenc(e|es|ed|ing)": "start", r"obtain(s|ed|ing)?": "get",
    r"approximately": "about", r"in excess of": "more than", r"(is|are|was|were) able to": "can",
    r"in order to": "to", r"prior to": "before", r"subsequently": "then", r"additionally": "also",
    r"furthermore|moreover": "also", r"numerous": "many", r"leverag(e|es|ed|ing)": "use",
    r"facilitat(e|es|ed|ing)": "help", r"in the event that": "if", r"due to the fact that": "because",
    r"a number of": "some", r"at this point in time": "now", r"with regard to|with regards to": "about",
}
PHRASAL = {r"find(s|ing)? out|found out": "find", r"head(s|ed|ing)? off": "leave", r"keep(s|ing)? on|kept on": "continue",
           r"figur(e|es|ed|ing) out": "find", r"end(s|ed|ing)? up": "become / finish"}
NUMBERS = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
           "eleven": 11, "twelve": 12, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "hundred": 100}
FILLER = [
    r"it(?:'s| is) worth (?:noting|mentioning)", r"needless to say", r"as you can see", r"in conclusion", r"a testament to",
    r"plays? a (?:crucial|key|vital|pivotal) role", r"game[- ]changer", r"seamless(?:ly)?", r"\brobust\b", r"\bdelv(?:e|es|ed|ing)\b",
    r"look no further", r"dive (?:deep )?into", r"simply put", r"at the end of the day", r"when it comes to", r"rest assured",
    r"\bbasically\b", r"\bessentially\b", r"\bincredibly\b", r"\bextremely\b", r"\btruly\b", r"cutting[- ]edge", r"state[- ]of[- ]the[- ]art",
]
_WORDS = [(re.compile(r"\b(" + k + r")\b", re.I), v) for k, v in WORDS.items()]
_PHRASAL = [(re.compile(r"\b(" + k + r")\b", re.I), v) for k, v in PHRASAL.items()]
_NUMBER = re.compile(r"(?<![-\w])(" + "|".join(NUMBERS) + r")(?![-\w])")
_FILLER = [re.compile(p, re.I) for p in FILLER]
_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"“(\[0-9])")


def plain(text):
    """Markdown and HTML markup removed; the words that a reader sees stay."""
    t = re.sub(r"<!--.*?-->", "", text)
    t = re.sub(r"\{[:#.][^{}]*\}|\{\s*\.[^{}]*\}", "", t)        # attribute lists
    t = re.sub(r"`[^`]*`", "code", t)                             # inline code is a name
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", t)             # links: keep the text
    t = re.sub(r"<[^>]+>", "", t)                                 # html tags
    t = re.sub(r":[a-z0-9-]+:", "", t)                            # icon shortcodes
    t = re.sub(r"&[a-z#0-9]+;", " ", t)                           # entities (so "&amp;" is not a semicolon)
    t = re.sub(r"\"[^\"]*\"|“[^”]*”", "quote", t)                 # quoted titles and quoted speech are not ours to change
    return t.replace("*", "").replace("_", " ")


def check_line(line, length=True):
    """Findings in one line of prose: [(rule, message)]. Sentence length is checked here too."""
    out = []
    if ";" in line:
        out.append(("semicolon", "a semicolon joins two sentences: write two sentences"))
    for m in MODAL.finditer(line):
        out.append(("modal", f"'{m.group(1)}': write can, must or a direct command"))
    for rx, good in _WORDS:
        for m in rx.finditer(line):
            out.append(("word", f"'{m.group(1)}': write '{good}'"))
    for rx, good in _PHRASAL:
        for m in rx.finditer(line):
            out.append(("phrasal", f"'{m.group(1)}': write '{good}'"))
    for m in _NUMBER.finditer(line):
        out.append(("number-word", f"'{m.group(1)}': write {NUMBERS[m.group(1)]}"))
    for rx in _FILLER:
        for m in rx.finditer(line):
            out.append(("filler", f"'{m.group(0)}': remove it or state the fact"))
    for sent in _SPLIT.split(line):
        n = len(sent.split())
        if sent.count("·") >= 2 or not length:      # "A 5/5 · B 3/3 · C 1/1" is a list on one line, not a sentence
            continue
        commas = sent.count(",")
        if commas >= 4 and n / (commas + 1) <= 4.5:  # "12 Bolt of Runecloth, 8 Essence of Fire, …": a list of names
            continue
        if n > MAX_SENTENCE:
            out.append(("long-sentence", f"{n} words (maximum {MAX_SENTENCE}): '{sent[:60]}…'"))
    return out


def check_text(text):
    """Findings in a block of Markdown: [(line number, rule, message)]."""
    out, fenced, off, para, para_line = [], False, False, 0, 0
    lines = str(text).splitlines()
    in_front = bool(lines) and lines[0].strip() == "---"
    for no, raw in enumerate(lines, 1):
        s = raw.strip()
        if in_front:                                   # front matter: only the description is prose
            if no > 1 and s == "---":
                in_front = False
            elif s.startswith("description:"):
                # a search-result summary: the word rules apply, the sentence length does not
                out += [(no, r, m) for r, m in check_line(plain(s.split(":", 1)[1].strip().strip('"')), length=False)]
            continue
        if "unslop-prose: off" in s:
            off = True
        if "unslop-prose: on" in s:
            off = False
            continue
        if s.startswith("```") or s.startswith("~~~"):
            fenced = not fenced
            continue
        if fenced or off:
            continue
        if not s or s.startswith(("#", "!!!", "???", "===", "---", "<!--", "{", "<div", "</div", "<aside", "</aside", "<details", "</details", "<script", "<style")):
            para = 0
            continue
        if s.startswith("|"):                           # a table cell is prose only when it holds a sentence
            if re.fullmatch(r"[|:\- ]+", s):
                continue
            for cell in s.strip("|").split("|"):
                c = plain(cell).strip()
                if len(c.split()) >= 8:
                    out += [(no, r, m) for r, m in check_line(c)]
            para = 0
            continue
        line = plain(raw).strip()
        if not line:
            continue
        pills = raw.count(".pill") >= 3                 # a row of pills is a list of names, not a sentence
        if s.startswith("<"):                           # an HTML line is its own block: check its words, do not count a paragraph
            out += [(no, r, m) for r, m in check_line(line, length=not pills)]
            para = 0
            continue
        is_item = bool(re.match(r"^([-*+]|\d+\.)\s+", line))
        line = re.sub(r"^([-*+]|\d+\.)\s+", "", line)
        out += [(no, r, m) for r, m in check_line(line, length=not pills)]
        if is_item:
            para = 0
            continue
        if not para:
            para_line = no
        para += len([x for x in _SPLIT.split(line) if len(x.split()) > 2])
        if para > MAX_PARAGRAPH:
            out.append((para_line, "long-paragraph", f"more than {MAX_PARAGRAPH} sentences in one paragraph: split it or use a list"))
            para = -10 ** 6                             # report a paragraph once
    return out


def lint_files(paths):
    found = {}
    for p in paths:
        full = p.resolve()
        rel = full.relative_to(ROOT).as_posix() if full.is_relative_to(ROOT) else full.as_posix()
        hits = check_text(p.read_text(encoding="utf-8"))
        if hits:
            found[rel] = hits
    return found


def counts(found):
    out = {}
    for rel, hits in found.items():
        for _, rule, _ in hits:
            out.setdefault(rel, {}).setdefault(rule, 0)
            out[rel][rule] += 1
    return out


def main():
    if hasattr(sys.stdout, "reconfigure"):      # a Windows console is not UTF-8 by default
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="unslop-prose: lint the wiki prose")
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--all", action="store_true", help="show every finding and ignore the baseline")
    ap.add_argument("--summary", action="store_true", help="print counts by rule")
    ap.add_argument("--update-baseline", action="store_true")
    a = ap.parse_args()
    paths = [Path(x) for x in a.paths] or sorted(DOCS.rglob("*.md"))
    found = lint_files(paths)
    now = counts(found)
    if a.update_baseline:
        BASELINE.write_text(json.dumps(now, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(f"baseline written: {sum(sum(v.values()) for v in now.values())} findings in {len(now)} files")
        return 0
    base = {} if a.all or not BASELINE.exists() else json.loads(BASELINE.read_text(encoding="utf-8"))
    if a.summary:
        by_rule = {}
        for v in now.values():
            for rule, n in v.items():
                by_rule[rule] = by_rule.get(rule, 0) + n
        for rule, n in sorted(by_rule.items(), key=lambda kv: -kv[1]):
            print(f"{n:6} {rule}")
        print(f"{sum(by_rule.values()):6} total in {len(now)} of {len(paths)} files")
        return 0
    bad = 0
    for rel, hits in sorted(found.items()):
        over = {rule for rule, n in now[rel].items() if n > base.get(rel, {}).get(rule, 0)}
        for no, rule, msg in hits:
            if rule in over:
                print(f"{rel}:{no}: {rule}: {msg}")
                bad += 1
    stale = sum(1 for rel, rules in base.items() for rule, n in rules.items() if now.get(rel, {}).get(rule, 0) < n)
    if bad:
        print(f"\nunslop-prose: {bad} finding(s) in files that are over their baseline. Fix the text, or see tools/unslop_prose/README.md.")
        return 1
    print(f"unslop-prose: clean ({len(paths)} files)." + (f" {stale} baseline entries can be lowered: run --update-baseline." if stale else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
