---
wide: true
description: Estimated (not measured) sustained and maximum healing, and off-damage, for every healer build and race in WoW Forever at level 60.
---

# Healing calculator

**What the table shows.** The best healing that each healer build can do at level 60: Priest, Paladin, Druid and Shaman, 21 talent builds, every race. Each row is one build and race. *Sustained HPS* is the most healing per second that lasts a 5-minute fight. The other columns show the healing for each point of mana, how fast the mana runs out at full pace, the maximum healing, and the damage that the same character deals when it does not heal. The numbers are model estimates, not measured results: see [Limits](#limits).

**How to use it.**

- **Healing job:** pick *One target (tank)* or *Party of 5*.
- **Filter:** select one or more classes, the gear, healers or hybrids, or a race, or type in *Search*. Turn on the best-race switch to keep only the best race of each build. The bar shows how many rows match, and *Reset filters* returns to the start.
- **Sort:** select the header of a number column, or use *Sort by*. Select the header again to reverse the order.
- **Open a build:** select a row to see its talents, the exact spells and ranks to cast, the mana flow, the off-damage and the gear.
- **Column meanings:** point at a header, or move keyboard focus to it. *How to read this table*, under the table, lists them all.
- **Keyboard:** Tab reaches every filter, header and row name. The header row stays in view while you scroll.

<div class="dps-calc" data-heal-sim><p>Loading the healing simulation. It needs JavaScript.</p></div>

## What the numbers mean

- **Sustained HPS:** the most healing per second that lasts a 5-minute fight. The healer starts on full mana and ends on empty. This is the number to plan a fight around.
- **Total healing in the fight:** sustained HPS times the 300 seconds of the fight.
- **Healing per mana:** healing bought by each point of mana with the sustained mix.
- **Seconds until empty:** how long a full mana bar lasts at maximum pace.
- **Sustain:** sustained HPS as a percentage of maximum HPS. A build at 25% must hold back three quarters of what it could cast.
- **Endless HPS:** the most healing per second on mana regeneration alone. A healer casting this mix never runs out.
- **Maximum HPS:** the most healing per second with mana ignored, and how many seconds the mana bar lasts at that pace.

**Off-DPS** is the same build in the same healing gear, run through the [DPS calculator](dps-calculator.md)'s level 60 simulator with its best damage rotation.

Pick the healing job:

- **One target (tank):** one player takes all the damage. Party heals hit one player and each heal-over-time spell can only be on that one target.
- **Party of 5:** all five party members are hurt. Party heals hit five players, Chain Heal hits three and Prayer of Mending jumps five times.

**Click any row** for the full build: talents by tree, the exact spells and ranks to cast per minute for each of the three numbers, a breakout of each sustain stat by pace and by spell (total healing, healing per mana, seconds until empty), healing by source, the off-damage breakdown and every gear slot.

## Every talent, ability and stat

This section shows how each piece of a healer is calculated and what it is worth. Pick a class. The reference healer is a deep healing build of that class in the best craftable healing gear. The card names the build and the race.

- **Stats:** the healing gained from one more point of each stat.
- **Healing abilities:** every castable rank with its cast time, mana, healing per cast, healing per second while casting and healing per mana, and whether the best mix uses it.
- **Talents:** every talent in all three trees. The value is the reference healer with the talent at maximum rank, minus the same healer without it. Off-DPS comes from the damage simulator.

A talent or ability with no healing or damage output (survival, control, threat, travel, resistances, resurrection) has nothing to calculate here. It is listed and marked.

<div class="dps-calc" data-heal-ledger><p>Loading the talent, ability and stat values. They need JavaScript.</p></div>

### How each stat is calculated

| Stat | Formula | Source |
|---|---|---|
| Intellect, Spirit, Stamina | Base value for the class, race and level, plus gear, times the class talent (Mental Strength, Divine Intellect, Heart of the Wild, Ancestral Knowledge: +10% Intellect; Living Spirit: +15% Spirit; The Human Spirit: +10% Spirit) | Base stats: Classic. Talents: tooltips |
| Maximum mana | Base mana + 15 per Intellect - 260. Gnomes: +5% | Client base mana; Classic rule |
| Health | Class base health + 10 per Stamina. Tauren: +5% | Classic, unchecked |
| Healing power | Gear healing + gear spell power, plus Spiritual Guidance (25% of Spirit), Natural Instinct (25% of Intellect) or Mental Quickness (30% of Intellect) | Client items; tooltips |
| Spell crit | Intellect x 0.0168% per point (client value, level 60) + gear crit rating / 14 + talents + racials. A crit heals for 150% (Holy Power: 175%) | Client; rating conversion inferred |
| Haste | Racial only: Skyborne 2%, Berserking 10% for 15 s. Divides cast time; the 1.5 s global cooldown is not shortened | Client |
| Mana regeneration | Per 2 s: Priest 12.5 + Spirit/4; Paladin and Druid 15 + Spirit/5; Shaman 17 + Spirit/5. Full rate after 5 s without spending mana; Meditation, Reflection and Mindfulness keep 50% while casting, Reverence 30% | Classic |
| Mana per 5 seconds | Gear value, always active | Client items |
| One heal | (base + coefficient x healing power) x talent multipliers x (1 + crit chance x (crit multiplier - 1)) | Client base and coefficient |
| Coefficient | Client value (cast time / 3.5; heal-over-time and party heals have their own). Spells learned before level 20 lose 3.75% per level below 20 | Client; Classic penalty |
| Mana cost | Client cost x talent reductions, minus refunds (Illumination, Litany of Light) | Client; tooltips |

## What the model finds

With the best craftable gear:

- **Tank healing, sustained:** Restoration Druid with Nature's Splendor leads (about 330 HPS). It keeps Regrowth and Rejuvenation on the tank, uses Swiftmend and rests between casts to regenerate. Holy/Penance Priest and Mental Quickness Shaman are close behind (about 300 HPS).
- **Party healing, sustained:** Holy Priest with Prayer of Mending leads by a wide margin (about 660 HPS). One Prayer of Mending every 10 seconds heals six times for one cast.
- **Maximum healing:** Holy Priest, Holy Paladin, Restoration Druid and Restoration Shaman builds all reach about 1,100 to 1,210 HPS on one target and empty their mana in about 20 seconds. Discipline Priest reaches about 1,000. On a party, Restoration Druid (Wild Growth and Regrowth, about 1,890 HPS) and Holy Priest (Prayer of Healing, about 1,740 HPS) lead.
- **Sustained healing is about a quarter of maximum healing.** Mana, not cast time, is the limit. The best sustained mixes use cheap lower ranks and spend much of the fight not casting, so that Spirit regeneration runs at its full rate.
- **Off-damage:** hybrids trade healing for damage. An Enhancement hybrid Shaman deals about 340 DPS and sustains about 210 HPS on a tank. A deep Restoration Shaman deals about 200 DPS and sustains about 290 HPS.
- **Race matters little:** the gap between the best and worst race of a build is a few percent. Humans lead Priest and Paladin builds through The Human Spirit.

## How the model works

The model (`tools/healsim`) does not play out a fight. It uses expected values.

- **Every spell rank is an action** with a cast time, a net mana cost and an expected heal (average roll, healing power times the spell's coefficient, talents and crit).
- **A linear program picks the casts per second of each action** that maximise healing. Its limits are time (casting plus resting cannot exceed the fight), mana (mana spent cannot exceed the pool plus regeneration), cooldowns and one copy of each heal-over-time spell per target.
- **Resting is a choice.** Time spent not casting regenerates mana at the full Spirit rate (the 5-second rule). The program decides how much to rest.
- **Effects that depend on the mix** are solved by repeating the program until they settle: Nature's Grace, Infusion of Light, Litany of Light, Renewed Hope, Riptide's Chain Heal bonus and Water Shield.
- **Downranking is allowed.** The detail panel also shows the result with top ranks only.
- **Racial cooldowns** are used on cooldown and averaged over the fight.

Not modelled: overhealing, movement, pushback, damage to the healer, dispels, threat, mana potions, runes, party buffs, Seal of Light and Judgement of Wisdom (they need the healer in melee). Inspiration and Ancestral Healing are reported as armor buff uptime, not as healing. Lightwell assumes the party uses all five charges. Lay on Hands drains all mana, so it only counts toward maximum healing.

## Limits

No raid opens until 9 December 2026, so no one has real healing logs to check these numbers against.

!!! warning "Estimates on incomplete data"
    Treat every number on this page as an estimate.

    - **No overhealing:** every point of healing counts. Real healing loses a large share to overhealing, more for slow heals and heal-over-time spells.
    - **Missing Forever data:** talent values come from launch tooltips, not the client. Holy Shock's cost, Light's Vigil's heal, Oath of Light at lower ranks, the water totems, Innervate, Spirit regeneration and the penalty on spells learned before level 20 use Classic values or tagged assumptions.
    - **Crafted gear only:** the gear is the best craftable healing set. Dungeon and raid gear would raise every number.
    - **No party buffs or consumables:** each healer brings only their own buffs. No mana potions.

    **What is more trustworthy:** comparing builds within one class, and comparing sustained with maximum healing for one build.

## Sources

- Forever client data, patch 1.60.1: healing spell ranks, costs, cast times, coefficients, durations and cooldowns.
- Forever launch talent tooltips: talent values.
- Forever client item data: the craftable healing gear.
- warcraft.wiki.gg and Wowhead Classic: Spirit regeneration, the 5-second rule, the level 20 coefficient penalty, totem values and Innervate.
