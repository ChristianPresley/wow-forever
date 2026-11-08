---
tags:
  - Warlock
  - Troll
  - Horde
---

# Troll Warlock

<div class="guide-head" data-class="warlock" markdown>

:codex-warlock:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Add-on</span> **:codex-horde:{ .fc-sigil aria-hidden="true" } Horde**{ .badge .faction } **DPS**{ .badge .dps }

<p class="gh-note" markdown>Read with the [Warlock guide](index.md). This page covers only what changes when your Warlock is a Troll.</p>

</div>

## Why this combo

**New in Forever.** Trolls couldn't be Warlocks in Classic; Forever is the first Classic-era version to allow it. It was also one of the beta's talking points: reviewers singled out Troll Warlock when complaining about overtuned revamped racials, and Blizzard went on to tune the Troll and Orc racials before launch. Trolls bring **Berserking** for a cast-speed burst, the new **Rapid Regeneration** for fast recovery between pulls, and **Beast Slaying** against beasts. Warcraft Tavern says Troll is good in beast-heavy content; Method.gg ranks it lowest of the five (C tier), so it is the flavor pick rather than the min-max one.

| | |
|---|---|
| **Status** | **NEW** combination |
| **Faction** | **Horde**{ .pill .pill--horde } |
| **Start / capital** | Valley of Trials, Durotar / Orgrimmar |
| **Mount** | Raptor (Felsteed from 40) |
| **Home reputation** | Darkspear Trolls |

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Berserking** <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 } Destro · **3/5**{ .stars .s3 } Aff/Demo</p>
<p markdown>+10% cast and attack speed for **15 s** (raised from 10 s in the 26 Oct beta notes). Speeds Incinerate, Shadow Bolt, Searing Pain, Soul Fire and the global cooldown; per Warcraft Tavern it doesn't speed DoT ticks or channels, so it does little for Wrack. Cooldown not published (3 min in Classic)</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Rapid Regeneration** *(new)* <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 } leveling · **2/5**{ .stars .s2 } PvP</p>
<p markdown>Regenerates **50% of max health over 6 s**, cancelled by any action. A free half-heal after every Life Tap session: tap down to half, Rapid Regenerate back, keep the mana</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Beast Slaying** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **2/5**{ .stars .s2 }</p>
<p markdown>+5% damage against beasts. Good for leveling (lots of beasts) and any beast bosses; nothing confirmed for the launch raids</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Regeneration** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **2/5**{ .stars .s2 }</p>
<p markdown>+20% health regeneration, part of it in combat. Synergizes with Life Tap and drain-tanking</p>
</div>

</div>

!!! conflict "Conflict: Berserking"
    Blizzard's 26 Oct notes and Icy Veins give a 15-second duration. Games.gg still lists 10 seconds on a 3-minute cooldown, and an earlier beta guide described a nerf to a flat 10%. This page uses Blizzard's figure.

??? example "Macros"

    Destruction burst:

    ```
    #showtooltip Berserking
    /cast Berserking
    /cast Incinerate
    ```

    Leveling recovery (out of combat):

    ```
    #showtooltip Rapid Regeneration
    /cast Life Tap
    /cast Rapid Regeneration
    ```

    *Rapid Regeneration is cancelled by any action, so after this macro don't press anything for 6 s.*

## Starting zone walkthrough (1–12)

Trolls share the **Valley of Trials** in Durotar with orcs; Blizzard says it gained new NPCs, quests and profession hooks in Forever. Trainer names follow Classic.

<div class="steps" markdown>

1.  **1**{ .lvl } sell your gear, buy **Immolate** from the warlock trainer in the Den (Classic: *Nartok*), and do the **Imp** quest.
2.  **1–5**{ .lvl } boars, scorpids, Sarkoth and the Burning Blade cave. **Corruption**, **Curse of Weakness** and the **Blood Pact** grimoire at 4.
3.  **~5**{ .lvl } **The Great Outdoors** ([camping](../../systems/camping.md)) and the gathering starter. Move to **Razor Hill** (trainer, Classic: *Dhugru Gorelust*).
4.  **6–10**{ .lvl } Life Tap at 6, Bane of Agony and Fear at 8. Visit **Sen'jin Village** and the **Echo Isles** quests: the Darkspear home ground and the story of Zalazane's hexed trolls. Rapid Regeneration makes your first Life Tap habits painless.
5.  **10**{ .lvl } first talent point (**Improved Corruption**), Drain Soul, Healthstone. For the **Voidwalker**, Warcraft Tavern and Method.gg both prefer the **Undercity** quest over Orgrimmar's Skull Rock version.
6.  **10–13**{ .lvl } Ragefire Chasm, then the Barrens.

</div>

## Route to 60 from Orgrimmar

<div class="steps" markdown>

1.  **10–20**{ .lvl } Barrens, Silverpine

    Barrens beasts make Beast Slaying shine. Wailing Caverns, Ragefire Chasm, **[Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md)**. Sayaad at 20 (eight-quest Horde chain)

2.  **20–30**{ .lvl } Stonetalon, Ashenvale, Hillsbrad

    Shadowfang Keep, Blackfathom Deeps. Arathi Basin opens at 20

3.  **30–40**{ .lvl } Thousand Needles, Desolace, Stranglethorn, Arathi, Dustwallow

    Felhunter at 30. Stranglethorn's tigers, panthers and raptors are prime Beast Slaying targets. **[Battle for the Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands)** opens at 30

4.  **35–45**{ .lvl } **[Riverglades](../../world/zones.md#riverglades)**

    Rog'mar is the Horde hub; Bolder'ok ogres are Horde-aligned. Felsteed at 40 via Strahad Farsan, Ratchet

5.  **40–50**{ .lvl } Feralas, Tanaris, Badlands

    Krol'dok Stronghold, Zul'Farrak (troll-themed), Alcaz Prison

6.  **50–60**{ .lvl } Azshara, Un'Goro (lots of beasts and devilsaurs), Felwood, Plaguelands, Winterspring

    Blackmaw Hold, Shaper's Terrace, Sunken Temple (troll-themed). Then Mount Hyjal

</div>

**Class trainer city:** Orgrimmar, Cleft of Shadow. Library-book quests go to **Owen Thadd** in Undercity's Magic Quarter.

## Faction-specific notes

- **Class quests:** the same Horde chains as orcs: Imp (1), Voidwalker (10), Sayaad (20), Felhunter (30), Felsteed (40), Dreadsteed (60). No troll-specific Warlock quests are documented.
- **Reputation:** Darkspear Trolls; Honored gives 10% off Riding and raptors. **Darkspear Raiders** is a separate PvP reputation from the Darkspear Islands battleground, fittingly themed for a troll.
- **Lore:** Darkspear culture distrusts demonology, and their shadow hunters and witch doctors deal with loa, not demons. A troll warlock is an outsider among the Darkspear, an angle Forever's new combinations invite you to role-play. Blizzard hasn't announced troll-specific Warlock lore.
- **Raids:** Horde Onyxia attunement as for orcs.

## Verdict

<div class="verdict" markdown>

**The fun, fresh option, fine in practice.** Berserking gives Destruction a decent burst window, and Rapid Regeneration plus Regeneration make leveling smooth. For maximum damage pick Orc, for PvP pick Undead; pick Troll because you want a Darkspear Warlock.

</div>
