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
    Forever launched on 4 November. The public beta capped at level 30, so **almost every talent build above level 30 is theory**, not tested play. A class-tuning patch is planned for **Tuesday 10 November** that makes Hunter pets more durable (Classic Era parity). Re-check numbers after it lands. Reference data lives on the [Hunter class page](../../characters/classes/hunter.md).

## Overview

The Hunter is a ranged physical damage dealer who fights alongside a tamed beast. Forever keeps that core and adds three real choices: a pet-focused **Beast Mastery**, a **Marksmanship** that can drop the pet entirely, and a **Survival** rebuilt around melee, traps and bleeds.

<aside class="infobox" markdown>
<p class="infobox-title">Hunter at a glance</p>

| | |
|---|---|
| **Roles** | Damage (ranged or melee). Pets can off-tank solo content |
| **Armor** | **Cloth**{ .pill .pill--cloth } and **Leather**{ .pill .pill--leather } from level 1, **Mail at 40** |
| **Resource** | **Mana**{ .pill .pill--mana } (pets use Focus) |
| **Leveling speed** | **Fastest class in the beta**, ahead of Warlock and Mage |
| **Difficulty** | Easy to level, harder to master (pet control, the 8-yard deadzone, mana) |

</aside>

<div class="proscons" markdown>
<div class="pros" markdown>

Strengths

- Kills fast and safely: the pet tanks while you shoot.
- Excellent kiting tools: Concussive Shot, Wing Clip, Frost Trap, and now **traps in combat**.
- Feign Death and Freezing Trap give you emergency exits that few classes have.
- Pets scale with **your** gear, so a pet tamed at 30 is no longer left behind.

</div>
<div class="cons" markdown>

Weaknesses

- The **deadzone**: you can't shoot targets closer than 8 yards, and you're weak in melee unless you're Survival.
- Mana runs dry on long fights before talents like Rapid Recuperation.
- Pets die in AoE until the 10 November durability fix.
- Ammunition, food for your pet, and stable fees add bag clutter and cost (Classic-era behaviour, not changed as far as we know).

</div>
</div>

### What's new in Forever

- **Aimed Shot is baseline at 20** for every spec. Multi-Shot shares its cooldown; Arcane Shot has its own.
- **Traps work in combat.** All traps share one **30 s** cooldown.
- Aspect of the Beast now adds melee AP; Scorpid Sting reduces the target's hit chance by 2% (doesn't stack with Insect Swarm); Disengage drops more threat.
- Pre-launch buffs: Aimed Shot +110% bonus damage, Arcane Shot +30% base damage, Serpent Sting buffed, Aspect of the Hawk ranks 20/35/50/70/90/110 RAP. Hunter's Mark ranks no longer stack.
- **Pets** scale with the Hunter's gear (10% of your Attack Power and 100% of your crit chance, per Warcraft Tavern) and no longer receive player buffs. Every family learns Bite or Claw, and Dive or Dash, and has **one unique ability**. **Fox** is a new family.
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

Talent points start at **level 10**, one per level, for **51 points at 60**. The Legacy talent *Talented* can bring your first point forward to level 5 (Warcraft Tavern counts this as up to 5 extra points); see [Professions & Legacy](#professions-legacy).

=== "Beast Mastery"

    **The leveling spec.** Method, Mobalytics and Icy Veins all recommend it for 1–60.

    | Talent | What it does in Forever |
    |---|---|
    | Deadly Aspects | Early talent; boosts your aspects. Max it first |
    | Improved Aspect of the Monkey | Also gives 50% of the bonus to your pet |
    | Endurance Training | Now also includes the old Thick Hide |
    | **Focused Fire** | New; replaces Improved Eyes of the Beast |
    | **Summon Hawk** | New 16-point talent: up to 2 hawks fight with you. Shares Arcane Shot's cooldown |
    | Bestial Discipline | Pet Focus regen, and now **also restores mana** |
    | Unleashed Fury / Ferocity | Pet damage and crit; slightly lower values than Classic |
    | Intimidation | Pet stun; now also gives the pet 100% crit chance on the next hit |
    | Bestial Swiftness, Frenzy | Pet speed and attack-speed proc |

=== "Marksmanship"

    **The raid spec**, and the only one that can go petless.

    | Talent | What it does in Forever |
    |---|---|
    | Lethal Attacks | New early damage talent |
    | Improved Stings | Replaces Improved Scorpid Sting; available earlier |
    | Efficiency, Improved Arcane Shot | Small buffs |
    | **Lone Wolf** | 11-point talent: **+20% damage while you have no pet** |
    | **Careful Aim** | Converts 20–100% of your Intellect into Attack Power |
    | Rapid Killing | Lowers Rapid Fire's cooldown; the next shot after a Serpent-Stung target dies hits harder |
    | **Trueshot Aura** | Now a 21-point talent (earlier than Classic) and gives **Ranged** AP only |
    | Rapid Recuperation | While Serpent Sting is on the target, 50% of your Spirit regen continues while casting |
    | Barrage | Now also covers Aimed Shot, at 5/10/15% |
    | Mortal Shots, Ranged Weapon Specialization | Classic-style damage talents |
    | **Sniper Shot** | 31-point capstone: **4 s cast, 15 s cooldown, 45 yd range**; the next three shots gain +10 yd range |

    !!! conflict "Conflict"
        One search-result summary describes Sniper Shot as having a "4-second cooldown". Warcraft Tavern's Marksmanship guide and the class page both give a **4 s cast** and **15 s cooldown**; this guide uses those.

=== "Survival"

    **Melee hybrid.** Traps, Mongoose Bite and bleeds. Weaker for leveling than BM, but strong in PvP.

    | Talent | What it does in Forever |
    |---|---|
    | Improved Tracking | Replaces Monster Slaying and Humanoid Slaying |
    | **Entrapment** | Now **always** procs when a trap triggers |
    | Savage Strikes | Covers all melee attacks, at a lower value |
    | Deflection, Surefooted | Buffed; Surefooted also shortens snares |
    | **Predator's Edge** | Dual-wield support |
    | **Counterattack** | 16-point talent |
    | Resourcefulness | New (reported bugged in beta: didn't proc from crits) |
    | Expose Prey | Replaces Killer Instinct |
    | Survivalist's Discipline | New |
    | **Strider Kick** | 21-point talent |
    | **Lacerating Strikes** | 31-point capstone; replaces Wyvern Sting. Mongoose Bite applies a **21 s bleed** |

    Proc roots (Entrapment, Counterattack, Improved Wing Clip and others) **share diminishing returns** in Forever.

### Recommended builds

Talent calculators show builds as images, so exact rank-by-rank orders aren't published in text. The milestones below come from Method, Mobalytics and Warcraft Tavern, and only up to level 30 were tested in the beta.

<div class="milestones" markdown>

<p class="milestones-cap">Beast Mastery (leveling)</p>

Lv 10–14
:   Deadly Aspects (max)

    *Notes:* Early damage from your aspect

Lv 15–19
:   Endurance Training / Focused Fire

    *Notes:* Mobalytics' 30 build takes Focused Fire 2/2

Lv 20–24
:   Bestial Swiftness, Unleashed Fury or Bestial Discipline

    *Notes:* Sources differ: Warcraft Tavern's leveling guide takes Bestial Swiftness and Ferocity; its class overview prefers Bestial Discipline for mana

**25**
:   **Summon Hawk**

    *Notes:* First big power spike

Lv 26–30
:   Ferocity, then Intimidation

    *Notes:* Mobalytics: **21/0/0** at 30

Lv 31–40
:   Frenzy, Bestial Wrath line (*Classic-era layout, unconfirmed*)

    *Notes:* Untested in beta

Lv 40–60
:   Finish BM, then dip Marksmanship for Efficiency/Lethal Attacks

    *Notes:* Respec to MM for raids at 60

</div>

!!! conflict "Conflict"
    Warcraft Tavern's two Hunter pages disagree on the level-30 BM focus: Bestial Swiftness + Ferocity (leveling guide) versus Unleashed Fury + Ferocity with Bestial Discipline (class overview). Both work; Bestial Discipline helps more if you run out of mana.

**Endgame builds (theory until raids open on 9 December):**

- **Marksmanship raid, 5/46/0** (Warcraft Tavern): Deadly Aspects in BM, then everything damage-related in MM through Sniper Shot, including Lone Wolf. Swap Lone Wolf for 1 point in Improved Tracking if you keep the pet, or drop Hawk Eye for 3 points.
- **Beast Mastery raid/solo**: deep BM for Summon Hawk, Intimidation and pet talents, with the rest in MM. Pets do well now that they scale with your gear.
- **Survival PvP**: Survival to Lacerating Strikes with Counterattack and Strider Kick, plus Marksmanship for Improved Stings and Efficiency. No published point split yet.

### Dual spec at 40

[Dual specialization](../../characters/leveling.md#dual-specialization) unlocks at **level 40** for **50g** at your class trainer. A good pair: BM for questing, plus Survival (PvP) or Marksmanship (dungeons). Respec fees decay to 1g over time.

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

Aspect of the Monkey, Wing Clip, Mongoose Bite, Disengage, Scatter Shot, Immolation and Explosive Traps, Tranquilizing Shot and the rest arrive at roughly their Classic levels (*not checked against Forever*).

### Rotations

=== "Beast Mastery"

    !!! rotation "Beast Mastery priority"

        <div class="priority" markdown>

        1. Aspect of the Hawk. Send the pet, then open with Auto Shot.
        2. Serpent Sting.
        3. **Summon Hawk** on cooldown.
        4. Arcane Shot once both hawks are out with 6+ s left (they share a cooldown).
        5. Aimed Shot on cooldown; Rapid Fire on cooldown for big pulls.
        6. If the pet loses aggro: Wing Clip, Concussive Shot or Frost Trap, then step back.

        </div>


=== "Marksmanship"

    !!! rotation "Marksmanship: Single target"

        <div class="priority" markdown>

        1. Pre-place Immolation Trap where the tank will stand
        2. Start **Sniper Shot** as the pull lands
        3. Serpent Sting (refresh on expiry; it powers Rapid Recuperation)
        4. Aimed Shot
        5. Arcane Shot
        6. Rapid Fire on cooldown
        7. Sniper Shot again on cooldown.

        </div>

    !!! rotation "Marksmanship: AoE"

        <div class="priority" markdown>

        1. Pre-place Explosive Trap
        2. Multi-Shot
        3. Serpent Sting on several targets
        4. Sniper Shot
        5. Arcane Shot
        6. Re-trap on cooldown
        7. Rapid Fire.

        </div>

    Remember Multi-Shot and Aimed Shot share a cooldown.

=== "Survival"

    !!! rotation "Survival: Melee-weave"

        <div class="priority" markdown>

        1. Hawk or Beast aspect
        2. The right tracking
        3. Auto Shot, Serpent Sting, Arcane Shot, Aimed Shot, Rapid Fire as the target closes
        4. Step in: Raptor Strike, Immolation Trap at your feet, Mongoose Bite (applies the Lacerating bleed at 31 points), Strider Kick
        5. Step back out when the pet takes aggro and shoot again.

        </div>

    Full-melee Survival with Predator's Edge dual-wielding is also viable; no source has published a finished priority yet.

### Aspects

| Aspect | Use |
|---|---|
| Hawk | Default for all ranged damage |
| Beast | Melee AP in Forever; Survival melee |
| Monkey | Dodge (shares 50% with the pet if talented); when something is hitting you |
| Cheetah / Pack | Travel only: you're **Dazed** if hit |
| Wild | Nature resistance for the group |

### Useful macros

??? example "Show 5 macros"

    Warcraft Tavern lists these five; write them in the in-game macro editor (they use standard Classic macro conditionals).

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

    The texts above are written for this guide; whether `[@cursor]` works on Eagle Eye in Forever is *unconfirmed*.

## Leveling walkthrough 1–60

Hunters leveled fastest in the beta. Dungeon mobs give less XP and dungeon quests give much more, so quest through and hit dungeons for their quest chains. Zone ranges below are Classic ranges unless marked new; see [Zones](../../world/zones.md).

<div class="route" markdown>

### 1–10: Learn the basics, get your pet

- **Zones:** your race's starting zone ([Zephras Isle](../../world/zephras-isle.md) for Skyborne, to about 12). Each race add-on has the exact route.
- **Train:** Serpent Sting (4), Arcane Shot and Hunter's Mark (6), Concussive Shot (8).
- **Play:** Auto Shot to pull, Serpent Sting, Arcane Shot, kite with Concussive Shot, Raptor Strike when something reaches you.
- **Level 10:** Aspect of the Hawk and the **taming chain**. The trainer gives *Taming the Beast*: tame three specific beasts with a Taming Rod, then *Training the Beast* teaches Tame Beast, Feed Pet, Revive Pet and Beast Training. Quest givers vary by race.
- **Camping:** at about level 5, take *The Great Outdoors* outside your level-5 hub and build a Basic Campfire. See [Camping](../../systems/camping.md).
- **Profession:** take the starter gathering quest (+2 skill). Skinning is the classic Hunter pick.

### 10–20: Pet and first talents

- **Alliance:** Westfall and Loch Modan (or Darkshore). The new **Stormwind Harbor–Auberdine boat** makes crossing continents easy.
- **Horde:** the Barrens (Crossroads), Silverpine Forest. The *Durotar Supply and Logistics* crate camp is west of the Crossroads.
- **Talents:** Deadly Aspects first.
- **Pet:** a Cat or Boar is the safe leveling pick. Remember you can only tame beasts at your level or lower.
- **Dungeons:** Ragefire Chasm, [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) (13–18), [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) (15–22), Deadmines, Wailing Caverns.
- **Cozy Sleeping Bag** scavenger hunt starts at level 14.

### 20–30: Aimed Shot and Summon Hawk

- **Level 20:** **Aimed Shot**, Aspect of the Cheetah, Freezing Trap. Expert professions open.
- **Alliance:** Redridge (Three Corners crate camp), Wetlands, Duskwood, Ashenvale.
- **Horde:** Stonetalon, Hillsbrad (Tarren Mill), Ashenvale, Thousand Needles.
- **Level 25:** **Summon Hawk** (BM), and the Novice Hunter Legacy tier (+1 Legacy Point).
- **Level 26–28:** Rapid Fire, Frost Trap.
- **Dungeons:** Shadowfang Keep, [Excavation Site: Wetlands](../../content/dungeons/excavation-site.md), Stockade, Blackfathom Deeps, [City of Dalaran](../../content/dungeons/city-of-dalaran.md) (Alliance-friendly; Horde are attacked on sight in Dalaran).
- **Library books:** turn in books at Garion Wendell (Stormwind) or Owen Thadd (Undercity). See the note below.

### 30–40: Feign Death, Darkspear Islands

- **Level 30:** **Feign Death**, Intimidation, pet Dash. Battle for the [Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands) opens.
- **Alliance:** Hillsbrad, Arathi, Stranglethorn, Desolace, Dustwallow (Theramore).
- **Horde:** Arathi (Hammerfall), Stranglethorn (Grom'gol), Desolace, Thousand Needles.
- **Level 35+:** the new contested zone [Riverglades](../../world/zones.md#riverglades) (35–45; Farholde Keep for Alliance, Rog'mar for Horde). Desolace centaur quests now need level 35. Artisan professions at 35.
- **Dungeons:** Razorfen Kraul, Gnomeregan, Scarlet Monastery wings, [The Drowned City](../../content/dungeons/drowned-city.md) (35–40).
- **Level 40:** **Mail armor**, **riding** (100g including your first mount; see [Riding](../../characters/leveling.md#riding)) and **dual spec** (50g). Budget gold from about level 30.

### 40–50: Riverglades and Tanaris

- **Both factions:** finish Riverglades, then Badlands, Swamp of Sorrows, Tanaris (Steamwheedle Port ferry to Riverglades), Feralas, the Hinterlands.
- **Level 45:** Experienced Hunter Legacy tier.
- **Level 46:** Aspect of the Wild.
- **Dungeons:** [Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md) (40–45), Razorfen Downs, Uldaman, Zul'Farrak, [Alcaz Prison](../../content/dungeons/alcaz-prison.md) (48–53).
- **Pet upgrade:** swap to a Wolf for dungeons (Furious Howl), keep a Boar or Cat for questing.

### 50–60: Azshara, Un'Goro and Hyjal

- **Zones:** [Azshara](../../world/zones.md#changed-classic-zones) (lots of new quests), Un'Goro, Felwood, Western and Eastern Plaguelands, Burning Steppes, Winterspring, Silithus.
- **Level 60:** [Mount Hyjal](../../world/zones.md#mount-hyjal) through Darkwhisper Gorge in Winterspring, and the Master Hunter Legacy tier.
- **Dungeons:** Maraudon, Sunken Temple, [Blackmaw Hold](../../content/dungeons/blackmaw-hold.md) (55–60), Blackrock Depths, then the 60 dungeons and [Shaper's Terrace](../../content/dungeons/shapers-terrace.md).
- Start the **Onyxia attunement** early; it runs through Blackrock Spire.

!!! conflict "Conflict: library-book quests"
    The [leveling page](../../characters/leveling.md#carried-over-from-season-of-discovery) says 10/20/25 books unlock quests at levels **20/35/45**. Warcraft Tavern's library-book guide lists the same book counts as unlocking *Friend of the Library* rewards at levels **1/20/30** (the 25-book tier offers a bow, *Truthseeker's Bow*, among other rewards). Neither source describes a Hunter-only quest. Check with Garion Wendell or Owen Thadd in game.

!!! warning "No Rhok'delar yet"
    The Classic level-60 Hunter epic bow quest needs a drop from Molten Core, which isn't in Forever at launch. Whether it returns with a revamped Molten Core is unknown.

</div>

## Dungeons

**Your job:** ranged damage, crowd control, pulling.

- **Pull with Hunter's Mark and Auto Shot**, then Feign Death if you pulled too much. Feign Death can be resisted, so don't rely on it alone.
- **Freezing Trap** is a 10 s hard CC that breaks on damage. With traps now usable in combat, you can re-trap mid-fight. Remember the **shared 30 s trap cooldown**: if you used Explosive Trap, Freezing Trap isn't ready.
- **Pet:** set it to Passive or Defensive in groups, and turn off Growl when you have a tank.
- **Tranquilizing Shot** removes Enrage and Frenzy.
- **No Misdirection** (a TBC spell; nothing suggests Forever added it), so let the tank build threat first.

| Level | Dungeons a Hunter should prioritise | Why |
|---|---|---|
| 13–22 | Hall of Thanes, Ruins of Lordaeron | New; blue drops, camp blueprints (Fermenter, Arcane Salvager in Ruins) |
| 24–35 | Excavation Site, City of Dalaran, SFK | New dungeons with quest XP |
| 35–47 | Drowned City, Krol'dok Stronghold, SM | Mail and ranged upgrades |
| 48–60 | Alcaz Prison, Blackmaw Hold, ZF, Maraudon | Pre-raid blues |
| 60 | Shaper's Terrace, BRD, LBRS/UBRS, Strat, Scholo, DM | Pre-raid gear, Onyxia attunement |

See [Dungeons](../../content/dungeons/index.md) for the full list. Each new-dungeon boss reportedly drops a guaranteed blue.

## Raid preparation

Raids open **9 December 2026** for level-60 characters. See [Raids](../../content/raids/index.md).

| Raid | Size | Hunter notes |
|---|---|---|
| [The Barrow Deeps](../../content/raids/barrow-deeps.md) | 10 | Beneath Hyjal. Small raid, so pet utility (Wolf Furious Howl) and traps matter more |
| [Hyjal Summit](../../content/raids/hyjal-summit.md) | 20 | 13 bosses. Likely the main Hunter gear source |
| [Onyxia's Lair](../../content/raids/onyxias-lair.md) | 40 | Needs the Drakefire Amulet. Fire resistance and spreading out in phase 2 |

**Pre-raid approach:** no Forever BiS list exists yet, because nobody has seen level-60 loot tables. Until one appears:

1. Chase **Agility, hit and crit** blues from the level-60 dungeons and the new 55–60 dungeons.
2. Reach the hit cap. Sources disagree on the boss level: Warcraft Tavern's overview says **9%** at 300 weapon skill against level-60 bosses; its Marksmanship guide says 9% (or **6%** at 305 skill) against **level-63** bosses.
3. Get the best bow, gun or crossbow you can; ranged weapon damage matters most.
4. Run Darkspear Islands for its reputation rewards (trinkets, rings, weapons).

**Consumables:** Agility elixirs and food, mana potions, healing potions (now made by **First Aid**, not Alchemy), and the best ammunition.

**Role:** MM is the expected raid spec (Trueshot Aura, Sniper Shot). Lone Wolf's 20% bonus means some raid MMs will play without a pet; keep one for utility fights. Pets don't receive player buffs anymore, but they inherit your crit and some of your AP.

## PvP

See [PvP](../../content/pvp/index.md) and [Battlegrounds](../../content/pvp/battlegrounds.md).

- **Battlegrounds:** Warsong Gulch (10+), Arathi Basin (20+), **Darkspear Islands** (30+, new, 15v15 with four bases and a central flag), Alterac Valley (51+). Hunters are good flag hunters and node defenders.
- **Honor and ranks** run in seasons with weekly caps. Rank 14 is reachable around week 10.
- **World PvP:** Feign Death, Freezing Trap and Concussive Shot let you choose your fights. **Track Humanoids** and Track Hidden reveal ambushers.
- **Survival** is the PvP spec: Entrapment now always procs, Counterattack and Strider Kick lock melee down, and Lacerating Strikes adds bleed pressure. Remember proc roots share diminishing returns.
- **Pets for PvP:** Cat (fast attacks), Wind Serpent (Lightning Breath ignores armor), Crocolisk (Dismember, −50% healing), Bat (Sonic Blast silence), Bird of Prey (*Mine!* disarm).

| Matchup | Tips |
|---|---|
| Warrior / Rogue | Keep range; Wing Clip, Frost Trap, Concussive. Scorpid Sting reduces their hit. Human Will to Survive or Dwarf Stoneform breaks the opener |
| Mage | Hard. Viper Sting drains mana; Feign Death drops Polymorph targeting; save Scatter Shot (*Classic-era*) |
| Priest / Shaman / Druid healers | Pet with Dismember or Sonic Blast, Viper Sting, keep Serpent Sting up |
| Hunter mirror | Pet control and trap timing decide it. Tranquilizing Shot their pet's enrage |
| Warlock | Kill or Mine!-disarm the pet; Tranquilizing Shot; Shatter Curse helps Orcs |

## Gear, stats & enchants

**Weapons:** bows, guns and crossbows; melee weapons for stats (polearms from 20). No shields. Maces are not usable.

| Spec | Stat priority at level 30 (Warcraft Tavern, provisional) |
|---|---|
| Beast Mastery | Agility > Attack Power > Crit > Intellect > Stamina/Spirit > Strength > Armor |
| Marksmanship | Agility > Attack Power > Crit > Intellect > Stamina/Spirit > Strength > Armor |
| Survival | Agility > Attack Power > Crit > Strength > Intellect > Stamina/Spirit > Armor |

At 60, treat **hit up to the cap** as your first priority for raids (general Classic guidance; Forever's exact cap is disputed, see [Raid preparation](#raid-preparation)). Warcraft Tavern says its MM priority will change once level-60 testing is done.

- **Agility** gives 2 Ranged AP per point and about 1% crit per 53 points at 60.
- **Haste** is a new secondary stat; it speeds casts and the GCD too. Skyborne get it for free from Wind Blessed.
- **Intellect** matters more than in Classic because of Careful Aim and longer fights.
- **Enchants:** Agility on gloves and bracers, stamina on chest, run speed on boots while leveling. Engineers add **scopes** to their ranged weapon. Forever-specific enchant numbers aren't published.

## Professions & Legacy { #professions-legacy }

| Pair | Why |
|---|---|
| **Leatherworking + Skinning** | Method's pick. Many new BoP leather and mail patterns, cheap materials; you skin while the pet finishes kills |
| **Engineering + Mining** | Scopes, ammo, explosives and PvP gadgets (Warcraft Tavern's pick) |
| Alchemy + Herbalism | Elixirs for raids (healing potions now belong to First Aid) |

Leveling any of the six crafting professions to 150/225/300 also earns [Legacy Points](../../characters/legacy.md). Secondary skills: **Cooking** (camp fires, XP food, pet food), **First Aid** (bandages and now healing potions; Freezing Trap buys bandage time), Fishing.

**Camping:** the Skinning camp item, the **Camp Chair**, gives +2% crit; the Leatherworking **Camp Tent** stores rested XP.

**Legacy picks** (16 points per character at launch):

| Priority | Talent | Why |
|---|---|---|
| 1 | Well Rested 5/5 → **Talented** | Earlier talent points; rested XP |
| 2 | **Bountiful Harvest** (if you skin) | More scarce materials |
| 3 | Frequent Flier | Cheaper, faster flights |
| 4 | Thrill of Adventure | Health and mana from kills; open world only |
| 60 | Gourmand, For Great Honor, Reagent Economy | Raid food, PvP Honor, no vendor reagents |

## Hardcore notes

!!! hardcore "Hardcore survival"

    [Hardcore](../../about/hardcore.md) arrives in winter 2026/2027. Hunters are among the safest classes for it:

    - **Never tame while another mob can reach you.** Taming reduces your armor by 100% for the channel.
    - Keep **Feign Death** and a **Freezing Trap** ready before every pull, and remember the shared trap cooldown.
    - Don't fight in Cheetah or Pack: being Dazed is how many Hardcore Hunters die.
    - Keep a defensive pet (Boar, Bear, Turtle) for dangerous zones.
    - Skyborne **Walk on Air** and Night Elf **Shadowmeld** are extra escape buttons.
    - Feign Death can be resisted. Have a second plan.
    - Elite quests and dungeons: go with a group, and set the pet to Passive in corridors so it doesn't pull.

## Common mistakes & FAQ

??? question "My pet keeps dying. Is that me?"
    Partly the game: pets were less durable than in Classic Era at launch. The 10 November tuning raises their durability. Until then use Mend Pet early, Endurance Training, and a defensive family for AoE pulls.

??? question "Should I level as Marksmanship with Lone Wolf?"
    No. Warcraft Tavern and Method both recommend BM; the pet tanks for you, which saves downtime. Lone Wolf shines in raids. Some players dislike Lone Wolf because it rewards ignoring the pet; a Blizzard forum thread argued exactly that.

??? question "Why can't I place a Frost Trap after my Explosive Trap?"
    All traps share a single **30 s** cooldown in Forever.

??? question "Does Hunter's Mark boost my pet?"
    Yes, according to Method, because pets scale from your attack power.

??? question "Why won't my shot fire?"
    You're inside the **8-yard deadzone**. Step back, Wing Clip, or Disengage.

??? question "Is Survival a melee spec now?"
    Mostly. It can melee-weave, or go full melee with Predator's Edge dual-wielding. It's weaker for questing than BM.

??? question "Can I tame the new Fox family?"
    Yes. Foxes have *Trickster's Dance* (dodge and attack speed for 12 s). Skyborne Hunters reportedly find foxes on Zephras Isle (*unconfirmed*).

**Common mistakes**

- Using Multi-Shot and expecting Aimed Shot to be ready: they share a cooldown.
- Leaving Growl on in groups.
- Forgetting to feed the pet: an Unhappy pet deals only 75% damage, a Happy one 125%.
- Running out of ammo or arrows mid-dungeon.
- Ignoring Intellect as MM; Careful Aim turns it into damage.

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
