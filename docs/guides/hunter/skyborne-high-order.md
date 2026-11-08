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
    Skyborne require the **Skyborne Heroic Pack** or a higher edition. See [Editions](../../about/editions.md).

## Why this combo

**NEW in Forever.** The [Skyborne](../../characters/races.md#skyborne) are a Forever-only elven race, and the Alliance's **High Order** can be Hunters (along with Druid, Mage, Rogue and Warrior). Think of the Rangers of Thendal Grove, one of Zephras Isle's militias.

What they bring:

- **Wind Blessed** gives passive **haste**, a new stat in Forever that speeds up Auto Shot, casts and the global cooldown.
- **Read Ley Line** is a mana tool, and mana is the Hunter's long-fight weakness.
- **Walk on Air** is a 10 s controlled glide: an escape and a shortcut off cliffs.
- They start on **Zephras Isle**, Forever's new floating starting zone, and leave by airship to **Dalaran**.

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Walk on Air** <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 }</p>
<p markdown><span class="ability-label">PvE</span> 10 s glide. Skip long paths down from ledges; safe fall. Great for Hardcore</p>
<p markdown><span class="ability-label">PvP</span> Jump off a ledge to break line of sight and reset range</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Read Ley Line** <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 }</p>
<p markdown><span class="ability-label">PvE</span> +50% health and mana regen for 15 s; at a Ley Line it grants *Attuned* for 1 hr, raising the bonus to +100%. Fewer drinking breaks</p>
<p markdown><span class="ability-label">PvP</span> Small mana top-up between fights</p>
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
    - Read Ley Line can't be used with Innervate.

??? example "Macros"

    ```text
    #showtooltip Read Ley Line
    /cast Read Ley Line
    /sit
    ```

    Use after combat; regen ticks while you sit and eat.

    ```text
    #showtooltip Walk on Air
    /petfollow
    /cast Walk on Air
    ```

    On a cliff edge: call the pet back and glide away. (Forever's Disengage drops threat; it isn't a leap.)

## Starting zone walkthrough 1–12

All Skyborne start in **Thendal Village** on [Zephras Isle](../../world/zephras-isle.md), a sanctuary zone where both factions quest side by side but phased apart. The isle runs to about level 12–14. Trainers are in Thendal Village and the capital **Valanaar**.

<div class="steps" markdown>

1.  **1–5**{ .lvl } Thendal Village

    - *Coming of Age*, *Harmony in Balance*, *The Cirrusfly Queen*, *Harvesting Windstones* (a gathering-profession voucher: take Skinning), *Falling With Style* and *The Anchors of Zephras*.
    - The **Ursera** bear chain ends with Urs'anah.
    - Faction opener: **Reading the Leylines** (High Order), which introduces Read Ley Line.
    - Train Serpent Sting at 4.

2.  **5–9**{ .lvl } The road to Shen'dar Village

    - Fight Al'Aketh thugs under Malduko Cloudcrash. Ride the tornadoes for *Blessing of Zephras* (+40% speed).
    - Raan Wildwind gives **The Great Outdoors**: unlock [camping](../../systems/camping.md) here.
    - **Shen'dar Village** (Constable Aonda): bandits, hippogryphs and Prideclaws, "Badwind" Bennic, and *WANTED: Vulgara the Insatiable* (group up or wait until 9–10).
    - Train Arcane Shot, Hunter's Mark and Concussive Shot.

3.  **10**{ .lvl } The first pet

    - The Skyborne taming quest is *Taming the Beast* (Wowhead quest 94978). Wowhead's entry has you use a Taming Rod on a **Windsong Crawler**, a crab found near water. Warcraft Tavern lists the Skyborne final quest under the same *Taming the Beast* name (94013) rather than *Training the Beast*.
    - Completing the chain teaches Tame Beast, Feed Pet and Revive Pet.
    - Zephras has hippogryphs, prideclaws and other beasts. Players report **foxes** on the isle (*unconfirmed*); the Fox is a new family with *Trickster's Dance*.
    - First talent: **Deadly Aspects**.

4.  **9–12+**{ .lvl } Falaath, Valanaar and the finale

    - *Secret Agent Elf*: infiltrate **Falaath Village**, defeat Commander Cyclas and Commander Aanders, recover the Shadowsong Family Signet.
    - **Valanaar:** hand the signet to Talaanis Shadowsong and meet **Supreme Magister Elaadrin Evengale**. Set your hearthstone and train.
    - **Gustberry Lowlands:** *The Missing Scholar* (Shriekling Den), the Windfield Orchard chain. `/sing` at the frogs for the *Musical Gustjumper* pet.
    - **Shadowgale Forest:** the High Order chain to Index Esoteria; Nightclaw reputation (repeatable *Mercy Falls on Deaf Ears*); recording crystals in Nightclaw Cavern.
    - **Finale:** the Shrine of Akir, *Confront Lorthuna*, Rohash, then *The Fate of Zephras* and *What Comes Next*.

</div>

## Route to 60 from Valanaar

**Class trainer city:** Valanaar on Zephras Isle; use Stormwind, Ironforge or Darnassus once you leave.

The **east Skydock airship** goes to north **[Dalaran](../../world/zones.md#dalaran)** in the Alterac Mountains, a 30–40 area. At level 12 you need to walk south.

<div class="steps" markdown>

1.  **12–20**{ .lvl } Walk from Dalaran south through Hillsbrad (be careful: Hillsbrad's level 20+ mobs) to Southshore, boat to **Menethil**, then Loch Modan, or boat to **Auberdine** for Darkshore

    <span class="step-label">Travel</span> New Menethil–Southshore–Auberdine loop

2.  **15–25**{ .lvl } Westfall, Redridge (Three Corners crate camp)

    <span class="step-label">Travel</span> Stormwind Harbor ↔ Auberdine

3.  **20–30**{ .lvl } Wetlands ([Excavation Site](../../content/dungeons/excavation-site.md)), Duskwood, Ashenvale

    <span class="step-label">Travel</span> Menethil

4.  **26–35**{ .lvl } Hillsbrad, Dalaran (Kirin Tor chain, [City of Dalaran](../../content/dungeons/city-of-dalaran.md))

    <span class="step-label">Travel</span> Back where you landed

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
    Skyborne can leave Zephras at any level, but the island's ~145 quests are the fastest route to 12. Anyone can come back by airship.

## Faction-specific notes

- **Reputation:** **High Order**. Exalted lets other races buy Galestriders. Cloth turn-ins in **Dalaran** count.
- **Kirin Tor:** the High Order is allied with the Kirin Tor; Alliance can earn Kirin Tor reputation, Horde can't.
- **Mount:** **Galestrider** from Fairweather Stables (53.8, 81.3) on Zephras, in Umber, Stormy or Empyrean. High Order reputation gives 5/10/15/20% off.
- **Customization:** HD models only at launch; feathers, tattoos, sky-blue skin.
- **Language:** Darnassian and Common. You can talk to Windshaper Skyborne in Darnassian across factions.
- **Library books:** Garion Wendell, Stormwind.

## Verdict

<div class="verdict" markdown>

A strong, comfortable Alliance Hunter. Haste and Read Ley Line smooth out both damage and mana, and Walk on Air is a great Hardcore tool. Night Elf still has the biggest burst and Human the best PvP button. Pick High Order if you own the pack and want the Zephras story with a Dalaran landing.

</div>
