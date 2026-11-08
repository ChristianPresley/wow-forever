---
tags:
  - Warlock
  - Gnome
  - Alliance
---

# Gnome Warlock

<div class="guide-head" data-class="warlock" markdown>

:codex-warlock:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Add-on</span> **:codex-alliance:{ .fc-sigil aria-hidden="true" } Alliance**{ .badge .faction } **DPS**{ .badge .dps }

<p class="gh-note" markdown>Read with the [Warlock guide](index.md). This page covers only what changes when your Warlock is a Gnome.</p>

</div>

## Why this combo

A Classic combination with a new twist. Gnomes keep **Escape Artist** and **Expansive Mind**, and gain **Eureka!**, an 8-second window in which non-periodic spells cost less and hit harder. That makes Gnome a better fit for **Destruction and Demonology** (Incinerate, Soul Fire, Searing Pain) than for Affliction, whose damage comes mostly from DoTs and channels. Warcraft Tavern says Gnome gains the least of the Warlock races but still sits close to the others; Method.gg puts it in its B tier.

| | |
|---|---|
| **Status** | Classic combination |
| **Faction** | **Alliance**{ .pill .pill--alliance } |
| **Start / capital** | Coldridge Valley, Dun Morogh / Ironforge |
| **Mount** | Mechanostrider (Felsteed from 40) |
| **Home reputation** | Gnomeregan Exiles |

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Escape Artist** <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 } PvP · **2/5**{ .stars .s2 } PvE</p>
<p markdown>Removes roots and snares, plus 3 s immunity. Breaks Frost Nova, Entangling Roots, Hamstring and Wing Clip so you can get back to Fear range</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Eureka!** *(new)* <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 } Destro/Demo · **2/5**{ .stars .s2 } Aff</p>
<p markdown>For 8 s, non-periodic abilities cost 10% less and deal 10% more. Warcraft Tavern gives a 2-minute cooldown. DoT ticks and (per guides) channels don't benefit, so use it on Conflagrate + Shadowburn + Incinerate, or a Decimation Soul Fire</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Expansive Mind** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 }</p>
<p markdown>+5% maximum mana. Fewer Life Taps per fight, and a bigger buffer when leveling</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Engineering Specialization** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **2/5**{ .stars .s2 }</p>
<p markdown>20% fewer device failures. No longer adds Engineering skill. Only useful if you take Engineering, which Warcraft Tavern does suggest for top damage</p>
</div>

</div>

??? example "Macros"

    Destruction burst:

    ```
    #showtooltip Conflagrate
    /cast Eureka!
    /cast Conflagrate
    ```

    Demonology execute:

    ```
    #showtooltip Soul Fire
    /cast Eureka!
    /cast Soul Fire
    ```

    Root break, then Fear:

    ```
    #showtooltip Fear
    /cast Escape Artist
    /cast Fear
    ```

    *Whether Eureka! and Escape Artist trigger the global cooldown is unverified; if they do, press the macro twice.*

## Starting zone walkthrough (1–12)

You start in **Coldridge Valley**, Dun Morogh. Trainer names follow Classic; check in game.

<div class="steps" markdown>

1.  **1**{ .lvl } sell your starting gear and buy **Immolate** from the warlock trainer in Anvilmar (Classic: *Alamar Grimm*). Do the **Imp** quest.
2.  **1–5**{ .lvl } troggs, wolves and the Coldridge chain. Learn **Corruption**, **Curse of Weakness** and the **Blood Pact** grimoire at 4.
3.  **~5**{ .lvl } go through the tunnel to **Kharanos**. Pick up **The Great Outdoors** ([camping](../../systems/camping.md)) and the gathering-profession starter quest. The Kharanos warlock trainer (Classic: *Gimrizz Shadowcog*, Thunderbrew Distillery) covers 6–10.
4.  **6–10**{ .lvl } Life Tap at 6, Bane of Agony and Fear at 8. Quest around Kharanos, Brewnall Village, Gnomeregan's outer camps and the Frostmane trolls.
5.  **10**{ .lvl } first talent point (**Improved Corruption**), Drain Soul and Healthstone. For the **Voidwalker** quest Method.gg recommends taking the **Deeprun Tram** to Stormwind (Mage Quarter) rather than the Ironforge version.
6.  **10–13**{ .lvl } the new **[Hall of Thanes](../../content/dungeons/hall-of-thanes.md)** dungeon in Ironforge (13–18) is right on your doorstep. Then **Loch Modan**.

</div>

## Route to 60 from Ironforge

<div class="steps" markdown>

1.  **10–20**{ .lvl } Loch Modan, Westfall or **Darkshore**

    Menethil → Auberdine boat, or tram to Stormwind and take the new Stormwind Harbor boat. Hall of Thanes, then Deadmines. Sayaad quest at 20

2.  **20–30**{ .lvl } Wetlands, Redridge, Duskwood, Ashenvale

    New **[Excavation Site](../../content/dungeons/excavation-site.md)** in the Wetlands. Gnomeregan (29–38) is your home dungeon for the Gnomeregan Exiles story

3.  **30–40**{ .lvl } Hillsbrad, Arathi, Stranglethorn, Desolace, Dustwallow

    **[City of Dalaran](../../content/dungeons/city-of-dalaran.md)** and Kirin Tor reputation. Felhunter at 30

4.  **35–45**{ .lvl } **[Riverglades](../../world/zones.md#riverglades)**

    Walk in from Loch Modan via the Badlands or from Redridge. **Farholde Keep** flight master connects to Thelsamar. Felsteed quest at 40 (Strahad Farsan, Ratchet)

5.  **40–50**{ .lvl } Hinterlands, Tanaris, Feralas, Badlands

    Uldaman is a short ride from Loch Modan. Krol'dok Stronghold in the Riverglades

6.  **50–60**{ .lvl } Searing Gorge, Burning Steppes, Azshara, Un'Goro, Felwood, Plaguelands, Winterspring

    Blackrock Mountain is close to Ironforge. Then Mount Hyjal

</div>

**Class trainer city:** Ironforge (Classic: the Forlorn Cavern) or Stormwind. Library-book quests go to **Garion Wendell** in Stormwind's Wizard's Sanctum.

## Faction-specific notes

- **Class quests:** Imp (1), Voidwalker (10, Stormwind recommended), Sayaad (20), Felhunter (30), Felsteed (40), Dreadsteed (60).
- **Reputation:** Gnomeregan Exiles. Honored gives 10% off Riding and mechanostriders.
- **Professions:** Engineering pairs naturally with your racial, and Warcraft Tavern rates **Tailoring + Engineering** as the highest-damage Warlock pairing.
- **Raids:** Alliance Onyxia attunement (Burning Steppes, BRD, Stormwind). Blackrock Mountain is a short trip from Ironforge.
- **Cosmetic:** gnome Warlocks are a lore staple of the Gnomeregan exile era; the HD model's small size also makes you harder to click in PvP.

## Verdict

<div class="verdict" markdown>

**A good choice for Destruction or Demonology, the weakest of the five for pure Affliction.** Eureka! gives Fire builds a real burst window and Escape Artist is excellent against melee kiting. If you plan to play Affliction, Human gives more.

</div>
