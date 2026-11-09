---
description: "Paladin guide for WoW: Forever: specs and talents, rotations, a 1–60 leveling route, dungeons, raids, PvP, gear and Hardcore tips."
tags:
  - Paladin
search:
  boost: 2
---

# Paladin Guide

<div class="guide-head" data-class="paladin" markdown>

:codex-paladin:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Class guide</span> **Tank**{ .badge .tank } **Healer**{ .badge .heal } **DPS**{ .badge .dps }

<nav class="gh-jump" aria-label="Jump to section"><a href="#specs-talents">Talents</a> <a href="#abilities-rotation">Rotation</a> <a href="#leveling-walkthrough-160">Leveling</a> <a href="#dungeons">Dungeons</a> <a href="#raid-preparation">Raids</a> <a href="#pvp">PvP</a> <a href="#gear-stats-enchants">Gear</a> <a href="#hardcore-notes">Hardcore</a></nav>

</div>

!!! info "Current as of 7 November 2026"
    Written three days after launch (Patch 1.60.1). The paladin trees were reworked on **30 October** and retuned in the **2 November** pre-launch notes, so many beta-era guides are out of date. Blizzard has said a larger balance pass will come once players reach the 30s. Reference data lives on the [Paladin class page](../../characters/classes/paladin.md).

## Overview

The paladin is a plate-wearing hybrid of melee, healing and tanking. Forever gives it the tools it lacked in Classic: a real taunt, an early tank seal, a short-cooldown melee strike, and a much shorter Lay on Hands.

<aside class="infobox" markdown>
<p class="infobox-title">Paladin at a glance</p>

| | |
|---|---|
| **Roles** | Tank (Protection), healer (Holy), melee DPS (Retribution) |
| **Armor / weapons** | Plate from 40 (mail before); shields; one- and two-handed swords, maces and axes; polearms |
| **Resource** | **Mana**{ .pill .pill--mana } |
| **Races** | [Human](human.md), [Dwarf](dwarf.md) (Alliance) · [Undead](undead.md) (Horde, **new**) |
| **Class trainers** | Stormwind (Cathedral of Light), Ironforge (Mystic Ward), Northshire, Goldshire, Coldridge Valley, Thunderbrew Distillery, Theramore · Deathknell, Brill, **Bandarion Keep** (Tirisfal) |

</aside>

<div class="proscons" markdown>
<div class="pros" markdown>

Strengths

- Very hard to kill: plate, a shield, Divine Protection, Divine Shield, Lay on Hands every 20 minutes, and self-healing.
- Group value: blessings now last an hour, Blessing of Kings is baseline, and resistance auras cover the raid.
- Protection is now a full tank, with a taunt on Judgement of Fury and Consecration from level 20.
- One of the best dungeon-mob AoE pullers early on, though Consecration's full damage is capped at 4 targets.

</div>
<div class="cons" markdown>

Weaknesses

- **Mana** is the leveling bottleneck for every spec.
- Still no interrupt and no slow. Kiting casters and runners is awkward.
- Holy Shock (21 Holy) and Unsealed Wrath (31 Retribution) cannot both fit in 51 points, so the classic "Shockadin with seal twisting" hybrid is not possible.

</div>
</div>

### What is new in Forever

| Change | Effect |
|---|---|
| **Holy Strike** (level 6) | Baseline instant melee strike, part weapon damage and part Holy. Cooldown is 10 s at launch (12 s in early beta). |
| **Judgement keeps your Seal** | Judging no longer consumes the Seal, and Judgement is off the GCD. Judgement debuffs last 40 s. |
| **Seal of Fury** (level 10) | Tank seal: Holy damage per swing and a small absorb. Judgement of Fury **taunts** (10 yd). |
| **Righteous Fury** (level 10) | Was level 16. +33% threat, +90% Holy threat. |
| **Consecration** (level 20) | Baseline for every spec. Full damage only on the first 4 targets. |
| **Blessings** | Kings is baseline; Improved Wisdom is baseline; 5-minute blessings and Greater Blessings last 1 hour. |
| **Lay on Hands** | 20-minute cooldown (was 1 hour). |
| **Voice of Truth** | Now a trained spell: 6 s silence/interrupt immunity, 3-minute cooldown. |
| **Removed** | Blessing of Salvation, Mass Salvation, Blessing of Light, Greater Blessing of Light, Blessing of Sanctuary, Sanctity Aura, Revoke, Instrument of the Law. |
| **Dual spec** | Level 40, 50g, at your class trainer. |

!!! note "No Salvation"
    Without Blessing of Salvation, DPS players can no longer lean on a 30% threat cut. Expect tanks to matter more, and DPS paladins to be asked for Might, Wisdom or Kings instead.

---

## Specs & talents

Talents start at level 10, one point per level, 51 at level 60. Each tree has single-point "gold" talents at **11, 16, 21 and 31** points. Respec and dual spec are bought from a paladin trainer.

!!! warning "Builds are provisional"
    Talent trees changed on 30 October and again on 2 November. The point orders below come from guides updated on launch day and from talent-planner usage data. Check the in-game tooltip before you commit points.

=== "Retribution"

    **Role:** two-handed melee DPS and the default leveling spec.

    | Talent | Ranks | What it does (launch values) |
    |---|---|---|
    | Benediction | 5 | Cheaper instant spells (mana) |
    | Improved Judgement | 2 | −2 s Judgement cooldown at 2/2 |
    | Conviction | 3 | +2/4/6% crit with all spells and attacks |
    | Sanctified Judgement | 3 | Mana back on Judgement |
    | Seal of Command | 1 | The classic big-swing seal |
    | Pursuit of Justice | 2 | +15% movement speed at 2/2 |
    | Two-Handed Weapon Specialization | 3 | +2/4/6% damage with two-handers, lower threat |
    | **Sacred Arbiter** (16) | 1 | Holy Strike hits harder and refreshes your Judgement on the target |
    | Vengeance | 3 | Damage buff after crits, up to 5 stacks |
    | **Repentance** (21) | 1 | Incapacitate; required for Unsealed Wrath |
    | Vindication | 3 | Lowers the target's attack power |
    | **Champion of the Light** | 5 | 12% of Intellect per rank as spell damage (60%); faster Hammer of Wrath |
    | Eye for an Eye | 2 | Reflects crit damage (PvP) |
    | Turn Evil | 2 | Faster Turn Undead, now also hits Demons |
    | **Unsealed Wrath** (31) | 1 | Melee swings store a copy of your Seal (up to 3 stacks, 15 s). Swinging with a *different* Seal releases every stored Seal's proc chance |

    !!! conflict "Conflict: Twist of Light"
        Older guides (and the beta deep dive) list **Twist of Light**, a seal-twisting capstone with an "Echo" on swap. The 30 October rework **replaced** it with Unsealed Wrath. Several fan pages still list both.

=== "Protection"

    **Role:** shield tank. Forever's Protection has a taunt, an absorb seal and a big emergency button.

    | Talent | Ranks | What it does |
    |---|---|---|
    | Redoubt | 5 | +6% block per rank |
    | Divine Intellect | 5 | +Intellect % (moved here from Holy) |
    | Precision | 3 | +hit |
    | Sacred Duty | 2 | −30 s on Divine Shield, Divine Protection and Templar's Bulwark per rank; shorter Forbearance |
    | Shield Specialization | 2 | +block value; chance to restore mana on block |
    | **Templar's Bulwark** (row 3) | 1 | Absorb equal to 100% of max health for 8 s. 5-minute cooldown. Causes Forbearance and is now a dispellable Magic effect |
    | Toughness | 5 | Armor |
    | Improved Righteous Fury | 3 | 3/6/9% damage reduction |
    | **Swift Judgement** | 1 | Instantly unleashes your Seal on a target within 10 yd, without consuming it or sharing Judgement's cooldown |
    | Anticipation | 5 | +Defense (up to +20) |
    | **Holy Shield** (21) | 1 | 4 charges, +30% block, Holy damage per block |
    | Reckoning | 5 | Extra attacks after blocks |
    | Iron Creed | 3 | +10/20/30% Holy Strike threat; short damage reduction |
    | Deflection | 5 | Parry |
    | Stoicism | 2 | −10/20% stun and charm duration |
    | **Shieldsworn** (31) | 1 | Holy Strike −4 s cooldown and strikes with your shield (triggering block talents); briefly lets you block spells |

    !!! conflict "Conflict: Improved Seal of Fury"
        The beta deep dive had **Improved Seal of Fury** as the 11-point Protection talent. The 30 October rework removed it, along with One-Handed Weapon Specialization.

=== "Holy"

    **Role:** single-target and party healer; "Shockadin" melee hybrid in PvP and duos.

    | Talent | Ranks | What it does |
    |---|---|---|
    | Spiritual Focus | 5 | Pushback protection on Holy Light, Flash of Light and Light's Vigil |
    | Reverence | 2 | 15% mana regen per rank while casting |
    | Healing Light | 3 | Stronger Holy Light and Flash of Light |
    | Illumination | 5 | Mana back on heal crits |
    | **Divine Favor** (16) | 1 | Guaranteed crit on the next heal |
    | Holy Conduit | 2 | −40% mana on listed Holy spells (moved here from Retribution) |
    | Infusion of Light | 2 | Heal-crit proc |
    | **Oath of Light** | 1 | 5-minute oath on one ally: your Holy Light, Flash of Light and Holy Shock heal them for more. One Oath at a time |
    | Divine Precision | 2 | +4% hit per rank with Holy spells; shorter silences |
    | **Holy Shock** (21) | 1 | Instant heal or damage, **10 s** cooldown (was 30) |
    | Boundless Light | 2 | +15/30% crit on Holy Shock cast on an ally *not* under your Oath |
    | Purifying Power | 2 | Cheaper cleanses and stronger Exorcism/Holy Wrath (Classic effect; not re-checked) |
    | Holy Power | 5 | +10% crit-heal bonus per rank (up to 50%) |
    | Divine Strength | 5 | Strength (often taken by Retribution) |
    | Improved Seals | 5 | +3% seal damage per rank |
    | **Light's Vigil** (31) | 1 | Friendly only since 30 October: the target's next Holy Shock has no cooldown and also heals their party |

### Recommended builds

**Leveling (Retribution, then a second spec at 40).** The two most-used launch orders agree on the shape; they differ only in the order of the 15–23 picks.

<div class="milestones" markdown>

Lv 10–14
:   Benediction 5/5

Lv 15–19
:   Improved Judgement 2/2, Conviction 3/3 (either order)

Lv 20–23
:   Sanctified Judgement 3/3, Seal of Command 1/1

Lv 24–25
:   Pursuit of Justice 2/2

Lv 26–28
:   Two-Handed Weapon Specialization 3/3

Lv 29
:   Sacred Arbiter

Lv 30–34
:   Vengeance 3/3, Vindication 1, Repentance

Lv 35–39
:   Champion of the Light 5/5

Lv 40–45
:   Unsealed Wrath (as soon as legal), Divine Strength 5/5

Lv 46–55
:   Improved Seals 5/5, Divine Intellect 5/5

Lv 56–60
:   Precision 3/3 *or* Reverence 2 + Holy Conduit 2

</div>

This lands at **12/8/31** (Holy/Protection/Retribution), which is also the most-cited level-60 PvE Retribution build.

!!! conflict "Conflict: when to start Retribution's 15–23 points"
    Talents Forever's usage data has Improved Judgement at 15–16 and Seal of Command around 23. Leprestore takes Conviction first and Seal of Command at 20. Both are fine; take Seal of Command at 20 if you already use a slow two-hander.

**Endgame templates (level 60).**

| Spec | Split | Core |
|---|---|---|
| Retribution PvE | 12/8/31 | Divine Strength, Improved Seals, Holy Conduit · Divine Intellect, Precision 3 · full Ret to Unsealed Wrath |
| Retribution PvP | 0/14/37 | Adds Vindication 3, Eye for an Eye, Unyielding Faith; Prot side takes Guardian's Favor, Sacred Duty, Templar's Bulwark, Improved Hammer of Justice |
| Protection tank | ~0/40/11 | Redoubt, Templar's Bulwark, Holy Shield, Reckoning, Iron Creed, Anticipation, Shieldsworn; Ret side for Improved Judgement, Conviction, Sanctified Judgement |
| Holy raid healer | ~32/11/8 | Holy to Light's Vigil with Oath of Light and Boundless Light; Divine Intellect and Sacred Duty; Benediction and Conviction |

These are usage-data snapshots, not tuned theorycraft. Exact splits will move once raids open.

### Dual spec at 40

Buy it from your trainer for 50g at level 40. The common pairings:

- **Retribution + Protection:** quest as Ret, tank dungeons as Prot. The most popular choice.
- **Retribution + Holy:** for players who want to heal dungeons or join a raid as a healer.
- **Protection + Holy:** for dedicated group players.

Swapping is free outside combat and battlegrounds. Changing talents *within* a spec still costs a respec fee, which decays to 1g over time.

---

## Abilities & rotation

### Key trained spells by level

| Level | Spells |
|---|---|
| 1 | Devotion Aura, Holy Light, Seal of Righteousness |
| 4 | Blessing of Might, Judgement |
| 6 | **Holy Strike**, Divine Protection, Seal of the Crusader |
| 8 | Hammer of Justice, Purify |
| 10 | **Seal of Fury**, **Righteous Fury**, Lay on Hands, Blessing of Protection |
| 12 | Redemption (class quest) |
| 14 | Blessing of Wisdom |
| 16 | Retribution Aura |
| 18 | Blessing of Freedom |
| 20 | **Consecration**, **Blessing of Kings**, Exorcism, Flash of Light |
| 22 | Concentration Aura, Seal of Justice |
| 24 | Turn Undead |
| 28 / 32 / 36 | Shadow / Frost / Fire Resistance Aura |
| 30 | Divine Intervention |
| 34 | Divine Shield |
| 38 | Seal of Wisdom |
| 40 | Summon Warhorse (class mount; see below) |
| 42 | Cleanse |
| 44 | Hammer of Wrath |
| 46 | Blessing of Sacrifice |
| 50 | Holy Wrath |
| 52 / 54 / 60 | Greater Blessing of Might / Wisdom / Kings |

Source: a beta spellbook listing (build 70755). Newly learned spells are **not** placed on your bars automatically in Forever, so check your spellbook after every training visit.

### Rotations

=== "Retribution"

    !!! rotation "Retribution priority"

        <div class="priority" markdown>

        1. Keep a Seal up: **Seal of Righteousness** until 20, then **Seal of Command** with a slow two-hander (3.2 s or slower).
        2. **Judgement** on cooldown. It is off the GCD and no longer eats your Seal, so there is nothing to reapply.
        3. **Holy Strike** on cooldown.
        4. **Consecration** when two or more enemies are on you.
        5. On a tough mob: **Hammer of Justice**, then Judgement and Holy Strike while it is stunned.
        6. **Exorcism** on undead and demons; **Hammer of Wrath** (44+) as an execute.

        </div>


    **Unsealed Wrath (40+):** swing a few times with one Seal to build stacks, then switch Seals. The next hit with the new Seal fires each stored Seal's proc once. A common pattern is to build on Seal of Command and switch to Seal of Righteousness just before a slow swing lands. Timing is still being worked out, and the talent's value at launch is not settled.

=== "Protection"

    !!! rotation "Protection priority"

        <div class="priority" markdown>

        1. **Righteous Fury** on, **Seal of Fury** up.
        2. Pull with **Judgement**, or with **Swift Judgement** for a second instant hit.
        3. **Consecration** on packs; it is your main AoE threat.
        4. **Holy Strike** on cooldown (every 6 s with Shieldsworn), **Holy Shield** kept up.
        5. If a mob runs loose: **Judgement of Fury** taunts it (10 yd).
        6. Emergencies: **Templar's Bulwark**, then Divine Protection or Lay on Hands. Bulwark and Divine Shield share Forbearance, so do not plan to chain them.

        </div>


=== "Holy"

    !!! rotation "Holy priority"

        <div class="priority" markdown>

        1. **Oath of Light** on the tank before the pull, and keep it up (5 minutes).
        2. **Holy Light** (downranked) for steady healing on the Oath target; **Flash of Light** for efficient top-ups.
        3. **Holy Shock** for instant emergencies; on non-Oath targets it gets Boundless Light's crit.
        4. **Light's Vigil** before a big hit: the next Holy Shock has no cooldown and splashes the tank's party.
        5. **Divine Favor** + Holy Light for a guaranteed big crit.
        6. Cleanse poisons, diseases and magic. Keep **Concentration Aura** up if you are being hit.

        </div>


### Useful macros

??? example "Show 3 macros"

    ```
    #showtooltip Judgement
    /castsequence reset=target Seal of Righteousness, Judgement
    ```

    ```
    #showtooltip Holy Strike
    /startattack
    /cast Holy Strike
    ```

    ```
    #showtooltip Blessing of Kings
    /cast [@mouseover,help,nodead][help,nodead][@player] Blessing of Kings
    ```

    !!! tip "Bars"
        Keep Divine Protection, Lay on Hands and Hammer of Justice on easy keys. Put your Seals together so you can swap quickly for Unsealed Wrath.

---

## Leveling walkthrough 1–60

Retribution is the most common leveling spec; Protection works well for dungeon-heavy leveling. Forever's dungeons give *less* mob XP and *much more* quest XP, so pick up every dungeon quest before you zone in. Mana is the limit early: drink between pulls and use Seal of Righteousness, which is cheap.

!!! tip "Class trainers"
    Alliance paladins train in Stormwind or Ironforge. Forsaken paladins have **no trainer in Undercity or Orgrimmar**; they train at **Bandarion Keep** (Tirisfal), Brill or Deathknell. Plan your return trips — see [Undead Paladin](undead.md#route-to-60).

<div class="route" markdown>

### 1–10: Starting zone

- **Zones:** Elwynn Forest (Human), Dun Morogh (Dwarf), Tirisfal Glades (Undead).
- **Train:** Holy Strike at 6, Hammer of Justice at 8, then **Seal of Fury, Righteous Fury and Lay on Hands at 10**.
- Pick up **Cooking** and the camping quest *The Great Outdoors* around level 5 (see [Camping](../../systems/camping.md)).
- Take a gathering profession from the starter quest; Mining is the usual pick.
- **First talent point at 10:** Benediction (Retribution) or Redoubt (Protection).

### 10–20

- **Alliance:** Westfall or Loch Modan, then Redridge.
- **Horde:** Silverpine Forest, with trips to the Barrens.
- **Class quest at 12:** **Redemption** (*A Lesson in Divinity* for Forsaken; the Classic *Tome of Divinity* chain for Alliance).
- **Dungeons:** [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) (13–18, Ironforge), Ragefire Chasm, [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) (15–22, Tirisfal), the Deadmines, Wailing Caverns.
- **Weapon:** Rhahk'Zor's Hammer (Deadmines) is a strong slow two-hander for Seal of Command. Scepter of the Abandoned is a new one-hander with spell power for Holy.
- **Level 20:** Consecration, Blessing of Kings, Exorcism, Flash of Light, Seal of Command (talent). Your **weapon class quest** opens around here: *Verigan's Fist* for Alliance, *Wolfsbane* for Forsaken.
- **Library books:** at 20, turning in 10 books unlocks your first paladin library quest. Books come from Garion Wendell (Stormwind) or Owen Thadd (Undercity). Rewards for paladins are not yet documented.

### 20–30

- **Alliance:** Wetlands, Redridge, Duskwood, Ashenvale.
- **Horde:** Hillsbrad Foothills, Stonetalon Mountains, Ashenvale.
- **Dungeons:** Shadowfang Keep, [Excavation Site: Wetlands](../../content/dungeons/excavation-site.md), the Stockade, [City of Dalaran](../../content/dungeons/city-of-dalaran.md) (Alliance only for Kirin Tor quests; Horde are attacked in Dalaran), Blackfathom Deeps.
- **Talents:** finish Pursuit of Justice and Two-Handed Weapon Specialization; Sacred Arbiter at 29.
- **Legacy:** your first paladin Legacy Point arrives at **25**.
- **Battlegrounds:** Warsong Gulch from 10 and Arathi Basin from 20 are good breaks.

### 30–40

- **Alliance:** Arathi Highlands, Alterac Mountains, Stranglethorn Vale, Desolace.
- **Horde:** Arathi Highlands, Thousand Needles, Stranglethorn Vale, Desolace.
- **Dungeons:** Razorfen Kraul, Gnomeregan, Scarlet Monastery (Graveyard, Library, Armory, Cathedral), [The Drowned City](../../content/dungeons/drowned-city.md) (35–40).
- **Library quest at 35** (20 books).
- **Talents:** Vengeance, Repentance, Champion of the Light.
- **Level 40:** plate armor, **Apprentice Riding** (100g including a racial mount), the paladin **Warhorse**, and **dual spec** (50g). Budget about 150g for 40.
- **Darkspear Islands** battleground opens at 30.

!!! note "Warhorse at 40"
    Sources disagree on whether the level-40 paladin mount is a trainer spell, a quest, or both. The Forsaken version's quest (*A Trusty Steed* in datamined text) has no confirmed giver. Keep 100g for Apprentice Riding either way.

### 40–50

- **Contested:** [Riverglades](../../world/zones.md#riverglades) (35–45; Farholde Keep for Alliance, Rog'mar for Horde) is the big new zone of this range, with 150+ quests.
- **Also:** Dustwallow Marsh, Badlands, Swamp of Sorrows, Tanaris, Feralas, Hinterlands. Desolace centaur quests now need level 35.
- **Dungeons:** [Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md) (40–45), Razorfen Downs, Uldaman, Zul'Farrak, [Alcaz Prison](../../content/dungeons/alcaz-prison.md) (48–53), Maraudon.
- **Library quest at 45** (25 books); second paladin Legacy Point at **45**.
- **Talents:** Unsealed Wrath (as soon as you have 30 Ret points and Repentance), then the Holy tree.
- Hammer of Wrath at 44 and Holy Wrath at 50.

### 50–60

- **Zones:** Azshara (many new quests), Felwood, Un'Goro Crater, Western and Eastern Plaguelands, Winterspring, Burning Steppes, Silithus.
- **Dungeons:** Sunken Temple, Blackrock Depths, Dire Maul, [Blackmaw Hold](../../content/dungeons/blackmaw-hold.md) (55–60), Lower Blackrock Spire, Scholomance, Stratholme, [Shaper's Terrace](../../content/dungeons/shapers-terrace.md) (58–60).
- Undead-heavy Scholomance and Stratholme are paladin-friendly: Exorcism, Holy Wrath and Turn Undead all work on most of their mobs.
- **Level 60:** third paladin Legacy Point, Journeyman Riding (1,000g), the **epic mount quest** (Charger for Alliance; *Forsaken Charger* "in the name of Retribution" for Undead), and [Mount Hyjal](../../world/zones.md#mount-hyjal).

</div>

---

## Dungeons

**Tanking (Protection).** Righteous Fury and Seal of Fury from level 10 make the paladin a real tank from the first dungeon. Open with Judgement or Swift Judgement, then Consecration. Mark one target for crowd control on big pulls, because Consecration only hits 4 mobs at full damage. Meeting stones cannot summon in Forever, so be at the entrance on time.

**Healing (Holy).** Keep Oath of Light on the tank. Flash of Light is your efficient heal; save Holy Shock for spikes. Cleanse is a big asset in Wailing Caverns, Razorfen Downs, Scholomance and Stratholme.

**DPS (Retribution).** Use Blessing of Might or Kings on the group. Stay behind the mob, don't break crowd control with Consecration, and offer to off-tank with Judgement of Fury when a mob runs loose.

| Level | Recommended | Why for paladins |
|---|---|---|
| 13–22 | [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) (A) / [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) (H) | First new dungeons; undead-heavy Ruins suits Exorcism |
| 18–26 | Deadmines / Wailing Caverns | Rhahk'Zor's Hammer; Wolfsbane materials |
| 20–30 | Shadowfang Keep | Wolfsbane ingot (Forsaken); good two-handers |
| 26–35 | [Excavation Site](../../content/dungeons/excavation-site.md), [City of Dalaran](../../content/dungeons/city-of-dalaran.md) | New blues and camp blueprints |
| 30–45 | Scarlet Monastery | Ravager (Herod, Armory) is a classic Ret two-hander |
| 35–47 | [The Drowned City](../../content/dungeons/drowned-city.md), [Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md) | New mid-level blues |
| 48–55 | [Alcaz Prison](../../content/dungeons/alcaz-prison.md), Maraudon | — |
| 55–60 | BRD, LBRS, [Blackmaw Hold](../../content/dungeons/blackmaw-hold.md), Scholomance, Stratholme, [Shaper's Terrace](../../content/dungeons/shapers-terrace.md) | Pre-raid gear |

See [Dungeons](../../content/dungeons/index.md) for every instance.

---

## Raid preparation

Raids open on **9 December 2026**: [The Barrow Deeps](../../content/raids/barrow-deeps.md) (10), [Hyjal Summit](../../content/raids/hyjal-summit.md) (20) and [Onyxia's Lair](../../content/raids/onyxias-lair.md) (40). See [Raids](../../content/raids/index.md).

**Your raid role.** In 10- and 20-player raids every class buff counts. Expect to bring Kings, a resistance aura where needed, and Cleanse. Without Salvation, tanks carry more of the threat game.

- **Holy:** the most likely raid role. Build Intellect, healing power and mana regeneration.
- **Protection:** a solid off-tank or main tank in 10s and 20s. Reach the Defense needed to avoid crits (Classic's target was 440 Defense; Forever's has not been published).
- **Retribution:** brings utility and steady damage. Hit gear matters; Dwarf's Artisan's Precision helps.

**Pre-raid gear.** Forever's dungeon loot has new itemization, so Classic pre-raid lists don't apply. Run the 55–60 dungeons, the new ones especially, and pick the best item per slot for your role. A set of resistance gear may be useful; Onyxia needs Fire resistance on tanks in Classic.

**Onyxia attunement.** You need the **Drakefire Amulet**. Start the chain early; it is long.

**Consumables.** Mana potions (healing potions are now made with First Aid), elixirs, food buffs (Gourmand makes them last longer), weapon stones or oils. Camp buffs don't stack with the matching class buff.

---

## PvP

- **Battlegrounds:** Warsong Gulch, Arathi Basin, Alterac Valley, and the new [Battle for the Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands) (15v15, 30–60). Paladins excel as flag carriers and node defenders thanks to Blessing of Freedom, Divine Shield and self-healing.
- **Retribution:** burst with Seal of Command, Judgement, Holy Strike and Hammer of Justice. Repentance and Hammer of Justice give two controls. Blessing of Freedom counters slows.
- **Holy / Shockadin:** a durable healer. Voice of Truth (trained) protects your casts from interrupts for 6 s.
- **World PvP:** Forever runs PvP rulesets on megaservers. Divine Shield and Lay on Hands make paladins hard to gank, but you can't chase.
- **Ranks and Honor:** see [PvP](../../content/pvp/index.md). The Legacy talent *For Great Honor* adds up to +10% Honor.

**Matchups (general, Classic-era knowledge adjusted for Forever).**

| Opponent | Notes |
|---|---|
| Warrior | You out-sustain them. Save Blessing of Freedom for Hamstring and Hammer of Justice for their burst. |
| Rogue | Stuns are the threat. Humans have Will to Survive; Dwarfs remove poisons with Stoneform. |
| Mage / Warlock | Kiting and fears. Undead have Will of the Forsaken; everyone else needs Blessing of Freedom and patience. |
| Priest | Purge/dispel strip your buffs. Use Voice of Truth when they try to lock out heals. |
| Hunter | Close the gap with Pursuit of Justice and Freedom. Scatter Shot blocks Will of the Forsaken. |
| Druid / Shaman | Long fights. Save Hammer of Justice for their heal. |

---

## Gear, stats & enchants

| Spec | Stat priority (leveling → 60) |
|---|---|
| **Retribution** | Weapon DPS and a slow speed → Strength and crit → hit (to the cap at 60) → Stamina → Intellect (spell damage via Champion of the Light) |
| **Protection** | Stamina and Defense → block value and block → hit → Strength |
| **Holy** | Intellect and healing power → mana regeneration → crit → Stamina |

!!! conflict "Conflict: Retribution stat priority"
    ConquestCapped puts Stamina, Spirit and Intellect ahead of Strength for leveling, arguing most damage comes from abilities. Leprestore puts weapon DPS, Strength and crit first. Both agree weapon quality matters most.

- **Hit sources:** Divine Precision (Holy), Precision (Protection), and Dwarf's Artisan's Precision all add hit, so hit gear is less crucial than in Classic.
- **Weapon imbues** now stack with stones and oils.
- **Enchants:** Crusader on a Retribution weapon is the Classic standard. Forever's enchant list has not been fully published.
- **Transmog:** account-wide, same armor type only. Plate appearances need plate (40+).

---

## Professions & Legacy

<p class="divider">Professions</p>

Paladins wear plate at 40, and Blacksmithing covers all three specs.

<div class="prof-picks" markdown>

<div class="prof-pick prof-pick--best" markdown>

<p class="prof-rank" markdown>**S**{ .tier .tier-s } Best pick</p>

<p class="prof-pair" markdown>:material-pickaxe: Mining <span class="prof-plus">+</span> :material-anvil: Blacksmithing</p>

<p class="prof-for">Best for: All three specs</p>

<div class="pills" markdown>
**Leveling**{ .pill .pill--success .pill--sm } **Raids**{ .pill .pill--info .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
</dl>

- The Paladin standard
- Many new BoP patterns, including mail spell power gear before 40

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Lodestone (melee AP) · Sharpening Wheel (Strength)</p>

</div>

<div class="prof-pick prof-pick--alt" markdown>

<p class="prof-rank" markdown>**A**{ .tier .tier-a } Strong alternative</p>

<p class="prof-pair" markdown>:material-pickaxe: Mining <span class="prof-plus">+</span> :material-cog: Engineering</p>

<p class="prof-for">Best for: PvP</p>

<div class="pills" markdown>
**PvP**{ .pill .pill--danger .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:40%"><span>2/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:100%"><span>5/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:40%"><span>2/5</span></span></dd>
</dl>

- PvP gadgets

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Lodestone (melee AP) · Reagent Bot</p>

</div>

<div class="prof-pick prof-pick--sit" markdown>

<p class="prof-rank" markdown>**B**{ .tier .tier-b } Situational</p>

<p class="prof-pair" markdown>:material-leaf: Herbalism <span class="prof-plus">+</span> :material-flask: Alchemy</p>

<p class="prof-for">Best for: Holy healers</p>

<div class="pills" markdown>
**Raids**{ .pill .pill--info .pill--sm } **Gold**{ .pill .pill--gold .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:100%"><span>5/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
</dl>

- Self-supplied elixirs and mana potions

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Incense Candle (Intellect) · Mana Well (mana regen)</p>

</div>

</div>

<p class="legend" markdown>Codex ratings out of 5, based on the sources above. Compare every class in [Best professions by class](../../characters/professions.md#best-professions-by-class).</p>

<div class="pills" markdown>
**:material-medical-bag: First Aid · healing potions**{ .pill .pill--success } **:material-pot-steam: Cooking · campfires**{ .pill .pill--info } **:material-fish: Fishing · Fish Bowl**{ .pill .pill--info }
</div>

**Secondary skills.** Take First Aid on every character; it now makes healing potions. Cooking and Fishing feed the camping system.

!!! tip "Race notes"
    **Dwarf, Human, Undead:** no profession racials; pick freely.

Crafting professions award [Legacy Points](../../characters/legacy.md) at skill 150, 225 and 300, and each profession adds a [camp feature](../../systems/camping.md). Professions give no passive stats in Forever.

**Legacy talents** (up to 16 points per character):

- **Thrill of Adventure** (Adventure): restores health and mana on non-trivial kills in the open world. Best leveling pick for a mana-starved class.
- **Well Rested** then **Talented**: talent points from an earlier level.
- **Reagent Economy** (Resourcefulness): no vendor reagents for class spells (Symbol of Kings, Symbol of Divinity).
- **Permanence**: longer class buffs.
- **For Great Honor** for PvP, **Diplomat** for reputation grinds.

Paladin class Legacy Points come at levels **25, 45 and 60**. See [Legacy System](../../characters/legacy.md).

---

## Hardcore notes

!!! hardcore "Hardcore survival"

    The Hardcore ruleset arrives this winter. Paladins are among the safest Hardcore classes, but their survival tools need discipline.

    - **Divine Protection** at 6 and **Divine Shield** at 34 are escape buttons; hearth while shielded if a pull goes wrong.
    - **Lay on Hands** is now on a 20-minute cooldown, so you'll have it for most bad fights.
    - **Templar's Bulwark** and Divine Shield share **Forbearance**. Plan for one, not both.
    - No slow or interrupt: avoid fleeing humanoids near other packs and casters you can't reach.
    - Keep Blessing of Freedom handy for roots and snares.
    - Undead can drop fear with Will of the Forsaken. Humans can break stuns with Will to Survive.

---

## Common mistakes & FAQ

??? question "Does Judgement still eat my Seal?"
    No. In Forever, Judgement leaves the Seal active, so you don't need to recast it after judging.

??? question "Where is Blessing of Salvation?"
    Removed before launch, along with Mass Salvation, Blessing of Light and Blessing of Sanctuary.

??? question "Can I seal-twist?"
    Not in the Classic sense. Retribution's capstone **Unsealed Wrath** replaces twisting: swing with one Seal to store copies, then switch Seals.

??? question "Can I be a Shockadin with Unsealed Wrath?"
    No. Holy Shock needs 21 Holy points and Unsealed Wrath needs 31 Retribution, which is 52 points. You have 51.

??? question "Why does my Consecration feel weaker on big pulls?"
    Full damage only applies to the first 4 targets.

??? question "My new spells aren't on my action bar."
    Forever no longer adds newly learned spells to your bars. Open the spellbook after training.

??? question "Where do Horde paladins train?"
    At Bandarion Keep, Brill or Deathknell in Tirisfal Glades. Not in Undercity or Orgrimmar.

---

## Sources

??? quote "15 sources"

    - [Warcraft Tavern: All Changes to Paladins in WoW Forever](https://www.warcrafttavern.com/forever/news/all-changes-to-paladins-in-wow-forever/) (September beta)
    - [Warcraft Tavern: Class Trainer Locations](https://www.warcrafttavern.com/forever/guides/class-trainers/)
    - [Warcraft Tavern: Seal Twisting & Shockadins, Paladin Deep Dive](https://www.warcrafttavern.com/forever/news/seal-twisting-shockadins-paladin-deep-dive-for-wow-forever/)
    - [Warcraft Tavern: Pre-Launch Class Changes](https://www.warcrafttavern.com/forever/news/wow-forever-pre-launch-class-changes-bug-fixes/)
    - [Kami Labs: November 2 patch notes](https://kami-labs.fr/en/wow-forever/patch-notes-2-novembre-notes-de-lancement/)
    - [Method: Paladin Leveling Guide & Talents](https://www.method.gg/wow-forever/wow-forever-paladin-leveling-guide-and-talents)
    - [ConquestCapped: Paladin Leveling](https://conquestcapped.com/guides/wow-forever/wow-forever-paladin-leveling/)
    - [ConquestCapped: Paladin Mount Guide](https://conquestcapped.com/guides/wow-forever/wow-forever-paladin-mount/)
    - [Talents Forever: Paladin leveling orders](https://talentsforever.com/paladin/leveling)
    - [Leprestore: Retribution Paladin Guide](https://leprestore.com/guides/world-of-warcraft-forever/wow-forever-retribution-paladin-guide-best-builds-race-professions/)
    - [ForG: Forsaken Paladin class quests](https://forg.gg/en/forever/tips/forsaken-paladin)
    - [ForG: Wolfsbane](https://forg.gg/en/forever/wolfsbane)
    - [LFCarry: Undead Paladin guide](https://lfcarry.com/guides/wow-forever-undead-paladin)
    - [ChaosBoost: Undead Paladin guide](https://www.chaosboost.com/articles/wow-forever-undead-paladin-guide)
    - [ForeverDB: Paladin lore](https://foreverdb.net/lore/class/paladin)
