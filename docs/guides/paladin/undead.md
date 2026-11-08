---
tags:
  - Paladin
  - Undead
  - Horde
---

# Undead Paladin

<div class="guide-head" data-class="paladin" markdown>

:codex-paladin:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Add-on</span> **:codex-horde:{ .fc-sigil aria-hidden="true" } Horde**{ .badge .faction } **Tank**{ .badge .tank } **Healer**{ .badge .heal } **DPS**{ .badge .dps }

<p class="gh-note" markdown>Read with the [Paladin guide](index.md). This page covers what changes when your paladin is Forsaken.</p>

</div>

!!! warning "New combination, thin data"
    The Forsaken paladin is **new in Forever** and the Horde's **only** paladin option. Most quest details below come from fan databases built during the beta and launch week, and several disagree. Levels and coordinates are marked where sources conflict.

## Why this combo

- **It's the only way to play a Horde paladin.** Orcs, Trolls, Tauren and Windshaper Skyborne cannot be paladins.
- **It has its own story.** Forsaken paladins get a dedicated 10–60 journey based at **Bandarion Keep**, their own weapon quest (*Wolfsbane*), and their own epic mount ridden "in the name of **Retribution**", mirroring the Alliance's Redemption-themed charger.
- **It is popular.** Blizzard counted **612,096** Undead paladins created during the beta, and character creation for the combo was throttled at launch.
- **The racials fit.** Cannibalize returns mana as well as health, which helps the paladin's biggest leveling weakness. Will of the Forsaken covers fear, which paladins otherwise can't escape.

??? spoiler "Lore in brief"

    Forever is set in 25 ADP, right after the Warcraft III campaign *[Forsaken Kingdom](../../world/lore.md)*. Some of the Forsaken were paladins of Lordaeron in life and still answer to the Light, even though it pains their undead bodies. Other Forsaken distrust them deeply, and the only paladins most Forsaken have met are the Scarlet Crusade who hunt them.

    - **Bandarion Keep** sits in the **Whispering Wood**, a previously unreachable strip of western Tirisfal Glades, next to the new town of **Shadowvale**.
    - **Danitha Morr** runs the keep and gives most class quests. One fan guide (ChaosBoost) says she refused to join the Argent Dawn because she still saw the Forsaken as people paladins swore to protect, and that the keep was once an Argent Dawn fortress named for **Garek Bandarion**, a Lordaeron guard turned Deathguard captain. *Unconfirmed; single source.*
    - The pain is a mechanic: in *Rediscovering the Light*, healing others with Holy Light **also damages you**. It was added in a later beta build and is intended.
    - No source names a Forsaken paladin order.

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Will of the Forsaken** <span class="ability-type active">Active, 2 min</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **5/5**{ .stars .s5 }</p>
<p markdown><span class="ability-label">PvE</span> Breaks fear, charm and sleep on bosses that use them</p>
<p markdown><span class="ability-label">PvP</span> Removes Fear, Psychic Scream, Seduction, Sleep and Mind Control. No lasting immunity in Forever. Doesn't work under Scatter Shot</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Cannibalize** <span class="ability-type active">Active, 2 min</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 }</p>
<p markdown><span class="ability-label">PvE</span> Restores 7% health **and mana** every 2 s for 10 s from a humanoid or undead corpse. Big for leveling downtime</p>
<p markdown><span class="ability-label">PvP</span> Out-of-combat recovery between fights. Now usable while immune to physical damage, so Divine Protection or Blessing of Protection won't block it</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Touch of the Grave** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 }</p>
<p markdown><span class="ability-label">PvE</span> 20% chance on melee hits and damaging spells to drain up to 5% of max health, 15 s internal cooldown. Retribution and Protection proc it constantly</p>
<p markdown><span class="ability-label">PvP</span> A free self-heal every 15 s in long fights</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Underwater Breathing** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **1/5**{ .stars .s1 }</p>
<p markdown><span class="ability-label">PvE</span> +300% breath. Handy for the Wolfsbane naga and lumber steps</p>
<p markdown><span class="ability-label">PvP</span> —</p>
</div>

</div>

!!! conflict "Conflict: when Touch of the Grave changed"
    One source dates the cooldown cut (25 s → 15 s) to the 27 October patch; another to the 2 November notes. Both agree it is 15 s at launch. It does not proc from heals.

Undead no longer have Shadow Resistance; Forever removed racial resistances.

??? example "Macros"

    ```
    #showtooltip Will of the Forsaken
    /cast Will of the Forsaken
    /cast Holy Light
    ```

    (Use the second line only if you want to start a heal right after breaking a fear.)

    ```
    #showtooltip Cannibalize
    /cast Cannibalize
    ```

    Eat or drink first, then Cannibalize; the mana return stacks with drinking.

## Starting zone walkthrough (1–12)

You begin at **Deathknell** in Tirisfal Glades. Trainers: **Aramis Hammerhand** in the Deathknell church (31.1, 66.4; trains to level 6), **Shari Stilwell** in Brill (60.3, 52.6), and **Hilda the Breaker** at Bandarion Keep (22.0, 47.2).

<div class="steps" markdown>

1.  **1–4**{ .lvl } Deathknell

    *A Difficult Path* (read the Consecrated Scroll, see Aramis) → *Rediscovering the Light* (heal 5 Injured Deathguards; it hurts you) → *Coming to Terms* (find a Frightened Paladin in the hills west of the chapel). Do the normal Deathknell quests alongside

2.  **4**{ .lvl } Deathknell

    Train **Judgement** and **Blessing of Might**

3.  **4–8**{ .lvl } Brill

    *Continue Your Training* sends you to Shari Stilwell. Do Brill's quests. Train **Holy Strike** and Divine Protection at 6

4.  **8**{ .lvl } Brill

    *A Second Home* (Shari) sends you to **Breton Samuels** at the keep entrance. Train Hammer of Justice

5.  **8–11**{ .lvl } Bandarion Keep

    *Murlocs at the Gates* (8 Vile Fin Attackers, 8 Vile Fin Seers): choose **Skullthumper** (1H mace) or **Driftwood Smasher** (2H mace). *Touring the Grounds* (talk to four residents). *Making Repairs* (12 Sturdy Lumber from Shadowvale) for the Salvaged Wooden Tower Shield

6.  **9–12**{ .lvl } Shadowvale

    *The Tarnished* (Danitha Morr): kill Tarnished Drudges and Zealots and take **Commander Rudolph Gelhardt's** head

7.  **10**{ .lvl } Bandarion Keep

    Train **Seal of Fury, Righteous Fury, Lay on Hands**. First talent point: Benediction (Ret) or Redoubt (Prot)

8.  **10–12**{ .lvl } Undercity

    *A Token of Good Faith*: deliver the head to Sylvanas (Royal Quarter)

9.  **12**{ .lvl } Undercity, Venomweb Vale, keep

    *A Lesson in Divinity* (Danitha): bring 10 Linen Cloth to **Tanis Alderwood** (Trade Quarter), take the **Symbol of Life**, resurrect **Deathguard Falgan** at Venomweb Vale, collect Scarlet Crusade attack plans, report to **Deathguard Billmuth**, then back to Danitha. Reward: **Redemption**

</div>

!!! conflict "Conflicts"
    - *A Second Home* is "level 8" (ForG) or "level 11, available from 8" (ChaosBoost).
    - ForeverDB names the Redemption quest *The Tome of Divinity*, Classic's Alliance name. The two quest-tracking sources call it *A Lesson in Divinity*.
    - Deathguard Billmuth is placed "at the keep" in one source but pinned at 86.6, 47.6, which isn't near the keep. Check your quest map.

!!! tip "No inn at the keep"
    Bandarion Keep has a trainer, a forge and a supply vendor (**Jorin Croge**, 22.6, 44.8) but reportedly no inn, mailbox, bank or auction house. Keep your hearthstone in **Brill**.

## Route to 60

**Trainer access is the main thing to plan.** Horde paladin trainers are only at **Deathknell, Brill and Bandarion Keep**. There is no paladin trainer in Undercity, Orgrimmar or Thunder Bluff (one fan guide lists a "Garen Largo" in the Undercity War Quarter, but the Warcraft Tavern trainer table and ForeverDB have no Undercity paladin trainer; treat it as *unconfirmed*). The Brill trainer is a short run from the Undercity, and the zeppelin tower near Brill links to Orgrimmar and Grom'gol.

<div class="steps" markdown>

1.  **12–20**{ .lvl } Silverpine Forest, the Barrens

    [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) (15–22) above Undercity is your home dungeon; its quests need level 15

2.  **18–26**{ .lvl } Silverpine, Shadowfang Keep, Deadmines, Ashenvale

    **Wolfsbane** chain (below)

3.  **20–30**{ .lvl } Hillsbrad Foothills, Stonetalon, Ashenvale

    Return to Brill to train at even levels

4.  **30–40**{ .lvl } Arathi Highlands, Thousand Needles, Stranglethorn, Desolace; Scarlet Monastery

    SM is in Tirisfal, so you can train at Brill between runs

5.  **40–50**{ .lvl } [Riverglades](../../world/zones.md#riverglades) (Rog'mar), Dustwallow, Tanaris, Feralas, Badlands

    Fly back to Undercity for training

6.  **50–60**{ .lvl } Azshara, Felwood, Un'Goro, Western/Eastern Plaguelands, Winterspring

    The Plaguelands are close to Tirisfal for training

</div>

**Flight paths:** Undercity (Tirisfal), the Sepulcher (Silverpine), Tarren Mill (Hillsbrad), Hammerfall (Arathi), plus the zeppelins from Tirisfal to Orgrimmar and Grom'gol.

### Wolfsbane (18–26)

The Forsaken counterpart of the Alliance's *Verigan's Fist*. Start: **Danitha Morr**, Bandarion Keep (22.0, 44.6), with *Diplomatic Incident* (from level 18).

1. *Diplomatic Incident* → **Trevan Rol** at the Sepulcher (43.4, 41.0).
2. *A Suspicious Pair* → Deathguard Valdred (45.7, 41.8).
3. *A Grim Fate* → a charred body on Fenris Isle (65.0, 34.1).
4. *Into Fenris Keep* → free **Lumina Windsinger** from the keep's prison; *The Windcaller's Fury* escorts her out.
5. *Light*, then *A Moon-Kissed Blade* (from level 20): collect
    - an **Enchanted Silver Ingot** in Arugal's room, Shadowfang Keep;
    - **Whitestone Oak Lumber** from Goblin Woodcarvers in the Deadmines (Horde can swim up from Grom'gol);
    - a **Purified Kor Gem** (*Seeking the Kor Gem*, Ulric Frostveil, Zoram Strand in Ashenvale, 11.9, 34.5; from naga).
6. *An Underrated Talent* and *Ott's Masterpiece*: **Ott** at Tarren Mill (60.4, 26.2) forges the blade.
7. *The Moonsilver Blade*, then *Old Fire-Eye*: kill the elite worgen near the Greymane Wall in southern Silverpine and have Lumina finish **Wolfsbane**.

**Wolfsbane:** two-handed, 3.40 speed, about 25.6 DPS, +9 Stamina, +10 Intellect, with a Holy damage proc that triples against wolves and worgen. A fine Seal of Command weapon. Reportedly also gives Undercity, Orgrimmar and Earthen Ring reputation.

!!! conflict "Conflict: Wolfsbane's level"
    ForG says the chain finishes around level 20; ChaosBoost calls Old Fire-Eye a level-26 elite. The dungeon steps (SFK, Deadmines) suggest low-to-mid 20s is realistic.

## Faction-specific notes

- **Mounts.** The Forsaken **Warhorse** at 40 (*A Trusty Steed* in datamined text) and the **Forsaken Charger** at 60 (*Justice and Retribution* in the beta client) have **no confirmed quest giver or steps**. Bandarion Keep is the likely start. Do **not** run the Alliance mount chain; it is Alliance-only. Fan sources say the Forsaken paladin mounts will come to retail in patch 12.2.0.
- **Skeletal horse** is your Undead racial mount; Apprentice Riding at 40 costs 100g including it.
- **Reputation:** Undercity is your home faction (Honored gives −10% on Riding). The Wolfsbane chain adds Orgrimmar and Earthen Ring reputation.
- **Dalaran:** Horde are attacked on sight in the City of Dalaran zone; skip Kirin Tor quests.
- **No Salvation, no Horde paladin culture yet:** Horde groups may not expect a paladin's blessings. Offer Kings or Wisdom.
- **Scarlet Monastery** is next door and full of rival paladins; the Scarlet chain set reportedly gives bonuses against undead.

## Verdict

<div class="verdict" markdown>

**A strong pick for any role, and the clear choice if you want a Horde paladin.** Cannibalize's mana return and Will of the Forsaken make leveling smoother than on the Alliance side, and the Bandarion Keep story is some of Forever's newest content. The main costs are trainer trips back to Tirisfal and the unconfirmed mount quests. Protection gets the most from Touch of the Grave and the early taunt; Retribution is still the easiest way to level.

</div>
