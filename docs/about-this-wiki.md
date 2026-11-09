---
search:
  boost: 0.5
---

# About this wiki

**Forever Codex** is a catalog of *World of Warcraft: Forever*. It uses public sources. It is an unofficial fan project. It has no connection with Blizzard Entertainment, and Blizzard does not endorse it.

## How it was built

- The research used official Blizzard posts, the Warcraft Wiki, Wikipedia, and large news and guide sites, up to **7 November 2026** (3 days after launch).
- We **paraphrased** all text. We do not copy long parts of a source.
- The [Sources](sources.md) page lists every source.

## Conventions

| Marker | Meaning |
|---|---|
| **Conflict** (note box) | Sources disagree. The box lists every version |
| **Forever** box | A change that exists only in Forever (vs. original Classic) |
| *unconfirmed*{ .unconfirmed } | Comes from only 1 source, and that source is not official |
| *fan source*{ .fan-source } | From a fan or guide site that is less reliable |
| **New**{ .pill .pill--new } | New in Forever (vs. original Classic) |
| **Official**{ .badge .official } **Stated**{ .badge .stated } **Done**{ .badge .done } | How sure we are about a dated plan (see [Roadmap](content/roadmap.md)) |
| **Tank**{ .badge .tank } **Healer**{ .badge .heal } **DPS**{ .badge .dps } | Roles a class can fill |
| <span class="fc-alias">BRD</span> **Also called** | Common abbreviations and slang. The page shows them so that search can find them ([Glossary](community/glossary.md#player-shorthand)) |

When the beta Class Deep Dives and the later pre-launch notes disagree, the wiki follows the **newer** pre-launch notes.

## Known gaps

- Boss rosters and loot for The Drowned City, Krol'dok Stronghold, Alcaz Prison, Blackmaw Hold and Shaper's Terrace
- Raid loot tables and tier sets
- Mount Hyjal and Shen'dralas quest content
- An official battleground list and brackets for WSG, AB and AV
- A Hardcore launch date and its full rules
- Official player counts

## Contributing

Each page has an edit link (the pencil icon). This link opens the Markdown source on GitHub. The site uses [MkDocs Material](https://squidfunk.github.io/mkdocs-material/). On every push to `main`, GitHub Actions deploys the site to GitHub Pages.

```bash
pip install -r requirements.txt
mkdocs serve
```
