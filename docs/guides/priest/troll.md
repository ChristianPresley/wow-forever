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

Troll Priest is a Classic combination and **not new**. Its Priest spells, **Hex of Weakness** and **Shadowguard**, are unchanged and rated weak by Warcraft Tavern. The race itself carries the combo: **Berserking** is +10% cast speed on demand, and the new **Rapid Regeneration** heals half your health over 6 s out of combat, which cuts downtime a lot while leveling.

**Best for:** Horde raid healers and Shadow DPS who want a haste cooldown, and players who want fast leveling downtime.

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Berserking** <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **5/5**{ .stars .s5 }</p>
<p markdown><span class="ability-label">PvE</span> **+10% cast speed for 15 s.** More Greater Heals in a crisis, or more Mind Flay ticks and Mind Blasts in a burn</p>
<p markdown><span class="ability-label">PvP</span> Burst</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Rapid Regeneration** *(new)* <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 } leveling</p>
<p markdown><span class="ability-label">PvE</span> Regenerates **50% of max health over 6 s**; any action cancels it. Use it instead of eating after a fight</p>
<p markdown><span class="ability-label">PvP</span> Only to top up out of combat</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Beast Slaying** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 } leveling</p>
<p markdown><span class="ability-label">PvE</span> Extra damage against Beasts (value not given on this wiki). Many leveling quests are beasts</p>
<p markdown><span class="ability-label">PvP</span> Druid forms aren't Beasts (*Classic-era*)</p>
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
| **Hex of Weakness** | (Classic spell) | Weakens the target's damage and the healing it receives | PvP against melee; marginal in PvE |
| **Shadowguard** | (Classic spell) | A self-buff that deals Shadow damage to attackers with each hit, using charges | A little extra damage while leveling, especially when mobs reach you |

Blizzard lists both as unchanged from Classic, without levels. Expect them at the race-spell levels of 10 and 20.

??? example "Macros"

    Berserking with a big heal:

    ```
    #showtooltip Greater Heal
    /cast Berserking
    /cast [@mouseover,help,nodead][help][@player] Greater Heal
    ```

    Rapid Regeneration after a fight (it cancels if you act, so don't spam):

    ```
    #showtooltip Rapid Regeneration
    /cast [nocombat] Rapid Regeneration
    ```

    !!! note
        It isn't documented whether Rapid Regeneration can be cast in combat. The `[nocombat]` guard stops you wasting it.

## Starting zone walkthrough (1–~12)

Trolls start in the **Valley of Trials**, Durotar, with Orcs. Blizzard says the Valley of Trials got **new NPCs, quests, profession hooks and "small moments"**. Quest names below are Classic-era and may differ.

<div class="steps" markdown>

1.  **1–2**{ .lvl } take *Your Place in the World* and the opening quests from the den. Kill boars and scorpids. The Priest trainer is in the **Den** (Classic: Ken'jai).
2.  **2–5**{ .lvl } the quilboar *Sarkoth*, *Vile Familiars* and the cactus apples. Train **Shadow Word: Pain** at 4.
3.  **5**{ .lvl } take **The Great Outdoors** and learn Cooking. Kill **Yarrog Baneshadow** in the cave for the Burning Blade medallion.
4.  **6**{ .lvl } **Power Word: Shield**. Head toward **Sen'jin Village**, the Darkspear home on the coast.
5.  **6–10**{ .lvl } Sen'jin and **Razor Hill**: the Echo Isles, Thunder Ridge, the Skull Rock Burning Blade, and Tiragarde Keep. Sen'jin has early class trainers (Classic-era).
6.  **10**{ .lvl } learn your first race spell and first talent, and take the class quest. Full training is in **Orgrimmar** in the **Valley of Spirits**.
7.  **10–12**{ .lvl } finish Durotar, then cross west into **the Barrens** at the Crossroads.

</div>

## Route to 60 from Orgrimmar

<div class="steps" markdown>

1.  **10–20**{ .lvl } The Barrens

    <span class="step-label">Hub / flight path</span> The Crossroads; Durotar Supply and Logistics camp to the west

2.  **13–19**{ .lvl } Ragefire Chasm (Orgrimmar)

    <span class="step-label">Hub / flight path</span> —

3.  **15–25**{ .lvl } Stonetalon Mountains, Silverpine Forest (via the Undercity zeppelin), Wailing Caverns

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
- Horde players are **attacked on sight in Dalaran** and can't earn Kirin Tor reputation, so skip the City of Dalaran quest hubs.
- Stranglethorn's new [Drowned City](../../content/dungeons/drowned-city.md) and the troll-themed Zul'Farrak are on your route.

## Faction-specific notes

- **Mount:** raptors at 40 (100g). Honored with **Darkspear Trolls** gives 10% off.
- **Reputation:** Darkspear Trolls is your home faction. The new **Darkspear Raiders** battleground faction ([Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands)) is separate. Its Exalted rewards include a tabard and a Legacy Point.
- **Lore:** Darkspear priests honor the loa as well as the Light and shadow; the Echo Isles and Sen'jin are your people's home.
- **PvP vendor:** Hall of Legends, Orgrimmar.

## Verdict

<div class="verdict" markdown>

**The Horde raid-healer and Shadow pick.** Berserking is the best throughput racial a Priest can get, and Rapid Regeneration makes leveling smoother. The Troll Priest spells are weak, so you're choosing the race for its racials, not its Priest kit. Pick Undead instead for Will of the Forsaken in PvP.

</div>
