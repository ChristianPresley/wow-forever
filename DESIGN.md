# Forever Codex design system

This is a summary of the November 2026 UI overhaul. The overhaul was based on six research reports covering navigation, typography, colour and accessibility, game-wiki components, layout and motion, and MkDocs capabilities.

## Where things live

| File | What it does |
|---|---|
| `docs/stylesheets/extra.css` | All tokens and the base component styles. The numbered sections run: fonts and tokens → colour tokens → chrome (header, search, tabs, sidebar, path, article footer, footer) → type → focus → tables → admonitions → tabs → cards → chips and tags → components → hero → touch → preferences |
| `overrides/main.html` | Full page titles ("Orc Rogue · Forever Codex", "Mage Talents · Forever Codex"), the announcement bar and its end date, and prev/next labels that include the class |
| `overrides/partials/content.html`, `combo-switcher.html` | The switcher line below the meta row of every add-on page (Talents, Equipment, races). It is generated from the nav |
| `overrides/partials/header.html`, `nav.html`, `source.html` | Material's header and drawer without the repository widget. The header topic is the full guide title |
| `overrides/partials/path.html` | The breadcrumb. A section does not show in the path of its own index page |
| `overrides/partials/source-file.html`, `tags.html` | The article footer: tags, "Updated" with the date, and the edit link. A generated page shows its date in the meta row, not here |
| `overrides/partials/footer.html` | Previous and next with the full guide titles, then the bottom bar |
| `docs/javascripts/codex.js` | Ctrl/⌘+K opens search. Scrollable tables become labelled, focusable regions, and long tables keep their header row in view. The A to Z row of the glossary. The "On this page" button for phones and tablets |

## Principles

- **Accessibility.** The site targets WCAG 2.2 AA, with APCA used as a quality bar.
  - Prose links are always underlined.
  - Every element shares one 2px focus ring: blue in the light theme, gold in the dark theme and on the navy header.
  - Admonitions are grouped into six families that stay distinguishable for colour-blind readers.
  - Colour is never the only cue.
- **Type.**
  - Alegreya (a calligraphic "codex" serif) for H1–H3; Inter for body text, tables and UI.
  - Both fonts are self-hosted at build time by the `privacy` plugin.
  - Body text is 16px on phones and 17px from 960px. Prose is 34rem wide at most (about 70 characters), also on a wide page, and tables use tabular figures.
  - All sizes come from the 7-step scale `--fc-fs-*` (see *Foundations*).
- **Colour.**
  - Light and dark token sets are built in OKLCH and shipped as hex.
  - The dark theme uses warm off-white text on a navy-black background, never #000 or #fff.
  - Gold is for fills, for the current item (active tab, active page, selected chip in the dark theme) and for the rule under the H1. It appears as text only in its darker `--fc-gold-text` step.
  - Links use `--fc-link` (blue) in both themes.
- **Original identity.** No game assets.
  - Each class has its own original hue (`--fc-c-*`), used only as an accent next to the class name.
  - There is one ornament: the short gilt rule under the H1. An `hr` is a plain hairline. Surfaces are flat: no texture, no glow, no shadow.
- **Motion.**
  - Durations are 100, 200 and 300 ms, with `cubic-bezier(.2,0,0,1)` easing.
  - All motion is removed under `prefers-reduced-motion`.

## Authoring components

```markdown
**Tank**{ .badge .tank }  **Healer**{ .badge .heal }  **DPS**{ .badge .dps }  **New**{ .badge .new }
**S**{ .tier .tier-s }  …  **D**{ .tier .tier-d }
**4/5**{ .stars .s4 }                 <!-- stars drawn in CSS; screen readers hear "4/5" -->
**10–20**{ .lvl }                      <!-- level-range tag -->
[Orc](rogue/orc.md){ .fc-chip }

!!! conflict "Sources disagree on …"   <!-- also: forever, unconfirmed, rotation, hardcore; ??? spoiler -->

<aside class="infobox" markdown>        <!-- floated quick facts; use a "| | |" table inside; put it before the lede -->
<div class="steps" markdown>            <!-- numbered walkthrough with a route line; wrap an <ol> -->
<div class="priority" markdown>         <!-- rotation priority; wrap an <ol> -->
<div class="fc-matrix" markdown>        <!-- compact comparison grid -->
<div class="fc-data" data-prose="1 5" markdown>   <!-- data table: one line for each cell, columns 1 and 5 wrap -->
<div class="fc-stack" markdown>         <!-- table with long text in 2 or more columns: on a phone each row is a block -->
<div class="stats" markdown>            <!-- stat strip: "- **value** label" -->
<div class="fc-glossary" markdown>      <!-- definition list in 2 columns, with an A to Z row -->
```

Guide pages carry `tags:` front matter (class, race, faction), which feeds search and `docs/tags.md`. The tags show in the article footer.

## Foundations (round 3, 10 Nov 2026)

The tokens are in section 1 of `docs/stylesheets/extra.css`. A new rule uses a token, not a raw value.

| Group | Tokens | Rule |
|---|---|---|
| Type | `--fc-fs-xs` .68rem, `--fc-fs-sm` .75rem, `--fc-fs-body` .8rem (.85rem from 960px), `--fc-fs-lede` .9rem (.95rem), `--fc-fs-h3` 1.05rem, `--fc-fs-h2` 1.35rem, `--fc-fs-h1` 1.75rem (2rem) | 1rem is 20px. `xs` is the minimum size: tags, chips, labels, captions, navigation. `sm` is for tables, callouts and boxes. The steps are fixed. Do not use `clamp()` with `vw`: the CSS minifier removes the spaces around `+` and the browser drops the rule |
| Weight | 400, 500, 600, 700 | Inter is a 400–700 variable font |
| Radius | `--fc-radius-s` .2rem, `--fc-radius` .3rem, `--fc-radius-full` | Small for tags, tier letters and inputs. Medium for boxes, cards and tables. Full for chips and buttons. `50%` only for circles |
| Border | `--fc-border`, `--fc-border-strong` | One hairline for each box and table. The strong line for chips and for a box that needs emphasis |
| Spacing | `--fc-space-1` to `--fc-space-7` | Box padding `--fc-space-3` `--fc-space-4`, gap in a box `--fc-space-2`, margin between components `--fc-space-5`, grid gap `--fc-space-3` |

**Shape tells function** (`extra.css`, section 11):

- A **tag** is a static label: `.badge`, `.pill`, `.lvl`, `.pts`, `.ability-type`, `.tt-new`, `.fc-alias`, `em.unconfirmed`. It is a small rectangle with no border and no hover. A tag that is longer than its line wraps, but not in a table cell. The tone comes from `--pt` (fill) and `--px` (text).
- A **chip** is something that you can click: `.fc-chip`, the picker options, the filter options, `.fc-done`, the reset buttons, `.md-tag`. It is fully round, with hover, focus and selected states. Selected is a navy fill in the light theme and a gold fill in the dark theme.
- The **tier letter** (`.tier`) is the only filled tile.
- The pill variants `--sm`, `--lg`, `--solid`, `--outline`, `--kv`, the armour pills and the resource pills do not exist. A page that has one of these classes shows the standard tag.

**Boxes.** A box (`.infobox`, `.fc-pick`, `.verdict`, `.ability-card`, `.fc-goals`, stat tiles, pros and cons, cards) is a hairline border, the medium radius and the `--fc-surface-1` fill. It has no shadow and no coloured edge. A card that is one link gets the strong border and a small lift on hover. Only callouts and add-on blocks (`.fc-addon`) have a coloured bar on the left.

**Callouts.** A callout is a hairline box with a faint tint of its family, a left bar, and a title with no fill. The bar, the icon and the title text use the colour of the same family. The base rule uses `:not([hidden])` to get the specificity of Material's rules for each type, so no Material colour shows.

**UI labels.** Legends, kinds and captions (`.fc-meta__kind`, `.fc-pick__legend`, `.fc-addon__kind` and others) share one rule in section 5 of `extra.css`: Inter, `--fc-fs-xs`, weight 600, upper case. Alegreya SC is only for the kicker of the home hero.

**Arrival marker.** When you go to a heading (`#id`), `codex.js` adds `.fc-flash` and a thin gold bar fades at the left of the heading. With `prefers-reduced-motion`, the script adds nothing.

## Chrome and navigation (round 3, 10 Nov 2026)

The styles are in section 4 of `docs/stylesheets/extra.css`. The "On this page" button is in `interactive.css`.

| Part | How it works |
|---|---|
| Top | 3 bars: the announcement, the header (sticky) and the tabs (not sticky). There is no repository widget. The content starts `--fc-space-5` below the tabs: the two sidebars and the breadcrumb share that top edge |
| Announcement | One line at each width. Text in `.fc-announce__more` does not show on phones. `fc_announce_until` in `overrides/main.html` is the end date: from that date the head script sets `data-fc-noannounce` and the bar does not paint. Change the text and the date together |
| Search | The field is 15rem wide and shows `Ctrl K` (`⌘ K` on a Mac) from 60em, but not on touch devices |
| Sidebar | `navigation.sections` is off. Only the group of the current page is open, and `navigation.prune` removes the links of the closed groups from the HTML. An open group hangs from a hairline. The current page has gold text, weight 600 and the gold bar of the table of contents |
| Nav titles | The nav gives `Talents` and `Equipment` a short title, as it does for the races. `full_title` in `overrides/main.html` adds the class for the `<title>`, the header topic, previous and next, the tags index and the social cards ("Mage Talents", "Gnome Mage"). If you add an add-on type, add its slug to `full_title`, to `overrides/fragments/tags/default/listing.html` and to `layouts/codex.yml` |
| Sidebar titles | The section name and "On this page" are plain caps labels: no box, not sticky |
| Breadcrumb | Desktop shows the path to the parent. Phones show 1 item: a back link to the parent, with a chevron that points left |
| Article footer | `.fc-pagemeta` ends each article: the tags (chips with a "Tags" label), "Updated 9 November 2026", and "Edit this page on GitHub". There are no tags above the H1 and no edit icon. A page shows 1 date with 1 label: a generated page has "Updated" in its meta row, so its footer has only the tags. A tag that is a link is a chip. The name of a group on the Tags page is a plain heading |
| Generated pages | The 3 generators write `generated: true` in the front matter. A page with this key has no edit link |
| Previous and next | 2 hairline cards on the page surface. Both titles show at each width |
| Bottom bar | The copyright, the "Keyboard shortcuts" button (not on touch devices or phones) and the one link to GitHub |
| Floating control | There is 1: the "On this page" button. `codex.js` shows it only below 60em and only on a page with 3 or more H2 sections. Its list starts with "Top of page", so there is no "Back to top" button. It becomes a round icon button after the page scrolls 200px, on phones and on tablets |
| 404 | A standard page: H1, text, 2 buttons and a row of chips. The links use `fc_root`, so a preview build stays on the preview |

## Data pages and shared components (round 3, 10 Nov 2026)

| Part | How it works |
|---|---|
| Tables | One style, in section 7 of `extra.css`: `--fc-fs-sm` text, an `--fc-fs-xs` header on `--fc-surface-2`, hairline rows, a hover tint, tabular figures. Material's 5rem minimum column width is off, so a column is as wide as its content. The table is a table box (`display: table`), so its border is the edge of its cells. In `.fc-data` and in an infobox it fills its box. A table that scrolls sideways is 38rem wide at minimum, so its text columns do not become 1 word wide. A route table (*Levels*, *Zone*) gets a tick column from `codex.js`, which marks the table with `data-fc-route`, not with a class, so the table keeps this style. There is no zebra |
| Numeric columns | The Markdown separator row sets the alignment (`---:`). A right-aligned cell does not wrap, and a first column that is right-aligned is not medium weight. `.fc-na` is the muted dash for a value that does not exist |
| Sticky header | `labelScrollers` in `codex.js` adds `.fc-sticky` to the wrapper of a table that fits its column and has more than 15 rows, or that is in a `.fc-sticky` wrapper. The header row then sticks at `--fc-sticky-top` (2.4rem, the header height). Set this variable on a page that has a second sticky bar. The script runs again when the window size, a `<details>` or a content tab changes |
| Wide tables | A table that does not fit scrolls sideways in its wrapper, with a fade and a shadow at the hidden side (the table has no fill of its own, so the shadow of the wrapper shows). The script makes the wrapper a labelled, focusable region. In `.fc-data`, `.fc-matrix` and `.compare` the first column of such a table stays in view |
| Data tables | `<div class="fc-data" data-prose="1 5" markdown>`: the table uses the full column, each cell is one line, and the columns in `data-prose` wrap. On phones a text column is 11rem wide at minimum (the first column 6.5rem), so a row is 1 to 3 lines and the table scrolls sideways. `tools/professions/build.py` writes all its tables this way (`data_table`) |
| Tables with long text | `<div class="fc-stack" markdown>`: on a phone each row is a block, not a row of narrow cells. The first cell is the title. Each other cell starts with the name of its column (`data-label`, from `initStackTables` in `codex.js`, which also gives the table its roles again). The generators use it for *Quick picks*, *Equipment sets*, *Enchants and consumables* and the *Professions* table of a progression. The Races page uses it for the racial abilities. The talent table (`.fc-talents`) shares the rule |
| Page width | `wide: true` in the front matter adds a hidden `.fc-wide` marker (`overrides/partials/content.html`). From 76.25em the content column of that page grows to the right, by 9rem at most, and the sidebar stays under the logo. Prose keeps its 34rem measure. The profession pages, the Talents add-ons, the dungeon list, the raid list and the Races page use it |
| Infobox | 15rem wide, floated right from 60em, and before the lede in the source. Its table fills the box, with no inner surface. A first section that is a list starts beside the infobox, and the lines of that list use the full width below the box. `.infobox--row` (the facts of a class progression) has no float: the box is as wide as the text, and from 45em its facts are in 2 columns. A table, a card grid and a stat strip go below it. The text beside an infobox has the body size, not the lede size |
| Cards | One component, `.grid.cards`. The grid never leaves 1 card alone: 3, 5, 7 and 9 cards use 3 columns (a 7th card fills its row), and 4 cards use 2 columns. `.fc-start` on the home page puts 4 cards in 1 row |
| Stat strip | One component: `.stats` (`.specs` is the same). Joined cells, the value in Alegreya at `--fc-fs-h3`, then the label |
| Home | The hero holds the kicker, the H1, 1 sentence (2 more from 45em, in `.fc-hero__more`), a search label that opens the site search (`.fc-hero__search`), the link "What is Forever?" and the 9 class sigils. On phones the seal does not show and the sigils are 2 rows (5 and 4). Below: 1 trust line (`.fc-note`), Start here (4 cards), Key facts, Upcoming. There is no second card grid: the tabs are that menu |
| Glossary | `.fc-glossary` wraps the definition list: terms in A to Z order, medium weight, in a column beside the definitions (1 column on phones). `initGlossary` in `codex.js` gives each term an id and adds the A to Z row (`.fc-az`, chips) |
| Sources | `.fc-sources`: each site is a closed `<details>` row with its number of sources. The page has no heading for each site, so the table of contents is short |
| Profession guides | The header is the H1, the `p.fc-meta` row (kind, type tag, "Updated" date, "Data and sources" link), the infobox and the lede. The note about the data is in the *Sources* section. A recipe that is new or changed has a tag after its name |

## Deferred

- **Social cards.** These need cairo, so they would have to be CI-gated with `enabled: !ENV [CI, false]`.
- **Blog/RSS patch notes.**
- **Zensical migration.** Re-evaluate by March 2027, before Material's end-of-life on 5 May 2027.

## Round 2 additions (8 Nov 2026)

| Area | Where |
|---|---|
| Identity: crest, favicon and app icons, 9 class sigils + faction emblems (`:codex-mage:` …), the seal and the ridge of the hero | `docs/assets/`, `overrides/.icons/codex/`, `docs/stylesheets/identity.css` |
| Performance & SEO: self-hosted subset fonts with preload, meta descriptions, Open Graph, JSON-LD, canonical URLs, git-dated sitemap, robots.txt, CI-only social cards, minify/optimize | `overrides/main.html`, `overrides/sitemap.xml`, `layouts/`, `deploy.yml` |
| Interactive: guides-hub filter, glossary tooltips (`includes/abbreviations.md`), "On this page" for phones and tablets, copy-section links, leveling step checklists, `?` shortcut help | `docs/javascripts/codex.js`, `docs/stylesheets/interactive.css`, `overrides/partials/` |
| Guides: the meta row, steps, rotation priorities, ability cards | `docs/guides/**`, `docs/stylesheets/guides.css` |
| Reference: infoboxes, hub cards, Forever/unconfirmed callouts, aliases, class→guide bridges | `docs/**`, `docs/stylesheets/reference.css` |
| Quality gates: axe (both schemes), html-validate, links, lychee, Lighthouse CI | `.github/workflows/quality.yml`, `tests/`, `package.json` |

Local checks: `npm ci`, then `npm run test` (and `npm run test:lhci`); see `tests/README.md`.
`npm run test:css` compares each source stylesheet with the built one. The CSS minifier drops the space before `:is(`, `:where(`, `:not(` or `:has(` in the first rule of an `@media` block (`.md-typeset :is(h2, h3)` becomes `.md-typeset:is(h2,h3)`, which matches nothing). Thus, do not use a descendant pseudo-class in the first rule of an `@media` block: write the selectors in full.
The one remaining axe finding is `target-size` on sidebar links that are partially scrolled out of the sidebar's own viewport, which is a known axe false positive for clipped scroll containers.

## Visual element library (8 Nov 2026)

`docs/stylesheets/components.css` adds pills (status, change, faction, class, difficulty; one soft style and one size), the stat strip, timelines, meters, pros/cons and price cards. The live reference with copy-paste Markdown is the **Style guide** page (`docs/community/style-guide.md`).

## Writing: Simplified Technical English (9 Nov 2026)

All prose in `docs/` follows a Codex profile of ASD-STE100 Simplified Technical English (STE). The goal is text that is easy to read for every reader, including readers whose first language is not English and readers who use machine translation.

### Scope

- **Rewrite:** body text, list items, table cells that hold sentences, callout bodies, captions, `description:` front matter, and link text that is a sentence.
- **Do not change:** Markdown and HTML markup, attribute lists (`{ .pill .pill--new }`), CSS classes, anchors (`{ #id }`), link targets, front-matter keys, tags, code blocks, macros, and file names.
- **Technical names stay as they are:** spell, talent, item, quest, zone, NPC, faction, race, class, profession and stat names, game terms (DPS, aggro, kiting, pull, proc, tank, rotation, cooldown, haste), and quoted titles. A technical name can contain words that STE does not approve.
- **Facts stay the same:** numbers, levels, prices, dates, sources and their attribution ("Warcraft Tavern says …"), and the meaning of every hedge ("reportedly", "not confirmed"). If a sentence is ambiguous, keep the ambiguity: do not invent a fact to make it simpler.
- **Headings:** keep heading text when it is a technical name or when other pages link to its anchor. Otherwise make it short and simple. If a heading changes and it has no `{ #id }`, add the old anchor as `{ #old-slug }` so links do not break.

### Word rules

1. Use approved STE words with their approved meaning, where a simple word exists: *use* not *utilize*, *help* not *assist*, *start* not *commence*, *get* not *obtain*, *about* not *approximately*, *more than* not *in excess of*, *because* not *since* or *as* (for a reason), *if* or *when* not *in case*, *can* not *is able to*.
2. Use one word for one meaning, and one meaning for one word. Use the same term for the same thing on every page.
3. Do not use phrasal verbs when a single verb exists: *find* not *find out*, *leave* not *head off*, *continue* not *keep on*, *get* not *pick up* (except for game idioms such as *pick up a quest*).
4. Do not use *-ing* forms as nouns or as modifiers in general prose (*Leveling* is a technical name and can stay). Write *when you level* not *while leveling*, where this makes the sentence clearer.
5. Use only the simple tenses: present, simple past and future (*will*). Do not use *would*, *could*, *should*, *might* or *may* to give an instruction or a possibility. Write *can*, *must*, or a direct command.
6. Do not use slang, jokes, idioms or metaphors: *strong* not *a beast*, *easy* not *a breeze*.
7. Keep articles (*a*, *an*, *the*) and *that* where they make the meaning clear. Do not write telegraphic text in sentences.
8. Write numbers as digits.

### Sentence rules

1. **Procedures** (steps, instructions): a maximum of **20 words** per sentence. Write one instruction per sentence. Start with a verb in the imperative (*Take the boat to Auberdine.*). If an action has a condition, put the condition first (*At level 10, train Frost Nova.*).
2. **Descriptions:** a maximum of **25 words** per sentence. Write one topic per sentence.
3. Use the **active voice**. Use the passive only in descriptions where the agent is unknown or not important.
4. Put a **warning** or **caution** before the instruction it applies to. Start with the command, then give the reason in a second sentence.
5. Do not use semicolons to join sentences. Make two sentences. Colons that introduce a list or an explanation are permitted.
6. Do not use long noun clusters. Break a cluster of more than 3 nouns with *of*, *for* or a short clause.

### Paragraph rules

1. A paragraph has one topic.
2. A paragraph has a maximum of **6 sentences**. The first sentence gives the topic.
3. Use a list when you give 3 or more parallel items.

### Lists, tables and fragments

- Short list items, table cells and pros/cons items can be fragments (*Cloth armor and few escapes*). Do not make a fragment into a long sentence.
- If a list item has a full sentence, it follows the sentence rules.

## Class progressions and add-ons (10 Nov 2026)

The **Classes** tab holds 1 folder for each class, `docs/guides/<class>/`. It replaced the old *Races & Classes* and *Class Guides* tabs. The reference pages that are not about 1 class (races, class changes, Legacy, leveling, customization) are in the *Character Reference* group of the same tab.

| Page | What it is | Source |
|---|---|---|
| `index.md` | The **progression**: a narration in 9 chapters, from character creation to the raids | Generated by `tools/classes/build.py` from `tools/classes/guides/<class>.yml` |
| `talents.md` | The **Talents add-on**: each talent with a rating, a talent for each level, the level 60 builds | Generated by `tools/talents/build.py` from `tools/talents/guides/<class>.yml` |
| `equipment.md` | The **Equipment add-on**: the equipment sets, the items for each level range, enchants, consumables | Generated by `tools/classes/build.py` |
| `<race>.md` | A **Race add-on**: racials, start zone, route | Written by hand |

Do not edit a generated page by hand. Edit the `.yml` file, then run the script:

```bash
.venv/Scripts/python.exe tools/classes/build.py            # all classes
.venv/Scripts/python.exe tools/classes/build.py mage       # one class
.venv/Scripts/python.exe tools/classes/build.py --check    # validate only
.venv/Scripts/python.exe tools/talents/build.py            # the Talents add-ons
```

### The progression file

`tools/classes/guides/mage.yml` is the reference. A file has these parts:

- **`chapters`:** exactly 9, with fixed ids: `start`, `l1`, `l10`, `l20`, `l30`, `l40`, `l50`, `l60`, `raid`. Each has a `title` and a `story`. The optional `toc` is the short label for the table of contents and the pick bar. Without it, the script uses the first clause of the title. A chapter can have `train` rows (spells by level), `dungeons`, `goals` (a checklist), `warn`, `tip`, `hardcore` and `extra` (raw Markdown).
- **`races`:** 1 entry for each Race add-on page. `start` shows in chapter `l1`. `notes` add text to other chapters.
- **`factions`:** the zone route for each chapter, for the Alliance and for the Horde.
- **`paths`:** the talent paths. A path names a leveling build and level 60 builds from the talent file. `play` tells how you fight in each chapter. The script makes the talent table of each chapter from the build order.
- **`gear`:** the equipment sets, with text and items for each chapter. A crafted item must be a recipe in `tools/professions/recipes/`. The script adds the skill.
- **`equipment`:** proficiencies, item rules, enchants and consumables for the Equipment add-on.

The script stops if the data breaks a rule: a chapter is missing, a race has no page, a build does not exist, a crafted item is not in the client data, a dungeon has no page, or a sentence breaks the STE profile (more than 25 words, a semicolon, *should / would / could / might / may*).

### Page header

Each class page has one header: the H1, one meta row, then the first paragraph. There is no box, no row of jump chips and no "Current as of" callout.

- **Meta row** (`p.fc-meta`, section 1 of `guides.css`): the class sigil in the class hue, the kind ("Class progression", "Add-on: Talents", "Add-on: Race"), the role tags, "Updated 10 November 2026" and the link **Data and sources**. `meta_row` in `tools/talents/build.py` writes it for the 3 generated pages. The Race add-ons have it by hand, without the date.
- **Data and sources** goes to the last section of the page (`#sources`). That section starts with the note on the data, and then lists the sources. On a Race add-on the link goes to the section of the progression.
- **Aliases** ("Also called") are a row of the facts box in the first chapter.
- **Switcher** (`nav.fc-switch`, `overrides/partials/combo-switcher.html`): an add-on page shows one line of chips below the meta row, for the progression and the add-ons of the class. The same add-on of the other classes is in a closed disclosure. On a phone the chips are one row that scrolls.
- The Talents and Equipment pages have `wide: true` in the front matter, so the content column is wider.

### The add-on picker

The progression shows 3 rows of radio chips: **Race**, **Talents** and **Equipment**. The label is at the left of its options. On a phone it is above them. The last line has the help text and the switch **Show all add-ons**. Each chapter holds `.fc-addon` blocks with `data-pick` and `data-value`. Only the blocks of the selection show.

| File | What it does |
|---|---|
| `overrides/main.html` (head script, `window.fcPick`) | Reads the saved selection before the first paint and writes the CSS rules into `<style id="fc-pick-css">` |
| `docs/javascripts/codex.js` (`initPicker`, `buildBar`) | Sets the radio buttons, saves a change in `localStorage` (`fc:pick:<class>`), puts it in the URL (`?race=…&talents=…&gear=…`), and makes the pick bar |
| `docs/stylesheets/guides.css`, sections 11 to 13 | The picker, the add-on blocks, the chapters and the pick bar |

Without JavaScript, the picker and the pick bar do not show, and all add-on blocks show, each with a label. The first race, path and set in the `.yml` file are the defaults.

**Add-on blocks.** The blocks of a chapter are one group (`.fc-addons`) with one neutral bar at the left. A block has no box. It has a label line ("Race · Gnome", "Talents · Arcane"), the text, and a last line with the link to the full add-on page.

### The sticky pick bar

When the picker is above the viewport, a slim bar (`.fc-pickbar`) sticks below the header. It shows the selection ("Gnome · Arcane · Quests and dungeons"), a **Change** button, the number of goals that are done, and the links to the previous and the next chapter.

- `codex.js` makes the bar. It does not exist without JavaScript.
- The element has no height, and `codex.js` sets its `top` to the height of the header. Thus the page does not move when the bar shows, and the bar is in the correct position at each width.
- **Change** opens a copy of the picker below the bar. A change there goes to the picker itself, so there is one handler. `holdPlace` keeps the text in view where it is. Escape or a press outside closes the panel, and focus goes back to the button.
- The scroll padding of the page is the header height (2.4rem), so the bar is not in the padded zone and focus on its controls does not move the page. On a progression, a link target and a chapter heading have a scroll margin of 3.6rem (section 13 of `guides.css`): they stop below the bar. `place` reads the two values to find the current chapter, so the label and the chapter links of the bar agree with the position.
- Tab from the last control of the bar goes to the first link below the bar, and Shift+Tab from the first control goes to the last link above it. When focus goes to a link that the bar covers, the page moves so that the link shows.
- A value in the URL that is not an option does not replace the saved selection.
- The chapter links of the bar and the "Next" links go to their chapter also when the URL has that hash already (`navigation.tracking` writes the hash of the section in view).
- A sticky table header stays below the bar: section 13 sets `--fc-sticky-top`.
- `initPicker` runs on each page view, so the bar is correct after instant navigation.

### Chapters

- A chapter heading (`h2.fc-ch`) has a rule above, then the level tag (`.fc-ch__lv`, "Levels 10–19"), then the title. The table of contents shows the short label ("10–19 · First talents"). The heading has it in `data-label` for `codex.js`.
- In the first chapter the facts box (`.infobox.infobox--row`) is before the story. It is as wide as the text and has no float. The strengths and weaknesses are below the story in 2 columns.
- The cautions, tips and Hardcore notes of a chapter are short callouts (`fc-inline`): no box, and the title starts the text.
- The goals (`.fc-goals`) are the one box that ends a chapter. Each box shows its count ("1 of 4"). The page total and **Clear ticks** are in the pick bar. A press on a row ticks the goal. `codex.js` saves the ticks in `localStorage` (`fc:done:<path>`).
- Each chapter ends with a link to the next chapter (`.fc-next`).

### Talent data

| File | What it does |
|---|---|
| `tools/talents/trees/<class>.json` | The tree layout from the game client: talent name, row, column, maximum rank, prerequisite. Source: wowforevertalents.com, client build 1.60.1.70862 |
| `tools/talents/guides/<class>.yml` | Codex ratings (S–D for leveling, PvE and PvP), builds, and prose for one class |
| `tools/talents/build.py` | Checks each build against the tree rules, then writes `docs/guides/<class>/talents.md` |

The script stops if a build breaks a rule: 5 points for each row, prerequisites at maximum rank, and 51 points in total.

- **Tree grid** (`.ttree`, section 10 of `docs/stylesheets/guides.css`): 4 columns that shrink with the page, so the grid fits a phone. An empty slot is a faint tile. The number at the left is the number of points that opens the row. The letter in each tile is the best of the 3 ratings of the talent.
- **Talent table** (`.fc-talents`): 5 columns: Talent, Max, What it does, Ratings, Codex verdict. The 3 ratings are tier letters in one cell, with the labels L, PvE and PvP. On a phone each talent is a block (the row-block rule of `.fc-stack`).
- A build table and the talent table of a chapter show the rank after the talent name ("Ice Shards 3/5").

## Profession guides (10 Nov 2026)

The pages in `docs/professions/` are **generated**. Do not edit them by hand.

| File | What it does |
|---|---|
| `tools/professions/recipes/<slug>.json` | Each recipe from the game client: heading, learn skill, yellow, green and grey skill, reagents, source, status against Classic. Source: wowforevertalents.com, client build 1.60.1.70862 |
| `tools/professions/guides/<slug>.yml` | The Codex guide for one profession: prose, the path from 1 to 300, recipe picks, tips and FAQ |
| `tools/professions/build.py` | Checks each path against the recipe data, computes the crafts and the materials, then writes the guide, the recipe list and the hub |

To change a guide, edit the `.yml` file, then run `.venv/Scripts/python.exe tools/professions/build.py`. Use `--check` to validate only. A profession with more than 60 recipes gets a separate `<slug>-recipes.md` page.

The script stops if a path has a gap, names a recipe that does not exist, starts a recipe below its learn skill, or continues a recipe to its grey skill. The client does not hold trainer skill requirements. Thus, a step with a trainer recipe must give `learn` and `learn_basis` (`classic` or `estimate`), and the page shows this label.
