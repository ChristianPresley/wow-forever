---
description: "Priest guide for WoW: Forever: specs and talents, rotations, a 1–60 leveling route, dungeons, raids, PvP, gear and Hardcore tips."
tags:
  - Priest
search:
  boost: 2
---

# Priest Guide

<div class="guide-head" data-class="priest" markdown>

:codex-priest:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Class guide</span> **Healer**{ .badge .heal } **DPS**{ .badge .dps }

<nav class="gh-jump" aria-label="Jump to section"><a href="#specs-talents">Talents</a> <a href="#abilities-rotation">Rotation</a> <a href="#leveling-walkthrough-160">Leveling</a> <a href="#dungeons">Dungeons</a> <a href="#raid-preparation">Raids</a> <a href="#pvp">PvP</a> <a href="#gear-stats-enchants">Gear</a> <a href="#hardcore-notes">Hardcore</a></nav>

</div>

!!! info "Current as of 7 November 2026"
    This guide uses the Blizzard Priest deep dive, the [Priest reference page](../../characters/classes/priest.md) and fan guides from launch week. Warcraft Tavern reports **class tuning on 10 November**. Thus the numbers can change. Fan sites published exact talent point orders only as images. When this guide gives a build, it lists the talents for each milestone, not a point-by-point order.

## Overview

The Priest is still the most flexible healer in Azeroth. It heals with heal-over-time spells, direct heals and absorb shields. The Shadow tree changes it into a full caster DPS. The design goals of Forever for the class are:

- **Every spec viable.** Discipline gets a real identity with shields, Penance and Divine Aegis. Holy gets Prayer of Mending and Holy Binding. Shadow is now an independent DPS spec, not only a source of a raid debuff.
- **Less race lottery.** **Fear Ward** and **Devouring Plague** are now baseline for every Priest at level 20. The race-locked spells that remain are smaller utility spells.
- **Less need for hit gear.** *Holy Precision* (Discipline) gives a maximum of 18% Holy hit, and *Shadow Focus* (Shadow) now gives Shadow hit.

<aside class="infobox" markdown>
<p class="infobox-title">Priest at a glance</p>

| | |
|---|---|
| **Roles** | Healer (Holy, Discipline), ranged caster DPS (Shadow) |
| **Armor / weapons** | Cloth. Wands and one-handed maces by default. Daggers and staves from weapon trainers |
| **Dual spec** | Level 40, 50g at the class trainer |

</aside>

<div class="proscons" markdown>
<div class="pros" markdown>

Strengths

- Best all-round healer
- Strong self-sustain when you level (Shield, Renew, Penance)
- Fear Ward and Mind Control utility
- Two healer specs

</div>
<div class="cons" markdown>

Weaknesses

- Cloth armor and few escapes
- Slow kills at low levels: in beta, Priest and Warrior were the **slowest classes to level**
- Uses much mana before talents and gear

</div>
</div>


### What's new in Forever

- **Baseline for all Priests:** Fear Ward and Devouring Plague (level 20), Divine Spirit (level 30), Shadow Word: Death (level 32).
- **Fade** removes two times more threat.
- **Prayer of Healing** heals the party of the *target*, not your party. In raids, you can now heal each group.
- **Renew** from different Priests stacks on the same target.
- **New gold talents** at the new 16-point tier and the 21/31 tiers: Soul Warding, Penance, Divine Aegis, Holy Binding, Prayer of Mending, a 30-second Vampiric Embrace and a reworked Shadowform.
- **Removed:** Lightwell, Improved Prayer of Healing, Unbreakable Will, Force of Will, Improved Vampiric Embrace. Shortly before launch, *Holy Binding* replaced **Binding Heal**.
- **Damage and healing over time** use the current stats of the caster at each tick, not the stats at the time of the cast (Warcraft Tavern). Early wands also give spell power.

### Races

6 races can be Priests. **Gnome is a new combination** in Forever.

| Faction | Race | Race-locked Priest spells | Add-on |
|---|---|---|---|
| **Alliance**{ .pill .pill--alliance } | Human | Divine Grace *(new)*, Feedback | [Human Priest](human.md) |
| **Alliance**{ .pill .pill--alliance } | Dwarf | Desperate Prayer, Chastise *(new)* | [Dwarf Priest](dwarf.md) |
| **Alliance**{ .pill .pill--alliance } | Gnome **(new)** | Confounding Flash *(new)*, Contingency Plan *(new)* | [Gnome Priest](gnome.md) |
| **Alliance**{ .pill .pill--alliance } | Night Elf | Starshards (buffed), Elune's Grace (redesigned) | [Night Elf Priest](night-elf.md) |
| **Horde**{ .pill .pill--horde } | Troll | Hex of Weakness, Shadowguard | [Troll Priest](troll.md) |
| **Horde**{ .pill .pill--horde } | Undead | Touch of Weakness, Dark Sacrifice *(new)* | [Undead Priest](undead.md) |

Skyborne, Orc and Tauren cannot be Priests. For all racial abilities, see [Races](../../characters/races.md).

---

## Specs & talents

Talents start at **level 10**, with one point for each level. At 60, you have 51 points. Gold single-point tiers are at **11, 16, 21 and 31 points** spent in a tree. Without Legacy bonuses, the milestones are:

<div class="milestones" markdown>

11
:   **Lv 20**{ .pts } Tier-3 talents (Mind Flay for Shadow, Holy Nova for Holy)

16
:   **Lv 25**{ .pts } Soul Warding · Holy Binding · Vampiric Embrace

21
:   **Lv 30**{ .pts } Penance (Discipline)

31
:   **Lv 40**{ .pts } Prayer of Mending · Shadowform

</div>

The Legacy talent **Talented** gives you your first point a maximum of 5 levels earlier. Thus each milestone above also comes earlier. See [Legacy](#professions-legacy).

=== "Discipline"

    **Identity:** shields, Penance and absorbs. Discipline is the strongest *solo* healer spec. With a wand, it is also a good spec for quests.

    | Talent | Notes |
    |---|---|
    | Power in Light *(new)* | Increases Smite and Penance damage against targets that have your Holy Fire |
    | Twin Disciplines *(new)* | Increases damage and healing of instant spells (Shield, Renew, SW:Pain, Holy Nova and others) |
    | Wand Specialization | Now only 2 points. Get it for leveling |
    | Silent Resolve | Also makes stuns, fears and silences on you shorter. It replaces Unbreakable Will |
    | Holy Precision | A maximum of 18% Holy hit. You do not need hit gear for Holy damage |
    | Improved Power Word: Shield | Larger shields |
    | Mental Agility | Row 3, 3 points. Now also applies to Smite and Holy Fire |
    | Meditation | Much stronger in-combat regeneration from Spirit |
    | Improved Inner Fire | More armor and more charges |
    | Mental Strength | Now a % Intellect bonus, not a % mana bonus |
    | **Soul Warding** (16) | Power Word: Shield costs less and has a shorter cooldown |
    | Renewed Hope | More crit on your direct heals and Penance on Weakened Soul targets. Each heal makes Weakened Soul shorter |
    | **Penance** (21) | 2 s channel, 12 s cooldown. Hits an enemy or heals an ally each second |
    | Divine Aegis | Critical heals give a 12 s absorb shield, based on the heal. Does not stack |
    | Improved Mana Burn | Faster Mana Burn |

    Warcraft Tavern says that Power Infusion is still deep in the Discipline tree. The Blizzard deep dive does not mention it (*unconfirmed*).

=== "Holy"

    **Identity:** throughput and group healing. Holy has Prayer of Mending, Holy Binding and Spirit of Redemption, and mana tools for long fights.

    | Talent | Notes |
    |---|---|
    | Twilight Focus | New name of Healing Focus. Pushback protection on **all** casts, 3 points |
    | Blessed Recovery | Also starts from each single hit of more than 30% of your health |
    | Inspiration | Starts from each non-periodic critical heal |
    | Improved Healing | Also decreases the cost of Penance and Prayer of Mending |
    | Searing Light (redesigned) | A smaller Holy damage bonus. Holy Fire can make your next Holy Nova free |
    | **Holy Binding** (16) | When your Flash Heals heal other players, they also heal you for 50% of that healing |
    | Litany of Light | Gives back part of the cost of a heal if it is different from your previous heal. This rewards you when you use different spells |
    | Spiritual Guidance | The spell damage share is now about one third of the healing share |
    | Spiritual Healing | Now 3 points |
    | Spirit of Redemption | Now lasts 15 s |
    | **Prayer of Mending** (31) | 10 s cooldown, 30 s duration. Heals on the next hit, then jumps a maximum of 5 times within 20 yards |

    !!! conflict "Conflict: Binding Heal vs. Holy Binding"
        The Blizzard deep dive describes **Binding Heal**, a 1.5 s spell that heals you and your target. In the launch kit, the passive **Holy Binding** above replaced it (see [Classes](../../characters/classes/index.md#changes-between-the-deep-dives-and-launch)). Some fan guides still show Binding Heal. Possibly the tooltip of Renewed Hope also still shows its name.

=== "Shadow"

    **Identity:** a DoT and Mind Flay caster that buffs itself. Shadow Weaving now buffs only **your own** Shadow damage. Thus you bring a Shadow Priest for its damage, not for a raid debuff.

    | Talent | Notes |
    |---|---|
    | Shadow Focus | Row 1. Now gives Shadow **hit** |
    | Shadow Reach | Row 2, 2 points. More range |
    | Improved Mind Flay | Row 3. More damage and range, weaker slow |
    | Mind Flay | Tier 3 (11 points, level 20) |
    | **Vampiric Embrace** (16) | Now a 30 s duration on a 1-minute cooldown. A short burst of self and party healing, not a permanent debuff |
    | Shadow Affinity | A little more threat reduction |
    | Silence / Improved Psychic Scream | Silence no longer needs Improved Psychic Scream. Improved Psychic Scream now needs Blackout |
    | Devouring Contagion | Row 5. Devouring Plague costs less. When the target dies, the Plague jumps to an enemy within 5 yards with its remaining duration |
    | Early Demise | Row 6. More SW:Death crit below 20% health |
    | Shadow Weaving | Only on yourself, with a smaller bonus |
    | **Shadowform** (31) | You can cast all spells that do not heal. Shadow spells cost **50% less** and get **+100% crit damage**. The flat damage bonus is lower |

    !!! conflict "Conflict: Shadowform"
        The Blizzard text gives Shadowform +100% Shadow **crit damage**. The Warcraft Tavern summary says Shadow crit **chance**. This guide uses the Blizzard text.

    Warcraft Tavern says that Vampiric Touch is not in the Forever kit.

### Recommended builds

!!! note "Builds are milestone lists"
    The fan sites published their trees as images, and their builds are different for each patch. The lists below give the **talents to have at each milestone**. Put the remaining points into the clear damage, mana or survival talents of the tree. After the 10 November tuning, check a talent calculator ([Mobalytics](https://mobalytics.gg/wow-forever/priest-talent-calculator) or [Zockify](https://www.zockify.com/forever/priest/)).

=== "Leveling (recommended)"

    Two routes are popular. Both work. Select a route by how frequently you play in a group.

    **A. Discipline → Shadow at 40** (Method)

    <div class="milestones" markdown>

    Lv 10–19
    :   Wand Specialization (2), Twin Disciplines, Improved Power Word: Shield, Silent Resolve or Holy Precision

    Lv 20–25
    :   Mental Agility, Meditation, Improved Inner Fire, then **Soul Warding** at 16 points

    Lv 25–30
    :   Mental Strength, Renewed Hope, then **Penance** at 21 points

    Lv 30–39
    :   Power in Light, Divine Aegis and the other talents that decrease mana cost

    Lv 40
    :   Buy dual spec. Make spec 2 **Shadow** for quests and keep Discipline for dungeons, or change fully to Shadow

    </div>

    Method says that this build uses mana efficiently and survives well. But its damage decreases in the middle and late 30s. For this reason, it changes to Shadow at 40.

    **B. Shadow from level 10** (Mobalytics, Warcraft Tavern)

    <div class="milestones" markdown>

    Lv 10–19
    :   Shadow Focus, Shadow Reach, Improved Shadow Word: Pain (if present), then Mind Flay at 11 points

    Lv 20–25
    :   Improved Mind Flay, then **Vampiric Embrace** at 16 points

    Lv 25–39
    :   Shadow Affinity, Silence, Devouring Contagion, Shadow Weaving, Early Demise

    Lv 40
    :   **Shadowform** at 31 points

    Lv 41–60
    :   Complete Shadow, then Discipline: Wand Specialization, Twin Disciplines, Improved Shield, Mental Agility, Meditation

    </div>

    Warcraft Tavern says that Shadow is not really strong before about level 28, when you have some spell power. Before that level, Disc is easier.

=== "Holy raid"

    The fan guides give about **20/31/0** or **19/32/0**. This is deep Holy for Prayer of Mending and Spirit of Redemption, with about 20 Discipline points for Mental Agility, Meditation, Mental Strength, Improved Shield and Soul Warding. These splits come from beta calculators (*unconfirmed for launch*).

    Necessary talents: Twilight Focus, Inspiration, Improved Healing, Holy Binding, Litany of Light, Spiritual Healing, Spiritual Guidance, Spirit of Redemption, **Prayer of Mending**.

=== "Discipline raid"

    About **31/20/0**: Penance, Divine Aegis and Renewed Hope, with about 20 Holy points for Twilight Focus, Inspiration, Improved Healing and **Holy Binding**. This is the strongest build for tank healing and single-target healing (*unconfirmed for launch*).

=== "Shadow raid / PvP"

    Go deep into Shadow for **Shadowform** (31+). Put the other points in Discipline for Mental Agility, Twin Disciplines, Improved Shield and Meditation. For PvP, think about Silence, Improved Psychic Scream and Silent Resolve, not only damage talents. Exact splits are not published yet.

### Dual spec at 40

At 40, you can buy a second spec for **50g** from a Priest trainer. You can change specs outside combat and outside battlegrounds. If you change talents in a spec, you pay a fee. This fee decreases to 1g over time.

The usual pair is **Shadow for quests + Holy or Discipline for dungeons**. At 40, you also want your 100g mount. Method recommends that you do not buy low-value spell ranks before 40, so that you have money for both.

---

## Abilities & rotation

### Key spells by level

Spell levels come from Warcraft Tavern and Method. This table does not show ranks.

| Level | New spells |
|---|---|
| 1 | Smite, Lesser Heal, Power Word: Fortitude |
| 4 | Shadow Word: Pain |
| 6 | Power Word: Shield |
| 8 | Renew, Fade |
| 10 | Mind Blast, Resurrection, **first race spell**, first class quest. Talents start |
| 12 | Inner Fire |
| 14 | Psychic Scream, Cure Disease |
| 16 | Heal |
| 18 | Dispel Magic |
| 20 | Flash Heal, Holy Fire, **Fear Ward**, **Devouring Plague**, Mind Soothe, Shackle Undead, **second race spell**, second class quest. The library-book quest becomes available |
| 22 | Mind Vision |
| 24 | Mana Burn |
| 30 | **Divine Spirit**, Prayer of Healing, Mind Control |
| 32 | **Shadow Word: Death**, Abolish Disease |
| 34 | Levitate |
| 35 | The library-book quest becomes available |
| 40 | Greater Heal, dual spec, Apprentice Riding |
| 45 | The library-book quest becomes available |
| 48 | Prayer of Fortitude |
| 56 | Prayer of Shadow Protection |
| 60 | Prayer of Spirit |

!!! conflict "Conflict: Shadow Word: Death backlash"
    The Blizzard deep dive says that SW:Death causes damage to you of **10%** of your maximum health if the target does not die. The pre-launch notes on the [Priest page](../../characters/classes/priest.md) say **30%**, and no backlash on a miss. Think of it as a large hit on yourself. Do not use it as a filler when your health is low.

### Rotations

=== "Shadow"


    !!! rotation "Shadow: Solo questing (Method, 40+)"

        <div class="priority" markdown>

        1. Cast **Power Word: Shield** on yourself before the pull.
        2. Start with **Mind Blast** (cast it before the mob gets to you).
        3. **Shadow Word: Pain**.
        4. **Shadow Word: Death** on cooldown, if your health is sufficient.
        5. **Mind Blast** on cooldown.
        6. **Mind Flay** as filler. Add **Devouring Plague** on strong or elite mobs.

        </div>


    **Single-target raid (general):** Keep SW:Pain and Devouring Plague active. Use Mind Blast on cooldown and Mind Flay as filler. Use SW:Death when you move or during execute (Early Demise). Only your own spells give Shadow Weaving stacks. Thus start to build them immediately.

    **Multiple targets:** Put SW:Pain on each target. With Devouring Contagion, put the Plague on the target that will die first, so that the Plague jumps.

    **Vampiric Embrace:** a 30 s window each minute. Use it on large pulls in dungeons or when the healer has problems.

=== "Discipline"

    **Solo questing (Warcraft Tavern):** Shield yourself when you have sufficient mana. Start with Smite or Holy Fire (Power in Light) and apply SW:Pain. Use **Penance on cooldown** (as damage, or as a self-heal). Then use your wand or let the DoT kill the mob.


    !!! rotation "Discipline: Healing"

        <div class="priority" markdown>

        1. **Power Word: Shield** on the player who will take damage next. With Soul Warding, this is your main spell.
        2. **Penance** on cooldown on the target with the most damage.
        3. Flash Heal / Greater Heal on Weakened Soul targets for Renewed Hope crits. Each crit gives **Divine Aegis**.
        4. Renew on a tank that you cannot shield.
        5. In a 5-player group, Prayer of Healing for group damage.

        </div>


=== "Holy"


    !!! rotation "Holy: Healing"

        <div class="priority" markdown>

        1. Keep **Prayer of Mending** active. Put it on the tank again every 10 s.
        2. **Renew** on targets that take constant damage. Renew from other Priests stacks.
        3. **Flash Heal** for fast single-target healing. Holy Binding heals you for half.
        4. **Heal / Greater Heal** for efficient large heals.
        5. **Prayer of Healing** on a member of the group that has damage.
        6. Use different spells in turn for **Litany of Light** refunds. Do not cast the same spell again and again.

        </div>


    **Solo:** The same as Discipline, but without Penance. Holy is the slowest spec for leveling.

### Cooldowns & utility

| Spell | Use |
|---|---|
| Fear Ward | Every Priest now has it. Put it on the tank before fear casts |
| Psychic Scream | Emergency escape. It can pull more mobs. Look at the area around you |
| Fade | Two times stronger. Use it after a large heal on a new pull |
| Shackle Undead | Crowd control in Scholomance, Stratholme and the [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) |
| Mind Control | In PvP, move enemies to dangerous positions. Also some dungeon tricks |
| Mana Burn | PvP only |
| Divine Spirit | Now baseline. Keep it on casters and healers |

### Macros

??? example "Show 3 macros"

    Mouseover healing (you do not need an add-on):

    ```
    #showtooltip
    /cast [@mouseover,help,nodead][help,nodead][@player] Flash Heal
    ```

    Shield yourself and keep your target:

    ```
    #showtooltip
    /cast [@player] Power Word: Shield
    ```

    Fear Ward on the focus (set the tank as focus):

    ```
    #showtooltip
    /cast [@focus,help][help][@player] Fear Ward
    ```

    !!! note
        This guide assumes that the modern `@` macro conditionals and focus targets work, as they do in the current Classic clients. The add-on and macro rules of Forever are on [Add-ons & UI](../../systems/addons.md).

---

## Leveling walkthrough 1–60

General advice:

- **Get a wand at level 5–13.** Until you have Penance or Shadowform, your wand is your main damage that uses no mana. See the wand list in the 10–20 section.
- **Shield, DoT, wand.** Before 30, most kills are Power Word: Shield → Shadow Word: Pain → Mind Blast → wand. DoTs tag a mob instantly. When other players also want the mob, start with SW:Pain.
- **Drink, do not rest.** Each time you go to a town, buy water for your level. Spirit gives mana regeneration outside the five-second rule.
- **Camping and rested XP:** A campfire with a Leatherworking Camp Tent gives rested XP. The Cozy Sleeping Bag scavenger hunt starts at level 14. See [Camping](../../systems/camping.md) and [Leveling](../../characters/leveling.md).
- **Quest XP is better than dungeon mob XP.** Do dungeons for their quests.

<div class="route" markdown>

### 1–10: starting zones

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Human: Northshire → Elwynn Forest | Troll: Valley of Trials → Durotar |
| Dwarf, Gnome: Coldridge Valley → Dun Morogh | Undead: Deathknell → Tirisfal Glades |
| Night Elf: Shadowglen → Teldrassil | |

- **Train:** Smite and Lesser Heal (1), SW:Pain (4), Power Word: Shield (6), Renew and Fade (8), Mind Blast (10).
- Do the quest chain of the starting zone and train at each level. At about level 5, get the camping quest *The Great Outdoors*.
- At **10**: you get your first race spell, your first class quest and your first talent point.
- Durotar, Teldrassil and Tirisfal have new quests and NPCs in Forever. Tirisfal now has **Shadowvale** and **Bandarion Keep** in its empty west area.

Each race add-on gives the steps for its starting zone.

### 10–20

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Westfall, Loch Modan, Darkshore | The Barrens, Silverpine Forest |
| Redridge Mountains (15+) | Stonetalon Mountains (15+) |

- **Train:** Inner Fire (12), Psychic Scream and Cure Disease (14), Heal (16), Dispel Magic (18).
- **Talents:** your first 10 points. If you start with Discipline, get Wand Specialization early.
- **Wands** (Method and Warcraft Tavern. The lists are different):

| Wand | Level | Source |
|---|---|---|
| Lesser Magic Wand | 5 | Enchanting (make it yourself or buy it) |
| Greater Magic Wand | 13 | Enchanting |
| Sizzle Stick | 15 | Wailing Caverns quest (Warcraft Tavern) |
| Gravestone Scepter | 18 | Blackfathom Deeps quest *Blackfathom Villainy* |
| Charred Wand | 19 | Hillsbrad quest *Dangerous!* (Method) |

- **Dungeons:** [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) (Ironforge, 13–20), Ragefire Chasm (13–19), [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) (Tirisfal, 15–22), The Deadmines and Wailing Caverns (17–25).
- **Library books:** Start to collect class library books now. When you turn in 10 books, a quest becomes available at level 20. This wiki does not show the locations yet.

### 20–30

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Wetlands, Duskwood, Ashenvale, Redridge | Hillsbrad Foothills, Ashenvale, Stonetalon, Thousand Needles (25+) |

- **Train at 20:** Flash Heal, Holy Fire, **Fear Ward**, **Devouring Plague**, Shackle Undead, Mind Soothe. This training costs much money. Save money for it.
- **At 20:** You get your second race spell, the second class quest, and the first library-book quest (10 books).
- **Talents:** 11 points give access to tier 3 (Mind Flay for Shadow). At **25**, you get to the 16-point gold tier: Soul Warding, Holy Binding or Vampiric Embrace.
- **Dungeons:** Shadowfang Keep, Blackfathom Deeps (Gravestone Scepter), the Stockade, and the new [Excavation Site: Wetlands](../../content/dungeons/excavation-site.md) (24–33).
- **Wands at 26–27:** *Dancing Flame* (Arathi quest *Final Passage*), *Wand of Eventide* (world drop), *Wand of Mana Concentration* (City of Dalaran quest *Arcanic Enigma*). *Unconfirmed: each has only one source.*

### 30–40

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Alterac Mountains (Dalaran), Arathi Highlands, Stranglethorn Vale, Desolace, Dustwallow (35+) | Arathi Highlands, Stranglethorn Vale, Desolace, Thousand Needles, Dustwallow (35+) |
| **Riverglades** (35+) from Farholde Keep | **Riverglades** (35+) from Rog'mar |

- **Train:** Divine Spirit, Prayer of Healing, Mind Control (30). **SW:Death** and Abolish Disease (32). Levitate (34).
- **Talents:** At 30, 21 points give **Penance** for Discipline.
- **At 35:** the second library-book quest (20 books in total).
- **Riverglades** is new and contested, and it is about the size of Stranglethorn. You can go there from Redridge, the Badlands, the Swamp of Sorrows, the Burning Steppes, or with the Tanaris ferry. See [Zones](../../world/zones.md#riverglades).
- **Dungeons:** [City of Dalaran](../../content/dungeons/city-of-dalaran.md) (28–35. In Dalaran, Horde players are attacked on sight), Razorfen Kraul, Gnomeregan, Scarlet Monastery wings, [The Drowned City](../../content/dungeons/drowned-city.md) (35–42).
- Desolace centaur quests now need level 35. [Shen'dralas](../../world/zones.md#shendralas) is on the other side of the Valley of Bones (level range unknown).

### 40–50

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Riverglades, Badlands, Swamp of Sorrows, Feralas, Tanaris, Hinterlands | Riverglades, Badlands, Swamp of Sorrows, Feralas, Tanaris, Hinterlands |
| Searing Gorge (43+), Azshara and Felwood (45+) | Searing Gorge (43+), Azshara and Felwood (45+) |

- **At 40:** Apprentice Riding and your first mount (100g), **dual spec** (50g), Greater Heal. Shadow gets **Shadowform**. Holy gets **Prayer of Mending**.
- **At 45:** the third library-book quest (25 books in total).
- **Train:** Prayer of Fortitude (48).
- **Dungeons:** [Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md) (Riverglades, 40–47), Scarlet Armory and Cathedral, Razorfen Downs, Uldaman, Zul'Farrak, [Alcaz Prison](../../content/dungeons/alcaz-prison.md) (48–55).

### 50–60

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Un'Goro (48+), Burning Steppes, Western Plaguelands, Azshara | Un'Goro (48+), Burning Steppes, Western Plaguelands, Azshara |
| Winterspring and Eastern Plaguelands (53+), Silithus (55+) | Winterspring and Eastern Plaguelands (53+), Silithus (55+) |

- **Train:** Prayer of Shadow Protection (56), Prayer of Spirit (60).
- **Azshara** has many new quests and the new [Blackmaw Hold](../../content/dungeons/blackmaw-hold.md) (55–60). The north of Un'Goro has [Shaper's Terrace](../../content/dungeons/shapers-terrace.md) (58–60).
- At 60, **Mount Hyjal** opens from Darkwhisper Gorge in Winterspring. Its 2 raids open on 9 December.
- The Legacy class tiers give points at 25, 45 and 60 for the first Priest on your account.

</div>

---

## Dungeons

Groups always want Priests. The [group finder](../../content/dungeons/index.md#general-rules) of Forever shows groups, but it does not teleport you. Meeting Stones do not summon.

**Healer tips**

- **Shield the tank before the pull.** Also put Renew on the tank before the pull. With Soul Warding, you can keep a shield on the tank almost all the time.
- **Fear Ward the tank** before bosses that fear. Every Priest has it now.
- **Fade is two times stronger.** If a large heal gets you aggro, use Fade and let the tank get the mob back.
- **Prayer of Healing heals the party of the target.** In a 5-player group, this is still your group.
- **Drink between pulls.** Tell the group when you have low mana.
- Method says that Shadow Priests can heal dungeons to 60 without a respec, but with worse mana efficiency. Dual spec at 40 makes this easier.

**Shadow tips**

- Shadow Affinity decreases your threat. But let the tank build threat before you cast Mind Blast.
- Vampiric Embrace heals the party during its 30 s window. Use it on large pulls.
- Silence and Psychic Scream are emergency interrupts and CC. Mobs that run from Scream can pull other packs.

**Notable dungeons**

| Level | Dungeon | Priest notes |
|---|---|---|
| 13–20 | [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) | New. First dungeon for Alliance Priests |
| 15–22 | [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) | New. Undead mobs give practice with Shackle. Drops the Fermenter and Arcane Salvager camp blueprints |
| 18–26 | Deadmines, Wailing Caverns | Classic. Sizzle Stick wand quest in WC |
| 24–33 | [Excavation Site: Wetlands](../../content/dungeons/excavation-site.md) | New |
| 25–32 | Blackfathom Deeps | Gravestone Scepter quest |
| 28–35 | [City of Dalaran](../../content/dungeons/city-of-dalaran.md) | New. Wand of Mana Concentration quest (*single source*) |
| 35–42 | [The Drowned City](../../content/dungeons/drowned-city.md) | New |
| 40–47 | [Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md) | New, in the Riverglades |
| 48–55 | [Alcaz Prison](../../content/dungeons/alcaz-prison.md) | New |
| 55–60 | [Blackmaw Hold](../../content/dungeons/blackmaw-hold.md) | New. Has a Barrow Deeps entrance |
| 58–60 | [Shaper's Terrace](../../content/dungeons/shapers-terrace.md), Scholomance, Stratholme | Shackle Undead is very important in Scholomance and Stratholme |

---

## Raid preparation

The launch raids open on **9 December 2026**: [The Barrow Deeps](../../content/raids/barrow-deeps.md) (10), [Hyjal Summit](../../content/raids/hyjal-summit.md) (20) and [Onyxia's Lair](../../content/raids/onyxias-lair.md) (40). Blizzard says that the difficulty comes from preparation, not from hundreds of attempts.

### Your role

| Raid | Healers | Priest focus |
|---|---|---|
| Barrow Deeps (10) | About 2–3 | Discipline or Holy on tanks. Each heal is important. Thus Penance and shields are strong |
| Hyjal Summit (20) | About 4–5 | Holy for raid healing (Prayer of Mending, Prayer of Healing on each group). Shadow is a valid DPS slot |
| Onyxia's Lair (40) | Many | **Fear Ward** the main tank before Bellowing Roar in phase 3 (Classic-era fight). Fire resistance helps |

The healer counts above are general guidance. They are not published numbers.

### Pre-raid gear approach

Nobody has published pre-raid lists for Forever. The dungeon items of Forever have unique stats with a theme. Thus the classic BiS lists do not apply. A practical approach:

1. Do the **new level-60 dungeons** ([Blackmaw Hold](../../content/dungeons/blackmaw-hold.md), [Shaper's Terrace](../../content/dungeons/shapers-terrace.md)) and the classic level-60 dungeons (Scholomance, Stratholme, Dire Maul, LBRS/UBRS). Reportedly, each boss in the new dungeons always drops a blue item.
2. Get each upgrade with **healing power** and **Intellect** (healer) or **hit and Shadow power** (Shadow). These are better than only Stamina.
3. Look at the PvP vendors. Honor buys blue and epic sets, and the new sets fill gaps for each spec.
4. Crafted gear: Tailoring has many new BoP patterns.
5. For Onyxia, start the **Drakefire Amulet** attunement early. It is not account-wide.

### Consumables

- Mana potions and the best water that you can buy or that a Mage can conjure.
- **Healing potions now come from First Aid**, not from Alchemy.
- Flasks and elixirs from Alchemy. Buff food from Cooking.
- Camp buffs work in the open world. They **do not stack** with the matching class buff. The First Aid Kit gives the same buff as Power Word: Fortitude, and the Tailoring Faction Banner gives the same buff as Divine Spirit.
- Dungeons and raids remove world buffs from the Chronoboon Displacer.

---

## PvP

In PvP, Priests are strong healers and casters that are difficult to fight. Fear Ward, Psychic Scream, Mana Burn, Mind Control and Dispel Magic are all important. Your race spell is frequently important too.

- **Battlegrounds:** Warsong Gulch (10v10), Arathi Basin (15v15), Alterac Valley (40v40) and the new **[Battle for the Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands)** (15v15, levels 30–60). Darkspear Islands has 4 bases and a central flag. As a healer, you can hold a base or shield the flag carrier. Both work well.
- **Healer play:** Stay at maximum range behind pillars and walls. Shield yourself when enemies attack you. Fade has no effect against players. Psychic Scream is your best escape. Dispel enemy buffs (Blessing of Freedom, Power Infusion and similar buffs).
- **Shadow play:** Use Silence, Psychic Scream and Mind Blast burst, then SW:Death to kill. Be careful of the SW:Death backlash.
- **Mind Control:** Move enemies off ledges or into your team. In Warsong Gulch, you can control the flag carrier.
- **Fear Ward yourself** against Warlocks and Warriors before you attack.
- **Progression:** Seasons reset ranks. Honor buys gear. You get Rank Points from battlegrounds and weekly tasks. See [PvP](../../content/pvp/index.md).

| Matchup | Notes (general guidance) |
|---|---|
| Warrior | Stay at a distance. Shield, Scream, wand or DoT. Fear Ward against Intimidating Shout |
| Rogue | Expect stuns. Keep Inner Fire active. Scream after the opener. Human, Dwarf and Undead racials help much here |
| Mage | Dispel Polymorph on allies. Mana Burn and Silence |
| Warlock | First Fear Ward, then Dispel and DoT. Undead Will of the Forsaken stops fear |
| Hunter | Go into the dead zone or out of range. Mana Burn their mana pool |
| Paladin | Mana Burn and Dispel. Long fights are better for them |
| Priest | Shadow wins with burst. Discipline wins long fights |

---

## Gear, stats & enchants

| Spec | Stat priority (Warcraft Tavern) |
|---|---|
| **Holy / Discipline** | Healing power > Intellect > MP5 > Spirit > Crit |
| **Shadow** | Hit (to cap) > Spell / Shadow power > Crit > Intellect > Spirit |
| **Leveling (any)** | Intellect and spell power > Stamina and Spirit > Armor |

- **Intellect** increases your mana pool and spell crit. Mental Strength now multiplies it.
- **Spirit** is more important when you level (out-of-combat regeneration), and for Holy/Discipline through Meditation. Shadow must not look for it.
- **Hit:** Holy Precision gives the Holy hit. Shadow Focus gives Shadow hit. Thus Shadow needs less hit gear. Nobody has published the exact cap.
- **Weapons:** wands until 60. Then a caster staff, or a mace or dagger with an off-hand.

**Enchants:** The Enchanting recipe list of Forever is not fully documented. Look for Intellect, healing or spell power, Spirit and Stamina enchants on chest, bracers, cloak and weapon. Enchanting also makes spell power oils for weapons (Warcraft Tavern).

---

## Professions & Legacy { #professions-legacy }

### Professions

The classic Priest pair is still the best, mostly because you can make your own wand.

<div class="prof-picks" markdown>

<div class="prof-pick prof-pick--best" markdown>

<p class="prof-rank" markdown>**S**{ .tier .tier-s } Best pick</p>

<p class="prof-pair" markdown>:material-needle: Tailoring <span class="prof-plus">+</span> :material-auto-fix: Enchanting</p>

<p class="prof-for">Best for: Every Priest</p>

<div class="pills" markdown>
**Leveling**{ .pill .pill--success .pill--sm } **Raids**{ .pill .pill--info .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
</dl>

- Cloth leveling gear and many new BoP patterns
- Your own wands (Lesser at 5, Greater at 13) and spell power oils
- Method recommends that you learn both at launch

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Faction Banner (Spirit) · Enchanted Lute (armor, stats, resists)</p>

</div>

<div class="prof-pick prof-pick--alt" markdown>

<p class="prof-rank" markdown>**A**{ .tier .tier-a } Strong alternative</p>

<p class="prof-pair" markdown>:material-leaf: Herbalism <span class="prof-plus">+</span> :material-flask: Alchemy</p>

<p class="prof-for">Best for: Raid nights</p>

<div class="pills" markdown>
**Raids**{ .pill .pill--info .pill--sm } **Gold**{ .pill .pill--gold .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:100%"><span>5/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
</dl>

- Mana potions, flasks and elixirs

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Incense Candle (Intellect) · Mana Well (mana regen)</p>

</div>

<div class="prof-pick prof-pick--sit" markdown>

<p class="prof-rank" markdown>**B**{ .tier .tier-b } Situational</p>

<p class="prof-pair" markdown>:material-leaf: Herbalism <span class="prof-plus">+</span> :material-knife: Skinning</p>

<p class="prof-for">Best for: Gold when you level</p>

<div class="pills" markdown>
**Leveling**{ .pill .pill--success .pill--sm } **Gold**{ .pill .pill--gold .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:20%"><span>1/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:20%"><span>1/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:100%"><span>5/5</span></span></dd>
</dl>

- Gold when you level, with the smallest interruption (Method)

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Incense Candle (Intellect) · Camp Chair (+2% crit)</p>

</div>

</div>

<p class="legend" markdown>Codex ratings out of 5, based on the sources above. Compare all classes in [Best professions by class](../../characters/professions.md#best-professions-by-class).</p>

<div class="pills" markdown>
**:material-medical-bag: First Aid · healing potions**{ .pill .pill--success } **:material-pot-steam: Cooking · campfires**{ .pill .pill--info } **:material-fish: Fishing · Fish Bowl**{ .pill .pill--info }
</div>

**Secondary skills.** Cooking (food buffs, campfires) and Fishing (crates, pearls). First Aid now makes healing potions. But Method rates bandages as low value for Priests.

!!! tip "Race notes"
    **Gnome:** fewer Engineering failures. But Engineering is not a top profession for Priests.

Crafting professions give [Legacy Points](../../characters/legacy.md) at skill 150, 225 and 300, and each profession adds a [camp feature](../../systems/camping.md). In Forever, professions give no passive stats.

### Legacy talents

You can spend a maximum of **16 points** on each character. Good choices for a Priest:

| Talent | Tree | Why |
|---|---|---|
| **Well Rested** → **Talented** | Adventure | Faster rested XP, then earlier talent points. Very helpful for a slow leveler |
| **Thrill of Adventure** | Adventure | Health and mana back on kills: you drink less |
| **Permanence** | Resourcefulness | Fortitude, Divine Spirit and Shadow Protection last longer |
| **Reagent Economy** | Resourcefulness | No reagents for Prayer of Fortitude, Prayer of Spirit or Prayer of Shadow Protection |
| **The Quick and the Dead** | Resourcefulness | Faster corpse runs |
| **Frequent Flier** | Adventure | Flights cost less and are faster |

See [Legacy System](../../characters/legacy.md).

---

## Hardcore notes

!!! hardcore "Hardcore survival"

    The [Hardcore](../../about/hardcore.md) ruleset comes this winter. Because of self-healing, Priests are one of the safer Hardcore classes. But they are slow and they have weak defenses.

    - **Always shield before the pull.** Most deaths start with a pull without a shield.
    - **Keep Psychic Scream for escapes.** Look around before you use it. Feared mobs can pull other mobs.
    - **Fear Ward yourself** in areas with mobs that fear.
    - **Do not use SW:Death** when your health is low.
    - **Know the emergency button of your race:** Desperate Prayer (Dwarf), Contingency Plan (Gnome), Divine Grace for a party member (Human), Elune's Grace (Night Elf), Rapid Regeneration (Troll), Will of the Forsaken (Undead).
    - Keep healing potions (First Aid) and bandages.
    - Dungeons give less mob XP. Make a group for quests, not for many dungeon runs one after the other.

---

## Common mistakes / FAQ

??? question "Which spec is best for leveling?"
    Shadow is the most usual answer, and the easiest after about level 28. Discipline is safer at low levels and better if you heal dungeons. Holy is the slowest solo. With dual spec at 40, you can keep a healer spec.

??? question "Do I need to be a specific race for Fear Ward now?"
    No. Fear Ward and Devouring Plague are baseline for every Priest at level 20.

??? question "Why doesn't my Prayer of Healing heal my own party?"
    In Forever, it heals the party of the **target**. Target a player in the group that you want to heal.

??? question "Is Shadow wanted in raids?"
    Shadow Weaving no longer buffs other players. Thus Shadow must get its raid spot with its damage. The lower costs and the doubled crit damage of Shadowform are there to make Shadow competitive. Early raid logs will show the result.

??? question "Can I DPS in Shadowform and still heal?"
    No. In Shadowform, you can cast all spells that do not heal.

??? question "Is Binding Heal in the game?"
    No. Before launch, the passive Holy Binding replaced it.

**Common mistakes**

- You do not get a wand before level 13.
- You start with Mind Blast in an area with many players, not with SW:Pain, which tags instantly.
- You forget the cost of water and training. Save money for level 20 and level 40.
- You use Prayer of Healing on your own party in a raid because of old habit.
- You do not collect library books until 20.

---

## Sources

??? quote "8 sources"

    - Blizzard, *Class Deep Dives — Priest and Warrior*: <https://news.blizzard.com/en-us/article/24301514/world-of-warcraft-forever-class-deep-dives-priest-and-warrior>
    - Warcraft Tavern, Priest guide: <https://www.warcrafttavern.com/forever/guides/priest/>
    - Warcraft Tavern, Priest leveling guide: <https://www.warcrafttavern.com/forever/guides/priest-leveling/>
    - Method, Priest leveling guide and talents: <https://www.method.gg/wow-forever/wow-forever-priest-leveling-guide-and-talents>
    - Mobalytics, Priest guides and talent calculator: <https://mobalytics.gg/wow-forever/priest-guides>, <https://mobalytics.gg/wow-forever/priest-talent-calculator>
    - Icy Veins, Holy and Discipline Priest guides: <https://www.icy-veins.com/wow-forever/holy-priest-healer-pve-guide>, <https://www.icy-veins.com/wow-forever/discipline-priest-healer-pve-guide>
    - Zockify, Priest talent calculator: <https://www.zockify.com/forever/priest/>
    - Wiki pages: [Priest](../../characters/classes/priest.md), [Races](../../characters/races.md), [Leveling](../../characters/leveling.md), [Legacy](../../characters/legacy.md), [Sources](../../sources.md)
