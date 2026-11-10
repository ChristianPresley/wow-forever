---
description: "Warlock guide for WoW: Forever: specs and talents, rotations, a 1–60 leveling route, dungeons, raids, PvP, gear and Hardcore advice."
tags:
  - Warlock
search:
  boost: 2
---

# Warlock Guide

<div class="guide-head" data-class="warlock" markdown>

:codex-warlock:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Class guide</span> **DPS**{ .badge .dps } <span class="gh-diff" title="Guide: one of the easiest classes to level">Leveling difficulty: <strong>Easy</strong><span class="gh-pips" data-level="1" aria-hidden="true"><i></i></span></span>

<nav class="gh-jump" aria-label="Jump to section"><a href="#specs-talents">Talents</a> <a href="#abilities-rotation">Rotation</a> <a href="#leveling-walkthrough-160">Leveling</a> <a href="#dungeons">Dungeons</a> <a href="#raid-preparation">Raids</a> <a href="#pvp">PvP</a> <a href="#gear-stats-enchants">Gear</a> <a href="#hardcore-notes">Hardcore</a></nav>

</div>

!!! info "Current as of 7 November 2026"
    Forever launched on 4 November. This guide uses these sources:

    - The Blizzard Rogue & Warlock class deep dive (7 Oct 2026).
    - The Warcraft Tavern launch-week spec guides (1–3 Nov).
    - The Method.gg leveling guide (4 Nov).
    - The Blizzard class-tuning notice of 6 Nov.

    **A Warlock hotfix is scheduled for Tuesday 10 November** (see [Upcoming tuning](#upcoming-tuning)). Thus, the Affliction rotation advice and Voidwalker tanking will probably change. You can find reference data on the [Warlock class page](../../characters/classes/warlock.md).

## Overview

The Warlock is a ranged caster in cloth armor. It fights with damage-over-time spells, fire nukes and a summoned demon. It changes health into mana with **Life Tap** and heals itself with drains. It controls fights with Fear, Banish and its demons. In groups, it gives the only summon in the game, Healthstones, Soulstones and **Curse of the Elements**. In Forever, Curse of the Elements increases damage from all magic schools.

<aside class="infobox" markdown>
<p class="infobox-title">Warlock at a glance</p>

| | |
|---|---|
| **Role** | Ranged damage, crowd control, raid utility (curses, summons, stones) |
| **Armor / weapons** | Cloth. Daggers, wands, one-hand swords and staves |
| **Resource** | **Mana**{ .pill .pill--mana } (refilled from health with Life Tap) and **Soul Shards** |
| **Leveling speed** | Second fastest in the beta, after Hunter |

</aside>

<div class="proscons" markdown>
<div class="pros" markdown>

Strengths

- Very self-sufficient leveling
- Pet tanking
- Strong sustained damage
- Fear in PvP
- Unique group utility

</div>
<div class="cons" markdown>

Weaknesses

- Low armor
- DoTs are slow to reach full damage
- Soul Shard upkeep
- Weak mobility
- Melee-range AoE (Hellfire)

</div>
</div>


### What's new in Forever

- **Banes.** Curse of Agony and Curse of Doom are now *Bane of Agony* and *Bane of Doom*. You can keep **1 Bane per target**, separate from your 1 Curse. Thus, a Warlock now uses a Bane **plus** a raid curse. All effects on Curses also apply to Banes.
- **Curse of the Elements** increases damage taken from **all** magic schools. **Curse of Shadows is gone.**
- **DoTs can crit**. The game recalculates DoT damage on each tick. Warcraft Tavern says that DoTs do not snapshot buffs.
- **Firestone and Spellstone are weapon imbues.** They stack with Wizard Oil. Firestone adds Fire damage and crit. Spellstone adds Shadow damage and spell haste.
- **Life Tap scales with Spirit**, not Stamina.
- **Drain Soul** has a chance to give a shard on each tick. The chance increases on each tick until it is 100%.
- **Demon scaling:** demons scale from your stats and gear. Pre-launch notes give the bonus as **2 Health per point of your Stamina** (decreased from 7.5). Boss AoE does **half damage to demons** (Warcraft Tavern).
- **Pet command "Move"** replaces Stay.
- **Talents rebuilt:** the new capstones are *Wrack*, *Demonic Pact* and *Incinerate*. *Pandemic*, *Bane of Havoc*, *Demonic Brand*, *Decimation*, *Shadow and Flame* and other talents are also new. Forever removed about 17 old talents.
- **Training is cheaper**, because you must also buy **Grimoires** (demon abilities) from demon trainers.
- The Warcraft Tavern guides now use the name **Sayaad** (Succubus or Incubus) for the Succubus line.

### Races

| Race | Faction | Status | Add-on |
|---|---|---|---|
| Human | **Alliance**{ .pill .pill--alliance } | Classic | [Human Warlock](human.md) |
| Gnome | **Alliance**{ .pill .pill--alliance } | Classic | [Gnome Warlock](gnome.md) |
| Orc | **Horde**{ .pill .pill--horde } | Classic | [Orc Warlock](orc.md) |
| Troll | **Horde**{ .pill .pill--horde } | **New** | [Troll Warlock](troll.md) |
| Undead | **Horde**{ .pill .pill--horde } | Classic | [Undead Warlock](undead.md) |

!!! conflict "Conflict: best race"
    Method.gg ranks them Human (S), Orc (A), Undead and Gnome (B), Troll (C). Warcraft Tavern says that all 5 are close. It says that Human and Orc are strong in both PvE and PvP, Undead is a PvP choice and Troll is good against beasts. 1 beta-era guide puts all races within 1% DPS. Choose the faction and look that you want.

## Specs & talents

!!! tip "Full talent guide"
    The [Warlock talent guide](../../talents/warlock.md) gives a rating to each talent and a talent for each level from 10 to 60. Its tree data is from the launch client. If this section and the talent guide disagree, use the talent guide.

Talents start at level 10 (1 point per level, 51 at 60). Single-point **gold-medal** talents are at **11, 16, 21 and 31** points in a tree. If you put all points in 1 tree, you get them at about levels 20, 25, 30 and 40. The *Talented* [Legacy talent](../../characters/legacy.md) gives you your first point earlier. **Dual spec** unlocks at **level 40** for **50g** from all Warlock trainers. Respec fees decrease to 1g over time.

| Spec | Capstones (11 / 16 / 21 / 31) | Plays like |
|---|---|---|
| **Affliction** | — / Curse of Exhaustion / — / **Wrack** | DoTs plus a channeled filler. Best sustain, slow to reach full damage |
| **Demonology** | Demonic Sacrifice / Fel Domination / Soul Link / **Demonic Pact** | Sacrifice 1 demon, fight with another. Tankiest spec, pet-tank option |
| **Destruction** | — / Conflagrate / Bane of Havoc / **Incinerate** | Fire burst and cleave. Best AoE and dungeon damage |

=== "Affliction"

    | Talent | Ranks | What it does |
    |---|---|---|
    | Improved Life Tap | 2 | More mana from Life Tap. Moved to row 1 |
    | Suppression | 5 | Redesigned: up to **+5% spell hit** and −20% threat |
    | Improved Corruption | 5 | Faster Corruption cast, up to +10% damage |
    | Malediction | — | New: up to +5% periodic damage (*see note below*) |
    | Improved Drains | 3 | New: up to +20% from Drain Life, Drain Soul and Wrack |
    | Improved Bane of Agony | 2 | Decreased from 3 points |
    | Amplify Curse | 1 | Next Bane of Agony does 50% more damage |
    | Fel Concentration | 3 | Decreased from 5. Less pushback on drains, now also on Wrack |
    | **Pandemic** | 3 | New: DoT and drain crits do up to **+100%** extra crit damage |
    | Nightfall | 2 | Drain Life, Drain Soul and Wrack can make your next Shadow Bolt instant |
    | **Curse of Exhaustion** | 1 (16 pts) | −30% movement speed. Moved from row 5 |
    | Malevolence | 5 | New: up to +5% Shadow crit |
    | Siphon Life | 1 | DoT that heals you |
    | Soul Siphon | 3 | New: drains and Wrack get up to 12% for each other Affliction effect on the target (max 36%) |
    | Shadow Mastery | 5 | Shadow damage bonus, smaller than Classic |
    | **Wrack** | 1 (31 pts) | Channel: Shadow damage each second. Your other Shadow DoTs do **+10%** to the target for 6 s. Pre-launch notes give about 86 dps base at 60 |

    *Soul Harvest* is the new name of Improved Drain Soul. The BlizzCon demo used the name "Drain Hope" for the capstone. All later sources say **Wrack**.

    !!! warning "Malediction possibly moved"
        Read the tooltip before you spend points on Malediction. 1 launch-week guide says that the periodic-damage Malediction from the deep dive is possibly not in that slot now.

=== "Demonology"

    | Talent | Ranks | What it does |
    |---|---|---|
    | Unholy Power | 5 | Pet damage (smaller bonus than Classic). Moved to row 1 |
    | Improved Health Funnel | — | More healing, up to 100% less threat, usable at all demon health levels |
    | Improved Imp | 3 | Does not affect Blood Pact now |
    | Demonic Aegis | — | New: Demon Skin/Armor up to +30% |
    | Fel Vitality | 3 | New: pet health and mana up to +15%, **your mana** up to +15% |
    | Demonic Energies | 2 | New: pet heals for up to 15% of your spell damage. Life Tap gives it mana |
    | Master Summoner | 2 | Faster, cheaper summons. Necessary for Fel Domination |
    | **Demonic Sacrifice** | 1 (11 pts) | Sacrifice a demon for a **2-hour** buff: Imp = Shadow damage, Voidwalker = mana regen, Sayaad = Fire damage, Felhunter = health regen |
    | **Fel Domination** | 1 (16 pts) | Next summon is fast |
    | Demonic Embrace | 5 | Stamina. Does not decrease Spirit now |
    | Improved Sayaad | 3 | Only Warcraft Tavern lists it (*unconfirmed*) |
    | Decimation | — | New: Shadow Bolt or Searing Pain on a target below 35% makes your next Soul Fire faster (up to 40%) and shard-free for 10 s. Soul Fire cooldown decreased by up to 90% |
    | **Demonic Brand** | 3 | New: Searing Pain makes less threat and brands the target. The next 2 attacks of your pet do bonus Fire or Shadow damage. With a **Voidwalker**, this makes a lot of threat, so **pet tanking** is possible |
    | **Soul Link** | 1 (21 pts) | Your demon takes about 30% of the damage that you take. Moved from row 7 |
    | Improved Felhunter | — | New: stronger Felhunter abilities, Spell Lock −2 s cooldown |
    | Demonic Knowledge | 3 | New: when a demon is out, you and your pet get spell damage that scales with your level |
    | Master Demonologist | 5 | Redesigned: Imp = Fire damage, Voidwalker = less physical damage taken, Sayaad = Shadow damage, Felhunter = less magic damage taken |
    | **Demonic Pact** | 1 (31 pts) | Requires Soul Link. You **keep** your sacrifice buff when you summon a *different* demon |

    No Felguard: no Forever source mentions it.

=== "Destruction"

    | Talent | Ranks | What it does |
    |---|---|---|
    | Destructive Reach | — | Range for all damage spells. Moved to row 1 |
    | Bane | 5 | Faster Shadow Bolt, Immolate and now **Incinerate** |
    | Cataclysm | 3 | Up to −10% Destruction mana cost |
    | Molten Skin | 5 | New: up to −10% damage taken (2% per point, Warcraft Tavern) |
    | Improved Shadow Bolt | 5 | Only your own Shadow damage. No charges |
    | Aftermath | 5 | Redesigned: initial hit of Immolate up to +50%. Conflagrate can Daze (−50% speed, 5 s) |
    | Ruin | 5 | Crit damage. Moved to row 3 |
    | Agonizing Flames | 3 | Old name: Improved Searing Pain |
    | Intensity | 3 | Pushback resistance for all Destruction spells |
    | **Conflagrate** | 1 (16 pts) | Moved from row 7 |
    | Fire and Brimstone | 3 | New: Conflagrate crit |
    | **Bane of Havoc** | 1 (21 pts) | 5-minute Bane: the cursed target also takes **15% of the damage that you do to other targets** |
    | Shadow and Flame | 5 | New: Conflagrate gives a Shadow buff and Shadowburn gives a Fire buff (20 s). Conflagrate can keep Immolate. Shadowburn can give back its shard |
    | **Incinerate** | 1 (31 pts) | 2.5 s Fire nuke, 30 yd, **+25%** if Immolate is on the target |

### Removed talents

Improved Healthstone · Fel Intellect · Fel Stamina · Improved Subjugate Demon · Improved Firestone · Improved Spellstone · Improved Curse of Weakness · Improved Drain Life · Improved Drain Mana · Improved Curse of Exhaustion · Grim Reach · Dark Pact · Improved Firebolt · Improved Lash of Pain · Devastation · Improved Immolate · Emberstorm.

!!! conflict "Conflict: Grim Reach"
    The Blizzard deep dive lists Grim Reach as removed. But the Warcraft Tavern and Method.gg leveling guides still recommend it for PvP. Use the in-game tree as the correct data. If Grim Reach is not there, *Destructive Reach* (Destruction row 1) gives range.

### Leveling builds

All major guides recommend **Affliction** for leveling. Demonology is a close second, and Destruction is best in groups. These are the Warcraft Tavern orders. The Method.gg orders are different only in timing.

=== "Affliction (40/7/4)"

    <div class="milestones" markdown>

    Lv 10–19
    :   Improved Corruption 5/5, Suppression 5/5

    Lv 20–26
    :   Unholy Power 5/5, Demonic Energies 2/2 (Demonology, for a stronger pet)

    Lv 27–30
    :   Improved Drains 3/3, Amplify Curse

    Lv 31–40
    :   Improved Bane of Agony 2/2, Improved Life Tap 2/2, Pandemic 3/3, Soul Siphon 3/3

    Lv 41–60
    :   Malevolence 5/5, Shadow Mastery 5/5, Siphon Life, Fel Concentration 3/3, Nightfall 2/2, Improved Shadow Bolt 4/5

    </div>

    If mobs interrupt your drains frequently, take Fel Concentration earlier. The Voidwalker tanks until 20, then the Sayaad. Drain-tanking with Drain Life starts at about 30.

=== "Demonology (20/31/0)"

    Level as Affliction to 27, then respec:

    <div class="milestones" markdown>

    Lv 27 (respec, 18 pts)
    :   Unholy Power 5, Demonic Energies 2, Fel Vitality 3, Master Summoner 2, Improved Sayaad 3, Demonic Brand 3

    Lv 28–40
    :   Demonic Sacrifice, Soul Link, Demonic Knowledge 3/3, Demonic Embrace 1/5, Fel Domination, Master Demonologist 5/5, **Demonic Pact** at 40

    Lv 41–60
    :   Affliction: Improved Corruption 5, Improved Life Tap 2, Suppression 5, Improved Drains 3, Pandemic 3, Malevolence 2

    </div>

    You can also put all points in Demonology from 10. Method.gg stays Affliction until about level 45.

=== "Destruction (17/3/31)"

    <div class="milestones" markdown>

    Lv 10–20
    :   Bane 5/5, Cataclysm 3/3, Aftermath 2/5, Shadowburn at 20

    Lv 21–25
    :   Aftermath 5/5, Ruin 1/5, **Conflagrate** at 25

    Lv 26–30
    :   Ruin 3/5, Agonizing Flames 3/3

    Lv 31–40
    :   Bane of Havoc, Fire and Brimstone 3/3, Shadow and Flame 5/5, **Incinerate** at 40

    Lv 41–60
    :   Suppression 5/5, Improved Life Tap 2/2, Improved Corruption 5/5, Improved Imp 3/3, Amplify Curse, Pandemic 3/3, Malevolence 1/5

    </div>

    Method.gg lists Shadowburn at 24 and Conflagrate at 29. This is a different build order, not a different rule.

### Endgame builds (level 60)

From the Warcraft Tavern spec guides (1–3 Nov). No raid is open yet, so these are pre-raid simulations.

| Spec | Build | Split (A/D/D) | Notes |
|---|---|---|---|
| Affliction | **Wrack** | 33 / 0 / 18 | Wrack is the filler, with Soul Siphon 3/3. Shadow Bolt only on Nightfall procs |
| Affliction | SM/Ruin | 30 / 0 / 21 | Shadow Bolt filler. Slightly lower than Wrack. The dungeon choice (move the third Cataclysm point into Shadowburn) |
| Demonology | Fire | 2 / 31 / 18 | Sacrifice the Sayaad, keep the Imp out. Searing Pain filler, Soul Fire execute, Firestone |
| Demonology | Shadow | 2 / 31 / 18 | Sacrifice the Imp, keep the Sayaad out. Shadow Bolt filler, Spellstone. Within ~3% of Fire |
| Destruction | Sayaad | 14 / 4 / 33 | Keep the Sayaad summoned. Best Destruction build |
| Destruction | Imp | 14 / 4 / 33 | Moves points from Aftermath and Unholy Power into Improved Imp and Demonic Energies. Slightly lower |
| Destruction | Sacrifice | 7 / 11 / 33 | Sacrifice the Sayaad for +15% Fire. Lower than the Sayaad build |

!!! note "Affliction is about to change"
    On 6 Nov, Blizzard said that it is better to only channel Wrack than to keep Siphon Life, Corruption and Bane of Agony active. Blizzard will make those DoTs worth a cast with Wrack. The total Affliction damage will not increase. The Wrack build priority will probably change after 10 Nov.

## Abilities & rotation

### Key spells by level

The levels below come from Method.gg and Warcraft Tavern for Forever. The levels marked *(Classic)* are from Classic, and nobody has checked them against Forever.

| Level | Spells |
|---|---|
| 1 | Shadow Bolt, Demon Skin, Immolate, Summon Imp (quest) |
| 4 | Corruption, Curse of Weakness; **Blood Pact** grimoire from the demon trainer |
| 6 | Life Tap |
| 8 | Bane of Agony; Fear *(Classic)* |
| 10 | Drain Soul, Create Healthstone, Summon Voidwalker (quest) |
| 14 | Drain Life |
| 18 | Searing Pain, Create Soulstone |
| 20 | Demon Armor, Rain of Fire, **Ritual of Summoning**, Sayaad (quest) |
| 28 | Create Firestone; Banish *(Classic)* |
| 30 | Siphon Life (talent), Felhunter (quest), Hellfire *(Classic)* |
| 36 | Create Spellstone |
| 40 | Felsteed (quest), Howl of Terror *(Classic)* |
| 42 | Death Coil *(Classic)* |
| 48 | Soul Fire |
| 50 | Inferno |
| 60 | Ritual of Doom, Dreadsteed (quest) |

### Rotations

=== "Affliction"


    !!! rotation "Affliction: Single target (Wrack build)"

        <div class="priority" markdown>

        1. **Bane of Doom** if the fight will continue for 1 minute or more. If not, Amplify Curse → **Bane of Agony**.
        2. Your assigned **Curse** (Elements for caster-heavy raids, Recklessness for melee-heavy ones).
        3. Corruption.
        4. Siphon Life.
        5. Immolate.
        6. Shadow Bolt **only** when Nightfall makes it instant.
        7. Life Tap in the gap before a refresh, or when you move.
        8. **Wrack** as filler. Stop the channel when an item above is necessary.

        </div>


    Start with a Shadow Bolt when the tank pulls. On a second target, add Corruption. If the target will live 30 s or more, also add Bane of Agony and Siphon Life.

    **Leveling:** pull with Bane of Agony. Then use Corruption, and Immolate on stronger mobs. When the pet tanks, use the wand (before 30) or Drain Life (after 30). Use Life Tap when your health is higher than your mana.

=== "Demonology"


    !!! rotation "Demonology: Fire build"

        <div class="priority" markdown>

        1. Searing Pain if **Demonic Brand** is missing from the target.
        2. Bane of Doom / Bane of Agony as above.
        3. Assigned Curse.
        4. Immolate.
        5. **Soul Fire** when Decimation is active (below 35%).
        6. Corruption.
        7. Life Tap.
        8. Searing Pain filler.

        </div>


    **Shadow build:** Bane, Curse, Searing Pain to keep the brand, Immolate, Corruption, Life Tap, then Shadow Bolt filler. Do not use Soul Fire.

    **Pet tanking:** summon the Voidwalker and send it to the target. Then use Searing Pain on the target, so that Demonic Brand puts a lot of threat on the demon. Before you have Demonic Brand, Searing Pain makes too much threat. Let the pet make threat first.

=== "Destruction"


    !!! rotation "Destruction: Single target"

        <div class="priority" markdown>

        1. Bane of Doom / Bane of Agony as above.
        2. Assigned Curse.
        3. Immolate.
        4. Corruption.
        5. **Conflagrate** (needs Immolate).
        6. **Shadowburn** (needs a shard. With Shadow and Flame, it can give back the shard).
        7. Life Tap in gaps.
        8. **Incinerate** filler (Shadow Bolt before 40).

        </div>


    Start with **Soul Fire** when the tank pulls. Start each fight with a minimum of 2 shards. On 2 targets, put **Bane of Havoc** on the second target. Do not use Hellfire on 2 targets. In dungeons: Bane of Havoc on 1 mob, Bane of Agony on others, **Hellfire** on packs of 3 or more.

### Demons

| Demon | Get it | Use it for |
|---|---|---|
| **Imp** | Level 1 quest | Ranged damage, Blood Pact (Stamina). Raid default for Fire builds |
| **Voidwalker** | Level 10 quest | Tanking when you level and in Demonology pet-tank setups. Sacrifice shield |
| **Sayaad** (Succubus/Incubus) | Level 20 quest | Highest damage demon. Seduction CC. Leveling pet after 20 |
| **Felhunter** | Level 30 quest | Spell Lock and Devour Magic. **The PvP demon** |
| **Infernal** | Inferno, level 50 | Temporary emergency summon |
| **Doomguard** | Ritual of Doom, level 60 | Temporary, costly |

On 6 Nov, Blizzard said that Voidwalkers are **not durable enough** as tanks. Blizzard will tune them to match Classic Era. They will probably be better after the 10 Nov hotfix.

**Grimoires:** you buy demon abilities other than the basic ones from demon trainers. The costs and the full list are not published. At low levels, keep a few silver for each rank.

### Keybinds and macros

??? example "Show 3 macros"

    Put pet **Attack** and **Follow** (and the new **Move**) on easy keys. Useful macros:

    ```
    #showtooltip
    /petattack
    /cast Bane of Agony
    ```

    ```
    #showtooltip Fear
    /cast [@focus,exists,harm] Fear; Fear
    ```

    ```
    #showtooltip Soul Fire
    /cast Demonic Sacrifice
    /cast Soul Fire
    ```

    !!! note
        Forever uses a modern client with Midnight-style add-on limits. `@focus` conditionals work in standard macros. Complex add-ons such as WeakAuras do not work. See [Add-ons](../../systems/addons.md).

## Leveling walkthrough 1–60

Warlocks are one of the easiest classes to level. The pet tanks, and Life Tap and drains give you little downtime. With DoTs, you can fight 2 or 3 mobs at the same time. **Buy a wand** quickly (Lesser Magic Wand at 5, Greater Magic Wand at 13 if you or a friend can enchant). Use it when your DoTs are active.

!!! tip "General habits"
    - Keep **Demon Skin / Demon Armor** up.
    - Use health as mana: use Life Tap to change health into mana, then use Drain Life to get the health back.
    - 2 mobs: put DoTs on the 2 mobs. 3 mobs: put DoTs on 2 and use **Fear** on the third. Do not hit the feared mob.
    - Keep 2–3 spare shards for Soulstone, Healthstone and emergencies. Get them with Drain Soul on kills.
    - For difficult pulls, put a Soulstone on yourself.

<div class="route" markdown>

### 1–10: Starting zone

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Elwynn Forest (Human) · Dun Morogh (Gnome) | Durotar (Orc, Troll) · Tirisfal Glades (Undead) |

- Level 1: sell your starting gear and buy Immolate. Then do the **Imp** quest.
- At 4, learn Corruption, Curse of Weakness and the Blood Pact grimoire.
- At **10**: first talent point (Improved Corruption), Drain Soul, Create Healthstone, and the **Voidwalker** quest. Method.gg rates the Stormwind and Undercity versions as the fastest.
- **The Great Outdoors** at about level 5 unlocks [camping](../../systems/camping.md). Also pick up the gathering-profession starter quest.

### 10–20: First zones and first dungeons

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Westfall, Loch Modan, Darkshore (you can now go there on the **Stormwind Harbor ↔ Auberdine** boat) | Barrens, Silverpine Forest |

- The **Voidwalker** tanks all mobs. Improved Corruption 5/5 makes Corruption almost instant.
- Dungeons: **Ragefire Chasm**, the new **[Hall of Thanes](../../content/dungeons/hall-of-thanes.md)** (13–18, Ironforge) and the new **[Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md)** (15–22, Tirisfal), then Deadmines or Wailing Caverns.
- At **20**: Ritual of Summoning (groups will want you), Demon Armor, Rain of Fire, and the **Sayaad** quest. Warcraft Tavern says that the Horde version is an 8-quest chain in the Barrens and Stonetalon.
- **Library books:** the first library quest unlocks at **20** after you turn in 10 books. Turn them in to Garion Wendell in the Wizard's Sanctum, Stormwind, or Owen Thadd in the Magic Quarter, Undercity. There is no documentation of Warlock rewards yet.
- **Level-20 quest reward:** the *Staff* or *Orb of Soran'ruk* chain (Warcraft Tavern, the same as in Classic).

### 20–30: Pet swap and drain-tanking

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Redridge, Duskwood, Wetlands, Ashenvale | Stonetalon, Ashenvale, Hillsbrad Foothills |

- Change to the **Sayaad** for faster kills, or keep the Voidwalker for safety.
- Unholy Power and Demonic Energies make your demon much stronger.
- Dungeons: Shadowfang Keep, Blackfathom Deeps (the *Gravestone Scepter* wand is a classic warlock reward), The Stockade, the new **[Excavation Site: Wetlands](../../content/dungeons/excavation-site.md)** (24–29+) and the new **[City of Dalaran](../../content/dungeons/city-of-dalaran.md)** (28–35, the city is hostile to the Horde).
- Profession crates: the Alliance supply camp is at Three Corners (Redridge). The Horde camp is west of the Crossroads.
- **Arathi Basin** opens at 20.

### 30–40: Felhunter, Felsteed and dual spec

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Arathi Highlands, Stranglethorn Vale, Desolace, Dustwallow (Theramore) | Thousand Needles, Stranglethorn Vale, Desolace, Arathi |

- **Felhunter** quest at 30. Siphon Life (talent) and **Drain Life as filler** make you a drain-tank: long pulls and almost no rest.
- New zones: **[Riverglades](../../world/zones.md#riverglades)** (35–45, Farholde Keep for Alliance, Rog'mar for Horde) and the mysterious **[Shen'dralas](../../world/zones.md#shendralas)** (south of Desolace, level range not clear).
- Dungeons: Razorfen Kraul, Gnomeregan, Scarlet Monastery wings, the new **[Drowned City](../../content/dungeons/drowned-city.md)** (35–40, Stranglethorn coast).
- **Darkspear Islands** battleground opens at 30.
- **Library quest 2** unlocks at **35** (20 books).
- At **40**: Riding (100g with your racial mount). But Warlocks also get the **Felsteed** from a short quest that sends you to **Strahad Farsan in Ratchet**.
- **Dual spec** (50g) at 40: many players keep Affliction for quests and add Destruction or Demonology for dungeons.
- **Wrack / Demonic Pact / Incinerate** come at 31 points.

### 40–50: Riverglades and the desert

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Riverglades, Tanaris, Feralas, Hinterlands | Riverglades, Tanaris, Feralas, Badlands |

- Use Curse of the Elements on strong targets to make long fights shorter.
- **Library quest 3** unlocks at **45** (25 books).
- Dungeons: the new **[Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md)** (40–45, Riverglades), Razorfen Downs, Uldaman, Zul'Farrak, and the new **[Alcaz Prison](../../content/dungeons/alcaz-prison.md)** (48–53, Dustwallow).
- **Legacy:** the "Experienced" class tier comes at 45 (some sources say 40).
- Soul Fire at 48, Inferno at 50.
- Steamwheedle Port in Tanaris has a ferry to Powderfuse Port in the Riverglades.

### 50–60: Azshara, Un'Goro and the Plaguelands

| Both factions |
|---|
| Azshara (many new quests), Un'Goro Crater, Felwood, Burning Steppes, Western and Eastern Plaguelands, Winterspring, Silithus |

- Dungeons: Maraudon, Sunken Temple, Blackrock Depths, the new **[Blackmaw Hold](../../content/dungeons/blackmaw-hold.md)** (55–60, Azshara), Lower Blackrock Spire, Dire Maul, Scholomance, Stratholme, the new **[Shaper's Terrace](../../content/dungeons/shapers-terrace.md)** (58–60, Un'Goro).
- At **60**: Ritual of Doom and the long **Dreadsteed** epic mount chain (Classic-style, no documentation of Forever changes). Journeyman Riding costs 1,000g.
- Then go through Darkwhisper Gorge in Winterspring into **[Mount Hyjal](../../world/zones.md#mount-hyjal)**, the level-60 zone.

</div>

## Dungeons

All groups want Warlocks:

- **Ritual of Summoning** is the only summon in the game. Meeting Stones do not summon. Thus, a Warlock and 2 players at the entrance can bring all the other players. Groups will ask you to do this.
- **Healthstones** have their own cooldown, separate from potions. Give them to the group before the first pull.
- Before bosses, put a **Soulstone** on a healer.
- Use **Banish** on elementals and demons. Use **Fear** only when the group agrees, because feared mobs can pull more mobs.
- **Threat:** Suppression decreases Affliction threat. Destruction and Searing Pain spam can pull. Give the tank a few seconds.
- **AoE:** Destruction is the dungeon spec. Bane of Havoc on the main target spreads damage. Use Hellfire on packs of 3+ only if the healer can heal you enough. If not, use Rain of Fire.

| Level | Notable dungeons for Warlocks |
|---|---|
| 13–22 | Ragefire Chasm, **Hall of Thanes**, **Ruins of Lordaeron** |
| 18–33 | Deadmines, Wailing Caverns, Shadowfang Keep, Blackfathom Deeps, **Excavation Site**, **City of Dalaran** |
| 30–47 | Scarlet Monastery, Razorfen Kraul/Downs, Gnomeregan, **The Drowned City**, **Krol'dok Stronghold** |
| 44–55 | Uldaman, Zul'Farrak, Maraudon, **Alcaz Prison** |
| 52–60 | Sunken Temple, BRD, LBRS/UBRS, Dire Maul, Scholomance, Stratholme, **Blackmaw Hold**, **Shaper's Terrace** |

See the full list on [Dungeons](../../content/dungeons/index.md). Loot stats stay hidden until a player discovers them, so some loot will be a surprise.

## Raid preparation

All 3 raids open on **9 December 2026**: **[Barrow Deeps](../../content/raids/barrow-deeps.md)** (10 players), **[Hyjal Summit](../../content/raids/hyjal-summit.md)** (20) and **[Onyxia's Lair](../../content/raids/onyxias-lair.md)** (40). Blizzard says that the difficulty comes from **preparation**, not from hundreds of pulls.

**Your job in a raid**

- Keep your **Bane** active, and the **Curse** that your raid leader gives you. Curse of Shadows is removed, so **Curse of the Elements** is the main caster curse. It applies to Fire, Frost, Arcane, Nature and Shadow equally. In a 10-player raid, usually 1 Warlock is sufficient for it.
- Summon players who come late, give Healthstones to the raid, and keep a Soulstone on a healer.
- When the raid leader tells you, use Banish or Fear on adds.

**Pre-raid gear approach**

- Raid loot stays encrypted until players discover it, so there is no fixed BiS list yet. Use this priority: **spell power → hit (to 17%) → crit**.
- Dungeon blues from the 55–60 instances, crafted Tailoring robes (*Filigreed Shadow Gown* for Affliction, *Filigreed Flame Gown* for Fire builds, from Method.gg), and PvP Honor blues.
- **Hit:** spell hit cap is **17%** against raid bosses. Suppression gives 5%.

**Consumables**

- Elixirs of greater spell power, Arcane or Shadow/Fire power elixirs, mana potions, Wizard Oil **plus** your Firestone/Spellstone (they stack now).
- **Onyxia:** fire resistance gear is recommended. Get the **Drakefire Amulet** attunement early (it is not account-wide).
- Camp buffs (Herbalism Intellect, Skinning crit, Tailoring Spirit) for raid nights.

## PvP

Warlocks are one of the strongest PvP casters. They have Fear, Death Coil, Howl of Terror, Seduction, Spell Lock and Soul Link.

- **Felhunter** is the standard PvP demon (Spell Lock, Devour Magic).
- **Builds:** Affliction with **Curse of Exhaustion** (16 points), or Demonology with **Soul Link** for survivability. With Demonic Pact, you can keep a sacrifice buff and also have a Felhunter out.
- **Battlegrounds:** WSG (10–19 brackets and higher), AB (20+), the new **[Battle for the Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands)** (30+, 15v15, 4 bases and a central flag) and AV (51+). On Darkspear Islands, Curse of Exhaustion and Fear are very good to stop flag carriers. Howl of Terror removes enemies from bases.
- **World PvP:** on PvP rulesets, keep a Soulstone and Healthstone ready. Use Fear first, then DoTs, then drains.
- **Be careful of these:**
    - **Orcs** can remove your curses and Banes with *Shatter Curse*.
    - **Undead** ignore Fear with Will of the Forsaken.
    - **Humans** break stuns with *Will to Survive*.
    - Priests and Paladins dispel. Make them use their cleanses before you cast your important curse.
- Progression: Honor and Rank Points for each season. See [PvP](../../content/pvp/index.md).

## Gear, stats & enchants

Armor is **cloth**. Weapons: daggers, wands, and (from the correct trainer) one-hand swords and staves. The stat system now uses a unified crit and hit, plus haste and **spell pierce**.

| Spec | Priority (Warcraft Tavern) |
|---|---|
| **Affliction** | Spell power / Shadow damage > Crit > Hit (17%) > Haste > Spell pierce > Intellect > Spirit |
| **Demonology** | Spell power / school damage > **Hit** > Crit > Haste > Spell pierce > Intellect > Spirit (your demon uses your hit) |
| **Destruction** | Spell power / Fire damage > Crit > Hit > Haste > Spell pierce > Intellect > Spirit. Sims value 1% crit ≈ 8.8 SP and 1% hit ≈ 8.6 SP |
| **Leveling** | Wand DPS (until ~30) > Spell power > Spirit / Intellect > Stamina |

- Haste is weak for Wrack, because it only makes casts and the global cooldown faster.
- **Spirit** is more important than in Classic, because Life Tap scales with it.
- Enchants: this guide assumes Classic caster enchants (spell power on weapon, Intellect/Stamina on other items). There is no documentation of Forever-specific enchant changes.

## Professions & Legacy

<p class="divider">Professions</p>

Warlocks wear cloth, so all top pairs include Tailoring. The Tailoring Faction Banner gives Spirit, which helps Life Tap.

<div class="prof-picks" markdown>

<div class="prof-pick prof-pick--best" markdown>

<p class="prof-rank" markdown>**S**{ .tier .tier-s } Best pick</p>

<p class="prof-pair" markdown>:material-needle: Tailoring <span class="prof-plus">+</span> :material-auto-fix: Enchanting</p>

<p class="prof-for">Best for: Every Warlock</p>

<div class="pills" markdown>
**Leveling**{ .pill .pill--success .pill--sm } **Raids**{ .pill .pill--info .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
</dl>

- Method.gg's pick: crafted robes, wands and disenchanting dungeon loot

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Faction Banner (Spirit) · Enchanted Lute (armor, stats, resists)</p>

</div>

<div class="prof-pick prof-pick--alt" markdown>

<p class="prof-rank" markdown>**A**{ .tier .tier-a } Strong alternative</p>

<p class="prof-pair" markdown>:material-needle: Tailoring <span class="prof-plus">+</span> :material-cog: Engineering</p>

<p class="prof-for">Best for: Highest damage</p>

<div class="pills" markdown>
**Raids**{ .pill .pill--info .pill--sm } **PvP**{ .pill .pill--danger .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:100%"><span>5/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:100%"><span>5/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:40%"><span>2/5</span></span></dd>
</dl>

- Warcraft Tavern's highest-damage pick
- Gadgets and the Engineering camp features. Gnomes fail less frequently

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Faction Banner (Spirit) · Reagent Bot</p>

</div>

<div class="prof-pick prof-pick--sit" markdown>

<p class="prof-rank" markdown>**B**{ .tier .tier-b } Situational</p>

<p class="prof-pair" markdown>:material-leaf: Herbalism <span class="prof-plus">+</span> :material-flask: Alchemy</p>

<p class="prof-for">Best for: Raid consumables</p>

<div class="pills" markdown>
**Raids**{ .pill .pill--info .pill--sm } **Gold**{ .pill .pill--gold .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
</dl>

- Cheap elixirs and potions for raid nights

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Incense Candle (Intellect) · Mana Well (mana regen)</p>

</div>

</div>

<p class="legend" markdown>Codex ratings out of 5, based on the sources above. Compare every class in [Best professions by class](../../characters/professions.md#best-professions-by-class).</p>

<div class="pills" markdown>
**:material-medical-bag: First Aid · healing potions**{ .pill .pill--success } **:material-pot-steam: Cooking · campfires**{ .pill .pill--info } **:material-fish: Fishing · Fish Bowl**{ .pill .pill--info }
</div>

**Secondary skills.** Healing potions are now part of First Aid, so level it. Cooking and Fishing give items for camping.

!!! tip "Race notes"
    **Gnome:** 20% fewer Engineering device failures, so the Tailoring + Engineering pair is better for a Gnome.

Crafting professions give [Legacy Points](../../characters/legacy.md) at skill 150, 225 and 300, and each profession adds a [camp feature](../../systems/camping.md). Professions give no passive stats in Forever.

**Legacy picks (16 points at launch)**

- **Leveling:** *Well Rested* 5/5, then *Talented* (earlier talent points). Or *Thrill of Adventure* for less downtime.
- **Endgame:**
    - *Reagent Economy*: class abilities need no vendor reagents. You must still use Soul Shards.
    - *Permanence*: long class buffs last up to 100% longer. It is *unconfirmed* if it makes the 2-hour Demonic Sacrifice longer.
    - *Gourmand*.
- **PvP:** *For Great Honor*.

## Hardcore notes

!!! hardcore "Hardcore survival"

    The Hardcore ruleset comes in **winter 2026/27**. Its detailed rules are not published. See [Hardcore](../../about/hardcore.md). For a careful Warlock:

    - Level **Affliction or Demonology** with the **Voidwalker**. Soul Link gives you much safety.
    - Keep a **Soulstone** on yourself, and have a Healthstone and a potion. It is *unconfirmed* if Hardcore permits self-Soulstones.
    - **Fear is dangerous**: feared mobs run into other packs. Use it only when there are no other mobs near you. If not, use Seduction and Banish.
    - Use Life Tap only when you are safe. In combat, do not use Life Tap when you have less than half health.
    - Use **Death Coil** and **Howl of Terror** to escape.
    - Keep 3+ shards. Use Drain Soul when a mob has low health.

## Common mistakes / FAQ

??? question "Can I have two Banes or a Bane and a Curse on one target?"
    1 Bane for each Warlock on each target (Agony **or** Doom, or Havoc for Destruction), **plus** 1 Curse. 2 Warlocks can each keep their own Bane.

??? question "Why is my Voidwalker dying?"
    Pets scale from your Stamina, at a lower rate than Classic. Blizzard agrees that Voidwalkers are under-tuned. Keep your own gear at your level. Take Fel Vitality and Demonic Energies. Check again after the 10 Nov hotfix.

??? question "Should I use Curse of Shadows?"
    It does not exist now. Curse of the Elements also applies to Shadow.

??? question "Do I still need Soul Shards for everything?"
    You get shards from Drain Soul ticks and kills. The *Reagent Economy* Legacy talent removes vendor reagent costs. But there is no documentation that it replaces shards.

??? question "Is Demonology really a tank?"
    With Demonic Brand, Voidwalker pet-tanking is a real option in dungeons and the open world. Blizzard has not said that it will tank raids.

??? question "My Firestone replaced my Wizard Oil."
    This is not correct: imbues and oils stack in Forever. Apply the 2 items.

**Mistakes to avoid**

- Searing Pain spam before Demonic Brand: you will take threat from your pet.
- Shadow Bolt on a feared mob.
- Life Tap before a big pull.
- No Felsteed quest at 40, and money spent on a regular mount.
- No Ritual of Summoning on your bars.

## Upcoming tuning

The Blizzard notice of 6 Nov (reported by Warcraft Tavern) gives changes for **Tuesday 10 November 2026**:

- Blizzard will make **Voidwalkers** (and Hunter pets) more durable as tanks, to match Classic Era.
- **Affliction:** Blizzard will make Siphon Life, Corruption and Bane of Agony worth a cast with Wrack. The total Affliction damage will not change.

Blizzard gave no numbers. We will update this page after the hotfix.

## Sources

??? quote "6 sources"

    - Blizzard: [World of Warcraft: Forever Class Deep Dives — Rogue and Warlock](https://worldofwarcraft.blizzard.com/news/24310968) (7 Oct 2026)
    - Blizzard forums: [Class Tuning Incoming – November 10](https://us.forums.blizzard.com/en/wow/t/class-tuning-incoming-november-10/2404092) (cited via Warcraft Tavern)
    - Warcraft Tavern: [Class tuning coming for Shamans, Warlocks, Hunter pets](https://www.warcrafttavern.com/forever/news/class-tuning-coming-for-shamans-warlocks-hunter-pets-in-wow-forever/) (6 Nov 2026)
    - Warcraft Tavern: [Warlock guide](https://www.warcrafttavern.com/forever/guides/warlock/), [Warlock leveling](https://www.warcrafttavern.com/forever/guides/warlock-leveling/), [Affliction](https://www.warcrafttavern.com/forever/guides/affliction-warlock/), [Demonology](https://www.warcrafttavern.com/forever/guides/demonology-warlock/), [Destruction](https://www.warcrafttavern.com/forever/guides/destruction-warlock/), [Racial abilities](https://www.warcrafttavern.com/forever/guides/racial-abilities/)
    - Method.gg: [WoW Forever Warlock leveling guide and talents](https://www.method.gg/wow-forever/wow-forever-warlock-leveling-guide-and-talents) (4 Nov 2026)
    - wowtbc.gg: [Affliction Warlock PvE guide](https://wowtbc.gg/warcraftforever/class-guides/affliction-warlock/)
