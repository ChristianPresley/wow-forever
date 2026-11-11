---
tags:
  - Priest
  - Dwarf
  - Alliance
---

# Dwarf Priest

<div class="guide-head" data-class="priest" markdown>

:codex-priest:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Add-on</span> **:codex-alliance:{ .fc-sigil aria-hidden="true" } Alliance**{ .badge .faction } **Healer**{ .badge .heal } **DPS**{ .badge .dps }

<p class="gh-note" markdown>Read with the [Priest progression](index.md).</p>

</div>

## Why this combo

Dwarf Priest is a Classic combination and **not new**. In Classic, Dwarves were *the* raid Priest because only they had Fear Ward. In Forever, **Fear Ward is baseline for every Priest**. Now the strengths of the Dwarf are **Stoneform**, the most flexible defensive racial in the game, +1% hit, Desperate Prayer and the new **Chastise** root.

**Best for:** Shadow Priests (free hit), Hardcore players (two self-saves), and PvP healers who fear Rogues and poisons.

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Stoneform** *(changed)* <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **5/5**{ .stars .s5 }</p>
<p markdown><span class="ability-label">PvE</span> Removes bleeds, poisons and diseases and gives immunity to them, plus **10% physical damage reduction for 8 s**. Protects you from poisons and plague effects, and from a mob that attacks the healer</p>
<p markdown><span class="ability-label">PvP</span> Removes Rogue poisons, Hunter Serpent Sting and Warrior Rend. 10% reduction when many melee players attack you</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Find Treasure** <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **2/5**{ .stars .s2 }</p>
<p markdown><span class="ability-label">PvE</span> Shows treasure chests on the minimap. Useful gold when you level</p>
<p markdown><span class="ability-label">PvP</span> —</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Artisan's Precision** *(new)* <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 } Shadow / **2/5**{ .stars .s2 } healer</p>
<p markdown><span class="ability-label">PvE</span> **+1% hit**. This is a real gain for Shadow, because Shadow needs hit. Holy Precision gives most of the hit that Holy damage needs</p>
<p markdown><span class="ability-label">PvP</span> Same</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Big Game Hunter** *(new)* <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 } leveling</p>
<p markdown><span class="ability-label">PvE</span> +5% damage against Beasts. Many leveling quests have Beasts as targets</p>
<p markdown><span class="ability-label">PvP</span> Druids in animal forms are probably not Beasts (*unconfirmed*)</p>
</div>

</div>

**Priest spells unique to Dwarves**

| Spell | Level | Effect | Use |
|---|---|---|---|
| **Desperate Prayer** | (Classic spell) | An instant self-heal on a long cooldown (Classic-era behavior. Blizzard lists it as unchanged) | Emergency button when you solo and in Hardcore |
| **Chastise** *(new)* | 20 | Roots a **Humanoid** for 2 s. Instant, 2-minute cooldown | Escape from a melee Humanoid, protect a flag carrier, or stop a player who runs. It works only on Humanoids. It is weak against Beasts, Undead and Elementals |

With Psychic Scream and Stoneform, a Dwarf has three self-defense buttons by level 20.

??? example "Macros"

    Use Stoneform and shield yourself:

    ```
    #showtooltip Stoneform
    /cast Stoneform
    /cast [@player] Power Word: Shield
    ```

    Cast Chastise on the focus (in PvP, set a Warrior or Rogue as focus):

    ```
    #showtooltip Chastise
    /cast [@focus,harm][harm] Chastise
    ```

## Starting zone walkthrough (1–~12)

Dwarves start in **Coldridge Valley**, Dun Morogh. Quest names are Classic-era. Forever adds the new [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) dungeon near Ironforge. Blizzard has not announced a rework of Coldridge.

<div class="steps" markdown>

1.  **1–2**{ .lvl } Get the first quests at **Anvilmar**. Kill wolves and troggs in the valley. Your Priest trainer is in **Anvilmar** (Classic: Branstock Khalder).
2.  **2–5**{ .lvl } Do the troll camp quests (frostmane seers and novices) and the mail delivery to Kharanos. At 4, train **Shadow Word: Pain**.
3.  **5**{ .lvl } Get **The Great Outdoors** and learn Cooking. Plan how to get your wand: Tailoring + Enchanting, or buy one in Ironforge.
4.  **6**{ .lvl } Train **Power Word: Shield**. Kill **Grik'nir the Cold** in the cave for the last quest of the valley.
5.  **6–10**{ .lvl } Go through the tunnel to **Kharanos**. Do the Thunderbrew, wendigo, Shimmerweed and Gnomeregan-refugee quests near the town. Kharanos has a Priest trainer for early ranks (Classic-era).
6.  **10**{ .lvl } Get your first talent and the level-10 class quest. Go to the **Mystic Ward in Ironforge** for the full Priest trainers.
7.  **10–12**{ .lvl } Complete Dun Morogh (Brewnall Village, Shimmer Ridge, the Gnomeregan approach). Then go east through the tunnel to **Loch Modan**.

</div>

## Route to 60 from Ironforge

<div class="steps" markdown>

1.  **10–18**{ .lvl } Loch Modan

    <span class="step-label">Hub / flight path</span> Thelsamar

2.  **13–20**{ .lvl } [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) (Ironforge)

    <span class="step-label">Hub / flight path</span> —

3.  **15–22**{ .lvl } Westfall or Redridge through the Deeprun Tram

    <span class="step-label">Hub / flight path</span> Sentinel Hill, Lakeshire

4.  **20–30**{ .lvl } **Wetlands** (new [Excavation Site](../../content/dungeons/excavation-site.md)), Duskwood, Ashenvale through Menethil

    <span class="step-label">Hub / flight path</span> Menethil Harbor

5.  **30–40**{ .lvl } Arathi Highlands, Alterac Mountains, Stranglethorn Vale, Desolace

    <span class="step-label">Hub / flight path</span> Refuge Pointe, Booty Bay

6.  **35–45**{ .lvl } **Riverglades** (from the Badlands or Redridge)

    <span class="step-label">Hub / flight path</span> **Farholde Keep** (flights to Thelsamar and Lakeshire)

7.  **40–50**{ .lvl } Badlands, Swamp of Sorrows, Hinterlands, Tanaris, Feralas, Dustwallow

    <span class="step-label">Hub / flight path</span> Aerie Peak, Gadgetzan, Theramore

8.  **50–60**{ .lvl } Searing Gorge, Burning Steppes, Un'Goro, Azshara, Plaguelands, Winterspring, Silithus

    <span class="step-label">Hub / flight path</span> Morgan's Vigil, Chillwind Camp

9.  **60**{ .lvl } Mount Hyjal (from Winterspring)

    <span class="step-label">Hub / flight path</span> Tainted Foothills

</div>

- **Class trainers:** the **Mystic Ward** in Ironforge.
- Ironforge is the nearest capital to the Riverglades. The flight master at Farholde Keep connects to **Thelsamar** in Loch Modan.
- Uldaman (Badlands) and Gnomeregan are dungeons with a dwarf theme on your route.

## Faction-specific notes

- **Mount:** Ironforge rams at 40 (100g). Honored with Ironforge gives 10% off.
- **Reputation:** Ironforge. The Wetlands Excavation Site and Uldaman connect to the Explorers' League story (Classic-era lore).
- **Fear Ward is no longer only yours.** In Classic, raid guilds wanted Dwarves for Fear Ward. That demand is gone. Stoneform and hit are still good reasons to play a Dwarf.
- **Lore:** The priests of Ironforge serve the Holy Light together with the church of Stormwind. The Mystic Ward is their home.

## Verdict

<div class="verdict" markdown>

**The best defensive Priest.** Stoneform helps against poisons, bleeds, diseases and melee damage. Desperate Prayer is a free self-heal, and Chastise adds a third escape. +1% hit makes Dwarf a strong Alliance **Shadow** choice. Without exclusive Fear Ward, Dwarf is less necessary than in Classic. But it is still one of the safest choices, especially on Hardcore.

</div>
