"""Build the talent guide pages (docs/talents/*.md) from data.

Inputs
  tools/talents/trees/<class>.json   Talent trees as read from the game client
                                     (name, row, column, max rank, tooltip, prerequisite).
  tools/talents/guides/<class>.yml   Codex ratings, builds and prose for one class.

Outputs
  docs/talents/<class>.md and docs/talents/index.md

Usage
  .venv/Scripts/python.exe tools/talents/build.py            # all classes that have a .yml
  .venv/Scripts/python.exe tools/talents/build.py mage       # one class
  .venv/Scripts/python.exe tools/talents/build.py --check    # validate only, write nothing

Every build is checked against the tree rules before a page is written:
a row opens after 5 points per row above it in the same tree, a prerequisite
must be at its maximum rank, no talent goes above its maximum rank, and a
full build has exactly 51 points. The script stops with a list of errors if
a rule is broken, so a page cannot show a build that the game refuses.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = ROOT / "docs" / "talents"
ORDER = ["druid", "hunter", "mage", "paladin", "priest", "rogue", "shaman", "warlock", "warrior"]
TIERS = "SABCD"
MAX_POINTS = 51
CLIENT_BUILD = "1.60.1.70862"
DATA_DATE = "9 November 2026"
PAGE_DATE = "10 November 2026"
CALC = "https://wowforevertalents.com"
BADGES = {"tank": "**Tank**{ .badge .tank }", "heal": "**Healer**{ .badge .heal }", "dps": "**DPS**{ .badge .dps }"}


class BuildError(Exception):
    pass


def load(slug: str):
    tree = json.loads((HERE / "trees" / f"{slug}.json").read_text(encoding="utf8"))
    guide = yaml.safe_load((HERE / "guides" / f"{slug}.yml").read_text(encoding="utf8"))
    return tree, guide


def index_talents(tree):
    """name -> talent dict, with the tree name and tree index added."""
    out = {}
    for ti, tr in enumerate(tree["trees"]):
        ordered = sorted(tr["talents"], key=lambda t: (t["row"], t["col"]))
        for pos, t in enumerate(ordered):
            if t["name"] in out:
                raise BuildError(f"duplicate talent name {t['name']}")
            out[t["name"]] = dict(t, tree=tr["name"], tree_i=ti, pos=pos)
    return out


def tier_chip(letter: str) -> str:
    return f"**{letter}**{{ .tier .tier-{letter.lower()} }}"


def walk(build, talents, tree_names, errors, where):
    """Apply the steps of a build one point at a time. Returns (rows, ranks).

    rows: one dict per step chunk with level range, talent, rank reached, split and reason.
    """
    ranks = {n: 0 for n in talents}
    spent = [0, 0, 0]
    start = int(build.get("respec_at", 10))
    banked = start - 9 if "respec_at" in build else 0  # points that exist when you respec
    total = 0
    rows = []
    for step in build["steps"]:
        name, n = step[0], int(step[1])
        why = step[2] if len(step) > 2 else ""
        if name not in talents:
            errors.append(f"{where}: unknown talent '{name}'")
            continue
        t = talents[name]
        first_total = total + 1
        for _ in range(n):
            need = (t["row"] - 1) * 5
            if spent[t["tree_i"]] < need:
                errors.append(f"{where}: '{name}' needs {need} points in {t['tree']}, has {spent[t['tree_i']]}")
            for req in t.get("requires") or []:
                if ranks[req] < talents[req]["max"]:
                    errors.append(f"{where}: '{name}' needs '{req}' at {talents[req]['max']}/{talents[req]['max']}")
            if ranks[name] >= t["max"]:
                errors.append(f"{where}: '{name}' is above its maximum of {t['max']}")
            ranks[name] += 1
            spent[t["tree_i"]] += 1
            total += 1
        # levels: point k (1-based) arrives at level 9 + k
        lo, hi = 9 + first_total, 9 + total
        if banked and first_total <= banked:
            level = f"At {start}" if total <= banked else f"At {start}, then {start + 1}–{hi}" if hi > start + 1 else f"At {start}, then {hi}"
        else:
            level = f"{lo}" if lo == hi else f"{lo}–{hi}"
        rows.append({
            "level": level, "name": name, "rank": f"{ranks[name]}/{t['max']}",
            "split": "/".join(str(s) for s in spent), "why": why,
        })
    if total > MAX_POINTS:
        errors.append(f"{where}: {total} points, the maximum is {MAX_POINTS}")
    if total != MAX_POINTS and not build.get("partial"):
        errors.append(f"{where}: {total} points, a full build needs {MAX_POINTS} (or set partial: true)")
    return rows, ranks, spent, total


def calc_link(slug, talents, tree_names, ranks):
    parts = []
    for ti, _ in enumerate(tree_names):
        ordered = sorted((t for t in talents.values() if t["tree_i"] == ti), key=lambda t: t["pos"])
        parts.append("".join(str(ranks[t["name"]]) for t in ordered).rstrip("0"))
    return f"{CALC}/{slug}/?t=h" + "-".join(parts).rstrip("-")


def final_layout(talents, tree_names, ranks, spent):
    lines = []
    for ti, tn in enumerate(tree_names):
        if not spent[ti]:
            continue
        picks = sorted((t for t in talents.values() if t["tree_i"] == ti and ranks[t["name"]]), key=lambda t: t["pos"])
        items = " · ".join(f"{t['name']} {ranks[t['name']]}/{t['max']}" for t in picks)
        lines.append(f"- **{tn} ({spent[ti]}):** {items}")
    return lines


def indent(lines, n=4):
    pad = " " * n
    return [pad + ln if ln else "" for ln in lines]


def render_build(build, slug, talents, tree_names, errors):
    where = f"{slug}/{build['id']}"
    rows, ranks, spent, total = walk(build, talents, tree_names, errors, where)
    split = "/".join(str(s) for s in spent)
    out = []
    head = f"**{build['role']}**{{ .pill .pill--info }} **{split}**{{ .pill .pill--outline }}"
    if build.get("partial"):
        head += f" **{total} points**{{ .pill .pill--outline }}"
    out += [head, ""]
    out += [build["summary"].strip(), ""]
    if build["kind"] == "leveling":
        out += ["| Level | Talent | Rank | Points | Why |", "|---|---|---|---|---|"]
        for r in rows:
            out.append(f"| {r['level']} | **{r['name']}** | {r['rank']} | {r['split']} | {r['why']} |")
        out.append("")
        if not build.get("partial"):
            out += ["At level 60 the build is:", ""]
            out += final_layout(talents, tree_names, ranks, spent) + [""]
    else:
        out += final_layout(talents, tree_names, ranks, spent) + [""]
        whys = [r for r in rows if r["why"]]
        if whys:
            out += ["Key choices:", ""]
            out += [f"- **{r['name']}:** {r['why']}" for r in whys] + [""]
    for note in build.get("notes") or []:
        out += [f"- {note}"]
    if build.get("notes"):
        out.append("")
    out += [f"[Open this build in the talent calculator]({calc_link(slug, talents, tree_names, ranks)})", ""]
    return out, split, total


def render_tree(tr, gtree, talents):
    name = tr["name"]
    out = [f"## {name}", "", gtree["summary"].strip(), ""]
    # the grid, in the same layout as the in-game tree
    nrows = max(t["row"] for t in tr["talents"])
    cells = []
    for r in range(1, nrows + 1):
        cells.append(f'<li class="tt-row" style="grid-row:{r}">{(r - 1) * 5} pts</li>')
    for t in sorted(tr["talents"], key=lambda t: (t["row"], t["col"])):
        g = gtree["talents"][t["name"]]
        best = min((g["lvl"], g["pve"], g["pvp"]), key=TIERS.index)
        req = "".join(f'<span class="tt-req">Needs {r}</span>' for r in t.get("requires") or [])
        new = '<span class="tt-new">New</span>' if t["status"] == "new" else ""
        cells.append(
            f'<li class="tt-node" style="grid-row:{t["row"]};grid-column:{t["col"] + 1}">'
            f'<span class="tt-name">{t["name"]}</span>{req}'
            f'<span class="tt-meta"><span class="tier tier-{best.lower()}">{best}</span> max {t["max"]}{new}</span></li>'
        )
    out += [
        f'<div class="ttree-wrap" role="group" aria-label="{name} talent tree" tabindex="0">',
        '<ul class="ttree">', *cells, "</ul>", "</div>", "",
        f'<p class="legend">The grid shows the layout of the tree in the game. The letter is the best rating of the talent in the table below.</p>',
        "",
        "| Talent | Opens at | Max | What it does | Leveling | PvE | PvP | Codex verdict |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for t in sorted(tr["talents"], key=lambda t: (t["row"], t["col"])):
        g = gtree["talents"][t["name"]]
        label = f"**{t['name']}**"
        if t["status"] == "new":
            label += " **New**{ .pill .pill--new .pill--sm }"
        for r in t.get("requires") or []:
            label += f"<br><small>Needs {r}</small>"
        out.append(
            f"| {label} | {(t['row'] - 1) * 5} pts | {t['max']} | {g['does']} | {tier_chip(g['lvl'])} | "
            f"{tier_chip(g['pve'])} | {tier_chip(g['pvp'])} | {g.get('note', '')} |"
        )
    out.append("")
    return out


def render_class(slug, tree, guide, errors):
    talents = index_talents(tree)
    tree_names = [t["name"] for t in tree["trees"]]
    cls = guide["class"]
    # every talent must have a rating, and no rating can name a talent that does not exist
    for tr in tree["trees"]:
        gt = (guide["trees"].get(tr["name"]) or {}).get("talents") or {}
        for t in tr["talents"]:
            g = gt.get(t["name"])
            if not g:
                errors.append(f"{slug}: no rating for '{t['name']}' ({tr['name']})")
                continue
            for k in ("lvl", "pve", "pvp"):
                if str(g.get(k)) not in list(TIERS):
                    errors.append(f"{slug}: '{t['name']}' has a bad {k} tier: {g.get(k)!r}")
            if not g.get("does"):
                errors.append(f"{slug}: '{t['name']}' has no 'does' text")
        for extra in set(gt) - {t["name"] for t in tr["talents"]}:
            errors.append(f"{slug}: rating for unknown talent '{extra}' in {tr['name']}")
    if errors:
        return None, None

    builds = {b["id"]: b for b in guide["builds"]}
    rendered = {}
    for b in guide["builds"]:
        rendered[b["id"]] = render_build(b, slug, talents, tree_names, errors)

    badges = " ".join(BADGES[b] for b in guide["badges"])
    jump = ['<a href="#quick-picks">Quick picks</a>', '<a href="#leveling-builds">Leveling</a>', '<a href="#level-60-builds">Level 60</a>']
    jump += [f'<a href="#{tn.lower().replace(" ", "-")}">{tn}</a>' for tn in tree_names]
    n_talents = len(talents)
    out = [
        "---",
        f'description: "{guide["description"]}"',
        "tags:", f"  - {cls}",
        "search:", "  boost: 2",
        "---",
        "",
        f"# {cls} Talents",
        "",
        "<!-- This page is generated. Edit tools/talents/guides/%s.yml, then run tools/talents/build.py. -->" % slug,
        "",
        f'<div class="guide-head" data-class="{slug}" markdown>',
        "",
        f':codex-{slug}:{{ .fc-sigil aria-hidden="true" }} <span class="gh-kind">Talent guide</span> {badges}',
        "",
        f'<nav class="gh-jump" aria-label="Jump to section">{" ".join(jump)}</nav>',
        "",
        "</div>",
        "",
        f'!!! info "Current as of {PAGE_DATE}"',
        f"    The tree data is from the game client, build {CLIENT_BUILD}, with the server hotfixes of {DATA_DATE}. "
        f"[wowforevertalents.com]({CALC}/{slug}/) reads this data from the client. "
        f"The ratings are Codex ratings. No source has published simulations, and the raids open on 9 December. "
        f"Read this page with the [{cls} guide](../guides/{slug}/index.md).",
        "",
        guide["intro"].strip(),
        "",
        "## Quick picks",
        "",
        "| Stage | Build | Points at 60 | Why |",
        "|---|---|---|---|",
    ]
    for q in guide["quick"]:
        b = builds.get(q["build"])
        if not b:
            errors.append(f"{slug}: quick pick names unknown build '{q['build']}'")
            continue
        anchor = "#leveling-builds" if b["kind"] == "leveling" else "#level-60-builds"
        out.append(f"| {q['stage']} | [{b['name']}]({anchor}) | {rendered[b['id']][1]} | {q['why']} |")
    out += [
        "",
        "## How to read this page",
        "",
        f"The {cls} has {n_talents} talents in 3 trees. You get 1 talent point for each level from 10 to 60, for a total of {MAX_POINTS} points.",
        "",
        "- **Opens at:** the number of points that you must spend in the same tree before the row opens. Each row needs 5 more points.",
        "- **Max:** the maximum rank of the talent.",
        "- **Leveling:** the value of the talent when you quest and do dungeons from level 10 to 59.",
        "- **PvE:** the value at level 60 in dungeons and raids. This is damage, healing or tank value, for the role of the tree.",
        "- **PvP:** the value in battlegrounds and world PvP.",
        "",
        f"{tier_chip('S')} Core. Take it in each build of that type. "
        f"{tier_chip('A')} Strong. Take it when you can. "
        f"{tier_chip('B')} Good. Use it to fill points. "
        f"{tier_chip('C')} Situational or a personal preference. "
        f"{tier_chip('D')} Do not take it.",
        "",
        "## Leveling builds",
        "",
        "Each table gives the talent for each level. The *Points* column shows the points in each tree after that step.",
        "",
    ]
    for b in guide["builds"]:
        if b["kind"] == "leveling":
            out += [f'=== "{b["name"]}"', ""] + indent(rendered[b["id"]][0])
    out += [
        '!!! tip "Talented"',
        "    The Legacy talent *Talented* gives your first talent point up to 5 levels earlier. The order of the talents does not change.",
        "",
        "## Level 60 builds",
        "",
        "Dual spec becomes available at level 40 for 50g. Thus, you can keep 2 of these builds at the same time.",
        "",
    ]
    for b in guide["builds"]:
        if b["kind"] == "endgame":
            out += [f'=== "{b["name"]}"', ""] + indent(rendered[b["id"]][0])
    for tr in tree["trees"]:
        out += render_tree(tr, guide["trees"][tr["name"]], talents)
    if guide.get("faq"):
        out += ["## FAQ", ""]
        for f in guide["faq"]:
            out += [f'??? question "{f["q"]}"', f"    {f['a'].strip()}", ""]
    out += ["## Sources", "", f"- [wowforevertalents.com: {cls} talents, read from the client]({CALC}/{slug}/)"]
    for s in guide.get("sources") or []:
        out.append(f"- [{s['title']}]({s['url']})")
    out.append("")
    return "\n".join(out), rendered


def render_index(done):
    out = [
        "---",
        'description: "Talent guides for all 9 classes in WoW: Forever: each talent with a rating, a talent for each level from 10 to 60, and level 60 builds."',
        "search:", "  boost: 3",
        "hide:", "  - toc",
        "---",
        "",
        "# Talent Guides",
        "",
        "<!-- This page is generated by tools/talents/build.py. -->",
        "",
        "A talent guide for each of the **9 classes**. Each guide shows all 3 trees, gives a rating to each talent, and tells you where to put each point from level 10 to 60.",
        "",
        f'??? info "How the talent guides work · current as of {PAGE_DATE}"',
        f"    - **Tree data:** from the game client, build {CLIENT_BUILD}, as read by [wowforevertalents.com]({CALC}/).",
        "    - **Ratings:** Codex ratings from S (core) to D (do not take), for leveling, PvE and PvP. No source has published simulations.",
        "    - **Builds:** a script checks each build against the rules of the tree. Each build has a link to a talent calculator.",
        "    - The class guides give rotations, routes and gear. Find them in [Class & Race Guides](../guides/index.md).",
        "",
        "## Pick a class",
        "",
        '<div class="grid cards fc-multi fc-class-card" markdown>',
        "",
    ]
    for slug, guide in done:
        c = guide["card"]
        badges = " · ".join(b.capitalize() if b != "dps" else "DPS" for b in guide["badges"]).replace("Heal", "Healer")
        out += [
            f"-   :codex-{slug}:{{ .lg .middle }} **[{guide['class']}]({slug}.md)**",
            "",
            "    ---",
            "",
            f"    **{badges}**",
            "",
            f"    - **Leveling:** {c['leveling']}",
            f"    - **PvE at 60:** {c['pve']}",
            f"    - **PvP:** {c['pvp']}",
            "",
        ]
    out += ["</div>", ""]
    return "\n".join(out)


def main(argv):
    check = "--check" in argv
    want = [a for a in argv if not a.startswith("--")]
    slugs = [s for s in ORDER if (HERE / "guides" / f"{s}.yml").exists()]
    errors, done = [], []
    pages = {}
    for slug in slugs:
        tree, guide = load(slug)
        errs = []
        try:
            page, _ = render_class(slug, tree, guide, errs)
        except (BuildError, KeyError, TypeError) as e:
            errs.append(f"{slug}: {type(e).__name__}: {e}")
            page = None
        if errs:
            if not want or slug in want:
                errors += errs
            continue
        done.append((slug, guide))
        pages[slug] = page
    if errors:
        print("\n".join(errors))
        print(f"\n{len(errors)} error(s). Nothing written.")
        return 1
    if check:
        print("OK:", ", ".join(s for s, _ in done))
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, page in pages.items():
        if not want or slug in want:
            (OUT / f"{slug}.md").write_text(page, encoding="utf8", newline="\n")
    (OUT / "index.md").write_text(render_index(done), encoding="utf8", newline="\n")
    print("Wrote:", ", ".join(s for s in pages if not want or s in want), "+ index")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
