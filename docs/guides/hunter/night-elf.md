---
tags:
  - Hunter
  - Night Elf
  - Alliance
---

# Night Elf Hunter

<div class="guide-head" data-class="hunter" markdown>

:codex-hunter:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Add-on</span> **:codex-alliance:{ .fc-sigil aria-hidden="true" } Alliance**{ .badge .faction } **DPS**{ .badge .dps }

<p class="gh-note" markdown>Read with the [Hunter guide](index.md).</p>

</div>

## Why this combo

The classic kaldorei archer. Method calls Night Elf "arguably the strongest" Hunter race in Forever. Warcraft Tavern puts it together with Human as the top Alliance PvE choice.

The reason is **Elune's Light**, a new +10% crit cooldown for 15 s. When you use it together with Rapid Fire, Summon Hawk and trinkets, it is the biggest burst racial that an Alliance Hunter can get. Shadowmeld adds an extra escape and a threat drop.

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Elune's Light** *(new)* <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **5/5**{ .stars .s5 }</p>
<p markdown><span class="ability-label">PvE</span> +10% crit for 15 s. Use it on the pull with Rapid Fire. Your pet gets your crit, so the pet also gets the bonus</p>
<p markdown><span class="ability-label">PvP</span> Burst window: start with it, then Aimed Shot, Arcane Shot</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>Shadowmeld <span class="ability-type active">Active</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 }</p>
<p markdown><span class="ability-label">PvE</span> Method: 10 s cooldown out of combat, 2 min in combat. It **moves you to the bottom of the threat table**. A second Feign Death in dungeons</p>
<p markdown><span class="ability-label">PvP</span> Reset fights, ambush flag carriers, wait until the stealth of a Rogue ends</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>Quickness <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 }</p>
<p markdown><span class="ability-label">PvE</span> +1% dodge and +2% run speed: more survivability and faster kiting</p>
<p markdown><span class="ability-label">PvP</span> Kiting melee</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>Wisp Spirit <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **2/5**{ .stars .s2 }</p>
<p markdown><span class="ability-label">PvE</span> Faster corpse runs as a wisp</p>
<p markdown><span class="ability-label">PvP</span> Faster return after a death in a battleground</p>
</div>

</div>

Bow Specialization and Nature Resistance are not in the game now.

!!! note "Shadowmeld hotfix"
    On 6 November, Blizzard stopped the use of Ravage or Pounce by Druids in Shadowmeld. Nothing changed for Hunters.

??? example "Macros"

    ```text
    #showtooltip Rapid Fire
    /cast Elune's Light
    /cast Rapid Fire
    ```

    No source tells if Elune's Light triggers the global cooldown. If one press does not cast both spells, press again.

    ```text
    #showtooltip Shadowmeld
    /stopattack
    /petfollow
    /cast Shadowmeld
    ```

    This macro stops your attack and calls the pet back before you vanish.

## Starting zone walkthrough 1–12

Night Elves start in **Shadowglen**, Teldrassil. Blizzard gave Shadowglen the same changes as the Valley of Trials: **new NPCs, quests, profession hooks and "small moments"**. No source gives the names of the new quests. Thus the route below follows Classic where it did not change (*Classic-era*).

<div class="steps" markdown>

1.  **1–5**{ .lvl } Shadowglen

    - Start with Conservator Ilthalaine at Aldrassil: grells and young nightsabers. Then do the Fel Moss and Webwood spider quests in the Shadowthread Cave.
    - The **Hunter trainer is at Aldrassil** (Ayanna Everstride in Classic; *Classic-era*). At 4, train **Serpent Sting**.
    - Look for the new Forever additions in Shadowglen and get them as you go.

2.  **5–10**{ .lvl } Dolanaar

    - Walk to **Dolanaar** (inn, flight path to Rut'theran through the portal and Darnassus). Take *The Great Outdoors* to unlock [camping](../../systems/camping.md). Also take the starter gathering quest.
    - Do the quests in the Ban'ethil Barrow Den, Fel Rock, Starbreeze Village and the Oracle Glade.
    - Train Arcane Shot and Hunter's Mark (6), Concussive Shot (8).

3.  **10**{ .lvl } The first pet

    - In Classic, **Dazalar** in Dolanaar gave the taming chain: **Webwood Lurker** (spider), **Nightsaber Stalker** (cat) and **Strigid Screecher** (owl) (*Classic-era*). The Forever quest is *Taming the Beast* (Night Elf; Warcraft Tavern gives 6063). The chain ends with *Training the Beast* (6103).
    - Owls are now **Birds of Prey**, with the *Mine!* disarm.
    - Keep a **Nightsaber** (cat) for leveling damage. First talent: **Deadly Aspects**.

4.  **10–12**{ .lvl } Teldrassil to Darkshore

    - Complete the Lake Al'Ameth and Wellspring quests. Go to Darnassus to train. Then take the boat from Rut'theran Village to **Auberdine**.

</div>

## Route to 60 from Darnassus

**Class trainer city:** Darnassus, Cenarion Enclave (*Classic-era location*).

<div class="steps" markdown>

1.  **10–20**{ .lvl } Darkshore (Auberdine)

    <span class="step-label">Travel</span> Auberdine boat. **Auberdine ↔ Stormwind Harbor** (new) gives early access to the Eastern Kingdoms

2.  **15–25**{ .lvl } Westfall or Loch Modan, Redridge (Three Corners crate camp)

    <span class="step-label">Travel</span> Stormwind Harbor

3.  **18–30**{ .lvl } Ashenvale (Astranaar), Stonetalon, Wetlands ([Excavation Site](../../content/dungeons/excavation-site.md)), Duskwood

    <span class="step-label">Travel</span> Menethil–Southshore–Auberdine loop (new)

4.  **25–35**{ .lvl } Hillsbrad, [Dalaran](../../world/zones.md#dalaran), Thousand Needles

    <span class="step-label">Travel</span> Southshore

5.  **30–40**{ .lvl } Desolace (Nijel's Point), Stranglethorn, Dustwallow, Arathi

    <span class="step-label">Travel</span> Desolace centaur quests need level 35

6.  **35–45**{ .lvl } **[Riverglades](../../world/zones.md#riverglades)** (Farholde Keep)

    <span class="step-label">Travel</span> Ferry from Tanaris, or walk from Redridge

7.  **40–50**{ .lvl } Feralas (Feathermoon), Tanaris, Hinterlands, Swamp of Sorrows

    <span class="step-label">Travel</span> Feathermoon ↔ Forgotten Coast boat

8.  **50–60**{ .lvl } Azshara, Un'Goro, Felwood, Winterspring, Plaguelands, Silithus

    <span class="step-label">Travel</span> Talonbranch Glade, Everlook

9.  **60**{ .lvl } [Mount Hyjal](../../world/zones.md#mount-hyjal)

    <span class="step-label">Travel</span> Darkwhisper Gorge

</div>

For Night Elves, it is natural to level in Kalimdor first. The new Stormwind boat makes it easy to also do zones in the Eastern Kingdoms.

## Faction-specific notes

- **Mount:** Frostsaber from Rut'theran Village (*Classic-era location*) at 40. **Honored with Darnassus** gives a 10% discount.
- **Darnassus** now has a barbershop (beta notes).
- **Library books:** Garion Wendell, Wizard's Sanctum, Stormwind.
- **Crates:** Azeroth Commerce Authority at Three Corners, Redridge.
- **PvP:** Theramore Expeditionary Force from Darkspear Islands. Champion's Hall in Stormwind.
- **Lore:** Sentinels and huntresses of Elune. Skyborne are a related elven people. Night Elves and Skyborne both speak Darnassian.

## Verdict

<div class="verdict" markdown>

Method says that this is the **strongest Alliance Hunter for PvE damage**. Shadowmeld makes it very good for solo play and Hardcore. Human is a little better in duels because of the stun break. Select Night Elf if raid burst and a free threat drop are the most important to you.

</div>
