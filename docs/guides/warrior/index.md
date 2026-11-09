---
description: "Warrior guide for WoW: Forever: specs and talents, rotations, a 1–60 leveling route, dungeons, raids, PvP, gear and Hardcore tips."
tags:
  - Warrior
search:
  boost: 2
---

# Warrior

<div class="guide-head" data-class="warrior" markdown>

:codex-warrior:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Class guide</span> **Tank**{ .badge .tank } **DPS**{ .badge .dps } <span class="gh-diff" title="Method: somewhat high entry difficulty">Leveling difficulty: <strong>Hard</strong><span class="gh-pips" data-level="3" aria-hidden="true"><i></i></span></span>

<nav class="gh-jump" aria-label="Jump to section"><a href="#specs-talents">Talents</a> <a href="#abilities-rotation">Rotation</a> <a href="#leveling-walkthrough-160">Leveling</a> <a href="#dungeons">Dungeons</a> <a href="#raid-preparation">Raids</a> <a href="#pvp">PvP</a> <a href="#gear-stats-enchants">Gear</a> <a href="#hardcore-notes">Hardcore</a></nav>

</div>

!!! info "Current as of 7 November 2026"
    This guide follows Blizzard's pre-launch notes (2–4 Nov), the launch-week hotfixes and the first community guides. Talent numbers in Forever still change. For reference data, see the [Warrior class page](../../characters/classes/warrior.md).

## Overview

The Warrior is Forever's plate-wearing melee class. It can **tank** (Protection) or do **melee damage** (Arms with a two-hander, Fury with two weapons). It uses **rage**. You get rage when you hit and when you are hit. It changes between three stances to get different abilities.

<aside class="infobox" markdown>
<p class="infobox-title">Warrior at a glance</p>

| | |
|---|---|
| **Roles** | Tank (Protection) · Melee DPS (Arms, Fury) |
| **Armor** | **Cloth**{ .pill .pill--cloth }, leather and mail from level 1. ****Plate**{ .pill .pill--plate } at 40** from the class trainer |
| **Weapons** | All types except wands. Shields. You can train polearms from level 20 |
| **Resource** | **Rage**{ .pill .pill--rage } (now normalized, see below) |
| **Races** | All ten: every race in the game can be a Warrior |

</aside>

<div class="proscons" markdown>
<div class="pros" markdown>

Strengths

- The best-supported tank class, with a much larger Defensive Stance threat bonus (+80%) in Forever.
- Very high damage when you have good gear, with strong cleave from Sweeping Strikes and Whirlwind.
- Because of rage normalization, **gear no longer decreases your rage**: armor and absorbs do not decrease the rage that you get when you are hit.
- Victory Rush and Tactical Mastery are baseline, so early leveling is easier than in Classic.

</div>
<div class="cons" markdown>

Weaknesses

- In the beta, players reported it as one of the **two slowest leveling classes** (with Priest). Kill speed depends almost fully on your weapon.
- Little self-healing and almost no crowd control. You need a healer to tank difficult content.
- Needs much gear. A Warrior with a bad weapon is much weaker than any other class with a bad weapon.

</div>
</div>

### What's new in Forever

- **Rage normalization.** The game calculates rage from damage taken as if your armor is always 50%. Absorbs (Power Word: Shield and similar) no longer decrease it. Rage from damage done now depends on **weapon speed**, so slow weapons give more rage per swing. **Crits give +75% rage.**
- **Baseline changes.** Tactical Mastery (level 14) keeps 10 rage when you change stance. Victory Rush (level 20) has a 30 s cooldown and heals 10%. Recklessness, Retaliation and Shield Wall no longer share a cooldown. Retaliation and Shield Wall have a 15-minute cooldown. Rend and Thunder Clap scale with attack power. Thunder Clap works in Defensive Stance with a 6 s cooldown. Improved Battle Shout is now part of the base ability. Sunder Armor and a Rogue's Expose Armor can now be on a target at the same time.
- **Pre-launch tuning.** Defensive Stance threat is **+80%** (was 30%), and Slam has a **15 s cooldown**. A 4 Nov hotfix changed Defensive Stance and Defiance threat again.
- **New talents.** Spearing Strike, Bloodthrill and Weaponmaster (Arms), Raging Blows, Boundless Rage, Reckless Swings and Improved Whirlwind (Fury), and Vanguard, Bastion and Focused Rage (Protection).
- **Removed talents.** The weapon specializations (merged into Weaponmaster), Improved Battle Shout, Improved Demoralizing Shout, Improved Shield Block and Improved Taunt (now baseline), and One-Handed Weapon Specialization.

### Race add-ons

All races can be Warriors. Choose a race, then read its add-on together with this guide.

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| [Human](human.md): Will to Survive, +1% crit | [Orc](orc.md): Blood Fury, stun reduction |
| [Dwarf](dwarf.md): Stoneform, +1% hit | [Troll](troll.md): Berserking, out-of-combat regen |
| [Gnome](gnome.md): Escape Artist, Eureka! | [Tauren](tauren.md): War Stomp, +5% health, top Strength |
| [Night Elf](night-elf.md): Elune's Light, Shadowmeld | [Undead](undead.md): Will of the Forsaken, Touch of the Grave |
| [Skyborne (High Order)](skyborne-high-order.md): **NEW** | [Skyborne (Windshaper)](skyborne-windshaper.md): **NEW** |

Skyborne Warriors are the only new Warrior combinations in Forever. You must have the Skyborne Heroic Pack or a higher edition to play them. See [Skyborne](../../characters/races.md#skyborne).

---

## Specs & talents

Forever's Warrior trees keep the Classic shape, but many talents are different. The new **16-point tier** gives each tree a signature talent (Spearing Strike, Raging Blows, Vanguard). Exact point costs and positions still change from build to build. Thus the builds below give **priorities and milestones**, not a full list of points. Before you spend your points, compare the builds with a current talent calculator.

!!! tip "Talent points earlier with Legacy"
    The Legacy talent **Talented** (requires 5/5 **Well Rested**) moves your first talent point 1 level earlier per rank, down to level 5. This costs 10 Legacy Points, so it is an extra for a second character. See [Legacy](../../characters/legacy.md).

=== "Arms"

    **Two-handed weapons, Overpower, Mortal Strike.** The traditional leveling and PvP spec.

    | Talent | What it does in Forever |
    |---|---|
    | Improved Rend | Rend now scales with attack power, so this talent has more value than in Classic |
    | Improved Tactical Mastery | Keeps 5/10/15 rage when you change stance, in addition to the baseline 10 |
    | Improved Overpower | More Overpower crits, so more rage |
    | **Spearing Strike** (16) | 15 rage, 20 s cooldown. Dismounts the target. Does double damage to mounted targets, dragons and giants |
    | **Bloodthrill** | 10/20% (two ranks pre-launch). The Tavern build uses it, not Weaponmaster, for more Overpower uses |
    | **Weaponmaster** | Replaces the weapon specializations: crit for axes and polearms, armor penetration for maces and staves, extra attacks for swords |
    | Improved Slam | Slam no longer resets your swing timer |
    | Iron Will | Moved here from Protection |
    | Sweeping Strikes · Mortal Strike | Still the cleave tool and the capstone |

=== "Fury"

    **Dual-wield, Bloodthirst, Flurry.** The raid damage spec.

    | Talent | What it does in Forever |
    |---|---|
    | Unbridled Rage · Blood Craze | Rage and sustain while you take hits |
    | Improved Cleave · Precision | Cleave damage and hit chance |
    | **Boundless Rage** | New rage talent. The details can still change |
    | Dual Wield Specialization | Off-hand damage. Leads to Death Wish |
    | **Raging Blows** (16) | The new Fury signature talent |
    | Enrage | Redesigned. Almost permanent uptime when you level, according to Method |
    | Death Wish | Now also increases damage taken |
    | Flurry | 10/20/30% attack speed, **no longer requires Death Wish** |
    | **Bloodthirst** | No longer heals. It gives +10% movement speed for 10 s |
    | **Reckless Swings** | Added 3 Nov (see conflict below) |
    | **Improved Whirlwind** | Added 3 Nov: shorter Whirlwind cooldown and more damage to the closest target (*single source*) |

    !!! conflict "Conflict: Reckless Swings"
        The wiki's research notes describe a pre-launch version that **costs 25% of base health** and adds **+5 rage to your next 4 swings**. RankedBoost's talent list says that it **heals 0.5% of max health** on your next 3 melee hits after Enrage, Berserker Rage, Bloodrage, Death Wish or Bloodthirst. Both descriptions are possibly correct for different builds. Read the tooltip in game.

=== "Protection"

    **Shield, threat, mitigation.** In Forever, it is also an unexpectedly good spec for solo leveling.

    | Talent | What it does in Forever |
    |---|---|
    | Shield Specialization | **5 rage per block**. The first talent: it gives you enough rage and leads to Master of Defense |
    | Anticipation · Master of Defense | Defense and avoidance |
    | Improved Revenge | Now adds **damage** instead of a stun |
    | Defiance | Threat, 7/13/20%. **Requires a shield** |
    | Improved Disarm · Improved Shield Wall | As in Classic |
    | **Vanguard** (16) | **Charge in Defensive Stance**. You do not have to stance-dance to start a pull |
    | **Bastion** · **Focused Rage** | New. Method recommends both for leveling speed |
    | Shield Slam | Now scales with **block value** |

### Recommended builds

=== "Leveling: Protection (solo)"

    Method recommends this build for solo play. Icy Veins' leveling guide reportedly calls it the fastest Warrior leveling spec, but it starts slowly before the 16-point tier.

    <div class="steps" markdown>

    1. **Shield Specialization** first, for rage.
    2. **Improved Thunder Clap** and **Improved Bloodrage** for pulls of 2–3 mobs.
    3. Around level 20: **Master of Defense** and **Improved Revenge** (Revenge is now a damage button).
    4. **Vanguard** at the 16-point tier. From this point, stay in Defensive Stance: Charge, Thunder Clap, Revenge, and later Shield Slam.
    5. Then **Bastion** and **Focused Rage**, then Anticipation, Last Stand and Concussion Blow.

    </div>

    Warcraft Tavern's version is similar, but it takes Anticipation and Defiance earlier. Both builds agree on Shield Specialization → Master of Defense → Vanguard.

=== "Leveling: Arms (group)"

    The classic two-hander route. It is best with a healer or in dungeons.

    <div class="steps" markdown>

    1. **Improved Rend** (with AP scaling, it now does good damage), then **Improved Heroic Strike** or **Deep Wounds**.
    2. **Improved Overpower**. Overpower is your main ability for most of the leveling.
    3. Get **Sweeping Strikes** as soon as possible. Mobalytics calls it the most important leveling talent.
    4. **Bloodthrill** (or Weaponmaster if it gives your weapon type a large benefit).
    5. Do not take **Spearing Strike** unless you fight giants, dragons or mounted players. Warcraft Tavern recommends max Two-Handed Weapon Specialization instead.
    6. **Improved Slam**, then **Mortal Strike**.
    7. Method then puts points into Fury for **Unbridled Wrath** and **Enrage**.

    </div>

    !!! conflict "Conflict"
        Warcraft Tavern's Arms build stays in the Arms tree (listed as 26/0/0). Method's build is a hybrid that puts some points into Fury. Both builds are good. The hybrid is better for longer fights.

=== "Leveling: Fury"

    This build works, but at low levels, missed auto attacks give you too little rage. It is better after level 40 with a good pair of weapons.

    <div class="steps" markdown>

    1. **Cruelty**, then **Unbridled Wrath**, then **Precision** (hit).
    2. **Blood Craze** for sustain.
    3. **Dual Wield Specialization**, then **Death Wish**.
    4. **Enrage** and **Flurry** (Flurry no longer needs Death Wish).
    5. **Bloodthirst** for damage and the movement speed buff.

    </div>

=== "Endgame"

    The community does not agree yet: raids open **9 Dec** and nobody has logs at level 60. General direction:

    | Role | Build direction |
    |---|---|
    | **Raid DPS** | Deep Fury: Bloodthirst, Flurry, Raging Blows, Improved Whirlwind, Precision. A two-hander Arms build is probably competitive in the 10- and 20-player raids, which possibly do not have many buffs |
    | **Main tank** | Deep Protection: Defiance, Vanguard, Bastion, Focused Rage, Shield Slam. Threat is now so high that you possibly do not need Fury points |
    | **Off-tank / dungeon** | Protection with a few Fury points for Cruelty if the build allows it |
    | **PvP** | Arms: Mortal Strike, Spearing Strike (dismount!), Improved Slam, Weaponmaster |

    *General guidance. Nobody has published endgame point splits.*

### Dual spec

**Dual specialization** unlocks at **level 40** for **50g** at your class trainer. For a Warrior, we recommend it: keep a **Protection** spec for dungeons and a **damage** spec (Arms for questing and PvP, Fury for raids). Respec fees decrease to 1g over time. See [Dual specialization](../../characters/leveling.md#dual-specialization).

---

## Abilities & rotation

### Key abilities by level

From Method's leveling guide. Victory Rush and Tactical Mastery are Forever baseline.

| Level | Ability | Notes |
|---|---|---|
| 1 | Battle Shout, Heroic Strike | Battle Stance |
| 4 | Charge, Rend | Rend scales with AP now |
| 8 | Hamstring | |
| 10 | **Defensive Stance**, Sunder Armor, Taunt | From the level-10 class quest |
| 12 | Overpower | |
| 14 | Revenge, Demoralizing Shout, **Tactical Mastery** | Tactical Mastery is now baseline |
| 20 | **Victory Rush**, Retaliation | Victory Rush: 30 s cooldown, heals 10% |
| 30 | **Berserker Stance** | From the level-30 class quest |
| 36 | Whirlwind | |
| 40 | **Plate** | |

### Rotations

=== "Protection"

    !!! rotation "Protection: Single target"

        <div class="priority" markdown>

        1. Shield Slam (if talented)
        2. Revenge when it is available
        3. Sunder Armor
        4. Heroic Strike to spend rage when you have more than ~50 rage.

        </div>

    **Multi-target:** start with **Thunder Clap** (usable in Defensive Stance, 6 s cooldown, now scales with AP), then Demoralizing Shout, then tab-Sunder and Cleave.

    **Opening:** with **Vanguard**, you can Charge in Defensive Stance. Without Vanguard, Charge in Battle Stance, then change stance (Tactical Mastery keeps 10 rage), then use Thunder Clap.

=== "Arms"

    !!! rotation "Arms: Leveling"

        <div class="priority" markdown>

        1. Charge
        2. Rend
        3. Auto-attack
        4. **Overpower** each time it is available
        5. Mortal Strike on cooldown
        6. Slam (15 s cooldown now)
        7. Heroic Strike only with extra rage.

        </div>

        Keep Demoralizing Shout active on packs. On 2 targets, use **Sweeping Strikes**, then Whirlwind or Cleave.

    **Pool rage:** do not spend your last rage on a mob that is almost dead. Keep it for the next pull. Finish low mobs with **Victory Rush** for the heal.

=== "Fury"

    !!! rotation "Fury priority"

        <div class="priority" markdown>

        1. Bloodthirst on cooldown
        2. Whirlwind on cooldown
        3. Heroic Strike (or Cleave on 2+ targets) above ~50 rage
        4. Execute below 20% health.

        </div>

        Stay in **Berserker Stance**. Use Bloodrage and Berserker Rage on cooldown for rage.

    **Cooldowns:** Death Wish and Recklessness together in raids. Death Wish now increases damage taken, so monitor your health.

### Cooldowns

Recklessness, Retaliation and Shield Wall **no longer share a cooldown** in Forever. Retaliation and Shield Wall now have 15-minute cooldowns. Thus you can use one and keep the others available.

### Useful macros

??? example "Show 3 macros"

    ```text
    #showtooltip Charge
    /cast [stance:1] Charge; [stance:3] Intercept; Battle Stance
    ```

    ```text
    #showtooltip Overpower
    /cast [stance:1] Overpower; Battle Stance
    ```

    ```text
    #showtooltip Victory Rush
    /cast Victory Rush
    /startattack
    ```

    !!! tip "Keybinds"
        Put Revenge, Overpower and Victory Rush on easy keys. They are reactive, and you will press them frequently. With Vanguard, most Protection Warriors do not need their stance-swap Charge macro.

---

## Leveling walkthrough 1–60

!!! warning "Slow start, fast finish"
    In the beta, Warriors were among the slowest classes to level. Solo, a normal mob takes about 10–15 s to kill. Get all the weapon upgrades that you can from quests or the Auction House. Method estimates that almost all of your leveling damage comes from your weapon. Make a group for elites and dungeon quests, because they give much more XP in Forever.

The zone suggestions below follow the Classic-era leveling order and add the new zones. Forever does not show zone level ranges in game. See [Zones](../../world/zones.md).

<div class="route" markdown>

### 1–10: Starting zone

| | **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|---|
| **Zones** | Elwynn Forest · Dun Morogh · Teldrassil · [Zephras Isle](../../world/zephras-isle.md) | Durotar · Mulgore · Tirisfal Glades · Zephras Isle |
| **Train** | Battle Shout, Charge and Rend (4), Hamstring (8) | Same |
| **Talents** | None until 10 (earlier with Talented) | Same |

- Do all quests. Take all weapon rewards. When a better weapon drops, **sell your starting weapon** immediately.
- Learn **Cooking** and do **The Great Outdoors** (around level 5) to unlock [camping](../../systems/camping.md). The campfire rested bonus helps a slow class.
- Get a gathering profession from the starter quest (+2 skill). Mining is good for Warriors (see [Professions](#professions-legacy)).
- At **10**, take the **Defensive Stance** quest from your class trainer. It gives Defensive Stance, Sunder Armor and Taunt. The next quest in the chain gives a one-hander.

### 10–20

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Westfall, Loch Modan, Darkshore, Redridge (from ~15) | The Barrens, Silverpine Forest, Stonetalon Mountains (from ~15) |

- **Talents start.** Protection: Shield Specialization first. Arms: Improved Rend.
- At **14**, Tactical Mastery is baseline: now a stance change for Overpower costs little rage.
- Dungeons: **Ragefire Chasm** (13–18), **[Hall of Thanes](../../content/dungeons/hall-of-thanes.md)** (13–18, Ironforge), **[Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md)** (15–22, Tirisfal), **Deadmines** and **Wailing Caverns** (late teens). Bosses in new dungeons reportedly always drop a blue item.
- Supply camps open: **Three Corners** in Redridge (Alliance) and west of the **Crossroads** (Horde).
- From 14, do the **Cozy Sleeping Bag** scavenger hunt. Its XP buff is worth the time.

### 20–30

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Duskwood, Wetlands, Ashenvale, Hillsbrad Foothills | Hillsbrad Foothills, Ashenvale, Thousand Needles, Stonetalon |

- **Victory Rush** at 20 makes leveling much easier. Use it to kill each mob.
- **Polearms** become trainable at 20.
- **Library books:** at **20**, a turn-in of **10 books** unlocks a Warrior quest. The later tiers unlock at 35 and 45. Forever has not documented the Warrior rewards yet. Pick up class books when they drop.
- At about this level, Arms gets to the 16-point tier. Protection players get **Vanguard**.
- Dungeons: **Shadowfang Keep**, **Blackfathom Deeps**, **The Stockade**, **[Excavation Site: Wetlands](../../content/dungeons/excavation-site.md)** (24–29), **[City of Dalaran](../../content/dungeons/city-of-dalaran.md)** (28–33, hostile to the Horde).
- **25:** first Warrior class milestone for a **Legacy Point** (Novice).
- At **30**, take the **Berserker Stance** quest (the trainer sends you to Fray Island near Ratchet. This is a Classic-era quest, *check in game*). Also start the **Whirlwind Axe** chain in Alterac Mountains. Method warns that it is hard at 30. Bring a friend or buy the reagents on the Auction House.

### 30–40

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Arathi Highlands, Stranglethorn Vale, Desolace, Alterac Mountains | Arathi Highlands, Stranglethorn Vale, Desolace, Thousand Needles |

- **Whirlwind** at 36.
- **[Riverglades](../../world/zones.md#riverglades)** opens at about **35** (contested, 150+ quests). Alliance base: **Farholde Keep**. Horde base: **Rog'mar**. You can go there from Redridge, Badlands, Swamp of Sorrows, Burning Steppes, or with the Tanaris ferry.
- Desolace centaur quests now need level 35.
- Dungeons: **Razorfen Kraul**, **Gnomeregan**, **Scarlet Monastery** (all four wings), **[The Drowned City](../../content/dungeons/drowned-city.md)** (35–40).
- **35:** second library-book tier (20 books). Artisan professions open.
- At **40**: **plate**, **Apprentice Riding** (100g, including your first mount) and **dual spec** (50g). Keep about 150g for this.

### 40–50

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Riverglades, Dustwallow Marsh, Badlands, Swamp of Sorrows, Tanaris, Feralas, Hinterlands | Riverglades, Dustwallow Marsh, Badlands, Swamp of Sorrows, Tanaris, Feralas, Hinterlands |

- Replace leather and mail with plate gradually. Do not give up a big weapon upgrade for armor.
- **45:** final library-book tier (25 books) and the second Warrior Legacy Point (Experienced).
- Dungeons: **Razorfen Downs**, **[Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md)** (40–45, Riverglades), **Uldaman**, **Zul'Farrak**, **[Alcaz Prison](../../content/dungeons/alcaz-prison.md)** (48–53, Dustwallow), **Maraudon**.
- The Darkspear Islands battleground opens from level 30, in brackets of 10. It is a good change from questing.

### 50–60

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Azshara, Un'Goro Crater, Felwood, Searing Gorge, Burning Steppes, Western/Eastern Plaguelands, Winterspring, Silithus | Same |

- **Azshara** has many new quests and **[Blackmaw Hold](../../content/dungeons/blackmaw-hold.md)** (55–60). The north of Un'Goro has **[Shaper's Terrace](../../content/dungeons/shapers-terrace.md)** (58–60).
- Run **Sunken Temple**, **Blackrock Depths** and **Lower Blackrock Spire** for pre-raid gear when you level.
- At **60**: third Warrior Legacy Point (Master). Go to **[Mount Hyjal](../../world/zones.md#mount-hyjal)** through Darkwhisper Gorge in Winterspring. Epic riding is 1,000g.

</div>

---

## Dungeons

**As tank:** with +80% Defensive Stance threat, it is easy to hold single targets. For packs, you still need Thunder Clap, Demoralizing Shout and tab-Sunder. There are no Meeting Stone summons, so you must walk to each entrance. Vanguard makes chain pulls fast.

**As DPS:** let the tank get threat for 2 or 3 seconds. Death Wish increases damage taken. Do not use it on trash pulls that you are not sure about.

**Notable dungeons for Warriors**

| Level | Dungeon | Why |
|---|---|---|
| 13–20 | [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) · Ragefire Chasm | First chance at a blue weapon |
| 15–22 | [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) | 6 bosses, a good early Horde run |
| 18–24 | The Deadmines | Classic weapon drops |
| 24–33 | [Excavation Site](../../content/dungeons/excavation-site.md) · [City of Dalaran](../../content/dungeons/city-of-dalaran.md) | New loot themed to class and spec |
| 34–45 | Scarlet Monastery (Armory, Cathedral) · [The Drowned City](../../content/dungeons/drowned-city.md) | Arms two-hander upgrades. Practice for prot |
| 40–55 | [Krol'dok](../../content/dungeons/kroldok-stronghold.md) · Zul'Farrak · [Alcaz Prison](../../content/dungeons/alcaz-prison.md) | Plate and weapon upgrades when you start to wear plate |
| 55–60 | BRD · LBRS/UBRS · [Blackmaw Hold](../../content/dungeons/blackmaw-hold.md) · [Shaper's Terrace](../../content/dungeons/shapers-terrace.md) · Scholomance · Stratholme · Dire Maul | Pre-raid gear |

See the full [dungeon list](../../content/dungeons/index.md).

---

## Raid preparation

All 3 launch raids open on **9 December 2026**. There is no difficulty mode, so preparation (gear, consumables, strategy) is the most important thing. See [Raids](../../content/raids/index.md).

| Raid | Size | Warrior role |
|---|---|---|
| [The Barrow Deeps](../../content/raids/barrow-deeps.md) | 10 | Probably 1 tank Warrior and 1–2 DPS. In small raids, an off-tank who can DPS is valuable |
| [Hyjal Summit](../../content/raids/hyjal-summit.md) | 20 | 2 or 3 tanks. Fury and Arms DPS. Split routes possibly need 2 tank teams |
| [Onyxia's Lair](../../content/raids/onyxias-lair.md) | 40 | The main tank holds Onyxia. Fire resistance helps. Needs the **Drakefire Amulet** attunement through UBRS |

**Pre-raid gear approach:** Forever's loot is not fully documented, and dungeon items have stats themed to spec. Thus nobody has a reliable pre-raid best-in-slot list yet. In general:

- **Tanks:** get Stamina, Defense and armor first, then avoidance and block value (Shield Slam scales with it). Hit helps threat.
- **DPS:** get to the hit cap with crit and Strength. Your **weapon** is still your biggest upgrade.
- Farm reputation and Honor for items that fill gaps. PvP blues can be good early raid gear.

**Consumables to stock:** health potions (now made by **First Aid**), Elixirs of the Mongoose/Giants or their Forever equivalents, weapon stones from Blacksmithing, Rage potions, and food buffs (the Legacy talent *Gourmand* makes them last longer). In Forever, world buffs from the Chronoboon Displacer **do not work in raids**.

---

## PvP

Arms is the PvP spec: **Mortal Strike** for healing reduction, **Hamstring** to stay near the target, **Spearing Strike** to dismount riders (double damage to mounted targets), and **Improved Slam**, which no longer resets your swing.

- **Battlegrounds:** Warsong Gulch, Arathi Basin, Alterac Valley and the new **[Battle for the Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands)** (15v15, levels 30–60). In Darkspear, Warriors are good flag carriers and base defenders. Spearing Strike does high damage to all players that ride between bases.
- **World PvP:** on PvP realms, you are almost always at risk. Victory Rush heals after each kill. Charge/Intercept win fights against careless casters.
- **Progression:** a seasonal Rank 1–14 system with Honor gear. See [PvP](../../content/pvp/index.md).

**Matchups (general Classic-era guidance)**

| Opponent | Notes |
|---|---|
| Mage | Hardest matchup. Keep Intercept/Charge for after Blink. Use a trinket or racial to break Polymorph or Frost Nova |
| Rogue | Win with Mortal Strike and Hamstring. Retaliation and the racial stop their burst |
| Hunter | Close the gap fast. Intercept after Concussive Shot. Line-of-sight their pet |
| Priest / Shaman / Druid | Mortal Strike their heals. Stay near them through fear and roots |
| Paladin | Long fights. Keep your burst for when Divine Shield is on cooldown |
| Warrior | The Warrior that hits with Mortal Strike and Hamstring first usually wins |

---

## Gear, stats & enchants

| Spec | Stat priority (general) |
|---|---|
| **Protection** | Stamina = Defense > armor > Dodge/Parry/Block > Block value (for Shield Slam) > Hit (threat) > Strength |
| **Arms** | Weapon damage and speed > Hit (to cap) > Crit > Strength > Agility |
| **Fury** | Hit (dual-wield) > Crit > Strength > Agility. Fast off-hand, good main hand |

*No source has published stat priorities for Forever yet. These priorities follow Classic logic, with changes for Forever.*

**Forever changes that affect gear:**

- **Crits give +75% rage**, so crit is worth more than in Classic for every spec.
- Rage from dealing damage depends on **weapon speed**, so slow two-handers are still the best Arms choice.
- **Weaponmaster** decides your Arms weapon type: axes and polearms (crit), maces and staves (armor penetration), swords (extra attacks).
- Armor no longer decreases the rage that you get when you are hit. Thus tanks do not lose rage when their gear improves.
- Dungeon items get random themed stats. When you loot an item, you unlock its transmog.

**Enchants:** Crusader on weapons (or the Forever equivalent) for DPS. Stamina, Agility and Defense for tanks. Blacksmithing weapon stones are a cheap flat damage increase when you level.

---

## Professions & Legacy

<p class="divider">Professions</p>

Warriors depend on gear more than all other classes. Thus a crafting pair that makes weapons and plate is a good choice.

<div class="prof-picks" markdown>

<div class="prof-pick prof-pick--best" markdown>

<p class="prof-rank" markdown>**S**{ .tier .tier-s } Best pick</p>

<p class="prof-pair" markdown>:material-pickaxe: Mining <span class="prof-plus">+</span> :material-anvil: Blacksmithing</p>

<p class="prof-for">Best for: Tanks and Fury</p>

<div class="pills" markdown>
**Leveling**{ .pill .pill--success .pill--sm } **Raids**{ .pill .pill--info .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
</dl>

- The classic Warrior pair: weapon stones, plate and many new BoP patterns
- Both camp features add melee power

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Lodestone (melee AP) · Sharpening Wheel (Strength)</p>

</div>

<div class="prof-pick prof-pick--alt" markdown>

<p class="prof-rank" markdown>**A**{ .tier .tier-a } Strong alternative</p>

<p class="prof-pair" markdown>:material-pickaxe: Mining <span class="prof-plus">+</span> :material-cog: Engineering</p>

<p class="prof-for">Best for: PvP</p>

<div class="pills" markdown>
**Raids**{ .pill .pill--info .pill--sm } **PvP**{ .pill .pill--danger .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:40%"><span>2/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:100%"><span>5/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:40%"><span>2/5</span></span></dd>
</dl>

- Bombs and gadgets. Warcraft Tavern gives Engineering a high rating
- Gnomes have 20% fewer device failures

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Lodestone (melee AP) · Reagent Bot</p>

</div>

<div class="prof-pick prof-pick--sit" markdown>

<p class="prof-rank" markdown>**B**{ .tier .tier-b } Situational</p>

<p class="prof-pair" markdown>:material-knife: Skinning <span class="prof-plus">+</span> :material-pickaxe: Mining</p>

<p class="prof-for">Best for: Mount money</p>

<div class="pills" markdown>
**Leveling**{ .pill .pill--success .pill--sm } **Gold**{ .pill .pill--gold .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:20%"><span>1/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:20%"><span>1/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:100%"><span>5/5</span></span></dd>
</dl>

- Pays for your mount at 40. After that, replace one with a crafting skill

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Camp Chair (+2% crit) · Lodestone (melee AP)</p>

</div>

</div>

<p class="legend" markdown>Codex ratings out of 5, based on the sources above. Compare every class in [Best professions by class](../../characters/professions.md#best-professions-by-class).</p>

<div class="pills" markdown>
**:material-medical-bag: First Aid · healing potions**{ .pill .pill--success } **:material-pot-steam: Cooking · campfires**{ .pill .pill--info } **:material-fish: Fishing · Fish Bowl**{ .pill .pill--info }
</div>

**Secondary skills.** First Aid is mandatory: it now makes health potions and bandages. Cooking and Fishing give materials for camping.

!!! tip "Race notes"
    **Gnome:** best Engineering race. **Tauren:** *Cultivation* helps only if you take Herbalism.

Crafting professions award [Legacy Points](../../characters/legacy.md) at skill 150, 225 and 300, and each profession adds a [camp feature](../../systems/camping.md). Professions give no passive stats in Forever.

**Legacy talents** (16 points per character at launch)

| Pick | Why |
|---|---|
| **Well Rested** (5) → **Talented** (5) | Warriors level slowly. Rested XP and earlier talents help most |
| **Thrill of Adventure** | Restores health on kills in the open world. Less downtime |
| **Field Medicine** | Bandage more often |
| **Reinforce** | Tanks and Hardcore players die and repair more |
| **For Great Honor** | If you plan to PvP |

See [Legacy](../../characters/legacy.md).

---

## Hardcore notes

!!! hardcore "Hardcore survival"

    The Hardcore ruleset comes in winter. Warrior is a difficult Hardcore class because you cannot heal or escape well. Tips:

    - **Level as Protection** with a shield. You lose some kill speed, but you get much more safety.
    - Do not pull more mobs than you can kill with Thunder Clap. Keep **Retaliation** and **Shield Wall** for emergencies (they do not share a cooldown now).
    - Carry bandages and potions (First Aid makes both), and use Victory Rush to restore health.
    - Choose a race with an escape or survival racial: Will to Survive (Human), Stoneform (Dwarf), Escape Artist (Gnome), Shadowmeld (Night Elf), War Stomp (Tauren), Will of the Forsaken (Undead).
    - Legacy points that you earn on Hardcore apply to other rulesets. Legacy points from other rulesets do not apply to Hardcore.

    See [Hardcore](../../about/hardcore.md).

---

## Common mistakes & FAQ

??? question "Why do I run out of rage?"
    At low levels, the cause is usually your weapon. Rage from hits now depends on weapon speed, so slow weapons with high damage give more rage. Use Bloodrage. Take Shield Specialization (Prot) or Improved Overpower (Arms). Do not spend rage on mobs that are almost dead.

??? question "Is Protection really good for leveling?"
    In Forever, yes. Vanguard lets you Charge in Defensive Stance, Thunder Clap works in Defensive Stance, Revenge does damage, and Shield Specialization gives rage. Many guides recommend it for solo play.

??? question "Do I still need to stance-dance?"
    Less than before. Tactical Mastery is baseline (it keeps 10 rage), and Improved Tactical Mastery adds up to 15 more. Arms still changes stance for Overpower. Protection with Vanguard almost never changes stance.

??? question "Should I pick Bloodthrill or Weaponmaster?"
    Sources do not agree. Warcraft Tavern takes Bloodthrill for more Overpower. Method takes both. If your weapon type gains a lot from Weaponmaster (for example, an axe or polearm for crit), take it.

??? question "Is Skyborne a good Warrior race?"
    It is good for leveling (haste, a glide, and a speed or regen cooldown). But Warcraft Tavern rates it weak for Warriors compared with Orc, Human, Troll or Tauren. Choose it for the look and the story.

**Common mistakes**

- You keep your quest-reward weapon for too long. Look at the Auction House at each level.
- You use Heroic Strike when you do not have extra rage.
- You do not learn First Aid, but it now makes health potions.
- You forget the level 10 and 30 stance quests.
- You tank without Defiance and a shield (Defiance requires a shield).

---

## Sources

??? quote "9 sources"

    - Wiki research notes (`.research/characters.md`) and the [Warrior class page](../../characters/classes/warrior.md)
    - [Method — WoW Forever Warrior leveling guide and talents](https://www.method.gg/wow-forever/wow-forever-warrior-leveling-guide-and-talents)
    - [Warcraft Tavern — Warrior guide](https://www.warcrafttavern.com/forever/guides/warrior/)
    - [Warcraft Tavern — Pre-launch class changes](https://www.warcrafttavern.com/forever/news/wow-forever-pre-launch-class-changes-bug-fixes/)
    - [Warcraft Tavern — Priest & Warrior deep dive](https://www.warcrafttavern.com/forever/news/rage-will-benefit-from-crit-priest-warrior-deep-dive-for-wow-forever/)
    - [Icy Veins — Protection Warrior leveling](https://www.icy-veins.com/wow-forever/protection-warrior-leveling) (search summary only)
    - [Mobalytics — Arms Warrior leveling](https://mobalytics.gg/wow-forever/profile/kargoz/classes/1-60-arms-warrior-leveling-guide-talents-rotation-weapons-tips) (search summary only)
    - [RankedBoost — Forever new talents](https://rankedboost.com/world-of-warcraft/forever/whats-new/talents/) (search summary only)
    - [Destructoid — Beta patch notes, 3 Nov 2026](https://www.destructoid.com/wow-forever-beta-patch-notes-nov-3-2026/) (search summary only)
