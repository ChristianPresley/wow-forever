---
tags:
  - Druid
  - Skyborne
  - Alliance
---

# High Order Skyborne Druid

<div class="guide-head" data-class="druid" markdown>

:codex-druid:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Add-on</span> **:codex-alliance:{ .fc-sigil aria-hidden="true" } Alliance**{ .badge .faction } **Tank**{ .badge .tank } **Healer**{ .badge .heal } **DPS**{ .badge .dps }

<p class="gh-note" markdown>Read this page with the [Druid guide](index.md). This page gives only the differences for an Alliance Skyborne.</p>

</div>

## Why this combo

**NEW in Forever.** The Skyborne (*shen'dorei*) exist only in this game. The High Order are their Alliance faction. Their ancestors are Highborne magisters of Eldre'Thalas. Skyborne druids get their forms from the wind spirits **Urs'endris** (the Great Windborne Bear) and **Saeyleenan** (the Great Windborne Cat). Their forms have a special appearance, with 4 colors at the barbershop.

You get **haste** (Wind Blessed), a **regeneration cooldown** (Read Ley Line) and **Walk on Air**, which works in forms. Warcraft Tavern calls the difference from Night Elf **marginal**. Your selection is mostly about appearance and the Zephras Isle story.

!!! warning "Paid race"
    Skyborne need the **Skyborne Heroic Pack** or a higher edition. See [Editions](../../about/editions.md) and [Skyborne](../../characters/races.md#skyborne).

**Best for:** Balance and Restoration (mana regen), Cat if haste is important to you. **Compared with Night Elf:** less burst crit and no Shadowmeld, but more sustain and mobility. See [Night Elf Druid](night-elf.md).

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Read Ley Line** <span class="ability-type active">Active: +50% health and mana regen for 15 s. +100% when *Attuned* (1 hr buff when you stand at a Ley Line)</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 }</p>
<p markdown><span class="ability-label">PvE</span> Very useful for Balance downtime when you level, and for Resto mana. **Not usable with Innervate**</p>
<p markdown><span class="ability-label">PvP</span> Short reset between fights</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Walk on Air** <span class="ability-type active">Active: 10 s controlled glide. **Works in forms**</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 }</p>
<p markdown><span class="ability-label">PvE</span> Skip paths, survive falls, reach ledges</p>
<p markdown><span class="ability-label">PvP</span> Escape off cliffs, flag-carrier tricks. Cooldown 1.5 or 2 min (*conflict*)</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Wind Blessed** <span class="ability-type passive">Passive: haste</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 }</p>
<p markdown><span class="ability-label">PvE</span> Faster casts and swings, more Energy use</p>
<p markdown><span class="ability-label">PvP</span> Same</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Elemental Insight** <span class="ability-type passive">Passive: +5% damage vs Elementals</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **2/5**{ .stars .s2 }</p>
<p markdown><span class="ability-label">PvE</span> Situational: Hyjal and Skywall elementals, some dungeons</p>
<p markdown><span class="ability-label">PvP</span> None</p>
</div>

</div>

!!! conflict "Conflict: Wind Blessed"
    Sources give 1%, 2% or 3% haste. Blizzard's latest notes say **2%**.

??? example "Macros"

    ```text
    #showtooltip Read Ley Line
    /cast [nocombat] Read Ley Line
    /use [nocombat] Morning Glory Dew
    ```

    ```text
    #showtooltip Walk on Air
    /cast Walk on Air
    ```

    Replace *Morning Glory Dew* with the drink that you have. Read Ley Line and Innervate do not stack. Thus, as Resto, use 1 and keep the other.

## Starting zone walkthrough: Zephras Isle (1–~12)

Both Skyborne factions use [Zephras Isle](../../world/zephras-isle.md), in different phases. It takes you to about **12–14**.

**Thendal Village (1–5)**

<div class="steps" markdown>

1.  Start at Thendal Village. Quests: *Coming of Age*, *Harmony in Balance*, *The Cirrusfly Queen*, *Harvesting Windstones* (gathering profession voucher), *Falling With Style* (teaches you to use Walk on Air) and *The Anchors of Zephras*.
2.  Your faction opener is ***Reading the Leylines***, which shows you how to get Attuned.
3.  Play as a caster, as usual: Wrath, Moonfire, Rejuvenation.

</div>

**Road to Shen'dar Village (5–9)**

1. Fight Al'Aketh thugs under Malduko Cloudcrash. Ride the *Blessing of Zephras* tornadoes for +40% speed.
2. **The Great Outdoors** (Raan Wildwind) teaches [camping](../../systems/camping.md).
3. In Shen'dar Village, Constable Aonda gives bandit, hippogryph and Prideclaw quests. The last quests are "Badwind" Bennic and *WANTED: Vulgara the Insatiable*.

**Falaath Village and Valanaar (9–11)**

1. Wear the Mark of Akir. Infiltrate **Falaath Village**, which the cult holds.
2. Return the Shadowsong Family Signet to High Elder Talaanis Shadowsong in **Valanaar** and meet Supreme Magister **Elaadrin Evengale**.
3. **Level 10 Bear Form:** ***The Great Ursera Spirit***. Skyborne get Bear Form on the island, not from the Darnassus quest. The Ursera bear chain from Thendal Village ends with Urs'anah.

**Gustberry Lowlands and Shadowgale Forest (11–13)**

1. High Order chain *The Missing Scholar* (Shriekling Den), then Index Esoteria at the Overlook Standing Stones.
2. **Nightclaw druids** in Shadowgale Forest: the repeatable *Mercy Falls on Deaf Ears* gives Nightclaw reputation. *The Ties That Bind* and *Wounds of Betrayal* lead to Commander Haalien. Recording crystals in Nightclaw Cavern tell the Skyborne origin story.
3. Secret: `/sing` at the frogs in Gustberry Lowlands for the *Musical Gustjumper* pet.
4. Finish with the Shrine of Akir assault and *Confront Lorthuna*.

**Trainers:** Method lists **Xyton Silverwind**, **Naeluna Swiftmend** and **Lotheluum Starbreeze** on Zephras Isle. A 5 Nov hotfix fixed a Zephras druid trainer that did not spawn.

**Galestrider:** Fairweather Stables (53.8, 81.3) sells the racial mount for level 40. High Order reputation gives a discount of 5–20%.

## Route to 60 from Valanaar

The High Order airship leaves the **east Skydock** for **north Dalaran** in the Alterac Mountains, a 30–40 zone. Do not quest there at 12. Go to the Alliance lowbie zones.

<div class="steps" markdown>

1.  **1–13**{ .lvl } Zephras Isle

    Bear Form at 10 on the island

2.  **13**{ .lvl } Dalaran → Hillsbrad → Southshore

    Walk south. Take the new **Southshore pier** boat loop to Menethil, or continue on foot to Arathi and the Wetlands

3.  **13–20**{ .lvl } Loch Modan, Westfall, Redridge (via Ironforge and the Tram) or Darkshore (via Menethil → Auberdine)

    Lessons Anew (14) and Aquatic Form (16): it is *unconfirmed* where Skyborne take these. Look in Valanaar first, then in Darnassus

4.  **20**{ .lvl } Zephras Isle

    ***The Great Windborne Cat Spirit*** (Cat Form, Prowl, Claw, Rip)

5.  **20–30**{ .lvl } Ashenvale, Wetlands, Duskwood, Hillsbrad

    [Excavation Site](../../content/dungeons/excavation-site.md)

6.  **28–40**{ .lvl } **Alterac and [Dalaran](../../world/zones.md#dalaran)**, Arathi, Desolace, Stranglethorn, Dustwallow

    Your airship hub becomes your quest hub. [City of Dalaran](../../content/dungeons/city-of-dalaran.md). Kirin Tor reputation

7.  **35–45**{ .lvl } **[Riverglades](../../world/zones.md#riverglades)** (Farholde Keep)

8.  **40–60**{ .lvl } Same Alliance route as the [Druid guide](index.md#leveling-walkthrough-160)

    Felwood trainer Golhine the Hooded. Moonglade via Teleport

</div>

**Return home:** the airship goes in both directions, and all players can visit the island. Reportedly, Dalaran has no flight master. Walk to Southshore or Refuge Pointe for flights. Sources list **Alfina Nightgaze** in Dalaran as a druid trainer.

## Faction-specific notes

- **Class quests:** island versions at 10 (*The Great Ursera Spirit*) and 20 (*The Great Windborne Cat Spirit*). The Darnassus quests are for Night Elves.
- **Reputation:** High Order (home) and **Kirin Tor** (Dalaran, Alliance-only). Nightclaw from the Zephras repeatable. Exalted High Order lets other races buy Galestriders.
- **Mount:** Galestrider (Umber, Stormy, Empyrean, plus Swift versions).
- **Form colors:** Default (blue/white), Deep Purple and Blue, Umber, Empyrean, changed at the barbershop.
- **Models:** HD only at launch. SD models are expected in early 2027.
- **Languages:** Darnassian and Common. You can talk Darnassian with Windshaper elves across the faction line.
- **Lore:** the High Order look for lost arcane knowledge and are close to the Kirin Tor. A druid among them follows the older, kaldorei side of Skyborne tradition.

## Verdict

<div class="verdict" markdown>

A good, distinctive Alliance druid. **Wind Blessed** and **Read Ley Line** make it the best Alliance pick for **Balance and Restoration**, and it is almost equal to Night Elf for Cat. You lose Shadowmeld and Elune's Light burst. The difficult part is the start: at level 12, you arrive in a 30–40 zone and must walk to the lowbie zones.

| Spec | Rating |
|---|---|
| Cat | **4/5**{ .stars .s4 } |
| Bear | **3/5**{ .stars .s3 } |
| Balance | **5/5**{ .stars .s5 } |
| Restoration | **5/5**{ .stars .s5 } |
| PvP | **3/5**{ .stars .s3 } |

*The ratings are the opinion of this guide.*

</div>
