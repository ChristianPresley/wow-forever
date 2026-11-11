"""Build the profession guide pages (docs/professions/*.md) from data.

Inputs
  tools/professions/recipes/<slug>.json  Every recipe of the profession as read from the game
                                         client: heading, learn skill, yellow/green/grey skill,
                                         reagents, source, status against Classic.
  tools/professions/guides/<slug>.yml    Codex guide for one profession: prose, the 1-300 path,
                                         recipe picks, tips, FAQ.

Outputs
  docs/professions/<slug>.md            The guide.
  docs/professions/<slug>-recipes.md    The full recipe list (only when the profession has more
                                         than INLINE_MAX recipes; smaller lists go in the guide).
  docs/professions/index.md             The hub.

Usage
  .venv/Scripts/python.exe tools/professions/build.py              # all professions with a .yml
  .venv/Scripts/python.exe tools/professions/build.py alchemy      # one profession
  .venv/Scripts/python.exe tools/professions/build.py --check alchemy   # validate only

Rules that the script checks before it writes a page
  - The path starts at skill 1, ends at skill 300, and has no gaps or overlaps.
  - A `craft` step names a recipe that exists in the recipe data (exact name).
  - A craft step does not start below the learn skill of the recipe. If the client does not
    hold the learn skill (trainer recipes), the step must give `learn` and `learn_basis`
    (`classic` for a Classic-era trainer value, `estimate` for a Codex estimate).
  - A craft step does not continue to a skill where the recipe is grey.
  - Each recipe named in `picks` exists in the recipe data.

Numbers that the script computes (do not write them in the .yml)
  - The colour of the recipe at the start and at the end of a step.
  - The expected number of crafts for a step. The script uses the Classic-era rule:
    a craft always gives a point below the yellow skill, and the chance then decreases in a
    straight line to 0 at the grey skill.
  - The materials for each bracket and for the full path.
"""
from __future__ import annotations

import json
import math
import sys
from collections import Counter, OrderedDict
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = ROOT / "docs" / "professions"
ORDER = ["alchemy", "blacksmithing", "enchanting", "engineering", "leatherworking", "tailoring",
         "herbalism", "mining", "skinning", "cooking", "first-aid", "fishing"]
KINDS = {"crafting": "Primary · Crafting", "gathering": "Primary · Gathering", "secondary": "Secondary"}
INLINE_MAX = 60
CLIENT_BUILD = "1.60.1.70862"
PAGE_DATE = "10 November 2026"
SITE = "https://wowforevertalents.com"


def load(slug):
    data = json.loads((HERE / "recipes" / f"{slug}.json").read_text(encoding="utf8"))
    guide = yaml.safe_load((HERE / "guides" / f"{slug}.yml").read_text(encoding="utf8"))
    return data, guide


def colour(r, skill):
    if skill >= r["grey"]:
        return "Grey"
    if skill >= r["green"]:
        return "Green"
    if skill >= r["yellow"]:
        return "Yellow"
    return "Orange"


def expected_crafts(r, lo, hi):
    total = 0.0
    for s in range(lo, hi):
        if s < r["yellow"]:
            p = 1.0
        elif r["grey"] > r["yellow"]:
            p = max((r["grey"] - s) / (r["grey"] - r["yellow"]), 0.05)
        else:
            p = 1.0
        total += 1 / p
    return math.ceil(total)


def reagent_text(r):
    return ", ".join(f"{n} {name}" for n, name in r["reagents"]) or "—"


def source_text(r):
    s = "Trainer" if r["src"] == "trainer" else "Recipe item"
    if r.get("bop_recipe"):
        s += " (BoP)"
    if r.get("favor"):
        s += " · Merchant's Favor"
    return s


def learn_text(r):
    return str(r["learn"]) if r["learn"] is not None else "—"


def name_text(r):
    n = r["name"]
    if r.get("makes") and r["makes"] != "1":
        n += f" (makes {r['makes']})"
    return n


def recipe_tables(recipes, level="##"):
    groups = OrderedDict()
    for r in recipes:
        groups.setdefault(r["group"], []).append(r)
    out = []
    for g, rs in groups.items():
        out += [f"{level} {g}", "", "| Recipe | Learn | Yellow | Grey | Reagents | Source | Forever |", "|---|---|---|---|---|---|---|"]
        for r in rs:
            st = {"new": "New", "changed": "Changed"}.get(r["status"], "—")
            out.append(f"| **{name_text(r)}** | {learn_text(r)} | {r['yellow'] if r['yellow'] is not None else '—'} | "
                       f"{r['grey'] if r['grey'] is not None else '—'} | {reagent_text(r)} | {source_text(r)} | {st} |")
        out.append("")
    return out


def check_path(slug, guide, by_name, errors):
    """Validate the path and return rendered rows per bracket plus material totals."""
    expect = 1
    rendered = []
    grand = Counter()
    for b in guide.get("path") or []:
        rows, mats = [], Counter()
        for st in b["steps"]:
            lo, hi = int(st["from"]), int(st["to"])
            where = f"{slug}: step {lo}-{hi}"
            if lo != expect:
                errors.append(f"{where}: starts at {lo}, the previous step ends at {expect}")
            if hi <= lo:
                errors.append(f"{where}: 'to' must be more than 'from'")
            expect = hi
            if "craft" in st:
                r = by_name.get(st["craft"])
                if not r:
                    errors.append(f"{where}: unknown recipe '{st['craft']}'")
                    continue
                if r["yellow"] is None or r["grey"] is None:
                    errors.append(f"{where}: '{r['name']}' has no skill colours in the client; do not use it in the path")
                    continue
                learn, basis = r["learn"], ""
                if learn is None:
                    if "learn" not in st or st.get("learn_basis") not in ("classic", "estimate"):
                        errors.append(f"{where}: '{r['name']}' has no learn skill in the client; add learn: N and learn_basis: classic|estimate")
                        continue
                    learn, basis = int(st["learn"]), st["learn_basis"]
                    if learn > r["yellow"]:
                        errors.append(f"{where}: learn {learn} is above the yellow skill {r['yellow']} of '{r['name']}'")
                if lo < learn:
                    errors.append(f"{where}: '{r['name']}' is learned at {learn}")
                if hi > r["grey"]:
                    errors.append(f"{where}: '{r['name']}' is grey at {r['grey']}")
                    continue
                n = expected_crafts(r, lo, hi)
                for cnt, name in r["reagents"]:
                    mats[name] += cnt * n
                c0, c1 = colour(r, lo), colour(r, hi - 1)
                col = c0 if c0 == c1 else f"{c0} → {c1}"
                lt = f"{learn}" + {"classic": " (Classic value)", "estimate": " (estimate)", "": ""}[basis]
                rows.append(f"| {lo}–{hi} | **{name_text(r)}** | {n} | {reagent_text(r)} | {col} | {source_text(r)}, learn {lt} | {st.get('note', '')} |")
            elif "gather" in st:
                basis = {"classic": "Classic-era value", "forever": "Forever source"}.get(st.get("basis", "classic"), "Classic-era value")
                rows.append(f"| {lo}–{hi} | **{st['gather']}** | — | — | — | {st.get('where', '')} ({basis}) | {st.get('note', '')} |")
            else:
                errors.append(f"{where}: a step needs 'craft' or 'gather'")
        rendered.append((b, rows, mats))
        grand.update(mats)
    if expect != 300 and guide.get("path"):
        errors.append(f"{slug}: the path ends at {expect}, it must end at 300")
    if not guide.get("path"):
        errors.append(f"{slug}: no path")
    return rendered, grand


def mats_table(mats):
    out = ["| Material | Amount |", "|---|---|"]
    for name, n in sorted(mats.items(), key=lambda kv: (-kv[1], kv[0])):
        out.append(f"| {name} | {n} |")
    return out


def render(slug, data, guide, errors):
    recipes = data["recipes"]
    by_name = {}
    for r in recipes:
        if r["name"] in by_name:
            errors.append(f"{slug}: duplicate recipe name {r['name']}")
        by_name[r["name"]] = r
    for k in ("profession", "kind", "icon", "description", "intro", "card", "glance", "new", "path"):
        if k not in guide:
            errors.append(f"{slug}: missing key '{k}'")
    if guide.get("kind") not in KINDS:
        errors.append(f"{slug}: kind must be one of {list(KINDS)}")
    if errors:
        return None
    rendered, grand = check_path(slug, guide, by_name, errors)
    for sec in guide.get("picks") or []:
        for it in sec["items"]:
            if it["recipe"] not in by_name:
                errors.append(f"{slug}: picks: unknown recipe '{it['recipe']}'")
    if errors:
        return None

    name = guide["profession"]
    n = len(recipes)
    st = Counter(r["status"] for r in recipes)
    n_tr = sum(1 for r in recipes if r["src"] == "trainer")
    n_fav = sum(1 for r in recipes if r.get("favor"))
    separate = n > INLINE_MAX
    has_picks = bool(guide.get("picks"))
    camp = [r for r in recipes if r["group"] == "Camping"]

    jump = ['<a href="#new-in-forever">New</a>', '<a href="#level-1-to-300">1–300</a>']
    if has_picks:
        jump.append('<a href="#recipes-to-get">Recipes to get</a>')
    if camp:
        jump.append('<a href="#camp-features">Camp</a>')
    jump.append('<a href="#all-recipes">All recipes</a>')

    o = [
        "---", f'description: "{guide["description"]}"', "tags:", "  - Professions", "search:", "  boost: 2", "---", "",
        f"# {name} Guide", "",
        f"<!-- This page is generated. Edit tools/professions/guides/{slug}.yml, then run tools/professions/build.py. -->", "",
        '<div class="guide-head" markdown>', "",
        f':{guide["icon"]}:{{ aria-hidden="true" }} <span class="gh-kind">Profession guide</span> **{KINDS[guide["kind"]]}**{{ .badge }}', "",
        f'<nav class="gh-jump" aria-label="Jump to section">{" ".join(jump)}</nav>', "", "</div>", "",
        f'!!! info "Current as of {PAGE_DATE}"',
        f"    The recipe data is from the game client, build {CLIENT_BUILD}. [wowforevertalents.com]({SITE}/professions/{slug}/) reads this data from the client. "
        "The client does not hold the skill that a trainer asks for, the prices, or the drop locations. "
        "The path and the recipe picks are Codex recommendations.", "",
        guide["intro"].strip(), "",
        '<aside class="infobox" markdown>', f'<p class="infobox-title">{name} at a glance</p>', "", "| | |", "|---|---|",
        f"| **Type** | {KINDS[guide['kind']]} |",
    ]
    for label, value in guide["glance"]:
        o.append(f"| **{label}** | {value} |")
    o += [
        f"| **Recipes** | {n} ({st.get('new', 0)} new, {st.get('changed', 0)} changed) |",
        f"| **From a trainer** | {n_tr} |",
        f"| **From a recipe item** | {n - n_tr} |",
    ]
    if n_fav:
        o.append(f"| **Merchant's Favor** | {n_fav} recipes |")
    o += ["", "</aside>", "", "## New in Forever", ""]
    o += [f"- {b}" for b in guide["new"]] + [""]

    o += ["## Level 1 to 300", ""]
    if guide.get("path_intro"):
        o += [guide["path_intro"].strip(), ""]
    o += [
        "The *Crafts* column is an estimate. A recipe always gives a skill point while it is orange. "
        "The chance decreases when the recipe is yellow and green, and a grey recipe gives no points. "
        "The estimate uses the Classic-era rule, which is not confirmed for Forever.", "",
    ]
    for b, rows, mats in rendered:
        o += [f"### {b['bracket']}", ""]
        if b.get("intro"):
            o += [b["intro"].strip(), ""]
        o += ["| Skill | Make or gather | Crafts | Reagents for 1 | Colour | Source | Notes |", "|---|---|---|---|---|---|---|"] + rows + [""]
        for note in b.get("notes") or []:
            o.append(f"- {note}")
        if b.get("notes"):
            o.append("")
        if mats:
            o += [f'??? example "Materials for {b["bracket"]}"', ""] + ["    " + ln for ln in mats_table(mats)] + [""]
    if grand:
        o += ["### All materials", "",
              "This list is the sum of all steps. It counts materials that you make in an earlier step again, so the real amount can be smaller.", ""]
        o += mats_table(grand) + [""]

    if has_picks:
        o += ["## Recipes to get", ""]
        if guide.get("picks_intro"):
            o += [guide["picks_intro"].strip(), ""]
        for sec in guide["picks"]:
            o += [f"### {sec['title']}", ""]
            if sec.get("intro"):
                o += [sec["intro"].strip(), ""]
            o += ["| Recipe | Learn | Reagents | Source | Why |", "|---|---|---|---|---|"]
            for it in sec["items"]:
                r = by_name[it["recipe"]]
                o.append(f"| **{name_text(r)}** | {learn_text(r)} | {reagent_text(r)} | {source_text(r)} | {it['why']} |")
            o.append("")

    if guide.get("sources_note"):
        o += ["## Where recipes come from", "", guide["sources_note"].strip(), ""]
    if guide.get("specializations"):
        o += ["## Specializations", ""]
        if guide.get("specializations_intro"):
            o += [guide["specializations_intro"].strip(), ""]
        for s in guide["specializations"]:
            o.append(f"- **{s['name']}:** {s['text']}")
        o.append("")
    if camp:
        o += ["## Camp features", "",
              f"{name} makes these features for a [camp](../systems/camping.md). The camp page gives the effect of each feature.", "",
              "| Feature | Learn | Reagents | Source |", "|---|---|---|---|"]
        for r in camp:
            o.append(f"| **{r['name']}** | {learn_text(r)} | {reagent_text(r)} | {source_text(r)} |")
        o.append("")
        if guide.get("camp_note"):
            o += [guide["camp_note"].strip(), ""]
    if guide.get("tips"):
        o += ["## Tips", ""] + [f"- {t}" for t in guide["tips"]] + [""]

    o += ["## All recipes", ""]
    legend = ("**Learn** is the skill that the client gives for the recipe. A dash shows a trainer recipe, because the client does not hold that skill. "
              "**Yellow** and **Grey** are the skills where the recipe changes colour. **Forever** shows a recipe that is new or changed from Classic Era.")
    if separate:
        o += [f"The full list of {n} recipes is on a separate page: [{name} recipes]({slug}-recipes.md).", ""]
    else:
        o += [legend, ""] + recipe_tables(recipes, "###")
    if data.get("removed"):
        o += ['??? note "Classic recipes that are not in Forever"', "    " + ", ".join(r["name"] for r in data["removed"]) + ".", ""]
    if guide.get("faq"):
        o += ["## FAQ", ""]
        for f in guide["faq"]:
            o += [f'??? question "{f["q"]}"', f"    {f['a'].strip()}", ""]
    o += ["## Sources", "", f"- [wowforevertalents.com: {name} recipes, read from the client]({SITE}/professions/{slug}/)"]
    for s in guide.get("sources") or []:
        o.append(f"- [{s['title']}]({s['url']})")
    o.append("")

    rec = None
    if separate:
        rec = [
            "---", f'description: "All {n} {name} recipes in WoW: Forever, with the learn skill, the yellow and grey skills, the reagents and the source of each recipe."',
            "tags:", "  - Professions", "---", "",
            f"# {name} Recipes", "",
            "<!-- This page is generated by tools/professions/build.py from tools/professions/recipes/%s.json. -->" % slug, "",
            f"This page lists all {n} {name} recipes in the game client, build {CLIENT_BUILD}. The headings are the headings of the in-game window. "
            f"For the path from 1 to 300 and the recipe picks, see the [{name} guide]({slug}.md).", "",
            legend, "",
        ] + recipe_tables(recipes, "##")
        rec += [f"Source: [wowforevertalents.com]({SITE}/professions/{slug}/), read from the client.", ""]
    return "\n".join(o), ("\n".join(rec) if rec else None)


def render_index(done):
    o = [
        "---",
        'description: "Guides for all 12 professions in WoW: Forever: a path from skill 1 to 300, the materials, the recipes to get, and the full recipe list of each profession."',
        "search:", "  boost: 3", "hide:", "  - toc", "---", "",
        "# Profession Guides", "",
        "<!-- This page is generated by tools/professions/build.py. -->", "",
        "A guide for each of the **12 professions**. Each guide gives a path from skill 1 to 300, the materials for the path, the recipes to get, and the full recipe list.", "",
        f'??? info "How the profession guides work · current as of {PAGE_DATE}"',
        f"    - **Recipe data:** from the game client, build {CLIENT_BUILD}, as read by [wowforevertalents.com]({SITE}/professions/).",
        "    - **Paths and picks:** Codex recommendations. A script checks each path against the recipe data.",
        "    - **Not in the client:** trainer skill requirements, prices and drop locations. The guides mark Classic-era values and estimates.",
        "    - For the rules of professions and the best professions for each class, see [Professions](../characters/professions.md).", "",
    ]
    for kind, title in (("crafting", "Crafting professions"), ("gathering", "Gathering professions"), ("secondary", "Secondary skills")):
        rows = [(s, g, d) for s, g, d in done if g["kind"] == kind]
        if not rows:
            continue
        o += [f"## {title}", "", '<div class="grid cards fc-multi" markdown>', ""]
        for slug, g, d in rows:
            o += [f"-   :{g['icon']}:{{ .lg .middle }} **[{g['profession']}]({slug}.md)**", "", "    ---", "",
                  f"    {g['card']['use']}", "",
                  f"    - **Pairs with:** {g['card']['pairs']}",
                  f"    - **Recipes:** {len(d['recipes'])}", ""]
        o += ["</div>", ""]
    return "\n".join(o)


def main(argv):
    check = "--check" in argv
    want = [a for a in argv if not a.startswith("--")]
    slugs = [s for s in ORDER if (HERE / "guides" / f"{s}.yml").exists()]
    errors, done, pages = [], [], {}
    for slug in slugs:
        errs = []
        try:
            data, guide = load(slug)
            res = render(slug, data, guide, errs)
        except (yaml.YAMLError, KeyError, TypeError, ValueError) as e:
            errs.append(f"{slug}: {type(e).__name__}: {e}")
            res = None
        if errs or res is None:
            if not want or slug in want:
                errors += errs
            continue
        done.append((slug, guide, data))
        pages[slug] = res
    if errors:
        print("\n".join(errors))
        print(f"\n{len(errors)} error(s). Nothing written.")
        return 1
    if check:
        print("OK:", ", ".join(s for s, _, _ in done))
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, (page, rec) in pages.items():
        if want and slug not in want:
            continue
        (OUT / f"{slug}.md").write_text(page, encoding="utf8", newline="\n")
        if rec:
            (OUT / f"{slug}-recipes.md").write_text(rec, encoding="utf8", newline="\n")
    (OUT / "index.md").write_text(render_index(done), encoding="utf8", newline="\n")
    print("Wrote:", ", ".join(s for s in pages if not want or s in want), "+ index")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
