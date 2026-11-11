"""Build the class progression pages and the Equipment add-ons.

Inputs
  tools/classes/guides/<class>.yml       The narrated progression of one class: chapters, races,
                                         talent paths and equipment sets.
  tools/talents/trees/<class>.json       Talent trees from the game client.
  tools/talents/guides/<class>.yml       Talent builds. A talent path names builds from this file.
  tools/professions/recipes/<slug>.json  Recipes from the game client. A crafted item must be in this data.

Outputs
  docs/guides/<class>/index.md           The progression: 9 chapters from character creation to raids.
  docs/guides/<class>/equipment.md       The Equipment add-on.
  (docs/guides/<class>/talents.md is written by tools/talents/build.py.
   docs/guides/<class>/<race>.md are hand-written Race add-ons.)

Usage
  .venv/Scripts/python.exe tools/classes/build.py            # all classes that have a .yml
  .venv/Scripts/python.exe tools/classes/build.py mage       # one class
  .venv/Scripts/python.exe tools/classes/build.py --check    # validate only, write nothing

The script stops with a list of errors if the data breaks a rule:
  - a chapter is missing or out of order, or a spell level is outside its chapter
  - a race has no Race add-on page, or a Race add-on page has no race entry
  - a talent path names a build that does not exist, or a build that breaks the tree rules
  - a crafted item is not in the client recipe data, or a dungeon has no page
  - a sentence breaks the Simplified Technical English profile (DESIGN.md):
    more than 25 words, a semicolon, or should / would / could / might / may
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DOCS = ROOT / "docs"
sys.path.insert(0, str(HERE.parent / "talents"))
import build as talents_build  # noqa: E402  (tools/talents/build.py)

ORDER = ["druid", "hunter", "mage", "paladin", "priest", "rogue", "shaman", "warlock", "warrior"]
PAGE_DATE = "10 November 2026"
BADGES = talents_build.BADGES

# id, level range, heading prefix
CHAPTERS = [
    ("start", None, "Before level 1"),
    ("l1", (1, 9), "Levels 1–9"),
    ("l10", (10, 19), "Levels 10–19"),
    ("l20", (20, 29), "Levels 20–29"),
    ("l30", (30, 39), "Levels 30–39"),
    ("l40", (40, 49), "Levels 40–49"),
    ("l50", (50, 59), "Levels 50–59"),
    ("l60", None, "Level 60"),
    ("raid", None, "Raids and PvP"),
]
CH_IDS = [c[0] for c in CHAPTERS]
LEVEL_CH = [c[0] for c in CHAPTERS if c[1]]
FACTIONS = {"alliance": "Alliance", "horde": "Horde"}
ITEM_FROM = {
    "craft": "Crafted", "quest": "Quest", "dungeon": "Dungeon", "raid": "Raid", "vendor": "Vendor",
    "drop": "World drop", "rep": "Reputation", "pvp": "PvP", "class": "Class quest", "any": "All sources",
}
BASIS = {
    "forever": "",
    "classic": " **Classic-era**{ .pill .pill--outline .pill--sm }",
    "unverified": " **Not confirmed**{ .pill .pill--outline .pill--sm }",
}
PROFESSIONS = sorted(p.stem for p in (HERE.parent / "professions" / "recipes").glob("*.json"))


# ---------------------------------------------------------------- data access

_recipes: dict[str, dict] = {}


def recipe(profession: str, name: str):
    if profession not in _recipes:
        data = json.loads((HERE.parent / "professions" / "recipes" / f"{profession}.json").read_text(encoding="utf8"))
        _recipes[profession] = {r["name"].lower(): r for r in data["recipes"]}
    return _recipes[profession].get(name.lower())


def place(slug: str):
    """A dungeon or raid page. Returns (relative link from docs/guides/<class>/, title) or None."""
    for folder in ("dungeons", "raids"):
        p = DOCS / "content" / folder / f"{slug}.md"
        if p.exists():
            m = re.search(r"^# (.+)$", p.read_text(encoding="utf8"), re.M)
            return f"../../content/{folder}/{slug}.md", (m.group(1).strip() if m else slug)
    return None


# ---------------------------------------------------------------- STE lint

_MODAL = re.compile(r"\b(should|would|could|might|may)\b")


def plain(text: str) -> str:
    t = re.sub(r"\{[^{}]*\}", "", text)                 # attribute lists
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", t)   # links
    t = re.sub(r"<[^>]+>", "", t)                       # html
    t = re.sub(r":[a-z0-9-]+:", "", t)                  # icons
    t = re.sub(r"&[a-z]+;", " ", t)
    return t.replace("*", "").replace("`", "")


def lint(text, where, errors):
    if not text:
        return
    fenced = False
    for raw in str(text).splitlines():
        if raw.strip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        line = plain(raw).strip()
        if not line or line.startswith(("|", "#", "<", "???", "!!!", "===")):
            continue
        line = re.sub(r"^([-*]|\d+\.)\s+", "", line)
        if ";" in line:
            errors.append(f"{where}: STE: semicolon in '{line[:70]}'")
        for m in _MODAL.finditer(line):
            errors.append(f"{where}: STE: '{m.group(1)}' in '{line[:70]}'")
        for sent in re.split(r"(?<=[.!?])\s+(?=[A-Z\"“(\[0-9])", line):
            n = len(sent.split())
            if n > 25:
                errors.append(f"{where}: STE: sentence has {n} words (maximum 25): '{sent[:70]}…'")


# ---------------------------------------------------------------- talents

def build_points(build, talents):
    """One entry per talent point: (level, talent name, rank reached, max rank, reason)."""
    ranks: dict[str, int] = {}
    out = []
    k = 0
    for step in build["steps"]:
        name, n = step[0], int(step[1])
        why = step[2] if len(step) > 2 else ""
        for _ in range(n):
            k += 1
            ranks[name] = ranks.get(name, 0) + 1
            out.append((9 + k, name, ranks[name], talents[name]["max"], why))
    return out


def chapter_talent_rows(points, lo, hi):
    """Group the points of one chapter by talent: level range, talent, rank, reason."""
    rows = []
    for level, name, rank, mx, why in points:
        if not lo <= level <= hi:
            continue
        if rows and rows[-1]["name"] == name:
            rows[-1].update(hi=level, rank=rank)
        else:
            rows.append({"lo": level, "hi": level, "name": name, "rank": rank, "max": mx, "why": why})
    return rows


def split_at(points, talents, level):
    spent = [0, 0, 0]
    for lv, name, *_ in points:
        if lv <= level:
            spent[talents[name]["tree_i"]] += 1
    return "/".join(str(s) for s in spent)


# ---------------------------------------------------------------- rendering helpers

def md_block(text):
    return str(text).strip().splitlines() + [""]


def addon(pick, values, kind, label, body_lines, link=None, default=False):
    """One add-on block. The reader's pick decides which blocks show (docs/javascripts/codex.js)."""
    if not any(ln.strip() for ln in body_lines):
        return []
    icon = {"race": ":material-account-group:", "talents": ":material-star-four-points:", "gear": ":material-shield-sword:"}[pick]
    more = f" [{link[1]}]({link[0]}){{ .fc-addon__more }}" if link else ""  # Markdown, so MkDocs resolves the .md link
    return [
        f'<div class="fc-addon" data-pick="{pick}" data-value="{" ".join(values)}"{" data-default" if default else ""} markdown>',
        "",
        f'<p class="fc-addon__label" markdown>{icon} <span class="fc-addon__kind">{kind} add-on</span> '
        f'<strong>{html.escape(label)}</strong>{more} <a class="fc-addon__change" href="#picks">Change</a></p>',
        "",
        *body_lines,
        "",
        "</div>",
        "",
    ]


def item_source(it, errors, where):
    """Markdown for the Source cell of one item. Checks crafted items and dungeons against the data."""
    kind = it.get("from")
    if kind not in ITEM_FROM:
        errors.append(f"{where}: item '{it.get('name')}' has a bad 'from': {kind!r}")
        return ""
    basis = it.get("basis", "classic" if kind != "craft" else "forever")
    if basis not in BASIS:
        errors.append(f"{where}: item '{it.get('name')}' has a bad 'basis': {basis!r}")
        basis = "forever"
    where_txt = (it.get("where") or "").strip()
    if kind == "craft":
        prof = it.get("profession")
        if prof not in PROFESSIONS:
            errors.append(f"{where}: crafted item '{it.get('name')}' needs a valid 'profession'")
            return ""
        r = recipe(prof, it.get("recipe") or it["name"])
        if not r:
            errors.append(f"{where}: '{it.get('recipe') or it['name']}' is not a {prof} recipe in the client data")
            return ""
        txt = f"[{prof.replace('-', ' ').title()}](../../professions/{prof}.md)"
        if r.get("learn"):
            txt += f", skill {r['learn']}"
        elif r.get("src") == "trainer":
            txt += ", trainer recipe"  # the client does not hold the skill that the trainer asks for
        if r.get("status") == "new":
            txt += " **New**{ .pill .pill--new .pill--sm }"
    elif kind in ("dungeon", "raid"):
        slug = it.get("dungeon") or it.get("raid")
        if slug:
            pl = place(slug)
            if not pl:
                errors.append(f"{where}: item '{it.get('name')}': no page for '{slug}' in docs/content")
                return ""
            txt = f"[{pl[1]}]({pl[0]})"
        elif where_txt:
            txt, where_txt = where_txt, ""
        else:
            errors.append(f"{where}: item '{it.get('name')}' needs 'dungeon:' (a page slug) or 'where:'")
            return ""
    else:
        txt = ITEM_FROM[kind]
    if where_txt:
        txt += f": {where_txt}"
    return txt + BASIS[basis]


def item_table(items, errors, where, level_col=None):
    if not items:
        return []
    head = "| Slot | Item | Source |"
    out = [head, "|---|---|---|"]
    for it in items:
        if not it.get("slot") or not it.get("name"):
            errors.append(f"{where}: each item needs 'slot' and 'name': {it}")
            continue
        lint(it.get("where"), where, errors)
        out.append(f"| {it['slot']} | **{it['name']}** | {item_source(it, errors, where)} |")
    return out + [""]


# ---------------------------------------------------------------- validation

def check(slug, g, tguide, talents, errors):
    def need(obj, keys, where):
        for k in keys:
            if not obj.get(k):
                errors.append(f"{where}: missing '{k}'")

    need(g, ["class", "badges", "description", "intro", "glance", "strengths", "weaknesses", "changes", "chapters", "races", "factions",
               "paths", "gear", "equipment", "professions", "legacy", "faq", "sources"], slug)
    if errors:
        return
    ids = [c.get("id") for c in g["chapters"]]
    if ids != CH_IDS:
        errors.append(f"{slug}: chapters must be exactly {CH_IDS} in this order, found {ids}")
        return
    for (cid, rng, _), ch in zip(CHAPTERS, g["chapters"]):
        w = f"{slug}/chapter {cid}"
        need(ch, ["title", "story"], w)
        for key in ("story", "warn", "tip", "extra", "hardcore"):
            lint(ch.get(key), f"{w}/{key}", errors)
        for goal in ch.get("goals") or []:
            lint(goal, f"{w}/goals", errors)
        for row in ch.get("train") or []:
            if len(row) < 2:
                errors.append(f"{w}: a train row is [level, spell, note]")
                continue
            if rng and not rng[0] <= int(row[0]) <= rng[1]:
                errors.append(f"{w}: '{row[1]}' at level {row[0]} is outside levels {rng[0]}–{rng[1]}")
            if not rng:
                errors.append(f"{w}: only level chapters can have 'train' rows")
            if len(row) > 2:
                lint(row[2], f"{w}/train", errors)
        for d in ch.get("dungeons") or []:
            if isinstance(d, dict) and d.get("id") and not place(d["id"]):
                errors.append(f"{w}: no page for dungeon '{d['id']}'")
            if isinstance(d, str) and not place(d):
                errors.append(f"{w}: no page for dungeon '{d}' (use {{name:, levels:}} for a dungeon without a page)")
            if isinstance(d, dict):
                lint(d.get("note"), f"{w}/dungeons", errors)

    # races: one entry for each Race add-on page, and the reverse
    pages = {p.stem for p in (DOCS / "guides" / slug).glob("*.md")} - {"index", "talents", "equipment"}
    seen = set()
    for r in g["races"]:
        w = f"{slug}/race {r.get('id')}"
        need(r, ["id", "name", "faction", "status", "pitch", "start"], w)
        if r.get("faction") not in FACTIONS:
            errors.append(f"{w}: faction must be alliance or horde")
        if r.get("id") not in pages:
            errors.append(f"{w}: no Race add-on page docs/guides/{slug}/{r.get('id')}.md")
        seen.add(r.get("id"))
        for k in ("pitch", "start"):
            lint(r.get(k), f"{w}/{k}", errors)
        for cid, txt in (r.get("notes") or {}).items():
            if cid not in CH_IDS:
                errors.append(f"{w}: unknown chapter '{cid}' in notes")
            lint(txt, f"{w}/notes/{cid}", errors)
    for missing in sorted(pages - seen):
        errors.append(f"{slug}: Race add-on page '{missing}.md' has no entry in races")
    for f, chs in g["factions"].items():
        if f not in FACTIONS:
            errors.append(f"{slug}: unknown faction '{f}'")
        for cid in LEVEL_CH[1:] + ["l60"]:
            if not (chs or {}).get(cid):
                errors.append(f"{slug}/faction {f}: missing route text for chapter '{cid}'")
        for cid, txt in (chs or {}).items():
            if cid not in CH_IDS:
                errors.append(f"{slug}/faction {f}: unknown chapter '{cid}'")
            lint(txt, f"{slug}/faction {f}/{cid}", errors)

    # talent paths
    builds = {b["id"]: b for b in tguide["builds"]}
    pids = set()
    for p in g["paths"]:
        w = f"{slug}/path {p.get('id')}"
        need(p, ["id", "name", "pitch", "leveling", "endgame", "play"], w)
        if p.get("id") in pids:
            errors.append(f"{w}: duplicate id")
        pids.add(p.get("id"))
        b = builds.get(p.get("leveling"))
        if not b or b["kind"] != "leveling":
            errors.append(f"{w}: '{p.get('leveling')}' is not a leveling build in tools/talents/guides/{slug}.yml")
        for e in p.get("endgame") or []:
            if e not in builds or builds[e]["kind"] != "endgame":
                errors.append(f"{w}: '{e}' is not a level 60 build in tools/talents/guides/{slug}.yml")
        play = p.get("play") or {}
        for cid in LEVEL_CH + ["l60", "raid"]:
            if not play.get(cid):
                errors.append(f"{w}: missing 'play' text for chapter '{cid}'")
        for cid, txt in play.items():
            if cid not in CH_IDS:
                errors.append(f"{w}: unknown chapter '{cid}' in play")
            lint(txt, f"{w}/play/{cid}", errors)
        lint(p.get("pitch"), f"{w}/pitch", errors)
        for line in p.get("priority") or []:
            lint(line, f"{w}/priority", errors)

    # equipment sets
    gids = set()
    for s in g["gear"]:
        w = f"{slug}/gear {s.get('id')}"
        need(s, ["id", "name", "pitch", "stats", "chapters"], w)
        if s.get("id") in gids:
            errors.append(f"{w}: duplicate id")
        gids.add(s.get("id"))
        lint(s.get("pitch"), f"{w}/pitch", errors)
        chs = s.get("chapters") or {}
        for cid in LEVEL_CH + ["l60"]:
            if not (chs.get(cid) or {}).get("text"):
                errors.append(f"{w}: missing chapter '{cid}' text")
        for cid, c in chs.items():
            if cid not in CH_IDS:
                errors.append(f"{w}: unknown chapter '{cid}'")
            lint((c or {}).get("text"), f"{w}/{cid}", errors)
    for p in g["paths"]:
        if p.get("gear") and p["gear"] not in gids:
            errors.append(f"{slug}/path {p.get('id')}: gear set '{p['gear']}' does not exist")
    eq = g["equipment"]
    need(eq, ["intro", "proficiencies"], f"{slug}/equipment")
    for k in ("intro",):
        lint(eq.get(k), f"{slug}/equipment/{k}", errors)
    for k in ("rules",):
        for line in eq.get(k) or []:
            lint(line, f"{slug}/equipment/{k}", errors)
    for k in ("proficiencies", "enchants", "consumables"):
        for row in eq.get(k) or []:
            if len(row) != 3:
                errors.append(f"{slug}/equipment/{k}: each row has 3 cells: {row}")
            for cell in row:
                lint(cell, f"{slug}/equipment/{k}", errors)
    for f in g.get("faq") or []:
        lint(f.get("q"), f"{slug}/faq", errors)
        lint(f.get("a"), f"{slug}/faq", errors)
    for k in ("intro", "professions", "legacy"):
        lint(g.get(k), f"{slug}/{k}", errors)
    for k in ("strengths", "weaknesses", "mistakes"):
        for line in g.get(k) or []:
            lint(line, f"{slug}/{k}", errors)
    for line in (g.get("changes") or {}).get("notes") or []:
        lint(line, f"{slug}/changes", errors)


# ---------------------------------------------------------------- progression page

def picker(slug, g):
    cls = g["class"]

    def group(pick, legend, options):
        out = [f'<fieldset class="fc-pick__group" data-pick="{pick}"><legend>{legend}</legend>', '<div class="fc-pick__opts">']
        for i, (value, label) in enumerate(options):
            out.append(
                f'<label class="fc-pick__opt"><input type="radio" name="fc-{pick}" value="{value}"{" checked" if i == 0 else ""}>'
                f"<span>{html.escape(label)}</span></label>"
            )
        return out + ["</div>", "</fieldset>"]

    out = [f'<div class="fc-pick" data-class="{slug}" role="group" aria-label="Add-ons for your {cls}">']
    out += group("race", "Race", [(r["id"], r["name"]) for r in g["races"]])
    out += group("talents", "Talents", [(p["id"], p["name"]) for p in g["paths"]])
    out += group("gear", "Equipment", [(s["id"], s["name"]) for s in g["gear"]])
    out += [
        '<p class="fc-pick__note"><label class="fc-pick__all"><input type="checkbox" name="fc-all"><span>Show all add-ons</span></label> '
        "Each chapter shows only the add-ons that you select. This browser saves your selection.</p>",
        "</div>",
        "",
    ]
    return out


def render_progression(slug, g, tguide, talents, tree_names, errors):
    cls = g["class"]
    builds = {b["id"]: b for b in tguide["builds"]}
    races = g["races"]
    by_faction = {f: [r["id"] for r in races if r["faction"] == f] for f in FACTIONS}
    first_race, first_path, first_gear = races[0]["id"], g["paths"][0]["id"], g["gear"][0]["id"]
    points = {p["id"]: build_points(builds[p["leveling"]], talents) for p in g["paths"]}
    badges = " ".join(BADGES[b] for b in g["badges"])
    jump = ['<a href="#picks">Add-ons</a>'] + [
        f'<a href="#{cid}">{"Start" if cid == "start" else "Raids & PvP" if cid == "raid" else "60" if cid == "l60" else f"{rng[0]}–{rng[1]}"}</a>'
        for cid, rng, _ in CHAPTERS
    ]
    out = [
        "---",
        f'description: "{g["description"]}"',
        "tags:", f"  - {cls}",
        "search:", "  boost: 2",
        "---",
        "",
        f"# {cls} Progression",
        "",
        f"<!-- This page is generated. Edit tools/classes/guides/{slug}.yml, then run tools/classes/build.py. -->",
        "",
        f'<div class="guide-head" data-class="{slug}" markdown>',
        "",
        f':codex-{slug}:{{ .fc-sigil aria-hidden="true" }} <span class="gh-kind">Class progression</span> {badges}',
        "",
        f'<nav class="gh-jump" aria-label="Jump to chapter">{" ".join(jump)}</nav>',
        "",
        "</div>",
        "",
    ]
    if g.get("aka"):
        out += [f"**Also called:** {g['aka']}", "{: .fc-aka }", ""]
    out += md_block(g["intro"])
    out += [
        f'!!! info "Current as of {PAGE_DATE}"',
        "    Forever started on 4 November 2026. The talent data and the recipe data are from the game client, build "
        f"{talents_build.CLIENT_BUILD}. Spell levels, quests and zones that Forever did not change are Classic-era values. "
        "The raids open on 9 December, and no source has published simulations.",
        "",
        "## Pick your add-ons { #picks }",
        "",
        f"This page tells the progression of a {cls} in 9 chapters, from character creation to the raids. "
        "The main text is the same for each character. An **add-on** adds the text for 1 selection: your race, your talents or your equipment.",
        "",
    ]
    out += picker(slug, g)
    out += [
        '<div class="grid cards fc-addon-cards" markdown>',
        "",
        f"-   :material-star-four-points: **[Talents add-on](talents.md)**",
        "",
        f"    All {len(talents)} talents with a rating, a talent for each level and the level 60 builds.",
        "",
        f"-   :material-shield-sword: **[Equipment add-on](equipment.md)**",
        "",
        "    The equipment sets, the items for each level range, enchants and consumables.",
        "",
        f"-   :material-account-group: **Race add-ons**",
        "",
        "    " + " ".join(f"[{r['name']}]({r['id']}.md){{ .fc-chip }}" for r in races),
        "",
        "</div>",
        "",
    ]

    for (cid, rng, prefix), ch in zip(CHAPTERS, g["chapters"]):
        out += [f"## {prefix}: {ch['title']} {{ #{cid} }}", ""]
        out += md_block(ch["story"])

        if cid == "start":
            if g.get("glance"):
                out += [f'<aside class="infobox" data-class="{slug}" markdown>', f'<p class="infobox-title">{cls} at a glance</p>', "", "| | |", "|---|---|"]
                out += [f"| **{k}** | {v} |" for k, v in g["glance"]] + ["", "</aside>", ""]
            if g.get("strengths") and g.get("weaknesses"):
                out += ['<div class="proscons" markdown>', '<div class="pros" markdown>', "", "Strengths", ""]
                out += [f"- {s}" for s in g["strengths"]] + ["", "</div>", '<div class="cons" markdown>', "", "Weaknesses", ""]
                out += [f"- {s}" for s in g["weaknesses"]] + ["", "</div>", "</div>", ""]
            chg = g.get("changes") or {}
            if chg:
                out += ['!!! forever "What Forever changed"']
                if chg.get("added"):
                    out += ["    **Additions**", "", "    " + " ".join(f"**{a}**{{ .pill .pill--new }}" for a in chg["added"]), ""]
                if chg.get("removed"):
                    out += ["    **Removals**", "", "    " + " ".join(f"**{a}**{{ .pill .pill--removed }}" for a in chg["removed"]), ""]
                out += [f"    - {n}" for n in chg.get("notes") or []]
                out += ["", "    All classes: [cross-class changes](../../characters/classes/index.md#cross-class-changes).", ""]

        if ch.get("train"):
            out += ["| Level | You train | Why it is important |", "|---|---|---|"]
            out += [f"| {r[0]} | **{r[1]}** | {r[2] if len(r) > 2 else ''} |" for r in ch["train"]] + [""]
        if ch.get("dungeons"):
            out += ["**Dungeons in this chapter**", ""]
            for d in ch["dungeons"]:
                d = {"id": d} if isinstance(d, str) else d
                if d.get("id"):
                    link, title = place(d["id"])
                    name = f"[{d.get('name') or title}]({link})"
                else:
                    name = d["name"]
                lv = f" **{d['levels']}**{{ .lvl }}" if d.get("levels") else ""
                note = f": {d['note']}" if d.get("note") else ""
                out.append(f"- {name}{lv}{note}")
            out.append("")
        if ch.get("extra"):
            out += md_block(ch["extra"])
        if ch.get("warn"):
            out += ['!!! warning "Caution"'] + ["    " + ln for ln in str(ch["warn"]).strip().splitlines()] + [""]
        if ch.get("tip"):
            out += ['!!! tip "Tip"'] + ["    " + ln for ln in str(ch["tip"]).strip().splitlines()] + [""]
        if ch.get("hardcore"):
            out += ['!!! hardcore "Hardcore"'] + ["    " + ln for ln in str(ch["hardcore"]).strip().splitlines()] + [""]

        # ---- add-ons of this chapter
        blocks = []
        # race: the faction route, then the note of each race
        if cid == "start":
            for r in races:
                body = [f"{r['pitch'].strip()} **{FACTIONS[r['faction']]}**{{ .pill .pill--{r['faction']} .pill--sm }}"
                        + (" **New**{ .pill .pill--new .pill--sm }" if str(r["status"]).lower().startswith("new") else "")]
                blocks += addon("race", [r["id"]], "Race", r["name"], body, (f"{r['id']}.md", f"{r['name']} {cls}"), r["id"] == first_race)
        else:
            for f, label in FACTIONS.items():
                txt = (g["factions"].get(f) or {}).get(cid)
                if txt and by_faction[f]:
                    blocks += addon("race", by_faction[f], "Race", f"{label} route", md_block(txt), None, first_race in by_faction[f])
            for r in races:
                body = []
                if cid == "l1":
                    body += md_block(r["start"])
                if (r.get("notes") or {}).get(cid):
                    body += md_block(r["notes"][cid])
                blocks += addon("race", [r["id"]], "Race", r["name"], body, (f"{r['id']}.md", f"{r['name']} {cls}"), r["id"] == first_race)
        # talents
        for p in g["paths"]:
            body = []
            lev = builds[p["leveling"]]
            if cid == "start":
                body += md_block(p["pitch"])
                body += [f"Leveling build: **{lev['name']}**. Level 60 builds: " + ", ".join(f"**{builds[e]['name']}**" for e in p["endgame"]) + ".", ""]
                if p.get("gear"):
                    gname = next(s2["name"] for s2 in g["gear"] if s2["id"] == p["gear"])
                    body += [f"Usual equipment set: **{gname}**.", ""]
            elif rng:
                if (p.get("play") or {}).get(cid):
                    body += md_block(p["play"][cid])
                rows = chapter_talent_rows(points[p["id"]], *rng)
                if rows:
                    body += ["| Level | Talent | Rank | Why |", "|---|---|---|---|"]
                    for r in rows:
                        lv = f"{r['lo']}" if r["lo"] == r["hi"] else f"{r['lo']}–{r['hi']}"
                        body.append(f"| {lv} | **{r['name']}** | {r['rank']}/{r['max']} | {r['why']} |")
                    body += ["", f"Points at level {rng[1]}: **{split_at(points[p['id']], talents, rng[1])}** ({' / '.join(tree_names)}).", ""]
            else:
                if (p.get("play") or {}).get(cid):
                    body += md_block(p["play"][cid])
                if cid == "raid" and p.get("priority"):
                    body += ['<div class="priority" markdown>', ""]
                    body += [f"{i}. {line}" for i, line in enumerate(p["priority"], 1)]
                    body += ["", "</div>", ""]
                if cid == "l60":
                    body += [f"The leveling build ends at **{split_at(points[p['id']], talents, 60)}**. The level 60 builds of this path:", ""]
                    for e in p["endgame"]:
                        b = builds[e]
                        ranks = {n: 0 for n in talents}
                        spent = [0, 0, 0]
                        for st in b["steps"]:
                            ranks[st[0]] += int(st[1])
                            spent[talents[st[0]]["tree_i"]] += int(st[1])
                        link = talents_build.calc_link(slug, talents, tree_names, ranks)
                        body.append(f"- **{b['name']}** ({'/'.join(map(str, spent))}, {b['role']}): [talent calculator]({link})")
                    body.append("")
            blocks += addon("talents", [p["id"]], "Talents", p["name"], body,
                            ("talents.md#leveling-builds" if rng or cid == "start" else "talents.md#level-60-builds", f"{cls} talents"),
                            p["id"] == first_path)
        # equipment
        for s in g["gear"]:
            body = []
            if cid == "start":
                body += md_block(s["pitch"]) + [f"Stat priority: {s['stats']}", ""]
            c = (s.get("chapters") or {}).get(cid) or {}
            if c.get("text"):
                body += md_block(c["text"])
            body += item_table(c.get("items"), errors, f"{slug}/gear {s['id']}/{cid}")
            blocks += addon("gear", [s["id"]], "Equipment", s["name"], body, (f"equipment.md#{s['id']}", f"{cls} equipment"), s["id"] == first_gear)
        if blocks:
            out += ['<div class="fc-addons" markdown>', ""] + blocks + ["</div>", ""]

        if ch.get("goals"):
            out += [f"**Before you continue**", ""] + [f"- [ ] {goal}" for goal in ch["goals"]] + [""]

    if g.get("professions"):
        out += ["## Professions { #professions }", ""] + md_block(g["professions"])
    if g.get("legacy"):
        out += ["## Legacy talents { #legacy }", ""] + md_block(g["legacy"])
    if g.get("mistakes"):
        out += ["## Common mistakes", ""] + [f"- {m}" for m in g["mistakes"]] + [""]
    if g.get("faq"):
        out += ["## FAQ", ""]
        for f in g["faq"]:
            out += [f'??? question "{f["q"]}"', f"    {f['a'].strip()}", ""]
    out += ["## Sources", "", f'??? quote "{len(g.get("sources") or []) + 2} sources"', "",
            f"    - [wowforevertalents.com: {cls} talents, read from the client]({talents_build.CALC}/{slug}/)",
            f"    - [wowforevertalents.com: profession recipes, read from the client]({talents_build.CALC}/professions/)"]
    out += [f"    - [{s['title']}]({s['url']})" for s in g.get("sources") or []] + [""]
    return "\n".join(out)


# ---------------------------------------------------------------- equipment page

def render_equipment(slug, g, errors):
    cls = g["class"]
    eq = g["equipment"]
    badges = " ".join(BADGES[b] for b in g["badges"])
    jump = [f'<a href="#{s["id"]}">{html.escape(s["name"])}</a>' for s in g["gear"]]
    jump += ['<a href="#enchants-and-consumables">Enchants</a>'] if eq.get("enchants") or eq.get("consumables") else []
    out = [
        "---",
        f'description: "{eq.get("description") or f"{cls} equipment for WoW: Forever: the equipment sets, the items for each level range, enchants and consumables."}"',
        "tags:", f"  - {cls}",
        "---",
        "",
        f"# {cls} Equipment",
        "",
        f"<!-- This page is generated. Edit tools/classes/guides/{slug}.yml, then run tools/classes/build.py. -->",
        "",
        f'<div class="guide-head" data-class="{slug}" markdown>',
        "",
        f':codex-{slug}:{{ .fc-sigil aria-hidden="true" }} <span class="gh-kind">Add-on · Equipment</span> {badges}',
        "",
        f'<p class="gh-note" markdown>Read with the [{cls} progression](index.md). This page gives the full equipment data for each set.</p>',
        "",
        f'<nav class="gh-jump" aria-label="Jump to section">{" ".join(jump)}</nav>',
        "",
        "</div>",
        "",
        f'!!! info "Current as of {PAGE_DATE}"',
        "    The client data gives the name and the skill of each crafted item, but not its stats. "
        "A **Classic-era** label shows an item or a value from Classic that no source confirms for Forever. Read the tooltip in the game.",
        "",
    ]
    out += md_block(eq["intro"])
    out += ["## Equipment sets", "", "| Set | Use it for | Stat priority |", "|---|---|---|"]
    out += [f"| [{s['name']}](#{s['id']}) | {s['pitch'].strip()} | {s['stats']} |" for s in g["gear"]] + [""]
    out += ["## What a " + cls + " can equip { #proficiencies }", "", "| Type | Available | Notes |", "|---|---|---|"]
    out += [f"| **{a}** | {b} | {c} |" for a, b, c in eq["proficiencies"]] + [""]
    if eq.get("rules"):
        out += ["## Item rules in Forever { #rules }", ""] + [f"- {r}" for r in eq["rules"]] + [""]
    for s in g["gear"]:
        out += [f"## {s['name']} {{ #{s['id']} }}", "", s["pitch"].strip(), "", f"**Stat priority:** {s['stats']}", ""]
        for cid, rng, prefix in CHAPTERS:
            c = (s.get("chapters") or {}).get(cid) or {}
            if not c.get("text") and not c.get("items"):
                continue
            out += [f"### {prefix} {{ #{s['id']}-{cid} }}", ""]
            if c.get("text"):
                out += md_block(c["text"])
            out += item_table(c.get("items"), errors, f"{slug}/gear {s['id']}/{cid}")
    if eq.get("enchants") or eq.get("consumables"):
        out += ["## Enchants and consumables", ""]
        if eq.get("enchants"):
            out += ["| Slot | Enchant | Notes |", "|---|---|---|"] + [f"| {a} | **{b}** | {c} |" for a, b, c in eq["enchants"]] + [""]
        if eq.get("consumables"):
            out += ["| Stage | Consumable | Notes |", "|---|---|---|"] + [f"| {a} | **{b}** | {c} |" for a, b, c in eq["consumables"]] + [""]
    if eq.get("sources"):
        out += ["## Sources", ""] + [f"- [{s['title']}]({s['url']})" for s in eq["sources"]] + [""]
    return "\n".join(out)


# ---------------------------------------------------------------- main

def main(argv):
    only_check = "--check" in argv
    want = [a for a in argv if not a.startswith("--")]
    slugs = [s for s in ORDER if (HERE / "guides" / f"{s}.yml").exists() and (not want or s in want)]
    errors, pages = [], {}
    for slug in slugs:
        errs: list[str] = []
        try:
            g = yaml.safe_load((HERE / "guides" / f"{slug}.yml").read_text(encoding="utf8"))
            tree, tguide = talents_build.load(slug)
            talents = talents_build.index_talents(tree)
            tree_names = [t["name"] for t in tree["trees"]]
            check(slug, g, tguide, talents, errs)
            if not errs:
                for b in tguide["builds"]:
                    talents_build.walk(b, talents, tree_names, errs, f"{slug}/{b['id']}")
            if not errs:
                pages[slug] = (render_progression(slug, g, tguide, talents, tree_names, errs), render_equipment(slug, g, errs))
        except (KeyError, TypeError, ValueError, AttributeError, yaml.YAMLError) as e:
            errs.append(f"{slug}: {type(e).__name__}: {e}")
        errors += errs
    if errors:
        seen = []
        for e in errors:
            if e not in seen:
                seen.append(e)
        print("\n".join(seen))
        print(f"\n{len(seen)} error(s). Nothing written.")
        return 1
    if only_check:
        print("OK:", ", ".join(pages))
        return 0
    for slug, (prog, equip) in pages.items():
        folder = DOCS / "guides" / slug
        (folder / "index.md").write_text(prog, encoding="utf8", newline="\n")
        (folder / "equipment.md").write_text(equip, encoding="utf8", newline="\n")
    print("Wrote:", ", ".join(pages))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf8")
    sys.exit(main(sys.argv[1:]))
