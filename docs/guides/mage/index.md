---
description: "Mage guide for WoW: Forever: specs and talents, rotations, a 1–60 leveling route, dungeons, raids, PvP, gear and Hardcore tips."
tags:
  - Mage
search:
  boost: 2
---

# Mage Guide

<div class="guide-head" data-class="mage" markdown>

:codex-mage:{ .fc-sigil aria-hidden="true" } <span class="gh-kind">Class guide</span> **DPS**{ .badge .dps }

<nav class="gh-jump" aria-label="Jump to section"><a href="#specs-talents">Talents</a> <a href="#abilities-rotation">Rotation</a> <a href="#leveling-walkthrough-160">Leveling</a> <a href="#dungeons">Dungeons</a> <a href="#raid-preparation">Raids</a> <a href="#pvp">PvP</a> <a href="#gear-stats-enchants">Gear</a> <a href="#hardcore-notes">Hardcore</a></nav>

</div>

!!! info "Current as of 7 November 2026"
    Forever launched on 4 November. This guide uses Blizzard's class deep dive (Oct 2026), the pre-launch development notes (early Nov) and launch-week guides. Talent numbers changed in the last beta builds. Thus, read the in-game tooltip before you spend gold on a respec. Reference data is on the [Mage class page](../../characters/classes/mage.md).

## Overview

The Mage is a ranged caster that wears cloth. The Mage has:

- The best crowd control in the game (Polymorph)
- Strong burst and group AoE
- Utility that no other class has: conjured food and water, teleports and portals, Remove Lesser Curse, Counterspell and Slow Fall

In Forever, Blizzard rebuilt all 3 trees so that each school plays differently. The class also got a cross-school spell and its own minor tradeskill.

<aside class="infobox" markdown>
<p class="infobox-title">Mage at a glance</p>

| | |
|---|---|
| **Role** | Ranged damage, crowd control, utility |
| **Armor / weapons** | Cloth; staves, one-hand swords, daggers, wands, off-hand items |
| **Resource** | **Mana**{ .pill .pill--mana } |
| **Leveling speed** | Third fastest in the beta, after Hunter and Warlock |

</aside>

<div class="proscons" markdown>
<div class="pros" markdown>

Strengths

- Polymorph and Frost Nova kiting
- Burst (Arcane Power, Combustion, Ice Lance shatter)
- Makes its own food and water
- Fast travel

</div>
<div class="cons" markdown>

Weaknesses

- Lowest armor in the game
- Uses much mana
- Weak when an enemy is in melee range or stuns the Mage

</div>
</div>


### What's new in Forever

- **Frostfire Bolt** (level 40, baseline). This spell has a 3 s cast and counts as both Fire and Frost. It gives a large hit, a damage-over-time effect and a slow. It uses your higher spell power of Fire or Frost, against the lower of the target's two resistances. Talents in both trees increase it.
- **Comprehension**, a minor tradeskill for Mages only. *Comprehend Scroll* (General tab of the spellbook) changes scrolls that drop in the world into temporary stat scrolls. Sometimes it gives better items. See [Professions & Legacy](#professions-legacy).
- **New talents:** Arcane Blast and Missile Barrage (Arcane), Heating Up (Fire), Ice Lance and Fingers of Frost (Frost). Ice Block and Cold Snap are now gold-medal talents.
- **New gold-medal tier at 16 points**, together with 11, 21 and 31.
- **Magic Attunement is baseline.** Mage Armor gives more mana regeneration.
- **Nerfs against farming:** Cone of Cold has a shorter duration. Improved Blizzard now slows by a maximum of 40% (it was 65%). Mass AoE pulls still work, but it is less safe to kite large packs.
- **Removed before launch:** Frost Blast and Piercing Ice.
- **Teleport: Dalaran** at level 50: only a fan source (Kami-Labs) reports this. *Unconfirmed.*

### Races

| Race | Faction | Status | Add-on |
|---|---|---|---|
| Human | **Alliance**{ .pill .pill--alliance } | Classic | [Human Mage](human.md) |
| Gnome | **Alliance**{ .pill .pill--alliance } | Classic | [Gnome Mage](gnome.md) |
| Skyborne (High Order) | **Alliance**{ .pill .pill--alliance } | **New** (paid race) | [Skyborne Mage](skyborne-high-order.md) |
| Orc | **Horde**{ .pill .pill--horde } | **New** | [Orc Mage](orc.md) |
| Troll | **Horde**{ .pill .pill--horde } | Classic | [Troll Mage](troll.md) |
| Undead | **Horde**{ .pill .pill--horde } | Classic | [Undead Mage](undead.md) |

!!! conflict "Conflict: best race"
    Warcraft Tavern names Skyborne as the best Alliance Mage and Orc as the best Horde Mage. Method.gg recommends Human or Gnome for Alliance and Orc or Troll for Horde. The differences are small. Choose the race that you will like for a few hundred hours.

## Specs & talents

Talents start at level 10 (or earlier with the *Talented* Legacy talent). At level 60 you have 51 points. Gold-medal talents with 1 point are at **11, 16, 21 and 31** points in a tree. **Dual spec** becomes available at **level 40** for **50g** from all Mage trainers. Respec costs decrease to 1g over time.

=== "Arcane"

    Arcane is now a full damage spec that uses **Arcane Blast**. It is not only a small investment for mana regeneration.

    | Talent | Tier | What it does |
    |---|---|---|
    | Arcane Focus | Early | Now gives spell hit |
    | Improved Channeling | Early | Old name: Improved Arcane Missiles |
    | Arcane Geometry | Row 3 | More range (Kami-Labs says +6 yd) |
    | Arcane Impact | Mid | Crit for Arcane spells |
    | **Arcane Blast** | **11 pts** | 2.5 s cast. Each cast adds a stack of a buff for 18 s. Each stack adds **12% of Intellect as spell damage** and increases the mana cost of Arcane Blast by **100%** |
    | **Missile Barrage** | **16 pts** | Fireball, Frostbolt, Frostfire Bolt and Arcane Blast (at double chance) can make your next Arcane Missiles free and faster |
    | Arcane Mind | Mid | New design that uses Intellect |
    | Arcane Meditation | Mid | Much stronger regeneration while you cast (Warcraft Tavern: up to 50%) |
    | Arcane Resilience | Mid | 3 points, up to 75% of Intellect as armor |
    | Presence of Mind → Arcane Power | Deep | Arcane Power now needs Presence of Mind |

    !!! conflict "Conflict: Arcane Blast numbers"
        The deep dive gave +175% mana per stack, 15% Intellect, 4 stacks and 8–15 s. The pre-launch notes give **+100% mana per stack, 12% Intellect, 18 s**. Use the pre-launch values. In the beta, the Missile Barrage chance was 40% from Arcane Blast and 20% from other bolts.

=== "Fire"

    Fire uses crits. Crits give stacks of **Heating Up**, which makes Pyroblast as fast as a filler spell.

    | Talent | Tier | What it does |
    |---|---|---|
    | Wake of Fire | Row 1 | Shorter Fire Blast cooldown and more crit after a kill |
    | Incineration | Row 1 | 5 points for 10% crit. Also applies to Ice Lance and Arcane Blast |
    | Ignite | Early | Now **per Mage**, so 2 or more Fire Mages do not share one Ignite |
    | Burning Soul | Mid | 3 points; protection against pushback |
    | Improved Scorch | Mid | Debuff that increases Fire damage taken, now **only for your spells** |
    | **Heating Up** | Row 4 | Crits that are not periodic, from Fireball, Frostfire Bolt, Fire Blast or Scorch, decrease the cast time of your next Pyroblast by 25% per stack. Maximum 3 stacks (a 1.5 s Pyroblast) |
    | Blast Wave | Mid | AoE knockback/daze |
    | Critical Mass | Mid | Again 3 points for 6% crit |
    | Combustion | Deep | Now lasts for 4 crits (it was 3) |

    !!! conflict "Conflict: naming"
        The BlizzCon demo and some guides call the proc **Hot Streak**. Blizzard's deep dive and the spell ID call it **Heating Up**. It is one talent.

=== "Frost"

    Frost is a control spec first. Its freeze-and-shatter burst with **Ice Lance** makes it the strongest PvP spec on paper.

    | Talent | Tier | What it does |
    |---|---|---|
    | Elemental Precision | Early | 2/4/6% spell hit for Frost and Fire |
    | Improved Frostbolt, Frostbite, Ice Shards | Early | Same as in Classic |
    | Permafrost | Mid | Chill duration is now a percentage |
    | **Ice Lance** | **11 pts** | Instant. **300%** damage to Frozen targets. Has the same **8 s** cooldown as Fire Blast |
    | **Ice Block** | **16 pts** | Moved to row 4 |
    | **Cold Snap** | **21 pts** | Cooldown increased to **10 min** |
    | Fingers of Frost | Row 5 | Chill effects can make your next spells treat the target as Frozen |
    | Shatter | Mid | 3 points |
    | Winter's Chill | Mid | Debuff that increases Frost crit, now **only for your spells** |
    | Ice Barrier | Deep | Also gives **+15% Frost damage** for 1 min |

    !!! conflict "Conflict: Fingers of Frost"
        Blizzard writes about "charges". Kami-Labs says that it applies to the next **two** spells. Method.gg gives a 15% proc chance for one spell. Expect 15–30% from Chill effects. Read the tooltip.

### Recommended leveling build

Two builds are popular, and both are good. Frost is safer. Arcane kills a little faster per mana when it has its core talents.

=== "Frost (safe, recommended)"

    The talent order comes from the Warcraft Tavern leveling build. The level column is a calculation by this wiki (one point per level from 10, no *Talented* Legacy points). It is not a published table.

    <div class="milestones" markdown>

    Lv 10–16
    :   **7 Arcane**{ .pts } Arcane Concentration and the early Arcane talents. Warcraft Tavern takes these first to get Missile Barrage procs from rank-1 Frostbolt

    Lv 17–27
    :   **11 Frost**{ .pts } Improved Frostbolt, Frostbite, Ice Shards → **Ice Lance** at 27

    Lv 28–32
    :   **16 Frost**{ .pts } Shatter, **Ice Block**

    Lv 33–37
    :   **21 Frost**{ .pts } Fingers of Frost, **Cold Snap**

    Lv 38–60
    :   **rest**{ .pts } Winter's Chill, Ice Barrier, Elemental Precision, Arctic Reach. Put the remaining points back into Arcane

    </div>

    To get Ice Lance at 20, do not take the Arcane points first. Put them in at the end.

    !!! conflict "Conflict: where Missile Barrage is"
        Blizzard's deep dive calls Missile Barrage a **16-point** gold talent. The Warcraft Tavern leveling build gets it with 7 Arcane points. Another guide says that it moved to Arcane tier 2. Look at the in-game tree before you make a plan that uses it.

=== "Arcane (open-world solo)"

    Warcraft Tavern says that an Arcane build is the best open-world solo option. Mobalytics recommends Frost until about level 25, then a respec. Get **Arcane Blast (11)** and **Missile Barrage (16)** first. Then get Arcane Meditation, Arcane Mind, Presence of Mind and Arcane Power. Put the 30 or more remaining points into Frost for Improved Frostbolt, Frostbite and Ice Shards.

!!! tip "Talented"
    Five points in the Legacy talent *Talented* (needs 5/5 *Well Rested*) give your first talent point up to five levels earlier. This is a large early advantage for all Mage alts.

### Endgame builds (level 60)

No source has published tested raid builds. Raids open on 9 December. The builds below follow the talent trees and the priorities that the guides give.

| Build | Points (approx.) | Core | Use |
|---|---|---|---|
| **Deep Arcane** | 31+/x/x | Arcane Blast, Missile Barrage, Arcane Power, Arcane Meditation, plus Frost or Fire for crit/hit | Single-target raid burst, good mana return |
| **Fire** | x/31+/x | Heating Up, Combustion, Critical Mass, Incineration, Ignite (now per Mage) | Raids with few fire-resistant bosses; gets the most from crit |
| **Frost** | x/x/31+ | Ice Lance, Fingers of Frost, Cold Snap, Ice Barrier, Elemental Precision | PvP, Hardcore safety, raids with bosses that are immune to Fire |
| **Frostfire hybrid** | Fire + Frost | Elemental Precision, Ice Shards, Incineration, Heating Up | *Theory, not tested*: talents in both trees increase Frostfire Bolt, and it gives Heating Up procs |

Recommended dual spec at 40: one PvE damage build (Arcane or Fire) and one Frost build for PvP, farming and Hardcore-style safety.

## Abilities & rotation

### Key spells by level (Classic levels, not changed unless noted) { #key-spells-by-level-classic-levels-unchanged-unless-noted }

| Lvl | Spell |
|---|---|
| 1 | Fireball, Frost Armor, Arcane Intellect (now 1 hr, Kami-Labs says) |
| 4 | Frostbolt, Conjure Water |
| 6 | Fire Blast, Conjure Food |
| 8 | Polymorph, Arcane Missiles |
| 10 | Frost Nova |
| 12 | Slow Fall |
| 14 | Arcane Explosion |
| 16 | Flamestrike |
| 18 | Remove Lesser Curse, Amplify Magic |
| 20 | Blink, Blizzard, Evocation, Mana Shield, Fire Ward, **Teleports** (capital cities) |
| 22 | Scorch, Frost Ward |
| 24 | Counterspell |
| 26 | Cone of Cold |
| 28 | Conjure Mana Agate |
| 30 | Ice Armor; teleport to the third capital of your faction |
| 34 | Mage Armor |
| 40 | **Frostfire Bolt** (new), first Portals |
| 50 | **Teleport: Dalaran** (*unconfirmed*) |

### Rotations

=== "Arcane"

    !!! rotation "Arcane priority"

        <div class="priority" markdown>

        1. Cast **Arcane Blast** to get stacks. Each stack also increases the damage of your other spells through Intellect.
        2. Cast **Arcane Missiles** when **Missile Barrage** procs (free and faster).
        3. Cast Arcane Blast on **Clearcasting** (Arcane Concentration) procs. The free cast ignores the stack cost.
        4. Do not cast only Arcane Blast to 4 stacks unless you do burst damage. Cast Frostbolt or Fireball between them, because they also proc Missile Barrage. Let the stacks expire.
        5. Burn phase: Presence of Mind → Arcane Power → Arcane Blast chain, then Evocation.

        </div>


=== "Fire"

    !!! rotation "Fire priority"

        <div class="priority" markdown>

        1. Cast **Pyroblast** before the pull.
        2. Cast **Scorch** until Improved Scorch has 5 stacks. It applies only to your spells, so each Fire Mage keeps a separate debuff.
        3. Cast **Fireball** as filler and **Fire Blast** on cooldown.
        4. At 3 **Heating Up** stacks, cast **Pyroblast** (1.5 s).
        5. Cast **Arcane Missiles** on Missile Barrage if you have the talent.
        6. Use **Combustion** while Heating Up stacks increase, for large crits.

        </div>


=== "Frost"

    !!! rotation "Frost priority"

        <div class="priority" markdown>

        1. Cast **Frostbolt** as your main spell.
        2. Cast **Ice Lance** when the target is Frozen: Frost Nova, Frostbite or a **Fingers of Frost** proc. Remember that it has the same 8 s cooldown as Fire Blast.
        3. If you have no proc and the target is in melee range: **Frost Nova → step back → Ice Lance**.
        4. Cast **Cone of Cold** to kill low-health targets and for AoE, if possible after Winter's Chill has its stacks.
        5. Cast **Frostfire Bolt** (40+) against targets with high Frost resistance, or to slow a target that runs.

        </div>


### Useful macros

??? example "Show 3 macros"

    ```
    #showtooltip Polymorph
    /cast [@focus,exists,harm,nodead][] Polymorph
    ```

    ```
    #showtooltip Counterspell
    /stopcasting
    /cast [@focus,exists,harm][] Counterspell
    ```

    ```
    #showtooltip
    /use Mana Agate
    /use Mana Jade
    /use Mana Citrine
    /use Mana Ruby
    ```

    The client has mouseover and self-cast keys and a Cooldown Manager. Thus, many old macro tricks are now settings.

## Leveling walkthrough 1–60

General rules for all levels:

- Train new ranks of **Conjure Water** and **Conjure Food** when they become available. Drink to full mana between pulls. It costs about **206g** to train all spells from 1 to 60, for all classes.
- Get a **wand** early (Enchanting, quest rewards or the Auction House). In Forever, wand damage increases with spell power.
- A solo kill takes about 10–15 s. Pull one mob at a time until you have Frost Nova and Ice Lance.
- **Quests give much more XP than dungeon mobs.** Do dungeons for their quests, not for boosts.

<div class="route" markdown>

### 1–10


- **Zones:** your starting zone (see each race add-on). Skyborne start on [Zephras Isle](../../world/zephras-isle.md) and stay there until about level 12.
- **Train:** Frostbolt (4), Conjure Water (4), Fire Blast (6), Polymorph and Arcane Missiles (8), Frost Nova (10).
- Do the class letter quest from your first trainer (Classic-era).
- Choose a gathering profession at the starter quest (+2 skill), or start Tailoring immediately.
- Attack with Frostbolt. Use Fire Blast to kill the target.

### 10–20


- **Alliance:** Westfall or Loch Modan. Then go to Darkshore on the new **Stormwind Harbor ↔ Auberdine** boat. Go to Redridge at 16+.
- **Horde:** the Barrens or Silverpine Forest.
- **Skyborne (Alliance):** take the airship to Dalaran, then go to Hillsbrad and the Wetlands (see the add-on).
- **Talents:** first points at 10. See [the leveling build](#recommended-leveling-build).
- **Dungeons:** [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) (13–18, Ironforge), Ragefire Chasm (13–19), [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) (15–22, Tirisfal), Deadmines and Wailing Caverns (17–25).
- **Level 20:** Blink, Evocation, Blizzard, Mana Shield, capital teleports. Turn in **10 library books** for your first book quest.
- At 14, start to look for the **Cozy Sleeping Bag**.

### 20–30


- **Alliance:** Duskwood, Wetlands, Ashenvale, Hillsbrad.
- **Horde:** Stonetalon, Hillsbrad, Ashenvale, Thousand Needles.
- **Dungeons:** Shadowfang Keep, [Excavation Site: Wetlands](../../content/dungeons/excavation-site.md) (24–33), Blackfathom Deeps, the Stockade, [City of Dalaran](../../content/dungeons/city-of-dalaran.md) (28–35, needs the Dalaran Sewer Key).
- **Gear:** Tailoring robes, spell power drops from Excavation Site and Dalaran.
- **Level 25:** first *Mage — Novice* Legacy Point (only for the first Mage on your account).
- On each double pull, use Polymorph on the second mob.

### 30–40


- **Alliance:** Arathi Highlands, Stranglethorn, Desolace, Alterac Mountains (Dalaran is friendly to Alliance).
- **Horde:** Arathi, Stranglethorn, Desolace, Dustwallow. NPCs in Dalaran **attack Horde Mages on sight**.
- **Dungeons:** Razorfen Kraul, Gnomeregan, Scarlet Monastery wings, [The Drowned City](../../content/dungeons/drowned-city.md) (35–42).
- **Level 35:** second library-book quest (20 books). Artisan professions become available.
- **Level 30:** Ice Armor. **34:** Mage Armor (much better regeneration in Forever; use it while you level).
- Battlegrounds from 30: [Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands).

### 40–50


- **Level 40:** **Frostfire Bolt**, **dual spec (50g)**, **riding (100g)**. Save gold from level 30.
- **New zone:** [Riverglades](../../world/zones.md#riverglades) (35–45): Farholde Keep (A) or Rog'mar (H).
- Also: Tanaris, Feralas, Badlands, Swamp of Sorrows, the Hinterlands.
- **Dungeons:** [Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md) (40–47), Uldaman, Zul'Farrak, Razorfen Downs.
- **Level 45:** third library-book quest (25 books) and *Mage — Experienced* Legacy Point.

### 50–60


- **Zones:** Un'Goro, Azshara (many new quests), Felwood, Western/Eastern Plaguelands, Winterspring, Burning Steppes, Silithus.
- **Dungeons:** [Alcaz Prison](../../content/dungeons/alcaz-prison.md) (48–55), Maraudon, Sunken Temple, Blackrock Depths, [Blackmaw Hold](../../content/dungeons/blackmaw-hold.md) (55–60), [Shaper's Terrace](../../content/dungeons/shapers-terrace.md) (58–60).
- **Level 60:** *Mage — Master* Legacy Point. [Mount Hyjal](../../world/zones.md#mount-hyjal) opens through Darkwhisper Gorge in Winterspring.
- Conjure Mana Ruby at 58 (Classic level).

!!! warning "AoE leveling"
    The world-first level-60 group had 3 Mages that used large AoE pulls, so this method still works. But because of the Improved Blizzard and Cone of Cold nerfs, solo kiting of large packs is more dangerous than in Classic. Also, dungeon mobs give less XP. Learn single-target questing first.

</div>

## Dungeons

**Your job:** damage, Polymorph on the marked target, Counterspell on dangerous casters, Remove Lesser Curse, and food and water for the group.

- Set a **focus** on your Polymorph target and use the macros above.
- Do not break Polymorph with AoE. Look before you cast Arcane Explosion or Blizzard.
- When a pull goes wrong, Frost Nova and Blink can save healers.
- Each dungeon has one difficulty and no summoning stones. Only a Warlock's ritual can summon. Bring water for the group.

| Level | Dungeon | Mage notes |
|---|---|---|
| 13–20 | [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) | New; early spell power drops |
| 15–22 | [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) | New; good for Horde, near Tirisfal |
| 24–33 | [Excavation Site](../../content/dungeons/excavation-site.md) | New, short (3 bosses) |
| 28–35 | [City of Dalaran](../../content/dungeons/city-of-dalaran.md) | New, arcane theme; *Violet Sorcerer's Mantle* and *Wand of Mana Concentration* look like Mage items |
| 35–42 | [The Drowned City](../../content/dungeons/drowned-city.md) | New |
| 40–47 | [Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md) | New, in Riverglades |
| 48–55 | [Alcaz Prison](../../content/dungeons/alcaz-prison.md) | New, Dustwallow |
| 55–60 | [Blackmaw Hold](../../content/dungeons/blackmaw-hold.md) | New, Azshara; has an entrance to the Barrow Deeps |
| 58–60 | [Shaper's Terrace](../../content/dungeons/shapers-terrace.md) | New, Un'Goro |

The Classic dungeons (Scholomance, Stratholme, Dire Maul, LBRS, UBRS) are still in the game. Full list: [Dungeons](../../content/dungeons/index.md).

## Raid preparation

All 3 launch raids open on **9 December 2026**. See [Raids](../../content/raids/index.md).

| Raid | Size | Mage notes |
|---|---|---|
| [The Barrow Deeps](../../content/raids/barrow-deeps.md) | 10 | Small raid: you are probably the only Mage, so you give all food, water and curse removal |
| [Hyjal Summit](../../content/raids/hyjal-summit.md) | 20 | 13 bosses, routes that branch; Polymorph and Counterspell jobs are probable |
| [Onyxia's Lair](../../content/raids/onyxias-lair.md) | 40 | Much fire damage: Fire Mages are less useful, Frost or Arcane is the safer choice. Needs the Drakefire Amulet |

**Before 9 December:**

1. **Get spell power first, then hit.** Each tree has a hit talent (Arcane Focus, Elemental Precision). Get the remaining hit from gear.
2. Farm the new level 55+ dungeons (Blackmaw Hold, Shaper's Terrace) and the Classic dungeons (Scholomance, Stratholme, Dire Maul) for spell power cloth. New items have unique stats. Reportedly, each boss in the new dungeons drops a blue item.
3. Tailors: look for the new BoP cloth patterns in Forever.
4. Get a supply of consumables. Classic-era standard items: Greater Arcane Elixir, Elixir of Frost/Shadow Power, Brilliant Wizard Oil, Major Mana Potion, Flask of Supreme Power. No source has documented changes to these items in Forever.
5. Do the Onyxia attunement now. It is not account-wide.

## PvP

- **Frost** is the PvP spec. Ice Lance does 300% damage to Frozen targets, and Fingers of Frost makes freezes more reliable. Ice Block and Cold Snap give you 2 escapes.
- Roots from procs (Frostbite and others) now **share diminishing returns**. Thus, chains of freezes are shorter than in Classic.
- **Polymorph** removes a healer from a fight. Use **Counterspell** on healers and on Warlock fears.
- Battlegrounds: Warsong Gulch, Arathi Basin, Alterac Valley and the new **[Battle for the Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands)** (15v15, from level 30). Mages are strong defenders of flags and nodes.
- See [PvP](../../content/pvp/index.md) for ranks and seasons.

| Matchup | Notes |
|---|---|
| Rogue | Stay out of stealth range; Frost Nova, Blink, Ice Block. Human Perception and Will to Survive help |
| Warrior | Kite: Frost Nova, Cone of Cold, Blink. After you use Blink, do not let the Warrior Charge to you |
| Warlock | Counterspell Fear; Undead *Will of the Forsaken* or Orc *Shatter Curse* removes curses and Banes |
| Priest | Counterspell heals and Mind Control; do burst damage before the Priest applies Power Word: Shield again |
| Hunter | Go into the dead zone (Classic mechanic) or Blink away; use Frost Nova on the pet |
| Other Mages | The first Counterspell wins; keep Ice Block for Polymorph or Pyroblast |

## Gear, stats & enchants

| Spec | Stat priority (Warcraft Tavern, endgame) |
|---|---|
| Arcane | Spell Power > Hit > Haste > Intellect > Crit > Spirit > MP5 |
| Fire | Spell Power > Hit > Crit > Haste > Spirit > MP5 |
| Frost | Spell Power > Hit > Haste > Crit > Intellect > Spirit > MP5 |

- **Leveling:** Intellect and Spirit early (longer fights, less time to drink). Spell power when you can get it.
- It is not known how haste affects Missile Barrage.
- **Enchants:** Classic-era enchants (for example Spell Power on a weapon, Intellect and Stamina on other slots) are still available. The 600+ new recipes in Forever include new options, but sources do not document all of them.
- **Weapon oils:** Minor Wizard Oil is strong early (Method.gg). Oils now stack with class imbues for other classes. Mages have no imbues.

## Professions & Legacy { #professions-legacy }

### Professions

All sources recommend Tailoring for a Mage. Method.gg says that gathering professions are not necessary.

<div class="prof-picks" markdown>

<div class="prof-pick prof-pick--best" markdown>

<p class="prof-rank" markdown>**S**{ .tier .tier-s } Best pick</p>

<p class="prof-pair" markdown>:material-needle: Tailoring <span class="prof-plus">+</span> :material-auto-fix: Enchanting</p>

<p class="prof-for">Best for: Every Mage</p>

<div class="pills" markdown>
**Leveling**{ .pill .pill--success .pill--sm } **Raids**{ .pill .pill--info .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
</dl>

- BoP spell power cloth from about level 10, robes, bags and the reagent bag
- Disenchant your own cloth drops; craft BoP wands
- Warcraft Tavern and Method.gg both recommend it

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Faction Banner (Spirit) · Enchanted Lute (armor, stats, resists)</p>

</div>

<div class="prof-pick prof-pick--alt" markdown>

<p class="prof-rank" markdown>**A**{ .tier .tier-a } Strong alternative</p>

<p class="prof-pair" markdown>:material-leaf: Herbalism <span class="prof-plus">+</span> :material-flask: Alchemy</p>

<p class="prof-for">Best for: Raid consumables</p>

<div class="pills" markdown>
**Raids**{ .pill .pill--info .pill--sm } **Gold**{ .pill .pill--gold .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:100%"><span>5/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:80%"><span>4/5</span></span></dd>
</dl>

- Mana potions and elixirs for raid nights

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Incense Candle (Intellect) · Mana Well (mana regen)</p>

</div>

<div class="prof-pick prof-pick--sit" markdown>

<p class="prof-rank" markdown>**B**{ .tier .tier-b } Situational</p>

<p class="prof-pair" markdown>:material-needle: Tailoring <span class="prof-plus">+</span> :material-cog: Engineering</p>

<p class="prof-for">Best for: PvP</p>

<div class="pills" markdown>
**PvP**{ .pill .pill--danger .pill--sm }
</div>

<dl class="prof-scores">
<dt>Leveling</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>Raids</dt><dd><span class="meter" style="--v:60%"><span>3/5</span></span></dd>
<dt>PvP</dt><dd><span class="meter" style="--v:100%"><span>5/5</span></span></dd>
<dt>Gold</dt><dd><span class="meter" style="--v:40%"><span>2/5</span></span></dd>
</dl>

- Keep Tailoring, and replace Enchanting with PvP gadgets
- Gnomes have 20% fewer device failures

<p class="prof-camp" markdown>:material-campfire: **Camp features:** Faction Banner (Spirit) · Reagent Bot</p>

</div>

</div>

<p class="legend" markdown>Codex ratings out of 5, from the sources above. Compare all classes in [Best professions by class](../../characters/professions.md#best-professions-by-class).</p>

<div class="pills" markdown>
**:material-medical-bag: First Aid · healing potions**{ .pill .pill--success } **:material-pot-steam: Cooking · campfires**{ .pill .pill--info } **:material-fish: Fishing · Fish Bowl**{ .pill .pill--info }
</div>

**Secondary skills.** Cooking, First Aid (which now makes healing potions) and Fishing are all useful.

!!! tip "Race notes"
    **Skyborne:** Read Ley Line already decreases the time between fights while you level. Thus, Tailoring is a better choice than early Alchemy. **Gnome:** best Engineering race.

Crafting professions give [Legacy Points](../../characters/legacy.md) at skill 150, 225 and 300, and each profession adds a [camp feature](../../systems/camping.md). In Forever, professions give no passive stats.

### Comprehension

- A minor tradeskill for Mages only. Warcraft Tavern says that it becomes available at level 6.
- Loot scrolls from creatures. Then use *Comprehend Scroll* to change them into temporary buffs or higher-tier items.
- If a decipher fails, it can change you into a **sheep** until your skill increases (Warcraft Tavern).
- Reportedly, library-book turn-ins gave a *Research* spell that made a Bundle of Scrolls once each hour. A 6 Nov hotfix says that Mages no longer learn the "Research" spell, which disappeared after a relog. It is not known if the spell will return.

### Legacy talents

You can spend up to 16 points per character.

| Tree | Picks for a Mage |
|---|---|
| Adventure | **Well Rested** 5/5 → **Talented** 5/5 for faster leveling; *Thrill of Adventure* decreases the time to drink |
| Resourcefulness | **Reagent Economy** 1/1 removes the reagent cost of teleports, portals and Arcane Brilliance; **Permanence** for long buffs |
| Professions | *Working Overtime* helps skill-ups in Tailoring and Comprehension |

## Hardcore notes

!!! hardcore "Hardcore survival"

    [Hardcore](../../about/hardcore.md) comes in winter 2026/27. Mages die when enemies catch them.

    - Play **Frost**. It has 2 escapes (Ice Block plus a Cold Snap reset) and many slows.
    - Before a pull that you are not sure about, make sure that **Blink, Frost Nova and Ice Block** are not on cooldown.
    - Cast Mana Shield and Ice Barrier before pulls. Evocation is an emergency mana refill, not a damage tool.
    - Use Polymorph on adds. Do not fight more mobs than you can kill. Look for mobs that run away (the slow from Frostfire Bolt helps at 40+).
    - Remember that the Troll *Rapid Regeneration* and Human *Will to Survive* can save your life.

## Common mistakes & FAQ

??? question "Should I level Frost, Arcane or Fire?"
    Frost is the safest, and most guides recommend it. Arcane is strong solo when you have Arcane Blast and Missile Barrage. Fire is the weakest early because it needs crit.

??? question "Why does Arcane Blast use so much mana?"
    Each stack doubles its own cost (+100% per stack). Cast other spells between them and let the stacks expire outside burn phases.

??? question "Why won't my Ice Lance cast?"
    It has the same 8 s cooldown as Fire Blast.

??? question "Can Horde Mages go to Dalaran?"
    NPCs in Dalaran attack Horde characters on sight, and Horde characters cannot get Kirin Tor reputation. They can still go into the City of Dalaran dungeon through the sewer.

??? question "Is AoE farming dead?"
    No, but it is weaker. Improved Blizzard slows by a maximum of 40%, and Cone of Cold is shorter.

- **Mistake:** you forget that the game no longer adds new spells to your bars automatically.
- **Mistake:** you cast low-rank spells for Arcane Concentration, Frostbite or Fingers of Frost procs. Ranks that are more than 12 levels below you have a lower proc chance.
- **Mistake:** you buy dual spec without gold for riding at 40. Plan for 150g+.

## Sources

??? quote "9 sources"

    - [Warcraft Tavern: Mage & Shaman deep dive](https://www.warcrafttavern.com/forever/news/scrolls-totems-mage-shaman-deep-dive-for-wow-forever/)
    - [Warcraft Tavern: Mage leveling guide](https://www.warcrafttavern.com/forever/guides/mage-leveling/)
    - [Warcraft Tavern: Mage guide](https://www.warcrafttavern.com/forever/guides/mage/)
    - [Method.gg: Mage leveling guide and talents](https://www.method.gg/wow-forever/wow-forever-mage-leveling-guide-and-talents)
    - [Kami-Labs: every reworked Mage spell and talent](https://kami-labs.fr/en/wow-forever/mage-wow-forever-sorts-et-talents-modifies/)
    - [Kami-Labs: Ice Lance 8-second cooldown](https://kami-labs.fr/en/wow-forever/mage-wow-forever-changements-28-octobre/)
    - [Mobalytics: Arcane Mage guide](https://mobalytics.gg/wow-forever/classes/arcane-mage-guide)
    - [Mobalytics: Frost AoE leveling guide](https://mobalytics.gg/wow-forever/profile/kargoz/classes/1-60-frost-mage-aoe-leveling-guide-talents-strategy-best-grinding-spots)
    - [Warcraft Tavern: world-first level 60s](https://www.warcrafttavern.com/forever/news/world-first-level-60s-in-wow-forever-paladin-shaman-3-mages/)
