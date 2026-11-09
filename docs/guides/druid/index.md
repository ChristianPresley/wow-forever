---
description: "Druid guide for WoW: Forever: specs and talents, rotations, a 1–60 leveling route, dungeons, raids, PvP, gear and Hardcore tips."
tags:
  - Druid
search:
  boost: 2
---

# Druid Guide

<div class="guide-head" data-class="druid" markdown>

:codex-druid:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Class guide</span> **Tank**{ .badge .tank } **Healer**{ .badge .heal } **DPS**{ .badge .dps }

<nav class="gh-jump" aria-label="Jump to section"><a href="#specs-talents">Talents</a> <a href="#abilities-rotation">Rotation</a> <a href="#leveling-walkthrough-160">Leveling</a> <a href="#dungeons">Dungeons</a> <a href="#raid-preparation-9-december">Raids</a> <a href="#pvp">PvP</a> <a href="#gear-stats-enchants">Gear</a> <a href="#hardcore-notes">Hardcore</a></nav>

</div>

!!! info "Status: 7 November 2026"
    This page was written 3 days after launch (Patch 1.60.1). The sources are the pre-launch development notes, launch-week hotfixes and the first community guides. Talent calculators still change. Thus, **the builds on this page list key talents and milestones, not exact point-by-point orders**. Check the [Druid reference page](../../characters/classes/druid.md) for the raw list of changes.

## Overview

The Druid is the most flexible hybrid class. With 1 character, you can tank (Bear), do melee damage (Cat), cast at range (Balance/Moonkin) or heal (Restoration). You can also change between the first 2 roles during a fight.

The main change in Forever is that **forms no longer have large disadvantages**. Potions, most consumables, weapon enchants and procs all work in form. Form auto-attacks use the DPS of your weapon. You can use most doors and objects and stay in form.

<aside class="infobox" markdown>
<p class="infobox-title">Druid at a glance</p>

| | |
|---|---|
| **Roles** | Tank (Bear), melee DPS (Cat), ranged DPS (Balance), healer (Restoration) |
| **Armor / weapons** | Leather (cloth and leather early), staves, maces, daggers, fist weapons, polearms (trainer at 20), off-hand items |
| **Resources** | Mana (caster), Rage (Bear), Energy (Cat). In form, you cannot see your mana unless you turn on the Personal Resource Display |
| **Factions** | **Both**{ .pill .pill--neutral-faction } |

</aside>

<div class="proscons" markdown>
<div class="pros" markdown>

Strengths

- Best solo leveling kit in the game for a melee class: stealth, sprint, self-heals, a speed form at 30 and no pet to manage.
- Feral can change between tank and DPS without a respec. With +115% bear threat in Forever, Bear is a real dungeon tank.
- Gives unique raid utility: Innervate, Rebirth (combat resurrection), Mark of the Wild, Moonkin Form or Leader of the Pack crit auras.
- Forever's baseline additions (Omen of Clarity at 20, Revive at 12, Nature's Grasp at 10) mean that you no longer spend talent points on these spells.

</div>
<div class="cons" markdown>

Weaknesses

- Gear competition: Feral needs leather with Strength/Agility. Balance and Resto need caster leather and cloth. You need 2 gear sets for dual spec.
- Shifting costs mana. In long fights, you can still run out of mana if you shift too much.
- Balance uses a lot of mana when you level: you spend mana to kill and to heal.
- Important bear tools (Dire Bear, Lacerate) come at levels 25–40. Thus, at low levels, a Bear is a weaker tank than a Warrior or Paladin.

</div>
</div>

### What's new in Forever

- **Cat:** Shred 200% weapon damage (was 155%), Claw 140%, Ravage 435%. Rip, Rake, Ferocious Bite and Pounce scale about 25% more.
- **Bear:** +115% threat, Swipe hits 3 targets with AP scaling, Growl works like Taunt, Frenzied Regeneration can heal to full.
- *Furor* (Energy regenerates out of Cat Form at 5/5) and the talent *Shifting Power* (instant 40 Energy for mana) **replace Powershifting**.
- **New baseline:** Omen of Clarity (20), Revive (12), Nature's Grasp (10), Poised (32: next Energy ability costs 10 less), Faerie Fire usable in forms (free, 6 s cooldown), Barkskin usable in forms, Entangling Roots indoors, no Hurricane cooldown.
- **Removed:** Berserk (pre-launch), Mangle (replaced by Primal Bite), Tiger's Fury (replaced by Shifting Power).
- **Launch hotfixes:** a 4 Nov hotfix adjusted Druid damage and threat. A 6 Nov hotfix made **Bloom** heal correctly. It also stopped Night Elf druids in Shadowmeld from opening with Ravage or Pounce.

### Races

| Race | Faction | Status | Add-on |
|---|---|---|---|
| Night Elf | **Alliance**{ .pill .pill--alliance } | Classic | [Night Elf Druid](night-elf.md) |
| Skyborne (High Order) | **Alliance**{ .pill .pill--alliance } | **New**{ .pill .pill--new .pill--sm } | [High Order Skyborne Druid](skyborne-high-order.md) |
| Tauren | **Horde**{ .pill .pill--horde } | Classic | [Tauren Druid](tauren.md) |
| Skyborne (Windshaper) | **Horde**{ .pill .pill--horde } | **New**{ .pill .pill--new .pill--sm } | [Windshaper Skyborne Druid](skyborne-windshaper.md) |

Community guides call the race differences **marginal**. Select your faction and appearance first. See [Races](../../characters/races.md) for every racial.

---

## Specs & talents

Forever changed all 3 trees. It also added a **16-point tier** to the classic 11/21/31 tiers. **Dual spec** unlocks at **level 40** for **50g** from your class trainer. Use it: the usual pair is Feral (tank/cat) plus either Restoration or Balance.

=== "Balance"

    **Role:** ranged caster DPS. Raid crit aura with Moonkin Form.

    <div class="milestones" markdown>

    Early
    :   **Genesis** (bonus periodic damage), **Improved Wrath** (cheaper, faster Wrath), **Nature's Majesty** (crit), **Nature's Reach** (spell hit and range)

    11
    :   **Nature's Splendor**

    16
    :   **Insect Swarm** (moved here from Resto)

    Mid
    :   **Overgrowth** (Roots several targets. With 2 points, you can root a maximum of 3 targets, per Warcraft Tavern), Moonglow, improved Nature's Grace

    Deep
    :   **Eclipse** (Wrath makes your next Starfires faster)

    Capstone
    :   **Moonkin Form**: party/raid crit for spells and attacks. Doubles Omen of Clarity procs. Does **not** stack with Leader of the Pack

    </div>

=== "Feral"

    **Role:** Cat melee DPS and Bear tank, from one tree.

    <div class="milestones" markdown>

    Early
    :   **Ferocity** (cheaper Maul/Swipe and Cat abilities), **Feral Instinct**, **Thick Hide**, **Feral Swiftness** (Cat speed, works indoors, adds dodge in all forms), **Savage Fury**

    11
    :   **Feral Charge** (now has a Cat version. The Bear version interrupts)

    Mid
    :   **Shredding Attacks**, **Predatory Discipline**, **Natural Instinct**, **Natural Reaction** (dodge, plus Rage when you dodge)

    16
    :   **Shifting Power** (Cat: instant 40 Energy for mana, 16 s cooldown, 8 s when improved) and **Primal Bite** (Bear: the Mangle replacement, high threat)

    21
    :   **Leader of the Pack** (party crit aura)

    Deep
    :   **Predatory Strikes**, **Rend and Tear**, **Blood Frenzy**, **Lacerate** (now a talent)

    </div>

    **Furor 5/5** lets Energy regenerate outside Cat Form and gives Rage when you shift into Bear.

=== "Restoration"

    **Role:** healer. Focus on HoTs, strong when you move.

    <div class="milestones" markdown>

    Early
    :   **Heart of the Wild** (changed places with Furor), **Naturalist** (now also +2–10% damage), **Reflection** (a maximum of 50% mana regen when you cast, at max rank)

    11
    :   **Gift of the Earthmother**: −0.5 s global cooldown on Rejuvenation, Swiftmend and Wild Growth

    16
    :   **Swiftmend** (consumes 1 of **your own** HoTs)

    Mid
    :   **Living Spirit**, Nature's Swiftness, Improved Tranquility

    Tier 3
    :   **Bloom** (added before launch. Fixed on 6 Nov so that it heals)

    Capstone
    :   **Wild Growth** (31 points, 3 s cast in the pre-launch notes)

    </div>

### Recommended builds

!!! warning "No point-by-point orders yet"
    All major sites publish their builds as calculator links or images. Some sites still mark them "expected, not final". The milestones below are the consensus. Put them into an in-game or site calculator. Do not trust an exact order that you read today.

| Build | Use | Milestones |
|---|---|---|
| **Feral leveling** (recommended) | 10–60 solo | See the [Feral leveling timeline](#feral-leveling-timeline) below |
| **Balance leveling** | Solo caster | Genesis to unlock Nature's Majesty and Nature's Reach, Improved Wrath, Nature's Splendor, Insect Swarm (16-point), 2 points of Overgrowth for multi-root pulls, then Eclipse. |
| **Hybrid Feral (endgame)** | Cat DPS + off-tank | Warcraft Tavern's 9/37/5-style hybrid: Balance for Nature's Reach (hit), the full Feral tree including Shifting Power, Primal Bite, Leader of the Pack and Lacerate, and a few Resto points. *The page does not say which number is which tree.* |
| **Bear tank (endgame)** | Main tank in 5s, 10s | Feral with Thick Hide, Feral Instinct, Natural Reaction, Ferocity, Primal Bite, Lacerate, Rend and Tear. Kami-labs skips Brutal Impact. Commenters suggested that you move points to Nature's Reach/Majesty for hit and crit. |
| **Restoration (endgame)** | Raid/dungeon healer | Heart of the Wild, Reflection, Gift of the Earthmother, Swiftmend, Living Spirit, Nature's Swiftness, Bloom, Wild Growth. |
| **Moonkin (endgame)** | Raid caster | Deep Balance through Eclipse and Moonkin Form. |

<p class="milestones-cap" id="feral-leveling-timeline">Feral leveling timeline</p>

<div class="milestones" markdown>

Lv 10–15
:   Ferocity, then Feral Instinct/Thick Hide for Bear

Lv 20
:   Feral Swiftness and Savage Fury for Cat

11 pts
:   Feral Charge

16 pts
:   Shifting Power (and Primal Bite if you tank dungeons)

21 pts
:   Leader of the Pack

Then
:   Predatory Strikes and the Cat damage talents. Warcraft Tavern skips Shredding Attacks for leveling. Finish with Furor or Balance hit talents.

</div>

!!! conflict "Conflict: talent names"
    Warcraft Tavern calls the Cat speed talent *Feral Swiftness*. Method calls it *Feline Swiftness*, with a different spell ID. They seem to be the same slot in the tree. It is possible that the talent has a new name.

---

## Abilities & rotation

### Key spells by level

The data comes from trainer and quest tables on Warcraft Tavern and Method. Levels with the mark *(fan)* come from a single summarized source.

| Level | Spell | Notes |
|---|---|---|
| 1 | Wrath, Healing Touch, Mark of the Wild | |
| 4–6 | Moonfire, Rejuvenation, Thorns | Thorns scales with spell power in Forever |
| 8 | Entangling Roots | Works indoors now |
| 10 | **Bear Form**, Teleport: Moonglade, **Nature's Grasp** | Bear Form from a class quest |
| 12 | **Revive**, Enrage *(fan)* | Revive = out-of-combat resurrection |
| 14 | Cure Poison (quest), Bash *(fan)* | |
| 16 | **Aquatic Form** (quest), Swipe *(fan)* | |
| 18 | Faerie Fire, Hibernate | Faerie Fire usable in forms |
| 20 | **Cat Form**, Prowl, Claw, Rip (quest); **Rebirth**; **Omen of Clarity** (passive) | Polearm training is also available |
| 22–26 | Soothe Animal, Remove Curse, Dash, Abolish Poison | |
| 25 | Insect Swarm (talent), Lacerate (talent) | |
| 28 | Challenging Roar, Cower *(fan)* | |
| 30 | **Travel Form**, Tranquility *(fan)* | Travel Form is +40% speed outdoors |
| 32 | Track Humanoids, Ravage, **Poised** | |
| 36 | Frenzied Regeneration, Pounce *(fan)* | |
| 40 | **Dire Bear Form**, **Innervate**, Feline Grace, Dual Spec, riding | |

### Rotations

=== "Cat"

    **Opener:** Prowl → Ravage (or Pounce in PvP) from behind. Before level 32, use Shred from behind or Claw.


    !!! rotation "Cat priority"

        <div class="priority" markdown>

        1. Faerie Fire (free in form) if it is missing.
        2. **Rip** at 5 combo points on targets that will live until it ends.
        3. **Ferocious Bite** at 4–5 combo points with 70+ Energy, or as the finisher on targets that are about to die.
        4. **Rake** if it's missing.
        5. **Shifting Power** when you have less than 50 Energy and it is not on cooldown.
        6. **Shred** from behind, **Claw** from the front.

        </div>


    Do not refresh bleeds until they expire. When you solo, cast Thorns before the pull for free damage. *Poised* (32) makes your next Energy ability cost 10 less. After it procs, use the cheap ability. Omen of Clarity procs make your next ability free. Use them on Shred.

=== "Bear"


    !!! rotation "Bear: Single target"

        <div class="priority" markdown>

        1. Keep Faerie Fire and **Demoralizing Roar** active.
        2. **Primal Bite** on cooldown (main threat button).
        3. **Lacerate** to 5 stacks. Refresh it before it expires.
        4. **Maul** as a Rage dump (25+ Rage).

        </div>


    **Multi-target:** Swipe (3 targets) between Primal Bites. Challenging Roar for emergencies.

    **Defensive:** Barkskin (now usable in form), Frenzied Regeneration (can heal to full), Enrage for Rage on the pull. Use Feral Charge (Bear) as an interrupt.

    Kami-labs' bear simulation put Maul, Lacerate and Primal Bite at about 35/26/16% of damage. The exact numbers will change after the 4 Nov threat hotfix, but the general pattern stays the same.

    !!! conflict "Conflict: opener"
        Warcraft Tavern's leveling guide stacks Lacerate before Primal Bite. Its Feral guide and Kami-labs' simulation use Primal Bite first. A Primal Bite opener is safer for threat.

=== "Balance"

    !!! rotation "Balance: Leveling (multi-DoT)"

        <div class="priority" markdown>

        1. Wrath to pull
        2. Moonfire
        3. Insect Swarm
        4. Entangling Roots
        5. Kite, or continue to cast Wrath.

        </div>

        With Overgrowth, root and DoT 2–3 mobs.

    **Leveling (Eclipse):** Wrath, Moonfire, Insect Swarm, Wrath until level 30. Then Wrath procs Eclipse, so the pattern becomes about **2 Starfire : 1 Wrath**.

    **Raid:** if the fight is long, keep Moonfire and Insect Swarm on the target. Use Wrath to trigger Eclipse, then cast Starfire during Eclipse. For AoE packs, use Hurricane, which has no cooldown. Before launch, the base damage of Starfire increased by about 40%.

=== "Restoration"

    !!! rotation "Restoration"

        - Pre-HoT the tank with **Rejuvenation** (shorter GCD because of Gift of the Earthmother).
        - **Regrowth** for medium damage, **Healing Touch** (downranked) for big, planned heals.
        - **Swiftmend** needs 1 of your own HoTs on the target. Use it on spikes.
        - **Wild Growth** for group damage. **Bloom** is your tier-3 tool, because it now heals.
        - **Nature's Swiftness → Healing Touch** for emergencies. **Innervate** yourself or another healer. **Rebirth** a dead healer or tank.

### Useful macros

??? example "Show 3 macros"

    ```text
    #showtooltip
    /cast [nostance:1] !Dire Bear Form; Primal Bite
    ```

    ```text
    #showtooltip
    /cast [stance:3,nostealth] Prowl; [nostance:3] !Cat Form
    ```

    ```text
    #showtooltip Innervate
    /cast [@mouseover,help,nodead][] Innervate
    ```

    !!! note
        Stance numbers depend on which forms you know. Check which form is 1, 2 and 3 on your stance bar. Forever's client supports modern macro conditionals (*mouseover* targeting). See [Addons & UI](../../systems/addons.md).

---

## Leveling walkthrough 1–60

**Spec:** Feral is the consensus. Cats have Prowl, Dash and almost no downtime. Balance works, but it runs out of mana. Restoration is good only if you play in a group or do dungeons.
**Pace:** the developers estimate about 20 hours for levels 1–20. Quests give much more XP than dungeon mobs. See [Leveling](../../characters/leveling.md).

!!! tip "First 20 levels in one line"
    Caster until 10, Bear 10–20, Cat from 20. Go to the trainer at every even level.

<div class="route" markdown>

### 1–10: Caster

| | **Alliance**{ .pill .pill--alliance } | **Horde**{ .pill .pill--horde } |
|---|---|---|
| Night Elf / Tauren | Shadowglen → Dolanaar (Teldrassil) | Camp Narache → Bloodhoof Village (Mulgore) |
| Skyborne | Thendal Village → Shen'dar Village ([Zephras Isle](../../world/zephras-isle.md)) | same, phased |

- Spam **Wrath**. Open with **Moonfire**. Heal with **Rejuvenation**, then melee. Use Healing Touch between pulls.
- At about level 5, take **The Great Outdoors** to unlock [camping](../../systems/camping.md). Select a gathering profession from the starter quest.
- You get your first talent point at 10 (earlier with the Legacy talent *Talented*).
- **Level 10:** take the **Bear Form quest**, *Heeding the Call* in Teldrassil and Mulgore, or *The Great Ursera Spirit* on Zephras Isle. It also teaches Teleport: Moonglade.

### 10–20: Bear

- **Zones:** Alliance — Darkshore, then Westfall/Loch Modan via the new **Stormwind Harbor ↔ Auberdine** boat, or Redridge. Horde — the Barrens, then Silverpine or Stonetalon. Skyborne finish Zephras Isle (to about 12–14), then take the airship (High Order to Dalaran, Windshapers to Mulgore). See each race add-on for the route.
- **Rotation:** pull with 2 Wraths and a Moonfire. Then shift to Bear and use Enrage, Demoralizing Roar and Maul. Use Swipe for groups.
- **Talents:** Ferocity first, then Feral Instinct/Thick Hide. Some guides prefer to start with Cat damage talents and to stay in caster form until 20.
- **Quests:** Cure Poison at 14 (*Lessons Anew*) and **Aquatic Form at 16** (*A Lesson to Learn*). Do both quests. Aquatic Form saves a lot of time.
- **Dungeons:** [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) (13–18, Ironforge), Ragefire Chasm, [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) (15–22, Tirisfal), Wailing Caverns, Deadmines. You can tank these, but a Warrior or Paladin will hold aggro more easily before Lacerate.
- **Gear:** any leather with Strength or Agility. Stamina is good. Ignore Spirit when you play as Bear.

### 20–30: Cat

- **Level 20:** the **Cat Form quest**, *The Great Cat Spirit* (Night Elf and Tauren) or *The Great Windborne Cat Spirit* (Skyborne, Zephras Isle). It also teaches Prowl, Claw and Rip. Omen of Clarity and Rebirth are now baseline. Get polearm training.
- **Library books (first unlock):** when you turn in **10 class library books**, you unlock a level-20 quest. The books drop as loot. You turn them in to Garion Wendell (Wizard's Sanctum, Stormwind) or Owen Thadd (Magic Quarter, Undercity), per the research notes. There are no published rewards for Druid yet.
- **Zones:** Alliance — Ashenvale, Wetlands, Redridge, Duskwood, Hillsbrad. Horde — Stonetalon, Ashenvale, Hillsbrad, Thousand Needles.
- **Talents:** Feral Swiftness, Savage Fury, Feral Charge (11), then work toward Shifting Power (16).
- **Dungeons:** Shadowfang Keep, Blackfathom Deeps, Stockade, [Excavation Site: Wetlands](../../content/dungeons/excavation-site.md) (24–33), [City of Dalaran](../../content/dungeons/city-of-dalaran.md) (28–35. Horde players are attacked in Dalaran). Insect Swarm and Lacerate (talents) become available at about 25.
- **Level 25:** your first Legacy class tier (*Novice*) if you're the first Druid on your account.
- **Level 30:** **Travel Form** (+40% outdoors). This is your mount for the next 10 levels.

### 30–40: Cat, Travel Form

- **Zones:** Alliance — Arathi Highlands, Alterac (Dalaran), Desolace, Stranglethorn, Dustwallow. Horde — Desolace, Arathi, Stranglethorn, Dustwallow. New at 35–45: **[Riverglades](../../world/zones.md#riverglades)** (contested. Farholde Keep for Alliance, Rog'mar for Horde). **Shen'dralas** south of Desolace has an unknown level range.
- **Level 32:** Ravage, Poised, Track Humanoids. Your opener is now Prowl → Ravage.
- **Level 35:** second library book unlock (**20 books**). Desolace centaur quests now need level 35.
- **Talents:** Shifting Power at 16 points, Leader of the Pack at 21, then Predatory Strikes.
- **Dungeons:** Razorfen Kraul, Gnomeregan, Scarlet Monastery wings, [The Drowned City](../../content/dungeons/drowned-city.md) (35–42).
- **Level 40:** **Dire Bear Form**, Innervate, Feline Grace, **dual spec** (50g), and riding (100g including your first racial mount). Have about 150g ready.

### 40–50

- **Zones:** Riverglades (to about 45), Badlands, Swamp of Sorrows, Tanaris, Feralas, Hinterlands. Horde's Feralas trainer is Jannos Lighthoof (Camp Mojache).
- **Dual spec:** use Feral (tank/cat) plus Resto for dungeons, or keep both as Feral (Cat leveling and Bear tank).
- **Level 45:** last library book unlock (**25 books**), and Legacy *Experienced* tier (some sources say 40).
- **Dungeons:** [Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md) (40–47), Razorfen Downs, SM Cathedral, Uldaman, Zul'Farrak, [Alcaz Prison](../../content/dungeons/alcaz-prison.md) (48–55).

### 50–60

- **Zones:** Un'Goro, Felwood (Golhine the Hooded trains Alliance druids at Talonbranch Glade), Azshara (many new quests), Western and Eastern Plaguelands, Burning Steppes, Winterspring, Silithus.
- **Dungeons:** Maraudon, Sunken Temple, Blackrock Depths, Dire Maul, [Blackmaw Hold](../../content/dungeons/blackmaw-hold.md) (Azshara, 55–60), LBRS, [Shaper's Terrace](../../content/dungeons/shapers-terrace.md) (Un'Goro, 58–60), Scholomance, Stratholme.
- **At 60:** [Mount Hyjal](../../world/zones.md#mount-hyjal) via Darkwhisper Gorge in Winterspring. Legacy *Master* tier. Epic riding is 1,000g.

!!! tip "Moonglade"
    Teleport: Moonglade from level 10 is a free hearth to the druid trainer Loganaar in Moonglade. From there, take a flight path. Use it to get to Kalimdor fast as Horde or Alliance.

</div>

---

## Dungeons

**Role tips**

- **Bear:** pull with Feral Charge or Faerie Fire, open with Primal Bite, and Swipe packs of 3. Swipe hits only 3 targets. Thus, mark the other targets for CC. Because of the threat buff in Forever (+115%), you do not need Lacerate stacks before the DPS start.
- **Cat:** stay behind the target for Shred. Let the tank use 1 Primal Bite first. Keep Cower for spikes. Leader of the Pack helps the whole party.
- **Balance:** Hurricane has no cooldown, and Entangling Roots now works indoors. Hibernate beasts and dragonkin. Use Soothe Animal to skip mobs.
- **Resto:** cast Rejuvenation on the tank before the pull. Keep Innervate for yourself, and keep Rebirth for the tank or healer.
- **Utility:** Remove Curse and Abolish Poison are very necessary in Shadowfang Keep, Zul'Farrak, Maraudon and Dire Maul.

| Level | Notable dungeons | Druid notes |
|---|---|---|
| 13–22 | [Hall of Thanes](../../content/dungeons/hall-of-thanes.md), [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md), Ragefire, Wailing Caverns, Deadmines | Bear tank before Lacerate. Wailing Caverns has Journeyman Campfire blueprint |
| 24–35 | [Excavation Site](../../content/dungeons/excavation-site.md), [City of Dalaran](../../content/dungeons/city-of-dalaran.md), SFK, BFD, Stockade | Remove Curse in SFK. Rock Garden/Greenhouse blueprints in Excavation Site |
| 35–47 | [Drowned City](../../content/dungeons/drowned-city.md), [Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md), SM, RFK, RFD | Dire Bear at 40 is the big tanking upgrade |
| 48–55 | [Alcaz Prison](../../content/dungeons/alcaz-prison.md), Uldaman, ZF, Maraudon | Abolish Poison in Maraudon and ZF |
| 55–60 | [Blackmaw Hold](../../content/dungeons/blackmaw-hold.md), [Shaper's Terrace](../../content/dungeons/shapers-terrace.md), BRD, DM, LBRS, Scholo, Strat, UBRS | Blackmaw Hold also has an entrance to the Barrow Deeps |

See [Dungeons](../../content/dungeons/index.md) for the full list.

---

## Raid preparation (9 December)

All 3 launch raids open on **9 Dec 2026**. See [Raids](../../content/raids/index.md).

| Raid | Size | Druid role |
|---|---|---|
| [The Barrow Deeps](../../content/raids/barrow-deeps.md) | 10 | Bear main/off-tank, Resto, or Moonkin/Cat for auras. A druid is almost necessary for Rebirth and Innervate |
| [Hyjal Summit](../../content/raids/hyjal-summit.md) | 20 | Resto, plus one aura druid (Moonkin or Leader of the Pack). Fel corruption themes. Remove Curse/Abolish Poison duty is probable (*speculation*) |
| [Onyxia's Lair](../../content/raids/onyxias-lair.md) | 40 | Resto and off-tank for whelps. Fire resistance helps. Needs the Drakefire Amulet attunement |

**Pre-raid gear:** the original Classic pre-raid lists do not apply without changes, because new dungeons drop items with unique, spec-themed stats. A practical procedure:

1. Do the 55–60 dungeons for drops that match your spec. Look for themed "druid" items from Blackmaw Hold and Shaper's Terrace.
2. Use crafted Leatherworking pieces to fill gaps (many new BoP patterns).
3. Rank 3–10 PvP blues and epic upgrade tokens are a valid source for Feral and Balance.
4. Tanks: get some Fire Resistance for Onyxia.

**Consumables** (all usable in form now): Mighty Rage Potion (Bear), Elixir of the Mongoose/Giants (Cat), Greater Arcane Elixir (Balance), mana potions, Major Healing Potions (now crafted by **First Aid**), Thistle Tea for Cat, weightstones and weapon oils. The Manual Crowd Pummeler still appears in bear simulations.

**Role in the raid:** a druid brings Innervate, Rebirth and either Moonkin Form or Leader of the Pack. Moonkin and Leader of the Pack **do not stack** (both are crit auras). Thus, a raid almost never needs more than 1 of each.

---

## PvP

See [PvP](../../content/pvp/index.md) and [Battlegrounds](../../content/pvp/battlegrounds.md).

- **Battlegrounds:** Druids are the best flag carriers in Warsong Gulch: Travel Form, Feral Charge, Dash, and Frenzied Regeneration that heals to full. In **[Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands)** (15v15, 30–60), carry the central flag, or use Prowl to capture bases that nobody defends. Arathi Basin and Alterac Valley also reward this mobility.
- **World PvP:** Prowl and Travel Form let you choose your fights. Nature's Grasp (now baseline at 10) and Entangling Roots indoors make melee kiting much easier.
- **Specs:** Resto with Feral utility to heal in battlegrounds. Feral to carry flags and for burst. Balance for ranged damage (Starfire hits harder now).

| Matchup | Notes |
|---|---|
| Rogue | Keep Faerie Fire on the Rogue to stop restealth. Barkskin in form now protects you when you shift |
| Warrior | Root and kite. Shift out of Hamstring. Do not stay in melee with a Warrior in Cat |
| Mage | Shift out of Polymorph and slows. Use Feral Charge after Blink |
| Priest / Warlock | Fear is the problem. Shifting does not break it (Classic behavior). Tauren can War Stomp before the cast. If not, fight at range as Balance, or burst from Prowl |
| Hunter | Close the gap with Feral Charge, Dash and Travel Form. Root their pet |
| Paladin / Shaman | Long fights. Feral burst after a defensive cooldown, or Balance with roots |

---

## Gear, stats & enchants

| Spec | Stat priority |
|---|---|
| **Cat** | Hit (to the 9% raid-boss cap. Nature's Reach gives 4%) > Strength (2 AP per point) ≈ Agility > Crit > Attack Power. Haste is low value |
| **Bear** | Stamina and Armor > Defense (440 for raid bosses) and Dodge > threat stats (Strength, Hit, Crit) |
| **Balance** | Spell Hit (to the cap) > Spell Damage > Spell Crit > Intellect > Spirit |
| **Restoration** | Healing Power > mana regeneration (Spirit with Reflection, MP5) > Intellect > Stamina |
| **Leveling (Feral)** | Strength/Agility/AP > Stamina > Intellect/Spirit > Armor |

!!! conflict "Conflict: leveling stats"
    Warcraft Tavern says Strength/Agility first. Method suggests Intellect and Spirit pieces for leveling, to keep enough mana for shifts. Both work. Spirit helps a Balance or mixed playstyle. With Strength/Agility, you kill faster as Cat.

!!! conflict "Conflict: Expertise"
    Warcraft Tavern's Feral guide mentions an Expertise cap after Hit. Expertise is not in the Classic stat system. No other source mentions it in Forever. Treat it as *unconfirmed*.

**Weapons:** form damage uses the DPS of your weapon. Thus, a high-DPS staff, polearm or two-hander is important. Weapon enchants (Crusader) and weightstones work in form.
**Enchants (Classic-era advice):** Crusader or +Agility on the weapon, Stamina or Agility on chest, Agility on gloves for Cat, Stamina/Defense for Bear, Spell Power/Healing for casters.

---

## Professions & Legacy

<p class="divider">Professions</p>

Druids wear leather and can use potions in all forms. Thus, the correct pair depends on your spec.

<div class="prof-picks" markdown>

<div class="prof-pick prof-pick--best" markdown>

<p class="prof-rank" markdown>**S**{ .tier .tier-s } Best pick</p>

<p class="prof-pair" markdown>:material-bag-personal: Leatherworking <span class="prof-plus">+</span> :material-knife: Skinning</p>

<p class="prof-for">Best for: Feral and leveling</p>

<div class="pills" markdown>
**Leveling**{ .pill .pill--success .pill--sm } **Gold**{ .pill .pill--gold .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
</dl>

- The classic Feral choice: leather armor and many new BoP patterns
- Skin your own kills when you level

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Camp Tent (rested XP) · Camp Chair (+2% crit)</p>

</div>

<div class="prof-pick prof-pick--alt" markdown>

<p class="prof-rank" markdown>**A**{ .tier .tier-a } Strong alternative</p>

<p class="prof-pair" markdown>:material-leaf: Herbalism <span class="prof-plus">+</span> :material-flask: Alchemy</p>

<p class="prof-for">Best for: Balance and Restoration raiders</p>

<div class="pills" markdown>
**Raids**{ .pill .pill--info .pill--sm } **Gold**{ .pill .pill--gold .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:100%"><span>5/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
</dl>

- Potions now work in form, so every druid uses them
- Herbalism works well with Travel Form. Tauren Cultivation adds herbs

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Incense Candle (Intellect) · Mana Well (mana regen)</p>

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

- Trinkets and bombs. SAF-T and EZ-Thro bombs work in form

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Lodestone (melee AP) · Reagent Bot</p>

</div>

</div>

<p class="legend" markdown>Codex ratings out of 5, based on the sources above. Compare every class in [Best professions by class](../../characters/professions.md#best-professions-by-class).</p>

<div class="pills" markdown>
**:material-medical-bag: First Aid · healing potions**{ .pill .pill--success } **:material-pot-steam: Cooking · campfires**{ .pill .pill--info } **:material-fish: Fishing · Fish Bowl**{ .pill .pill--info }
</div>

**Secondary skills.** Cooking feeds campfires. First Aid now makes healing potions. Fishing adds the Fish Bowl.

!!! tip "Race notes"
    **Tauren:** *Cultivation* grows an herb with bonus yield for Herbalists.

Crafting professions award [Legacy Points](../../characters/legacy.md) at skill 150, 225 and 300, and each profession adds a [camp feature](../../systems/camping.md). Professions give no passive stats in Forever.

**Legacy talents** (16 points per character. See [Legacy](../../characters/legacy.md))

| Goal | Picks |
|---|---|
| Leveling | **Well Rested** 5/5 → **Talented** (first talent point a maximum of 5 levels early) · Thrill of Adventure · Frequent Flier |
| Endgame | **Permanence** (Mark of the Wild and Thorns last longer) · **Reagent Economy** (no reagents for Rebirth or the group Mark) · Gourmand |
| PvP | For Great Honor · The Quick and the Dead |
| Gathering | Bountiful Harvest · Working Overtime |

---

## Hardcore notes

!!! hardcore "Hardcore survival"

    [Hardcore](../../about/hardcore.md) comes in winter 2026/27. The Druid is one of the safest classes for it.

    - **Escape kit:** Travel Form, Dash, Prowl (out of combat), Aquatic Form, Nature's Grasp and Entangling Roots. Night Elves also have Shadowmeld.
    - **Bear is your emergency option:** high armor, Frenzied Regeneration to full, and you can now use potions in form.
    - **Self-healing:** shift out, Regrowth plus Rejuvenation, shift back. Keep enough mana for this. Do not use all of it on shifts.
    - **Be careful of fear casters** (you have no fear break) and of packs that you cannot control. Hibernate only works on Beasts and Dragonkin.
    - **Revive** (12) and **Rebirth** (20) help your group, not you.
    - Blizzard designed the new dungeon items with special effects partly for Hardcore.

---

## Common mistakes & FAQ

??? question "Do I still need to powershift?"
    No. Blizzard replaced powershifting. Take **Furor 5/5** for Energy regeneration out of Cat Form and use **Shifting Power** for instant Energy.

??? question "Do I need to leave form to drink a potion?"
    No, not any more. Potions, Rage potions, Thistle Tea and most consumables work in form.

??? question "Is Bear a real tank in Forever?"
    Yes, for 5-player dungeons and 10-player raids. Threat is +115% and Growl works like Taunt. In the beta, tier lists put Bear at B to C tier against Warrior and Paladin. Launch hotfixes changed threat again. Wait for raid data.

??? question "Where's Mangle? Berserk?"
    **Primal Bite** replaced Mangle. Blizzard removed Berserk before launch. Shifting Power replaced Tiger's Fury.

??? question "Why can't I Ravage out of Shadowmeld?"
    A 6 Nov hotfix stopped Night Elf druids from opening with Ravage or Pounce out of Shadowmeld. Use Prowl.

??? question "Moonkin or Leader of the Pack?"
    Both are crit auras and do not stack. The raid needs a maximum of 1 of each.

??? question "Which race is best?"
    Differences are marginal. See the race add-ons: [Night Elf](night-elf.md), [High Order Skyborne](skyborne-high-order.md), [Tauren](tauren.md), [Windshaper Skyborne](skyborne-windshaper.md).

**Common mistakes**

- You skip the level-16 Aquatic Form quest.
- You forget that Faerie Fire is now free and usable in form.
- You refresh Rip and Rake early. Let them expire first.
- You level in caster gear as Feral. Your form damage depends on the DPS of your weapon.
- You do not train at every even level.

---

## Sources

??? quote "9 sources"

    - [Warcraft Tavern — Druid Guide](https://www.warcrafttavern.com/forever/guides/druid/)
    - [Warcraft Tavern — Druid Leveling Guide](https://www.warcrafttavern.com/forever/guides/druid-leveling/)
    - [Warcraft Tavern — Feral Druid Guide](https://www.warcrafttavern.com/forever/guides/feral-druid/)
    - [Warcraft Tavern — Hunter & Druid deep dive](https://www.warcrafttavern.com/forever/news/powershifting-is-back-sort-of-hunter-druid-deep-dive-for-wow-forever/)
    - [Method — WoW Forever Druid Leveling Guide & Talents](https://www.method.gg/wow-forever/wow-forever-druid-leveling-guide-and-talents)
    - [Kami-labs — Guardian Druid PvE Build](https://kami-labs.fr/en/wow-forever/build-druide-gardien-wow-forever/)
    - [Mobalytics — Druid guides](https://mobalytics.gg/wow-forever/druid-guides)
    - [Warcraft Wiki — Druid abilities (Forever)](https://warcraft.wiki.gg/wiki/Druid_abilities_(Forever))
    - [games.gg — Best tank classes](https://games.gg/world-of-warcraft/guides/wow-forever-guide-best-tank-classes/)
