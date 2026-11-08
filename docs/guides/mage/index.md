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
    Forever launched on 4 November. This guide follows Blizzard's class deep dive (Oct 2026), the pre-launch development notes (early Nov) and launch-week guides. Talent numbers were still moving in the last beta builds, so check the in-game tooltip before you commit gold to a respec. Reference data lives on the [Mage class page](../../characters/classes/mage.md).

## Overview

The Mage is a cloth-wearing ranged caster: the best crowd control in the game (Polymorph), strong burst, group AoE, and a toolkit of utility nobody else has (conjured food and water, teleports and portals, Remove Lesser Curse, Counterspell, Slow Fall). In Forever all three trees were rebuilt so that each school plays differently, and the class gained a cross-school spell and its own minor tradeskill.

<aside class="infobox" markdown>
<p class="infobox-title">Mage at a glance</p>

| | |
|---|---|
| **Role** | Ranged damage, crowd control, utility |
| **Armor / weapons** | Cloth; staves, one-hand swords, daggers, wands, off-hand items |
| **Resource** | **Mana**{ .pill .pill--mana } |
| **Strengths** | Polymorph and Frost Nova kiting, burst (Arcane Power, Combustion, Ice Lance shatter), self-sufficient food and water, fast travel |
| **Weaknesses** | Lowest armor in the game, mana-hungry, vulnerable when caught in melee or stunned |
| **Leveling speed** | Third fastest in the beta, behind Hunter and Warlock |

</aside>

### What's new in Forever

- **Frostfire Bolt** (level 40, baseline). A 3 s cast that counts as both Fire and Frost: a large hit plus a damage-over-time and a slow. It uses whichever of your Fire or Frost spell power is higher, against whichever of the target's two resistances is lower. It benefits from talents in both trees.
- **Comprehension**, a Mage-only minor tradeskill. *Comprehend Scroll* (General tab of the spellbook) deciphers scrolls dropped in the world into temporary stat scrolls and sometimes better items. See [Professions & Legacy](#professions-legacy).
- **New talents:** Arcane Blast and Missile Barrage (Arcane), Heating Up (Fire), Ice Lance and Fingers of Frost (Frost). Ice Block and Cold Snap became gold-medal talents.
- **New gold-medal tier at 16 points**, alongside 11, 21 and 31.
- **Magic Attunement is baseline.** Mage Armor regenerates more mana.
- **Anti-farming nerfs:** Cone of Cold lasts less time, and Improved Blizzard now slows by at most 40% (was 65%). Mass AoE pulls still work, but kiting large packs is less forgiving.
- **Removed before launch:** Frost Blast and Piercing Ice.
- **Teleport: Dalaran** at level 50 is reported by a fan source (Kami-Labs) only. *Unconfirmed.*

### Races

| Race | Faction | Status | Add-on |
|---|---|---|---|
| Human | Alliance | Classic | [Human Mage](human.md) |
| Gnome | Alliance | Classic | [Gnome Mage](gnome.md) |
| Skyborne (High Order) | Alliance | **New** (paid race) | [Skyborne Mage](skyborne-high-order.md) |
| Orc | Horde | **New** | [Orc Mage](orc.md) |
| Troll | Horde | Classic | [Troll Mage](troll.md) |
| Undead | Horde | Classic | [Undead Mage](undead.md) |

!!! conflict "Conflict: best race"
    Warcraft Tavern names Skyborne as the best Alliance Mage and Orc as the best Horde Mage. Method.gg suggests Human or Gnome for Alliance and Orc or Troll for Horde. The differences are small; pick the race you'll enjoy for a few hundred hours.

## Specs & talents

Talents start at level 10 (or earlier with the *Talented* Legacy talent) and you have 51 points at 60. Gold-medal single-point talents sit at **11, 16, 21 and 31** points in a tree. **Dual spec** unlocks at **level 40** for **50g** from any Mage trainer; respec fees decay to 1g over time.

=== "Arcane"

    Arcane is now a stand-alone damage spec built on **Arcane Blast**, not just a mana-regen dip.

    | Talent | Tier | What it does |
    |---|---|---|
    | Arcane Focus | Early | Now grants spell hit |
    | Improved Channeling | Early | Renamed Improved Arcane Missiles |
    | Arcane Geometry | Row 3 | Extra range (Kami-Labs says +6 yd) |
    | Arcane Impact | Mid | Crit for Arcane spells |
    | **Arcane Blast** | **11 pts** | 2.5 s cast. Each cast stacks a buff that adds **12% of Intellect as spell damage** and raises Arcane Blast's own mana cost by **100%**, for 18 s |
    | **Missile Barrage** | **16 pts** | Fireball, Frostbolt, Frostfire Bolt and (at double chance) Arcane Blast can make your next Arcane Missiles free and channel faster |
    | Arcane Mind | Mid | Redesigned around Intellect |
    | Arcane Meditation | Mid | Much stronger casting regen (Warcraft Tavern: up to 50%) |
    | Arcane Resilience | Mid | 3 points, up to 75% of Intellect as armor |
    | Presence of Mind → Arcane Power | Deep | Arcane Power now requires Presence of Mind |

    !!! conflict "Conflict: Arcane Blast numbers"
        The deep dive described +175% mana per stack, 15% Intellect, 4 stacks and 8–15 s. The pre-launch notes set **+100% mana per stack, 12% Intellect, 18 s**. Use the pre-launch values. Missile Barrage chance was 40% from Arcane Blast and 20% from other bolts in beta.

=== "Fire"

    Fire is crit-driven. Crits feed **Heating Up**, which turns Pyroblast into a filler-speed nuke.

    | Talent | Tier | What it does |
    |---|---|---|
    | Wake of Fire | Row 1 | Shorter Fire Blast cooldown and a crit boost after a kill |
    | Incineration | Row 1 | 5 points for 10% crit; also covers Ice Lance and Arcane Blast |
    | Ignite | Early | Now tracked **per Mage**, so several Fire Mages no longer fight over one Ignite |
    | Burning Soul | Mid | 3 points; pushback protection |
    | Improved Scorch | Mid | Fire vulnerability debuff, now **self-only** |
    | **Heating Up** | Row 4 | Non-periodic crits from Fireball, Frostfire Bolt, Fire Blast or Scorch cut your next Pyroblast's cast by 25% per stack, up to 3 (a 1.5 s Pyroblast) |
    | Blast Wave | Mid | AoE knockback/daze |
    | Critical Mass | Mid | Reverted to 3 points for 6% crit |
    | Combustion | Deep | Now lasts 4 crits (was 3) |

    !!! conflict "Conflict: naming"
        The BlizzCon demo and some guides call the proc **Hot Streak**. Blizzard's deep dive and the spell ID call it **Heating Up**. It is one talent.

=== "Frost"

    Frost is control first, and the freeze-and-shatter burst of **Ice Lance** makes it the strongest PvP spec on paper.

    | Talent | Tier | What it does |
    |---|---|---|
    | Elemental Precision | Early | 2/4/6% spell hit for Frost and Fire |
    | Improved Frostbolt, Frostbite, Ice Shards | Early | As in Classic |
    | Permafrost | Mid | Chill duration now percentage-based |
    | **Ice Lance** | **11 pts** | Instant. **300%** damage to Frozen targets. Shares an **8 s** cooldown with Fire Blast |
    | **Ice Block** | **16 pts** | Moved to row 4 |
    | **Cold Snap** | **21 pts** | Cooldown raised to **10 min** |
    | Fingers of Frost | Row 5 | Chill effects can make your next spells treat the target as Frozen |
    | Shatter | Mid | 3 points |
    | Winter's Chill | Mid | Frost crit debuff, now **self-only** |
    | Ice Barrier | Deep | Also grants **+15% Frost damage** for 1 min |

    !!! conflict "Conflict: Fingers of Frost"
        Blizzard describes "charges". Kami-Labs says the next **two** spells; Method.gg gives a 15% proc chance and says one spell. Expect 15–30% from Chill effects; read the tooltip.

### Recommended leveling build

Two approaches are popular. Both are fine; Frost is safer, Arcane kills a little faster per mana once it comes online.

=== "Frost (safe, recommended)"

    Talent order from Warcraft Tavern's leveling build; the level column is this wiki's arithmetic (one point per level from 10, no *Talented* Legacy points), not a published table.

    <div class="milestones" markdown>

    Lv 10–16
    :   **7 Arcane**{ .pts } Arcane Concentration and the early Arcane path; Warcraft Tavern takes these first for Missile Barrage procs from rank-1 Frostbolt

    Lv 17–27
    :   **11 Frost**{ .pts } Improved Frostbolt, Frostbite, Ice Shards → **Ice Lance** at 27

    Lv 28–32
    :   **16 Frost**{ .pts } Shatter, **Ice Block**

    Lv 33–37
    :   **21 Frost**{ .pts } Fingers of Frost, **Cold Snap**

    Lv 38–60
    :   **rest**{ .pts } Winter's Chill, Ice Barrier, Elemental Precision, Arctic Reach; leftover points back into Arcane

    </div>

    If you'd rather have Ice Lance at 20, skip the Arcane points and put them in at the end.

    !!! conflict "Conflict: where Missile Barrage sits"
        Blizzard's deep dive labels Missile Barrage a **16-point** gold talent. Warcraft Tavern's leveling build reaches it with 7 Arcane points, and another guide says it moved to Arcane tier 2. Check the in-game tree before planning around it.

=== "Arcane (open-world solo)"

    Warcraft Tavern rates an Arcane build as the best open-world solo option; Mobalytics suggests leveling Frost to about 25 and respeccing. Rush **Arcane Blast (11)** and **Missile Barrage (16)**, then Arcane Meditation, Arcane Mind, Presence of Mind and Arcane Power. The 30-odd remaining points go into Frost for Improved Frostbolt, Frostbite and Ice Shards.

!!! tip "Talented"
    Five points of the Legacy talent *Talented* (requires 5/5 *Well Rested*) give your first talent point up to five levels earlier. That's a big early boost for any Mage alt.

### Endgame builds (level 60)

No source has published tested raid builds yet; raids open on 9 December. The shapes below follow the talent trees and the guides' stated priorities.

| Build | Points (approx.) | Core | Use |
|---|---|---|---|
| **Deep Arcane** | 31+/x/x | Arcane Blast, Missile Barrage, Arcane Power, Arcane Meditation, plus Frost or Fire for crit/hit | Single-target raid burst, strong mana return |
| **Fire** | x/31+/x | Heating Up, Combustion, Critical Mass, Incineration, Ignite (now per Mage) | Raids with fire-light bosses; scales hardest with crit |
| **Frost** | x/x/31+ | Ice Lance, Fingers of Frost, Cold Snap, Ice Barrier, Elemental Precision | PvP, Hardcore safety, raids with Fire-immune bosses |
| **Frostfire hybrid** | Fire + Frost | Elemental Precision, Ice Shards, Incineration, Heating Up | *Untested theory*: Frostfire Bolt benefits from both trees and procs Heating Up |

Suggested dual spec at 40: one PvE damage build (Arcane or Fire) and one Frost build for PvP, farming and Hardcore-style safety.

## Abilities & rotation

### Key spells by level (Classic levels, unchanged unless noted)

| Lvl | Spell |
|---|---|
| 1 | Fireball, Frost Armor, Arcane Intellect (now 1 hr per Kami-Labs) |
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
| 30 | Ice Armor; teleport to your faction's third capital |
| 34 | Mage Armor |
| 40 | **Frostfire Bolt** (new), Portals begin |
| 50 | **Teleport: Dalaran** (*unconfirmed*) |

### Rotations

=== "Arcane"

    !!! rotation "Arcane priority"

        <div class="priority" markdown>

        1. **Arcane Blast** to build stacks (each stack also raises your other spells' damage via Intellect).
        2. **Arcane Missiles** whenever **Missile Barrage** procs (free and faster).
        3. Cast Arcane Blast on **Clearcasting** (Arcane Concentration) procs — the free cast ignores the stack cost.
        4. Don't spam Arcane Blast to 4 stacks unless you're bursting: weave Frostbolt or Fireball, which also proc Missile Barrage, and let the stacks fall off.
        5. Burn phase: Presence of Mind → Arcane Power → Arcane Blast chain, then Evocation.

        </div>


=== "Fire"

    !!! rotation "Fire priority"

        <div class="priority" markdown>

        1. Pre-pull **Pyroblast**.
        2. **Scorch** until Improved Scorch is at 5 stacks (self-only, so every Fire Mage keeps their own).
        3. **Fireball** as filler, **Fire Blast** on cooldown.
        4. At **3 Heating Up** stacks, cast **Pyroblast** (1.5 s).
        5. **Arcane Missiles** on Missile Barrage if you took it.
        6. **Combustion** with Heating Up stacks building for the big crits.

        </div>


=== "Frost"

    !!! rotation "Frost priority"

        <div class="priority" markdown>

        1. **Frostbolt** as your main spell.
        2. **Ice Lance** whenever the target is Frozen: Frost Nova, Frostbite or a **Fingers of Frost** proc. Remember the shared 8 s cooldown with Fire Blast.
        3. If nothing has procced in melee range: **Frost Nova → step back → Ice Lance**.
        4. **Cone of Cold** for finishing and AoE, ideally once Winter's Chill is stacked.
        5. **Frostfire Bolt** (40+) against Frost-resistant targets, or as a slow on a runner.

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

    The client has built-in mouseover and self-cast keys and a Cooldown Manager, so many old macro tricks are now settings.

## Leveling walkthrough 1–60

General rules for the whole trip:

- Keep **Conjure Water** and **Conjure Food** ranks current; drink to full between pulls. Training every spell 1–60 costs about **206g** for any class.
- Get a **wand** early (Enchanting, quest rewards or the Auction House). Wands scale with spell power in Forever.
- Mobs take about 10–15 s to kill solo. Pull one at a time until you have Frost Nova and Ice Lance.
- **Quests give much more XP than dungeon mobs.** Run dungeons with their quests, not for boosting.

<div class="route" markdown>

### 1–10


- **Zones:** your starting zone (see each race add-on). Skyborne start on [Zephras Isle](../../world/zephras-isle.md) and stay there to about 12.
- **Train:** Frostbolt (4), Conjure Water (4), Fire Blast (6), Polymorph and Arcane Missiles (8), Frost Nova (10).
- Do the class letter quest from your first trainer (Classic-era).
- Pick a gathering profession at the starter quest (+2 skill) or start Tailoring right away.
- Fight with Frostbolt; finish with Fire Blast.

### 10–20


- **Alliance:** Westfall or Loch Modan, then Darkshore by the new **Stormwind Harbor ↔ Auberdine** boat; Redridge at 16+.
- **Horde:** the Barrens or Silverpine Forest.
- **Skyborne (Alliance):** airship to Dalaran, then route into Hillsbrad and the Wetlands (see the add-on).
- **Talents:** first points at 10. See [the leveling build](#recommended-leveling-build).
- **Dungeons:** [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) (13–18, Ironforge), Ragefire Chasm (13–19), [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) (15–22, Tirisfal), Deadmines and Wailing Caverns (17–25).
- **Level 20:** Blink, Evocation, Blizzard, Mana Shield, capital teleports. Turn in **10 library books** for your first book quest.
- Start the **Cozy Sleeping Bag** hunt at 14.

### 20–30


- **Alliance:** Duskwood, Wetlands, Ashenvale, Hillsbrad.
- **Horde:** Stonetalon, Hillsbrad, Ashenvale, Thousand Needles.
- **Dungeons:** Shadowfang Keep, [Excavation Site: Wetlands](../../content/dungeons/excavation-site.md) (24–33), Blackfathom Deeps, the Stockade, [City of Dalaran](../../content/dungeons/city-of-dalaran.md) (28–35, needs the Dalaran Sewer Key).
- **Gear:** Tailoring robes, Excavation Site and Dalaran spell power drops.
- **Level 25:** first *Mage — Novice* Legacy Point (first Mage on your account only).
- Use Polymorph on the second mob of every double pull.

### 30–40


- **Alliance:** Arathi Highlands, Stranglethorn, Desolace, Alterac Mountains (Dalaran is Alliance-friendly).
- **Horde:** Arathi, Stranglethorn, Desolace, Dustwallow. Horde Mages are **attacked on sight in Dalaran**.
- **Dungeons:** Razorfen Kraul, Gnomeregan, Scarlet Monastery wings, [The Drowned City](../../content/dungeons/drowned-city.md) (35–42).
- **Level 35:** second library-book quest (20 books). Artisan professions open.
- **Level 30:** Ice Armor. **34:** Mage Armor (much better regen in Forever; use it when leveling).
- Battlegrounds from 30: [Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands).

### 40–50


- **Level 40:** **Frostfire Bolt**, **dual spec (50g)**, **riding (100g)**. Save gold from 30 onward.
- **New zone:** [Riverglades](../../world/zones.md#riverglades) (35–45): Farholde Keep (A) or Rog'mar (H).
- Also: Tanaris, Feralas, Badlands, Swamp of Sorrows, the Hinterlands.
- **Dungeons:** [Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md) (40–47), Uldaman, Zul'Farrak, Razorfen Downs.
- **Level 45:** third library-book quest (25 books) and *Mage — Experienced* Legacy Point.

### 50–60


- **Zones:** Un'Goro, Azshara (many new quests), Felwood, Western/Eastern Plaguelands, Winterspring, Burning Steppes, Silithus.
- **Dungeons:** [Alcaz Prison](../../content/dungeons/alcaz-prison.md) (48–55), Maraudon, Sunken Temple, Blackrock Depths, [Blackmaw Hold](../../content/dungeons/blackmaw-hold.md) (55–60), [Shaper's Terrace](../../content/dungeons/shapers-terrace.md) (58–60).
- **Level 60:** *Mage — Master* Legacy Point; [Mount Hyjal](../../world/zones.md#mount-hyjal) opens through Darkwhisper Gorge in Winterspring.
- Conjure Mana Ruby at 58 (Classic level).

!!! warning "AoE leveling"
    The world-first level-60 group included three Mages using big AoE pulls, so it still works. But the Improved Blizzard and Cone of Cold nerfs make solo kiting of huge packs riskier than in Classic, and dungeon mobs give less XP. Learn single-target questing first.

</div>

## Dungeons

**Your job:** damage, Polymorph on the marked target, Counterspell on dangerous casters, Remove Lesser Curse, and food and water for the group.

- Set a **focus** on your sheep target and use the macros above.
- Don't break Polymorph with AoE. Check before you Arcane Explosion or Blizzard.
- Frost Nova and Blink save healers when a pull goes wrong.
- One difficulty per dungeon, no summoning stones — a Warlock's ritual is the only summon. Bring water for the group.

| Level | Dungeon | Mage notes |
|---|---|---|
| 13–20 | [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) | New; early spell power drops |
| 15–22 | [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) | New; Horde-friendly, near Tirisfal |
| 24–33 | [Excavation Site](../../content/dungeons/excavation-site.md) | New, short (3 bosses) |
| 28–35 | [City of Dalaran](../../content/dungeons/city-of-dalaran.md) | New, arcane theme; *Violet Sorcerer's Mantle* and *Wand of Mana Concentration* look made for Mages |
| 35–42 | [The Drowned City](../../content/dungeons/drowned-city.md) | New |
| 40–47 | [Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md) | New, in Riverglades |
| 48–55 | [Alcaz Prison](../../content/dungeons/alcaz-prison.md) | New, Dustwallow |
| 55–60 | [Blackmaw Hold](../../content/dungeons/blackmaw-hold.md) | New, Azshara; leads to a Barrow Deeps entrance |
| 58–60 | [Shaper's Terrace](../../content/dungeons/shapers-terrace.md) | New, Un'Goro |

Classic dungeons (Scholomance, Stratholme, Dire Maul, LBRS, UBRS) remain. Full list: [Dungeons](../../content/dungeons/index.md).

## Raid preparation

All three launch raids open on **9 December 2026**. See [Raids](../../content/raids/index.md).

| Raid | Size | Mage notes |
|---|---|---|
| [The Barrow Deeps](../../content/raids/barrow-deeps.md) | 10 | Small raid: you are likely the only Mage, so you supply all food, water and curse removal |
| [Hyjal Summit](../../content/raids/hyjal-summit.md) | 20 | 13 bosses, branching routes; Polymorph and Counterspell jobs likely |
| [Onyxia's Lair](../../content/raids/onyxias-lair.md) | 40 | Heavy fire damage: Fire Mages lose value, Frost or Arcane is the safer choice. Needs the Drakefire Amulet |

**Before 9 December:**

1. **Spell power first, then hit.** Each tree has a hit talent (Arcane Focus, Elemental Precision); fill the rest from gear.
2. Farm the new level-55+ dungeons (Blackmaw Hold, Shaper's Terrace) and classic ones (Scholomance, Stratholme, Dire Maul) for spell power cloth. New items carry unique stats and every new-dungeon boss reportedly drops a blue.
3. Tailors: look for Forever's new BoP cloth patterns.
4. Stock consumables. Classic-era staples: Greater Arcane Elixir, Elixir of Frost/Shadow Power, Brilliant Wizard Oil, Major Mana Potion, Flask of Supreme Power. Forever's changes to these haven't been documented.
5. Do the Onyxia attunement now; it isn't account-wide.

## PvP

- **Frost** is the PvP spec: Ice Lance hits 300% on Frozen targets, Fingers of Frost makes freezes more reliable, Ice Block and Cold Snap give you two escapes.
- Proc roots (Frostbite and others) now **share diminishing returns**, so chain-freezing isn't as long as in Classic.
- **Polymorph** removes a healer from a fight. **Counterspell** on healers and Warlock fears.
- Battlegrounds: Warsong Gulch, Arathi Basin, Alterac Valley and the new **[Battle for the Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands)** (15v15, from level 30). Mages are strong flag defenders and node defenders.
- See [PvP](../../content/pvp/index.md) for ranks and seasons.

| Matchup | Notes |
|---|---|
| Rogue | Stay out of stealth range; Frost Nova, Blink, Ice Block. Humans' Perception and Will to Survive help |
| Warrior | Kite: Frost Nova, Cone of Cold, Blink. Don't let them reach you with Charge after Blink is down |
| Warlock | Counterspell Fear; Undead *Will of the Forsaken* or an Orc *Shatter Curse* removes curses and Banes |
| Priest | Counterspell heals and Mind Control; burst before Power Word: Shield is reapplied |
| Hunter | Get into the dead zone (Classic mechanic) or Blink away; Frost Nova the pet |
| Other Mages | Counterspell first wins; save Ice Block for Polymorph or Pyroblast |

## Gear, stats & enchants

| Spec | Stat priority (Warcraft Tavern, endgame) |
|---|---|
| Arcane | Spell Power > Hit > Haste > Intellect > Crit > Spirit > MP5 |
| Fire | Spell Power > Hit > Crit > Haste > Spirit > MP5 |
| Frost | Spell Power > Hit > Haste > Crit > Intellect > Spirit > MP5 |

- **Leveling:** Intellect and Spirit early (longer fights, less drinking), spell power once you can get it.
- How haste interacts with Missile Barrage is not yet known.
- **Enchants:** Classic-era ones (e.g. Spell Power on weapon, Intellect and Stamina elsewhere) remain; Forever's 600+ new recipes include new options that aren't fully documented.
- **Weapon oils:** Minor Wizard Oil is strong early (Method.gg). Oils now stack with class imbues for other classes; Mages have none.

## Professions & Legacy { #professions-legacy }

### Professions

| Pick | Why |
|---|---|
| **Tailoring** | BoP cloth with spell power from about level 10, robes, bags and the reagent bag slot. Every source recommends it |
| **Enchanting** | Disenchant your own cloth drops; BoP wands |
| Alchemy / Herbalism | Mana and elixirs for raids |
| Engineering | PvP gadgets; Gnomes fail less often |

Warcraft Tavern's guides suggest Tailoring + Enchanting; Method.gg agrees and says not to bother gathering. Cooking, First Aid (which now makes **healing potions**) and Fishing are all useful.

### Comprehension

- A Mage-only minor tradeskill. Warcraft Tavern says it unlocks at level 6.
- Loot scrolls from creatures, then use *Comprehend Scroll* to turn them into temporary buffs or higher-tier items.
- A failed decipher can turn you into a **sheep** until your skill rises (Warcraft Tavern).
- Library-book turn-ins reportedly unlocked a *Research* spell that made a Bundle of Scrolls once an hour. A 6 Nov hotfix says Mages no longer learn the "Research" spell that vanished on relog; whether it returns is unknown.

### Legacy talents

You can spend up to 16 points per character.

| Tree | Picks for a Mage |
|---|---|
| Adventure | **Well Rested** 5/5 → **Talented** 5/5 for faster leveling; *Thrill of Adventure* saves drinking |
| Resourcefulness | **Reagent Economy** 1/1 makes teleports, portals and Arcane Brilliance need no reagents; **Permanence** for long buffs |
| Professions | *Working Overtime* helps Tailoring and Comprehension skill-ups |

## Hardcore notes

!!! hardcore "Hardcore survival"

    [Hardcore](../../about/hardcore.md) arrives in winter 2026/27. Mages die to being caught.

    - Play **Frost**. Two escapes (Ice Block plus Cold Snap reset) and constant slows.
    - Always keep **Blink, Frost Nova and Ice Block** off cooldown before a pull you aren't sure about.
    - Mana Shield and Ice Barrier before pulls; Evocation is an emergency refill, not a damage tool.
    - Polymorph the adds and never fight more than you can kill. Watch for runners (Frostfire Bolt's slow helps at 40+).
    - Remember the Troll's *Rapid Regeneration* and Human's *Will to Survive* as extra lifelines.

## Common mistakes & FAQ

??? question "Should I level Frost, Arcane or Fire?"
    Frost is safest and the most common recommendation. Arcane is strong solo once you have Arcane Blast and Missile Barrage. Fire is weakest early because it needs crit.

??? question "Why does Arcane Blast drain my mana?"
    Each stack doubles its own cost (+100% per stack). Weave other spells and let the stacks drop outside burn phases.

??? question "Why won't my Ice Lance cast?"
    It shares an 8 s cooldown with Fire Blast.

??? question "Can Horde Mages go to Dalaran?"
    Horde characters are attacked on sight in Dalaran and can't earn Kirin Tor reputation. They can still enter the City of Dalaran dungeon through the sewer.

??? question "Is AoE farming dead?"
    No, but it's weaker: Improved Blizzard slows by 40% max and Cone of Cold is shorter.

- **Mistake:** forgetting new spells aren't added to your bars automatically any more.
- **Mistake:** casting low-rank spells for Arcane Concentration, Frostbite or Fingers of Frost procs; ranks learned more than 12 levels below you have reduced proc chance.
- **Mistake:** buying dual spec without gold for riding at 40. Plan for 150g+.

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
