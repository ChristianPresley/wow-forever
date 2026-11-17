---
wide: true
description: Estimated (not measured) raid DPS for every race and DPS spec in WoW Forever, with every input sourced and editable.
---

# DPS calculator

**What the table shows.** Simulated damage per second (DPS) for every class, talent tree and race, at the level and with the gear that you pick. Each row is one spec and race in a 3-minute fight against a target of the same level. A higher number is better. The numbers are model estimates, not measured results: see [Limits](#limits).

**How to use it.**

- **Level and gear:** move the Level slider, and pick *Best craftable gear* or *No gear*.
- **Filter:** select one or more classes, a faction or a race, or type in *Search*. Turn on the best-race switch to keep only the best race of each spec. The bar shows how many rows match, and *Reset filters* returns to the start.
- **Sort:** select a column header. Select it again to reverse the order.
- **Chart:** the chart above the table draws DPS at every level from 1 to 60. It starts with the best race of the top 4 specs in the table. Select *Compare* in a row to chart that row instead, up to 6 rows. Point at the chart, or focus it and press the arrow keys, to read every charted row at one level. The table under the chart has the same numbers.
- **Open a build:** select a row to see its talents, gear, opening sequence and damage by source at that level. The panel also charts that build across all 60 levels: its DPS with and without crafted gear, and its damage by source. A table lists every level with the talent point spent there.
- **Column meanings:** point at a header, or move keyboard focus to it. *How to read this table*, under the table, lists them all.
- **Keyboard:** Tab reaches every filter, header and row name. The header row stays in view while you scroll.

<div class="dps-calc" data-dps-levels><p>Loading the level simulation. It needs JavaScript.</p></div>

Healers have their own page: the [healing calculator](healing-calculator.md) covers sustained and maximum healing, and the off-damage of every healer build.

## Simulated raid estimates

**What the table shows.** Estimated single-target raid DPS for every race and DPS spec at level 60, against a level 63 boss, with pre-raid gear and raid buffs. It answers a different question from the table above: how specs compare in a raid, not how they level.

**How to use it.** Filter by class or faction, sort by any column, and open a spec name to see its damage by ability. *Data confidence* shows how much of the spec's input is Forever data.

These estimates come from 2 event-driven combat simulators in the repository (`tools/sim/physical` and `tools/sim/casters`). They play out each fight with swing timers, cast times, the attack table, resources, procs and cooldowns, using a priority list for each spec. Their READMEs list every assumption and gap.

<div class="dps-calc" data-dps-sim><p>Loading the simulated estimates. They need JavaScript.</p></div>

## Quick estimate (editable)

This is a faster, simpler formula model. It doesn't simulate fights, but you can change every input below and see the effect at once.

<div id="dps-calc" class="dps-calc" markdown>

<div class="dps-filters" data-dps-filters></div>

<div data-dps-results><p>Loading the calculator. It needs JavaScript.</p></div>

## How the model works

- **Melee:** Classic attack table (miss, dodge, glancing, crit), weapon damage + AP/14 × speed, normalized specials, Flurry uptime from crit chance.
- **Spells:** base damage + coefficient × spell power, spell hit against a +3 boss, crit multiplier with talents.
- **Cooldowns:** racial and class cooldowns are used on cooldown from the pull. The result blends the DPS with and without each racial, weighted by its uptime over the fight.
- **Gear:** each class uses one gear profile, stated as Human totals. Other races add their racial stat offsets.
- **Not modelled:** mana and rage limits (except the Rogue energy cycle), movement, execute phases and multiple targets.

Source tags: **Forever** = Wowhead Forever, Blizzard notes or client tooltips. **Forever est.** = a third-party Forever number that its own source calls untested. **Classic** = a Classic 1.12 value checked against Wowhead Classic or warcraft.wiki.gg. **Classic, unchecked** = a Classic value that no page confirmed. **Assumption** = made for this calculator.

## Inputs

Change any number and the table updates. Changes are not saved.

<div class="dps-inputs-wrap" data-dps-inputs></div>

</div>

## How DPS by level works

This simulator (`tools/levelsim`) plays out every class, talent tree and race at every level from 1 to 60. Each fight lasts 3 minutes against a same-level target with no armor. The character knows every spell rank and talent point it can have at that level, and uses its racial abilities. Casters spend their mana so it lasts the fight. They pick spell ranks to suit, and shoot a wand or melee while their mana comes back.

Pick the gear:

- **Best craftable gear:** each slot holds the crafted item and enchant that scores best for the spec at that level. Item stats are decoded from the Forever client. Crafting makes almost no rings, necks or trinkets, so those slots are mostly empty. Weapon procs and set bonuses are not counted.
- **No gear:** the character fights unarmed and unarmored. Hunters have no ranged weapon, so they lose their shots.

**Click any row** to open its full build at that level:

- Race, class and spec.
- DPS at every level, with and without crafted gear, as a chart.
- Damage by source at every level, as a chart and as a table with one row per level.
- Talents by tree.
- Every gear slot with its enchant.
- The opening sequence of abilities from a simulated fight.
- Casts per minute.
- Damage by source.

Racials are part of every fight. The simulator models each racial that changes damage against one target: Ruthless, The Human Spirit, Artisan's Precision, Eureka!, Expansive Mind, Elune's Light, Blood Fury, Command, Berserking, Touch of the Grave and Wind Blessed. The coverage section below lists all 40 racials and their status.

Spell values come from the Forever client data. The client doesn't ship some rules: combat formulas, rage, most talent ranks above 1, scripted effects, and hit and crit rating conversion. These rules use Classic rules or tagged assumptions. The module docstrings list them. It is not raid DPS: raid buffs, consumables and boss armor are left out.

## Coverage: what is simulated and what is not

**What is complete.** Every class, talent tree, race, gear mode and level from 1 to 60 is simulated: 27 specs, 56 class and race pairs, 168 spec and race pairs, 2 gear modes and 60 levels, which is 20,160 cells. A test fails when a cell is missing. Every damaging class spell in the Forever client is either used, tested and not chosen, or left out for a stated reason. Every talent of every level 60 build is tested by removing it and running the fight again.

**What is not.** Each spec runs one talent order and one priority list. The simulator does not try every other way to spend 51 talent points, or every other order of abilities. There are far too many to run. Talents that no build takes, and spells marked *Not tested*, are listed below so that the gaps are visible.

<div class="dps-calc" data-dps-audit><p>Loading the coverage audit. It needs JavaScript.</p></div>

The audit is `tools/levelsim/audit.py`. It reads the simulation results and writes the data for this section.

## Limits

No raid opens until 9 December 2026, so no one has real raid logs to check these numbers against.

!!! warning "Estimates on incomplete data"
    Treat every number on this page as an estimate. Absolute DPS can be off by 20–30%, and the order of specs can change when real logs exist.

    - **Missing Forever data:** most Rogue, Hunter, Paladin, Druid and Shaman ability ranks and most spell coefficients. Also missing: pet and demon damage, base stats by race, rating conversions and the armor formula. Each gap is filled with a Classic value or a tagged assumption.
    - **Assumed gear:** most gear profiles are assumptions. Only Arms uses published pre-raid totals.
    - **Untested rotations:** each spec uses a priority list written for this page, not one tested by players.
    - **Data confidence** shows how much of each spec's input is Forever data. No simulated spec is above 67%.

    **What is more trustworthy:** comparing races within one spec, when the gap is larger than the ± margin. Every racial value comes from Wowhead Forever, and all races of a class use the same gear. Gaps under about 1% are effectively ties.

## Sources

- Wowhead Forever spell database, patch 1.60.1: racials, raid buffs, Warrior abilities, Shadow Bolt.
- Metabot Forever ability pages: caster spell base damage.
- Warcraft Tavern pre-launch class changes and spec guides.
- RankedBoost Forever stat pages (estimates).
- forever.warcraftdb.com item tooltips: weapons.
- Kami-Labs pre-raid Arms set totals.
- warcraft.wiki.gg and Wowhead Classic: Classic formulas and fallback values.
