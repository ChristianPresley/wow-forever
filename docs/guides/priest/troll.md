---
tags:
  - Priest
  - Troll
  - Horde
---

# Troll Priest

<div class="guide-head" data-class="priest" markdown>

:codex-priest:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Add-on</span> **:codex-horde:{ .fc-sigil aria-hidden="true" } Horde**{ .badge .faction } **Healer**{ .badge .heal } **DPS**{ .badge .dps }

<p class="gh-note" markdown>Read with the [Priest guide](index.md).</p>

</div>

## Why this combo

Troll Priest is a Classic combination and **not new**. Its Priest spells, **Hex of Weakness** and **Shadowguard**, did not change, and Warcraft Tavern rates them as weak. The strength of the combination comes from the race. **Berserking** gives +10% cast speed when you want it. The new **Rapid Regeneration** heals half your health over 6 s out of combat. This decreases downtime much when you level.

**Best for:** Horde raid healers and Shadow DPS who want a haste cooldown, and players who want short downtime when they level.

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Berserking** <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **5/5**{ .stars .s5 }</p>
<p markdown><span class="ability-label">PvE</span> **+10% cast speed for 15 s.** More Greater Heals in an emergency, or more Mind Flay ticks and Mind Blasts in a burn phase</p>
<p markdown><span class="ability-label">PvP</span> Burst</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Rapid Regeneration** *(new)* <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 } leveling</p>
<p markdown><span class="ability-label">PvE</span> Gives back **50% of max health over 6 s**. Each action stops it. Use it after a fight, not food</p>
<p markdown><span class="ability-label">PvP</span> Only to fill your health out of combat</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Beast Slaying** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 } leveling</p>
<p markdown><span class="ability-label">PvE</span> More damage against Beasts (this wiki does not give the value). Many leveling quests have Beasts as targets</p>
<p markdown><span class="ability-label">PvP</span> Druid forms are not Beasts (*Classic-era*)</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Regeneration** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **2/5**{ .stars .s2 }</p>
<p markdown><span class="ability-label">PvE</span> +20% health regen, part of it in combat</p>
<p markdown><span class="ability-label">PvP</span> Small</p>
</div>

</div>

**Priest spells unique to Trolls**

| Spell | Level | Effect (Classic-era) | Use |
|---|---|---|---|
| **Hex of Weakness** | (Classic spell) | Decreases the damage of the target and the healing that it gets | PvP against melee. Of little use in PvE |
| **Shadowguard** | (Classic spell) | A self-buff with charges. Each hit on you causes Shadow damage to the attacker | A little more damage when you level, especially when mobs get to you |

Blizzard lists both spells as unchanged from Classic, without levels. They probably come at the race-spell levels of 10 and 20.

??? example "Macros"

    Berserking with a large heal:

    ```
    #showtooltip Greater Heal
    /cast Berserking
    /cast [@mouseover,help,nodead][help][@player] Greater Heal
    ```

    Rapid Regeneration after a fight (an action stops it. Do not push the button again and again):

    ```
    #showtooltip Rapid Regeneration
    /cast [nocombat] Rapid Regeneration
    ```

    !!! note
        It is not documented if you can cast Rapid Regeneration in combat. The `[nocombat]` condition prevents a wasted cast.

## Starting zone walkthrough (1–~12)

Trolls and Orcs start in the **Valley of Trials**, Durotar. Blizzard says that the Valley of Trials got **new NPCs, quests, profession hooks and "small moments"**. The quest names below are Classic-era and can be different.

<div class="steps" markdown>

1.  **1–2**{ .lvl } Get *Your Place in the World* and the first quests from the den. Kill boars and scorpids. The Priest trainer is in the **Den** (Classic: Ken'jai).
2.  **2–5**{ .lvl } Do the quilboar quest *Sarkoth*, *Vile Familiars* and the cactus apples. At 4, train **Shadow Word: Pain**.
3.  **5**{ .lvl } Get **The Great Outdoors** and learn Cooking. Kill **Yarrog Baneshadow** in the cave for the Burning Blade medallion.
4.  **6**{ .lvl } Train **Power Word: Shield**. Go to **Sen'jin Village**, the Darkspear home on the coast.
5.  **6–10**{ .lvl } Do the quests at Sen'jin and **Razor Hill**: the Echo Isles, Thunder Ridge, the Skull Rock Burning Blade, and Tiragarde Keep. Sen'jin has early class trainers (Classic-era).
6.  **10**{ .lvl } Learn your first race spell and first talent. Get the class quest. Full training is in **Orgrimmar**, in the **Valley of Spirits**.
7.  **10–12**{ .lvl } Complete Durotar. Then go west into **the Barrens** at the Crossroads.

</div>

## Route to 60 from Orgrimmar

<div class="steps" markdown>

1.  **10–20**{ .lvl } The Barrens

    <span class="step-label">Hub / flight path</span> The Crossroads. Durotar Supply and Logistics camp to the west

2.  **13–19**{ .lvl } Ragefire Chasm (Orgrimmar)

    <span class="step-label">Hub / flight path</span> —

3.  **15–25**{ .lvl } Stonetalon Mountains, Silverpine Forest (through the Undercity zeppelin), Wailing Caverns

    <span class="step-label">Hub / flight path</span> Sun Rock Retreat, the Sepulcher

4.  **15–22**{ .lvl } [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) (Tirisfal)

    <span class="step-label">Hub / flight path</span> —

5.  **20–30**{ .lvl } Ashenvale, Hillsbrad Foothills, Thousand Needles

    <span class="step-label">Hub / flight path</span> Splintertree Post, Tarren Mill, Freewind Post

6.  **30–40**{ .lvl } Desolace, Stranglethorn Vale, Arathi Highlands, Dustwallow

    <span class="step-label">Hub / flight path</span> Shadowprey Village, Grom'gol, Hammerfall, Brackenwall

7.  **35–45**{ .lvl } **Riverglades** (through the Swamp of Sorrows or Badlands)

    <span class="step-label">Hub / flight path</span> **Rog'mar** (flights to Stonard, Hammerfall, Kargath, Flame Crest)

8.  **40–50**{ .lvl } Tanaris, Feralas, Hinterlands, Badlands, Azshara (45+), Felwood

    <span class="step-label">Hub / flight path</span> Gadgetzan, Camp Mojache, Revantusk Village

9.  **50–60**{ .lvl } Un'Goro, Burning Steppes, Plaguelands, Winterspring, Silithus

    <span class="step-label">Hub / flight path</span> Flame Crest, the Bulwark, Everlook

10.  **60**{ .lvl } Mount Hyjal (from Winterspring)

    <span class="step-label">Hub / flight path</span> Tainted Foothills

</div>

- **Class trainers:** Valley of Spirits, Orgrimmar.
- In Dalaran, Horde players are **attacked on sight**, and they cannot get Kirin Tor reputation. Thus do not go to the quest hubs in the City of Dalaran.
- The new [Drowned City](../../content/dungeons/drowned-city.md) in Stranglethorn and Zul'Farrak, which has a troll theme, are on your route.

## Faction-specific notes

- **Mount:** raptors at 40 (100g). Honored with **Darkspear Trolls** gives 10% off.
- **Reputation:** Darkspear Trolls is your home faction. The new **Darkspear Raiders** battleground faction ([Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands)) is a different faction. Its Exalted rewards include a tabard and a Legacy Point.
- **Lore:** Darkspear priests honor the loa, and also the Light and shadow. The Echo Isles and Sen'jin are the home of your people.
- **PvP vendor:** Hall of Legends, Orgrimmar.

## Verdict

<div class="verdict" markdown>

**The Horde choice for raid healers and Shadow.** Berserking is the best throughput racial that a Priest can get. Rapid Regeneration makes leveling easier. The Troll Priest spells are weak. Thus you select the race for its racials, not for its Priest kit. For Will of the Forsaken in PvP, select Undead.

</div>
