---
tags:
  - Priest
  - Gnome
  - Alliance
---

# Gnome Priest

<div class="guide-head" data-class="priest" markdown>

:codex-priest:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Add-on</span> **:codex-alliance:{ .fc-sigil aria-hidden="true" } Alliance**{ .badge .faction } **Healer**{ .badge .heal } **DPS**{ .badge .dps }

<p class="gh-note" markdown>Read with the [Priest guide](index.md).</p>

</div>

## Why this combo

**New in Forever.** Gnomes couldn't be Priests in Classic. Blizzard gave them two brand-new race spells: **Confounding Flash**, a group confuse, and **Contingency Plan**, a ward that catches you at low health. Add **Eureka!**, which boosts direct spells and heals for 8 s, and +5% mana, and the Gnome becomes what Warcraft Tavern calls a "deceptively strong" Priest.

**Best for:** Discipline and Holy healers (Eureka! boosts Penance, Flash Heal and Greater Heal), Shadow burst, and anyone who wants to play the new combination.

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Escape Artist** <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 }</p>
<p markdown><span class="ability-label">PvE</span> Breaks roots and snares, then gives 3 s immunity. Useful against netting and frost mobs</p>
<p markdown><span class="ability-label">PvP</span> Breaks Frost Nova, Hamstring, Entangling Roots and Crippling Poison. Excellent for a fragile caster</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Eureka!** *(new)* <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 }</p>
<p markdown><span class="ability-label">PvE</span> For 8 s, **non-periodic** spells cost 10% less and deal or heal 10% more. Good for Mind Blast, Penance (assuming its channel counts as non-periodic; *unconfirmed*), Flash Heal, Greater Heal and Prayer of Healing. It does nothing for SW:Pain, Renew or Devouring Plague</p>
<p markdown><span class="ability-label">PvP</span> Burst window for Mind Blast and SW:Death</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Expansive Mind** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 }</p>
<p markdown><span class="ability-label">PvE</span> **+5% maximum mana.** Bigger pool on long fights</p>
<p markdown><span class="ability-label">PvP</span> Same</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Engineering Specialization** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **1/5**{ .stars .s1 } (**3/5**{ .stars .s3 } with Engineering)</p>
<p markdown><span class="ability-label">PvE</span> 20% fewer device failures. Only matters with Engineering</p>
<p markdown><span class="ability-label">PvP</span> Engineering gadgets in PvP</p>
</div>

</div>

**Priest spells unique to Gnomes**

| Spell | Level | Effect | Use |
|---|---|---|---|
| **Confounding Flash** *(new)* | 10 | Confuses up to **5 enemies for 3 s**; damage breaks it. 0.5 s cast, 2-minute cooldown | A short group CC. Interrupt a bad pull to drink a potion, or break up a melee train before Psychic Scream. Avoid DoTing confused targets |
| **Contingency Plan** *(new)* | 20 | A 30 s ward. If you fall below 35% health while it's up, you get an absorb shield and a heal-over-time. Stacks with Renew and Power Word: Shield. Instant, 5-minute cooldown | Cast before risky pulls or boss phases. Also an excellent Hardcore safety net |

!!! note "Is Confounding Flash a PvP diminishing-return CC?"
    Not documented. Expect it to share diminishing returns with other confuse effects, as in later expansions (*unconfirmed*).

??? example "Macros"

    Eureka! into Penance (Discipline):

    ```
    #showtooltip Penance
    /cast Eureka!
    /cast [@mouseover,help,nodead][] Penance
    ```

    Escape Artist, then Shield yourself:

    ```
    #showtooltip Escape Artist
    /cast Escape Artist
    /cast [@player] Power Word: Shield
    ```

    !!! note
        It isn't documented whether Eureka! is on the global cooldown. If the spell on the second line doesn't fire, press twice.

## Starting zone walkthrough (1–~12)

Gnomes share **Coldridge Valley**, Dun Morogh, with Dwarves. Quest names are Classic-era.

!!! warning "Trainer location"
    Classic gnomes had no Priests, so there was no Gnome Priest trainer. The expectation is that the **Anvilmar** Priest trainer (Classic: Branstock Khalder) teaches gnomes too, but Blizzard hasn't confirmed whether Forever adds a gnome trainer (*unconfirmed*).

<div class="steps" markdown>

1.  **1–2**{ .lvl } quests at **Anvilmar**: wolves and troggs. Train at the Priest trainer in Anvilmar.
2.  **2–5**{ .lvl } troll camp quests and the mail run to **Kharanos**. Train **Shadow Word: Pain** at 4.
3.  **5**{ .lvl } take **The Great Outdoors** and learn Cooking. Engineering is an on-theme profession, but for a Priest, Tailoring + Enchanting is stronger (wands).
4.  **6**{ .lvl } **Power Word: Shield**, then kill **Grik'nir the Cold** in the cave.
5.  **6–10**{ .lvl } the Kharanos quest hub, Brewnall Village and the Gnomeregan refugees (gnome-themed quests near the Gnomeregan entrance).
6.  **10**{ .lvl } learn **Confounding Flash** and your first talent, and take the class quest. Visit Ironforge's **Mystic Ward** for full Priest training.
7.  **10–12**{ .lvl } finish Dun Morogh, then head east to **Loch Modan**.

</div>

## Route to 60 from Ironforge

<div class="steps" markdown>

1.  **10–18**{ .lvl } Loch Modan

    <span class="step-label">Hub / flight path</span> Thelsamar

2.  **13–20**{ .lvl } [Hall of Thanes](../../content/dungeons/hall-of-thanes.md)

    <span class="step-label">Hub / flight path</span> Ironforge

3.  **15–22**{ .lvl } Westfall or Redridge (Deeprun Tram)

    <span class="step-label">Hub / flight path</span> Sentinel Hill, Lakeshire

4.  **20–30**{ .lvl } Wetlands ([Excavation Site](../../content/dungeons/excavation-site.md)), Duskwood, Ashenvale

    <span class="step-label">Hub / flight path</span> Menethil Harbor

5.  **29–38**{ .lvl } **Gnomeregan** (your race's ruined capital)

    <span class="step-label">Hub / flight path</span> Dun Morogh

6.  **30–40**{ .lvl } Arathi Highlands, Alterac Mountains (Dalaran), Stranglethorn Vale, Desolace

    <span class="step-label">Hub / flight path</span> Refuge Pointe, Booty Bay

7.  **35–45**{ .lvl } **Riverglades**

    <span class="step-label">Hub / flight path</span> Farholde Keep

8.  **40–50**{ .lvl } Badlands, Swamp of Sorrows, Hinterlands, Tanaris, Feralas, Dustwallow

    <span class="step-label">Hub / flight path</span> Aerie Peak, Gadgetzan, Theramore

9.  **50–60**{ .lvl } Searing Gorge, Burning Steppes, Un'Goro, Azshara, Plaguelands, Winterspring, Silithus

    <span class="step-label">Hub / flight path</span> Morgan's Vigil, Everlook

10.  **60**{ .lvl } Mount Hyjal

    <span class="step-label">Hub / flight path</span> Tainted Foothills

</div>

- **Class trainers:** Ironforge's Mystic Ward.
- **Riverglades** connects to Loch Modan (Thelsamar) by flight from Farholde Keep, so it's an easy trip from Ironforge.
- Gnomes reach Kalimdor through the Deeprun Tram to Stormwind, then the Stormwind Harbor boat to Auberdine (new).

## Faction-specific notes

- **Mount:** mechanostriders at 40 (100g). Honored with **Gnomeregan Exiles** gives 10% off.
- **Reputation:** Gnomeregan Exiles is your home faction.
- **Lore:** gnomes were traditionally tinkers and mages; a gnome turning to the Light is new for Forever. The Mystic Ward in Ironforge, shared with dwarven priests, is where they train.
- **Popularity:** being new, Gnome Priests are rare in early groups.

## Verdict

<div class="verdict" markdown>

**A strong, safe and unusual pick.** Contingency Plan is a free self-save every five minutes, Confounding Flash is a group CC no other Priest has, and Eureka! is a real throughput cooldown for Discipline and Holy. Night Elf and Human have stronger passive stats, but Gnome has the most interesting Priest kit in Forever.

</div>
