---
description: "Shaman guide for WoW: Forever: specs and talents, rotations, a 1–60 leveling route, dungeons, raids, PvP, gear and Hardcore tips."
tags:
  - Shaman
search:
  boost: 2
---

# Shaman Guide

<div class="guide-head" data-class="shaman" markdown>

:codex-shaman:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Class guide</span> **Healer**{ .badge .heal } **DPS**{ .badge .dps }

<nav class="gh-jump" aria-label="Jump to section"><a href="#specs-talents">Talents</a> <a href="#abilities-rotation">Rotation</a> <a href="#leveling-walkthrough-160">Leveling</a> <a href="#dungeons">Dungeons</a> <a href="#raid-preparation">Raids</a> <a href="#pvp">PvP</a> <a href="#gear-stats-enchants">Gear</a> <a href="#hardcore-notes">Hardcore</a></nav>

</div>

!!! info "Current as of 7 November 2026"
    Forever launched on 4 November. This guide uses the latest pre-launch notes (builds 70753 and 70755) and launch-week hotfixes. The talent builds and stat priorities come from the beta, and they will probably change. This is especially true after the **planned 10 November class tuning**. For reference data, see the [Shaman class page](../../characters/classes/shaman.md).

## Overview

The Shaman is a hybrid that can fill **any non-tank role**: ranged caster (Elemental), melee (Enhancement) or healer (Restoration). Your main tools are your **totems**: 4 elements, with one totem of each element at a time. Totems buff your group, heal it, cleanse it or hurt enemies.

<aside class="infobox" markdown>
<p class="infobox-title">Shaman at a glance</p>

| | |
|---|---|
| **Roles** | Ranged DPS, melee DPS, healer |
| **Armor** | **Leather**{ .pill .pill--leather }, then mail from level 40 (Classic rule, not confirmed again for Forever) |
| **Weapons** | Maces, staves, fist weapons, daggers, axes. **Two-handed axes and maces are now baseline** |
| **Resource** | **Mana**{ .pill .pill--mana } |
| **Races** | [Dwarf](dwarf.md) (Alliance, **new**), [Orc](orc.md), [Troll](troll.md), [Tauren](tauren.md), [Skyborne Windshaper](skyborne-windshaper.md) (Horde only, **new**) |

</aside>

<div class="proscons" markdown>
<div class="pros" markdown>

Strengths

- Party-wide buffs that every group wants: Windfury, Flametongue, Strength of Earth, Mana Spring and the resistance totems, which now cover the **whole raid**.
- Strong utility in PvP and dungeons: Purge, Grounding Totem, Tremor Totem, Earth Shock interrupts and Earthbind.
- Every spec can heal in an emergency. Reincarnation can save a group after a wipe.
- Enhancement levels quickly and solos well.

</div>
<div class="cons" markdown>

Weaknesses

- High mana use, especially for Elemental when you level.
- Totems do not move. In moving fights, you go away from your buffs, but Totemic Call (level 22) now brings them to you.
- No tank spec. Blizzard removed Shield Specialization.
- Totems need **totem items in your bags**. You get them from 4 class quests.

</div>
</div>

### What's new in Forever

- **Totems need much less work.** The totem GCD is **1.0 s** (was 1.5), and persistent totems last **5 minutes** (was 2). With the totem tracker, you can right-click a totem to destroy it.
- **Totem bar presets:** *Call of the Elements* (20), *Call of the Ancestors* (30) and *Call of the Spirits* (40) put down all 4 totems with one 3 s cast.
- **Totemic Recall** (20) refunds 25% of a totem's mana. **Totemic Call** (22) teleports your totems to you on a 30 s cooldown. Its name in the beta was Totemic Projection.
- **Fire Nova is now a spell** that bursts from your active Fire Totem. Fire Nova Totem is gone.
- Windfury and Flametongue Totem are party buffs, and Windfury adds an extra swing. **Totem twisting is gone**: Grace of Air no longer needs it, and Blizzard removed Tranquil Air Totem.
- **Imbues last 60 minutes** and stack with sharpening stones, weightstones and oils.
- Lightning Bolt and Chain Lightning cast faster. The top rank of Lightning Bolt does **+80%** damage. Chain Lightning is a 2.5 s cast again.
- Enhancing Totems, Weapon Mastery and Improved Weapon Totems are now **baseline**.
- **Removed:** Elemental Mastery (too strong in PvP), **Lava Burst** (removed shortly before launch), Tranquil Air Totem, Shield Specialization, Nature's Guidance.
- PvP gear has separate **healer, melee and caster** sets.
- **Alliance gets Shamans for the first time**, as Dwarves.

!!! warning "Planned 10 November tuning"
    Blizzard plans to make **Strength the strongest stat for Enhancement**. During launch week, Enhancement Shamans found that Intellect and spell power had more value than Strength and attack power. Until the change comes, keep all Strength and attack power gear that you find.

## Specs & talents

!!! tip "Full talent guide"
    The [Shaman talent guide](../../talents/shaman.md) gives a rating to each talent and a talent for each level from 10 to 60. Its tree data is from the launch client. If this section and the talent guide disagree, use the talent guide.

Talents start at **level 10** and give **51 points** by level 60. The single-point "gold medal" tiers are at **11, 16, 21 and 31** points. You change talents, and Legacy talents, at a class trainer in a major city. **Dual spec** unlocks at **level 40** for **50g** from your trainer. A talent change inside a spec still costs a respec fee. The fee for each spec decreases to 1g over time.

=== "Elemental"

    A ranged caster that uses Lightning Bolt and Chain Lightning as its main spells.

    <div class="milestones" markdown>

    Early
    :   Elemental Devastation, Elemental Alacrity, Improved Fire Nova, Eye of the Storm — Elemental Devastation moved up the tree

    16
    :   **Call of Thunder** — +5% crit (added in the launch build)

    —
    :   Elemental Reach — Range

    —
    :   **Lightning Overload** — 10/20/30% chance for a free extra bolt

    21
    :   **Earthbound** — Earthbind also roots for 5 s

    —
    :   Elemental Fury — Crit damage

    Tier 7
    :   **Lightning Mastery** — Takes Elemental Mastery's old slot. *What it does is unconfirmed*

    </div>

    Blizzard removed Elemental Mastery and the 31-point Lava Burst. The deep-dive capstone no longer exists.

=== "Enhancement"

    A melee hybrid that mixes weapon hits, shocks and instant spells.

    <div class="milestones" markdown>

    Early
    :   **Thundering Strikes** — Now a standalone first-row talent

    —
    :   **Ancestral Knowledge** — Now gives Intellect instead of mana

    —
    :   **Mental Dexterity** — 50/100/150% of Intellect as attack power

    —
    :   Improved Ghost Wolf — Usable indoors, then instant

    11
    :   **Shamanistic Focus**

    —
    :   Toughness — Now % Stamina

    —
    :   **Flurry** — 6–30% attack speed after a crit

    16
    :   **Stormstrike** — 150% weapon damage, 6 s cooldown. No longer the capstone

    21
    :   **Spirit Weapons**

    —
    :   Mental Quickness, Improved Stormstrike

    —
    :   **Maelstrom Weapon** — Works with **Lightning Bolt only** (Warcraft Tavern)

    31
    :   **Rage of the Farseer** — +30% attack speed for 25 s, 3 min cooldown. A self-only Bloodlust

    </div>

=== "Restoration"

    A healer with chain heals, shields and strong mana tools.

    <div class="milestones" markdown>

    Early
    :   Totemic Focus, **Mindfulness**, Natural Grace, Tidal Focus (reworked)

    —
    :   Improved Reincarnation

    11
    :   **Water Shield** — Mana return. Other specs also take it

    —
    :   Restorative Totems

    16
    :   **Mana Tide Totem** — Moved down from 31 points

    —
    :   Healing Way

    31
    :   **Riptide** — 12 s cooldown, 40% cheaper, a HoT with no upfront heal. Warcraft Tavern says Chain Heal also heals the Riptide target for 25% more (*unconfirmed*)

    </div>

### Recommended builds

No major source has published exact point-by-point builds for the launch talent trees yet. The splits below come from beta-era guides. Use them only as a starting point.

| Purpose | Elemental / Enhancement / Restoration | Source | Notes |
|---|---|---|---|
| Leveling to 30, Enhancement | 0 / 21 / 0 | Mobalytics | Straight to Spirit Weapons |
| Leveling to 30, Elemental | 21 / 0 / 0 | Mobalytics | Straight to Earthbound |
| Endgame Elemental | 31 / 9 / 11 | Warcraft Tavern | Takes Mindfulness and Water Shield for mana |
| Endgame Enhancement | 8 / 35 / 8 | Warcraft Tavern | Elemental Devastation, Mindfulness, Ancestral Knowledge 4/5 |
| Endgame Restoration | 0 / 10 / 41 | Warcraft Tavern | Thundering Strikes and Ancestral Knowledge only |

!!! conflict "Conflict"
    Warcraft Tavern made its builds before the **3 November** launch build. That build removed Lava Burst, added Call of Thunder and changed the name of Elemental Mastery to Lightning Mastery. Its Elemental build possibly still uses the old tree. Check the in-game talent pane before you spend points.

**Leveling milestones (general guidance)**

- **Enhancement:** fill Thundering Strikes and Ancestral Knowledge. Take Shamanistic Focus at 11 points, then Flurry. Take Stormstrike at 16 points (about level 25) and Spirit Weapons at 21. Then go deep for Maelstrom Weapon and Rage of the Farseer. Icy Veins says that these last talents need many points, so you get them late.
- **Elemental:** fill the damage and crit talents first. Take Call of Thunder at 16 points and Earthbound at 21 for safe kiting. Then take Lightning Overload. Expect to drink often until you have Water Shield or gear.
- **Restoration:** weak for solo leveling. Level as Enhancement or Elemental. At 40, add a Restoration spec with dual spec.

The **Legacy talent *Talented*** gives your first talent point earlier, as early as level 5 at 5/5. See [Professions & Legacy](#professions-legacy).

## Abilities & rotation

### Key spells by level

This list comes from Warcraft Tavern's milestone table. It does not include talents.

| Level | Spells |
|---|---|
| 1 | Rockbiter Weapon, Lightning Bolt |
| 4 | Earth Shock; **Stoneskin Totem** (Earth totem quest) |
| 6 | Earthbind Totem |
| 8 | Stoneclaw Totem, Lightning Shield |
| 10 | Flame Shock, Flametongue Weapon, Strength of Earth Totem; **Searing Totem** (Fire totem quest) |
| 12 | Fire Nova (spell), Purge, Ancestral Spirit |
| 16 | Cure Poison |
| 18 | Tremor Totem |
| 20 | **Call of the Elements**, Totemic Recall, Frost Shock, Frostbrand Weapon, **Ghost Wolf**, Lesser Healing Wave; **Healing Stream Totem** (Water totem quest) |
| 22 | **Totemic Call**, Cure Disease, Poison Cleansing Totem |
| 26 | Magma Totem, Mana Spring Totem |
| 30 | **Call of the Ancestors**, Grounding Totem, Windfury Weapon, Reincarnation |
| 32 | Chain Lightning, Windfury Totem |
| 40 | **Call of the Spirits**; dual spec |

For all classes, all abilities from 1 to 60 cost about **206–207g** to train. The game does **not** put new spells on your action bars automatically. Check your spellbook after each visit to the trainer.

### Rotations

=== "Elemental"

    !!! rotation "Elemental priority"

        <div class="priority" markdown>

        1. Put down totems with your Call preset: a Fire totem (Searing for single target, Magma for packs), **Mana Spring**, and the correct Earth and Air totems for the situation.
        2. Use **Flame Shock** if the target will live long enough.
        3. Use **Lightning Bolt** as your filler. Lightning Overload gives free extra bolts.
        4. Use **Chain Lightning** on 2 or more targets.
        5. Use **Earth Shock** to interrupt, or to kill a target that runs away. Shocks share a cooldown.
        6. Use **Fire Nova** on packs that are near your Fire Totem.

        </div>


    Use your racial (Blood Fury, Berserking, or Wind Blessed as a passive) with your opening bolts.

=== "Enhancement"

    !!! rotation "Enhancement priority"

        <div class="priority" markdown>

        1. Keep **Windfury Weapon** on your main hand (Rockbiter or Flametongue before level 30) and **Lightning Shield**. Use Water Shield instead if you have it and your mana is low.
        2. Put down Strength of Earth and Searing Totem. In groups, also put down Windfury Totem.
        3. Pull with a **Lightning Bolt**, or run to the target.
        4. Use **Stormstrike** on cooldown (6 s).
        5. Use **Flame Shock** on targets that live long. On other targets, use **Earth Shock** as a filler and interrupt.
        6. Spend **Maelstrom Weapon** stacks on Lightning Bolt.
        7. Keep **Rage of the Farseer** for elites, bosses and PvP bursts.

        </div>


=== "Restoration"

    !!! rotation "Restoration priority"

        <div class="priority" markdown>

        1. Keep **Water Shield** active. Put down **Mana Spring** or **Healing Stream**.
        2. Use **Riptide** on the tank, then **Chain Heal** on the tank for the bonus (if confirmed).
        3. Use **Lesser Healing Wave** for emergencies and **Healing Wave** (downranked) for efficiency.
        4. Use **Mana Tide Totem** when your mana is low in long fights.
        5. Use Poison Cleansing or Disease Cleansing Totem, or Cure spells, on the right fights.

        </div>


### Macros and keybinds

??? example "Show 3 macros"

    The Forever client has Midnight-style add-on restrictions (no WeakAuras, see [Add-ons & UI](../../systems/addons.md)), but usual macros work. Useful macros:

    ```text
    #showtooltip Earth Shock
    /stopcasting
    /cast Earth Shock
    ```

    Interrupts, also when you are casting.

    ```text
    #showtooltip Lesser Healing Wave
    /cast [@mouseover,help,nodead][] Lesser Healing Wave
    ```

    Mouseover healing for Restoration or emergency off-heals.

    ```text
    #showtooltip Stormstrike
    /cast Blood Fury
    /cast Stormstrike
    ```

    Burst for Orc Enhancement. For Trolls, use Berserking instead.

    **Keybind priorities:** your three Call presets, Totemic Call, Earth Shock, Purge, Grounding Totem, Tremor Totem, Earthbind Totem, and Ghost Wolf. With the 1.0 s totem GCD, it costs little to change one totem during a fight. Bind Grounding and Tremor to their own keys.

## Leveling walkthrough 1–60

!!! info "Zone ranges"
    The Forever client does not give level ranges to zones. The ranges below are Classic ranges or estimates from Forever sources. See [Zones](../../world/zones.md) and [Leveling](../../characters/leveling.md).

**General plan:** level as **Enhancement** (the most common recommendation) or Elemental. In Forever, quests give much more XP than dungeon mobs, and dungeon *quests* give a lot of XP. Solo, you need about 10–15 s to kill a normal mob. The developers say that levels 1–20 take about 20 hours.

<div class="route" markdown>

### 1–10: starting zone and the Earth totem

| Faction | Zones |
|---|---|
| **Alliance**{ .pill .pill--alliance } | Coldridge Valley → Kharanos (Dun Morogh). See [Dwarf](dwarf.md) |
| **Horde**{ .pill .pill--horde } | Valley of Trials → Razor Hill (Durotar) for [Orc](orc.md) and [Troll](troll.md). Camp Narache → Bloodhoof Village (Mulgore) for [Tauren](tauren.md). Zephras Isle for [Windshapers](skyborne-windshaper.md), who stay there until about 12 |

- **Spells:** Rockbiter Weapon, Lightning Bolt, Earth Shock (4), Earthbind (6), Stoneclaw and Lightning Shield (8).
- **Class quest, about level 4: *Call of Earth*.** Your first trainer sends you to an Earth Spirit and gives you Earth Sapta to drink. Then you defeat a Minor Manifestation of Earth. Reward: the **Earth Totem** and Stoneskin Totem.
- **Fighting style:** open with a Lightning Bolt. Use Earth Shock when the mob comes near, then melee with Rockbiter. Keep a Stoneclaw Totem for adds.
- **Level 10:** your first talent point, and the **Fire totem quest**.

### 10–20: Fire totem and the first dungeons

| Faction | Zones | Dungeons |
|---|---|---|
| **Alliance**{ .pill .pill--alliance } | Loch Modan, then Westfall or Darkshore (Stormwind Harbor now sails to Auberdine) | [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) (13–18), Deadmines (18–24) |
| **Horde**{ .pill .pill--horde } | The Barrens, Silverpine Forest | Ragefire Chasm (13–18), [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) (15–22), Wailing Caverns |

- **Class quest, level 10: *Call of Fire*.** A multi-step quest that gives the **Fire Totem** and Searing Totem at the end. Do it immediately. Searing Totem gives a large damage increase.
- **Spells:** Flame Shock, Flametongue Weapon, Strength of Earth (10). Fire Nova, Purge, Ancestral Spirit (12). Cure Poison (16). Tremor (18).
- **Talents:** Enhancement takes Shamanistic Focus at 11 points (around level 20 without Legacy).
- **Weapon:** a slow two-handed mace or axe does the most damage with Rockbiter and later with Windfury. Two-handed axes and maces no longer need training.

### 20–30: Water totem, Ghost Wolf, totem bar

| Faction | Zones | Dungeons |
|---|---|---|
| **Alliance**{ .pill .pill--alliance } | Wetlands, Redridge, Duskwood, Ashenvale | Deadmines, [Excavation Site](../../content/dungeons/excavation-site.md) (24–29), The Stockade, Blackfathom Deeps |
| **Horde**{ .pill .pill--horde } | Stonetalon, Hillsbrad Foothills, Ashenvale, Thousand Needles | Shadowfang Keep, Blackfathom Deeps |

- **Level 20 is the most important level:** Ghost Wolf, Call of the Elements, Totemic Recall, Frost Shock, Frostbrand Weapon and Lesser Healing Wave.
- **Class quest, level 20: *Call of Water*.** The longest totem quest. Warcraft Tavern says that the Alliance version needs about 2 hours of travel. Reward: the **Water Totem** and Healing Stream Totem.
- **Library books, level 20.** Every class can turn in library books: 10/20/25 books unlock quests at levels 20/35/45. Nobody has documented the Shaman rewards yet. Reports put the book quests at Garion Wendell (Wizard's Sanctum, Stormwind) and Owen Thadd (Magic Quarter, Undercity). It is *unconfirmed* if Shamans use those NPCs.
- **Level 22:** Totemic Call, Cure Disease and Poison Cleansing Totem. **Level 26:** Magma and Mana Spring Totem.
- **Talents:** Stormstrike at 16 points (Enhancement), Call of Thunder at 16 points (Elemental).
- **Dungeon:** the **[City of Dalaran](../../content/dungeons/city-of-dalaran.md)** (28–33) is Alliance-friendly. Horde players are attacked on sight in Dalaran.

### 30–40: Air totem and Windfury

| Faction | Zones | Dungeons |
|---|---|---|
| **Alliance**{ .pill .pill--alliance } | Arathi Highlands, Hillsbrad, Stranglethorn Vale, Desolace, **Riverglades** (35+, Farholde Keep) | Gnomeregan, Scarlet Monastery, Razorfen Kraul, [The Drowned City](../../content/dungeons/drowned-city.md) (35–40) |
| **Horde**{ .pill .pill--horde } | Arathi Highlands, Stranglethorn Vale, Desolace, **Riverglades** (35+, Rog'mar), Dustwallow Marsh | Razorfen Kraul, Scarlet Monastery, The Drowned City |

- **Level 30:** **Windfury Weapon**, Grounding Totem, Reincarnation and Call of the Ancestors. Enhancement damage increases a lot at this level.
- **Class quest, level 30: *Call of Air*.** New for this level range in Forever (Classic had no Air totem quest). Reward: the **Air Totem**. The quest also offers a **spec weapon**: *Rage of the Storm* (Enhancement), *Lightning's Grasp* (Elemental), *Tidebringer's Claw* (Restoration), or *Elementalist's Guard* for casters. The names come from Warcraft Tavern's beta guide.
- **Level 32:** Chain Lightning and Windfury Totem.
- **Desolace** centaur quests now need level 35. **Shen'dralas** (south of Desolace) has no confirmed level range.
- **Riverglades** is new and contested. It is about the size of Stranglethorn and has 150–200 quests. Its dungeon is [Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md) (40–45).
- **Library books at 35** unlock the second book quest.
- **Level 40:** mount (100g including your first racial mount), **dual spec** (50g), **Call of the Spirits**, and mail armor (Classic rule).

### 40–50

| Faction | Zones | Dungeons |
|---|---|---|
| **Alliance**{ .pill .pill--alliance } | Riverglades, Dustwallow Marsh (Theramore), Badlands, Swamp of Sorrows, Feralas, Hinterlands, Tanaris | Krol'dok Stronghold, Uldaman, Zul'Farrak, [Alcaz Prison](../../content/dungeons/alcaz-prison.md) (48–53) |
| **Horde**{ .pill .pill--horde } | Riverglades, Dustwallow Marsh, Badlands, Feralas, Hinterlands, Tanaris | Same |

- Tanaris has a new ferry from Steamwheedle Port to Powderfuse Port in Riverglades.
- **Library books at 45** unlock the third book quest.
- With dual spec, keep a **Restoration** spec for dungeons and a DPS spec for quests. Groups in the group finder always need healers. The group finder is a listing tool with no auto-matching.

### 50–60

| Faction | Zones | Dungeons |
|---|---|---|
| **Both**{ .pill .pill--neutral-faction } | Azshara (many new quests), Un'Goro Crater, Felwood, Burning Steppes, Searing Gorge, Western and Eastern Plaguelands, Winterspring, Silithus | [Blackmaw Hold](../../content/dungeons/blackmaw-hold.md) (55–60), [Shaper's Terrace](../../content/dungeons/shapers-terrace.md) (58–60), Sunken Temple, Blackrock Depths, Lower Blackrock Spire, Dire Maul, Scholomance, Stratholme |

- At 60, **[Mount Hyjal](../../world/zones.md#mount-hyjal)** opens through Darkwhisper Gorge in Winterspring. Both new raids are there.
- Epic riding is **1,000g** at level 60. There is no flying.
- The world-first level-60 group, about 3 days after launch, included a Shaman. The group used large AoE pulls.

</div>

## Dungeons

**Your job in a group:**

- **Totems are your main contribution.** Ask the group what they need. Melee groups need Windfury and Strength of Earth. Caster groups need Mana Spring and Flametongue.
- **Interrupt** with Earth Shock and **Purge** enemy buffs. Put down **Tremor** in fights with much fear, **Poison Cleansing** against spiders and snakes, and **Grounding** against dangerous casters.
- **Reincarnation** (30) lets you come back to life after a wipe and resurrect everyone. It needs an Ankh, unless you take the Legacy talent *Reagent Economy*.
- When the tank moves the pack, use **Totemic Call**. Then you do not have to cast your totems again.

| Level | Dungeon | Shaman notes |
|---|---|---|
| 13–18 | **[Hall of Thanes](../../content/dungeons/hall-of-thanes.md)** (Ironforge) | The natural first dungeon for Dwarf Shamans |
| 15–22 | **[Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md)** (Tirisfal) | Horde-side early option |
| 24–29 | **[Excavation Site](../../content/dungeons/excavation-site.md)** (Wetlands) | On the Alliance Water totem route |
| 28–33 | **[City of Dalaran](../../content/dungeons/city-of-dalaran.md)** | Hostile to Horde |
| 30–45 | Scarlet Monastery | Tremor Totem helps in the Cathedral and Library |
| 35–40 | **[The Drowned City](../../content/dungeons/drowned-city.md)** (Stranglethorn coast) | Naga and trolls |
| 40–45 | **[Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md)** (Riverglades) | |
| 48–53 | **[Alcaz Prison](../../content/dungeons/alcaz-prison.md)** (Dustwallow Marsh) | |
| 55–60 | **[Blackmaw Hold](../../content/dungeons/blackmaw-hold.md)** (Azshara) | |
| 58–60 | **[Shaper's Terrace](../../content/dungeons/shapers-terrace.md)** (Un'Goro) | |

See [Dungeons](../../content/dungeons/index.md) for the full list. Meeting Stones cannot summon, so go to the entrance.

## Raid preparation

All three launch raids open on **9 December 2026**. There are no difficulty modes. Blizzard says difficulty comes from **preparation**: gear, consumables and strategy. See [Raids](../../content/raids/index.md).

| Raid | Size | Shaman notes |
|---|---|---|
| **[The Barrow Deeps](../../content/raids/barrow-deeps.md)** | 10 | With few players, the totems of one Shaman can possibly cover most of the raid. Expect the raid to ask for your strongest buff totem |
| **[Hyjal Summit](../../content/raids/hyjal-summit.md)** | 20 | 13 bosses. Plan totems by group with your other Shamans |
| **[Onyxia's Lair](../../content/raids/onyxias-lair.md)** | 40 | Much fire damage. **Fire Resistance Totem now affects the whole raid**, so it is very valuable. Needs the Drakefire Amulet attunement |

**Pre-raid gear plan.** Forever loot is new and only partly documented, so there is no community best-in-slot list yet. Do these steps instead:

- Do the level-60 dungeons, especially the new ones. Each boss in a new dungeon reportedly drops a guaranteed blue item. Before 9 December, Upper Blackrock Spire (10-player) is the most similar thing to a raid.
- If you play PvP, collect the PvP set for your role (healer, melee or caster). You upgrade blue PvP pieces to get epic PvP pieces.
- Keep a fire-resistance set for Onyxia.

**Consumables (Classic-era guidance, not checked again for Forever):**

| Spec | Weapon | Elixirs and food | Other |
|---|---|---|---|
| Elemental | Brilliant Wizard Oil | Greater Arcane Elixir, spell-power food | Mana potions |
| Enhancement | Weightstone or sharpening stone, plus Windfury | Strength and agility elixirs | Mana potions, Juju items |
| Restoration | Brilliant Mana Oil | Mana regeneration elixirs | Mana potions, Dark Runes |

Because **imbues now stack with stones and oils**, you get both your imbue and an oil or stone. Crafted food also gives a small XP bonus when you level. The Legacy talent *Gourmand* makes food buffs last longer.

## PvP

See [PvP](../../content/pvp/index.md) and [Battlegrounds](../../content/pvp/battlegrounds.md).

- **Battlegrounds:** Warsong Gulch, Arathi Basin, Alterac Valley and the new **[Battle for the Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands)** (15v15, levels 30–60). Darkspear Islands has four bases and a central flag. Ghost Wolf and Earthbind make Shamans good flag escorts and base defenders.
- **Gear:** Shamans have three PvP sets: **healer, melee and caster**.
- **World PvP:** on PvP rulesets, you are almost always in danger. Earthbind with Earthbound (a 5 s root) and Ghost Wolf help you escape.

**Matchups**

| Enemy | Tips |
|---|---|
| Warlock | **Tremor Totem** against fear, **Grounding Totem** against Death Coil or Fear. Purge their buffs. Orc Shatter Curse removes curses and Banes |
| Mage | Grounding against Polymorph. Frost Shock to stop kiting. Interrupt with Earth Shock |
| Rogue | Stoneclaw Totem absorbs hits. Dwarf Stoneform removes bleeds and poisons |
| Warrior | Frost Shock and Earthbind to kite. As Elemental, do not fight in melee |
| Priest | Tremor against Psychic Scream. Purge their shields |
| Paladin | Purge their blessings. Holy Strike and Seal of Fury make them more dangerous than in Classic |
| Druid | Purge HoTs. Earth Shock their heals |
| Hunter | Use Ghost Wolf to move near them. Grounding absorbs one spell |

Enhancement does burst damage with Stormstrike and Rage of the Farseer. Elemental lost Elemental Mastery, so its burst is lower than in Classic. Restoration is a strong battleground healer with Riptide and Chain Heal.

## Gear, stats & enchants

Warcraft Tavern's stat priorities (beta, and the author expects them to change at level cap):

| Spec | Priority |
|---|---|
| **Elemental** | Hit (to the 17% spell cap) > Haste > Spell Penetration > Spell Power > Intellect > Crit |
| **Enhancement** | Weapon damage > Hit (at least 8%) > Intellect / Strength > Spell Penetration / Spell Power > Crit > Agility |
| **Restoration** | Healing Power > Intellect > Haste > MP5 > Spirit > Crit |

!!! conflict "Conflict"
    The Enhancement order above gives Intellect the same value as Strength. It also gives an expertise target (6.5%) that no other source mentions. Blizzard's **planned 10 November tuning** will make **Strength** the top Enhancement stat. Plan for Strength and attack power, with some Intellect.

- **Weapons:** a slow two-hander for Enhancement (Windfury is better with slow hits). A one-hand caster weapon with a shield or off-hand for Elemental and Restoration. The weapon from the Level 30 Air totem quest stays useful for a long time.
- **Armor:** leather until 40, then mail (Classic rule). Do not ignore good leather with the correct stats.
- **Enchants (Classic options):** Crusader or Strength for Enhancement weapons, spell power for Elemental, healing power for Restoration. Forever enchants are not fully documented.
- **Hit from talents:** several classes now get hit from talents. If you take hit talents, you need less hit from gear.

## Professions & Legacy { #professions-legacy }

<p class="divider">Professions</p>

Mana is the largest Shaman cost, but Enhancement and leveling Shamans also have good options.

<div class="prof-picks" markdown>

<div class="prof-pick prof-pick--best" markdown>

<p class="prof-rank" markdown>**S**{ .tier .tier-s } Best pick</p>

<p class="prof-pair" markdown>:material-leaf: Herbalism <span class="prof-plus">+</span> :material-flask: Alchemy</p>

<p class="prof-for">Best for: Elemental and Restoration</p>

<div class="pills" markdown>
**Raids**{ .pill .pill--info .pill--sm } **Gold**{ .pill .pill--gold .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:100%"><span>5/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
</dl>

- Mana potions and elixirs are your largest raid cost
- Tauren Cultivation adds bonus herbs

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Incense Candle (Intellect) · Mana Well (mana regen)</p>

</div>

<div class="prof-pick prof-pick--alt" markdown>

<p class="prof-rank" markdown>**A**{ .tier .tier-a } Strong alternative</p>

<p class="prof-pair" markdown>:material-pickaxe: Mining <span class="prof-plus">+</span> :material-anvil: Blacksmithing</p>

<p class="prof-for">Best for: Enhancement</p>

<div class="pills" markdown>
**Raids**{ .pill .pill--info .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
</dl>

- Sharpening stones and weightstones, which now stack with imbues

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Lodestone (melee AP) · Sharpening Wheel (Strength)</p>

</div>

<div class="prof-pick prof-pick--alt" markdown>

<p class="prof-rank" markdown>**A**{ .tier .tier-a } Strong alternative</p>

<p class="prof-pair" markdown>:material-knife: Skinning <span class="prof-plus">+</span> :material-bag-personal: Leatherworking</p>

<p class="prof-for">Best for: Leveling</p>

<div class="pills" markdown>
**Leveling**{ .pill .pill--success .pill--sm } **Gold**{ .pill .pill--gold .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
</dl>

- Leather and mail armor
- The Leatherworking Camp Tent stores rested XP

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Camp Chair (+2% crit) · Camp Tent (rested XP)</p>

</div>

<div class="prof-pick prof-pick--sit" markdown>

<p class="prof-rank" markdown>**B**{ .tier .tier-b } Situational</p>

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

- Best for PvP gadgets

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Lodestone (melee AP) · Reagent Bot</p>

</div>

</div>

<p class="legend" markdown>Codex ratings out of 5, based on the sources above. Compare every class in [Best professions by class](../../characters/professions.md#best-professions-by-class).</p>

A **pure gathering pair** (for example Herbalism + Mining) gives gold fastest when you level, so you can buy your 40 and 60 mounts sooner.

<div class="pills" markdown>
**:material-medical-bag: First Aid · healing potions**{ .pill .pill--success } **:material-pot-steam: Cooking · campfires**{ .pill .pill--info } **:material-fish: Fishing · Fish Bowl**{ .pill .pill--info }
</div>

**Secondary skills.** Cooking for campfires, First Aid for healing potions, Fishing for the Fish Bowl.

!!! tip "Race notes"
    **Tauren:** *Cultivation* adds herbs, which is good for the Herbalism + Alchemy pair.

Crafting professions award [Legacy Points](../../characters/legacy.md) at skill 150, 225 and 300. Each profession adds a [camp feature](../../systems/camping.md). Professions give no passive stats in Forever.

**Legacy talents.** Up to 16 points per character at launch.

| Talent | Why for a Shaman |
|---|---|
| **Well Rested** + **Talented** | Faster leveling and earlier talent points |
| **Thrill of Adventure** | Health and mana back on kills, so Elemental needs fewer breaks to drink |
| **Reagent Economy** | No vendor reagents: Reincarnation no longer needs an Ankh |
| **Permanence** | Long class buffs last longer. *Unconfirmed* whether imbues and shields count |
| **Frequent Flier** | Cheaper, faster flights. Useful for the long Water totem quest |
| **For Great Honor** | PvP players |

## Hardcore notes

!!! hardcore "Hardcore survival"

    The **Hardcore** ruleset arrives in winter 2026/27. There is no date yet. See [Hardcore](../../about/hardcore.md).

    - **Reincarnation** (30) is the obvious question. Nobody has **confirmed** how it works on Hardcore. Do not plan with it.
    - **Earthbind**, **Frost Shock** and **Ghost Wolf** (20) are your escape kit. Before a risky pull, make sure that Ghost Wolf is not on cooldown.
    - **Stoneclaw Totem** pulls an add to it for a few seconds when you run.
    - Keep **Lesser Healing Wave** ranks on a bar in every spec.
    - **Grounding Totem** stops one deadly spell, such as an elite caster's Polymorph or Fear.
    - The Fire totem quest for Dwarves sends you to groups of level-14 troggs. Pull carefully.
    - Hardcore Legacy points apply to other rulesets. Points from other rulesets do not apply to Hardcore.

## Common mistakes / FAQ

??? question "My totem spells are greyed out."
    You need the totem item for that element in your bags. Do the Earth (4), Fire (10), Water (20) and Air (30) totem quests.

??? question "Do I still need to twist totems?"
    No. Twisting is gone. Grace of Air works without it, and Windfury is a party buff that adds an extra swing.

??? question "Where is Lava Burst?"
    It was in the September deep dive as Elemental's 31-point talent. Blizzard removed it before launch. Older beta guides still list it.

??? question "Can Alliance play Shaman?"
    Yes, as **Dwarves only**. See [Dwarf Shaman](dwarf.md). Skyborne Shamans are Horde only.

??? question "Enhancement feels weak with Strength gear."
    In launch week, Intellect and spell power had more value. The 10 November tuning will possibly correct this. Keep Strength gear.

??? question "Elemental does not have enough mana when I level."
    Use downranked Lightning Bolts, Mana Spring, Water Shield when you have it, and the Legacy talent *Thrill of Adventure*. You can also level as Enhancement and change at 40 with dual spec.

??? question "My new spells are not on my bars."
    Forever does not add them automatically now. Drag them from your spellbook.

??? question "Why could I not create a Tauren Shaman at launch?"
    On launch night, Blizzard limited the creation of popular combos, including Tauren Shaman. Blizzard also locked Horde creation on PvP rulesets for some time because of faction imbalance.

## Sources

??? quote "13 sources"

    - [Warcraft Tavern: Shaman guide](https://www.warcrafttavern.com/forever/guides/shaman/)
    - [Warcraft Tavern: Shaman leveling guide](https://www.warcrafttavern.com/forever/guides/shaman-leveling/)
    - [Warcraft Tavern: Enhancement Shaman guide](https://www.warcrafttavern.com/forever/guides/enhancement-shaman/)
    - [Warcraft Tavern: Dwarf Shaman totem quests](https://www.warcrafttavern.com/forever/guides/dwarf-shaman-totem-quests/)
    - [Warcraft Tavern: Class trainer locations](https://www.warcrafttavern.com/forever/guides/class-trainers/)
    - [Warcraft Tavern: Dwarf race overview](https://www.warcrafttavern.com/forever/guides/dwarf/)
    - [Warcraft Tavern: Class tuning coming for Shamans, Warlocks and Hunter pets](https://www.warcrafttavern.com/forever/news/class-tuning-coming-for-shamans-warlocks-hunter-pets-in-wow-forever/)
    - [Warcraft Tavern: Mage & Shaman deep dive](https://www.warcrafttavern.com/forever/news/scrolls-totems-mage-shaman-deep-dive-for-wow-forever/)
    - [Warcraft Wiki: Shaman abilities (Forever)](https://warcraft.wiki.gg/wiki/Shaman_abilities_(Forever))
    - [Mobalytics: Shaman leveling guide](https://mobalytics.gg/wow-forever/classes/shaman-leveling-guide)
    - [Mobalytics: Elemental Shaman leveling guide](https://mobalytics.gg/wow-forever/classes/elemental-shaman-leveling-guide)
    - [Icy Veins: Enhancement Shaman leveling](https://www.icy-veins.com/wow-forever/enhancement-shaman-leveling)
    - [Method: Shaman leveling guide and talents](https://www.method.gg/wow-forever/wow-forever-shaman-leveling-guide-and-talents)
