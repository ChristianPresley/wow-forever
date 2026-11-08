---
tags:
  - Shaman
  - Tauren
  - Horde
---

# Tauren Shaman

<div class="guide-head" data-class="shaman" markdown>

:codex-shaman:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Add-on</span> **:codex-horde:{ .fc-sigil aria-hidden="true" } Horde**{ .badge .faction } **Healer**{ .badge .heal } **DPS**{ .badge .dps }

<p class="gh-note" markdown>Read with the [Shaman guide](index.md).</p>

</div>

## Why this combo

Tauren are the Horde's spiritual heart: Thunder Bluff's Elder Rise is home to shamans and druids. Tauren Shaman was popular enough that its **creation was throttled on launch night**. In Forever the Tauren racials are the most *utility*-focused for a Shaman. **War Stomp** is still a strong PvP and emergency tool, but Warcraft Tavern rates the Tauren racials the **weakest for Shamans** because none of them adds damage or healing.

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**War Stomp** <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 }</p>
<p markdown><span class="ability-label">PvE</span> Stuns up to 5 nearby enemies for 2 s. Interrupts a pack of casters or buys time for a Lesser Healing Wave</p>
<p markdown><span class="ability-label">PvP</span> The best racial for a Restoration Shaman in melee range: stomp, then heal</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Cultivation** *(new)* <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 }</p>
<p markdown><span class="ability-label">PvE</span> Grows an herb anyone can gather. Herbalists get duplicate nodes or bonus herbs. Pairs well with Alchemy for your own mana potions</p>
<p markdown><span class="ability-label">PvP</span> —</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Plainsrunning** *(new)* <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **2/5**{ .stars .s2 }</p>
<p markdown><span class="ability-label">PvE</span> +2% movement speed per stack while moving, up to +60%. Doesn't work while mounted, so it mostly helps before level 40</p>
<p markdown><span class="ability-label">PvP</span> On 5 November it was hotfixed to **no longer stack and to drop on flag pickup**, after Warsong Gulch abuse. Its current exact effect is unclear</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Endurance** *(changed)* <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 }</p>
<p markdown><span class="ability-label">PvE</span> +5% health. The beta hit and crit bonus was removed</p>
<p markdown><span class="ability-label">PvP</span> More health for a healer in battlegrounds</p>
</div>

</div>

??? example "Macro: stomp and heal"

    ```text
    #showtooltip War Stomp
    /cast War Stomp
    ```

    ```text
    #showtooltip Lesser Healing Wave
    /cast [@mouseover,help,nodead][@player] Lesser Healing Wave
    ```

    Press War Stomp, then heal yourself. Keep them as two keys, since War Stomp has a short cast time.

    !!! conflict "Conflict"
        The 5 November hotfix note for Plainsrunning is short. It says the racial "no longer stacks" and drops when you pick up a flag. Whether the speed bonus still works at all outside battlegrounds isn't clear. Test it in game.

## Starting zone: Camp Narache to Bloodhoof Village (1–12)

!!! note "Classic layout"
    Mulgore gained **Skywatcher Plateau** in the northwest, the landing point for the Windshaper airship. Trainer names and totem quest details below are Classic ones.

<div class="steps" markdown>

1.  **1–6**{ .lvl } Camp Narache

    - The Shaman trainer is in Camp Narache (Classic: Meela Dawnstrider).
    - Quest on plainstriders, cougars and the quilboar of Brambleblade Ravine.
    - **Level 4: *Call of Earth*.** In Classic, Meela sends you up Red Cloud Mesa to an earth spirit. Drink the Earth Sapta, defeat the Minor Manifestation of Earth, and return for the **Earth Totem** and Stoneskin Totem.

2.  **6–12**{ .lvl } Bloodhoof Village

    - Bloodhoof Village has a Shaman trainer (Classic: Narm Skychaser).
    - Quest around the Venture Co. camps, Palemane gnolls and the wells.
    - **Level 10: *Call of Fire*.** Your trainer starts the Fire quest. The Forever route isn't documented in our sources. Reward: **Fire Totem** and Searing Totem.
    - **First talent point** at 10.
    - If you take **Herbalism**, Cultivation means you'll never be short of Peacebloom and Silverleaf.

</div>

## Route to 60 from Thunder Bluff

**Class trainer city:** Thunder Bluff, on **Elder Rise** (Classic location). Horde has about **15 Shaman trainers**, including Orgrimmar and Stonard.

<div class="steps" markdown>

1.  **1–12**{ .lvl } Mulgore

    <span class="step-label">Flight path / travel</span> Thunder Bluff

2.  **10–25**{ .lvl } **The Barrens**

    <span class="step-label">Flight path / travel</span> Crossroads, Camp Taurajo

3.  **15–27**{ .lvl } Stonetalon Mountains (widened east)

    <span class="step-label">Flight path / travel</span> Sun Rock Retreat

4.  **20–30**{ .lvl } Ashenvale, Hillsbrad

    <span class="step-label">Flight path / travel</span> Splintertree Post, Tarren Mill

5.  **25–35**{ .lvl } **Thousand Needles**

    <span class="step-label">Flight path / travel</span> Freewind Post

6.  **30–40**{ .lvl } **Desolace** (path from Skywatcher Plateau), Arathi, Stranglethorn

    <span class="step-label">Flight path / travel</span> Shadowprey, Hammerfall, Grom'gol

7.  **35–45**{ .lvl } Riverglades (Rog'mar), Dustwallow Marsh, **Shen'dralas** (level range unknown)

    <span class="step-label">Flight path / travel</span> Rog'mar flights

8.  **40–50**{ .lvl } Feralas, Tanaris, Badlands, Swamp of Sorrows, Hinterlands

    <span class="step-label">Flight path / travel</span> Camp Mojache, Gadgetzan, Kargath, Stonard, Revantusk

9.  **50–60**{ .lvl } Un'Goro, Azshara, Felwood, Burning Steppes, Winterspring, the Plaguelands

    <span class="step-label">Flight path / travel</span> Marshal's Refuge, Valormok, Bloodvenom, Flame Crest, Everlook

10.  **60**{ .lvl } Mount Hyjal

    <span class="step-label">Flight path / travel</span> Darkwhisper Gorge

</div>

**Totem quests:** Earth (4), Fire (10), Water (20; Classic used Southern Barrens and Thousand Needles), Air (30; new in Forever, with a spec weapon).

**Kalimdor-first leveling:** as a Tauren you can stay in Kalimdor for most of the way. Stonetalon, Thousand Needles, Desolace and Feralas all have Tauren camps.

## Faction-specific notes

- **Mount:** kodo, from Bloodhoof Village. Riding is 100g at 40 including your first kodo. Honored with Thunder Bluff gives 10% off. A separate **Reins of the Pack Kodo** costs 6,000 Merchant's Favor.
- **Reputation:** Thunder Bluff.
- **Skywatcher Plateau** is right outside Thunder Bluff. The airship to **Zephras Isle** stops here, so you can visit the island and earn **Windshaper** reputation for a Galestrider mount at Exalted. Cloth turn-ins for Skyborne reputation are reported in Mulgore.
- **Muln Earthfury** of the Earthen Ring is the Windshapers' ally in Mulgore and appears in the Zephras Isle finale.
- **Barbershop:** Thunder Bluff gained one in Forever.

## Verdict

<div class="verdict" markdown>

**The defensive pick.** War Stomp and Endurance make a sturdy Restoration Shaman in battlegrounds, and Cultivation is a nice bonus for Alchemists. For damage, Orc Blood Fury and Troll Berserking are stronger, and Plainsrunning has been weakened. Choose Tauren for the look, the Kalimdor leveling route and the PvP survival tools, not for the numbers.

</div>
