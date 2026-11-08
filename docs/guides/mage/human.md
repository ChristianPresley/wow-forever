---
tags:
  - Mage
  - Human
  - Alliance
---

# Human Mage

<div class="guide-head" data-class="mage" markdown>

:codex-mage:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Add-on</span> **:codex-alliance:{ .fc-sigil aria-hidden="true" } Alliance**{ .badge .faction } **DPS**{ .badge .dps }

<p class="gh-note" markdown>Read with the [Mage guide](index.md). This page covers only what changes when your Mage is a Human.</p>

</div>

## Why this combo

Human Mage is the classic Alliance caster and remains one of the best all-round picks. Forever replaced the old weapon racials with a **stun breaker** and **+1% crit**, both of which a Mage uses constantly. You also start next to Stormwind, which now has a harbor with a boat to Darkshore, so your early route is the most flexible on the Alliance side.

| | |
|---|---|
| **Status** | Classic combination |
| **Faction** | **Alliance**{ .pill .pill--alliance } |
| **Start / capital** | Northshire Valley, Elwynn Forest / Stormwind |
| **Mount** | Horse |
| **Home reputation** | Stormwind |

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Will to Survive** *(new)* <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **5/5**{ .stars .s5 } PvP · **3/5**{ .stars .s3 } PvE</p>
<p markdown>Instantly removes stuns. A Rogue's Cheap Shot or a Warrior's Intercept no longer means death: break it, then Frost Nova and Blink</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Perception** <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 } PvP · **1/5**{ .stars .s1 } PvE</p>
<p markdown>Detect stealth for 20 s. Pop it when a Rogue or Druid disappears near a flag or node</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Ruthless** *(new)* <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 }</p>
<p markdown>+1% crit. Feeds Fire's Heating Up and Ignite, Arcane Impact, and Frost shatter combos</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**The Human Spirit** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 } leveling · **2/5**{ .stars .s2 } raid</p>
<p markdown>+10% Spirit (was 5%). Noticeably less drinking at low levels</p>
</div>

</div>

The old Human *Diplomacy* racial is now the account-wide Legacy talent *Diplomat*, so you don't lose anything there.

??? example "Macros"

    Break a stun and escape (whether Will to Survive triggers the global cooldown is *not verified*; if it does, press the macro twice):

    ```
    #showtooltip Will to Survive
    /cast Will to Survive
    /cast Blink
    ```

    Detect stealth and drop a Frost Nova around you:

    ```
    #showtooltip Perception
    /cast Perception
    /cast Frost Nova
    ```

## Starting zone walkthrough (1–12)

Northshire and Elwynn are largely the Classic zones. Quest names below are Classic-era; Forever kept the core chains but added new NPCs and side quests in some starting zones.

<div class="steps" markdown>

1.  **1–5**{ .lvl } **Northshire Abbey.** Deputy Willem starts you off with the wolves and kobolds outside the abbey. Your Mage trainer is **Khelden Bremen** on the upper floor of the abbey (Classic location); he also sends a class letter you'll find in your bags.
2.  **2–4**{ .lvl } Train Frostbolt at 4, plus Conjure Water. Kill kobolds in the vineyard and the Echo Ridge Mine.
3.  **5–6**{ .lvl } Hand in *Report to Goldshire* and leave the valley. Fire Blast at 6.
4.  **6–10**{ .lvl } **Goldshire.** The Lion's Pride Inn is your hub. A Mage trainer works inside the inn (Classic). Do the Fargodeep Mine, Jerod's Landing and Eastvale Logging Camp quests. Polymorph at 8 makes double pulls safe.
5.  **10**{ .lvl } Frost Nova and your first talent point. Pick a gathering or crafting profession now — Tailoring trainers are in Stormwind's Trade District.
6.  **10–12.** Finish Elwynn (Princess, the Brotherhood of Thieves chain) and run *Westfall* letters, or ride the new **Stormwind Harbor** boat to Darkshore.

</div>

!!! tip "Stormwind Mage Quarter"
    The full trainer set and the Mage portal trainer are in the Wizard's Sanctum in the Mage Quarter. The transmogrifier, **Fyrenz Vishonar**, is also in the Mage Quarter (48, 84).

## Route to 60 from Stormwind

<div class="steps" markdown>

1.  **10–20**{ .lvl } Westfall, then Redridge **or** Darkshore

    <span class="step-label">Travel</span> Fly from Stormwind; the harbor boat goes straight to Auberdine

2.  **18–25**{ .lvl } Loch Modan or Darkshore end-game, Redridge

    <span class="step-label">Travel</span> Deeprun Tram to Ironforge for Loch Modan

3.  **20–30**{ .lvl } Duskwood, Wetlands, Ashenvale

    <span class="step-label">Travel</span> Wetlands has the new [Excavation Site](../../content/dungeons/excavation-site.md) dungeon

4.  **25–35**{ .lvl } Hillsbrad (new Southshore pier), Alterac Mountains

    <span class="step-label">Travel</span> Menethil → Southshore → Auberdine boat loop

5.  **30–40**{ .lvl } Stranglethorn, Arathi, Desolace, Dustwallow

    <span class="step-label">Travel</span> Dalaran (Alterac) is Alliance-friendly; the [City of Dalaran](../../content/dungeons/city-of-dalaran.md) key chain starts in Southshore or Stormwind

6.  **35–45**{ .lvl } **[Riverglades](../../world/zones.md#riverglades)**

    <span class="step-label">Travel</span> Walk east from Redridge; Farholde Keep flight connects to Lakeshire

7.  **40–50**{ .lvl } Tanaris, Feralas, Hinterlands, Badlands

    <span class="step-label">Travel</span> Riding at 40

8.  **50–60**{ .lvl } Un'Goro, Azshara, Felwood, Plaguelands, Winterspring, Burning Steppes

    <span class="step-label">Travel</span> Winterspring leads to [Mount Hyjal](../../world/zones.md#mount-hyjal)

</div>

**Teleports (Classic levels):** Stormwind and Ironforge at 20, Darnassus at 30. Ask other Mages for a Dalaran portal; *Teleport: Dalaran* at 50 is unconfirmed.

**Dungeons along the way:** The Deadmines (Westfall) and The Stockade (Stormwind) are right on your doorstep; [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) is a tram ride away.

## Faction-specific notes

- **Class quests:** Classic-era Alliance Mage quests run through the Stormwind and Ironforge trainers. The library-book quests at 20/35/45 are available to every class; turn books in at your capital.
- **Reputation:** Stormwind Honored gives 10% off riding and the Horse. The **Azeroth Commerce Authority** crate faction is at Three Corners, Redridge — close to your route at 15–25.
- **Kirin Tor:** Alliance-only reputation in Dalaran.
- **PvP:** Champion's Hall in Stormwind holds PvP vendors.
- **Lore:** Humans make up the bulk of the Kirin Tor's magi; the restored Dalaran in the Alterac Mountains is very much your city.

## Verdict

<div class="verdict" markdown>

A no-regrets choice. Will to Survive is the best Alliance PvP racial for a Mage, Ruthless helps every spec, and the extra Spirit keeps early leveling smooth. Pick Gnome if you want more burst and root-breaking, or Skyborne for haste and regen.

</div>
