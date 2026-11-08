---
tags:
  - Hunter
  - Troll
  - Horde
---

# Troll Hunter

<div class="guide-head" data-class="hunter" markdown>

:codex-hunter:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Add-on</span> **:codex-horde:{ .fc-sigil aria-hidden="true" } Horde**{ .badge .faction } **DPS**{ .badge .dps }

<p class="gh-note" markdown>Read with the [Hunter guide](index.md).</p>

</div>

## Why this combo

The Darkspear headhunter. Troll Hunters existed in Classic, but Forever removed Bow Specialization and Throwing Specialization and gave Trolls a new self-heal. What's left still suits the class:

- **Berserking**: +10% cast and attack speed for 15 s. More Auto Shots and faster Aimed Shots.
- **Beast Slaying**: bonus damage to Beasts, the most common leveling enemy.
- **Rapid Regeneration** *(new)*: 50% of your max health over 6 s, out of combat. Less eating.

Trolls are also the faction of the new **Darkspear Islands** battleground and the Darkspear Raiders reputation.

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Berserking** <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **5/5**{ .stars .s5 }</p>
<p markdown><span class="ability-label">PvE</span> +10% cast and attack speed for 15 s. Stack with Rapid Fire; also shortens Aimed Shot and Sniper Shot casts</p>
<p markdown><span class="ability-label">PvP</span> Faster Aimed Shot in a burst window</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Rapid Regeneration** *(new)* <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 }</p>
<p markdown><span class="ability-label">PvE</span> Heals 50% of max health over 6 s, but **any action cancels it**. Use between pulls instead of eating</p>
<p markdown><span class="ability-label">PvP</span> Between fights only</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Beast Slaying** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 } leveling</p>
<p markdown><span class="ability-label">PvE</span> Bonus damage to Beasts (+5% in Classic; Forever's value isn't published). Strong in questing, rarely matters in raids</p>
<p markdown><span class="ability-label">PvP</span> Hunter pets and Druid animal forms: unclear, *Classic-era rule says Druid forms aren't Beasts*</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Regeneration** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **2/5**{ .stars .s2 }</p>
<p markdown><span class="ability-label">PvE</span> +20% health regen, part of it continuing in combat</p>
<p markdown><span class="ability-label">PvP</span> Small sustain</p>
</div>

</div>

??? example "Macros"

    ```text
    #showtooltip Berserking
    /cast Berserking
    /cast Rapid Fire
    ```

    ```text
    #showtooltip Rapid Regeneration
    /petpassive
    /cast Rapid Regeneration
    ```

    Sets the pet to Passive so it doesn't start a fight and cancel your regen. Set it back to Defensive afterwards.

## Starting zone walkthrough 1–12

Trolls share the **Valley of Trials**, Durotar, with Orcs. Blizzard reworked the Valley with **new NPCs, quests, profession hooks and "small moments"**. The route below follows Classic where it still applies (*Classic-era*).

<div class="steps" markdown>

1.  **1–5**{ .lvl } Valley of Trials

    - Gornek's quests at the Den: mottled boars, scorpids, Sarkoth, Vile Familiars, cactus apples, lazy peons.
    - The **Hunter trainer is near the Den** (Jen'shan in Classic, *Classic-era*). Train **Serpent Sting** at 4.
    - Pick up the new Forever quests as you find them.

2.  **5–10**{ .lvl } Sen'jin Village and Razor Hill

    - **Sen'jin Village** is the Darkspear home: quests on the **Echo Isles** against Zalazane's trolls, plus Tiragarde Keep and the Razor Hill quests.
    - Take *The Great Outdoors* for [camping](../../systems/camping.md) and the starter gathering quest (Skinning).
    - Train Arcane Shot and Hunter's Mark (6), Concussive Shot (8).

3.  **10**{ .lvl } The first pet

    - Same chain as Orcs: in Classic, **Thotar** at Razor Hill sent you after a **Dire Mottled Boar**, a **Surf Crawler** and an **Armored Scorpid** (*Classic-era*). Forever quest *Taming the Beast* (Orc/Troll; Warcraft Tavern gives 6062), then *Training the Beast* (6081).
    - A boar for durability, a Durotar Tiger (cat) for damage. Beast Slaying makes your own beast-killing quests faster.
    - First talent: **Deadly Aspects**.

4.  **10–12**{ .lvl } To the Barrens

    - Finish Durotar, train in Orgrimmar, then head to the **Crossroads**.

</div>

## Route to 60 from Orgrimmar

**Class trainer city:** Orgrimmar, Valley of Honor (*Classic-era location*).

<div class="steps" markdown>

1.  **10–20**{ .lvl } The Barrens (Crossroads; **Durotar Supply and Logistics** crate camp), Silverpine

    <span class="step-label">Travel</span> Zeppelin to Undercity

2.  **13–25**{ .lvl } Ragefire Chasm, Wailing Caverns, [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md)

3.  **20–30**{ .lvl } Stonetalon, Ashenvale, Hillsbrad (Tarren Mill), Thousand Needles

    <span class="step-label">Travel</span> Sun Rock, Tarren Mill

4.  **30–40**{ .lvl } Arathi (Hammerfall), Stranglethorn (Grom'gol), Desolace, Dustwallow (Brackenwall)

    <span class="step-label">Travel</span> Grom'gol zeppelin

5.  **30–40**{ .lvl } **[Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands)** from level 30

    <span class="step-label">Travel</span> Portal at Merchant Coast

6.  **35–45**{ .lvl } **[Riverglades](../../world/zones.md#riverglades)**: Rog'mar

    <span class="step-label">Travel</span> Rog'mar FP to Stonard, Hammerfall, Kargath, Flame Crest

7.  **40–50**{ .lvl } Badlands, Swamp of Sorrows, Tanaris, Feralas, Hinterlands (Revantusk Village)

    <span class="step-label">Travel</span> Steamwheedle ferry

8.  **50–60**{ .lvl } Azshara, Un'Goro (many beasts), Felwood, Plaguelands, Winterspring

    <span class="step-label">Travel</span> Everlook

9.  **60**{ .lvl } [Mount Hyjal](../../world/zones.md#mount-hyjal)

    <span class="step-label">Travel</span> Darkwhisper Gorge

</div>

Beast-heavy zones (the Barrens, Stonetalon, Stranglethorn, Feralas, Un'Goro, Winterspring) are where Beast Slaying pays off most.

## Faction-specific notes

- **Mount:** Raptor from Sen'jin Village (*Classic-era location*) at 40. Home reputation is **Darkspear Trolls**; Honored saves 10%.
- **Darkspear Islands:** the new battleground's Horde faction is the **Darkspear Raiders**. Exalted gives a tabard questline and **1 Legacy Point**.
- **Library books:** Owen Thadd, Magic Quarter, Undercity.
- **Crates:** Durotar Supply and Logistics, west of the Crossroads.
- **PvP gear:** Hall of Legends, Orgrimmar.
- **Lore:** Darkspear hunters and headhunters; the Echo Isles and the new battleground islands off Dustwallow tie the race to Forever's new PvP content.

## Verdict

<div class="verdict" markdown>

A strong Horde Hunter, especially for **Marksmanship** raiding: Berserking keeps its full value with no pet, while Orc's Command doesn't. Leveling is quick thanks to Beast Slaying and Rapid Regeneration. Pick Orc for Beast Mastery and stun resistance, Troll for petless or haste-focused play.

</div>
