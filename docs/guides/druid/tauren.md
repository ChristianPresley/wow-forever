---
tags:
  - Druid
  - Tauren
  - Horde
---

# Tauren Druid

<div class="guide-head" data-class="druid" markdown>

:codex-druid:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Add-on</span> **:codex-horde:{ .fc-sigil aria-hidden="true" } Horde**{ .badge .faction } **Tank**{ .badge .tank } **Healer**{ .badge .heal } **DPS**{ .badge .dps }

<p class="gh-note" markdown>Read with the [Druid guide](index.md). This page covers only what changes for a Tauren.</p>

</div>

## Why this combo

The Tauren is the original Horde druid. You start at Camp Narache in Mulgore, train in Thunder Bluff's Elder Rise, and your people are close to the Cenarion Circle through Hamuul Runetotem. Method recommends Tauren for **Bear tanking and PvP**: **Endurance** (+5% health) is the best tank racial for druids, and **War Stomp** now works in form. It is a Classic combination, not new in Forever.

**Best for:** Bear tank, battleground and world PvP, Herbalism.
**Compared with Windshaper Skyborne:** you trade haste for health, an AoE stun and better gathering. See [Windshaper Skyborne Druid](skyborne-windshaper.md).

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**War Stomp** <span class="ability-type active">Active: stuns up to 5 nearby enemies for 2 s</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **5/5**{ .stars .s5 }</p>
<p markdown><span class="ability-label">PvE</span> Interrupts casters, buys time on a bad pull. **Usable in Bear and Cat**</p>
<p markdown><span class="ability-label">PvP</span> Stops a cast or fear, then shift or heal</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Endurance** <span class="ability-type passive">Passive: +5% health</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 }</p>
<p markdown><span class="ability-label">PvE</span> Always-on survivability for Bear</p>
<p markdown><span class="ability-label">PvP</span> Harder to burst</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Plainsrunning** *(new)* <span class="ability-type passive">Passive: +2% speed per stack while moving, up to +60%; not while mounted</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 } (leveling)</p>
<p markdown><span class="ability-label">PvE</span> Huge for leveling before Travel Form at 30 and before a mount at 40</p>
<p markdown><span class="ability-label">PvP</span> **Blocked in battlegrounds** by the 5 Nov hotfix</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Cultivation** *(new)* <span class="ability-type active">Active: grows an herb anyone can gather; bonus yield for Herbalists</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 }</p>
<p markdown><span class="ability-label">PvE</span> Gold and potion supply with Herbalism</p>
<p markdown><span class="ability-label">PvP</span> None</p>
</div>

</div>

The old Nature Resistance racial was removed. Endurance lost the hit/crit bonus it had in beta.

!!! note
    No source says whether Plainsrunning stacks with Travel Form, Cat Form or Feral Swiftness speed. Test it yourself. Ratings on this page are the guide's own judgment.

??? example "Macros"

    ```text
    #showtooltip War Stomp
    /cast War Stomp
    /cast [nostance] Healing Touch
    ```

    ```text
    #showtooltip
    /stopcasting
    /cast War Stomp
    ```

    The second macro interrupts your own cast to stomp a caster. Stomp, then shift out and heal, or shift into Bear while they're stunned.

## Starting zone walkthrough: Mulgore (1–~12)

**Camp Narache (1–6)**

<div class="steps" markdown>

1.  Your first trainer is **Gart Mistrunner** at Camp Narache.
2.  Plainstrider and mountain cougar quests, then the Battleboar quests and the Brambleblade Ravine quilboar. Spam Wrath and Moonfire, heal with Rejuvenation.
3.  Train Moonfire and Rejuvenation at **4**, Thorns at **6**.
4.  Take **The Great Outdoors** at about level 5 to unlock camping.

</div>

**Bloodhoof Village (6–11)**

1. The druid trainer is **Gennia Runetotem**. Set your hearthstone here.
2. Quests around the Venture Co. mine, Palemane gnolls, and the Red Rocks.
3. **Level 8:** Entangling Roots. **Level 10:** Nature's Grasp and your first talent point.
4. **Level 10 Bear Form:** take **Heeding the Call** in Thunder Bluff (Elder Rise, from Turak Runetotem in Classic). It sends you to Moonglade and teaches **Teleport: Moonglade**.

**Leaving (11–12)**

- **Skywatcher Plateau** (northwest Mulgore) is new: the Windshaper airship lands here, and a path leads toward Desolace. You can fly to [Zephras Isle](../../world/zephras-isle.md) to look around.
- Head east through the Barrens to the **Crossroads** at about 11.

## Route to 60 from Thunder Bluff

<div class="steps" markdown>

1.  **1–11**{ .lvl } Mulgore

    Bear Form quest at 10

2.  **11–20**{ .lvl } **The Barrens** (Crossroads)

    Lessons Anew at 14, **Aquatic Form at 16**. Durotar Supply and Logistics crates west of the Crossroads. Wailing Caverns

3.  **15–22**{ .lvl } Silverpine Forest

    [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) in Tirisfal; Ragefire Chasm

4.  **20**{ .lvl } Thunder Bluff

    **The Great Cat Spirit** (Cat Form, Prowl, Claw, Rip). First library-book unlock (Owen Thadd, Undercity)

5.  **20–30**{ .lvl } Stonetalon (Sun Rock Retreat), Ashenvale, Hillsbrad (Tarren Mill), Thousand Needles

    Shadowfang Keep, Razorfen Kraul

6.  **30–40**{ .lvl } Desolace, Arathi (Hammerfall), Stranglethorn (Grom'gol), Dustwallow (Brackenwall)

    Travel Form at 30. Avoid Dalaran: Horde are attacked on sight

7.  **35–45**{ .lvl } **[Riverglades](../../world/zones.md#riverglades)** from **Rog'mar**

    Flights to Stonard, Hammerfall, Kargath, Flame Crest. [Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md)

8.  **40–50**{ .lvl } Feralas (Camp Mojache; trainer Jannos Lighthoof), Tanaris, Badlands, Swamp of Sorrows, Hinterlands

    Kodo at 40; dual spec

9.  **50–58**{ .lvl } Un'Goro, Azshara, Felwood, Searing Gorge, Burning Steppes

    [Blackmaw Hold](../../content/dungeons/blackmaw-hold.md), [Shaper's Terrace](../../content/dungeons/shapers-terrace.md)

10.  **55–60**{ .lvl } Western and Eastern Plaguelands, Winterspring, Silithus

    Then [Mount Hyjal](../../world/zones.md#mount-hyjal)

</div>

**Class trainers:** Gart Mistrunner (Camp Narache), Gennia Runetotem (Bloodhoof Village), Turak, Sheal and Kym (Thunder Bluff), Jannos Lighthoof (Feralas), Loganaar (Moonglade).

## Faction-specific notes

- **Class quests:** Heeding the Call (10), Lessons Anew (14), A Lesson to Learn (16), The Great Cat Spirit (20), all from Thunder Bluff.
- **Mount:** **Kodo** at Bloodhoof Village at 40. Honored with Thunder Bluff gives −10%. The **Reins of the Pack Kodo** (6,000 Merchant's Favor) is a profession reward.
- **Reputation:** Thunder Bluff; Darkspear Raiders from [Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands). Windshaper reputation can be earned through cloth turn-ins in Mulgore and leads to a Galestrider at Exalted.
- **Barbershop:** Thunder Bluff gained one in Forever.
- **No Kirin Tor:** the Horde can't earn Kirin Tor reputation and is attacked in Dalaran.
- **Lore:** Hamuul Runetotem's Cenarion ties make Moonglade feel like home, and the Mount Hyjal story centers on the Cenarion Circle.

## Verdict

<div class="verdict" markdown>

The best Horde **bear** and the best druid for **PvP**. War Stomp in form is a real interrupt and escape. Endurance is permanent value for tanks. Plainsrunning makes 1–30 noticeably faster. Pick Windshaper Skyborne instead if you mostly play Cat or Balance in PvE and want haste.

| Spec | Rating |
|---|---|
| Bear | **5/5**{ .stars .s5 } |
| Cat | **4/5**{ .stars .s4 } |
| Balance | **3/5**{ .stars .s3 } |
| Restoration | **4/5**{ .stars .s4 } |
| PvP | **5/5**{ .stars .s5 } |

</div>
