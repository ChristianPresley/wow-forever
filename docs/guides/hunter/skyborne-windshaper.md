---
tags:
  - Hunter
  - Skyborne
  - Horde
---

# Skyborne (Windshaper) Hunter

<div class="guide-head" data-class="hunter" markdown>

:codex-hunter:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Add-on</span> **:codex-horde:{ .fc-sigil aria-hidden="true" } Horde**{ .badge .faction } **DPS**{ .badge .dps }

<p class="gh-note" markdown>Read with the [Hunter guide](index.md).</p>

</div>

!!! warning "Paid race"
    Skyborne need the **Skyborne Heroic Pack** or a higher edition. Refer to [Editions](../../about/editions.md).

## Why this combo

**NEW in Forever.** The Horde [Skyborne](../../characters/races.md#skyborne), the **Windshapers**, can be Hunters (and also Druid, Rogue, Shaman and Warrior). They are the shamanic half of the race. Their ancestors are kaldorei, and they are allies of the Earthen Ring.

The Alliance High Order has **Read Ley Line** (regen). Windshapers have **Skysight** (movement speed) in its place. For a Hunter, this gives:

- **Wind Blessed** gives passive **haste**. Haste makes Auto Shot, casts and the global cooldown faster.
- **Skysight** gives +15% speed for 15 s (+30% while *Charged*). Use it to kite and to travel.
- **Walk on Air** gives a 10 s glide to escape or to make a short path.
- They arrive at **Skywatcher Plateau**, near Thunder Bluff. From there, you follow the Kalimdor route of the Tauren.

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Walk on Air** <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 }</p>
<p markdown><span class="ability-label">PvE</span> 10 s glide. A short path down cliffs (Thousand Needles, Feralas, Un'Goro) and a Hardcore escape</p>
<p markdown><span class="ability-label">PvP</span> Jump off a ledge to break line of sight</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Skysight** <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 } PvP</p>
<p markdown><span class="ability-label">PvE</span> +15% speed for 15 s. At an elemental convergence, you get *Charged* for 1 hr, which increases it to +30%. Travel before you have a mount</p>
<p markdown><span class="ability-label">PvP</span> Kite melee out of the deadzone. Carry flags or chase flag carriers</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Wind Blessed** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 }</p>
<p markdown><span class="ability-label">PvE</span> Passive haste: more Auto Shots, faster Aimed and Sniper Shot casts</p>
<p markdown><span class="ability-label">PvP</span> Faster Aimed Shot</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Elemental Insight** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **2/5**{ .stars .s2 }</p>
<p markdown><span class="ability-label">PvE</span> +5% damage to Elementals: Zephras Isle, Silithus, Un'Goro, [Shaper's Terrace](../../content/dungeons/shapers-terrace.md)</p>
<p markdown><span class="ability-label">PvP</span> Nothing</p>
</div>

</div>

!!! conflict "Conflicts"
    - **Wind Blessed:** sources give 1%, 2% or 3% haste. The latest official notes say **2%**.
    - **Walk on Air** cooldown: 1.5 or 2 minutes.
    - The 5 November hotfix note puts Plainsrunning in the same group as Skyborne. Plainsrunning is a Tauren racial. It is not clear if Blizzard also changed a Skyborne speed racial.

??? example "Macros"

    ```text
    #showtooltip Skysight
    /cast Skysight
    /cast Concussive Shot
    ```

    When a melee enemy comes near, this macro gives you speed and snares the enemy at the same time.

    ```text
    #showtooltip Walk on Air
    /petfollow
    /cast Walk on Air
    ```

## Starting zone walkthrough 1–12

All Skyborne start in **Thendal Village** on [Zephras Isle](../../world/zephras-isle.md). It is a sanctuary zone where both factions do quests in the same area, but in different phases. The isle takes you to about level 12–14. Trainers are in Thendal Village and **Valanaar**.

<div class="steps" markdown>

1.  **1–5**{ .lvl } Thendal Village

    - *Coming of Age*, *Harmony in Balance*, *The Cirrusfly Queen*, *Harvesting Windstones* (a gathering-profession voucher: Skinning), *Falling With Style* and *The Anchors of Zephras*. The Ursera bear chain ends with Urs'anah.
    - Faction opener: **The Gift of Skysight** (Windshaper). This quest gives you your racial.
    - At 4, train Serpent Sting.

2.  **5–9**{ .lvl } The road to Shen'dar Village

    - Al'Aketh thugs under Malduko Cloudcrash. *Blessing of Zephras* tornadoes (+40% speed).
    - **The Great Outdoors** from Raan Wildwind unlocks [camping](../../systems/camping.md).
    - **Shen'dar Village**: bandits, hippogryphs, Prideclaws, "Badwind" Bennic and *WANTED: Vulgara the Insatiable*. The 2 factions fight small battles at the Windsong Standing Stones.
    - Train Arcane Shot, Hunter's Mark and Concussive Shot.

3.  **10**{ .lvl } The first pet

    - *Taming the Beast* (Wowhead quest 94978): use a Taming Rod on a **Windsong Crawler**, a crab near water. Warcraft Tavern gives the final Skyborne quest the same name (94013).
    - When you complete the chain, you learn Tame Beast, Feed Pet and Revive Pet.
    - Players report **foxes** on the island (*unconfirmed*). The Fox is a new family with *Trickster's Dance*.
    - First talent: **Deadly Aspects**.

4.  **9–12+**{ .lvl } Falaath, Valanaar and the finale

    - *Secret Agent Elf*: go secretly into **Falaath Village**. Defeat Commanders Cyclas and Aanders. Get the Shadowsong Family Signet back.
    - **Valanaar:** give the signet to Talaanis Shadowsong and meet **Grand Skyseer Ayessa Dawnsinger** (*The Grand Skyseer*). Set your hearthstone here.
    - **Gustberry Lowlands:** the Windshaper chain *The Broken Construct* and the Windfield Orchard chain. `/sing` at the frogs for the *Musical Gustjumper* pet.
    - **Shadowgale Forest:** *In Service of Zephras* → *Blood for Blood*. Nightclaw reputation from *Mercy Falls on Deaf Ears*. Recording crystals in Nightclaw Cavern.
    - **Finale:** East Pylon Watchtower, *Desperate Times*, the Shrine of Akir, *Confront Lorthuna*, Rohash, then *The Fate of Zephras* and *What Comes Next*.

</div>

## Route to 60 from Valanaar

**Class trainer city:** Valanaar. After you leave, Thunder Bluff (Hunter Rise) is the nearest.

The **west Skydock airship** goes to **Skywatcher Plateau** in northwest Mulgore, reportedly every 5 minutes.

<div class="steps" markdown>

1.  **12–20**{ .lvl } The remaining Mulgore quests, then the Barrens (Crossroads; **Durotar Supply and Logistics** crate camp)

    <span class="step-label">Travel</span> Thunder Bluff wind rider

2.  **15–25**{ .lvl } Wailing Caverns, Silverpine, [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md)

    <span class="step-label">Travel</span> Orgrimmar–Undercity zeppelin

3.  **18–30**{ .lvl } Stonetalon (Sun Rock), Ashenvale, Hillsbrad (Tarren Mill), Thousand Needles

    <span class="step-label">Travel</span> Sun Rock

4.  **30–40**{ .lvl } Desolace (path from Skywatcher Plateau), Arathi, Stranglethorn, Dustwallow

    <span class="step-label">Travel</span> Shadowprey Village

5.  **35–45**{ .lvl } **[Riverglades](../../world/zones.md#riverglades)** (Rog'mar), or Shen'dralas, the home of the Shen'dralar ancestors of the Skyborne (level range unknown)

    <span class="step-label">Travel</span> Steamwheedle ferry

6.  **40–50**{ .lvl } Feralas, Tanaris, Badlands, Swamp of Sorrows, Hinterlands

    <span class="step-label">Travel</span> Camp Mojache

7.  **50–60**{ .lvl } Un'Goro, Silithus (Elemental Insight), Azshara, Felwood, Winterspring, Plaguelands

    <span class="step-label">Travel</span> Everlook

8.  **60**{ .lvl } [Mount Hyjal](../../world/zones.md#mount-hyjal)

    <span class="step-label">Travel</span> Darkwhisper Gorge

</div>

!!! warning "Dalaran is hostile"
    Do not use the [City of Dalaran](../../content/dungeons/city-of-dalaran.md) quest hub. Dalaran belongs to the High Order, not to you. In Dalaran, the guards attack Horde players when they see them, and Horde players cannot get Kirin Tor reputation.

## Faction-specific notes

- **Reputation:** **Windshapers**. Cloth turn-ins in **Mulgore** count. At Exalted, other Horde races can buy Galestriders.
- **Earthen Ring:** the ally of the Windshapers. Muln Earthfury in Mulgore represents it.
- **Mount:** **Galestrider** from Fairweather Stables (53.8, 81.3) on Zephras, in Umber, Stormy or Empyrean, with a 5–20% reputation discount.
- **Language:** Darnassian and Orcish. You can speak Darnassian with Alliance Skyborne.
- **Library books:** Owen Thadd, Undercity.
- **PvP:** Darkspear Raiders reputation. Hall of Legends in Orgrimmar. At launch, Blizzard locked Horde character creation on PvP rulesets for population balance.

## Verdict

<div class="verdict" markdown>

A fast, mobile Horde Hunter. Troll has burst when you need it. Passive haste gives a constant bonus in its place. Skysight and Walk on Air give the best mobility of all Horde Hunters. You do not get the pet damage of Orc or the durability of Tauren. Select Windshaper if you have the pack and want the Zephras story with an arrival at Thunder Bluff.

</div>
