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
    We wrote this guide 3 days after launch (Patch 1.60.1). Blizzard rebuilt the paladin trees on **30 October** and changed the values again in the **2 November** pre-launch notes. Thus, many guides from the beta are out of date. Blizzard said that a larger balance update will come when players get to level 30–39. Reference data is on the [Paladin class page](../../characters/classes/paladin.md).

## Overview

The paladin is a hybrid class that wears plate. It can do melee damage, heal and tank. Forever gives it the tools that it did not have in Classic: a real taunt, an early tank seal, a melee strike with a short cooldown, and a much shorter Lay on Hands cooldown.

<aside class="infobox" markdown>
<p class="infobox-title">Paladin at a glance</p>

| | |
|---|---|
| **Roles** | Tank (Protection), healer (Holy), melee DPS (Retribution) |
| **Armor / weapons** | Plate from 40 (mail before); shields; one- and two-hand swords, maces and axes; polearms |
| **Resource** | **Mana**{ .pill .pill--mana } |
| **Races** | [Human](human.md), [Dwarf](dwarf.md) (Alliance) · [Undead](undead.md) (Horde, **new**) |
| **Class trainers** | Stormwind (Cathedral of Light), Ironforge (Mystic Ward), Northshire, Goldshire, Coldridge Valley, Thunderbrew Distillery, Theramore · Deathknell, Brill, **Bandarion Keep** (Tirisfal) |

</aside>

<div class="proscons" markdown>
<div class="pros" markdown>

Strengths

- Very difficult to kill: plate, a shield, Divine Protection, Divine Shield, Lay on Hands every 20 minutes, and self-healing.
- Useful to the group: blessings now last 1 hour, Blessing of Kings is baseline, and resistance auras protect the raid.
- Protection is now a full tank, with a taunt on Judgement of Fury and Consecration from level 20.
- One of the best classes for AoE pulls of dungeon mobs at low levels, but Consecration does full damage to a maximum of 4 targets.

</div>
<div class="cons" markdown>

Weaknesses

- **Mana** is the main limit for all specs while you level.
- No interrupt and no slow. It is difficult to fight casters and mobs that run away.
- Holy Shock (21 Holy) and Unsealed Wrath (31 Retribution) do not both fit in 51 points. Thus, the traditional "Shockadin with seal twisting" hybrid is not possible.

</div>
</div>

### What is new in Forever

| Change | Effect |
|---|---|
| **Holy Strike** (level 6) | Baseline instant melee strike that does part weapon damage and part Holy damage. The cooldown is 10 s at launch (12 s in the early beta). |
| **Judgement keeps your Seal** | Judgement no longer removes the Seal, and Judgement is off the GCD. Judgement debuffs last 40 s. |
| **Seal of Fury** (level 10) | Tank seal: Holy damage with each swing and a small absorb. Judgement of Fury **taunts** (10 yd). |
| **Righteous Fury** (level 10) | It was level 16. +33% threat, +90% Holy threat. |
| **Consecration** (level 20) | Baseline for all specs. Full damage only on the first 4 targets. |
| **Blessings** | Kings is baseline. Improved Wisdom is baseline. 5-minute blessings and Greater Blessings last 1 hour. |
| **Lay on Hands** | 20-minute cooldown (it was 1 hour). |
| **Voice of Truth** | Now a trained spell: 6 s immunity to silence and interrupt, 3-minute cooldown. |
| **Removed** | Blessing of Salvation, Mass Salvation, Blessing of Light, Greater Blessing of Light, Blessing of Sanctuary, Sanctity Aura, Revoke, Instrument of the Law. |
| **Dual spec** | Level 40, 50g, at your class trainer. |

!!! note "No Salvation"
    Without Blessing of Salvation, DPS players no longer get a 30% threat decrease. Expect tanks to be more important. Expect groups to ask DPS paladins for Might, Wisdom or Kings.

---

## Specs & talents

!!! tip "Full talent guide"
    The [Paladin talent guide](../../talents/paladin.md) gives a rating to each talent and a talent for each level from 10 to 60. Its tree data is from the launch client. If this section and the talent guide disagree, use the talent guide.

Talents start at level 10, with one point per level, and 51 points at level 60. Each tree has "gold" talents with 1 point at **11, 16, 21 and 31** points. You buy a respec and dual spec from a paladin trainer.

!!! warning "Builds are provisional"
    The talent trees changed on 30 October and again on 2 November. The point orders below come from guides that were updated on launch day and from usage data from talent planners. Read the in-game tooltip before you spend points.

=== "Retribution"

    **Role:** melee DPS with a two-hand weapon and the default spec to level.

    | Talent | Ranks | What it does (launch values) |
    |---|---|---|
    | Benediction | 5 | Instant spells cost less mana |
    | Improved Judgement | 2 | −2 s Judgement cooldown at 2/2 |
    | Conviction | 3 | +2/4/6% crit with all spells and attacks |
    | Sanctified Judgement | 3 | Gives back mana when you use Judgement |
    | Seal of Command | 1 | The traditional seal for large swings |
    | Pursuit of Justice | 2 | +15% movement speed at 2/2 |
    | Two-Handed Weapon Specialization | 3 | +2/4/6% damage with two-hand weapons, less threat |
    | **Sacred Arbiter** (16) | 1 | Holy Strike does more damage and refreshes your Judgement on the target |
    | Vengeance | 3 | Damage buff after crits, up to 5 stacks |
    | **Repentance** (21) | 1 | Incapacitate; necessary for Unsealed Wrath |
    | Vindication | 3 | Decreases the attack power of the target |
    | **Champion of the Light** | 5 | 12% of Intellect per rank as spell damage (60%); faster Hammer of Wrath |
    | Eye for an Eye | 2 | Reflects crit damage (PvP) |
    | Turn Evil | 2 | Faster Turn Undead, now also affects Demons |
    | **Unsealed Wrath** (31) | 1 | Melee swings keep a copy of your Seal (up to 3 stacks, 15 s). When you swing with a *different* Seal, each kept Seal gets its proc chance |

    !!! conflict "Conflict: Twist of Light"
        Older guides (and the beta deep dive) show **Twist of Light**, a final talent for seal twisting with an "Echo" when you change seals. The 30 October rework **replaced** it with Unsealed Wrath. Some fan pages still show both.

=== "Protection"

    **Role:** shield tank. Protection in Forever has a taunt, an absorb seal and a strong emergency ability.

    | Talent | Ranks | What it does |
    |---|---|---|
    | Redoubt | 5 | +6% block per rank |
    | Divine Intellect | 5 | +Intellect % (moved here from Holy) |
    | Precision | 3 | +hit |
    | Sacred Duty | 2 | −30 s per rank on Divine Shield, Divine Protection and Templar's Bulwark; shorter Forbearance |
    | Shield Specialization | 2 | +block value; chance to give back mana when you block |
    | **Templar's Bulwark** (row 3) | 1 | Absorbs damage equal to 100% of maximum health for 8 s. 5-minute cooldown. Causes Forbearance and is now a Magic effect that enemies can dispel |
    | Toughness | 5 | Armor |
    | Improved Righteous Fury | 3 | 3/6/9% damage reduction |
    | **Swift Judgement** | 1 | Immediately releases your Seal on a target in 10 yd. It does not remove the Seal and does not share the Judgement cooldown |
    | Anticipation | 5 | +Defense (up to +20) |
    | **Holy Shield** (21) | 1 | 4 charges, +30% block, Holy damage on each block |
    | Reckoning | 5 | More attacks after blocks |
    | Iron Creed | 3 | +10/20/30% Holy Strike threat; short damage reduction |
    | Deflection | 5 | Parry |
    | Stoicism | 2 | −10/20% stun and charm duration |
    | **Shieldsworn** (31) | 1 | Holy Strike −4 s cooldown, and it hits with your shield (this triggers block talents). For a short time, you can block spells |

    !!! conflict "Conflict: Improved Seal of Fury"
        In the beta deep dive, **Improved Seal of Fury** was the 11-point Protection talent. The 30 October rework removed it, together with One-Handed Weapon Specialization.

=== "Holy"

    **Role:** healer for one target and for the party. In PvP and in groups of 2, a "Shockadin" melee hybrid.

    | Talent | Ranks | What it does |
    |---|---|---|
    | Spiritual Focus | 5 | Protection against pushback on Holy Light, Flash of Light and Light's Vigil |
    | Reverence | 2 | 15% mana regeneration per rank while you cast |
    | Healing Light | 3 | Stronger Holy Light and Flash of Light |
    | Illumination | 5 | Gives back mana when a heal crits |
    | **Divine Favor** (16) | 1 | Your next heal is always a crit |
    | Holy Conduit | 2 | −40% mana on the Holy spells in the tooltip (moved here from Retribution) |
    | Infusion of Light | 2 | Proc from heal crits |
    | **Oath of Light** | 1 | 5-minute oath on one ally: your Holy Light, Flash of Light and Holy Shock heal that ally for more. Only one Oath at a time |
    | Divine Precision | 2 | +4% hit per rank with Holy spells; shorter silences |
    | **Holy Shock** (21) | 1 | Instant heal or damage, **10 s** cooldown (it was 30) |
    | Boundless Light | 2 | +15/30% crit on Holy Shock when you cast it on an ally that does *not* have your Oath |
    | Purifying Power | 2 | Cleanses cost less, and Exorcism/Holy Wrath are stronger (Classic effect; not examined again) |
    | Holy Power | 5 | +10% crit-heal bonus per rank (up to 50%) |
    | Divine Strength | 5 | Strength (Retribution players often take it) |
    | Improved Seals | 5 | +3% seal damage per rank |
    | **Light's Vigil** (31) | 1 | Only on friendly targets since 30 October: the next Holy Shock of the target has no cooldown and also heals the party of the target |

### Recommended builds

**Leveling (Retribution, then a second spec at 40).** The two launch orders that players use most have the same structure. Only the order of the picks at level 15–23 is different.

<div class="milestones" markdown>

Lv 10–14
:   Benediction 5/5

Lv 15–19
:   Improved Judgement 2/2, Conviction 3/3 (in either order)

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
:   Unsealed Wrath (immediately when it is available), Divine Strength 5/5

Lv 46–55
:   Improved Seals 5/5, Divine Intellect 5/5

Lv 56–60
:   Precision 3/3 *or* Reverence 2 + Holy Conduit 2

</div>

The result is **12/8/31** (Holy/Protection/Retribution). This is also the level 60 PvE Retribution build that sources give most often.

!!! conflict "Conflict: when to start Retribution's 15–23 points"
    The usage data from Talents Forever has Improved Judgement at 15–16 and Seal of Command at about 23. Leprestore takes Conviction first and Seal of Command at 20. Both orders are good. If you already use a slow two-hand weapon, take Seal of Command at 20.

**Endgame templates (level 60).**

| Spec | Split | Core |
|---|---|---|
| Retribution PvE | 12/8/31 | Divine Strength, Improved Seals, Holy Conduit · Divine Intellect, Precision 3 · full Ret to Unsealed Wrath |
| Retribution PvP | 0/14/37 | Adds Vindication 3, Eye for an Eye, Unyielding Faith; on the Prot side, Guardian's Favor, Sacred Duty, Templar's Bulwark, Improved Hammer of Justice |
| Protection tank | ~0/40/11 | Redoubt, Templar's Bulwark, Holy Shield, Reckoning, Iron Creed, Anticipation, Shieldsworn; on the Ret side, Improved Judgement, Conviction, Sanctified Judgement |
| Holy raid healer | ~32/11/8 | Holy to Light's Vigil with Oath of Light and Boundless Light; Divine Intellect and Sacred Duty; Benediction and Conviction |

These builds are snapshots of usage data. They are not tested theory. The exact point splits will change when raids open.

### Dual spec at 40

Buy it from your trainer for 50g at level 40. The usual pairs are:

- **Retribution + Protection:** do quests as Ret, and tank dungeons as Prot. This is the most popular choice.
- **Retribution + Holy:** for players who want to heal dungeons or heal in a raid.
- **Protection + Holy:** for players who play mostly in groups.

You can change specs for free outside combat and battlegrounds. If you change talents *in* a spec, you must pay a respec cost. This cost decreases to 1g over time.

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

Source: a spellbook list from the beta (build 70755). In Forever, the game does **not** put new spells on your bars automatically. Thus, look at your spellbook after each visit to a trainer.

### Rotations

=== "Retribution"

    !!! rotation "Retribution priority"

        <div class="priority" markdown>

        1. Always have a Seal active: **Seal of Righteousness** until 20, then **Seal of Command** with a slow two-hand weapon (3.2 s or slower).
        2. Use **Judgement** on cooldown. It is off the GCD and no longer removes your Seal, so you do not need to apply the Seal again.
        3. Use **Holy Strike** on cooldown.
        4. Use **Consecration** when 2 or more enemies attack you.
        5. Against a strong mob: use **Hammer of Justice**, then Judgement and Holy Strike while the mob is stunned.
        6. Use **Exorcism** on undead and demons. Use **Hammer of Wrath** (44+) to kill a target with low health.

        </div>


    **Unsealed Wrath (40+):** swing some times with one Seal to get stacks. Then change Seals. The next hit with the new Seal triggers the proc of each kept Seal one time. A usual method is to get stacks with Seal of Command, then change to Seal of Righteousness immediately before a slow swing hits. Players are still testing the timing, and the value of the talent at launch is not certain.

=== "Protection"

    !!! rotation "Protection priority"

        <div class="priority" markdown>

        1. Keep **Righteous Fury** and **Seal of Fury** active.
        2. Pull with **Judgement**, or with **Swift Judgement** for a second instant hit.
        3. Use **Consecration** on packs. It is your main AoE threat.
        4. Use **Holy Strike** on cooldown (every 6 s with Shieldsworn). Keep **Holy Shield** active.
        5. If a mob attacks another player, use **Judgement of Fury** to taunt it (10 yd).
        6. In emergencies, use **Templar's Bulwark**, then Divine Protection or Lay on Hands. Bulwark and Divine Shield share Forbearance, so do not plan to use them one after the other.

        </div>


=== "Holy"

    !!! rotation "Holy priority"

        <div class="priority" markdown>

        1. Put **Oath of Light** on the tank before the pull, and keep it active (5 minutes).
        2. Use **Holy Light** (a lower rank) for constant healing on the Oath target. Use **Flash of Light** for small heals that use little mana.
        3. Use **Holy Shock** for instant emergency heals. On targets without your Oath, it gets the crit from Boundless Light.
        4. Use **Light's Vigil** before a large hit. The next Holy Shock has no cooldown and also heals the party of the tank.
        5. Use **Divine Favor** + Holy Light for a large crit that is certain.
        6. Cleanse poisons, diseases and magic. If enemies hit you, keep **Concentration Aura** active.

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
        Put Divine Protection, Lay on Hands and Hammer of Justice on keys that are easy to push. Put your Seals near each other, so that you can change them quickly for Unsealed Wrath.

---

## Leveling walkthrough 1–60

Retribution is the most usual spec to level. Protection is good if you level mostly in dungeons. In Forever, dungeon mobs give *less* XP and quests give *much more* XP. Thus, get all the dungeon quests before you go into a dungeon. Mana is the limit at low levels. Drink between pulls and use Seal of Righteousness, which costs little mana.

!!! tip "Class trainers"
    Alliance paladins train in Stormwind or Ironforge. Forsaken paladins have **no trainer in Undercity or Orgrimmar**. They train at **Bandarion Keep** (Tirisfal), Brill or Deathknell. Plan your trips back to the trainer. See [Undead Paladin](undead.md#route-to-60).

<div class="route" markdown>

### 1–10: Starting zone

- **Zones:** Elwynn Forest (Human), Dun Morogh (Dwarf), Tirisfal Glades (Undead).
- **Train:** Holy Strike at 6, Hammer of Justice at 8, then **Seal of Fury, Righteous Fury and Lay on Hands at 10**.
- At about level 5, learn **Cooking** and get the camping quest *The Great Outdoors* (see [Camping](../../systems/camping.md)).
- Take a gathering profession from the starter quest. Most players choose Mining.
- **First talent point at 10:** Benediction (Retribution) or Redoubt (Protection).

### 10–20

- **Alliance:** Westfall or Loch Modan, then Redridge.
- **Horde:** Silverpine Forest, with trips to the Barrens.
- **Class quest at 12:** **Redemption** (*A Lesson in Divinity* for Forsaken; the Classic *Tome of Divinity* chain for Alliance).
- **Dungeons:** [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) (13–18, Ironforge), Ragefire Chasm, [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) (15–22, Tirisfal), the Deadmines, Wailing Caverns.
- **Weapon:** Rhahk'Zor's Hammer (Deadmines) is a strong slow two-hand weapon for Seal of Command. Scepter of the Abandoned is a new one-hand weapon with spell power for Holy.
- **Level 20:** Consecration, Blessing of Kings, Exorcism, Flash of Light, Seal of Command (talent). Your **weapon class quest** becomes available at about this level: *Verigan's Fist* for Alliance, *Wolfsbane* for Forsaken.
- **Library books:** at 20, turn in 10 books to unlock your first paladin library quest. You get books from Garion Wendell (Stormwind) or Owen Thadd (Undercity). The rewards for paladins are not documented.

### 20–30

- **Alliance:** Wetlands, Redridge, Duskwood, Ashenvale.
- **Horde:** Hillsbrad Foothills, Stonetalon Mountains, Ashenvale.
- **Dungeons:** Shadowfang Keep, [Excavation Site: Wetlands](../../content/dungeons/excavation-site.md), the Stockade, [City of Dalaran](../../content/dungeons/city-of-dalaran.md) (Kirin Tor quests are Alliance only; NPCs in Dalaran attack Horde), Blackfathom Deeps.
- **Talents:** complete Pursuit of Justice and Two-Handed Weapon Specialization. Take Sacred Arbiter at 29.
- **Legacy:** you get your first paladin Legacy Point at **25**.
- **Battlegrounds:** Warsong Gulch from 10 and Arathi Basin from 20 are good breaks.

### 30–40

- **Alliance:** Arathi Highlands, Alterac Mountains, Stranglethorn Vale, Desolace.
- **Horde:** Arathi Highlands, Thousand Needles, Stranglethorn Vale, Desolace.
- **Dungeons:** Razorfen Kraul, Gnomeregan, Scarlet Monastery (Graveyard, Library, Armory, Cathedral), [The Drowned City](../../content/dungeons/drowned-city.md) (35–40).
- **Library quest at 35** (20 books).
- **Talents:** Vengeance, Repentance, Champion of the Light.
- **Level 40:** plate armor, **Apprentice Riding** (100g, with a racial mount), the paladin **Warhorse**, and **dual spec** (50g). Keep about 150g for level 40.
- The **Darkspear Islands** battleground opens at 30.

!!! note "Warhorse at 40"
    Sources do not agree if the level 40 paladin mount is a trainer spell, a quest, or both. The quest for the Forsaken version (*A Trusty Steed* in datamined text) has no confirmed quest giver. In all cases, keep 100g for Apprentice Riding.

### 40–50

- **Contested:** [Riverglades](../../world/zones.md#riverglades) (35–45; Farholde Keep for Alliance, Rog'mar for Horde) is the large new zone for this level range. It has 150+ quests.
- **Also:** Dustwallow Marsh, Badlands, Swamp of Sorrows, Tanaris, Feralas, Hinterlands. The Desolace centaur quests now need level 35.
- **Dungeons:** [Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md) (40–45), Razorfen Downs, Uldaman, Zul'Farrak, [Alcaz Prison](../../content/dungeons/alcaz-prison.md) (48–53), Maraudon.
- **Library quest at 45** (25 books). Second paladin Legacy Point at **45**.
- **Talents:** Unsealed Wrath (when you have 30 Ret points and Repentance), then the Holy tree.
- Hammer of Wrath at 44 and Holy Wrath at 50.

### 50–60

- **Zones:** Azshara (many new quests), Felwood, Un'Goro Crater, Western and Eastern Plaguelands, Winterspring, Burning Steppes, Silithus.
- **Dungeons:** Sunken Temple, Blackrock Depths, Dire Maul, [Blackmaw Hold](../../content/dungeons/blackmaw-hold.md) (55–60), Lower Blackrock Spire, Scholomance, Stratholme, [Shaper's Terrace](../../content/dungeons/shapers-terrace.md) (58–60).
- Scholomance and Stratholme have many undead, so they are good for paladins. Exorcism, Holy Wrath and Turn Undead work on most of their mobs.
- **Level 60:** third paladin Legacy Point, Journeyman Riding (1,000g), the **epic mount quest** (Charger for Alliance; *Forsaken Charger* "in the name of Retribution" for Undead), and [Mount Hyjal](../../world/zones.md#mount-hyjal).

</div>

---

## Dungeons

**Tanking (Protection).** From level 10, Righteous Fury and Seal of Fury make the paladin a real tank in the first dungeon. Start with Judgement or Swift Judgement, then use Consecration. On large pulls, mark one target for crowd control, because Consecration does full damage to only 4 mobs. In Forever, meeting stones cannot summon, so be at the entrance on time.

**Healing (Holy).** Keep Oath of Light on the tank. Flash of Light is your heal that uses little mana. Keep Holy Shock for sudden large damage. Cleanse is very useful in Wailing Caverns, Razorfen Downs, Scholomance and Stratholme.

**DPS (Retribution).** Use Blessing of Might or Kings on the group. Stay behind the mob, and do not break crowd control with Consecration. When a mob attacks another player, offer to off-tank it with Judgement of Fury.

| Level | Recommended | Why for paladins |
|---|---|---|
| 13–22 | [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) (A) / [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) (H) | First new dungeons; the Ruins have many undead, which is good for Exorcism |
| 18–26 | Deadmines / Wailing Caverns | Rhahk'Zor's Hammer; Wolfsbane materials |
| 20–30 | Shadowfang Keep | Wolfsbane ingot (Forsaken); good two-hand weapons |
| 26–35 | [Excavation Site](../../content/dungeons/excavation-site.md), [City of Dalaran](../../content/dungeons/city-of-dalaran.md) | New blue items and camp blueprints |
| 30–45 | Scarlet Monastery | Ravager (Herod, Armory) is a traditional Ret two-hand weapon |
| 35–47 | [The Drowned City](../../content/dungeons/drowned-city.md), [Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md) | New blue items for middle levels |
| 48–55 | [Alcaz Prison](../../content/dungeons/alcaz-prison.md), Maraudon | — |
| 55–60 | BRD, LBRS, [Blackmaw Hold](../../content/dungeons/blackmaw-hold.md), Scholomance, Stratholme, [Shaper's Terrace](../../content/dungeons/shapers-terrace.md) | Pre-raid gear |

See [Dungeons](../../content/dungeons/index.md) for all instances.

---

## Raid preparation

Raids open on **9 December 2026**: [The Barrow Deeps](../../content/raids/barrow-deeps.md) (10), [Hyjal Summit](../../content/raids/hyjal-summit.md) (20) and [Onyxia's Lair](../../content/raids/onyxias-lair.md) (40). See [Raids](../../content/raids/index.md).

**Your raid role.** In 10- and 20-player raids, each class buff is important. Expect to give Kings, a resistance aura when necessary, and Cleanse. Without Salvation, tanks must control more of the threat.

- **Holy:** the most probable raid role. Get Intellect, healing power and mana regeneration.
- **Protection:** a good off-tank or main tank in 10- and 20-player raids. Get the Defense that is necessary to prevent crits (in Classic the target was 440 Defense; the target for Forever is not published).
- **Retribution:** gives utility and constant damage. Hit gear is important. Artisan's Precision on a Dwarf helps.

**Pre-raid gear.** Dungeon loot in Forever has new itemization, so the Classic pre-raid lists do not apply. Do the 55–60 dungeons, mostly the new ones, and choose the best item for each slot for your role. A set of resistance gear can be useful. In Classic, tanks need Fire resistance for Onyxia.

**Onyxia attunement.** You need the **Drakefire Amulet**. Start the chain early, because it is long.

**Consumables.** Mana potions (First Aid now makes healing potions), elixirs, food buffs (Gourmand makes them last longer), weapon stones or oils. Camp buffs do not stack with the equivalent class buff.

---

## PvP

- **Battlegrounds:** Warsong Gulch, Arathi Basin, Alterac Valley, and the new [Battle for the Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands) (15v15, 30–60). Paladins are very good flag carriers and node defenders because of Blessing of Freedom, Divine Shield and self-healing.
- **Retribution:** do burst damage with Seal of Command, Judgement, Holy Strike and Hammer of Justice. Repentance and Hammer of Justice give 2 controls. Blessing of Freedom removes slows.
- **Holy / Shockadin:** a healer that is difficult to kill. Voice of Truth (trained) protects your casts from interrupts for 6 s.
- **World PvP:** Forever has PvP rulesets on megaservers. Because of Divine Shield and Lay on Hands, it is difficult for enemies to gank paladins. But you cannot catch enemies that run.
- **Ranks and Honor:** see [PvP](../../content/pvp/index.md). The Legacy talent *For Great Honor* adds up to +10% Honor.

**Matchups (general Classic-era knowledge, changed for Forever).**

| Opponent | Notes |
|---|---|
| Warrior | You can survive longer than they can. Keep Blessing of Freedom for Hamstring and Hammer of Justice for their burst. |
| Rogue | Stuns are the danger. Humans have Will to Survive. Dwarfs remove poisons with Stoneform. |
| Mage / Warlock | Kiting and fears. Undead have Will of the Forsaken. All other races need Blessing of Freedom and patience. |
| Priest | Purge/dispel removes your buffs. Use Voice of Truth when they try to stop your heals. |
| Hunter | Get near them with Pursuit of Justice and Freedom. Scatter Shot blocks Will of the Forsaken. |
| Druid / Shaman | Long fights. Keep Hammer of Justice for their heal. |

---

## Gear, stats & enchants

| Spec | Stat priority (leveling → 60) |
|---|---|
| **Retribution** | Weapon DPS and a slow speed → Strength and crit → hit (to the cap at 60) → Stamina → Intellect (spell damage through Champion of the Light) |
| **Protection** | Stamina and Defense → block value and block → hit → Strength |
| **Holy** | Intellect and healing power → mana regeneration → crit → Stamina |

!!! conflict "Conflict: Retribution stat priority"
    For leveling, ConquestCapped puts Stamina, Spirit and Intellect before Strength. Its reason is that most damage comes from abilities. Leprestore puts weapon DPS, Strength and crit first. Both agree that the quality of the weapon is the most important.

- **Hit sources:** Divine Precision (Holy), Precision (Protection) and the Dwarf racial Artisan's Precision all add hit. Thus, hit gear is less important than in Classic.
- **Weapon imbues** now stack with stones and oils.
- **Enchants:** Crusader on a Retribution weapon is the Classic standard. Blizzard has not published the full enchant list for Forever.
- **Transmog:** account-wide, same armor type only. Plate appearances need plate (40+).

---

## Professions & Legacy

<p class="divider">Professions</p>

Paladins wear plate at 40, and Blacksmithing is good for all 3 specs.

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

- The standard choice for Paladins
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

- Make your own elixirs and mana potions

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Incense Candle (Intellect) · Mana Well (mana regen)</p>

</div>

</div>

<p class="legend" markdown>Codex ratings out of 5, from the sources above. Compare all classes in [Best professions by class](../../characters/professions.md#best-professions-by-class).</p>

<div class="pills" markdown>
**:material-medical-bag: First Aid · healing potions**{ .pill .pill--success } **:material-pot-steam: Cooking · campfires**{ .pill .pill--info } **:material-fish: Fishing · Fish Bowl**{ .pill .pill--info }
</div>

**Secondary skills.** Take First Aid on all characters. It now makes healing potions. Cooking and Fishing supply the camping system.

!!! tip "Race notes"
    **Dwarf, Human, Undead:** no profession racials. Choose the professions that you like.

Crafting professions give [Legacy Points](../../characters/legacy.md) at skill 150, 225 and 300, and each profession adds a [camp feature](../../systems/camping.md). In Forever, professions give no passive stats.

**Legacy talents** (up to 16 points per character):

- **Thrill of Adventure** (Adventure): gives back health and mana when you kill mobs in the open world that are not trivial. This is the best pick to level a class that often has no mana.
- **Well Rested**, then **Talented**: talent points at a lower level.
- **Reagent Economy** (Resourcefulness): class spells do not need vendor reagents (Symbol of Kings, Symbol of Divinity).
- **Permanence**: class buffs last longer.
- **For Great Honor** for PvP, **Diplomat** to get reputation.

You get paladin class Legacy Points at levels **25, 45 and 60**. See [Legacy System](../../characters/legacy.md).

---

## Hardcore notes

!!! hardcore "Hardcore survival"

    The Hardcore ruleset comes this winter. Paladins are one of the safest Hardcore classes, but you must use their survival tools carefully.

    - **Divine Protection** at 6 and **Divine Shield** at 34 are escape abilities. If a pull goes wrong, use your hearthstone while the shield is active.
    - **Lay on Hands** now has a 20-minute cooldown, so it is available for most bad fights.
    - **Templar's Bulwark** and Divine Shield share **Forbearance**. Plan to use one, not both.
    - You have no slow or interrupt. Do not fight humanoids that run away near other packs, or casters that you cannot get to.
    - Keep Blessing of Freedom ready for roots and snares.
    - Undead can remove fear with Will of the Forsaken. Humans can break stuns with Will to Survive.

---

## Common mistakes & FAQ

??? question "Does Judgement still eat my Seal?"
    No. In Forever, the Seal stays active after Judgement, so you do not need to cast it again.

??? question "Where is Blessing of Salvation?"
    Blizzard removed it before launch, together with Mass Salvation, Blessing of Light and Blessing of Sanctuary.

??? question "Can I seal-twist?"
    Not as in Classic. The Retribution final talent **Unsealed Wrath** replaces twisting. Swing with one Seal to keep copies, then change Seals.

??? question "Can I be a Shockadin with Unsealed Wrath?"
    No. Holy Shock needs 21 Holy points and Unsealed Wrath needs 31 Retribution points. This is 52 points, but you have 51.

??? question "Why does my Consecration feel weaker on big pulls?"
    It does full damage to only the first 4 targets.

??? question "My new spells aren't on my action bar."
    Forever no longer adds new spells to your bars. Open the spellbook after you train.

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
