---
tags:
  - Paladin
  - Undead
  - Horde
---

# Undead Paladin

<div class="guide-head" data-class="paladin" markdown>

:codex-paladin:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Add-on</span> **:codex-horde:{ .fc-sigil aria-hidden="true" } Horde**{ .badge .faction } **Tank**{ .badge .tank } **Healer**{ .badge .heal } **DPS**{ .badge .dps }

<p class="gh-note" markdown>Read this page with the [Paladin guide](index.md). This page gives the differences for a Forsaken paladin.</p>

</div>

!!! warning "New combination, little data"
    The Forsaken paladin is **new in Forever**. It is the **only** paladin option for the Horde. Most quest details below come from fan databases that people made during the beta and launch week, and some of them do not agree. This page marks levels and coordinates where sources do not agree.

## Why this combo

- **It is the only way to play a Horde paladin.** Orcs, Trolls, Tauren and Windshaper Skyborne cannot be paladins.
- **It has its own story.** Forsaken paladins get a 10–60 story with its base at **Bandarion Keep** and their own weapon quest (*Wolfsbane*). They also get their own epic mount, which they ride "in the name of **Retribution**". This is the equivalent of the Alliance charger with its Redemption theme.
- **It is popular.** Blizzard counted **612,096** Undead paladins that players made during the beta. At launch, Blizzard limited character creation for this combination.
- **The racials are a good match.** Cannibalize gives back mana and health. This helps with the largest paladin problem while you level. Will of the Forsaken removes fear, and paladins have no other escape from fear.

??? spoiler "Lore in brief"

    Forever is set in 25 ADP, immediately after the Warcraft III campaign *[Forsaken Kingdom](../../world/lore.md)*. In life, some of the Forsaken were paladins of Lordaeron. They still follow the Light, but the Light causes pain to their undead bodies. Many other Forsaken do not trust them. For most Forsaken, the only paladins that they know are the Scarlet Crusade, who hunt them.

    - **Bandarion Keep** is in the **Whispering Wood**, a part of western Tirisfal Glades that players could not go to before. It is near the new town of **Shadowvale**.
    - **Danitha Morr** is the leader of the keep and gives most class quests. One fan guide (ChaosBoost) says that she did not join the Argent Dawn. The reason: she still saw the Forsaken as people that paladins swore to protect. The same guide says that the keep was an Argent Dawn fortress with the name of **Garek Bandarion**, a Lordaeron guard who became a Deathguard captain. *Unconfirmed; one source only.*
    - The pain is a mechanic. In *Rediscovering the Light*, when you heal others with Holy Light, it **also damages you**. Blizzard added this in a later beta build, and it is intentional.
    - No source gives a name for a Forsaken paladin order.

## Racials in practice

<div class="ability-cards" markdown>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Will of the Forsaken** <span class="ability-type active">Active, 2 min</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **5/5**{ .stars .s5 }</p>
<p markdown><span class="ability-label">PvE</span> Breaks fear, charm and sleep from bosses that use them</p>
<p markdown><span class="ability-label">PvP</span> Removes Fear, Psychic Scream, Seduction, Sleep and Mind Control. In Forever it gives no immunity after. It does not work against Scatter Shot</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Cannibalize** <span class="ability-type active">Active, 2 min</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **4/5**{ .stars .s4 }</p>
<p markdown><span class="ability-label">PvE</span> Gives back 7% health **and mana** every 2 s for 10 s, from a humanoid or undead corpse. A large decrease of the time between fights while you level</p>
<p markdown><span class="ability-label">PvP</span> Recovery out of combat between fights. You can now use it while you are immune to physical damage, so Divine Protection or Blessing of Protection do not stop it</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Touch of the Grave** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **3/5**{ .stars .s3 }</p>
<p markdown><span class="ability-label">PvE</span> Melee hits and damage spells have a 20% chance to drain up to 5% of maximum health, with a 15 s internal cooldown. Retribution and Protection proc it all the time</p>
<p markdown><span class="ability-label">PvP</span> A free self-heal every 15 s in long fights</p>
</div>

<div class="ability-card" markdown>
<p class="ability-name" markdown>**Underwater Breathing** <span class="ability-type passive">Passive</span></p>
<p class="ability-rating" markdown><span class="ability-label">Rating</span> **1/5**{ .stars .s1 }</p>
<p markdown><span class="ability-label">PvE</span> +300% breath. Useful for the Wolfsbane naga and lumber steps</p>
<p markdown><span class="ability-label">PvP</span> —</p>
</div>

</div>

!!! conflict "Conflict: when Touch of the Grave changed"
    One source says that the cooldown decrease (25 s → 15 s) came in the 27 October patch. Another source says that it came in the 2 November notes. Both sources agree that it is 15 s at launch. Heals do not proc it.

Undead no longer have Shadow Resistance. Forever removed racial resistances.

??? example "Macros"

    ```
    #showtooltip Will of the Forsaken
    /cast Will of the Forsaken
    /cast Holy Light
    ```

    (Use the second line only if you want to start a heal immediately after you break a fear.)

    ```
    #showtooltip Cannibalize
    /cast Cannibalize
    ```

    Eat or drink first, then use Cannibalize. The mana from Cannibalize stacks with drinking.

## Starting zone walkthrough (1–12)

You start at **Deathknell** in Tirisfal Glades. Trainers: **Aramis Hammerhand** in the Deathknell church (31.1, 66.4; trains until level 6), **Shari Stilwell** in Brill (60.3, 52.6), and **Hilda the Breaker** at Bandarion Keep (22.0, 47.2).

<div class="steps" markdown>

1.  **1–4**{ .lvl } Deathknell

    *A Difficult Path* (read the Consecrated Scroll, talk to Aramis) → *Rediscovering the Light* (heal 5 Injured Deathguards; this damages you) → *Coming to Terms* (find a Frightened Paladin in the hills west of the chapel). Also do the usual Deathknell quests

2.  **4**{ .lvl } Deathknell

    Train **Judgement** and **Blessing of Might**

3.  **4–8**{ .lvl } Brill

    *Continue Your Training* sends you to Shari Stilwell. Do the Brill quests. Train **Holy Strike** and Divine Protection at 6

4.  **8**{ .lvl } Brill

    *A Second Home* (Shari) sends you to **Breton Samuels** at the keep entrance. Train Hammer of Justice

5.  **8–11**{ .lvl } Bandarion Keep

    *Murlocs at the Gates* (8 Vile Fin Attackers, 8 Vile Fin Seers): choose **Skullthumper** (1H mace) or **Driftwood Smasher** (2H mace). *Touring the Grounds*: talk to 4 residents. *Making Repairs*: get 12 Sturdy Lumber from Shadowvale for the Salvaged Wooden Tower Shield

6.  **9–12**{ .lvl } Shadowvale

    *The Tarnished* (Danitha Morr): kill Tarnished Drudges and Zealots and take the head of **Commander Rudolph Gelhardt**

7.  **10**{ .lvl } Bandarion Keep

    Train **Seal of Fury, Righteous Fury, Lay on Hands**. First talent point: Benediction (Ret) or Redoubt (Prot)

8.  **10–12**{ .lvl } Undercity

    *A Token of Good Faith*: give the head to Sylvanas (Royal Quarter)

9.  **12**{ .lvl } Undercity, Venomweb Vale, keep

    *A Lesson in Divinity* (Danitha): bring 10 Linen Cloth to **Tanis Alderwood** (Trade Quarter) and take the **Symbol of Life**. Resurrect **Deathguard Falgan** at Venomweb Vale. Get the Scarlet Crusade attack plans and report to **Deathguard Billmuth**. Then go back to Danitha. Reward: **Redemption**

</div>

!!! conflict "Conflicts"
    - *A Second Home* is "level 8" (ForG) or "level 11, available from 8" (ChaosBoost).
    - ForeverDB gives the Redemption quest the name *The Tome of Divinity*, which is the Alliance name from Classic. The two quest-tracking sources call it *A Lesson in Divinity*.
    - One source puts Deathguard Billmuth "at the keep", but it gives the coordinates 86.6, 47.6, which are not near the keep. Look at your quest map.

!!! tip "No inn at the keep"
    Bandarion Keep has a trainer, a forge and a supply vendor (**Jorin Croge**, 22.6, 44.8). Reportedly, it has no inn, mailbox, bank or auction house. Set your hearthstone in **Brill**.

## Route to 60

**The most important thing to plan is access to trainers.** Horde paladin trainers are only at **Deathknell, Brill and Bandarion Keep**. There is no paladin trainer in Undercity, Orgrimmar or Thunder Bluff. One fan guide gives a "Garen Largo" in the Undercity War Quarter. But the Warcraft Tavern trainer table and ForeverDB have no Undercity paladin trainer, so this is *unconfirmed*. The Brill trainer is a short run from the Undercity. The zeppelin tower near Brill has zeppelins to Orgrimmar and Grom'gol.

<div class="steps" markdown>

1.  **12–20**{ .lvl } Silverpine Forest, the Barrens

    [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) (15–22), above Undercity, is your home dungeon. Its quests need level 15

2.  **18–26**{ .lvl } Silverpine, Shadowfang Keep, Deadmines, Ashenvale

    **Wolfsbane** chain (below)

3.  **20–30**{ .lvl } Hillsbrad Foothills, Stonetalon, Ashenvale

    Go back to Brill to train at even levels

4.  **30–40**{ .lvl } Arathi Highlands, Thousand Needles, Stranglethorn, Desolace; Scarlet Monastery

    SM is in Tirisfal, so you can train at Brill between runs

5.  **40–50**{ .lvl } [Riverglades](../../world/zones.md#riverglades) (Rog'mar), Dustwallow, Tanaris, Feralas, Badlands

    Fly back to Undercity to train

6.  **50–60**{ .lvl } Azshara, Felwood, Un'Goro, Western/Eastern Plaguelands, Winterspring

    The Plaguelands are near Tirisfal, so it is easy to go back to train

</div>

**Flight paths:** Undercity (Tirisfal), the Sepulcher (Silverpine), Tarren Mill (Hillsbrad), Hammerfall (Arathi), and the zeppelins from Tirisfal to Orgrimmar and Grom'gol.

### Wolfsbane (18–26)

This is the Forsaken equivalent of the Alliance quest *Verigan's Fist*. Start: **Danitha Morr**, Bandarion Keep (22.0, 44.6), with *Diplomatic Incident* (from level 18).

1. *Diplomatic Incident* → **Trevan Rol** at the Sepulcher (43.4, 41.0).
2. *A Suspicious Pair* → Deathguard Valdred (45.7, 41.8).
3. *A Grim Fate* → a burned body on Fenris Isle (65.0, 34.1).
4. *Into Fenris Keep* → release **Lumina Windsinger** from the prison of the keep. In *The Windcaller's Fury*, escort her out.
5. *Light*, then *A Moon-Kissed Blade* (from level 20). Get these items:
    - an **Enchanted Silver Ingot** in Arugal's room, Shadowfang Keep;
    - **Whitestone Oak Lumber** from Goblin Woodcarvers in the Deadmines (Horde can swim there from Grom'gol);
    - a **Purified Kor Gem** (*Seeking the Kor Gem*, Ulric Frostveil, Zoram Strand in Ashenvale, 11.9, 34.5; from naga).
6. *An Underrated Talent* and *Ott's Masterpiece*: **Ott** at Tarren Mill (60.4, 26.2) makes the blade.
7. *The Moonsilver Blade*, then *Old Fire-Eye*: kill the elite worgen near the Greymane Wall in southern Silverpine. Then Lumina completes **Wolfsbane**.

**Wolfsbane:** two-hand, 3.40 speed, about 25.6 DPS, +9 Stamina, +10 Intellect. It has a Holy damage proc that does 3 times the damage against wolves and worgen. It is a good Seal of Command weapon. Reportedly, the chain also gives Undercity, Orgrimmar and Earthen Ring reputation.

!!! conflict "Conflict: Wolfsbane's level"
    ForG says that the chain ends at about level 20. ChaosBoost says that Old Fire-Eye is a level 26 elite. Because of the dungeon steps (SFK, Deadmines), a level in the low to middle 20s is realistic.

## Faction-specific notes

- **Mounts.** The Forsaken **Warhorse** at 40 (*A Trusty Steed* in datamined text) and the **Forsaken Charger** at 60 (*Justice and Retribution* in the beta client) have **no confirmed quest giver or steps**. The start is probably at Bandarion Keep. Do **not** do the Alliance mount chain. It is Alliance-only. Fan sources say that the Forsaken paladin mounts will come to retail in patch 12.2.0.
- **Skeletal horse:** this is your Undead racial mount. Apprentice Riding at 40 costs 100g, and this cost includes the horse.
- **Reputation:** Undercity is your home faction (Honored gives −10% on Riding). The Wolfsbane chain adds Orgrimmar and Earthen Ring reputation.
- **Dalaran:** NPCs in the City of Dalaran zone attack Horde on sight. Do not do the Kirin Tor quests.
- **No Salvation, and no Horde paladin culture yet:** Horde groups possibly do not expect paladin blessings. Offer Kings or Wisdom.
- **Scarlet Monastery** is near and has many enemy paladins. Reportedly, the Scarlet chain set gives bonuses against undead.

## Verdict

<div class="verdict" markdown>

**A strong choice for all roles, and the only choice if you want a Horde paladin.** Because of the mana from Cannibalize and Will of the Forsaken, leveling is easier than on the Alliance side. The Bandarion Keep story is some of the newest content in Forever. The main disadvantages are the trips back to Tirisfal to train and the mount quests that are not confirmed. Protection gets the most from Touch of the Grave and the early taunt. Retribution is still the easiest way to level.

</div>
