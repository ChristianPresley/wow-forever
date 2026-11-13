---
wide: true
description: Estimated raid DPS for every race and DPS spec in WoW Forever, with every input sourced and editable.
---

# DPS calculator

This page ranks every race and DPS spec pair by single-target raid DPS against a level 63 boss, with pre-raid gear. No raid opens until 9 December 2026, so no one has published real raid logs yet.

!!! warning "Built on incomplete data"
    Many Forever values are still unknown: most Rogue, Hunter, Paladin, Druid and Shaman ability ranks, most spell coefficients, pet and demon damage, rating conversions and the armor formula. Each gap is filled with a Classic value or a tagged assumption. The **Data confidence** column shows how much of each spec's input is Forever data.

    - **Race results within one spec are reliable** where the gap is larger than the ± margin. Every racial value comes from Wowhead Forever, and all races of a class use the same gear.
    - **Spec-against-spec rankings are rough.** They depend on assumed gear and the Classic fallbacks.

## Simulated results

These come from two event-driven combat simulators in the repository (`tools/sim/physical` and `tools/sim/casters`). They play out each fight with swing timers, cast times, the attack table, resources, procs and cooldowns, using a priority list for each spec. Their READMEs list every assumption and gap.

<div class="dps-calc" data-dps-sim><p>Loading the simulation results. They need JavaScript.</p></div>

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

## Sources

- Wowhead Forever spell database, patch 1.60.1: racials, raid buffs, Warrior abilities, Shadow Bolt.
- Metabot Forever ability pages: caster spell base damage.
- Warcraft Tavern pre-launch class changes and spec guides.
- RankedBoost Forever stat pages (estimates).
- forever.warcraftdb.com item tooltips: weapons.
- Kami-Labs pre-raid Arms set totals.
- warcraft.wiki.gg and Wowhead Classic: Classic formulas and fallback values.
