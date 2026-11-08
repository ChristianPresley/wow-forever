---
description: Every visual element the Forever Codex uses (pills, badges, stat tiles, timelines, meters, pros and cons, cards and callouts), with the Markdown to write each one.
search:
  boost: 0.5
---

# Style guide

These are the visual building blocks used across the Codex. Each one shows what it looks like and the Markdown that makes it, so contributors can reuse them. Every coloured element also carries a word or a symbol, so meaning never depends on colour alone.

## Pills

Pills are small inline labels. Add them to bold text with an attribute list: `**Text**{ .pill .pill--live }`.

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

### Armour and resources

<div class="pills" markdown>
**Cloth**{ .pill .pill--cloth } **Leather**{ .pill .pill--leather } **Mail**{ .pill .pill--mail } **Plate**{ .pill .pill--plate } **Rage**{ .pill .pill--rage } **Energy**{ .pill .pill--energy } **Mana**{ .pill .pill--mana }
</div>

### Difficulty

<div class="pills" markdown>
**Easy**{ .pill .pill--easy } **Moderate**{ .pill .pill--medium } **Hard**{ .pill .pill--hard }
</div>

### Label and value

<div class="pills" markdown>
<span class="pill pill--kv pill--gold"><span>Size</span><span>40</span></span>
<span class="pill pill--kv pill--info"><span>Level</span><span>60</span></span>
<span class="pill pill--kv"><span>Bosses</span><span>8</span></span>
</div>

```html
<span class="pill pill--kv pill--gold"><span>Size</span><span>40</span></span>
```

### Styles and sizes

<div class="pills" markdown>
**Soft**{ .pill .pill--info } **Solid**{ .pill .pill--info .pill--solid } **Outline**{ .pill .pill--info .pill--outline } **Small**{ .pill .pill--gold .pill--sm } **Large**{ .pill .pill--gold .pill--lg } **:material-shield: With icon**{ .pill .pill--info }
</div>

Wrap a row of pills in `<div class="pills" markdown>` to space them evenly.

## Badges, tiers and ratings

These existed before the pills and remain in use: role badges, letter tiers and CSS star ratings.

**Tank**{ .badge .tank } **Healer**{ .badge .heal } **DPS**{ .badge .dps } · **S**{ .tier .tier-s } **A**{ .tier .tier-a } **B**{ .tier .tier-b } **C**{ .tier .tier-c } · **4/5**{ .stars .s4 } · **10–20**{ .lvl }

```markdown
**Tank**{ .badge .tank } **S**{ .tier .tier-s } **4/5**{ .stars .s4 } **10–20**{ .lvl }
```

## Spec strip

Use a spec strip for a row of headline facts under a page title.

<div class="specs" markdown>

- **10 players** Raid size
- **8** Bosses
- **9 Dec 2026** Unlocks
- **Mount Hyjal** Location

</div>

```markdown
<div class="specs" markdown>

- **10 players** Raid size
- **8** Bosses

</div>
```

## Stat tiles

Use stat tiles for headline numbers.

<div class="stats" markdown>

- **8.86M** characters created in the beta
- **21%** of them were Skyborne
- **1.12M** peak Twitch viewers at launch
- **9** new dungeons

</div>

```markdown
<div class="stats" markdown>

- **8.86M** characters created in the beta
- **21%** of them were Skyborne

</div>
```

## Timeline

Start each item with its date in bold. A status pill in an item also colours that item's dot.

<div class="timeline" markdown>

- **12 Sep 2026** Revealed at BlizzCon. **Official**{ .pill .pill--official }
- **4 Nov 2026** Launch. **Live**{ .pill .pill--live }
- **9 Dec 2026** Raids unlock. **Coming soon**{ .pill .pill--soon }
- **Spring 2027** Two raids, two dungeons, a new area. **Planned**{ .pill .pill--planned }

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
- Gear-hungry

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

## Labelled divider

<p class="divider">Alliance</p>

```html
<p class="divider">Alliance</p>
```

## Callouts

The Codex also has six custom callout types, plus the built-in ones:

!!! forever "What Forever changed"
    Marks a change from Classic.

!!! conflict "Sources disagree"
    Lists every version when sources conflict.

!!! unconfirmed "Single source"
    The claim comes from one non-official source.

!!! hardcore "Hardcore risk"
    A danger for permadeath characters.

??? spoiler "Story spoiler"
    Collapsed by default.

```markdown
!!! forever "What Forever changed"
    Marks a change from Classic.
```

The remaining components (infobox, steps, milestones, rotation priority and the comparison matrix) are documented in `DESIGN.md` in the repository.
