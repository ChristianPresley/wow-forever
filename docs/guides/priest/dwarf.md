---
tags:
  - Priest
  - Dwarf
  - Alliance
---

# Dwarf Priest

<div class="guide-head" data-class="priest" markdown>

:codex-priest:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Add-on</span> **:codex-alliance:{ .fc-sigil aria-hidden="true" } Alliance**{ .badge .faction } **Healer**{ .badge .heal } **DPS**{ .badge .dps }

<p class="gh-note" markdown>Read with the [Priest guide](index.md).</p>

</div>

## Why this combo

Dwarf Priest is a Classic combination and **not new**. In Classic, Dwarves were *the* raid Priest because they owned Fear Ward. In Forever, **Fear Ward is baseline for every Priest**, so the Dwarf's case now rests on **Stoneform**, the most flexible defensive racial in the game, plus +1% hit, Desperate Prayer and the new **Chastise** root.

**Best for:** Shadow Priests (free hit), Hardcore players (two self-saves), and PvP healers who fear Rogues and poisons.

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Stoneform** *(changed)* <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **5/5**{ .stars .s5 }</p>
<p markdown><span class="ability-label">PvE</span> Removes bleeds, poisons and diseases and grants immunity, plus **10% physical damage reduction for 8 s**. Saves you from poisons and plague effects, and from a loose mob on the healer</p>
<p markdown><span class="ability-label">PvP</span> Cleanses Rogue poisons, Hunter Serpent Sting and Warrior Rend; 10% reduction under a melee train</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Find Treasure** <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **2/5**{ .stars .s2 }</p>
<p markdown><span class="ability-label">PvE</span> Shows treasure chests on the minimap. Useful gold while leveling</p>
<p markdown><span class="ability-label">PvP</span> —</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Artisan's Precision** *(new)* <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 } Shadow / **2/5**{ .stars .s2 } healer</p>
<p markdown><span class="ability-label">PvE</span> **+1% hit**. Shadow needs hit, so this is a real gain; Holy damage is mostly covered by Holy Precision</p>
<p markdown><span class="ability-label">PvP</span> Same</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Big Game Hunter** *(new)* <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 } leveling</p>
<p markdown><span class="ability-label">PvE</span> +5% damage against Beasts. A lot of leveling quests are beasts</p>
<p markdown><span class="ability-label">PvP</span> Druids in animal forms are probably not Beasts (*unconfirmed*)</p>
</div>

</div>

**Priest spells unique to Dwarves**

| Spell | Level | Effect | Use |
|---|---|---|---|
| **Desperate Prayer** | (Classic spell) | An instant self-heal on a long cooldown (Classic-era behavior; Blizzard lists it as unchanged) | Panic button while soloing and in Hardcore |
| **Chastise** *(new)* | 20 | Roots a **Humanoid** for 2 s. Instant, 2-minute cooldown | Escape a melee Humanoid, peel for a flag carrier, or stop a runner. It only works on Humanoids, so it's weak against Beasts, Undead and Elementals |

Combined with Psychic Scream and Stoneform, a Dwarf has three self-defense buttons by level 20.

??? example "Macros"

    Stoneform and shield yourself:

    ```
    #showtooltip Stoneform
    /cast Stoneform
    /cast [@player] Power Word: Shield
    ```

    Chastise the focus (set a Warrior or Rogue as focus in PvP):

    ```
    #showtooltip Chastise
    /cast [@focus,harm][harm] Chastise
    ```

## Starting zone walkthrough (1–~12)

Dwarves start in **Coldridge Valley**, Dun Morogh. Quest names are Classic-era; Forever adds the new [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) dungeon near Ironforge but hasn't announced a rework of Coldridge.

<div class="steps" markdown>

1.  **1–2**{ .lvl } take the opening quests at **Anvilmar** and kill wolves and troggs in the valley. Your Priest trainer is inside **Anvilmar** (Classic: Branstock Khalder).
2.  **2–5**{ .lvl } the troll camp quests (frostmane seers and novices) and the mail delivery to Kharanos. Train **Shadow Word: Pain** at 4.
3.  **5**{ .lvl } take **The Great Outdoors**, learn Cooking, and plan your wand (Tailoring + Enchanting or buy one in Ironforge).
4.  **6**{ .lvl } **Power Word: Shield**. Kill **Grik'nir the Cold** in the cave for the valley's last quest.
5.  **6–10**{ .lvl } walk through the tunnel to **Kharanos**. Do the Thunderbrew, wendigo, Shimmerweed and Gnomeregan-refugee quests around the town. There is a Priest trainer in Kharanos for early ranks (Classic-era).
6.  **10**{ .lvl } take your first talent and the level-10 class quest. Visit **Ironforge's Mystic Ward** for the full Priest trainers.
7.  **10–12**{ .lvl } finish Dun Morogh (Brewnall Village, Shimmer Ridge, the Gnomeregan approach), then go east through the tunnel to **Loch Modan**.

</div>

## Route to 60 from Ironforge

<div class="steps" markdown>

1.  **10–18**{ .lvl } Loch Modan

    <span class="step-label">Hub / flight path</span> Thelsamar

2.  **13–20**{ .lvl } [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) (Ironforge)

    <span class="step-label">Hub / flight path</span> —

3.  **15–22**{ .lvl } Westfall or Redridge via the Deeprun Tram

    <span class="step-label">Hub / flight path</span> Sentinel Hill, Lakeshire

4.  **20–30**{ .lvl } **Wetlands** (new [Excavation Site](../../content/dungeons/excavation-site.md)), Duskwood, Ashenvale via Menethil

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
- Ironforge is the closest capital to the Riverglades. Farholde Keep's flight master connects to **Thelsamar** in Loch Modan.
- Uldaman (Badlands) and Gnomeregan are dwarf-flavored dungeons on your route.

## Faction-specific notes

- **Mount:** Ironforge rams at 40 (100g). Honored with Ironforge gives 10% off.
- **Reputation:** Ironforge. The Wetlands Excavation Site and Uldaman tie into the Explorers' League storyline (Classic-era lore).
- **Fear Ward is no longer yours alone.** If you join a raid guild expecting Dwarf-only demand from Classic, that's gone. Stoneform and hit are still good reasons.
- **Lore:** Ironforge's priests serve the Holy Light alongside Stormwind's church; the Mystic Ward is their home.

## Verdict

<div class="verdict" markdown>

**The best defensive Priest.** Stoneform handles poisons, bleeds, diseases and melee damage, Desperate Prayer is a free self-heal, and Chastise adds a third escape. +1% hit makes Dwarf a strong Alliance **Shadow** pick. Losing exclusive Fear Ward makes it less mandatory than in Classic, but it's still one of the safest choices, especially on Hardcore.

</div>
