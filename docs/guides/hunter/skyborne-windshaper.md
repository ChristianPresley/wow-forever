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
    Skyborne require the **Skyborne Heroic Pack** or a higher edition. See [Editions](../../about/editions.md).

## Why this combo

**NEW in Forever.** The Horde's [Skyborne](../../characters/races.md#skyborne), the **Windshapers**, can be Hunters (with Druid, Rogue, Shaman and Warrior). They're the shamanic, kaldorei-descended half of the race, allied with the Earthen Ring.

Compared with the Alliance High Order, Windshapers swap **Read Ley Line** (regen) for **Skysight** (movement speed). For a Hunter that means:

- **Wind Blessed** gives passive **haste**, which speeds Auto Shot, casts and the global cooldown.
- **Skysight** gives +15% speed for 15 s (+30% while *Charged*): kiting and travel.
- **Walk on Air** gives a 10 s glide to escape or shortcut.
- They land at **Skywatcher Plateau**, just outside Thunder Bluff, which puts you on the Tauren's Kalimdor route.

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Walk on Air** <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 }</p>
<p markdown><span class="ability-label">PvE</span> 10 s glide. Shortcut down cliffs (Thousand Needles, Feralas, Un'Goro) and a Hardcore escape</p>
<p markdown><span class="ability-label">PvP</span> Break line of sight off a ledge</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Skysight** <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 } PvP</p>
<p markdown><span class="ability-label">PvE</span> +15% speed for 15 s; at an elemental convergence you get *Charged* for 1 hr, raising it to +30%. Travel before your mount</p>
<p markdown><span class="ability-label">PvP</span> Kite melee out of the deadzone; carry or chase flags</p>
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
    - The 5 November hotfix note groups Plainsrunning with Skyborne. Plainsrunning is a Tauren racial; it's unclear whether any Skyborne speed racial was changed too.

??? example "Macros"

    ```text
    #showtooltip Skysight
    /cast Skysight
    /cast Concussive Shot
    ```

    Speed up and snare at the same time when a melee closes in.

    ```text
    #showtooltip Walk on Air
    /petfollow
    /cast Walk on Air
    ```

## Starting zone walkthrough 1–12

All Skyborne start in **Thendal Village** on [Zephras Isle](../../world/zephras-isle.md), a sanctuary zone where both factions quest side by side, phased apart. The isle takes you to about level 12–14. Trainers are in Thendal Village and **Valanaar**.

<div class="steps" markdown>

1.  **1–5**{ .lvl } Thendal Village

    - *Coming of Age*, *Harmony in Balance*, *The Cirrusfly Queen*, *Harvesting Windstones* (a gathering-profession voucher: Skinning), *Falling With Style* and *The Anchors of Zephras*. The Ursera bear chain ends with Urs'anah.
    - Faction opener: **The Gift of Skysight** (Windshaper), which introduces your racial.
    - Train Serpent Sting at 4.

2.  **5–9**{ .lvl } The road to Shen'dar Village

    - Al'Aketh thugs under Malduko Cloudcrash; *Blessing of Zephras* tornadoes (+40% speed).
    - Raan Wildwind's **The Great Outdoors** unlocks [camping](../../systems/camping.md).
    - **Shen'dar Village**: bandits, hippogryphs, Prideclaws, "Badwind" Bennic and *WANTED: Vulgara the Insatiable*. The two factions skirmish at the Windsong Standing Stones.
    - Train Arcane Shot, Hunter's Mark and Concussive Shot.

3.  **10**{ .lvl } The first pet

    - *Taming the Beast* (Wowhead quest 94978): use a Taming Rod on a **Windsong Crawler**, a crab near water. Warcraft Tavern lists the final Skyborne quest under the same name (94013).
    - Completing the chain teaches Tame Beast, Feed Pet and Revive Pet.
    - Players report **foxes** on the island (*unconfirmed*). The Fox is a new family with *Trickster's Dance*.
    - First talent: **Deadly Aspects**.

4.  **9–12+**{ .lvl } Falaath, Valanaar and the finale

    - *Secret Agent Elf*: infiltrate **Falaath Village**; defeat Commanders Cyclas and Aanders; recover the Shadowsong Family Signet.
    - **Valanaar:** give the signet to Talaanis Shadowsong and meet **Grand Skyseer Ayessa Dawnsinger** (*The Grand Skyseer*). Hearth here.
    - **Gustberry Lowlands:** the Windshaper chain *The Broken Construct* and the Windfield Orchard chain. `/sing` at the frogs for the *Musical Gustjumper* pet.
    - **Shadowgale Forest:** *In Service of Zephras* → *Blood for Blood*; Nightclaw reputation via *Mercy Falls on Deaf Ears*; recording crystals in Nightclaw Cavern.
    - **Finale:** East Pylon Watchtower, *Desperate Times*, the Shrine of Akir, *Confront Lorthuna*, Rohash, then *The Fate of Zephras* and *What Comes Next*.

</div>

## Route to 60 from Valanaar

**Class trainer city:** Valanaar; once you leave, Thunder Bluff (Hunter Rise) is closest.

The **west Skydock airship** goes to **Skywatcher Plateau** in northwest Mulgore, reportedly every 5 minutes.

<div class="steps" markdown>

1.  **12–20**{ .lvl } Mulgore leftovers, then the Barrens (Crossroads; **Durotar Supply and Logistics** crate camp)

    <span class="step-label">Travel</span> Thunder Bluff wind rider

2.  **15–25**{ .lvl } Wailing Caverns, Silverpine, [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md)

    <span class="step-label">Travel</span> Orgrimmar–Undercity zeppelin

3.  **18–30**{ .lvl } Stonetalon (Sun Rock), Ashenvale, Hillsbrad (Tarren Mill), Thousand Needles

    <span class="step-label">Travel</span> Sun Rock

4.  **30–40**{ .lvl } Desolace (path from Skywatcher Plateau), Arathi, Stranglethorn, Dustwallow

    <span class="step-label">Travel</span> Shadowprey Village

5.  **35–45**{ .lvl } **[Riverglades](../../world/zones.md#riverglades)** (Rog'mar), or Shen'dralas, the home of the Skyborne's Shen'dralar ancestors (level range unknown)

    <span class="step-label">Travel</span> Steamwheedle ferry

6.  **40–50**{ .lvl } Feralas, Tanaris, Badlands, Swamp of Sorrows, Hinterlands

    <span class="step-label">Travel</span> Camp Mojache

7.  **50–60**{ .lvl } Un'Goro, Silithus (Elemental Insight), Azshara, Felwood, Winterspring, Plaguelands

    <span class="step-label">Travel</span> Everlook

8.  **60**{ .lvl } [Mount Hyjal](../../world/zones.md#mount-hyjal)

    <span class="step-label">Travel</span> Darkwhisper Gorge

</div>

!!! warning "Dalaran is hostile"
    The High Order's Dalaran isn't yours. Horde players are attacked on sight in Dalaran and can't earn Kirin Tor reputation, so skip the [City of Dalaran](../../content/dungeons/city-of-dalaran.md) quest hub.

## Faction-specific notes

- **Reputation:** **Windshapers**. Cloth turn-ins in **Mulgore** count. Exalted lets other Horde races buy Galestriders.
- **Earthen Ring:** the Windshapers' ally, represented by Muln Earthfury in Mulgore.
- **Mount:** **Galestrider** from Fairweather Stables (53.8, 81.3) on Zephras, Umber, Stormy or Empyrean, with a 5–20% reputation discount.
- **Language:** Darnassian and Orcish; you can speak Darnassian with Alliance Skyborne.
- **Library books:** Owen Thadd, Undercity.
- **PvP:** Darkspear Raiders reputation; Hall of Legends in Orgrimmar. Horde character creation on PvP rulesets was locked for population balance at launch.

## Verdict

<div class="verdict" markdown>

A fast, mobile Horde Hunter. Passive haste trades Troll's on-demand burst for steady uptime, and Skysight plus Walk on Air give the best mobility of any Horde Hunter. You give up Orc's pet damage and Tauren's sturdiness. Pick Windshaper if you own the pack and want the Zephras story with a Thunder Bluff landing.

</div>
