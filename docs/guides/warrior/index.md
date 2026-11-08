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
    This guide follows Blizzard's pre-launch notes (2–4 Nov), the launch-week hotfixes and the first community guides. Talent numbers in Forever are still moving. For reference data, see the [Warrior class page](../../characters/classes/warrior.md).

## Overview

The Warrior is Forever's plate-wearing melee class. It can **tank** (Protection) or deal **melee damage** (Arms with a two-hander, Fury dual-wielding). It runs on **rage**, which you gain by hitting and being hit, and it switches between three stances for different tools.

<aside class="infobox" markdown>
<p class="infobox-title">Warrior at a glance</p>

| | |
|---|---|
| **Roles** | Tank (Protection) · Melee DPS (Arms, Fury) |
| **Armor** | **Cloth**{ .pill .pill--cloth }, leather and mail from level 1. ****Plate**{ .pill .pill--plate } at 40** from the class trainer |
| **Weapons** | Every type except wands. Shields. Polearms trainable from level 20 |
| **Resource** | **Rage**{ .pill .pill--rage } (now normalized; see below) |
| **Races** | All ten: every race in the game can be a Warrior |

</aside>

**Strengths**

- The best-supported tank class, with a much larger Defensive Stance threat bonus (+80%) in Forever.
- Huge damage potential once geared, with strong cleave from Sweeping Strikes and Whirlwind.
- Rage normalization means **gear no longer starves you of rage**: armor and absorbs don't reduce what you gain from being hit.
- Victory Rush and Tactical Mastery are baseline, so early leveling hurts less than in Classic.

**Weaknesses**

- Reported in the beta as one of the **two slowest leveling classes** (with Priest). Kill speed depends almost entirely on your weapon.
- Little self-healing, no crowd control to speak of, and you need a healer to tank anything serious.
- Gear-hungry. A Warrior with a bad weapon feels far worse than any other class with a bad weapon.

### What's new in Forever

- **Rage normalization.** Rage from taking damage is calculated as if your armor were always 50%, and absorbs (Power Word: Shield and similar) no longer cut it. Rage from dealing damage now depends on **weapon speed**, so slow weapons give more per swing. **Crits give +75% rage.**
- **Baseline changes.** Tactical Mastery (level 14) keeps 10 rage on stance swap. Victory Rush (level 20) has a 30 s cooldown and heals 10%. Recklessness, Retaliation and Shield Wall no longer share a cooldown; Retaliation and Shield Wall are 15 minutes. Rend and Thunder Clap scale with attack power. Thunder Clap works in Defensive Stance with a 6 s cooldown. Improved Battle Shout is folded in, and Sunder Armor now coexists with a Rogue's Expose Armor.
- **Pre-launch tuning.** Defensive Stance threat is **+80%** (was 30%), and Slam has a **15 s cooldown**. A 4 Nov hotfix touched Defensive Stance and Defiance threat again.
- **New talents.** Spearing Strike, Bloodthrill and Weaponmaster (Arms), Raging Blows, Boundless Rage, Reckless Swings and Improved Whirlwind (Fury), and Vanguard, Bastion and Focused Rage (Protection).
- **Removed talents.** The weapon specializations (merged into Weaponmaster), Improved Battle Shout, Improved Demoralizing Shout, Improved Shield Block and Improved Taunt (now baseline), and One-Handed Weapon Specialization.

### Race add-ons

Every race can be a Warrior. Pick a race, then read its add-on alongside this guide.

| Alliance | Horde |
|---|---|
| [Human](human.md): Will to Survive, +1% crit | [Orc](orc.md): Blood Fury, stun reduction |
| [Dwarf](dwarf.md): Stoneform, +1% hit | [Troll](troll.md): Berserking, out-of-combat regen |
| [Gnome](gnome.md): Escape Artist, Eureka! | [Tauren](tauren.md): War Stomp, +5% health, top Strength |
| [Night Elf](night-elf.md): Elune's Light, Shadowmeld | [Undead](undead.md): Will of the Forsaken, Touch of the Grave |
| [Skyborne (High Order)](skyborne-high-order.md): **NEW** | [Skyborne (Windshaper)](skyborne-windshaper.md): **NEW** |

Skyborne Warriors are the only new Warrior combinations in Forever. They need the Skyborne Heroic Pack or a higher edition. See [Skyborne](../../characters/races.md#skyborne).

---

## Specs & talents

Forever's Warrior trees keep the Classic shape but swap many talents. The new **16-point tier** gives each tree a signature pick (Spearing Strike, Raging Blows, Vanguard). Exact point costs and positions are still changing build to build, so the builds below give **priorities and milestones**, not a point-by-point export. Check them against an up-to-date talent calculator before you commit.

!!! tip "Talent points earlier with Legacy"
    The Legacy talent **Talented** (requires 5/5 **Well Rested**) moves your first talent point one level earlier per rank, down to level 5. That's 10 Legacy Points, so it's a second-character luxury. See [Legacy](../../characters/legacy.md).

=== "Arms"

    **Two-handed weapons, Overpower, Mortal Strike.** The traditional leveling and PvP spec.

    | Talent | What it does in Forever |
    |---|---|
    | Improved Rend | Rend now scales with attack power, so this is worth more than in Classic |
    | Improved Tactical Mastery | 5/10/15 rage kept on swap, on top of the baseline 10 |
    | Improved Overpower | More Overpower crits, so more rage |
    | **Spearing Strike** (16) | 15 rage, 20 s cooldown. Dismounts, and deals double damage to mounted targets, dragons and giants |
    | **Bloodthrill** | 10/20% (two ranks pre-launch). The Tavern build takes it over Weaponmaster for more Overpower uses |
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
    | **Boundless Rage** | New rage talent; details still settling |
    | Dual Wield Specialization | Off-hand damage; leads to Death Wish |
    | **Raging Blows** (16) | The new Fury signature talent |
    | Enrage | Redesigned; near-permanent uptime while leveling, according to Method |
    | Death Wish | Now also raises damage taken |
    | Flurry | 10/20/30% attack speed, **no longer requires Death Wish** |
    | **Bloodthirst** | No longer heals. Instead gives +10% movement speed for 10 s |
    | **Reckless Swings** | Added 3 Nov (see conflict below) |
    | **Improved Whirlwind** | Added 3 Nov: shorter Whirlwind cooldown and more damage to the closest target (*single source*) |

    !!! conflict "Conflict: Reckless Swings"
        The wiki's research notes describe a pre-launch version that **costs 25% of base health** and adds **+5 rage to your next 4 swings**. RankedBoost's talent list describes it as **healing 0.5% of max health** on your next 3 melee hits after Enrage, Berserker Rage, Bloodrage, Death Wish or Bloodthirst. Both may be accurate for different builds. Read the tooltip in game.

=== "Protection"

    **Shield, threat, mitigation.** Also a surprisingly good solo leveling spec in Forever.

    | Talent | What it does in Forever |
    |---|---|
    | Shield Specialization | **5 rage per block**. The first pick: it fixes your rage economy and leads to Master of Defense |
    | Anticipation · Master of Defense | Defense and avoidance |
    | Improved Revenge | Now adds **damage** instead of a stun |
    | Defiance | Threat, 7/13/20%. **Requires a shield** |
    | Improved Disarm · Improved Shield Wall | As in Classic |
    | **Vanguard** (16) | **Charge in Defensive Stance**. You never have to stance-dance to open a pull |
    | **Bastion** · **Focused Rage** | New; Method recommends both for leveling speed |
    | Shield Slam | Now scales with **block value** |

### Recommended builds

=== "Leveling: Protection (solo)"

    Method recommends this for solo play, and Icy Veins' leveling guide reportedly calls it the fastest Warrior leveling spec, with a slow start before the 16-point tier.

    <div class="steps" markdown>

    1. **Shield Specialization** first, for rage.
    2. **Improved Thunder Clap** and **Improved Bloodrage** for pulls of 2–3 mobs.
    3. Around level 20: **Master of Defense** and **Improved Revenge** (Revenge is now a damage button).
    4. **Vanguard** at the 16-point tier. From here you live in Defensive Stance: Charge, Thunder Clap, Revenge, Shield Slam later.
    5. Then **Bastion** and **Focused Rage**, then Anticipation, Last Stand and Concussion Blow.

    </div>

    Warcraft Tavern's version is similar but leans on Anticipation and Defiance earlier. Both agree on Shield Specialization → Master of Defense → Vanguard.

=== "Leveling: Arms (group)"

    The classic two-hander route, best with a healer or in dungeons.

    <div class="steps" markdown>

    1. **Improved Rend** (AP scaling makes it real damage now), then **Improved Heroic Strike** or **Deep Wounds**.
    2. **Improved Overpower**. Overpower is your main button for most of leveling.
    3. **Sweeping Strikes** as soon as you can. Mobalytics calls it the single most important leveling talent.
    4. **Bloodthrill** (or Weaponmaster if your weapon type benefits a lot).
    5. Skip **Spearing Strike** unless you're fighting giants, dragons or mounted players; Warcraft Tavern suggests maxing Two-Handed Weapon Specialization instead.
    6. **Improved Slam**, then **Mortal Strike**.
    7. Method then goes into Fury for **Unbridled Wrath** and **Enrage**.

    </div>

    !!! conflict "Conflict"
        Warcraft Tavern's Arms build stays in the Arms tree (listed as 26/0/0). Method's is a hybrid that dips into Fury. Both are reasonable; the hybrid suits longer fights.

=== "Leveling: Fury"

    Works, but missed auto attacks leave you short on rage early. Better after level 40 with a good pair of weapons.

    <div class="steps" markdown>

    1. **Cruelty**, then **Unbridled Wrath**, then **Precision** (hit).
    2. **Blood Craze** for sustain.
    3. **Dual Wield Specialization**, then **Death Wish**.
    4. **Enrage** and **Flurry** (Flurry no longer needs Death Wish).
    5. **Bloodthirst** for damage and the movement speed buff.

    </div>

=== "Endgame"

    No community consensus yet: raids open **9 Dec** and nobody has 60-level logs. General direction:

    | Role | Build direction |
    |---|---|
    | **Raid DPS** | Deep Fury: Bloodthirst, Flurry, Raging Blows, Improved Whirlwind, Precision. A two-hander Arms build is likely competitive in the 10- and 20-player raids, which may not have a stack of buffs |
    | **Main tank** | Deep Protection: Defiance, Vanguard, Bastion, Focused Rage, Shield Slam. Threat is high enough now that you may not need Fury dips |
    | **Off-tank / dungeon** | Protection with a few Fury points for Cruelty if the build allows it |
    | **PvP** | Arms: Mortal Strike, Spearing Strike (dismount!), Improved Slam, Weaponmaster |

    *General guidance; no endgame point splits have been published.*

### Dual spec

**Dual specialization** unlocks at **level 40** for **50g** at your class trainer. For a Warrior it's an easy recommendation: keep a **Protection** spec for dungeons and a **damage** spec (Arms for questing and PvP, Fury for raids). Respec fees decay to 1g over time. See [Dual specialization](../../characters/leveling.md#dual-specialization).

---

## Abilities & rotation

### Key abilities by level

From Method's leveling guide; Victory Rush and Tactical Mastery are Forever baseline.

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
        2. Revenge whenever it lights up
        3. Sunder Armor
        4. Heroic Strike as a rage dump when above ~50 rage.

        </div>

    **Multi-target:** open with **Thunder Clap** (usable in Defensive Stance, 6 s cooldown, now scales with AP), Demoralizing Shout, then tab-Sunder and Cleave.

    **Opening:** with **Vanguard** you Charge without leaving Defensive Stance. Without it, Charge in Battle Stance, swap (Tactical Mastery keeps 10 rage), then Thunder Clap.

=== "Arms"

    !!! rotation "Arms: Leveling"

        <div class="priority" markdown>

        1. Charge
        2. Rend
        3. Auto-attack
        4. **Overpower** every time it lights up
        5. Mortal Strike on cooldown
        6. Slam (15 s cooldown now)
        7. Heroic Strike only with spare rage.

        </div>

        Keep Demoralizing Shout up on packs. Pop **Sweeping Strikes** on two targets, then Whirlwind or Cleave.

    **Pool rage:** don't spend your last rage on a mob that's about to die. Carry it into the next pull. Finish low mobs with **Victory Rush** for the heal.

=== "Fury"

    !!! rotation "Fury priority"

        <div class="priority" markdown>

        1. Bloodthirst on cooldown
        2. Whirlwind on cooldown
        3. Heroic Strike (or Cleave on 2+ targets) above ~50 rage
        4. Execute below 20% health.

        </div>

        Stay in **Berserker Stance**. Use Bloodrage and Berserker Rage on cooldown for rage.

    **Cooldowns:** Death Wish and Recklessness together in raids. Death Wish now increases damage taken, so mind your health.

### Cooldowns

Recklessness, Retaliation and Shield Wall **no longer share a cooldown** in Forever. Retaliation and Shield Wall are now 15-minute cooldowns, so you can use one without losing the others.

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
        Put Revenge, Overpower and Victory Rush on easy keys. They're reactive and you'll press them constantly. With Vanguard, most Protection Warriors can drop their stance-swap Charge macro.

---

## Leveling walkthrough 1–60

!!! warning "Slow start, fast finish"
    In the beta, Warriors were among the slowest classes to level. Normal mobs take about 10–15 s solo. Buy or quest every weapon upgrade you can: Method estimates almost all of your leveling damage comes from your weapon. Group up for elites and dungeon quests, which give much more XP in Forever.

Zone suggestions below follow the Classic-era leveling order plus the new zones. Forever doesn't show zone level ranges in game; see [Zones](../../world/zones.md).

<div class="route" markdown>

### 1–10: Starting zone

| | Alliance | Horde |
|---|---|---|
| **Zones** | Elwynn Forest · Dun Morogh · Teldrassil · [Zephras Isle](../../world/zephras-isle.md) | Durotar · Mulgore · Tirisfal Glades · Zephras Isle |
| **Train** | Battle Shout, Charge and Rend (4), Hamstring (8) | Same |
| **Talents** | None until 10 (earlier with Talented) | Same |

- Do every quest. Take every weapon reward and **sell your starting weapon** the moment a better one drops.
- Learn **Cooking** and do **The Great Outdoors** (around level 5) to unlock [camping](../../systems/camping.md). Campfire rested bonus helps a slow class.
- Pick up a gathering profession from the starter quest (+2 skill). Mining suits Warriors (see [Professions](#professions-legacy)).
- At **10**, take the **Defensive Stance** quest from your class trainer. It rewards Defensive Stance, Sunder Armor and Taunt, and a follow-up gives a one-hander.

### 10–20

| Alliance | Horde |
|---|---|
| Westfall, Loch Modan, Darkshore, Redridge (from ~15) | The Barrens, Silverpine Forest, Stonetalon Mountains (from ~15) |

- **Talents start.** Protection: Shield Specialization first. Arms: Improved Rend.
- At **14**, Tactical Mastery is baseline: stance-dancing for Overpower is cheap now.
- Dungeons: **Ragefire Chasm** (13–18), **[Hall of Thanes](../../content/dungeons/hall-of-thanes.md)** (13–18, Ironforge), **[Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md)** (15–22, Tirisfal), **Deadmines** and **Wailing Caverns** (late teens). New-dungeon bosses reportedly drop a guaranteed blue.
- Supply camps open: **Three Corners** in Redridge (Alliance) and west of the **Crossroads** (Horde).
- From 14, the **Cozy Sleeping Bag** scavenger hunt is worth doing for its XP buff.

### 20–30

| Alliance | Horde |
|---|---|
| Duskwood, Wetlands, Ashenvale, Hillsbrad Foothills | Hillsbrad Foothills, Ashenvale, Thousand Needles, Stonetalon |

- **Victory Rush** at 20 is a big quality-of-life upgrade. Use it to finish every mob.
- **Polearms** become trainable at 20.
- **Library books:** turning in **10 books** unlocks a Warrior quest at **20**, and the later tiers unlock at 35 and 45. Forever hasn't documented the Warrior rewards yet. Pick up class books whenever they drop.
- Arms reaches the 16-point tier around here; Protection players get **Vanguard**.
- Dungeons: **Shadowfang Keep**, **Blackfathom Deeps**, **The Stockade**, **[Excavation Site: Wetlands](../../content/dungeons/excavation-site.md)** (24–29), **[City of Dalaran](../../content/dungeons/city-of-dalaran.md)** (28–33, hostile to the Horde).
- **25:** first Warrior class milestone for a **Legacy Point** (Novice).
- At **30**, take the **Berserker Stance** quest (trainer sends you to Fray Island near Ratchet; Classic-era quest, *check in game*). Also start the **Whirlwind Axe** chain in Alterac Mountains; Method warns it's hard at 30, so bring a friend or buy the reagents on the Auction House.

### 30–40

| Alliance | Horde |
|---|---|
| Arathi Highlands, Stranglethorn Vale, Desolace, Alterac Mountains | Arathi Highlands, Stranglethorn Vale, Desolace, Thousand Needles |

- **Whirlwind** at 36.
- **[Riverglades](../../world/zones.md#riverglades)** opens around **35** (contested, 150+ quests). Alliance base: **Farholde Keep**. Horde base: **Rog'mar**. Reach it from Redridge, Badlands, Swamp of Sorrows, Burning Steppes, or the Tanaris ferry.
- Desolace centaur quests now need level 35.
- Dungeons: **Razorfen Kraul**, **Gnomeregan**, **Scarlet Monastery** (all four wings), **[The Drowned City](../../content/dungeons/drowned-city.md)** (35–40).
- **35:** second library-book tier (20 books). Artisan professions open.
- At **40**: **plate**, **Apprentice Riding** (100g including your first mount) and **dual spec** (50g). Budget about 150g.

### 40–50

| Alliance | Horde |
|---|---|
| Riverglades, Dustwallow Marsh, Badlands, Swamp of Sorrows, Tanaris, Feralas, Hinterlands | Riverglades, Dustwallow Marsh, Badlands, Swamp of Sorrows, Tanaris, Feralas, Hinterlands |

- Swap leather and mail for plate gradually; don't trade a big weapon upgrade for armor.
- **45:** final library-book tier (25 books) and the second Warrior Legacy Point (Experienced).
- Dungeons: **Razorfen Downs**, **[Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md)** (40–45, Riverglades), **Uldaman**, **Zul'Farrak**, **[Alcaz Prison](../../content/dungeons/alcaz-prison.md)** (48–53, Dustwallow), **Maraudon**.
- The Darkspear Islands battleground opens from level 30, in brackets of 10. It's a decent break from questing.

### 50–60

| Alliance | Horde |
|---|---|
| Azshara, Un'Goro Crater, Felwood, Searing Gorge, Burning Steppes, Western/Eastern Plaguelands, Winterspring, Silithus | Same |

- **Azshara** has many new quests and **[Blackmaw Hold](../../content/dungeons/blackmaw-hold.md)** (55–60). Un'Goro's north holds **[Shaper's Terrace](../../content/dungeons/shapers-terrace.md)** (58–60).
- Run **Sunken Temple**, **Blackrock Depths** and **Lower Blackrock Spire** for pre-raid gear while you level.
- At **60**: third Warrior Legacy Point (Master). Head to **[Mount Hyjal](../../world/zones.md#mount-hyjal)** through Darkwhisper Gorge in Winterspring. Epic riding is 1,000g.

</div>

---

## Dungeons

**As tank:** with +80% Defensive Stance threat, holding single targets is easy. Packs still need Thunder Clap, Demoralizing Shout and tab-Sundering. There are no Meeting Stone summons, so expect to walk to every entrance; Vanguard makes chain pulls fast.

**As DPS:** let the tank build threat for a couple of seconds. Death Wish raises damage taken, so don't use it during trash pulls you're not sure about.

**Notable dungeons for Warriors**

| Level | Dungeon | Why |
|---|---|---|
| 13–20 | [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) · Ragefire Chasm | First chance at a blue weapon |
| 15–22 | [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) | Six bosses, good Horde early run |
| 18–24 | The Deadmines | Classic weapon drops |
| 24–33 | [Excavation Site](../../content/dungeons/excavation-site.md) · [City of Dalaran](../../content/dungeons/city-of-dalaran.md) | New loot themed to class and spec |
| 34–45 | Scarlet Monastery (Armory, Cathedral) · [The Drowned City](../../content/dungeons/drowned-city.md) | Arms two-hander upgrades; prot practice |
| 40–55 | [Krol'dok](../../content/dungeons/kroldok-stronghold.md) · Zul'Farrak · [Alcaz Prison](../../content/dungeons/alcaz-prison.md) | Plate and weapon upgrades as you enter plate |
| 55–60 | BRD · LBRS/UBRS · [Blackmaw Hold](../../content/dungeons/blackmaw-hold.md) · [Shaper's Terrace](../../content/dungeons/shapers-terrace.md) · Scholomance · Stratholme · Dire Maul | Pre-raid gear |

See the full [dungeon list](../../content/dungeons/index.md).

---

## Raid preparation

All three launch raids open on **9 December 2026**. There's no difficulty mode, so preparation (gear, consumables, strategy) is what matters. See [Raids](../../content/raids/index.md).

| Raid | Size | Warrior role |
|---|---|---|
| [The Barrow Deeps](../../content/raids/barrow-deeps.md) | 10 | Likely one tank Warrior plus 1–2 DPS. In small raids, an off-tank who can DPS is valuable |
| [Hyjal Summit](../../content/raids/hyjal-summit.md) | 20 | Two or three tanks; Fury and Arms DPS. Split routes may need two tank teams |
| [Onyxia's Lair](../../content/raids/onyxias-lair.md) | 40 | Main tank holds Onyxia; fire resistance helps. Needs the **Drakefire Amulet** attunement through UBRS |

**Pre-raid gear approach:** Forever's loot isn't fully documented and dungeon items carry stats themed to spec. So nobody has a reliable pre-raid best-in-slot list yet. In general:

- **Tanks:** stack Stamina, Defense and armor first, then avoidance and block value (Shield Slam scales with it). Hit helps threat.
- **DPS:** get to the hit cap with crit and Strength; your **weapon** is still your biggest upgrade.
- Farm reputation and Honor for gap fillers; PvP blues can be good early raid gear.

**Consumables to stock:** health potions (now made by **First Aid**), Elixirs of the Mongoose/Giants or their Forever equivalents, weapon stones from Blacksmithing, Rage potions, and food buffs (the Legacy talent *Gourmand* makes them last longer). World buffs from the Chronoboon Displacer **don't work in raids** in Forever.

---

## PvP

Arms is the PvP spec: **Mortal Strike** for healing reduction, **Hamstring** to stick, **Spearing Strike** to dismount riders (double damage to mounted targets), and **Improved Slam** that no longer resets your swing.

- **Battlegrounds:** Warsong Gulch, Arathi Basin, Alterac Valley and the new **[Battle for the Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands)** (15v15, levels 30–60). In Darkspear, Warriors are good flag carriers and base defenders. Spearing Strike punishes anyone riding between bases.
- **World PvP:** on PvP realms you're almost always at risk. Victory Rush heals after every kill, and Charge/Intercept win fights against careless casters.
- **Progression:** a seasonal Rank 1–14 system with Honor gear. See [PvP](../../content/pvp/index.md).

**Matchups (general Classic-era guidance)**

| Opponent | Notes |
|---|---|
| Mage | Hardest matchup. Save Intercept/Charge for after Blink; trinket or racial out of Polymorph or Frost Nova |
| Rogue | Win with Mortal Strike and Hamstring; Retaliation and the racial break their burst |
| Hunter | Close the gap fast; Intercept after Concussive Shot. Line-of-sight their pet |
| Priest / Shaman / Druid | Mortal Strike their heals. Stay on them through fear and roots |
| Paladin | Long fights; save burst for when Divine Shield is down |
| Warrior | Whoever lands Mortal Strike and Hamstring first usually wins |

---

## Gear, stats & enchants

| Spec | Stat priority (general) |
|---|---|
| **Protection** | Stamina = Defense > armor > Dodge/Parry/Block > Block value (for Shield Slam) > Hit (threat) > Strength |
| **Arms** | Weapon damage and speed > Hit (to cap) > Crit > Strength > Agility |
| **Fury** | Hit (dual-wield) > Crit > Strength > Agility. Fast off-hand, good main hand |

*No source has published Forever-specific stat priorities yet. These follow Classic logic adjusted for Forever's changes.*

**Forever changes that affect gear:**

- **Crits give +75% rage**, so crit is worth more than in Classic for every spec.
- Rage from dealing damage depends on **weapon speed**, so slow two-handers are still the best Arms choice.
- **Weaponmaster** decides your Arms weapon type: axes and polearms (crit), maces and staves (armor penetration), swords (extra attacks).
- Armor no longer reduces rage from being hit, so tanks don't lose rage as they gear up.
- Dungeon items roll themed stats, and looting an item unlocks its transmog.

**Enchants:** Crusader on weapons (or the Forever equivalent) for DPS; Stamina, Agility and Defense for tanks. Blacksmithing weapon stones are a cheap flat damage boost while leveling.

---

## Professions & Legacy

**Professions**

| Pair | Why |
|---|---|
| **Mining + Blacksmithing** | The classic Warrior pair. Weapon stones, plate, many new BoP patterns. Mining's camp feature (**Lodestone**) adds melee AP |
| **Mining + Engineering** | Bombs and gadgets for PvP; Warcraft Tavern rates Engineering highly |
| **Skinning + Mining** (leveling) | Money for your mount at 40. Skinning's **Camp Chair** gives +2% crit |
| **First Aid** | Mandatory secondary skill: it now makes **health potions** as well as bandages |

Professions give no passive stat bonuses in Forever; their value is crafting, gathering and [camping](../../systems/camping.md). Crafting professions also award Legacy Points at 150/225/300. See [Professions](../../characters/professions.md).

**Legacy talents** (16 points per character at launch)

| Pick | Why |
|---|---|
| **Well Rested** (5) → **Talented** (5) | Warriors level slowly; rested XP and earlier talents help most |
| **Thrill of Adventure** | Restores health on kills in the open world; less downtime |
| **Field Medicine** | Bandage more often |
| **Reinforce** | Tanks and Hardcore players die and repair more |
| **For Great Honor** | If you plan to PvP |

See [Legacy](../../characters/legacy.md).

---

## Hardcore notes

!!! hardcore "Hardcore survival"

    The Hardcore ruleset arrives in winter. Warrior is a demanding Hardcore class because you can't heal or escape well. Tips:

    - **Level as Protection** with a shield. You give up some kill speed and gain a lot of safety.
    - Never pull more than you can Thunder Clap down; keep **Retaliation** and **Shield Wall** for emergencies (they don't share a cooldown now).
    - Carry bandages and potions (First Aid makes both), and use Victory Rush to top up.
    - Pick a race with an escape or survival racial: Will to Survive (Human), Stoneform (Dwarf), Escape Artist (Gnome), Shadowmeld (Night Elf), War Stomp (Tauren), Will of the Forsaken (Undead).
    - Legacy points earned on Hardcore apply to other rulesets, but not the other way around.

    See [Hardcore](../../about/hardcore.md).

---

## Common mistakes & FAQ

??? question "Why do I run out of rage?"
    Early on, it's usually your weapon. Rage from hitting now depends on weapon speed, so slow, hard-hitting weapons give more. Use Bloodrage, take Shield Specialization (Prot) or Improved Overpower (Arms), and don't spend rage on mobs that are about to die.

??? question "Is Protection really good for leveling?"
    In Forever, yes. Vanguard lets you Charge in Defensive Stance, Thunder Clap works in Defensive Stance, Revenge does damage, and Shield Specialization gives rage. Several guides recommend it for solo play.

??? question "Do I still need to stance-dance?"
    Less. Tactical Mastery is baseline (10 rage kept), and Improved Tactical Mastery adds up to 15 more. Arms still swaps for Overpower; Protection with Vanguard hardly swaps at all.

??? question "Should I pick Bloodthrill or Weaponmaster?"
    Sources disagree. Warcraft Tavern takes Bloodthrill for more Overpower; Method takes both. If your weapon type gains a lot from Weaponmaster (for example, an axe or polearm for crit), take it.

??? question "Is Skyborne a good Warrior race?"
    It's fine for leveling (haste, a glide, and a speed or regen cooldown), but Warcraft Tavern rates it weak for Warriors compared with Orc, Human, Troll or Tauren. Pick it for looks and story.

**Common mistakes**

- Keeping your quest-reward weapon too long. Check the Auction House at every level.
- Using Heroic Strike when you don't have spare rage.
- Skipping First Aid now that it makes health potions.
- Forgetting the level 10 and 30 stance quests.
- Tanking without Defiance and a shield (Defiance requires one).

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
