---
description: "Hunter guide for WoW: Forever: specs and talents, rotations, a 1–60 leveling route, dungeons, raids, PvP, gear and Hardcore tips."
tags:
  - Hunter
search:
  boost: 2
---

# Hunter Guide

<div class="guide-head" data-class="hunter" markdown>

:codex-hunter:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Class guide</span> **DPS**{ .badge .dps } <span class="gh-diff" title="Guide infobox; Method: one of the easiest classes to level">Leveling difficulty: <strong>Easy</strong><span class="gh-pips" data-level="1" aria-hidden="true"><i></i></span></span>

<nav class="gh-jump" aria-label="Jump to section"><a href="#specs-talents">Talents</a> <a href="#abilities-rotation">Rotation</a> <a href="#leveling-walkthrough-160">Leveling</a> <a href="#dungeons">Dungeons</a> <a href="#raid-preparation">Raids</a> <a href="#pvp">PvP</a> <a href="#gear-stats-enchants">Gear</a> <a href="#hardcore-notes">Hardcore</a></nav>

</div>

!!! info "Current as of 7 November 2026"
    Forever started on 4 November. The public beta had a level cap of 30. Thus **almost every talent build above level 30 is theory**, not tested play. A class-tuning patch for **Tuesday 10 November** will make Hunter pets more durable (Classic Era parity). Examine the numbers again after the patch. The reference data is on the [Hunter class page](../../characters/classes/hunter.md).

## Overview

The Hunter is a ranged physical damage dealer who fights together with a tamed beast. Forever keeps that core and adds 3 real choices. **Beast Mastery** focuses on the pet. **Marksmanship** can play with no pet. **Survival** now uses melee, traps and bleeds.

<aside class="infobox" markdown>
<p class="infobox-title">Hunter at a glance</p>

| | |
|---|---|
| **Roles** | Damage (ranged or melee). Pets can off-tank solo content |
| **Armor** | **Cloth**{ .pill .pill--cloth } and **Leather**{ .pill .pill--leather } from level 1, **Mail at 40** |
| **Resource** | **Mana**{ .pill .pill--mana } (pets use Focus) |
| **Leveling speed** | **Fastest class in the beta**, ahead of Warlock and Mage |
| **Difficulty** | Easy to level, more difficult to master (pet control, the 8-yard deadzone, mana) |

</aside>

<div class="proscons" markdown>
<div class="pros" markdown>

Strengths

- Kills fast and safely: the pet tanks while you shoot.
- Very good kiting tools: Concussive Shot, Wing Clip, Frost Trap, and now **traps in combat**.
- Feign Death and Freezing Trap give you emergency escapes that few classes have.
- Pets scale with **your** gear. Thus a pet that you tame at 30 does not become too weak later.

</div>
<div class="cons" markdown>

Weaknesses

- The **deadzone**: you cannot shoot targets nearer than 8 yards. You are weak in melee if you are not Survival.
- In long fights, you can use all your mana before you get talents such as Rapid Recuperation.
- Pets die in AoE until the 10 November durability fix.
- Ammunition, pet food and stable fees use bag space and cost gold (Classic-era behavior, not changed as far as we know).

</div>
</div>

### What's new in Forever

- **Aimed Shot is baseline at 20** for every spec. Multi-Shot shares its cooldown. Arcane Shot has its own cooldown.
- **Traps work in combat.** All traps share one **30 s** cooldown.
- Aspect of the Beast now adds melee AP.
- Scorpid Sting decreases the hit chance of the target by 2% (it does not stack with Insect Swarm).
- Disengage now removes more threat.
- Pre-launch buffs: Aimed Shot +110% bonus damage, Arcane Shot +30% base damage, Serpent Sting buffed, Aspect of the Hawk ranks 20/35/50/70/90/110 RAP. Hunter's Mark ranks do not stack now.
- **Pets** scale with the gear of the Hunter (10% of your Attack Power and 100% of your crit chance, per Warcraft Tavern). Pets do not get player buffs now. Every family learns Bite or Claw, and Dive or Dash, and has **1 unique ability**. **Fox** is a new family.
- **Removed:** Wyvern Sting, Killer Instinct, Improved Feign Death, Monster/Humanoid Slaying, Improved Hunter's Mark.
- **Human Hunter** is a new combination, and **both Skyborne factions** can be Hunters.

### Races

| Race | Faction | Status | Headline racial for Hunters | Add-on |
|---|---|---|---|---|
| Human | **Alliance**{ .pill .pill--alliance } | **New**{ .pill .pill--new .pill--sm } | Ruthless (+1% crit), Will to Survive (stun break) | [Human Hunter](human.md) |
| Dwarf | **Alliance**{ .pill .pill--alliance } | Classic | Artisan's Precision (+1% hit), Stoneform | [Dwarf Hunter](dwarf.md) |
| Night Elf | **Alliance**{ .pill .pill--alliance } | Classic | Elune's Light (+10% crit for 15 s), Shadowmeld | [Night Elf Hunter](night-elf.md) |
| Skyborne (High Order) | **Alliance**{ .pill .pill--alliance } | **New**{ .pill .pill--new .pill--sm } | Wind Blessed (haste), Walk on Air | [High Order Hunter](skyborne-high-order.md) |
| Orc | **Horde**{ .pill .pill--horde } | Classic | Blood Fury, Command (+5% pet damage) | [Orc Hunter](orc.md) |
| Troll | **Horde**{ .pill .pill--horde } | Classic | Berserking, Beast Slaying | [Troll Hunter](troll.md) |
| Tauren | **Horde**{ .pill .pill--horde } | Classic | War Stomp, Endurance | [Tauren Hunter](tauren.md) |
| Skyborne (Windshaper) | **Horde**{ .pill .pill--horde } | **New**{ .pill .pill--new .pill--sm } | Wind Blessed (haste), Skysight | [Windshaper Hunter](skyborne-windshaper.md) |

Full racial tables: [Races](../../characters/races.md#racial-abilities).

## Specs & talents

!!! tip "Full talent guide"
    The [Hunter talent guide](../../talents/hunter.md) gives a rating to each talent and a talent for each level from 10 to 60. Its tree data is from the launch client. If this section and the talent guide disagree, use the talent guide.

Talent points start at **level 10**, 1 for each level, for a total of **51 points at 60**. The Legacy talent *Talented* can move your first point to level 5 (Warcraft Tavern counts this as a maximum of 5 extra points). Refer to [Professions & Legacy](#professions-legacy).

=== "Beast Mastery"

    **The leveling spec.** Method, Mobalytics and Icy Veins all recommend it for 1–60.

    | Talent | What it does in Forever |
    |---|---|
    | Deadly Aspects | Early talent. Increases the effect of your aspects. Max it first |
    | Improved Aspect of the Monkey | Also gives 50% of the bonus to your pet |
    | Endurance Training | Now also includes the old Thick Hide |
    | **Focused Fire** | New. Replaces Improved Eyes of the Beast |
    | **Summon Hawk** | New 16-point talent: a maximum of 2 hawks fight with you. Shares the cooldown of Arcane Shot |
    | Bestial Discipline | Pet Focus regen, and now **also restores mana** |
    | Unleashed Fury / Ferocity | Pet damage and crit. Values are a little lower than in Classic |
    | Intimidation | Pet stun. Now also gives the pet 100% crit chance on the next hit |
    | Bestial Swiftness, Frenzy | Pet speed and attack-speed proc |

=== "Marksmanship"

    **The raid spec**, and the only spec that can play with no pet.

    | Talent | What it does in Forever |
    |---|---|
    | Lethal Attacks | New early damage talent |
    | Improved Stings | Replaces Improved Scorpid Sting. Available earlier |
    | Efficiency, Improved Arcane Shot | Small buffs |
    | **Lone Wolf** | 11-point talent: **+20% damage while you have no pet** |
    | **Careful Aim** | Changes 20–100% of your Intellect into Attack Power |
    | Rapid Killing | Decreases the cooldown of Rapid Fire. When a target with Serpent Sting dies, your next shot hits harder |
    | **Trueshot Aura** | Now a 21-point talent (earlier than in Classic). Gives **Ranged** AP only |
    | Rapid Recuperation | While Serpent Sting is on the target, 50% of your Spirit regen continues while you cast |
    | Barrage | Now also applies to Aimed Shot, at 5/10/15% |
    | Mortal Shots, Ranged Weapon Specialization | Classic-style damage talents |
    | **Sniper Shot** | 31-point capstone: **4 s cast, 15 s cooldown, 45 yd range**. The next 3 shots get +10 yd range |

    !!! conflict "Conflict"
        One search-result summary says that Sniper Shot has a "4-second cooldown". The Warcraft Tavern Marksmanship guide and the class page both give a **4 s cast** and a **15 s cooldown**. This guide uses those values.

=== "Survival"

    **Melee hybrid.** Traps, Mongoose Bite and bleeds. Weaker than BM for leveling, but strong in PvP.

    | Talent | What it does in Forever |
    |---|---|
    | Improved Tracking | Replaces Monster Slaying and Humanoid Slaying |
    | **Entrapment** | Now **always** procs when a trap triggers |
    | Savage Strikes | Applies to all melee attacks, at a lower value |
    | Deflection, Surefooted | Buffed. Surefooted also makes snares shorter |
    | **Predator's Edge** | Dual-wield support |
    | **Counterattack** | 16-point talent |
    | Resourcefulness | New (reported bugged in beta: it did not proc from crits) |
    | Expose Prey | Replaces Killer Instinct |
    | Survivalist's Discipline | New |
    | **Strider Kick** | 21-point talent |
    | **Lacerating Strikes** | 31-point capstone. Replaces Wyvern Sting. Mongoose Bite applies a **21 s bleed** |

    Proc roots (Entrapment, Counterattack, Improved Wing Clip and others) **share diminishing returns** in Forever.

### Recommended builds

Talent calculators show builds as images. Thus nobody has published the exact rank-by-rank orders in text. The milestones below come from Method, Mobalytics and Warcraft Tavern. Players tested them in the beta only to level 30.

<div class="milestones" markdown>

<p class="milestones-cap">Beast Mastery (leveling)</p>

Lv 10–14
:   Deadly Aspects (max)

    *Notes:* Early damage from your aspect

Lv 15–19
:   Endurance Training / Focused Fire

    *Notes:* The Mobalytics level-30 build takes Focused Fire 2/2

Lv 20–24
:   Bestial Swiftness, Unleashed Fury or Bestial Discipline

    *Notes:* Sources are different. The Warcraft Tavern leveling guide takes Bestial Swiftness and Ferocity. Its class overview prefers Bestial Discipline for mana

**25**
:   **Summon Hawk**

    *Notes:* First big power spike

Lv 26–30
:   Ferocity, then Intimidation

    *Notes:* Mobalytics: **21/0/0** at 30

Lv 31–40
:   Frenzy, Bestial Wrath line (*Classic-era layout, unconfirmed*)

    *Notes:* Not tested in beta

Lv 40–60
:   Complete BM, then put some points in Marksmanship for Efficiency/Lethal Attacks

    *Notes:* Respec to MM for raids at 60

</div>

!!! conflict "Conflict"
    The 2 Warcraft Tavern Hunter pages do not agree on the level-30 BM focus. The leveling guide uses Bestial Swiftness + Ferocity. The class overview uses Unleashed Fury + Ferocity with Bestial Discipline. Both work. Bestial Discipline helps more if you often have no mana.

**Endgame builds (theory until raids open on 9 December):**

- **Marksmanship raid, 5/46/0** (Warcraft Tavern): Deadly Aspects in BM, then all damage talents in MM through Sniper Shot, including Lone Wolf. If you keep the pet, replace Lone Wolf with 1 point in Improved Tracking. As an alternative, remove Hawk Eye for 3 points.
- **Beast Mastery raid/solo**: deep BM for Summon Hawk, Intimidation and pet talents, with the remaining points in MM. Pets are good now because they scale with your gear.
- **Survival PvP**: Survival to Lacerating Strikes with Counterattack and Strider Kick, plus Marksmanship for Improved Stings and Efficiency. Nobody has published a point split yet.

### Dual spec at 40

[Dual specialization](../../characters/leveling.md#dual-specialization) becomes available at **level 40** for **50g** at your class trainer. A good pair is BM for quests, plus Survival (PvP) or Marksmanship (dungeons). Respec fees decrease to 1g over time.

## Abilities & rotation

### Spells by level (Method)

| Level | Spells |
|---|---|
| 1 | Raptor Strike, Auto Shot |
| 4 | Serpent Sting |
| 6 | Arcane Shot, Hunter's Mark |
| 8 | Concussive Shot |
| 10 | Aspect of the Hawk, Call Pet; pet learns Growl, Great Stamina, Natural Armor |
| 12 | Mend Pet |
| 18 | Multi-Shot |
| **20** | **Aimed Shot**, Aspect of the Cheetah, Freezing Trap |
| 24 | Track Hidden |
| 25 | Summon Hawk (BM talent) |
| 26 | Rapid Fire |
| 28 | Frost Trap |
| 30 | Feign Death, Intimidation (talent), pet Dash |
| 36 | Viper Sting (Warcraft Tavern) |
| 46 | Aspect of the Wild (Warcraft Tavern) |

Aspect of the Monkey, Wing Clip, Mongoose Bite, Disengage, Scatter Shot, Immolation and Explosive Traps, Tranquilizing Shot and the other spells come at about their Classic levels (*not checked against Forever*).

### Rotations

=== "Beast Mastery"

    !!! rotation "Beast Mastery priority"

        <div class="priority" markdown>

        1. Aspect of the Hawk. Send the pet, then start with Auto Shot.
        2. Serpent Sting.
        3. **Summon Hawk** on cooldown.
        4. Arcane Shot when both hawks are out with 6+ s left (they share a cooldown).
        5. Aimed Shot on cooldown. Rapid Fire on cooldown for big pulls.
        6. If the pet loses aggro, use Wing Clip, Concussive Shot or Frost Trap. Then move back.

        </div>


=== "Marksmanship"

    !!! rotation "Marksmanship: Single target"

        <div class="priority" markdown>

        1. Put Immolation Trap where the tank will stand, before the pull
        2. Start **Sniper Shot** when the pull arrives
        3. Serpent Sting (apply it again when it expires. Rapid Recuperation needs it)
        4. Aimed Shot
        5. Arcane Shot
        6. Rapid Fire on cooldown
        7. Sniper Shot again on cooldown.

        </div>

    !!! rotation "Marksmanship: AoE"

        <div class="priority" markdown>

        1. Put Explosive Trap before the pull
        2. Multi-Shot
        3. Serpent Sting on many targets
        4. Sniper Shot
        5. Arcane Shot
        6. Trap again on cooldown
        7. Rapid Fire.

        </div>

    Remember that Multi-Shot and Aimed Shot share a cooldown.

=== "Survival"

    !!! rotation "Survival: Melee-weave"

        <div class="priority" markdown>

        1. Hawk or Beast aspect
        2. The correct tracking
        3. Auto Shot, Serpent Sting, Arcane Shot, Aimed Shot, Rapid Fire while the target comes near
        4. Move in: Raptor Strike, Immolation Trap at your feet, Mongoose Bite (applies the Lacerating bleed at 31 points), Strider Kick
        5. When the pet gets aggro, move back out and shoot again.

        </div>

    Full-melee Survival with Predator's Edge dual-wield is also possible. No source has published a complete priority yet.

### Aspects

| Aspect | Use |
|---|---|
| Hawk | Default for all ranged damage |
| Beast | Melee AP in Forever; Survival melee |
| Monkey | Dodge (shares 50% with the pet if talented); when something hits you |
| Cheetah / Pack | Travel only: you are **Dazed** if something hits you |
| Wild | Nature resistance for the group |

### Useful macros

??? example "Show 5 macros"

    Warcraft Tavern gives these 5 macros. Write them in the in-game macro editor (they use standard Classic macro conditionals).

    ```text
    #showtooltip Auto Shot
    /cast !Auto Shot
    ```

    ```text
    #showtooltip Hunter's Mark
    /cast [@mouseover,harm,nodead][] Hunter's Mark
    ```

    ```text
    /petattack [@mouseover,harm,nodead][]
    ```

    ```text
    #showtooltip
    /cast [@pet,dead] Revive Pet; [nopet] Call Pet; Mend Pet
    ```

    ```text
    #showtooltip Eagle Eye
    /cast [@cursor] Eagle Eye
    ```

    We wrote the texts above for this guide. It is *unconfirmed* if `[@cursor]` works on Eagle Eye in Forever.

## Leveling walkthrough 1–60

Hunters leveled fastest in the beta. Dungeon mobs give less XP, and dungeon quests give much more XP. Thus, do quests and go into dungeons for their quest chains. The zone ranges below are Classic ranges if they are not marked new. Refer to [Zones](../../world/zones.md).

<div class="route" markdown>

### 1–10: Learn the basics, get your pet

- **Zones:** the starting zone of your race ([Zephras Isle](../../world/zephras-isle.md) for Skyborne, to about 12). Each race add-on has the exact route.
- **Train:** Serpent Sting (4), Arcane Shot and Hunter's Mark (6), Concussive Shot (8).
- **Play:** Auto Shot to pull, Serpent Sting, Arcane Shot. Kite with Concussive Shot. Use Raptor Strike when a mob gets to you.
- **Level 10:** Aspect of the Hawk and the **taming chain**. The trainer gives *Taming the Beast*: tame 3 specified beasts with a Taming Rod. Then *Training the Beast* teaches Tame Beast, Feed Pet, Revive Pet and Beast Training. Quest givers are different for each race.
- **Camping:** at about level 5, take *The Great Outdoors* outside your level-5 hub and build a Basic Campfire. Refer to [Camping](../../systems/camping.md).
- **Profession:** take the starter gathering quest (+2 skill). Skinning is the classic Hunter choice.

### 10–20: Pet and first talents

- **Alliance:** Westfall and Loch Modan (or Darkshore). The new **Stormwind Harbor–Auberdine boat** makes it easy to go from one continent to the other.
- **Horde:** the Barrens (Crossroads), Silverpine Forest. The *Durotar Supply and Logistics* crate camp is west of the Crossroads.
- **Talents:** Deadly Aspects first.
- **Pet:** a Cat or Boar is the safe leveling choice. Remember that you can tame only beasts at your level or lower.
- **Dungeons:** Ragefire Chasm, [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) (13–18), [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) (15–22), Deadmines, Wailing Caverns.
- The **Cozy Sleeping Bag** scavenger hunt starts at level 14.

### 20–30: Aimed Shot and Summon Hawk

- **Level 20:** **Aimed Shot**, Aspect of the Cheetah, Freezing Trap. Expert professions become available.
- **Alliance:** Redridge (Three Corners crate camp), Wetlands, Duskwood, Ashenvale.
- **Horde:** Stonetalon, Hillsbrad (Tarren Mill), Ashenvale, Thousand Needles.
- **Level 25:** **Summon Hawk** (BM), and the Novice Hunter Legacy tier (+1 Legacy Point).
- **Level 26–28:** Rapid Fire, Frost Trap.
- **Dungeons:** Shadowfang Keep, [Excavation Site: Wetlands](../../content/dungeons/excavation-site.md), Stockade, Blackfathom Deeps, [City of Dalaran](../../content/dungeons/city-of-dalaran.md) (Alliance-friendly. In Dalaran, the guards attack Horde players when they see them).
- **Library books:** give books to Garion Wendell (Stormwind) or Owen Thadd (Undercity). Refer to the note below.

### 30–40: Feign Death, Darkspear Islands

- **Level 30:** **Feign Death**, Intimidation, pet Dash. Battle for the [Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands) opens.
- **Alliance:** Hillsbrad, Arathi, Stranglethorn, Desolace, Dustwallow (Theramore).
- **Horde:** Arathi (Hammerfall), Stranglethorn (Grom'gol), Desolace, Thousand Needles.
- **Level 35+:** the new contested zone [Riverglades](../../world/zones.md#riverglades) (35–45. Farholde Keep for Alliance, Rog'mar for Horde). Desolace centaur quests now need level 35. Artisan professions at 35.
- **Dungeons:** Razorfen Kraul, Gnomeregan, Scarlet Monastery wings, [The Drowned City](../../content/dungeons/drowned-city.md) (35–40).
- **Level 40:** **Mail armor**, **riding** (100g including your first mount. Refer to [Riding](../../characters/leveling.md#riding)) and **dual spec** (50g). Start to keep gold for these at about level 30.

### 40–50: Riverglades and Tanaris

- **Both factions:** complete Riverglades, then Badlands, Swamp of Sorrows, Tanaris (Steamwheedle Port ferry to Riverglades), Feralas, the Hinterlands.
- **Level 45:** Experienced Hunter Legacy tier.
- **Level 46:** Aspect of the Wild.
- **Dungeons:** [Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md) (40–45), Razorfen Downs, Uldaman, Zul'Farrak, [Alcaz Prison](../../content/dungeons/alcaz-prison.md) (48–53).
- **Pet upgrade:** use a Wolf for dungeons (Furious Howl). Keep a Boar or Cat for quests.

### 50–60: Azshara, Un'Goro and Hyjal

- **Zones:** [Azshara](../../world/zones.md#changed-classic-zones) (many new quests), Un'Goro, Felwood, Western and Eastern Plaguelands, Burning Steppes, Winterspring, Silithus.
- **Level 60:** [Mount Hyjal](../../world/zones.md#mount-hyjal) through Darkwhisper Gorge in Winterspring, and the Master Hunter Legacy tier.
- **Dungeons:** Maraudon, Sunken Temple, [Blackmaw Hold](../../content/dungeons/blackmaw-hold.md) (55–60), Blackrock Depths, then the level-60 dungeons and [Shaper's Terrace](../../content/dungeons/shapers-terrace.md).
- Start the **Onyxia attunement** early. It goes through Blackrock Spire.

!!! conflict "Conflict: library-book quests"
    The [leveling page](../../characters/leveling.md#carried-over-from-season-of-discovery) says that 10/20/25 books unlock quests at levels **20/35/45**. The Warcraft Tavern library-book guide says that the same book counts unlock *Friend of the Library* rewards at levels **1/20/30**. The 25-book tier gives a bow, *Truthseeker's Bow*, and other rewards. Neither source tells of a quest only for Hunters. Ask Garion Wendell or Owen Thadd in the game.

!!! warning "No Rhok'delar yet"
    The Classic level-60 Hunter epic bow quest needs a drop from Molten Core. Molten Core is not in Forever at launch. It is unknown if the quest will come back with a revamped Molten Core.

</div>

## Dungeons

**Your job:** ranged damage, crowd control, pulls.

- **Pull with Hunter's Mark and Auto Shot.** If you pulled too many mobs, use Feign Death. Mobs can resist Feign Death, so do not use it as your only plan.
- **Freezing Trap** is a 10 s hard CC that breaks when the target takes damage. Now you can use traps in combat, so you can trap again during the fight. Remember the **shared 30 s trap cooldown**: if you used Explosive Trap, Freezing Trap is not ready.
- **Pet:** in groups, set it to Passive or Defensive. When you have a tank, turn off Growl.
- **Tranquilizing Shot** removes Enrage and Frenzy.
- **No Misdirection** (a TBC spell. Nothing shows that Forever added it). Thus, let the tank get threat first.

| Level | Priority dungeons for a Hunter | Why |
|---|---|---|
| 13–22 | Hall of Thanes, Ruins of Lordaeron | New. Blue drops, camp blueprints (Fermenter, Arcane Salvager in Ruins) |
| 24–35 | Excavation Site, City of Dalaran, SFK | New dungeons with quest XP |
| 35–47 | Drowned City, Krol'dok Stronghold, SM | Mail and ranged upgrades |
| 48–60 | Alcaz Prison, Blackmaw Hold, ZF, Maraudon | Pre-raid blues |
| 60 | Shaper's Terrace, BRD, LBRS/UBRS, Strat, Scholo, DM | Pre-raid gear, Onyxia attunement |

Refer to [Dungeons](../../content/dungeons/index.md) for the full list. Each boss in a new dungeon reportedly drops a guaranteed blue.

## Raid preparation

Raids open on **9 December 2026** for level-60 characters. Refer to [Raids](../../content/raids/index.md).

| Raid | Size | Hunter notes |
|---|---|---|
| [The Barrow Deeps](../../content/raids/barrow-deeps.md) | 10 | Below Hyjal. Small raid, thus pet utility (Wolf Furious Howl) and traps are more important |
| [Hyjal Summit](../../content/raids/hyjal-summit.md) | 20 | 13 bosses. Possibly the main source of Hunter gear |
| [Onyxia's Lair](../../content/raids/onyxias-lair.md) | 40 | Needs the Drakefire Amulet. Fire resistance, and keep distance from other players in phase 2 |

**Pre-raid approach:** there is no Forever BiS list yet, because nobody has seen level-60 loot tables. Until a list is available:

1. Get blues with **Agility, hit and crit** from the level-60 dungeons and the new 55–60 dungeons.
2. Get to the hit cap. Sources do not agree on the boss level. The Warcraft Tavern overview says **9%** at 300 weapon skill against level-60 bosses. Its Marksmanship guide says 9% (or **6%** at 305 skill) against **level-63** bosses.
3. Get the best bow, gun or crossbow that you can. Ranged weapon damage is the most important.
4. Do Darkspear Islands for its reputation rewards (trinkets, rings, weapons).

**Consumables:** Agility elixirs and food, mana potions, healing potions (now made with **First Aid**, not Alchemy), and the best ammunition.

**Role:** players expect MM as the raid spec (Trueshot Aura, Sniper Shot). Because Lone Wolf gives 20% bonus damage, some raid MMs will play with no pet. Keep a pet for fights where its utility helps. Pets do not get player buffs now, but they get your crit and some of your AP.

## PvP

Refer to [PvP](../../content/pvp/index.md) and [Battlegrounds](../../content/pvp/battlegrounds.md).

- **Battlegrounds:** Warsong Gulch (10+), Arathi Basin (20+), **Darkspear Islands** (30+, new, 15v15 with 4 bases and a central flag), Alterac Valley (51+). Hunters are good flag hunters and node defenders.
- **Honor and ranks** occur in seasons with weekly caps. You can get Rank 14 at about week 10.
- **World PvP:** Feign Death, Freezing Trap and Concussive Shot let you select your fights. **Track Humanoids** and Track Hidden show enemies that wait to attack you.
- **Survival** is the PvP spec. Entrapment now always procs, and Counterattack and Strider Kick stop melee players. Lacerating Strikes adds bleed pressure. Remember that proc roots share diminishing returns.
- **Pets for PvP:** Cat (fast attacks), Wind Serpent (Lightning Breath ignores armor), Crocolisk (Dismember, −50% healing), Bat (Sonic Blast silence), Bird of Prey (*Mine!* disarm).

| Matchup | Tips |
|---|---|
| Warrior / Rogue | Keep range. Wing Clip, Frost Trap, Concussive. Scorpid Sting decreases their hit. Human Will to Survive or Dwarf Stoneform breaks the opener |
| Mage | Difficult. Viper Sting drains mana. Feign Death removes Polymorph targeting. Keep Scatter Shot for later (*Classic-era*) |
| Priest / Shaman / Druid healers | Pet with Dismember or Sonic Blast, Viper Sting, keep Serpent Sting on the target |
| Hunter mirror | Pet control and trap timing decide it. Use Tranquilizing Shot on the enrage of their pet |
| Warlock | Kill the pet or disarm it with Mine!. Tranquilizing Shot. Shatter Curse helps Orcs |

## Gear, stats & enchants

**Weapons:** bows, guns and crossbows. Melee weapons for stats (polearms from 20). No shields. You cannot use maces.

| Spec | Stat priority at level 30 (Warcraft Tavern, provisional) |
|---|---|
| Beast Mastery | Agility > Attack Power > Crit > Intellect > Stamina/Spirit > Strength > Armor |
| Marksmanship | Agility > Attack Power > Crit > Intellect > Stamina/Spirit > Strength > Armor |
| Survival | Agility > Attack Power > Crit > Strength > Intellect > Stamina/Spirit > Armor |

At 60, make **hit up to the cap** your first priority for raids. This is general Classic guidance. The exact cap in Forever is disputed (refer to [Raid preparation](#raid-preparation)). Warcraft Tavern says that its MM priority will change when level-60 tests are complete.

- **Agility** gives 2 Ranged AP for each point, and about 1% crit for each 53 points at 60.
- **Haste** is a new secondary stat. It also makes casts and the GCD faster. Skyborne get it free from Wind Blessed.
- **Intellect** is more important than in Classic because of Careful Aim and longer fights.
- **Enchants:** Agility on gloves and bracers, stamina on chest, run speed on boots while you level. Engineers add **scopes** to their ranged weapon. Nobody has published enchant numbers for Forever.

## Professions & Legacy { #professions-legacy }

<p class="divider">Professions</p>

Hunters wear leather until 40 and mail after that. They skin while the pet completes a kill.

<div class="prof-picks" markdown>

<div class="prof-pick prof-pick--best" markdown>

<p class="prof-rank" markdown>**S**{ .tier .tier-s } Best pick</p>

<p class="prof-pair" markdown>:material-bag-personal: Leatherworking <span class="prof-plus">+</span> :material-knife: Skinning</p>

<p class="prof-for">Best for: Leveling and gold</p>

<div class="pills" markdown>
**Leveling**{ .pill .pill--success .pill--sm } **Gold**{ .pill .pill--gold .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:100%"><span>5/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
</dl>

- The Method choice: many new BoP leather and mail patterns from cheap materials
- You skin while the pet completes kills

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Camp Tent (rested XP) · Camp Chair (+2% crit)</p>

</div>

<div class="prof-pick prof-pick--alt" markdown>

<p class="prof-rank" markdown>**A**{ .tier .tier-a } Strong alternative</p>

<p class="prof-pair" markdown>:material-cog: Engineering <span class="prof-plus">+</span> :material-pickaxe: Mining</p>

<p class="prof-for">Best for: PvP and raid utility</p>

<div class="pills" markdown>
**Raids**{ .pill .pill--info .pill--sm } **PvP**{ .pill .pill--danger .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:100%"><span>5/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:40%"><span>2/5</span></span></dd>
</dl>

- The Warcraft Tavern choice: scopes, ammo, explosives and PvP gadgets

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Reagent Bot · Lodestone (melee AP)</p>

</div>

<div class="prof-pick prof-pick--sit" markdown>

<p class="prof-rank" markdown>**B**{ .tier .tier-b } Situational</p>

<p class="prof-pair" markdown>:material-flask: Alchemy <span class="prof-plus">+</span> :material-leaf: Herbalism</p>

<p class="prof-for">Best for: Raid consumables</p>

<div class="pills" markdown>
**Raids**{ .pill .pill--info .pill--sm } **Gold**{ .pill .pill--gold .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:40%"><span>2/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
</dl>

- Elixirs for raids (healing potions are now part of First Aid)

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Mana Well (mana regen) · Incense Candle (Intellect)</p>

</div>

</div>

<p class="legend" markdown>Codex ratings out of 5, from the sources above. Compare all classes in [Best professions by class](../../characters/professions.md#best-professions-by-class).</p>

<div class="pills" markdown>
**:material-medical-bag: First Aid · healing potions**{ .pill .pill--success } **:material-pot-steam: Cooking · campfires**{ .pill .pill--info } **:material-fish: Fishing · Fish Bowl**{ .pill .pill--info }
</div>

**Secondary skills.** Cooking makes XP food and pet food. First Aid makes bandages (Freezing Trap gives you the time to use them) and healing potions. Fishing.

!!! tip "Race notes"
    **Tauren:** *Cultivation* adds herbs for Herbalists.

Crafting professions give [Legacy Points](../../characters/legacy.md) at skill 150, 225 and 300. Each profession adds a [camp feature](../../systems/camping.md). Professions give no passive stats in Forever.

**Legacy picks** (16 points for each character at launch):

| Priority | Talent | Why |
|---|---|---|
| 1 | Well Rested 5/5 → **Talented** | Earlier talent points; rested XP |
| 2 | **Bountiful Harvest** (if you skin) | More scarce materials |
| 3 | Frequent Flier | Cheaper, faster flights |
| 4 | Thrill of Adventure | Health and mana from kills; open world only |
| 60 | Gourmand, For Great Honor, Reagent Economy | Raid food, PvP Honor, no vendor reagents |

## Hardcore notes

!!! hardcore "Hardcore survival"

    [Hardcore](../../about/hardcore.md) comes in winter 2026/2027. Hunters are some of the safest classes for it:

    - **Do not tame while another mob can get to you.** Taming decreases your armor by 100% during the channel.
    - Keep **Feign Death** and a **Freezing Trap** ready before every pull. Remember the shared trap cooldown.
    - Do not fight in Cheetah or Pack. Many Hardcore Hunters die because they become Dazed.
    - Keep a defensive pet (Boar, Bear, Turtle) for dangerous zones.
    - Skyborne **Walk on Air** and Night Elf **Shadowmeld** are extra escape buttons.
    - Mobs can resist Feign Death. Have a second plan.
    - For elite quests and dungeons, go with a group. In corridors, set the pet to Passive so that it does not pull.

## Common mistakes & FAQ

??? question "My pet keeps dying. Is that me?"
    Partly it is the game: at launch, pets were less durable than in Classic Era. The 10 November tuning makes them more durable. Until then, use Mend Pet early, Endurance Training, and a defensive family for AoE pulls.

??? question "Should I level as Marksmanship with Lone Wolf?"
    No. Warcraft Tavern and Method both recommend BM. The pet tanks for you, and this decreases downtime. Lone Wolf is very good in raids. Some players do not like Lone Wolf because it gives a reward when you ignore the pet. A Blizzard forum thread said exactly that.

??? question "Why can't I place a Frost Trap after my Explosive Trap?"
    In Forever, all traps share 1 **30 s** cooldown.

??? question "Does Hunter's Mark boost my pet?"
    Yes, Method says that it does, because pets scale from your attack power.

??? question "Why won't my shot fire?"
    You are in the **8-yard deadzone**. Move back, or use Wing Clip or Disengage.

??? question "Is Survival a melee spec now?"
    Mostly. It can melee-weave, or go full melee with Predator's Edge dual-wield. It is weaker than BM for quests.

??? question "Can I tame the new Fox family?"
    Yes. Foxes have *Trickster's Dance* (dodge and attack speed for 12 s). Skyborne Hunters reportedly find foxes on Zephras Isle (*unconfirmed*).

**Common mistakes**

- You use Multi-Shot and expect Aimed Shot to be ready: they share a cooldown.
- You keep Growl on in groups.
- You do not feed the pet: an Unhappy pet does only 75% damage, a Happy pet does 125%.
- You have no ammo or arrows during a dungeon.
- You ignore Intellect as MM. Careful Aim changes it into damage.

## Sources

??? quote "14 sources"

    - [Warcraft Tavern: Hunter guide](https://warcrafttavern.com/forever/guides/hunter/)
    - [Warcraft Tavern: Hunter leveling](https://www.warcrafttavern.com/forever/guides/hunter-leveling/)
    - [Warcraft Tavern: Marksmanship Hunter](https://www.warcrafttavern.com/forever/guides/marksmanship-hunter/)
    - [Warcraft Tavern: Hunter pets](https://www.warcrafttavern.com/forever/guides/hunter-pets/)
    - [Warcraft Tavern: Hunter pet families](https://www.warcrafttavern.com/forever/guides/hunter-pet-families/)
    - [Warcraft Tavern: Best Hunter pets](https://www.warcrafttavern.com/forever/guides/best-hunter-pets/)
    - [Warcraft Tavern: Library books](https://www.warcrafttavern.com/forever/guides/library-books/)
    - [Warcraft Tavern: Beta dates and level caps](https://www.warcrafttavern.com/forever/guides/beta/)
    - [Method: Hunter leveling guide and talents](https://www.method.gg/wow-forever/wow-forever-hunter-leveling-guide-and-talents)
    - [Mobalytics: Hunter leveling guide](https://mobalytics.gg/wow-forever/classes/hunter-leveling-guide)
    - [Icy Veins: Hunter class quests](https://www.icy-veins.com/wow-forever/hunter-class-quests)
    - [Blizzard forums: "Lone Wolf is a mistake"](https://us.forums.blizzard.com/en/wow/t/2375143)
    - [Wowhead: Taming the Beast (Skyborne)](https://www.wowhead.com/forever/quest=94978)
    - [Warcraft Wiki: Josephine Carson](https://warcraft.wiki.gg/wiki/Josephine_Carson)
