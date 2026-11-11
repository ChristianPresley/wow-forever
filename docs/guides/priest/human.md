---
tags:
  - Priest
  - Human
  - Alliance
---

# Human Priest

:codex-priest:{ .fc-sigil aria-hidden="true" } <span class="fc-meta__kind">Add-on: Race</span> **:codex-alliance:{ .fc-sigil aria-hidden="true" } Alliance**{ .badge .faction } **Healer**{ .badge .heal } **DPS**{ .badge .dps } [Data and sources](index.md#sources)
{: .fc-meta data-class="priest" }

Read with the [Priest progression](index.md).

## Why this combo

Human Priest is a classic Alliance choice and **not a new combination**. It is the most simple healer in the game. Humans get more Spirit and crit, a stun breaker, and **Divine Grace**, a new emergency heal for another player. Stormwind is also the most central Alliance capital. It has the Stormwind Harbor boat to Auberdine, and you can easily go through Redridge to the new Riverglades.

**Best for:** Holy or Discipline healers, Alliance PvP healers, and players who want the easiest start.

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Will to Survive** *(new)* <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **5/5**{ .stars .s5 } PvP / **2/5**{ .stars .s2 } PvE</p>
<p markdown><span class="ability-label">PvE</span> Not often necessary. Breaks a stun from a mob during a bad pull</p>
<p markdown><span class="ability-label">PvP</span> Top-tier. Breaks Rogue openers, Hammer of Justice, Charge stuns</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Perception** <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 }</p>
<p markdown><span class="ability-label">PvE</span> Finds stealthed mobs in some dungeons</p>
<p markdown><span class="ability-label">PvP</span> Finds Rogues and Druids before they attack you</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Ruthless** *(new)* <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 }</p>
<p markdown><span class="ability-label">PvE</span> +1% crit: more Inspiration, Divine Aegis and Renewed Hope procs for healers. More damage for Shadow</p>
<p markdown><span class="ability-label">PvP</span> Same</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**The Human Spirit** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 }</p>
<p markdown><span class="ability-label">PvE</span> **+10% Spirit** (was 5%). Faster mana between pulls when you level. More in-combat regen through Meditation</p>
<p markdown><span class="ability-label">PvP</span> Longer fights</p>
</div>

</div>

**Priest spells unique to Humans**

| Spell | Level | Effect | Use |
|---|---|---|---|
| **Divine Grace** *(new)* | 10 | Instantly heals a friendly target below 50% health and **removes Weakened Soul**. You cannot cast it on yourself. 5-minute cooldown | Emergency save for a tank. Because it removes Weakened Soul, a Discipline Priest can shield the target again immediately |
| **Feedback** | (Classic spell) | Classic-era: drains the mana of casters who hit you | Some PvP situations |

Warcraft Tavern rates Divine Grace as acceptable for healers who use shields frequently. It is a group tool, because it cannot save *you*.

??? example "Macros"

    Break a stun and shield yourself with one button:

    ```
    #showtooltip Will to Survive
    /cast Will to Survive
    /cast [@player] Power Word: Shield
    ```

    Cast Divine Grace, then shield the same target (Discipline):

    ```
    #showtooltip Divine Grace
    /cast [@mouseover,help,nodead][help] Divine Grace
    /cast [@mouseover,help,nodead][help] Power Word: Shield
    ```

    !!! note
        It is not documented if Will to Survive and Divine Grace share the global cooldown. If the second line does not cast, push the macro button twice.

## Starting zone walkthrough (1–~12)

Humans start at **Northshire Abbey** in Elwynn Forest. The quest names below are from Classic. Northshire was not on the Blizzard list of reworked starting zones, but small changes are possible.

<div class="steps" markdown>

1.  **1–2**{ .lvl } Get the first quest from the Marshal outside the abbey. Kill wolves and kobolds in the valley. The Priest trainer is in **Northshire Abbey** (Classic: Priestess Anetta). Learn your spells there at each even level.
2.  **2–4**{ .lvl } Do the vineyard and kobold mine quests. At 4, train **Shadow Word: Pain** and use it as your first attack.
3.  **5**{ .lvl } Get **The Great Outdoors** for camping, and learn Cooking. Go to **Goldshire**. If you plan to make your own **Lesser Magic Wand**, learn Tailoring and Enchanting in Stormwind or Goldshire.
4.  **6**{ .lvl } Train **Power Word: Shield**. From now on, shield yourself before each pull.
5.  **6–10**{ .lvl } Do the Goldshire quests in Elwynn: Fargodeep Mine, the Stonefield and Maclure farms, the Eastvale logging camp, and the murlocs of Crystal Lake.
6.  **8**{ .lvl } Train Renew and Fade.
7.  **10**{ .lvl } Go to a Priest trainer in Goldshire or the **Cathedral of Light** in Stormwind. Learn **Mind Blast**, **Divine Grace** and your first talent point. Get the level-10 class quest (Warcraft Tavern says class quests come at 10 and 20).
8.  **10–12**{ .lvl } Complete Elwynn (Hogger, the Brackwell pumpkin patch). Then go to **Westfall**, or to **Loch Modan** through Dun Morogh.

</div>

## Route to 60 from Stormwind

<div class="steps" markdown>

1.  **10–15**{ .lvl } Westfall (or Loch Modan)

    <span class="step-label">Hub / flight path</span> Sentinel Hill

2.  **15–20**{ .lvl } Redridge Mountains

    <span class="step-label">Hub / flight path</span> Lakeshire. Three Corners supply camp (Azeroth Commerce Authority)

3.  **18–24**{ .lvl } The Deadmines. [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) from Ironforge

    <span class="step-label">Hub / flight path</span> —

4.  **18–30**{ .lvl } Darkshore (boat from Stormwind Harbor), Duskwood, Wetlands, Ashenvale

    <span class="step-label">Hub / flight path</span> Darkshire, Menethil Harbor, Astranaar

5.  **30–40**{ .lvl } Alterac Mountains (Dalaran), Arathi Highlands, Stranglethorn Vale, Desolace

    <span class="step-label">Hub / flight path</span> Refuge Pointe, Booty Bay, Nijel's Point

6.  **35–45**{ .lvl } **Riverglades** (from Redridge)

    <span class="step-label">Hub / flight path</span> **Farholde Keep** (flights to Lakeshire, Thelsamar, Morgan's Vigil)

7.  **40–50**{ .lvl } Dustwallow Marsh, Feralas, Tanaris, Hinterlands, Badlands, Swamp of Sorrows

    <span class="step-label">Hub / flight path</span> Theramore, Feathermoon, Gadgetzan, Aerie Peak

8.  **50–60**{ .lvl } Un'Goro, Azshara, Burning Steppes, Western and Eastern Plaguelands, Winterspring, Silithus

    <span class="step-label">Hub / flight path</span> Marshal's Refuge, Chillwind Camp, Everlook

9.  **60**{ .lvl } Mount Hyjal (from Winterspring)

    <span class="step-label">Hub / flight path</span> Tainted Foothills

</div>

- **Class trainers:** the Cathedral of Light in Stormwind, and Goldshire and Northshire for early ranks.
- **Boats:** Stormwind Harbor ↔ Auberdine is new. The Menethil → Southshore → Auberdine loop is also new. See [Travel](../../world/travel.md).
- **PvP vendor:** Champion's Hall, Stormwind.

## Faction-specific notes

- **Mount:** Stormwind horses at 40 (100g with Apprentice Riding). Honored with Stormwind gives 10% off.
- **Reputation:** Stormwind is your home faction. The Diplomacy racial is gone. If you want faster reputation, get the Legacy talent *Diplomat*.
- **Dalaran:** Alliance players can get **Kirin Tor** reputation. The [City of Dalaran](../../content/dungeons/city-of-dalaran.md) dungeon is there.
- **Riverglades** is the lost frontier of Stormwind. Sunnyglade was a Stormwind town that burned in the First War. The Brotherhood of the Horse at Farholde Keep are its descendants. A Human Priest fits the story well.
- **Lore:** The Cathedral of Light in Stormwind and the Church of the Holy Light lead the Alliance priests.

## Verdict

<div class="verdict" markdown>

**The safe, strong default for Alliance healers.** +10% Spirit and +1% crit help each spec. Will to Survive is one of the best PvP racials in the game, and Divine Grace adds a real tank save for Discipline. If you want more burst damage or self-protection, select Night Elf or Gnome. Select Dwarf for Stoneform.

</div>
