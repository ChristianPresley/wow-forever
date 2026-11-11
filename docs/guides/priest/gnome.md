---
tags:
  - Priest
  - Gnome
  - Alliance
---

# Gnome Priest

:codex-priest:{ .fc-sigil aria-hidden="true" } <span class="fc-meta__kind">Add-on: Race</span> **:codex-alliance:{ .fc-sigil aria-hidden="true" } Alliance**{ .badge .faction } **Healer**{ .badge .heal } **DPS**{ .badge .dps } [Data and sources](index.md#sources)
{: .fc-meta data-class="priest" }

Read with the [Priest progression](index.md).

## Why this combo

**New in Forever.** In Classic, Gnomes could not be Priests. Blizzard gave them two new race spells: **Confounding Flash**, a group confuse, and **Contingency Plan**, a ward that protects you at low health. Gnomes also have **Eureka!**, which increases direct spells and heals for 8 s, and +5% mana. With these, the Gnome is a Priest that Warcraft Tavern calls "deceptively strong".

**Best for:** Discipline and Holy healers (Eureka! increases Penance, Flash Heal and Greater Heal), Shadow burst, and all players who want to play the new combination.

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Escape Artist** <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 }</p>
<p markdown><span class="ability-label">PvE</span> Breaks roots and snares, then gives 3 s immunity. Useful against nets and frost mobs</p>
<p markdown><span class="ability-label">PvP</span> Breaks Frost Nova, Hamstring, Entangling Roots and Crippling Poison. Very good for a weak caster</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Eureka!** *(new)* <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 }</p>
<p markdown><span class="ability-label">PvE</span> For 8 s, **non-periodic** spells cost 10% less and do 10% more damage or healing. Good for Mind Blast, Penance (if its channel counts as non-periodic, *unconfirmed*), Flash Heal, Greater Heal and Prayer of Healing. It has no effect on SW:Pain, Renew or Devouring Plague</p>
<p markdown><span class="ability-label">PvP</span> Burst window for Mind Blast and SW:Death</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Expansive Mind** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 }</p>
<p markdown><span class="ability-label">PvE</span> **+5% maximum mana.** Larger mana pool for long fights</p>
<p markdown><span class="ability-label">PvP</span> Same</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Engineering Specialization** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **1/5**{ .stars .s1 } (**3/5**{ .stars .s3 } with Engineering)</p>
<p markdown><span class="ability-label">PvE</span> 20% fewer device failures. Important only with Engineering</p>
<p markdown><span class="ability-label">PvP</span> Engineering gadgets in PvP</p>
</div>

</div>

**Priest spells unique to Gnomes**

| Spell | Level | Effect | Use |
|---|---|---|---|
| **Confounding Flash** *(new)* | 10 | Confuses a maximum of **5 enemies for 3 s**. Damage breaks it. 0.5 s cast, 2-minute cooldown | A short group CC. Use it to stop a bad pull and drink a potion, or to break a group of melee attackers before Psychic Scream. Do not put DoTs on confused targets |
| **Contingency Plan** *(new)* | 20 | A 30 s ward. If your health goes below 35% while the ward is active, you get an absorb shield and a heal-over-time. Stacks with Renew and Power Word: Shield. Instant, 5-minute cooldown | Cast it before dangerous pulls or boss phases. Also a very good Hardcore safety net |

!!! note "Is Confounding Flash a PvP diminishing-return CC?"
    This is not documented. It probably shares diminishing returns with other confuse effects, as in later expansions (*unconfirmed*).

??? example "Macros"

    Eureka! and then Penance (Discipline):

    ```
    #showtooltip Penance
    /cast Eureka!
    /cast [@mouseover,help,nodead][] Penance
    ```

    Escape Artist, then shield yourself:

    ```
    #showtooltip Escape Artist
    /cast Escape Artist
    /cast [@player] Power Word: Shield
    ```

    !!! note
        It is not documented if Eureka! is on the global cooldown. If the spell on the second line does not cast, push the button twice.

## Starting zone walkthrough (1–~12)

Gnomes and Dwarves share **Coldridge Valley**, Dun Morogh. Quest names are Classic-era.

!!! warning "Trainer location"
    Because gnomes had no Priests in Classic, there was no Gnome Priest trainer. Probably the **Anvilmar** Priest trainer (Classic: Branstock Khalder) also teaches gnomes. Blizzard has not confirmed if Forever adds a gnome trainer (*unconfirmed*).

<div class="steps" markdown>

1.  **1–2**{ .lvl } Do the quests at **Anvilmar**: wolves and troggs. Train at the Priest trainer in Anvilmar.
2.  **2–5**{ .lvl } Do the troll camp quests and the mail delivery to **Kharanos**. At 4, train **Shadow Word: Pain**.
3.  **5**{ .lvl } Get **The Great Outdoors** and learn Cooking. Engineering fits the gnome theme. But for a Priest, Tailoring + Enchanting is stronger (wands).
4.  **6**{ .lvl } Train **Power Word: Shield**. Then kill **Grik'nir the Cold** in the cave.
5.  **6–10**{ .lvl } Do the quests at the Kharanos quest hub, Brewnall Village and the Gnomeregan refugees (gnome-themed quests near the Gnomeregan entrance).
6.  **10**{ .lvl } Learn **Confounding Flash** and your first talent. Get the class quest. Go to the **Mystic Ward** in Ironforge for full Priest training.
7.  **10–12**{ .lvl } Complete Dun Morogh. Then go east to **Loch Modan**.

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

5.  **29–38**{ .lvl } **Gnomeregan** (the ruined capital of your race)

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

- **Class trainers:** the Mystic Ward in Ironforge.
- **Riverglades** has a flight from Farholde Keep to Loch Modan (Thelsamar). This makes the trip from Ironforge easy.
- Gnomes go to Kalimdor through the Deeprun Tram to Stormwind. Then they take the Stormwind Harbor boat to Auberdine (new).

## Faction-specific notes

- **Mount:** mechanostriders at 40 (100g). Honored with **Gnomeregan Exiles** gives 10% off.
- **Reputation:** Gnomeregan Exiles is your home faction.
- **Lore:** Traditionally, gnomes were tinkers and mages. A gnome who follows the Light is new for Forever. Gnome priests train at the Mystic Ward in Ironforge, together with dwarven priests.
- **Popularity:** Because Gnome Priests are new, there are few of them in early groups.

## Verdict

<div class="verdict" markdown>

**A strong, safe and unusual choice.** Contingency Plan is a free self-save every 5 minutes. Confounding Flash is a group CC that no other Priest has. Eureka! is a real throughput cooldown for Discipline and Holy. Night Elf and Human have stronger passive stats, but Gnome has the most interesting Priest kit in Forever.

</div>
