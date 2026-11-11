---
description: Every visual element that the Forever Codex uses (pills, badges, stat strips, tables, timelines, meters, pros and cons, cards and callouts), with the Markdown to write each one.
search:
  boost: 0.5
---

# Style guide

These are the visual elements that the Codex uses. For each element, this page shows how it looks and the Markdown that makes it. Contributors can use these elements again. Every coloured element also has a word or a symbol, so the meaning never depends only on colour.

## Shape tells function

The Codex has 2 shapes for small labels. The shape tells you if you can click the element.

| Shape | What it is | Classes |
|---|---|---|
| **Tag**: a small rectangle with no border | A static label. You cannot click it, and it has no hover state | `.pill`, `.badge`, `.lvl` |
| **Chip**: a fully round outline | A link or a control. It has hover, focus and selected states | `.fc-chip`, the picker options, the filter options |

Each shape has 1 size. Do not use a tag for a link, and do not use a chip for a label.

## Pills

Pills are tags. Add them to bold text with an attribute list: `**Text**{ .pill .pill--live }`. A pill with no tone class is neutral.

### Status

<div class="pills" markdown>
**Live**{ .pill .pill--live } **Coming soon**{ .pill .pill--soon } **Planned**{ .pill .pill--planned } **Rumour**{ .pill .pill--rumor } **Official**{ .pill .pill--official }
</div>

```markdown
**Live**{ .pill .pill--live } **Coming soon**{ .pill .pill--soon } **Planned**{ .pill .pill--planned }
**Rumour**{ .pill .pill--rumor } **Official**{ .pill .pill--official }
```

### Changes from Classic

<div class="pills" markdown>
**New**{ .pill .pill--new } **Buffed**{ .pill .pill--buff } **Nerfed**{ .pill .pill--nerf } **Changed**{ .pill .pill--changed } **Removed**{ .pill .pill--removed } **Fixed**{ .pill .pill--fixed }
</div>

```markdown
**New**{ .pill .pill--new } **Buffed**{ .pill .pill--buff } **Nerfed**{ .pill .pill--nerf }
**Changed**{ .pill .pill--changed } **Removed**{ .pill .pill--removed } **Fixed**{ .pill .pill--fixed }
```

### Factions and classes

<div class="pills" markdown>
**Alliance**{ .pill .pill--alliance } **Horde**{ .pill .pill--horde } **Both factions**{ .pill .pill--neutral-faction }
</div>

<div class="pills" markdown>
**Druid**{ .pill .pill--druid } **Hunter**{ .pill .pill--hunter } **Mage**{ .pill .pill--mage } **Paladin**{ .pill .pill--paladin } **Priest**{ .pill .pill--priest } **Rogue**{ .pill .pill--rogue } **Shaman**{ .pill .pill--shaman } **Warlock**{ .pill .pill--warlock } **Warrior**{ .pill .pill--warrior }
</div>

```markdown
**Horde**{ .pill .pill--horde } **Mage**{ .pill .pill--mage }
```

### Difficulty

<div class="pills" markdown>
**Easy**{ .pill .pill--easy } **Moderate**{ .pill .pill--medium } **Hard**{ .pill .pill--hard }
</div>

### Tones and icons

<div class="pills" markdown>
**Neutral**{ .pill } **Info**{ .pill .pill--info } **Success**{ .pill .pill--success } **Warning**{ .pill .pill--warning } **Danger**{ .pill .pill--danger } **Gold**{ .pill .pill--gold } **:material-shield: With icon**{ .pill .pill--info }
</div>

```markdown
**Neutral**{ .pill } **Info**{ .pill .pill--info } **:material-shield: With icon**{ .pill .pill--info }
```

Put a row of pills in `<div class="pills" markdown>` to space them evenly.

## Badges, tiers and ratings

Role badges and level ranges are tags too. A letter tier is a filled tile. Stars are drawn in CSS.

**Tank**{ .badge .tank } **Healer**{ .badge .heal } **DPS**{ .badge .dps } · **S**{ .tier .tier-s } **A**{ .tier .tier-a } **B**{ .tier .tier-b } **C**{ .tier .tier-c } · **4/5**{ .stars .s4 } · **10–20**{ .lvl }

```markdown
**Tank**{ .badge .tank } **S**{ .tier .tier-s } **4/5**{ .stars .s4 } **10–20**{ .lvl }
```

## Chips

A chip is a link that looks like a control. Use it for a short list of links to related pages.

[Glossary](glossary.md){ .fc-chip } [Resources](resources.md){ .fc-chip }

```markdown
[Glossary](glossary.md){ .fc-chip } [Resources](resources.md){ .fc-chip }
```

## Stat strip

Use a stat strip for a row of headline facts or numbers. Write the value in bold, then its label. The class `specs` gives the same strip.

<div class="stats" markdown>

- **8.86M** characters created in the beta
- **21%** of them were Skyborne
- **9 Dec 2026** raids unlock
- **9** new dungeons

</div>

```markdown
<div class="stats" markdown>

- **8.86M** characters created in the beta
- **21%** of them were Skyborne

</div>
```

## Tables

All tables have one style. A column is as wide as its content.

- **Numbers:** align a numeric column to the right in the separator row (`---:`). Write `<span class="fc-na">—</span>` for a value that does not exist.
- **Long tables:** the header row of a table with more than 15 rows stays in view. For a shorter table, put the table in `<div class="fc-sticky" markdown>`.
- **Data tables:** put a table with many short columns in `<div class="fc-data" data-prose="1 5" markdown>`. Each cell is then one line. `data-prose` names the columns that hold text: those columns wrap.
- **Wide tables:** a table that is wider than the page scrolls sideways. In `.fc-data`, `.fc-matrix` and `.compare`, the first column then stays in view.
- **Tables with long text:** put a table that has long text in 2 or more columns in `<div class="fc-stack" markdown>`. On a phone each row is then a block: the first cell, then each other cell with the name of its column. The table does not change on wider screens.
- **Wide pages:** a page that is mostly tables can use a wider column. Add `wide: true` to its front matter. The text keeps its width of about 70 characters. Only tables, grids and the talent tree use the wider column.
- **Route tables:** a table with the columns *Levels* and *Zone* gets a tick box for each row. The reader's browser saves the ticks.

<div class="fc-data" data-prose="1 5" markdown>

| Recipe | Learn | Yellow | Grey | Reagents |
|---|---:|---:|---:|---|
| Linen Bag **Changed**{ .pill .pill--changed } | 1 | 30 | 65 | 3 Bolt of Linen Cloth, 3 Coarse Thread |
| Woolen Bag | <span class="fc-na">—</span> | 75 | 110 | 3 Bolt of Woolen Cloth, 1 Fine Thread |

</div>

```markdown
<div class="fc-data" data-prose="1 5" markdown>

| Recipe | Learn | Yellow | Grey | Reagents |
|---|---:|---:|---:|---|
| Linen Bag | 1 | 30 | 65 | 3 Bolt of Linen Cloth, 3 Coarse Thread |

</div>
```

## Card grids

A card grid (`<div class="grid cards" markdown>`) never leaves 1 card alone in a row: 3, 5 and 9 cards use 3 columns, and 4 cards use 2 columns. You do not set the columns.

## Timeline

Start each item with its date in bold. A status pill in an item also colours the dot of that item.

<div class="timeline" markdown>

- **12 Sep 2026** Revealed at BlizzCon. **Official**{ .pill .pill--official }
- **4 Nov 2026** Launch. **Live**{ .pill .pill--live }
- **9 Dec 2026** Raids unlock. **Coming soon**{ .pill .pill--soon }
- **Spring 2027** 2 raids, 2 dungeons, a new area. **Planned**{ .pill .pill--planned }

</div>

```markdown
<div class="timeline" markdown>

- **4 Nov 2026** Launch. **Live**{ .pill .pill--live }
- **9 Dec 2026** Raids unlock. **Coming soon**{ .pill .pill--soon }

</div>
```

## Meters

Meters show a proportion. The number stays visible next to the bar.

| Share | Meter |
|---|---|
| Skyborne share of beta characters | <span class="meter" style="--v:21%"><span>21%</span></span> |
| Undead Paladins among all characters | <span class="meter meter--info" style="--v:6.9%"><span>6.9%</span></span> |

```html
<span class="meter" style="--v:21%"><span>21%</span></span>
```

## Pros and cons

<div class="proscons" markdown>
<div class="pros" markdown>

Strengths

- Strong burst damage
- Great crowd control

</div>
<div class="cons" markdown>

Weaknesses

- Fragile in melee
- Needs much gear

</div>
</div>

```markdown
<div class="proscons" markdown>
<div class="pros" markdown>

Strengths

- Strong burst damage

</div>
<div class="cons" markdown>

Weaknesses

- Fragile in melee

</div>
</div>
```

## Callouts

A callout is a hairline box with a coloured bar on the left. The title, the icon and the bar have the colour of the callout family. The icon and the title tell the families apart without colour. The Codex has 6 custom callout types, plus the built-in types:

!!! forever "What Forever changed"
    Marks a change from Classic.

!!! conflict "Sources disagree"
    Lists every version when sources conflict.

!!! unconfirmed "Single source"
    The claim comes from only 1 source, and that source is not official.

!!! hardcore "Hardcore risk"
    A danger for permadeath characters.

??? spoiler "Story spoiler"
    Collapsed by default.

```markdown
!!! forever "What Forever changed"
    Marks a change from Classic.
```

A short callout in a chapter of a class progression has the class `fc-inline`. It has no box, and its title starts the text:

!!! tip fc-inline "Tip"
    Get a wand as soon as you can.

```markdown
!!! tip fc-inline "Tip"
    Get a wand as soon as you can.
```

## Class pages

A class page has one header: the H1, then one meta row, then the first paragraph. The meta row holds the class sigil, the kind of page, the role tags, and the link to the data note. There is no box below the H1. The generators write the row on the progression, Talents and Equipment pages, with the date. A Race add-on page has the row by hand:

:codex-mage:{ .fc-sigil aria-hidden="true" } <span class="fc-meta__kind">Add-on: Race</span> **:codex-alliance:{ .fc-sigil aria-hidden="true" } Alliance**{ .badge .faction } **DPS**{ .badge .dps } [Data and sources](../guides/mage/index.md#sources)
{: .fc-meta data-class="mage" }

```markdown
# Gnome Mage

:codex-mage:{ .fc-sigil aria-hidden="true" } <span class="fc-meta__kind">Add-on: Race</span> **:codex-alliance:{ .fc-sigil aria-hidden="true" } Alliance**{ .badge .faction } **DPS**{ .badge .dps } [Data and sources](index.md#sources)
{: .fc-meta data-class="mage" }

Read with the [Mage progression](index.md). This page gives only the changes when your Mage is a Gnome.
```

The template adds the switcher below the meta row of an add-on page: one line of chips for the pages of the class. Do not write it by hand.

The other parts of a class progression (the add-on picker, the sticky pick bar, the add-on blocks, the chapter headings, the goals and the talent tree) come from the generators. `DESIGN.md` describes them.

## Sizes, corners and spacing

New components use the tokens in `docs/stylesheets/extra.css`. Do not write a raw size.

| Token group | Values | Use |
|---|---|---|
| Type | `--fc-fs-xs`, `--fc-fs-sm`, `--fc-fs-body`, `--fc-fs-lede`, `--fc-fs-h3`, `--fc-fs-h2`, `--fc-fs-h1` | `xs` for tags, chips, labels and captions. `sm` for tables, callouts and boxes. No text is smaller than `xs` |
| Corners | `--fc-radius-s`, `--fc-radius`, `--fc-radius-full` | Small for tags and inputs. Medium for boxes and tables. Full for chips and buttons |
| Borders | `--fc-border`, `--fc-border-strong` | The hairline of each box. The strong line for chips and for the box that needs emphasis |
| Spacing | `--fc-space-1` to `--fc-space-7` | Box padding is `--fc-space-3` and `--fc-space-4`. The gap in a box is `--fc-space-2`. The margin between components is `--fc-space-5`. The gap in a grid is `--fc-space-3` |

A box is a hairline border, the medium corner and the `--fc-surface-1` fill. It has no shadow and no coloured edge. Only callouts and add-on blocks have a coloured bar on the left. Gold is for fills, for the current item and for the rule under the page title.

An infobox floats at the right of the text. With the class `infobox--row` it has no float: the box is as wide as the text, and its facts are in 2 columns. The class progressions use this form for the facts of the class.

A page shows 1 date. A page that you write by hand has "Updated" and the date in its footer. A generated page has "Updated" and the date in the meta row under the H1.

`DESIGN.md` in the repository documents the other components (infobox, glossary list, source list, steps, rotation priority and the comparison matrix).
