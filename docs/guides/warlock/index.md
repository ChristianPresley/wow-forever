---
description: "Warlock guide for WoW: Forever: specs and talents, rotations, a 1–60 leveling route, dungeons, raids, PvP, gear and Hardcore tips."
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
    Forever launched on 4 November. This guide follows Blizzard's Rogue & Warlock class deep dive (7 Oct 2026), Warcraft Tavern's launch-week spec guides (1–3 Nov), Method.gg's leveling guide (4 Nov) and Blizzard's class-tuning notice of 6 Nov. **A Warlock hotfix is scheduled for Tuesday 10 November** (see [Upcoming tuning](#upcoming-tuning)), so treat Affliction rotation advice and Voidwalker tanking as likely to shift. Reference data lives on the [Warlock class page](../../characters/classes/warlock.md).

## Overview

The Warlock is a cloth-wearing ranged caster that fights with damage-over-time spells, fire nukes and a summoned demon. It trades health for mana with **Life Tap**, heals itself with drains, and controls fights with Fear, Banish and its demons. In groups it brings the only summon in the game, Healthstones, Soulstones and **Curse of the Elements**, which in Forever boosts every magic school.

<aside class="infobox" markdown>
<p class="infobox-title">Warlock at a glance</p>

| | |
|---|---|
| **Role** | Ranged damage, crowd control, raid utility (curses, summons, stones) |
| **Armor / weapons** | Cloth; daggers, wands, one-hand swords and staves |
| **Resource** | **Mana**{ .pill .pill--mana } (refilled from health with Life Tap) and **Soul Shards** |
| **Leveling speed** | Second fastest in the beta, behind Hunter |

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
- Slow ramp on DoTs
- Soul Shard upkeep
- Weak mobility
- Melee-range AoE (Hellfire)

</div>
</div>


### What's new in Forever

- **Banes.** Curse of Agony and Curse of Doom are now *Bane of Agony* and *Bane of Doom*. You can keep **one Bane per target**, separate from your one Curse, so a Warlock now runs Bane **plus** a raid curse. Anything that affected Curses also affects Banes.
- **Curse of the Elements** raises damage taken from **all** magic schools. **Curse of Shadows is gone.**
- **DoTs can crit**, and DoT damage is recalculated every tick (no snapshotting buffs, per Warcraft Tavern).
- **Firestone and Spellstone are weapon imbues.** They stack with Wizard Oil. Firestone adds Fire damage and crit; Spellstone adds Shadow damage and spell haste.
- **Life Tap scales with Spirit**, not Stamina.
- **Drain Soul** has a chance to give a shard on every tick, rising each tick until it is guaranteed.
- **Demon scaling:** demons scale from your stats and gear. Pre-launch notes put the bonus at **2 Health per point of your Stamina** (down from 7.5). Boss AoE does **half damage to demons** (Warcraft Tavern).
- **Pet command "Move"** replaces Stay.
- **Talents rebuilt:** new capstones *Wrack*, *Demonic Pact* and *Incinerate*; *Pandemic*, *Bane of Havoc*, *Demonic Brand*, *Decimation*, *Shadow and Flame* and more are new. About 17 old talents were removed.
- **Training is cheaper** to offset buying **Grimoires** (demon abilities) from demon trainers.
- The Succubus line is now called the **Sayaad** (Succubus or Incubus) in Warcraft Tavern's guides.

### Races

| Race | Faction | Status | Add-on |
|---|---|---|---|
| Human | **Alliance**{ .pill .pill--alliance } | Classic | [Human Warlock](human.md) |
| Gnome | **Alliance**{ .pill .pill--alliance } | Classic | [Gnome Warlock](gnome.md) |
| Orc | **Horde**{ .pill .pill--horde } | Classic | [Orc Warlock](orc.md) |
| Troll | **Horde**{ .pill .pill--horde } | **New** | [Troll Warlock](troll.md) |
| Undead | **Horde**{ .pill .pill--horde } | Classic | [Undead Warlock](undead.md) |

!!! conflict "Conflict: best race"
    Method.gg ranks them Human (S), Orc (A), Undead and Gnome (B), Troll (C). Warcraft Tavern says all five are close, calling Human and Orc strong in both PvE and PvP, Undead a PvP pick and Troll good against beasts. One beta-era guide puts every race within 1% DPS. Pick the faction and look you want.

## Specs & talents

Talents start at level 10 (one point per level, 51 at 60). Single-point **gold-medal** talents sit at **11, 16, 21 and 31** points in a tree, so you reach them at roughly levels 20, 25, 30 and 40 if you go straight down one tree. The *Talented* [Legacy talent](../../characters/legacy.md) moves your first point earlier. **Dual spec** unlocks at **level 40** for **50g** from any Warlock trainer; respec fees decay to 1g over time.

| Spec | Capstones (11 / 16 / 21 / 31) | Plays like |
|---|---|---|
| **Affliction** | — / Curse of Exhaustion / — / **Wrack** | DoTs plus a channeled filler; best sustain, slow ramp |
| **Demonology** | Demonic Sacrifice / Fel Domination / Soul Link / **Demonic Pact** | Sacrifice one demon, fight with another; tankiest spec, pet-tank option |
| **Destruction** | — / Conflagrate / Bane of Havoc / **Incinerate** | Fire burst and cleave; best AoE and dungeon damage |

=== "Affliction"

    | Talent | Ranks | What it does |
    |---|---|---|
    | Improved Life Tap | 2 | More mana from Life Tap. Moved to row 1 |
    | Suppression | 5 | Redesigned: up to **+5% spell hit** and −20% threat |
    | Improved Corruption | 5 | Faster Corruption cast; up to +10% damage |
    | Malediction | — | New: up to +5% periodic damage (*see note below*) |
    | Improved Drains | 3 | New: up to +20% from Drain Life, Drain Soul and Wrack |
    | Improved Bane of Agony | 2 | Down from 3 points |
    | Amplify Curse | 1 | Next Bane of Agony deals 50% more |
    | Fel Concentration | 3 | Down from 5; less pushback on drains, now including Wrack |
    | **Pandemic** | 3 | New: DoT and drain crits deal up to **+100%** extra crit damage |
    | Nightfall | 2 | Drain Life, Drain Soul and Wrack can make your next Shadow Bolt instant |
    | **Curse of Exhaustion** | 1 (16 pts) | −30% movement speed. Moved up from row 5 |
    | Malevolence | 5 | New: up to +5% Shadow crit |
    | Siphon Life | 1 | DoT that heals you |
    | Soul Siphon | 3 | New: drains and Wrack gain up to 12% per other Affliction effect on the target (max 36%) |
    | Shadow Mastery | 5 | Shadow damage bonus, smaller than Classic |
    | **Wrack** | 1 (31 pts) | Channel: Shadow damage every second, and your other Shadow DoTs deal **+10%** to the target for 6 s. Pre-launch notes put it at about 86 dps base at 60 |

    *Soul Harvest* is the renamed Improved Drain Soul. The BlizzCon demo called the capstone "Drain Hope"; every later source says **Wrack**.

    !!! warning "Malediction may have moved"
        One launch-week guide warns that the periodic-damage Malediction from the deep dive may no longer be in that slot. Read the tooltip before spending points on it.

=== "Demonology"

    | Talent | Ranks | What it does |
    |---|---|---|
    | Unholy Power | 5 | Pet damage (smaller bonus than Classic). Moved to row 1 |
    | Improved Health Funnel | — | More healing, up to 100% less threat, usable at any demon health |
    | Improved Imp | 3 | No longer affects Blood Pact |
    | Demonic Aegis | — | New: Demon Skin/Armor up to +30% |
    | Fel Vitality | 3 | New: pet health and mana up to +15%, **your mana** up to +15% |
    | Demonic Energies | 2 | New: pet heals for up to 15% of your spell damage; Life Tap feeds it mana |
    | Master Summoner | 2 | Faster, cheaper summons; required for Fel Domination |
    | **Demonic Sacrifice** | 1 (11 pts) | Sacrifice a demon for a **2-hour** buff: Imp = Shadow damage, Voidwalker = mana regen, Sayaad = Fire damage, Felhunter = health regen |
    | **Fel Domination** | 1 (16 pts) | Next summon is fast |
    | Demonic Embrace | 5 | Stamina; no longer lowers Spirit |
    | Improved Sayaad | 3 | Listed by Warcraft Tavern only (*unconfirmed*) |
    | Decimation | — | New: Shadow Bolt or Searing Pain on a target below 35% makes your next Soul Fire faster (up to 40%) and shard-free for 10 s; Soul Fire cooldown cut up to 90% |
    | **Demonic Brand** | 3 | New: Searing Pain makes less threat and brands the target; your pet's next 2 attacks deal bonus Fire or Shadow damage. With a **Voidwalker** this generates big threat, making **pet tanking** viable |
    | **Soul Link** | 1 (21 pts) | About 30% of damage you take is moved to your demon. Moved up from row 7 |
    | Improved Felhunter | — | New: stronger Felhunter abilities, Spell Lock −2 s cooldown |
    | Demonic Knowledge | 3 | New: you and your pet gain spell damage based on your level while a demon is out |
    | Master Demonologist | 5 | Redesigned: Imp = Fire damage, Voidwalker = less physical damage taken, Sayaad = Shadow damage, Felhunter = less magic damage taken |
    | **Demonic Pact** | 1 (31 pts) | Requires Soul Link. Your sacrifice buff is **kept** when you summon a *different* demon |

    No Felguard: it isn't mentioned in any Forever source.

=== "Destruction"

    | Talent | Ranks | What it does |
    |---|---|---|
    | Destructive Reach | — | Range for all damaging spells. Moved to row 1 |
    | Bane | 5 | Faster Shadow Bolt, Immolate and now **Incinerate** |
    | Cataclysm | 3 | Up to −10% Destruction mana cost |
    | Molten Skin | 5 | New: up to −10% damage taken (2% per point, Warcraft Tavern) |
    | Improved Shadow Bolt | 5 | Only your own Shadow damage; no charges |
    | Aftermath | 5 | Redesigned: Immolate's initial hit up to +50%; Conflagrate can Daze (−50% speed, 5 s) |
    | Ruin | 5 | Crit damage. Moved to row 3 |
    | Agonizing Flames | 3 | Formerly Improved Searing Pain |
    | Intensity | 3 | Pushback resistance for all Destruction spells |
    | **Conflagrate** | 1 (16 pts) | Moved up from row 7 |
    | Fire and Brimstone | 3 | New: Conflagrate crit |
    | **Bane of Havoc** | 1 (21 pts) | 5-minute Bane: **15% of damage you deal to other targets** is copied to the cursed target |
    | Shadow and Flame | 5 | New: Conflagrate grants a Shadow buff and Shadowburn a Fire buff (20 s); Conflagrate can keep Immolate, Shadowburn can refund its shard |
    | **Incinerate** | 1 (31 pts) | 2.5 s Fire nuke, 30 yd, **+25%** if Immolate is on the target |

### Removed talents

Improved Healthstone · Fel Intellect · Fel Stamina · Improved Subjugate Demon · Improved Firestone · Improved Spellstone · Improved Curse of Weakness · Improved Drain Life · Improved Drain Mana · Improved Curse of Exhaustion · Grim Reach · Dark Pact · Improved Firebolt · Improved Lash of Pain · Devastation · Improved Immolate · Emberstorm.

!!! conflict "Conflict: Grim Reach"
    Blizzard's deep dive lists Grim Reach as removed, but Warcraft Tavern's and Method.gg's leveling guides still suggest it for PvP. Trust the in-game tree; if it is missing, *Destructive Reach* (Destruction row 1) covers range instead.

### Leveling builds

Every major guide recommends **Affliction** for leveling, with Demonology a close second and Destruction best in groups. These are Warcraft Tavern's orders; Method.gg's differ only in timing.

=== "Affliction (40/7/4)"

    <div class="milestones" markdown>

    Lv 10–19
    :   Improved Corruption 5/5, Suppression 5/5

    Lv 20–26
    :   Unholy Power 5/5, Demonic Energies 2/2 (Demonology, for a sturdier pet)

    Lv 27–30
    :   Improved Drains 3/3, Amplify Curse

    Lv 31–40
    :   Improved Bane of Agony 2/2, Improved Life Tap 2/2, Pandemic 3/3, Soul Siphon 3/3

    Lv 41–60
    :   Malevolence 5/5, Shadow Mastery 5/5, Siphon Life, Fel Concentration 3/3, Nightfall 2/2, Improved Shadow Bolt 4/5

    </div>

    Take Fel Concentration earlier if mobs keep interrupting your drains. Voidwalker tanks until 20, then the Sayaad; drain-tanking with Drain Life starts around 30.

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

    You can also go straight down Demonology from 10. Method.gg instead stays Affliction until the mid-40s.

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

    Method.gg lists Shadowburn at 24 and Conflagrate at 29; that is build order, not a different rule.

### Endgame builds (level 60)

From Warcraft Tavern's spec guides (1–3 Nov). No raid has opened yet, so these are pre-raid simulations.

| Spec | Build | Split (A/D/D) | Notes |
|---|---|---|---|
| Affliction | **Wrack** | 33 / 0 / 18 | Wrack is the filler, backed by Soul Siphon 3/3. Shadow Bolt only on Nightfall procs |
| Affliction | SM/Ruin | 30 / 0 / 21 | Shadow Bolt filler. Slightly behind Wrack; the dungeon pick (move the third Cataclysm point into Shadowburn) |
| Demonology | Fire | 2 / 31 / 18 | Sacrifice the Sayaad, keep the Imp out. Searing Pain filler, Soul Fire execute, Firestone |
| Demonology | Shadow | 2 / 31 / 18 | Sacrifice the Imp, keep the Sayaad out. Shadow Bolt filler, Spellstone. Within ~3% of Fire |
| Destruction | Sayaad | 14 / 4 / 33 | Keep the Sayaad summoned. Best Destruction build |
| Destruction | Imp | 14 / 4 / 33 | Moves points from Aftermath and Unholy Power into Improved Imp and Demonic Energies. Slightly lower |
| Destruction | Sacrifice | 7 / 11 / 33 | Sacrifice the Sayaad for +15% Fire. Behind the Sayaad build |

!!! note "Affliction is about to change"
    Blizzard said on 6 Nov that simply channeling Wrack beats keeping Siphon Life, Corruption and Bane of Agony up, and that it will make those DoTs worth casting alongside Wrack without raising Affliction's total damage. Expect the Wrack build's priority to change after 10 Nov.

## Abilities & rotation

### Key spells by level

Levels below come from Method.gg and Warcraft Tavern for Forever; those marked *(Classic)* follow Classic and haven't been checked against Forever.

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

        1. **Bane of Doom** if the fight has a minute or more left; otherwise Amplify Curse → **Bane of Agony**.
        2. Your assigned **Curse** (Elements for caster-heavy raids, Recklessness for melee-heavy ones).
        3. Corruption.
        4. Siphon Life.
        5. Immolate.
        6. Shadow Bolt **only** when Nightfall makes it instant.
        7. Life Tap in the gap before a refresh, or while moving.
        8. **Wrack** as filler. Break the channel whenever something above comes due.

        </div>


    Open with a Shadow Bolt while the tank pulls. On a second target add Corruption, plus Bane of Agony and Siphon Life if it will live 30 s or more.

    **Leveling:** Bane of Agony to pull, Corruption, Immolate on tougher mobs, then wand (before 30) or Drain Life (after 30) while the pet tanks. Life Tap whenever your health is higher than your mana.

=== "Demonology"


    !!! rotation "Demonology: Fire build"

        <div class="priority" markdown>

        1. Searing Pain if **Demonic Brand** is missing from the target.
        2. Bane of Doom / Bane of Agony as above.
        3. Assigned Curse.
        4. Immolate.
        5. **Soul Fire** while Decimation is up (below 35%).
        6. Corruption.
        7. Life Tap.
        8. Searing Pain filler.

        </div>


    **Shadow build:** Bane, Curse, Searing Pain to keep the brand, Immolate, Corruption, Life Tap, then Shadow Bolt filler. Skip Soul Fire.

    **Pet tanking:** summon the Voidwalker, send it in, then Searing Pain the target so Demonic Brand piles threat onto the demon. Before you have Demonic Brand, Searing Pain is a threat trap; let the pet build threat first.

=== "Destruction"


    !!! rotation "Destruction: Single target"

        <div class="priority" markdown>

        1. Bane of Doom / Bane of Agony as above.
        2. Assigned Curse.
        3. Immolate.
        4. Corruption.
        5. **Conflagrate** (needs Immolate).
        6. **Shadowburn** (needs a shard; with Shadow and Flame it can refund it).
        7. Life Tap in gaps.
        8. **Incinerate** filler (Shadow Bolt before 40).

        </div>


    Open with **Soul Fire** while the tank pulls and enter every fight with at least 2 shards. On two targets, put **Bane of Havoc** on the second one; Hellfire isn't worth it on two. In dungeons: Bane of Havoc on one mob, Bane of Agony on others, **Hellfire** on packs of 3 or more.

### Demons

| Demon | Get it | Use it for |
|---|---|---|
| **Imp** | Level 1 quest | Ranged damage, Blood Pact (Stamina). Raid default for Fire builds |
| **Voidwalker** | Level 10 quest | Tanking while leveling and in Demonology pet-tank setups. Sacrifice shield |
| **Sayaad** (Succubus/Incubus) | Level 20 quest | Highest damage demon; Seduction CC. Leveling pet after 20 |
| **Felhunter** | Level 30 quest | Spell Lock and Devour Magic. **The PvP demon** |
| **Infernal** | Inferno, level 50 | Temporary emergency summon |
| **Doomguard** | Ritual of Doom, level 60 | Temporary, costly |

Blizzard said on 6 Nov that Voidwalkers are **not durable enough** as tanks and will be tuned to match Classic Era. Expect them to feel better after the 10 Nov hotfix.

**Grimoires:** demon abilities beyond the basics are bought from demon trainers. Costs and the full list haven't been published; budget a few silver per rank early.

### Keybinds and macros

??? example "Show 3 macros"

    Bind pet **Attack** and **Follow** (and the new **Move**) to easy keys. Useful macros:

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
        Forever uses a modern client with Midnight-style add-on limits. `@focus` conditionals work in standard macros; complex add-ons such as WeakAuras do not. See [Add-ons](../../systems/addons.md).

## Leveling walkthrough 1–60

Warlocks are one of the easiest classes to level: the pet tanks, Life Tap and drains mean little downtime, and DoTs let you fight two or three mobs at once. **Buy a wand** as soon as you can (Lesser Magic Wand at 5, Greater Magic Wand at 13 if you or a friend enchant) and use it once your DoTs are rolling.

!!! tip "General habits"
    - Keep **Demon Skin / Demon Armor** up.
    - Treat health as mana: Life Tap down, then Drain Life back up.
    - Two mobs: DoT both. Three: DoT two and **Fear** the third, and don't hit the feared one.
    - Keep 2–3 spare shards for Soulstone, Healthstone and emergencies; collect them with Drain Soul on kills.
    - Bring a Soulstone on yourself for hard pulls.

<div class="route" markdown>

### 1–10: Starting zone

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Elwynn Forest (Human) · Dun Morogh (Gnome) | Durotar (Orc, Troll) · Tirisfal Glades (Undead) |

- Level 1: sell your starting gear to buy Immolate, then do the **Imp** quest.
- Learn Corruption and Curse of Weakness at 4, plus the Blood Pact grimoire.
- At **10**: first talent point (Improved Corruption), Drain Soul, Create Healthstone, and the **Voidwalker** quest. Method.gg rates the Stormwind and Undercity versions as the quickest.
- **The Great Outdoors** around level 5 unlocks [camping](../../systems/camping.md); pick up the gathering-profession starter quest too.

### 10–20: First zones and first dungeons

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Westfall, Loch Modan, Darkshore (now reachable by the **Stormwind Harbor ↔ Auberdine** boat) | Barrens, Silverpine Forest |

- **Voidwalker** tanks everything. Improved Corruption 5/5 makes Corruption near-instant.
- Dungeons: **Ragefire Chasm**, the new **[Hall of Thanes](../../content/dungeons/hall-of-thanes.md)** (13–18, Ironforge) and the new **[Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md)** (15–22, Tirisfal), then Deadmines or Wailing Caverns.
- At **20**: Ritual of Summoning (make yourself popular), Demon Armor, Rain of Fire, and the **Sayaad** quest. Warcraft Tavern says the Horde version is an eight-quest chain across the Barrens and Stonetalon.
- **Library books:** the first library quest unlocks at **20** after turning in 10 books (Garion Wendell in the Wizard's Sanctum, Stormwind; Owen Thadd in the Magic Quarter, Undercity). Warlock rewards aren't documented yet.
- **Level-20 quest reward:** the *Staff* or *Orb of Soran'ruk* chain (Warcraft Tavern, carried over from Classic).

### 20–30: Pet swap and drain-tanking

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Redridge, Duskwood, Wetlands, Ashenvale | Stonetalon, Ashenvale, Hillsbrad Foothills |

- Switch to the **Sayaad** for faster kills, or keep the Voidwalker for safety.
- Unholy Power and Demonic Energies make your demon much sturdier.
- Dungeons: Shadowfang Keep, Blackfathom Deeps (the *Gravestone Scepter* wand is a classic warlock prize), The Stockade, the new **[Excavation Site: Wetlands](../../content/dungeons/excavation-site.md)** (24–29+) and the new **[City of Dalaran](../../content/dungeons/city-of-dalaran.md)** (28–35; the city is hostile to the Horde).
- Profession crates: the Alliance supply camp is at Three Corners (Redridge), the Horde camp west of the Crossroads.
- **Arathi Basin** opens at 20.

### 30–40: Felhunter, Felsteed and dual spec

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Arathi Highlands, Stranglethorn Vale, Desolace, Dustwallow (Theramore) | Thousand Needles, Stranglethorn Vale, Desolace, Arathi |

- **Felhunter** quest at 30. Siphon Life (talent) and **Drain Life as filler** make you a drain-tank: long pulls, almost no rest.
- New zones: **[Riverglades](../../world/zones.md#riverglades)** (35–45; Farholde Keep for Alliance, Rog'mar for Horde) and the mysterious **[Shen'dralas](../../world/zones.md#shendralas)** (south of Desolace; level range unclear).
- Dungeons: Razorfen Kraul, Gnomeregan, Scarlet Monastery wings, the new **[Drowned City](../../content/dungeons/drowned-city.md)** (35–40, Stranglethorn coast).
- **Darkspear Islands** battleground opens at 30.
- **Library quest 2** unlocks at **35** (20 books).
- At **40**: Riding (100g with your racial mount), but Warlocks also get the **Felsteed** from a short quest that leads to **Strahad Farsan in Ratchet**. **Dual spec** (50g): many keep Affliction for questing and add Destruction or Demonology for dungeons. **Wrack / Demonic Pact / Incinerate** arrive at 31 points.

### 40–50: Riverglades and the desert

| **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|
| Riverglades, Tanaris, Feralas, Hinterlands | Riverglades, Tanaris, Feralas, Badlands |

- Curse of the Elements on tough targets speeds up long fights.
- **Library quest 3** unlocks at **45** (25 books).
- Dungeons: the new **[Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md)** (40–45, Riverglades), Razorfen Downs, Uldaman, Zul'Farrak, and the new **[Alcaz Prison](../../content/dungeons/alcaz-prison.md)** (48–53, Dustwallow).
- **Legacy:** the "Experienced" class tier comes at 45 (some sources say 40).
- Soul Fire at 48, Inferno at 50.
- Tanaris's Steamwheedle Port has a ferry to Powderfuse Port in the Riverglades.

### 50–60: Azshara, Un'Goro and the Plaguelands

| Both factions |
|---|
| Azshara (many new quests), Un'Goro Crater, Felwood, Burning Steppes, Western and Eastern Plaguelands, Winterspring, Silithus |

- Dungeons: Maraudon, Sunken Temple, Blackrock Depths, the new **[Blackmaw Hold](../../content/dungeons/blackmaw-hold.md)** (55–60, Azshara), Lower Blackrock Spire, Dire Maul, Scholomance, Stratholme, the new **[Shaper's Terrace](../../content/dungeons/shapers-terrace.md)** (58–60, Un'Goro).
- At **60**: Ritual of Doom and the long **Dreadsteed** epic mount chain (Classic-style; Forever changes undocumented). Journeyman Riding is 1,000g.
- Then head through Darkwhisper Gorge in Winterspring into **[Mount Hyjal](../../world/zones.md#mount-hyjal)**, the level-60 zone.

</div>

## Dungeons

Warlocks are welcome in every group:

- **Ritual of Summoning** is the only summon in the game. Meeting Stones don't summon, so a Warlock plus two players at the entrance can bring everyone else. Expect to be asked.
- **Healthstones** have their own cooldown, separate from potions. Hand them out before the first pull.
- **Soulstone** a healer before bosses.
- **Banish** elementals and demons; **Fear** only when the group agrees (runners pull more).
- **Threat:** Suppression lowers Affliction threat; Destruction and Searing Pain spam can pull. Let the tank get a few seconds.
- **AoE:** Destruction is the dungeon spec. Bane of Havoc on the main target spreads damage. Hellfire packs of 3+ only if the healer can keep up; Rain of Fire otherwise.

| Level | Notable dungeons for Warlocks |
|---|---|
| 13–22 | Ragefire Chasm, **Hall of Thanes**, **Ruins of Lordaeron** |
| 18–33 | Deadmines, Wailing Caverns, Shadowfang Keep, Blackfathom Deeps, **Excavation Site**, **City of Dalaran** |
| 30–47 | Scarlet Monastery, Razorfen Kraul/Downs, Gnomeregan, **The Drowned City**, **Krol'dok Stronghold** |
| 44–55 | Uldaman, Zul'Farrak, Maraudon, **Alcaz Prison** |
| 52–60 | Sunken Temple, BRD, LBRS/UBRS, Dire Maul, Scholomance, Stratholme, **Blackmaw Hold**, **Shaper's Terrace** |

See the full list on [Dungeons](../../content/dungeons/index.md). Loot stats are hidden until someone discovers them, so expect surprises.

## Raid preparation

All three raids open on **9 December 2026**: **[Barrow Deeps](../../content/raids/barrow-deeps.md)** (10 players), **[Hyjal Summit](../../content/raids/hyjal-summit.md)** (20) and **[Onyxia's Lair](../../content/raids/onyxias-lair.md)** (40). Blizzard says difficulty comes from **preparation**, not from hundreds of pulls.

**Your job in a raid**

- Keep your **Bane** up and the **Curse** your raid leader assigns. With Curse of Shadows gone, **Curse of the Elements** is the main caster curse and covers Fire, Frost, Arcane, Nature and Shadow alike. In a 10-player raid one Warlock usually covers it.
- Summon latecomers, hand out Healthstones, keep a Soulstone on a healer.
- Banish or Fear adds when asked.

**Pre-raid gear approach**

- Raid loot is encrypted until discovered, so there is no fixed BiS list yet. Prioritize **spell power → hit (to 17%) → crit**.
- Dungeon blues from the 55–60 instances, crafted Tailoring robes (*Filigreed Shadow Gown* for Affliction, *Filigreed Flame Gown* for Fire builds, per Method.gg), and PvP Honor blues.
- **Hit:** spell hit cap is **17%** against raid bosses. Suppression gives 5%.

**Consumables**

- Elixirs of greater spell power, Arcane or Shadow/Fire power elixirs, mana potions, Wizard Oil **plus** your Firestone/Spellstone (they stack now).
- **Onyxia:** fire resistance gear is recommended; get the **Drakefire Amulet** attunement early (it isn't account-wide).
- Camp buffs (Herbalism Intellect, Skinning crit, Tailoring Spirit) for raid nights.

## PvP

Warlocks are among the strongest PvP casters: Fear, Death Coil, Howl of Terror, Seduction, Spell Lock and Soul Link.

- **Felhunter** is the standard PvP demon (Spell Lock, Devour Magic).
- **Builds:** Affliction with **Curse of Exhaustion** (16 points), or Demonology with **Soul Link** for survivability. Demonic Pact lets you keep a sacrifice buff and still have a Felhunter out.
- **Battlegrounds:** WSG (10–19 brackets up), AB (20+), the new **[Battle for the Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands)** (30+, 15v15, four bases and a central flag) and AV (51+). On Darkspear Islands, Curse of Exhaustion and Fear are excellent for stopping flag carriers, and Howl of Terror clears bases.
- **World PvP:** on PvP rulesets, keep a Soulstone and Healthstone ready. Fear first, DoT, drain.
- **Watch for:** **Orcs** can remove your curses and Banes with *Shatter Curse*; **Undead** ignore Fear with Will of the Forsaken; **Humans** break stuns with *Will to Survive*; Priests and Paladins dispel. Bait cleanses before your important curse.
- Progression: Honor and Rank Points per season. See [PvP](../../content/pvp/index.md).

## Gear, stats & enchants

Armor is **cloth**. Weapons: daggers, wands, and (from the right trainer) one-hand swords and staves. The stat system now uses a unified crit and hit, plus haste and **spell pierce**.

| Spec | Priority (Warcraft Tavern) |
|---|---|
| **Affliction** | Spell power / Shadow damage > Crit > Hit (17%) > Haste > Spell pierce > Intellect > Spirit |
| **Demonology** | Spell power / school damage > **Hit** > Crit > Haste > Spell pierce > Intellect > Spirit (your demon uses your hit) |
| **Destruction** | Spell power / Fire damage > Crit > Hit > Haste > Spell pierce > Intellect > Spirit. Sims value 1% crit ≈ 8.8 SP and 1% hit ≈ 8.6 SP |
| **Leveling** | Wand DPS (until ~30) > Spell power > Spirit / Intellect > Stamina |

- Haste is weak for Wrack because it only speeds casts and the global cooldown.
- **Spirit** matters more than in Classic because Life Tap scales with it.
- Enchants: Classic caster enchants (spell power on weapon, Intellect/Stamina elsewhere) are assumed; Forever-specific enchant changes aren't documented.

## Professions & Legacy

<p class="divider">Professions</p>

Warlocks wear cloth, so Tailoring anchors every top pairing. Tailoring's Faction Banner gives Spirit, which helps Life Tap.

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
- Gadgets and the Engineering camp features; Gnomes fail less often

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

**Secondary skills.** Healing potions moved to First Aid; level it. Cooking and Fishing feed camping.

!!! tip "Race notes"
    **Gnome:** 20% fewer Engineering device failures, which favors the Tailoring + Engineering pair.

Crafting professions award [Legacy Points](../../characters/legacy.md) at skill 150, 225 and 300, and each profession adds a [camp feature](../../systems/camping.md). Professions give no passive stats in Forever.

**Legacy picks (16 points at launch)**

- **Leveling:** *Well Rested* 5/5 then *Talented* (earlier talent points), or *Thrill of Adventure* for less downtime.
- **Endgame:** *Reagent Economy* (class abilities need no vendor reagents; Soul Shards still apply), *Permanence* (long class buffs last up to 100% longer; whether it extends the 2-hour Demonic Sacrifice is *unconfirmed*), *Gourmand*.
- **PvP:** *For Great Honor*.

## Hardcore notes

!!! hardcore "Hardcore survival"

    The Hardcore ruleset arrives in **winter 2026/27**; its detailed rules aren't published. See [Hardcore](../../about/hardcore.md). For a careful Warlock:

    - Level **Affliction or Demonology** with the **Voidwalker**; Soul Link is a huge safety net.
    - Keep a **Soulstone** on yourself (whether self-Soulstones are allowed on Hardcore is *unconfirmed*), a Healthstone and a potion.
    - **Fear is dangerous**: feared mobs run into other packs. Use it only with clear space, or use Seduction and Banish instead.
    - Life Tap only when safe; never tap below half health in combat.
    - **Death Coil** and **Howl of Terror** are your escape buttons.
    - Keep 3+ shards; Drain Soul when anything is low.

## Common mistakes / FAQ

??? question "Can I have two Banes or a Bane and a Curse on one target?"
    One Bane per Warlock per target (Agony **or** Doom, or Havoc for Destruction), **plus** one Curse. Two Warlocks can each keep their own Bane.

??? question "Why is my Voidwalker dying?"
    Pets scale from your Stamina, at a lower rate than Classic, and Blizzard admits Voidwalkers are under-tuned. Keep your own gear up, take Fel Vitality and Demonic Energies, and check again after the 10 Nov hotfix.

??? question "Should I use Curse of Shadows?"
    It no longer exists. Curse of the Elements covers Shadow too.

??? question "Do I still need Soul Shards for everything?"
    Shards come from Drain Soul ticks and kills. The *Reagent Economy* Legacy talent removes vendor reagent costs, but it isn't documented to replace shards.

??? question "Is Demonology really a tank?"
    Demonic Brand makes Voidwalker pet-tanking a real option in dungeons and open world. Blizzard hasn't said it will tank raids.

??? question "My Firestone replaced my Wizard Oil."
    It shouldn't: imbues and oils stack in Forever. Apply both.

**Mistakes to avoid**

- Spamming Searing Pain before Demonic Brand: you'll pull threat off your pet.
- Shadow Bolting a feared mob.
- Life Tapping into a big pull.
- Forgetting the Felsteed quest at 40 and paying for a regular mount.
- Leaving Ritual of Summoning off your bars.

## Upcoming tuning

Blizzard's 6 Nov notice (reported by Warcraft Tavern) plans changes for **Tuesday 10 November 2026**:

- **Voidwalkers** (and Hunter pets) will be made more durable as tanks, to match Classic Era.
- **Affliction:** Siphon Life, Corruption and Bane of Agony will be made worthwhile alongside Wrack, without changing total Affliction damage.

No numbers were given. This page will be updated after the hotfix.

## Sources

??? quote "6 sources"

    - Blizzard: [World of Warcraft: Forever Class Deep Dives — Rogue and Warlock](https://worldofwarcraft.blizzard.com/news/24310968) (7 Oct 2026)
    - Blizzard forums: [Class Tuning Incoming – November 10](https://us.forums.blizzard.com/en/wow/t/class-tuning-incoming-november-10/2404092) (cited via Warcraft Tavern)
    - Warcraft Tavern: [Class tuning coming for Shamans, Warlocks, Hunter pets](https://www.warcrafttavern.com/forever/news/class-tuning-coming-for-shamans-warlocks-hunter-pets-in-wow-forever/) (6 Nov 2026)
    - Warcraft Tavern: [Warlock guide](https://www.warcrafttavern.com/forever/guides/warlock/), [Warlock leveling](https://www.warcrafttavern.com/forever/guides/warlock-leveling/), [Affliction](https://www.warcrafttavern.com/forever/guides/affliction-warlock/), [Demonology](https://www.warcrafttavern.com/forever/guides/demonology-warlock/), [Destruction](https://www.warcrafttavern.com/forever/guides/destruction-warlock/), [Racial abilities](https://www.warcrafttavern.com/forever/guides/racial-abilities/)
    - Method.gg: [WoW Forever Warlock leveling guide and talents](https://www.method.gg/wow-forever/wow-forever-warlock-leveling-guide-and-talents) (4 Nov 2026)
    - wowtbc.gg: [Affliction Warlock PvE guide](https://wowtbc.gg/warcraftforever/class-guides/affliction-warlock/)
