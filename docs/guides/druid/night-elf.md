---
tags:
  - Druid
  - Night Elf
  - Alliance
---

# Night Elf Druid

<div class="guide-head" data-class="druid" markdown>

:codex-druid:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Add-on</span> **:codex-alliance:{ .fc-sigil aria-hidden="true" } Alliance**{ .badge .faction } **Tank**{ .badge .tank } **Healer**{ .badge .heal } **DPS**{ .badge .dps }

<p class="gh-note" markdown>Read this page with the [Druid guide](index.md). This page gives only the differences for a Night Elf.</p>

</div>

## Why this combo

The Night Elf is the original Alliance druid. You start in Shadowglen below Teldrassil. Your class trainer is in Darnassus, and Moonglade is a short trip from Darkshore. Method calls it the **best all-round Alliance druid**, mainly for **Elune's Light** (a burst crit cooldown) and **Quickness** (dodge plus run speed). It is a Classic combination, not new in Forever.

**Best for:** Cat DPS, PvP stealth play, and players who want the Alliance druid that is most faithful to the lore.
**Compared with High Order Skyborne:** you get crit burst, dodge and Shadowmeld, but you lose haste and mana regen. See [High Order Skyborne Druid](skyborne-high-order.md).

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Elune's Light** *(new)* <span class="ability-type active">Active: +10% crit for 15 s</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **5/5**{ .stars .s5 }</p>
<p markdown><span class="ability-label">PvE</span> Works well with Cat burst, Moonkin Starfire windows or a Bear pull. One source gives a 3 min cooldown (*unconfirmed*)</p>
<p markdown><span class="ability-label">PvP</span> A kill window from Prowl</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Shadowmeld** <span class="ability-type active">Active: stealth when you do not move</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 }</p>
<p markdown><span class="ability-label">PvE</span> Removes aggro to prevent a wipe or to skip a patrol. Works in form</p>
<p markdown><span class="ability-label">PvP</span> Reset fights and ambush flag carriers. **After the 6 Nov hotfix, you cannot Ravage or Pounce out of it**</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Quickness** <span class="ability-type passive">Passive: +1% dodge, +2% run speed</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 }</p>
<p markdown><span class="ability-label">PvE</span> Small, but always active. Dodge helps Bear</p>
<p markdown><span class="ability-label">PvP</span> Extra speed for kiting and flag runs</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Wisp Spirit** <span class="ability-type passive">Passive: +75% run speed as a ghost</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **1/5**{ .stars .s1 }</p>
<p markdown><span class="ability-label">PvE</span> Faster corpse runs when you level</p>
<p markdown><span class="ability-label">PvP</span> Nothing in combat</p>
</div>

</div>

Blizzard removed the old Nature Resistance racial, like all other resistance racials.

??? example "Macros"

    ```text
    #showtooltip Elune's Light
    /cast Elune's Light
    /cast Ferocious Bite
    ```

    ```text
    #showtooltip
    /cast [nocombat,nostealth] Shadowmeld
    ```

    Use the first one at 5 combo points in Cat, or replace Ferocious Bite with Starfire for Balance. Sources do not list a global cooldown for Elune's Light. If your bite does not fire, push the macro again.

## Starting zone walkthrough: Teldrassil (1–~12)

!!! note "Changed in Forever"
    Blizzard added new NPCs, quests, profession hooks and "small moments" to Shadowglen, in the same way as the Valley of Trials. The quest chains below follow the familiar Classic sequence. Some new quests do not have documentation yet.

**Shadowglen (1–6)**

<div class="steps" markdown>

1.  Start at **Aldrassil**. Your first druid trainer is **Mardant Strongoak** inside the tree.
2.  Do the Grell and nightsaber kill quests, then the Shadowthread Cave and Fel Moss quests. Spam Wrath. Open with Moonfire. Heal with Rejuvenation.
3.  At **4**, train Moonfire and Rejuvenation. At **6**, train Thorns.
4.  At about level 5, take **The Great Outdoors** to unlock camping. Select a gathering profession at the starter quest.

</div>

**Dolanaar (6–11)**

1. Go to **Dolanaar**. The druid trainer is **Kal**. Set your hearthstone at the inn.
2. Do the quests around Lake Al'Ameth, the Oracle Glade, Ban'ethil Barrow Den and the Starbreeze furbolg village.
3. **Level 8:** Entangling Roots. **Level 10:** Nature's Grasp and your first talent point (Ferocity or Feral Instinct).
4. **Level 10 Bear Form:** take **Heeding the Call** from **Mathrengyl Bearwalker** in the Cenarion Enclave (Darnassus). It sends you to Moonglade to meet the bear spirit, and it teaches **Teleport: Moonglade**.

**Leaving (11–12)**

Complete the quests in Darnassus and Teldrassil. Then take the boat from **Rut'theran Village** to **Auberdine**, Darkshore. For all of the game, Teleport: Moonglade plus the Moonglade flight path is a fast route back to Kalimdor.

## Route to 60 from Darnassus

<div class="steps" markdown>

1.  **1–11**{ .lvl } Teldrassil

    Bear Form quest at 10

2.  **11–20**{ .lvl } **Darkshore**

    Lessons Anew (Cure Poison) at 14 and **Aquatic Form at 16**. Bear tank or solo

3.  **15–22**{ .lvl } Loch Modan / Westfall / Redridge

    New **Auberdine ↔ Stormwind Harbor** boat. Optional [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) and Deadmines

4.  **20**{ .lvl } Darnassus

    **The Great Cat Spirit** (Cat Form, Prowl, Claw, Rip). First library-book unlock

5.  **20–30**{ .lvl } Ashenvale (Astranaar), Wetlands, Duskwood, Hillsbrad

    [Excavation Site](../../content/dungeons/excavation-site.md) in the Wetlands. Blackfathom Deeps in Ashenvale

6.  **30–40**{ .lvl } Stonetalon, Arathi, [Dalaran](../../world/zones.md#dalaran) (Alterac), Desolace, Stranglethorn, Dustwallow (Theramore)

    Travel Form at 30. [City of Dalaran](../../content/dungeons/city-of-dalaran.md)

7.  **35–45**{ .lvl } **[Riverglades](../../world/zones.md#riverglades)** from **Farholde Keep**

    Flights to Lakeshire, Thelsamar and Morgan's Vigil

8.  **40–50**{ .lvl } Feralas (Feathermoon), Tanaris, Badlands, Swamp of Sorrows, Hinterlands

    Riding at 40 in Darnassus. Dual spec

9.  **50–58**{ .lvl } Un'Goro, Azshara, **Felwood** (Talonbranch Glade trainer Golhine the Hooded), Searing Gorge, Burning Steppes

    [Blackmaw Hold](../../content/dungeons/blackmaw-hold.md)

10.  **55–60**{ .lvl } Western and Eastern Plaguelands, Winterspring, Silithus

    Then [Mount Hyjal](../../world/zones.md#mount-hyjal) via Darkwhisper Gorge

</div>

**Class trainers:** Mardant Strongoak (Shadowglen), Kal (Dolanaar), Mathrengyl Bearwalker and the Cenarion Enclave trainers (Darnassus), Sheldras Moontree (Stormwind), Golhine the Hooded (Felwood), Loganaar (Moonglade).

## Faction-specific notes

- **Class quests:** Heeding the Call (10), Lessons Anew (14), A Lesson to Learn (16), The Great Cat Spirit (20), all from Darnassus.
- **Mount:** **Frostsaber** ("Tiger Riding") from Lelanai in Darnassus at 40 (100g including Riding). Honored with Darnassus gives −10%.
- **Reputation:** Darnassus. Kirin Tor (Dalaran) is open to the Alliance. Theramore Expeditionary Force from [Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands).
- **Barbershop:** Darnassus got a barbershop in Forever.
- **Lore:** the Cenarion Circle and Moonglade are your home. The [Barrow Deeps](../../content/raids/barrow-deeps.md) raid, Illidan's old prison full of Druids of the Claw, is the most night-elven content in the game.
- **Models:** HD or classic SD models, switchable.

## Verdict

<div class="verdict" markdown>

A strong, safe pick. **Elune's Light** is the best throughput racial an Alliance druid can get, especially for Cat. **Quickness** helps Bear. Shadowmeld lost its Ravage opener on 6 Nov, but it still saves runs and PvP fights. Select High Order Skyborne only if you want haste, mana regen and Walk on Air, or the Skyborne look.

| Spec | Rating |
|---|---|
| Cat | **5/5**{ .stars .s5 } |
| Bear | **4/5**{ .stars .s4 } |
| Balance | **4/5**{ .stars .s4 } |
| Restoration | **3/5**{ .stars .s3 } |
| PvP | **4/5**{ .stars .s4 } |

</div>
