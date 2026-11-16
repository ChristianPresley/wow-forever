---
wide: true
description: Estimated (not measured) raid DPS for every race and DPS spec in WoW Forever, with every input sourced and editable.
---

# DPS calculator

**What the table shows.** Simulated damage per second (DPS) for every class, talent tree and race, at the level and with the gear that you pick. Each row is one spec and race in a 3-minute fight against a target of the same level. A higher number is better. The numbers are model estimates, not measured results: see [Limits](#limits).

**How to use it.**

- **Level and gear:** move the Level slider, and pick *Best craftable gear* or *No gear*.
- **Filter:** pick a class. Tick the best-race box to keep only the best race of each spec.
- **Sort:** select a column header. Select it again to reverse the order.
- **Open a build:** select a row to see its talents, gear, opening sequence and damage by source at that level.
- **Column meanings:** point at a header, or move keyboard focus to it. *How to read this table*, under the table, lists them all.
- **Keyboard:** Tab reaches every filter, header and row name. The header row stays in view while you scroll.

<div class="dps-calc" data-dps-levels><p>Loading the level simulation. It needs JavaScript.</p></div>

Healers have their own page: the [healing calculator](healing-calculator.md) covers sustained and maximum healing, and the off-damage of every healer build.

## Simulated raid estimates

**What the table shows.** Estimated single-target raid DPS for every race and DPS spec at level 60, against a level 63 boss, with pre-raid gear and raid buffs. It answers a different question from the table above: how specs compare in a raid, not how they level.

**How to use it.** Filter by class or faction, sort by any column, and open a spec name to see its damage by ability. *Data confidence* shows how much of the spec's input is Forever data.

These estimates come from two event-driven combat simulators in the repository (`tools/sim/physical` and `tools/sim/casters`). They play out each fight with swing timers, cast times, the attack table, resources, procs and cooldowns, using a priority list for each spec. Their READMEs list every assumption and gap.

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

This simulator (`tools/levelsim`) plays out every class, talent tree and race at every level from 1 to 60, in a 3-minute fight against a same-level target with no armor. The character knows every spell rank and talent point it can have at that level, and uses its racial abilities. Casters spend their mana so it lasts the fight. They pick spell ranks to suit, and shoot a wand or melee while their mana comes back.

Pick the gear:

- **Best craftable gear:** each slot holds the crafted item and enchant that scores best for the spec at that level. Item stats are decoded from the Forever client. Crafting makes almost no rings, necks or trinkets, so those slots are mostly empty. Weapon procs and set bonuses are not counted.
- **No gear:** the character fights unarmed and unarmored. Hunters have no ranged weapon, so they lose their shots.

**Click any row** to open its full build at that level: race, class and spec, talents by tree, every gear slot with its enchant, the opening sequence of abilities from a simulated fight, casts per minute and damage by source.

Spell values come from the Forever client data. Rules the client doesn't ship (combat formulas, rage, most talent ranks above 1, scripted effects, hit and crit rating conversion) use Classic rules or tagged assumptions; the module docstrings list them. It is not raid DPS: raid buffs, consumables and boss armor are left out.

## Limits

No raid opens until 9 December 2026, so no one has real raid logs to check these numbers against.

!!! warning "Estimates on incomplete data"
    Treat every number on this page as an estimate. Absolute DPS could be off by 20–30%, and the order of specs could change once real logs exist.

    - **Missing Forever data:** most Rogue, Hunter, Paladin, Druid and Shaman ability ranks, most spell coefficients, pet and demon damage, base stats by race, rating conversions and the armor formula. Each gap is filled with a Classic value or a tagged assumption.
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
