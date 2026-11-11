---
tags:
  - Shaman
  - Tauren
  - Horde
---

# Tauren Shaman

<div class="guide-head" data-class="shaman" markdown>

:codex-shaman:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Add-on</span> **:codex-horde:{ .fc-sigil aria-hidden="true" } Horde**{ .badge .faction } **Healer**{ .badge .heal } **DPS**{ .badge .dps }

<p class="gh-note" markdown>Read with the [Shaman progression](index.md).</p>

</div>

## Why this combo

Tauren are the spiritual center of the Horde. Shamans and druids live on Elder Rise in Thunder Bluff. Tauren Shaman was so popular that its **creation was throttled on launch night**. In Forever, the Tauren racials give a Shaman the most *utility*. **War Stomp** is still a strong tool for PvP and emergencies. But Warcraft Tavern rates the Tauren racials the **weakest for Shamans**, because no Tauren racial adds damage or healing.

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**War Stomp** <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 }</p>
<p markdown><span class="ability-label">PvE</span> Stuns up to 5 nearby enemies for 2 s. Interrupts a pack of casters or gives you time for a Lesser Healing Wave</p>
<p markdown><span class="ability-label">PvP</span> The best racial for a Restoration Shaman in melee range: use War Stomp, then heal</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Cultivation** *(new)* <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 }</p>
<p markdown><span class="ability-label">PvE</span> Grows an herb that all players can gather. Herbalists get duplicate nodes or bonus herbs. Good with Alchemy, because you can make your own mana potions</p>
<p markdown><span class="ability-label">PvP</span> —</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Plainsrunning** *(new)* <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **2/5**{ .stars .s2 }</p>
<p markdown><span class="ability-label">PvE</span> +2% movement speed per stack when you move, up to +60%. Does not work when you are mounted, so it helps mostly before level 40</p>
<p markdown><span class="ability-label">PvP</span> After players abused it in Warsong Gulch, a 5 November hotfix changed it. Now it does **not stack, and you lose it when you pick up a flag**. Its exact current effect is not clear</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Endurance** *(changed)* <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 }</p>
<p markdown><span class="ability-label">PvE</span> +5% health. Forever removed the hit and crit bonus from the beta</p>
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

    Push War Stomp, then heal yourself. Keep them on 2 keys, because War Stomp has a short cast time.

    !!! conflict "Conflict"
        The 5 November hotfix note for Plainsrunning is short. It says the racial "no longer stacks" and drops when you pick up a flag. It is not clear if the speed bonus still works outside battlegrounds. Test it in the game.

## Starting zone: Camp Narache to Bloodhoof Village (1–12)

!!! note "Classic layout"
    Mulgore now has **Skywatcher Plateau** in the northwest. The Windshaper airship lands there. The trainer names and totem quest details below are from Classic.

<div class="steps" markdown>

1.  **1–6**{ .lvl } Camp Narache

    - The Shaman trainer is in Camp Narache (Classic: Meela Dawnstrider).
    - Quest on plainstriders, cougars and the quilboar of Brambleblade Ravine.
    - **Level 4: *Call of Earth*.** In Classic, Meela sends you to an earth spirit on top of Red Cloud Mesa. Drink the Earth Sapta and defeat the Minor Manifestation of Earth. Then go back to get the **Earth Totem** and Stoneskin Totem.

2.  **6–12**{ .lvl } Bloodhoof Village

    - Bloodhoof Village has a Shaman trainer (Classic: Narm Skychaser).
    - Quest around the Venture Co. camps, Palemane gnolls and the wells.
    - **Level 10: *Call of Fire*.** Your trainer starts the Fire quest. Our sources do not document the Forever route. Reward: **Fire Totem** and Searing Totem.
    - **First talent point** at 10.
    - If you take **Herbalism**, Cultivation gives you a constant supply of Peacebloom and Silverleaf.

</div>

## Route to 60 from Thunder Bluff

**Class trainer city:** Thunder Bluff, on **Elder Rise** (Classic location). Horde has about **15 Shaman trainers**, which include trainers in Orgrimmar and Stonard.

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

**Totem quests:** Earth (4), Fire (10), Water (20, Classic used Southern Barrens and Thousand Needles), Air (30, new in Forever, gives a spec weapon).

**Kalimdor-first leveling:** as a Tauren, you can stay in Kalimdor for most of your levels. Stonetalon, Thousand Needles, Desolace and Feralas all have Tauren camps.

## Faction-specific notes

- **Mount:** kodo, from Bloodhoof Village. At level 40, Riding costs 100g, and this price includes your first kodo. At Honored with Thunder Bluff, you get a 10% discount. A separate **Reins of the Pack Kodo** costs 6,000 Merchant's Favor.
- **Reputation:** Thunder Bluff.
- **Skywatcher Plateau** is immediately next to Thunder Bluff. The airship to **Zephras Isle** stops here. Thus, you can visit the island and get **Windshaper** reputation for a Galestrider mount at Exalted. Players report cloth turn-ins for Skyborne reputation in Mulgore.
- **Muln Earthfury** of the Earthen Ring is the Windshapers' ally in Mulgore and appears in the Zephras Isle finale.
- **Barbershop:** Forever added a barbershop to Thunder Bluff.

## Verdict

<div class="verdict" markdown>

**The defensive choice.** War Stomp and Endurance make a strong Restoration Shaman in battlegrounds. Cultivation is a good bonus for Alchemists. For damage, Orc Blood Fury and Troll Berserking are stronger, and Forever made Plainsrunning weaker. Choose Tauren for the look, the Kalimdor leveling route and the PvP survival tools, not for the numbers.

</div>
