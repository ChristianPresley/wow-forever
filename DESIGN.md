# Forever Codex design system

This is a summary of the November 2026 UI overhaul. The overhaul was based on six research reports covering navigation, typography, colour and accessibility, game-wiki components, layout and motion, and MkDocs capabilities.

## Where things live

| File | What it does |
|---|---|
| `docs/stylesheets/extra.css` | All tokens and component styles. The numbered sections run: fonts → colour tokens → chrome → type → focus → tables → admonitions → tabs → cards → chips → components → hero → touch → preferences |
| `overrides/main.html` | Full page titles ("Orc Rogue · Forever Codex"), the announcement bar, and prev/next labels that include the class |
| `overrides/partials/content.html`, `combo-switcher.html` | The race/class chip switcher under the H1 of every guide page. It is generated from the nav |
| `overrides/partials/footer.html` | A copy of Material's footer that uses the full guide titles |
| `docs/javascripts/codex.js` | Ctrl/⌘+K opens search. Scrollable tables become labelled, focusable regions |

## Principles

- **Accessibility.** The site targets WCAG 2.2 AA, with APCA used as a quality bar.
  - Prose links are always underlined.
  - Every element shares one 2px focus ring: blue in the light theme, gold in the dark theme and on the navy header.
  - Admonitions are grouped into six families that stay distinguishable for colour-blind readers.
  - Colour is never the only cue.
- **Type.**
  - Alegreya (a calligraphic "codex" serif) for H1–H3; Inter for body text, tables and UI.
  - Both fonts are self-hosted at build time by the `privacy` plugin.
  - Body text is 17–18px, prose is capped at 72ch, and tables use tabular figures.
- **Colour.**
  - Light and dark token sets are built in OKLCH and shipped as hex.
  - The dark theme uses warm off-white text on a navy-black background, never #000 or #fff.
  - Gold is used for fills and decoration only. It appears as text only in its darker `--fc-gold-text` step.
- **Original identity.** No game assets.
  - Each class has its own original hue (`--fc-c-*`), used only as an accent next to the class name.
  - There is one ornament family: the gilt diamond (`hr`) and the hairline under the H1.
- **Motion.**
  - Durations are 100, 200 and 300 ms, with `cubic-bezier(.2,0,0,1)` easing.
  - All motion is removed under `prefers-reduced-motion`.
  - A reading-progress hairline uses CSS scroll timelines.

## Authoring components

```markdown
**Tank**{ .badge .tank }  **Healer**{ .badge .heal }  **DPS**{ .badge .dps }  **New**{ .badge .new }
**S**{ .tier .tier-s }  …  **D**{ .tier .tier-d }
**4/5**{ .stars .s4 }                 <!-- stars drawn in CSS; screen readers hear "4/5" -->
**10–20**{ .lvl }                      <!-- level-range chip -->
[Orc](rogue/orc.md){ .fc-chip }

!!! conflict "Sources disagree on …"   <!-- also: forever, unconfirmed, rotation, hardcore; ??? spoiler -->

<aside class="infobox" markdown>        <!-- floated quick facts; use a "| | |" table inside -->
<div class="steps" markdown>            <!-- numbered walkthrough with a route line; wrap an <ol> -->
<div class="milestones" markdown>       <!-- talent timeline; wrap a definition list -->
<div class="priority" markdown>         <!-- rotation priority; wrap an <ol> -->
<div class="fc-matrix" markdown>        <!-- compact comparison grid, sticky first column -->
```

Guide pages carry `tags:` front matter (class, race, faction), which feeds search and `docs/tags.md`.

## Deferred

- **Social cards.** These need cairo, so they would have to be CI-gated with `enabled: !ENV [CI, false]`.
- **Blog/RSS patch notes.**
- **Zensical migration.** Re-evaluate by March 2027, before Material's end-of-life on 5 May 2027.

## Round 2 additions (8 Nov 2026)

| Area | Where |
|---|---|
| Identity: crest, favicon and app icons, 9 class sigils + faction emblems (`:codex-mage:` …), hero art, textures | `docs/assets/`, `overrides/.icons/codex/`, `docs/stylesheets/identity.css` |
| Performance & SEO: self-hosted subset fonts with preload, meta descriptions, Open Graph, JSON-LD, canonical URLs, git-dated sitemap, robots.txt, CI-only social cards, minify/optimize | `overrides/main.html`, `overrides/sitemap.xml`, `layouts/`, `deploy.yml` |
| Interactive: guides-hub filter, glossary tooltips (`includes/abbreviations.md`), mobile "On this page", copy-section links, leveling step checklists, `?` shortcut help | `docs/javascripts/codex.js`, `docs/stylesheets/interactive.css`, `overrides/partials/` |
| Guides: guide headers, steps, milestones, rotation priorities, ability cards | `docs/guides/**`, `docs/stylesheets/guides.css` |
| Reference: infoboxes, hub cards, Forever/unconfirmed callouts, aliases, class→guide bridges | `docs/**`, `docs/stylesheets/reference.css` |
| Quality gates: axe (both schemes), html-validate, links, lychee, Lighthouse CI | `.github/workflows/quality.yml`, `tests/`, `package.json` |

Local checks: `npm ci`, then `npm run test` (and `npm run test:lhci`); see `tests/README.md`.
The one remaining axe finding is `target-size` on sidebar links that are partially scrolled out of the sidebar's own viewport, which is a known axe false positive for clipped scroll containers.

## Visual element library (8 Nov 2026)

`docs/stylesheets/components.css` adds pills (status, change, faction, class, armour, resource, difficulty, label-value; soft, solid and outline styles), spec strips, stat tiles, timelines, meters, pros/cons, price cards and labelled dividers. The live reference with copy-paste Markdown is the **Style guide** page (`docs/community/style-guide.md`).

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
