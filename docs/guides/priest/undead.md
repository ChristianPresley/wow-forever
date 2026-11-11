---
tags:
  - Priest
  - Undead
  - Horde
---

# Undead Priest

<div class="guide-head" data-class="priest" markdown>

:codex-priest:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Add-on</span> **:codex-horde:{ .fc-sigil aria-hidden="true" } Horde**{ .badge .faction } **Healer**{ .badge .heal } **DPS**{ .badge .dps }

<p class="gh-note" markdown>Read with the [Priest progression](index.md).</p>

</div>

## Why this combo

Undead Priest is a Classic combination and **not new**. It is the classic Horde PvP Priest: **Will of the Forsaken** breaks fears, charms and sleeps. Forever adds **Touch of the Grave**, a passive health drain, and **Dark Sacrifice**, a new Priest spell that changes your health into mana. Warcraft Tavern calls Undead strong, mostly because of Touch of the Grave. It rates Touch of Weakness as weak.

**Best for:** Shadow Priests, PvP in all specs, and leveling (with Cannibalize and Dark Sacrifice, you drink less).

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Will of the Forsaken** <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **5/5**{ .stars .s5 } PvP / **3/5**{ .stars .s3 } PvE</p>
<p markdown><span class="ability-label">PvE</span> Breaks fear, charm and sleep. Useful against mobs and bosses that fear, but every Priest has Fear Ward now</p>
<p markdown><span class="ability-label">PvP</span> One of the best PvP racials. It stops Warlock Fear, Priest Scream and Warrior Intimidating Shout</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Cannibalize** <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 } leveling</p>
<p markdown><span class="ability-label">PvE</span> Eat humanoid or undead corpses to get health back out of combat</p>
<p markdown><span class="ability-label">PvP</span> —</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Underwater Breathing** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **1/5**{ .stars .s1 }</p>
<p markdown><span class="ability-label">PvE</span> Longer breath underwater</p>
<p markdown><span class="ability-label">PvP</span> —</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Touch of the Grave** *(new)* <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 }</p>
<p markdown><span class="ability-label">PvE</span> A chance on hit to drain **5% of max health** (15 s internal cooldown). Free sustain and damage</p>
<p markdown><span class="ability-label">PvP</span> Same</p>
</div>

</div>

**Priest spells unique to Undead**

| Spell | Level | Effect | Use |
|---|---|---|---|
| **Touch of Weakness** | (Classic spell) | Classic-era: a self-buff that causes Shadow damage to the next melee attacker and makes it weaker | Small effect. Better when you level than in raids |
| **Dark Sacrifice** *(new)* | 20 | Changes your own health into mana over time. The mana increases with **Spirit** | Use it with Cannibalize or a Renew on yourself, so that you can continue without drinking. In raids, a mana cooldown when a healer can fill your health |

??? example "Macros"

    Will of the Forsaken, then shield yourself:

    ```
    #showtooltip Will of the Forsaken
    /cast Will of the Forsaken
    /cast [@player] Power Word: Shield
    ```

    Dark Sacrifice with a Renew on yourself to replace the lost health:

    ```
    #showtooltip Dark Sacrifice
    /cast Dark Sacrifice
    /cast [@player] Renew
    ```

    !!! note
        It is not documented how much health Dark Sacrifice costs, or if actions interrupt it. Test it on mobs with a low risk first.

## Starting zone walkthrough (1–~12)

The Undead start in **Deathknell**, Tirisfal Glades. Tirisfal got the largest starting-zone change of the Horde. **Shadowvale** and **Bandarion Keep** in the Whispering Wood now fill the empty west area. This area is the home of the new Forsaken Paladin journey. The quest names below are Classic-era and can be different.

<div class="steps" markdown>

1.  **1–2**{ .lvl } Rise from the crypt and get the first quests in Deathknell (*Rude Awakening* in Classic). Kill mindless zombies and wretched ghouls. The Priest trainer is in the **chapel of Deathknell** (Classic: Dark Cleric Duesten).
2.  **2–5**{ .lvl } Do *Rattling the Rattlecages*, the Night Web's Hollow spiders, the Scarlet convert camp and *Marla's Last Wish*. At 4, train **Shadow Word: Pain**.
3.  **5**{ .lvl } Get **The Great Outdoors** and learn Cooking. The new content in Tirisfal includes profession hooks.
4.  **6**{ .lvl } Train **Power Word: Shield**. Kill *Samuel Fipps* and go east to **Brill**.
5.  **6–10**{ .lvl } Do the quests of Brill: Agamand Mills, Garren's Haunt, the Scarlet Crusade, the murlocs of Brightwater Lake, and Cold Hearth Manor. Brill has early class trainers (Classic-era). Explore the new **Shadowvale** content in the west.
6.  **10**{ .lvl } Get your first talent and the class quest. Full training is in the **Undercity**.
7.  **10–12**{ .lvl } Complete Tirisfal. Then go south into **Silverpine Forest**.

</div>

## Route to 60 from the Undercity

<div class="steps" markdown>

1.  **10–20**{ .lvl } Silverpine Forest (reportedly the Greymane Wall is rebuilt, and you can see Gilneas: *unconfirmed*)

    <span class="step-label">Hub / flight path</span> The Sepulcher

2.  **15–22**{ .lvl } **[Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md)** (Tirisfal)

    <span class="step-label">Hub / flight path</span> —

3.  **15–25**{ .lvl } The Barrens through the zeppelin. Shadowfang Keep (Silverpine)

    <span class="step-label">Hub / flight path</span> The Crossroads

4.  **20–30**{ .lvl } Hillsbrad Foothills, Ashenvale, Stonetalon

    <span class="step-label">Hub / flight path</span> Tarren Mill, Splintertree Post

5.  **30–40**{ .lvl } Arathi Highlands, Stranglethorn Vale, Desolace, Thousand Needles, Scarlet Monastery

    <span class="step-label">Hub / flight path</span> Hammerfall, Grom'gol, Shadowprey Village

6.  **35–45**{ .lvl } **Riverglades**

    <span class="step-label">Hub / flight path</span> **Rog'mar**

7.  **40–50**{ .lvl } Badlands, Swamp of Sorrows, Hinterlands, Tanaris, Feralas, Dustwallow

    <span class="step-label">Hub / flight path</span> Kargath, Stonard, Revantusk Village, Gadgetzan

8.  **50–60**{ .lvl } Western and Eastern Plaguelands, Burning Steppes, Un'Goro, Azshara, Winterspring, Silithus

    <span class="step-label">Hub / flight path</span> The Bulwark, Light's Hope, Flame Crest, Everlook

9.  **60**{ .lvl } Mount Hyjal (from Winterspring)

    <span class="step-label">Hub / flight path</span> Tainted Foothills

</div>

- **Class trainers:** the Undercity.
- **Zeppelins:** Undercity ↔ Orgrimmar and Undercity ↔ Grom'gol (Stranglethorn).
- **Dalaran:** Horde players are attacked on sight. Thus do not go there. The other quests in the Alterac Mountains are still good.
- Scarlet Monastery is near your home. Shackle Undead is useful in its undead wings.

## Faction-specific notes

- **Mount:** skeletal horses at 40 (100g). Honored with **Undercity** gives 10% off.
- **Reputation:** Undercity is your home faction.
- **Forsaken Paladins:** Forever adds Undead Paladins with their own journey at Bandarion Keep. Undead Priests do not share it, but you will see their story in Tirisfal.
- **Lore:** Most Forsaken priests turned from the Light to the shadow. Shadow is the spec that fits the theme, but Holy and Discipline Forsaken priests also exist.
- **World PvP:** In beta, raids on the Undercity occurred frequently. On PvP rulesets, expect Alliance raids near Brill and the city.

## Verdict

<div class="verdict" markdown>

**The best Horde PvP Priest and a strong Shadow choice.** Will of the Forsaken stops the most dangerous CC in the game. Touch of the Grave adds free sustain. Dark Sacrifice and Cannibalize decrease the time that you drink when you level. Troll has the better PvE throughput cooldown (Berserking). Undead is better in all situations where fear is a threat.

</div>
