---
description: "Rogue guide for WoW: Forever: specs and talents, rotations, a 1–60 leveling route, dungeons, raids, PvP, gear and Hardcore tips."
tags:
  - Rogue
search:
  boost: 2
---

# Rogue Guide

<div class="guide-head" data-class="rogue" markdown>

:codex-rogue:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Class guide</span> **DPS**{ .badge .dps } <span class="gh-diff" title="Method: one of the most approachable classes">Leveling difficulty: <strong>Easy</strong><span class="gh-pips" data-level="1" aria-hidden="true"><i></i></span></span>

<nav class="gh-jump" aria-label="Jump to section"><a href="#specs-talents">Talents</a> <a href="#abilities-rotation">Rotation</a> <a href="#leveling-walkthrough-160">Leveling</a> <a href="#dungeons">Dungeons</a> <a href="#raid-preparation">Raids</a> <a href="#pvp">PvP</a> <a href="#gear-stats-enchants">Gear</a> <a href="#hardcore-notes">Hardcore</a></nav>

</div>

!!! info "Current as of 7 November 2026"
    Forever launched on 4 November. This guide uses Blizzard's class deep dive (7 Oct), the pre-launch notes of 2–3 November and launch-week guides. The pre-launch notes changed the Rogue talents and added **Shank**, **Poised** and **Death Mark**. Warcraft Tavern points to a class-tuning pass on **10 November**, so expect the numbers to change. The reference data is on the [Rogue class page](../../characters/classes/rogue.md).

## Overview

The Rogue is a pure melee damage dealer that wears leather and uses **Energy** and **combo points**. You build points with attacks, then spend them on finishers. Stealth, stuns, Sap and Vanish give you more control over when and where a fight starts than any other class.

<aside class="infobox" markdown>
<p class="infobox-title">Rogue at a glance</p>

| | |
|---|---|
| **Role** | Melee DPS only |
| **Armor / weapons** | Leather; daggers, swords, maces, fist weapons, **one-handed axes (new)**, thrown, bows, crossbows, guns |
| **Resource** | **Energy**{ .pill .pill--energy } (now regenerates smoothly) + 5 combo points |

</aside>

<div class="proscons" markdown>
<div class="pros" markdown>

Strengths

- Top-tier single-target damage
- Best opener control in the game
- Strong solo survival through Stealth
- Vanish and Evasion
- Excellent world PvP

</div>
<div class="cons" markdown>

Weaknesses

- No healing
- No ranged pull besides throwing
- Weak multi-pull survival
- Gear-hungry
- Competes with Warriors for gear

</div>
</div>


### What's new in Forever

- **Smooth Energy regeneration.** The old 2-second Energy tick is gone, so you no longer "tick-time" abilities.
- **Combo points stay on the original target** when you switch, so you can build on one mob and finish it later.
- **One-handed axes** are usable, and **Hack and Slash** replaces the four weapon specializations.
- **Poisons** have more charges, **stack with sharpening stones and weightstones**, and Deadly and Instant Poison get twice as much benefit from attack power.
- **Sap no longer breaks Stealth**, so you can Sap one mob and stay in Stealth.
- **Shank** (level 24): a cheap off-hand stab that *generates* Energy. **Poised** (level 18) makes your next Energy ability cheaper.
- New talents: **Mutilate**, **Venom**, **Flawless Execution**, **Hack and Slash**, **Dirty Deeds** (Garrote from the front), **Quietus**, **Cutthroat**, **Thousand Cuts** and **Death Mark**.
- Feint threat is doubled, Expose Armor equals 5 Sunder Armors, and Distract lowers enemy stealth detection for 10 s.

### Races

Rogue is open to every race except Tauren. Each combination has an add-on page:

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| [Human](human.md) | [Orc](orc.md) |
| [Dwarf](dwarf.md) | [Troll](troll.md) |
| [Gnome](gnome.md) | [Undead](undead.md) |
| [Night Elf](night-elf.md) | [Skyborne (Windshaper)](skyborne-windshaper.md) **New**{ .pill .pill--new .pill--sm } |
| [Skyborne (High Order)](skyborne-high-order.md) **New**{ .pill .pill--new .pill--sm } | |

Blizzard rebuilt the racials for Forever: every race has two actives and two passives, and the old weapon-skill racials are gone. See [Races](../../characters/races.md).

??? question "Which race is best?"
    All races are good choices. For Alliance PvP, guides recommend **Human** or **Gnome** (stun break, snare break). For Alliance PvE, they recommend **Night Elf** or **Human**. For Horde, they recommend **Orc** for PvE and PvP. **Undead** is still the Horde PvP favourite. The add-on pages rate every racial for a Rogue.

---

## Specs & talents

Talents start at level 10 and cap at 51 points. Single-point "gold medal" talents are at **11, 16 (new), 21 and 31** points. You respec at a class trainer in a major city. **Dual spec** unlocks at **level 40 for 50g**. Respec fees decrease to 1g again over time.

=== "Assassination"

    **Theme:** poisons, crits and finishers.

    <div class="milestones" markdown>

    Early
    :   **Malice** (crit, now also for poisons), Remorseless Attacks, **Murder** (now hits Giants)

    16 pts
    :   **Cold Blood** — guaranteed crit on the next ability

    Mid
    :   **Lethality** (2 points, +10/20% crit damage), Improved Poisons (chance not to use a charge), Vile Poisons, **Vigor** (row 5), Improved Expose Armor

    21 pts
    :   **Mutilate** — 60 Energy, strikes with both daggers for 90% weapon damage, awards 2 combo points, more damage vs poisoned targets

    Deep
    :   **Seal Fate** (crits add an extra combo point)

    31 pts
    :   **Venom** — +30% poison damage and +10% application chance

    </div>

    Mutilate needs a **dagger in both hands**.

=== "Combat"

    **Theme:** sustained melee, any weapon type, cleave.

    <div class="milestones" markdown>

    Early
    :   Improved Eviscerate, Puncturing Wounds, Deflection, **Precision** (now one of the talents that grants hit), Endurance

    11 pts
    :   Riposte

    16 pts
    :   **Flawless Execution** — Eviscerate costs less Energy (−15 on the class page, −10 in Blizzard's deep dive)

    Mid
    :   **Hack and Slash** (axes and swords: extra-attack chance; maces: armor ignore; daggers and fists: crit), Dual Wield Specialization, **Weapon Expertise**, **Blade Flurry**

    Deep
    :   **Aggression**, **Efficient Strikes**, Flash of Steel

    31 pts
    :   **Adrenaline Rush**

    </div>

=== "Subtlety"

    **Theme:** openers, bleeds, burst from Stealth.

    <div class="milestones" markdown>

    Early
    :   **Camouflage**, **Master of Deception** (3 points), Opportunity, **Setup**, Dirty Tricks, Initiative, **Improved Distract** (new)

    16 pts
    :   **Premeditation** (20 s cooldown)

    Mid
    :   Serrated Blades, **Dirty Deeds** (Garrote from any side), **Hemorrhage** (+15% Rupture and Garrote damage), Ghostly Strike, Preparation

    Deep
    :   **Quietus** (bonus damage below 35% health), **Cutthroat** (Backstab can let your next Ambush work outside Stealth)

    31 pts
    :   **Thousand Cuts** and/or **Death Mark** — see conflict box

    </div>

!!! conflict "Conflict: Thousand Cuts vs Death Mark"
    - Blizzard's 7 Oct deep dive lists **Thousand Cuts** as the 31-point capstone. Each Rupture tick makes your next Backstab or Hemorrhage cheaper, and this effect stacks.
    - The 3 Nov pre-launch notes add **Death Mark**. Our [class page](../../characters/classes/rogue.md) lists it as a new active (25 Energy, 10 s cooldown). Warcraft Tavern's Subtlety guide describes it as a mark that **stores part of your damage and detonates after 6 s**, and lists no cost. Mein MMO calls it a finisher.
    - Treat both as correct until the in-game tooltip gives the answer. Expect the 10 November tuning to change them.

!!! conflict "Conflict: Venom"
    Blizzard's deep dive calls Venom a **25-Energy finisher**. Warcraft Tavern's general and Combat guides describe it as a **passive triggered by Shank**. The [class page](../../characters/classes/rogue.md) gives the effect (+30% poison damage, +10% application) without naming the trigger.

### Removed talents

Dagger, Mace, Sword and Fist Weapon Specialization (merged into Hack and Slash), Sleight of Hand and Deadliness. The "Restless Blades" talent shown at BlizzCon is *unconfirmed* at launch.

### Leveling builds

When we wrote this guide, the talent calculators did not show the 3 Nov rework. Use these builds as milestone plans, not as exact point orders.

=== "Combat (recommended)"

    Method, Mobalytics and Warcraft Tavern say that this is the smoothest solo spec. Use a slow sword, axe or mace in the main hand. Use Sinister Strike.

    <div class="milestones" markdown>

    Lv 10–14
    :   **5 pts**{ .pts } Improved Sinister Strike or **Precision** first (fewer misses). Some builds start with 5/5 Malice in Assassination

    Lv 15–19
    :   **10 pts**{ .pts } Deflection, Improved Gouge or Lightning Reflexes

    Lv 20
    :   **11 pts**{ .pts } **Riposte**

    Lv 21–25
    :   **16 pts**{ .pts } **Flawless Execution**, Dual Wield Specialization

    Lv 26–30
    :   **21 pts**{ .pts } **Blade Flurry**, Weapon Expertise, Hack and Slash for your weapon type

    Lv 31–40
    :   **31 pts**{ .pts } Aggression, Efficient Strikes, **Adrenaline Rush** at 31 points (level 40)

    Lv 41–60
    :   **51 pts**{ .pts } Spend the remaining points in Assassination: Malice, Remorseless Attacks, Ruthlessness, Improved Slice and Dice, Lethality, **Cold Blood**

    </div>

=== "Assassination (daggers)"

    Method's plan: use Backstab with daggers until you get Mutilate, and do not depend on poisons early. Warcraft Tavern's build takes Malice and Remorseless Attacks at 10, Lethality at 20 and Cold Blood around 25.

    <div class="milestones" markdown>

    Lv 10–14
    :   **5 pts**{ .pts } Malice

    Lv 15–19
    :   **10 pts**{ .pts } Remorseless Attacks, Ruthlessness

    Lv 20–25
    :   **16 pts**{ .pts } Lethality, Murder, **Cold Blood**

    Lv 26–30
    :   **21 pts**{ .pts } Improved Poisons, Vigor, **Mutilate**

    Lv 31–40
    :   **31 pts**{ .pts } Seal Fate, Vile Poisons, **Venom**

    Lv 41–60
    :   **51 pts**{ .pts } Combat for Precision, Dual Wield Specialization, Puncturing Wounds or Lightning Reflexes

    </div>

    Warcraft Tavern lists Mutilate at level 40 in its build. Blizzard's tree puts it at 21 points (level 30). The difference is only how many points you spend in other talents first.

=== "Subtlety (groups)"

    Method recommends Subtlety in groups: Hemorrhage as the builder, Ambush via Ghostly Strike, Vanish and Preparation. This spec needs daggers. It is weaker solo because you rarely get a chance to move to a new position.

### Endgame builds (level 60)

No guide has published final 51-point splits for the live tree yet. These are the shapes that the major guides use as their target:

| Build | Shape | Core |
|---|---|---|
| **Combat Swords/Axes** (raid default) | Deep Combat + Assassination | Precision, Flawless Execution, Dual Wield Spec, Weapon Expertise, Hack and Slash, Blade Flurry, Aggression, Adrenaline Rush, Flash of Steel; Malice, Improved Slice and Dice, Ruthlessness, Lethality, Improved Expose Armor, Cold Blood |
| **Combat Daggers** | Deep Combat | Puncturing Wounds, 5/5 Opportunity, Ruthlessness 2/3 |
| **Assassination Mutilate** | Deep Assassination | Mutilate, Seal Fate, Venom, Vile and Improved Poisons; Combat for Precision |
| **Hybrid poison** (Warcraft Tavern) | Combat/Assassination | One point in Hack and Slash, 4/5 Vile Poisons, skips Adrenaline Rush |
| **Subtlety Ambush** | Deep Subtlety | Opportunity, Master of Deception, Camouflage, Improved Ambush, Ghostly Strike, Preparation, Efficient Strikes; Lethality |
| **Subtlety Bleed** | Deep Subtlety | Dirty Deeds, Initiative, Ghostly Strike to keep Garrote up, Preparation, Death Mark; Malice, Improved Slice and Dice, Ruthlessness |

Pre-launch tier lists put **Assassination** and **Combat** in the top damage tier. Icy Veins says that Subtlety can possibly become stronger than them. Nobody has tested this at level 60 in live raids yet.

**Dual spec at 40:** the usual pair is a raid or dungeon spec (Combat or Assassination) and a PvP spec (Subtlety or a Cold Blood/Seal Fate build). A spec change is free outside combat.

---

## Abilities & rotation

### Key abilities by level

The training levels below come from Classic, except where the table shows *Forever*. All ranks from 1 to 60 cost about **206g** in total to train.

| Level | Ability |
|---|---|
| 1 | Sinister Strike, Eviscerate, Stealth |
| 4 | Backstab, Pick Pocket |
| 6 | Gouge |
| 8 | Evasion |
| 10 | Slice and Dice, Sap, Sprint (talents start) |
| 12 | Kick |
| 14 | Garrote, Expose Armor |
| 16 | Feint, Lockpicking unlocks |
| 18 | Ambush · **Poised** *(Forever)* |
| 20 | Rupture · poison quest (see below) |
| 22 | Vanish, Distract |
| 24 | **Shank** *(Forever)* |
| 26 | Cheap Shot |
| 30 | Kidney Shot |
| 34 | Blind |
| 40 | Safe Fall · dual spec · riding |
| 44 | **Shank rank 2** *(Forever: 25 Energy back)* |

**Poisons** (Warcraft Tavern): Instant from the quest, Crippling at 20, Mind-numbing at 24, Deadly at 30, Wound at 32.

### Shank and Poised

- **Shank:** 5 Energy, 10 s cooldown, hits for 50% off-hand damage and **returns 15 Energy** (25 at rank 2). It is a net gain, so press it on cooldown in every spec. Some builds connect Venom or Flash of Steel to it.
- **Poised:** your next Energy ability costs 10 less. Use it on your most expensive ability (Mutilate, Ambush or Eviscerate).

### Rotations

=== "Combat"

    !!! rotation "Combat priority"

        <div class="priority" markdown>

        1. Open from Stealth with **Cheap Shot**, or walk up and **Sinister Strike**.
        2. Use **Slice and Dice** at 1–2 combo points. Keep it active.
        3. Sinister Strike to build, **Shank** on cooldown, **Riposte** after every parry.
        4. **Eviscerate** at 5 combo points (cheaper with Flawless Execution).
        5. **Blade Flurry** with two or more targets, **Adrenaline Rush** for burst.

        </div>


=== "Assassination"

    !!! rotation "Assassination priority"

        <div class="priority" markdown>

        1. Open with **Garrote** (if the mob lives long) or **Ambush**.
        2. Use **Mutilate** to build. Sinister Strike can add the last point to save Energy.
        3. **Slice and Dice**, then **Shank** on cooldown.
        4. Eviscerate at 4–5 combo points. On bosses, **Expose Armor** first if no Warrior applies Sunder.
        5. **Cold Blood** on a 5-point Eviscerate.

        </div>


=== "Subtlety"

    !!! rotation "Subtlety priority"

        <div class="priority" markdown>

        1. **Premeditation** + **Ambush** (or Garrote with Dirty Deeds).
        2. **Hemorrhage** to build, **Ghostly Strike** on cooldown, **Shank** on cooldown.
        3. **Slice and Dice**, then **Rupture** in long fights (Thousand Cuts uses its ticks).
        4. **Death Mark** for burst while Slice and Dice is up.
        5. For more burst: Gouge → Vanish → Ambush, then Preparation to reset.

        </div>


### Useful macros

??? example "Show 3 macros"

    ```text
    #showtooltip Ambush
    /cast Pick Pocket
    /cast Ambush
    ```

    This macro loots the target, then opens the fight. Because Sap no longer breaks Stealth, a Sap → Pick Pocket → Ambush chain on a separate mob is now usual.

    ```text
    #showtooltip Sap
    /cleartarget
    /targetenemy
    /cast Sap
    ```

    ```text
    #showtooltip Kick
    /cast [@focus,exists,harm] Kick; Kick
    ```

    !!! warning "Macros"
        Forever uses a modern client, so conditionals like `@focus` probably work. Blizzard has not published a list of macro restrictions for Forever.

---

## Leveling walkthrough 1–60

The developers say that 1–20 takes about 20 hours. Quests give much more XP than dungeon mobs. Do quests first, and go to dungeons for their quests. See [Leveling](../../characters/leveling.md) and [Zones](../../world/zones.md).

??? tip "General leveling habits"
    - Replace the starting dagger when you find a slow sword, mace or axe (Combat) or a fast dagger (Assassination/Subtlety).
    - Use **Pick Pocket** on all humanoids. The coins and lockboxes pay for training.
    - Eat between pulls. Thistle Tea (from the poison quest) is a big Energy refill for emergencies.
    - **Sap** the second mob in a pack, kill the first, then fight the Sapped one. Sap no longer breaks Stealth, so you can also Sap and walk past.
    - Use **First Aid** bandages. You have no other healing.
    - At 14, do the **Cozy Sleeping Bag** scavenger hunt. Use [camping](../../systems/camping.md) to get rested XP.

<div class="route" markdown>

### 1–10: Starting zones

| Faction | Zones |
|---|---|
| **Alliance**{ .pill .pill--alliance } | Elwynn Forest, Dun Morogh, Teldrassil, or Zephras Isle (Skyborne) |
| **Horde**{ .pill .pill--horde } | Durotar, Tirisfal Glades, or Zephras Isle (Skyborne) |

- Your race's add-on page describes the starting zone and trainers.
- At 10, train **Slice and Dice**, **Sap** and **Sprint**. Spend your first talent point.
- Method mentions a level-10 rogue weapon quest (*Blade of Cunning*). It is *unconfirmed* for every race.

### 10–20

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Westfall, Loch Modan, Darkshore, Redridge (from 15) | The Barrens, Silverpine Forest, Stonetalon Mountains (from 15) |

- **Dungeons:** [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) (13–18, Ironforge), Ragefire Chasm (13–19), [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) (15–22, Tirisfal), The Deadmines (18–24), Wailing Caverns (19–25).
- **Ambush at 18**, **Poised at 18**.
- **Level 20:** the **poison quest** (below), **Rupture**, 11 talent points (enough for Riposte or Cold Blood).
- **Library books:** keep all class books that you find. See the note at the end of this section.

### The poison quest (level 20)

Warcraft Tavern recommends that you wait until **22** (for Vanish and Distract) and have **80+ Lockpicking**.

=== "Alliance"

    <div class="steps" markdown>

    1. **Master Mathias Shaw**, SI:7 in Old Town, Stormwind: *Mathias and the Defias*.
    2. Agent Kearnen in Westfall: *Klaven's Tower*. Sneak into the tower and open Klaven Mortwake's chest. Turn in the quest to learn **Poisons** and the **Thistle Tea** recipe.
    3. *The Touch of Zanzil* cures the debuff from the chest (Anti-Venom also works).

    </div>

=== "Horde"

    <div class="steps" markdown>

    1. **Shenthul**, Cleft of Shadow, Orgrimmar: *The Shattered Salute*, then *Deep Cover*.
    2. Taskmaster Fizzule in the Barrens: *Mission: Possible But Not Probable*.
    3. Serge Hinott in Hillsbrad Foothills: *Hinott's Assistance*. Warcraft Tavern calls this side noticeably harder.

    </div>

Poison crafting skill increases by 1 for each poison that you make, up to 5× your level. You can buy reagents from **Shady Dealers** and other poison vendors. Any Rogue trainer teaches new recipes.

### 20–30

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Redridge, Duskwood, **Wetlands** (new quests), Ashenvale, Hillsbrad | Stonetalon Mountains, Ashenvale, Hillsbrad Foothills, Thousand Needles |

- **Dungeons:** Shadowfang Keep (20–30), [Excavation Site: Wetlands](../../content/dungeons/excavation-site.md) (24–33), The Stockade, Blackfathom Deeps, [City of Dalaran](../../content/dungeons/city-of-dalaran.md) (28–35, Alliance-friendly, and Horde players are attacked on sight in the city).
- **Shank at 24** — add it to your rotation immediately.
- **Vanish 22, Cheap Shot 26, Kidney Shot 30.** **Deadly Poison at 30.**
- **Legacy:** your first rogue to **level 25** earns the *Novice* Rogue Legacy point.
- **Dalaran (Alliance):** Kirin Tor quests start around 26 with Emissary Jacques in Southshore.

### 30–40

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Arathi Highlands, Alterac Mountains, Stranglethorn Vale, Desolace, Thousand Needles, Dustwallow from 35 | Arathi Highlands, Stranglethorn Vale, Desolace, Dustwallow Marsh |

- **Riverglades** opens at about **35**: Farholde Keep (Alliance), Rog'mar (Horde). It is contested, so expect world PvP.
- **Desolace** centaur quests now require level 35.
- **Dungeons:** Razorfen Kraul, Gnomeregan, Scarlet Monastery (Graveyard, Library, Armory), [The Drowned City](../../content/dungeons/drowned-city.md) (35–42, Stranglethorn coast).
- **Blind at 34.**
- **Level 40:** riding (100g including your first racial mount), **dual spec** (50g), Safe Fall, and the 31-point capstone in your main tree.

### 40–50

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| **Riverglades** (Farholde Keep), Badlands, Swamp of Sorrows, Tanaris, Feralas, The Hinterlands | **Riverglades** (Rog'mar), Badlands, Swamp of Sorrows, Tanaris, Feralas, The Hinterlands |

- Go to Riverglades through the new passes from Badlands or Swamp of Sorrows. You can also take the **Steamwheedle Port ferry** in Tanaris to Powderfuse Port.
- **Dungeons:** Razorfen Downs, SM Cathedral, [Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md) (40–47, Riverglades), Uldaman, Zul'Farrak, [Alcaz Prison](../../content/dungeons/alcaz-prison.md) (48–55, Dustwallow).
- **Shank rank 2 at 44.**
- **Legacy:** first rogue to **45** earns the *Experienced* point.

### 50–60

| Both factions |
|---|
| Searing Gorge, Burning Steppes, **Azshara** (many new quests), Un'Goro Crater, Felwood, Western and Eastern Plaguelands, Winterspring, Silithus |

- **Dungeons:** Maraudon, Sunken Temple, Blackrock Depths, [Blackmaw Hold](../../content/dungeons/blackmaw-hold.md) (55–60, Azshara), Lower Blackrock Spire, Dire Maul, [Shaper's Terrace](../../content/dungeons/shapers-terrace.md) (58–60, Un'Goro), Scholomance, Stratholme.
- Lockpicking is useful in Blackrock Depths and Dire Maul: you can open boxes and doors.
- At 60, go to [Mount Hyjal](../../world/zones.md#mount-hyjal) through Darkwhisper Gorge in Winterspring. The first rogue to **60** earns the *Master* Legacy point.

!!! conflict "Conflict: library-book quests"
    Our [Leveling page](../../characters/leveling.md) says that when you turn in **10/20/25** class books, you unlock quests at **20/35/45**. Warcraft Tavern's library guide lists three *Friend of the Library* turn-ins at levels **1/20/30** for the same book counts. The rewards are jewelry and off-hand items. You can turn in books one at a time to **Garion Wendell** (Mage Quarter, Stormwind) or **Owen Thadd** (Magic Quarter, Undercity). No Rogue-only book has been documented.

</div>

---

## Dungeons

Your job is damage, interrupts and crowd control. Do not pull threat from the tank.

- **Sap** is your CC in every dungeon with humanoids. Sap first, then let the tank pull. Because Sap no longer breaks Stealth, you can Sap and then stay hidden.
- Use **Kick** on casters. It is the fastest interrupt in the group. Gouge and Kidney Shot also stop casts.
- **Feint** has double threat in Forever. On bosses, use it before you need it.
- **Expose Armor** now equals 5 Sunders. Use it only if no Warrior stacks Sunder. Coordinate with your group.
- **Lockpicking** opens boxes for the group and some doors.
- Use **Pick Pocket** on elites before the pull to get extra coin.
- Blade Flurry is very good on two-target trash. Turn it off near Sapped or Polymorphed mobs.

| Level | Notable for rogues |
|---|---|
| 13–22 | [Hall of Thanes](../../content/dungeons/hall-of-thanes.md), [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md), Deadmines (Cruel Barb, Smite's Mighty Hammer) |
| 24–35 | [Excavation Site](../../content/dungeons/excavation-site.md), [City of Dalaran](../../content/dungeons/city-of-dalaran.md), Shadowfang Keep, Stockade |
| 35–47 | [The Drowned City](../../content/dungeons/drowned-city.md), Scarlet Monastery, [Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md) |
| 48–55 | [Alcaz Prison](../../content/dungeons/alcaz-prison.md), Zul'Farrak, Maraudon |
| 55–60 | [Blackmaw Hold](../../content/dungeons/blackmaw-hold.md), [Shaper's Terrace](../../content/dungeons/shapers-terrace.md), BRD, LBRS, UBRS, Dire Maul, Scholomance, Stratholme |

Items from the new dungeons have stats for a specific class and spec. Each boss in a new dungeon reportedly drops a guaranteed blue item. Players are still datamining the item details. Check [Dungeons](../../content/dungeons/index.md) for each page.

---

## Raid preparation

All three launch raids open on **9 December 2026**. See [Raids](../../content/raids/index.md).

| Raid | Size | Rogue notes |
|---|---|---|
| [The Barrow Deeps](../../content/raids/barrow-deeps.md) | 10 | Illidan's old prison. Many night-elf and Druid of the Claw enemies. Small raids need your interrupts and stuns on trash |
| [Hyjal Summit](../../content/raids/hyjal-summit.md) | 20 | 13 bosses with branching routes. Expect a lot of trash, where Blade Flurry is very strong |
| [Onyxia's Lair](../../content/raids/onyxias-lair.md) | 40 | Classic fight: stay behind her and watch for the tail and Deep Breath. Fire resistance helps. Attunement needs UBRS |

### Pre-raid checklist

- **Gear:** BiS lists are not final. Get the best blue dungeon gear, including the class-themed items from the new dungeons. Also get PvP blues from Honor. Give priority to **hit** until you do not miss often, then to agility and crit.
- **Weapons:** decide your spec first. Combat needs a slow main hand (sword, axe or mace, for your Hack and Slash pick). Assassination and Subtlety need daggers.
- **Poisons:** the usual setup is Instant on the main hand and Deadly on the off hand. Poisons now stack with stones, so also add a sharpening stone or weightstone.
- **Consumables:** Elixir of the Mongoose (if available), Thistle Tea, Free Action Potions, Healing Potions (now made by First Aid), agility food and buff scrolls. Fire Protection for Onyxia.
- **World buffs** only work in the open world. The Chronoboon Displacer removes them in instances.
- **Attunement:** start the Onyxia chain at 58–60 (Burning Steppes for Alliance, Badlands for Horde).

---

## PvP

Every other class prepares for fights against Rogues. See [PvP](../../content/pvp/index.md) and [Battlegrounds](../../content/pvp/battlegrounds.md).

| Battleground | Rogue job |
|---|---|
| Warsong Gulch (10v10) | Flag-carrier killer and defender. Sap the escort and Kidney Shot the carrier |
| Arathi Basin (15v15) | Sneak-cap undefended nodes. Sap a lone defender and click the flag |
| [Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands) (15v15, 30–60) | Same job as AB on four bases. Also intercept the central flag carrier |
| Alterac Valley (40v40) | Gank reinforcements and cap towers while hidden |

- **Sap no longer breaks Stealth**: Sap a defender, then walk past or prepare a full opener.
- **Distract** now decreases enemy stealth detection for 10 s. It also tells players that a Rogue is near.
- Watch for **Human Perception** and the new Legacy talent **High Alert**, which lets players see you a level earlier (not in battlegrounds).

### Matchups

| Opponent | Tips |
|---|---|
| Warrior | Kite with Crippling Poison. Keep Evasion and Gouge for when they have Rage |
| Mage | Open with Cheap Shot → Kidney Shot. Kick Polymorph or Frostbolt. Use a trinket or racial to escape Frost Nova |
| Priest | Mind-numbing Poison. Keep Vanish or Will of the Forsaken for Psychic Scream |
| Warlock | Open on the Warlock, not the pet. Kick Fear |
| Hunter | Move to them fast. Vanish out of Freezing Trap range |
| Paladin | Wound Poison on heals. Burst when Divine Shield is down. Forever Paladins can tank, so check their spec |
| Druid | Kick heals and Entangling Roots. Crippling Poison when they go into Cat or Travel form |
| Shaman | Continue to attack them through Grounding. Kick heals |
| Rogue | The Rogue who opens first usually wins. Use Detect and Distract to find them |

---

## Gear, stats & enchants

| Spec | Stat priority |
|---|---|
| Combat | Hit (until misses are rare) > Agility > Crit > Attack Power > Strength > Stamina |
| Assassination | Hit > Agility > Crit (Seal Fate, Lethality) > Attack Power |
| Subtlety | Agility > Crit > Hit > Attack Power |

!!! conflict "Conflict: crit or agility first"
    Warcraft Tavern's leveling guide puts **crit** first. Its general guide puts **agility and hit** first. In practice: get enough hit to stop most misses (several talents like Precision now give hit). After that, agility and crit have about the same value.

- Many talents grant hit in Forever, so you need less hit on gear than in Classic.
- **Weapon speed:** a slow main hand for Sinister Strike and Eviscerate builds. A fast off-hand for poison procs.
- **Enchants:** Agility on gloves, cloak and weapons where available. Crusader on weapons is still the classic choice. Nobody has fully documented Forever's enchant list yet.
- **When you loot an item, you unlock its transmog**, so continue to collect items when they are too low for you.

---

## Professions & Legacy

<p class="divider">Professions</p>

Rogues need leather armor and armor kits for PvE, or explosives for PvP.

<div class="prof-picks" markdown>

<div class="prof-pick prof-pick--best" markdown>

<p class="prof-rank" markdown>**S**{ .tier .tier-s } Best pick</p>

<p class="prof-pair" markdown>:material-knife: Skinning <span class="prof-plus">+</span> :material-bag-personal: Leatherworking</p>

<p class="prof-for">Best for: PvE and leveling</p>

<div class="pills" markdown>
**Leveling**{ .pill .pill--success .pill--sm } **Gold**{ .pill .pill--gold .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
</dl>

- The standard Rogue pair: leather armor and armor kits
- Many new BoP armor patterns

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Camp Chair (+2% crit) · Camp Tent (rested XP)</p>

</div>

<div class="prof-pick prof-pick--alt" markdown>

<p class="prof-rank" markdown>**A**{ .tier .tier-a } Strong alternative</p>

<p class="prof-pair" markdown>:material-cog: Engineering <span class="prof-plus">+</span> :material-pickaxe: Mining</p>

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

- Bombs, grenades and nets
- Best for Gnomes (fewer device failures)

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Reagent Bot · Lodestone (melee AP)</p>

</div>

<div class="prof-pick prof-pick--sit" markdown>

<p class="prof-rank" markdown>**B**{ .tier .tier-b } Situational</p>

<p class="prof-pair" markdown>:material-leaf: Herbalism <span class="prof-plus">+</span> :material-flask: Alchemy</p>

<p class="prof-for">Best for: Self-supplied consumables</p>

<div class="pills" markdown>
**Raids**{ .pill .pill--info .pill--sm } **PvP**{ .pill .pill--danger .pill--sm } **Gold**{ .pill .pill--gold .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
</dl>

- Gold, your own Agility elixirs and Free Action Potions

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Incense Candle (Intellect) · Mana Well (mana regen)</p>

</div>

</div>

<p class="legend" markdown>Codex ratings out of 5, based on the sources above. Compare every class in [Best professions by class](../../characters/professions.md#best-professions-by-class).</p>

**Leveling plan**

<div class="timeline" markdown>

- **Early** Skinning + Mining for gold when you level.
- **Later** Replace Mining with Blacksmithing or Leatherworking when you have enough gold (Method's plan).

</div>

<div class="pills" markdown>
**:material-medical-bag: First Aid · healing potions**{ .pill .pill--success } **:material-pot-steam: Cooking · campfires**{ .pill .pill--info } **:material-fish: Fishing · Fish Bowl**{ .pill .pill--info }
</div>

**Secondary skills.** First Aid (now also makes healing potions) is the most important for a class with no heals. Cooking and Fishing are also useful.

!!! tip "Race notes"
    **Gnome:** 20% fewer Engineering device failures.

Crafting professions award [Legacy Points](../../characters/legacy.md) at skill 150, 225 and 300. Each profession adds a [camp feature](../../systems/camping.md). Professions give no passive stats in Forever.

### Legacy talents for a Rogue

| Tree | Pick | Why |
|---|---|---|
| Adventure | **Well Rested** 5/5 → **Talented** | Faster leveling and earlier talent points on alts |
| Adventure | **High Alert** | See enemy rogues and druids a level earlier in world PvP |
| Adventure | **Field Medicine** 2/2 | Shorter bandage cooldown, important for a class with no heals |
| Resourcefulness | **Reagent Economy** | Class abilities need no vendor reagents — covers Blinding Powder for Blind and Flash Powder for Vanish (Classic-era reagents, *unconfirmed* for Forever) |
| Resourcefulness | **For Great Honor** | PvP-focused characters |
| Professions | **Bountiful Harvest** | If you take Skinning |

---

## Hardcore notes

!!! hardcore "Hardcore survival"

    Hardcore arrives in **winter 2026/27**. See [Hardcore](../../about/hardcore.md).

    - Rogues are among the safest Hardcore classes: **Vanish**, **Sprint**, **Evasion**, Gouge and Blind all reset bad pulls.
    - Always carry **Flash Powder** (Vanish) and **Blinding Powder**, unless you have Reagent Economy.
    - Never fight two mobs without Sap or Gouge on one.
    - Bandage between every risky pull and carry Healing Potions.
    - Use Stealth to go past content. Do not clear it. At low level, do not go into unknown caves in Stealth.
    - Dwarf **Stoneform** (cleanses poisons and bleeds) and Gnome **Escape Artist** are strong survival racials.
    - The [Legacy](../../characters/legacy.md) talents *Thrill of Adventure* and *Field Medicine* add sustain.

---

## Common mistakes & FAQ

??? question "Do I still need to time abilities around the Energy tick?"
    No. Energy regenerates smoothly in Forever.

??? question "I switched targets — did I lose my combo points?"
    No. They stay on the original target, and you can go back to it and kill it.

??? question "Why does Mutilate not work?"
    It needs a dagger in **both** hands.

??? question "Is Expose Armor useful?"
    Only if your group has no Warrior that stacks Sunder Armor. It now equals 5 Sunders, so it is a good option for groups without a Warrior.

??? question "Do poisons override my sharpening stone?"
    No. In Forever they stack.

??? question "Is Shank worth the GCD?"
    Yes. It costs 5 Energy and returns 15 (25 at rank 2), and some builds connect other effects to it.

??? question "Can I Sap and stay in Stealth?"
    Yes. This is new in Forever.

**Common mistakes**

- You use the starting dagger for too long as a Combat Rogue.
- You forget to apply poisons again after a long dungeon.
- You open on elites when you have no escape (Vanish and Sprint on cooldown).
- You let Slice and Dice expire.
- You skip Lockpicking, which is the Rogue's best way to make money.

---

## Sources

??? quote "14 sources"

    - [Blizzard: Class Deep Dives — Rogue and Warlock](https://worldofwarcraft.blizzard.com/news/24310968)
    - [Warcraft Tavern: Rogue Leveling Guide](https://www.warcrafttavern.com/forever/guides/rogue-leveling/)
    - [Warcraft Tavern: Rogue Guide](https://www.warcrafttavern.com/forever/guides/rogue/)
    - [Warcraft Tavern: Combat Rogue](https://www.warcrafttavern.com/forever/guides/combat-rogue/)
    - [Warcraft Tavern: Subtlety Rogue](https://www.warcrafttavern.com/forever/guides/subtlety-rogue/)
    - [Warcraft Tavern: Assassination Rogue](https://www.warcrafttavern.com/forever/guides/assassination-rogue/)
    - [Warcraft Tavern: Poisons](https://www.warcrafttavern.com/forever/guides/poisons/)
    - [Warcraft Tavern: Library Books](https://www.warcrafttavern.com/forever/guides/library-books/)
    - [Warcraft Tavern: Rogue & Warlock deep dive](https://www.warcrafttavern.com/forever/news/poison-pets-rogue-warlock-deep-dive-for-wow-forever/)
    - [Method: Rogue Leveling Guide & Talents](https://www.method.gg/wow-forever/wow-forever-rogue-leveling-guide-and-talents)
    - [Mobalytics: Rogue Leveling Guide](https://mobalytics.gg/wow-forever/classes/rogue-leveling-guide)
    - [Icy Veins: Will Rogues Sneak to the Top?](https://www.icy-veins.com/wow-forever/news/countdown-to-forever-3-will-rogues-sneak-to-the-top/)
    - [ExitLag: WoW Forever Rogue](https://www.exitlag.com/blog/wow-forever-rogue)
    - [Mein MMO: the comeback of the rogues](https://mein-mmo.de/en/while-the-shamans-of-wow-forever-barricade-their-discord-in-protest-i-celebrate-the-comeback-of-the-rogues,1595001/)
