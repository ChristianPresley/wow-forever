---
tags:
  - Hunter
  - Skyborne
  - Alliance
---

# Skyborne (High Order) Hunter

<div class="guide-head" data-class="hunter" markdown>

:codex-hunter:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Add-on</span> **:codex-alliance:{ .fc-sigil aria-hidden="true" } Alliance**{ .badge .faction } **DPS**{ .badge .dps }

<p class="gh-note" markdown>Read with the [Hunter guide](index.md).</p>

</div>

!!! warning "Paid race"
    Skyborne need the **Skyborne Heroic Pack** or a higher edition. Refer to [Editions](../../about/editions.md).

## Why this combo

**NEW in Forever.** The [Skyborne](../../characters/races.md#skyborne) are an elven race that is only in Forever. The **High Order** of the Alliance can be Hunters (and also Druid, Mage, Rogue and Warrior). An example is the Rangers of Thendal Grove, one of the militias of Zephras Isle.

What they give:

- **Wind Blessed** gives passive **haste**. Haste is a new stat in Forever. It makes Auto Shot, casts and the global cooldown faster.
- **Read Ley Line** is a mana tool. Mana is the weakness of the Hunter in long fights.
- **Walk on Air** is a 10 s controlled glide. It is an escape, and a short path down from cliffs.
- They start on **Zephras Isle**, the new floating starting zone of Forever. They leave by airship to **Dalaran**.

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Walk on Air** <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 }</p>
<p markdown><span class="ability-label">PvE</span> 10 s glide. Go down from ledges with no long path. Safe fall. Very good for Hardcore</p>
<p markdown><span class="ability-label">PvP</span> Jump off a ledge to break line of sight and get range again</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Read Ley Line** <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 }</p>
<p markdown><span class="ability-label">PvE</span> +50% health and mana regen for 15 s. At a Ley Line, it gives *Attuned* for 1 hr, which increases the bonus to +100%. You stop to drink less often</p>
<p markdown><span class="ability-label">PvP</span> A small quantity of mana between fights</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Wind Blessed** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 }</p>
<p markdown><span class="ability-label">PvE</span> Passive haste: more Auto Shots, faster Aimed and Sniper Shot casts</p>
<p markdown><span class="ability-label">PvP</span> Faster casts on Aimed Shot</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Elemental Insight** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **2/5**{ .stars .s2 }</p>
<p markdown><span class="ability-label">PvE</span> +5% damage to Elementals. Good in Zephras, Silithus, Un'Goro, [Shaper's Terrace](../../content/dungeons/shapers-terrace.md)</p>
<p markdown><span class="ability-label">PvP</span> Nothing</p>
</div>

</div>

!!! conflict "Conflicts"
    - **Wind Blessed:** sources give 1%, 2% or 3% haste. The latest official notes say **2%**.
    - **Walk on Air** cooldown: 1.5 or 2 minutes.
    - You cannot use Read Ley Line with Innervate.

??? example "Macros"

    ```text
    #showtooltip Read Ley Line
    /cast Read Ley Line
    /sit
    ```

    Use this macro after combat. Regen ticks while you sit and eat.

    ```text
    #showtooltip Walk on Air
    /petfollow
    /cast Walk on Air
    ```

    Use this macro at the edge of a cliff: it calls the pet back, and you glide away. (In Forever, Disengage removes threat. It is not a leap.)

## Starting zone walkthrough 1–12

All Skyborne start in **Thendal Village** on [Zephras Isle](../../world/zephras-isle.md). It is a sanctuary zone where both factions do quests in the same area, but in different phases. The isle gives quests to about level 12–14. Trainers are in Thendal Village and in the capital, **Valanaar**.

<div class="steps" markdown>

1.  **1–5**{ .lvl } Thendal Village

    - *Coming of Age*, *Harmony in Balance*, *The Cirrusfly Queen*, *Harvesting Windstones* (a gathering-profession voucher: take Skinning), *Falling With Style* and *The Anchors of Zephras*.
    - The **Ursera** bear chain ends with Urs'anah.
    - Faction opener: **Reading the Leylines** (High Order). This quest gives you Read Ley Line.
    - At 4, train Serpent Sting.

2.  **5–9**{ .lvl } The road to Shen'dar Village

    - Fight Al'Aketh thugs under Malduko Cloudcrash. Ride the tornadoes for *Blessing of Zephras* (+40% speed).
    - Raan Wildwind gives **The Great Outdoors**. Unlock [camping](../../systems/camping.md) here.
    - **Shen'dar Village** (Constable Aonda): bandits, hippogryphs and Prideclaws, "Badwind" Bennic, and *WANTED: Vulgara the Insatiable* (make a group, or wait until 9–10).
    - Train Arcane Shot, Hunter's Mark and Concussive Shot.

3.  **10**{ .lvl } The first pet

    - The Skyborne taming quest is *Taming the Beast* (Wowhead quest 94978). In the Wowhead entry, you use a Taming Rod on a **Windsong Crawler**, a crab that lives near water. Warcraft Tavern gives the Skyborne final quest the same name, *Taming the Beast* (94013), not *Training the Beast*.
    - When you complete the chain, you learn Tame Beast, Feed Pet and Revive Pet.
    - Zephras has hippogryphs, prideclaws and other beasts. Players report **foxes** on the isle (*unconfirmed*). The Fox is a new family with *Trickster's Dance*.
    - First talent: **Deadly Aspects**.

4.  **9–12+**{ .lvl } Falaath, Valanaar and the finale

    - *Secret Agent Elf*: go secretly into **Falaath Village**. Defeat Commander Cyclas and Commander Aanders. Get the Shadowsong Family Signet back.
    - **Valanaar:** give the signet to Talaanis Shadowsong and meet **Supreme Magister Elaadrin Evengale**. Set your hearthstone and train.
    - **Gustberry Lowlands:** *The Missing Scholar* (Shriekling Den), the Windfield Orchard chain. `/sing` at the frogs for the *Musical Gustjumper* pet.
    - **Shadowgale Forest:** the High Order chain to Index Esoteria. Nightclaw reputation (repeatable *Mercy Falls on Deaf Ears*). Recording crystals in Nightclaw Cavern.
    - **Finale:** the Shrine of Akir, *Confront Lorthuna*, Rohash, then *The Fate of Zephras* and *What Comes Next*.

</div>

## Route to 60 from Valanaar

**Class trainer city:** Valanaar on Zephras Isle. After you leave, use Stormwind, Ironforge or Darnassus.

The **east Skydock airship** goes to north **[Dalaran](../../world/zones.md#dalaran)** in the Alterac Mountains, a 30–40 area. At level 12 you must walk south.

<div class="steps" markdown>

1.  **12–20**{ .lvl } Walk south from Dalaran through Hillsbrad to Southshore (be careful: the mobs in Hillsbrad are level 20+). Take the boat to **Menethil**, then go to Loch Modan. Or take the boat to **Auberdine** for Darkshore

    <span class="step-label">Travel</span> New Menethil–Southshore–Auberdine loop

2.  **15–25**{ .lvl } Westfall, Redridge (Three Corners crate camp)

    <span class="step-label">Travel</span> Stormwind Harbor ↔ Auberdine

3.  **20–30**{ .lvl } Wetlands ([Excavation Site](../../content/dungeons/excavation-site.md)), Duskwood, Ashenvale

    <span class="step-label">Travel</span> Menethil

4.  **26–35**{ .lvl } Hillsbrad, Dalaran (Kirin Tor chain, [City of Dalaran](../../content/dungeons/city-of-dalaran.md))

    <span class="step-label">Travel</span> Back where you arrived

5.  **30–40**{ .lvl } Arathi, Stranglethorn, Desolace, Dustwallow

    <span class="step-label">Travel</span> Booty Bay, Theramore

6.  **35–45**{ .lvl } **[Riverglades](../../world/zones.md#riverglades)** (Farholde Keep)

    <span class="step-label">Travel</span> Farholde FP

7.  **40–50**{ .lvl } Badlands, Tanaris, Feralas, Hinterlands, Swamp of Sorrows

    <span class="step-label">Travel</span> Steamwheedle ferry

8.  **50–60**{ .lvl } Azshara, Un'Goro (Elemental Insight), Felwood, Plaguelands, Winterspring, Silithus

    <span class="step-label">Travel</span> Everlook

9.  **60**{ .lvl } [Mount Hyjal](../../world/zones.md#mount-hyjal)

    <span class="step-label">Travel</span> Darkwhisper Gorge

</div>

!!! tip "Leaving early"
    Skyborne can leave Zephras at any level. But the ~145 quests on the island are the fastest route to 12. All players can come back by airship.

## Faction-specific notes

- **Reputation:** **High Order**. At Exalted, other races can buy Galestriders. Cloth turn-ins in **Dalaran** count.
- **Kirin Tor:** the High Order is an ally of the Kirin Tor. Alliance players can get Kirin Tor reputation. Horde players cannot.
- **Mount:** **Galestrider** from Fairweather Stables (53.8, 81.3) on Zephras, in Umber, Stormy or Empyrean. High Order reputation gives a 5/10/15/20% discount.
- **Customization:** only HD models at launch. Feathers, tattoos, sky-blue skin.
- **Language:** Darnassian and Common. You can speak to Windshaper Skyborne of the other faction in Darnassian.
- **Library books:** Garion Wendell, Stormwind.

## Verdict

<div class="verdict" markdown>

A strong, comfortable Alliance Hunter. Haste and Read Ley Line make both damage and mana more stable. Walk on Air is a very good Hardcore tool. Night Elf still has the biggest burst, and Human has the best PvP button. Select High Order if you have the pack and want the Zephras story with an arrival in Dalaran.

</div>
