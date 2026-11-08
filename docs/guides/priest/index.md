# Priest Guide

!!! info "Current as of 7 November 2026"
    This guide follows Blizzard's Priest deep dive, the [Priest reference page](../../characters/classes/priest.md) and launch-week fan guides. Warcraft Tavern reports **class tuning due on 10 November**, so expect numbers to move. Exact talent point orders were only published as images by fan sites. Where this guide gives a build, it lists the talents each milestone needs rather than a point-by-point order.

## Overview

The Priest is still Azeroth's most flexible healer. It heals with heal-over-time spells, direct heals and absorb shields, and the Shadow tree turns it into a full caster DPS. Forever's design goals for the class are:

- **Every spec viable.** Discipline gets a real identity built on shields, Penance and Divine Aegis. Holy gets Prayer of Mending and Holy Binding. Shadow is now a self-contained DPS spec, not a raid debuff bot.
- **Less race lottery.** **Fear Ward** and **Devouring Plague** are now baseline for every Priest at level 20. The remaining race-locked spells are smaller utility picks.
- **Less hit grinding.** *Holy Precision* (Discipline) gives up to 18% Holy hit, and *Shadow Focus* (Shadow) now grants Shadow hit.

| | |
|---|---|
| **Roles** | Healer (Holy, Discipline), ranged caster DPS (Shadow) |
| **Armor / weapons** | Cloth. Wands and one-handed maces by default; daggers and staves from weapon trainers |
| **Strengths** | Best all-round healer, strong self-sustain while leveling (Shield, Renew, Penance), Fear Ward and Mind Control utility, two healer specs to choose from |
| **Weaknesses** | Cloth armor and few escapes. Slow early kill speed: Priest and Warrior were the **slowest classes to level in beta**. Mana-hungry before talents and gear |
| **Dual spec** | Level 40, 50g at the class trainer |

### What's new in Forever

- **Baseline for everyone:** Fear Ward and Devouring Plague (level 20), Divine Spirit (level 30), Shadow Word: Death (level 32).
- **Fade** reduces twice as much threat.
- **Prayer of Healing** heals the *target's* party, not yours. In raids you can now heal any group.
- **Renew** from different Priests stacks on the same target.
- **New gold talents** at the new 16-point tier and the 21/31 tiers: Soul Warding, Penance, Divine Aegis, Holy Binding, Prayer of Mending, a 30-second Vampiric Embrace and a reworked Shadowform.
- **Removed:** Lightwell, Improved Prayer of Healing, Unbreakable Will, Force of Will, Improved Vampiric Embrace. **Binding Heal** was replaced by *Holy Binding* shortly before launch.
- **Damage and healing over time** take the caster's current stats when they tick, not when cast (Warcraft Tavern). Early wands also carry spell power.

### Races

Six races can be Priests. **Gnome is a new combination** in Forever.

| Faction | Race | Race-locked Priest spells | Add-on |
|---|---|---|---|
| Alliance | Human | Divine Grace *(new)*, Feedback | [Human Priest](human.md) |
| Alliance | Dwarf | Desperate Prayer, Chastise *(new)* | [Dwarf Priest](dwarf.md) |
| Alliance | Gnome **(new)** | Confounding Flash *(new)*, Contingency Plan *(new)* | [Gnome Priest](gnome.md) |
| Alliance | Night Elf | Starshards (buffed), Elune's Grace (redesigned) | [Night Elf Priest](night-elf.md) |
| Horde | Troll | Hex of Weakness, Shadowguard | [Troll Priest](troll.md) |
| Horde | Undead | Touch of Weakness, Dark Sacrifice *(new)* | [Undead Priest](undead.md) |

Skyborne, Orc and Tauren cannot be Priests. See [Races](../../characters/races.md) for every racial ability.

---

## Specs & talents

Talents start at **level 10**, one point per level, for 51 points at 60. Gold single-point tiers sit at **11, 16, 21 and 31 points** spent in a tree. Without Legacy bonuses that means:

| Points in one tree | Earliest level | What it unlocks |
|---|---|---|
| 11 | 20 | Tier-3 talents (Mind Flay for Shadow, Holy Nova for Holy) |
| 16 | 25 | Soul Warding · Holy Binding · Vampiric Embrace |
| 21 | 30 | Penance (Discipline) |
| 31 | 40 | Prayer of Mending · Shadowform |

The Legacy talent **Talented** moves your first point up to five levels earlier, so every milestone above arrives earlier too. See [Legacy](#professions-legacy).

=== "Discipline"

    **Identity:** shields, Penance and absorbs. Discipline is the strongest *solo* healer spec and a good questing spec with a wand.

    | Talent | Notes |
    |---|---|
    | Power in Light *(new)* | Boosts Smite and Penance damage against targets with your Holy Fire |
    | Twin Disciplines *(new)* | Boosts damage and healing of instant spells (Shield, Renew, SW:Pain, Holy Nova and others) |
    | Wand Specialization | Now only 2 points. Take it for leveling |
    | Silent Resolve | Also shortens stuns, fears and silences on you. It absorbed Unbreakable Will |
    | Holy Precision | Up to 18% Holy hit. Removes the need for hit gear on Holy damage |
    | Improved Power Word: Shield | Larger shields |
    | Mental Agility | Row 3, 3 points, now also covers Smite and Holy Fire |
    | Meditation | Much stronger in-combat regeneration from Spirit |
    | Improved Inner Fire | More armor and more charges |
    | Mental Strength | Now a % Intellect bonus instead of % mana |
    | **Soul Warding** (16) | Cheaper Power Word: Shield with a shorter cooldown |
    | Renewed Hope | Extra crit on your direct heals and Penance on Weakened Soul targets; each heal shortens Weakened Soul |
    | **Penance** (21) | 2 s channel, 12 s cooldown. Hits an enemy or heals an ally every second |
    | Divine Aegis | Critical heals leave a 12 s absorb shield based on the heal. Doesn't stack |
    | Improved Mana Burn | Faster Mana Burn |

    Power Infusion is still in the deep Discipline tree according to Warcraft Tavern. Blizzard's deep dive doesn't mention it (*unconfirmed*).

=== "Holy"

    **Identity:** throughput and group healing. Holy brings Prayer of Mending, Holy Binding and Spirit of Redemption, and has mana tools for long fights.

    | Talent | Notes |
    |---|---|
    | Twilight Focus | Renamed Healing Focus. Pushback protection on **all** casts, 3 points |
    | Blessed Recovery | Also triggers from any single hit over 30% of your health |
    | Inspiration | Triggers from any non-periodic critical heal |
    | Improved Healing | Also makes Penance and Prayer of Mending cheaper |
    | Searing Light (redesigned) | A smaller Holy damage bonus; Holy Fire can make your next Holy Nova free |
    | **Holy Binding** (16) | 50% of the healing your Flash Heals do to others also heals you |
    | Litany of Light | Refunds part of a heal's cost when it differs from your previous heal. Rewards mixing spells |
    | Spiritual Guidance | Spell damage share cut to about a third of the healing share |
    | Spiritual Healing | Now 3 points |
    | Spirit of Redemption | Now lasts 15 s |
    | **Prayer of Mending** (31) | 10 s cooldown, 30 s duration. Heals on the next hit, then jumps up to 5 times within 20 yards |

    !!! warning "Conflict: Binding Heal vs. Holy Binding"
        Blizzard's deep dive describes **Binding Heal**, a 1.5 s spell that heals you and your target. The launch kit replaced it with the passive **Holy Binding** described above (see [Classes](../../characters/classes/index.md#changes-between-the-deep-dives-and-launch)). Some fan guides still list Binding Heal. Renewed Hope's tooltip may still name it as well.

=== "Shadow"

    **Identity:** a self-buffing DoT and Mind Flay caster. Shadow Weaving now only buffs **your own** Shadow damage, so Shadow is a DPS spec you bring for its damage, not for a raid debuff.

    | Talent | Notes |
    |---|---|
    | Shadow Focus | Row 1. Now grants Shadow **hit** |
    | Shadow Reach | Row 2, 2 points. More range |
    | Improved Mind Flay | Row 3. More damage and range, weaker slow |
    | Mind Flay | Tier 3 (11 points, level 20) |
    | **Vampiric Embrace** (16) | Now 30 s duration on a 1-minute cooldown. A burst self/party heal window, not a permanent debuff |
    | Shadow Affinity | Slightly more threat reduction |
    | Silence / Improved Psychic Scream | Silence no longer requires Improved Psychic Scream. Blackout is now required for Improved Psychic Scream |
    | Devouring Contagion | Row 5. Cheaper Devouring Plague; on the target's death, the Plague jumps to an enemy within 5 yards with its remaining duration |
    | Early Demise | Row 6. More SW:Death crit below 20% health |
    | Shadow Weaving | Self-only, with a smaller bonus |
    | **Shadowform** (31) | You can cast all non-healing spells. Shadow spells cost **50% less** and get **+100% crit damage**; the flat damage bonus is lower |

    !!! note "Conflict: Shadowform"
        Blizzard's text gives Shadowform +100% Shadow **crit damage**. Warcraft Tavern's summary says Shadow crit **chance**. This guide follows Blizzard.

    Vampiric Touch is not in the Forever kit according to Warcraft Tavern.

### Recommended builds

!!! note "Builds are milestone lists"
    The fan sites published their trees as images, and their builds differ by patch. The lists below give the **talents to have at each milestone**. Fill the remaining points into the tree's obvious damage, mana or survival talents. Check a talent calculator ([Mobalytics](https://mobalytics.gg/wow-forever/priest-talent-calculator) or [Zockify](https://www.zockify.com/forever/priest/)) once the 10 November tuning lands.

=== "Leveling (recommended)"

    Two routes are popular. Both work; pick by how often you group.

    **A. Discipline → Shadow at 40** (Method)

    | Levels | Spend on |
    |---|---|
    | 10–19 | Wand Specialization (2), Twin Disciplines, Improved Power Word: Shield, Silent Resolve or Holy Precision |
    | 20–25 | Mental Agility, Meditation, Improved Inner Fire, then **Soul Warding** at 16 points |
    | 25–30 | Mental Strength, Renewed Hope, then **Penance** at 21 points |
    | 30–39 | Power in Light, Divine Aegis and the rest of the cheap-mana talents |
    | 40 | Buy dual spec. Make spec two **Shadow** for questing and keep Discipline for dungeons, or respec fully into Shadow |

    Method notes this build is mana-efficient and tanky, but its damage falls off in the mid-to-late 30s. That's why it swaps to Shadow at 40.

    **B. Shadow from level 10** (Mobalytics, Warcraft Tavern)

    | Levels | Spend on |
    |---|---|
    | 10–19 | Shadow Focus, Shadow Reach, Improved Shadow Word: Pain (if present), then Mind Flay at 11 points |
    | 20–25 | Improved Mind Flay, then **Vampiric Embrace** at 16 points |
    | 25–39 | Shadow Affinity, Silence, Devouring Contagion, Shadow Weaving, Early Demise |
    | 40 | **Shadowform** at 31 points |
    | 41–60 | Top up Shadow, then Discipline: Wand Specialization, Twin Disciplines, Improved Shield, Mental Agility, Meditation |

    Warcraft Tavern notes Shadow doesn't really shine until about level 28, when you have some spell power. Disc is smoother before that.

=== "Holy raid"

    The fan guides list about **20/31/0** or **19/32/0**: deep Holy for Prayer of Mending and Spirit of Redemption, with about 20 Discipline points for Mental Agility, Meditation, Mental Strength, Improved Shield and Soul Warding. These splits come from beta calculators (*unconfirmed for launch*).

    Must-haves: Twilight Focus, Inspiration, Improved Healing, Holy Binding, Litany of Light, Spiritual Healing, Spiritual Guidance, Spirit of Redemption, **Prayer of Mending**.

=== "Discipline raid"

    About **31/20/0**: Penance, Divine Aegis and Renewed Hope, with about 20 Holy points for Twilight Focus, Inspiration, Improved Healing and **Holy Binding**. This is the strongest tank-healing and single-target build (*unconfirmed for launch*).

=== "Shadow raid / PvP"

    Deep Shadow to **Shadowform** (31+) and the rest in Discipline for Mental Agility, Twin Disciplines, Improved Shield and Meditation. For PvP, consider Silence, Improved Psychic Scream and Silent Resolve over pure damage talents. Exact splits are not yet published.

### Dual spec at 40

At 40 you can buy a second spec for **50g** from any Priest trainer and swap outside combat and battlegrounds. Changing talents inside a spec still costs a fee, which decays to 1g over time.

The usual pairing is **Shadow for questing + Holy or Discipline for dungeons**. Note that 40 is also when you want your 100g mount. Method suggests skipping low-value spell ranks earlier so you can afford both.

---

## Abilities & rotation

### Key spells by level

Spell levels follow Warcraft Tavern and Method. Ranks are omitted.

| Level | New spells |
|---|---|
| 1 | Smite, Lesser Heal, Power Word: Fortitude |
| 4 | Shadow Word: Pain |
| 6 | Power Word: Shield |
| 8 | Renew, Fade |
| 10 | Mind Blast, Resurrection, **first race spell**, first class quest. Talents begin |
| 12 | Inner Fire |
| 14 | Psychic Scream, Cure Disease |
| 16 | Heal |
| 18 | Dispel Magic |
| 20 | Flash Heal, Holy Fire, **Fear Ward**, **Devouring Plague**, Mind Soothe, Shackle Undead, **second race spell**, second class quest; library-book quest unlocks |
| 22 | Mind Vision |
| 24 | Mana Burn |
| 30 | **Divine Spirit**, Prayer of Healing, Mind Control |
| 32 | **Shadow Word: Death**, Abolish Disease |
| 34 | Levitate |
| 35 | Library-book quest unlocks |
| 40 | Greater Heal, dual spec, Apprentice Riding |
| 45 | Library-book quest unlocks |
| 48 | Prayer of Fortitude |
| 56 | Prayer of Shadow Protection |
| 60 | Prayer of Spirit |

!!! warning "Conflict: Shadow Word: Death backlash"
    Blizzard's deep dive says SW:Death hurts you for **10%** of your maximum health if the target survives. The pre-launch notes collected on the [Priest page](../../characters/classes/priest.md) say **30%**, with no backlash on a miss. Treat it as a big self-hit and don't use it as a filler at low health.

### Rotations

=== "Shadow"

    **Solo questing (Method, 40+):**

    1. Pre-cast **Power Word: Shield** on yourself.
    2. Open with **Mind Blast** (cast before the mob reaches you).
    3. **Shadow Word: Pain**.
    4. **Shadow Word: Death** on cooldown, if your health allows.
    5. **Mind Blast** on cooldown.
    6. **Mind Flay** to fill. Add **Devouring Plague** on tough or elite mobs.

    **Single-target raid (general):** keep SW:Pain and Devouring Plague up, Mind Blast on cooldown, Mind Flay to fill, SW:Death while moving or during execute (Early Demise). Shadow Weaving stacks from your own spells only, so start building it immediately.

    **Multiple targets:** dot each target with SW:Pain. With Devouring Contagion, Plague the target that will die first so it jumps.

    **Vampiric Embrace:** a 30 s window every minute. Use it on big pulls in dungeons or when the healer is struggling.

=== "Discipline"

    **Solo questing (Warcraft Tavern):** Shield yourself when mana allows, open with Smite or Holy Fire (Power in Light), apply SW:Pain, **Penance on cooldown** (as damage, or as a self-heal), then wand or let the DoT finish.

    **Healing:**

    1. **Power Word: Shield** on whoever is about to take damage. Soul Warding makes this your main spell.
    2. **Penance** on cooldown on the most injured target.
    3. Flash Heal / Greater Heal on Weakened Soul targets for Renewed Hope crits. Each crit leaves **Divine Aegis**.
    4. Renew on a tank you can't shield.
    5. In a 5-player group, Prayer of Healing for group damage.

=== "Holy"

    **Healing:**

    1. Keep **Prayer of Mending** bouncing. Put it back on the tank every 10 s.
    2. **Renew** on targets taking steady damage. Renew from other Priests stacks.
    3. **Flash Heal** for fast single-target healing. Holy Binding heals you for half.
    4. **Heal / Greater Heal** for efficient big heals.
    5. **Prayer of Healing** on a member of the damaged group.
    6. Alternate spells for **Litany of Light** refunds rather than spamming one.

    **Solo:** same as Discipline minus Penance. Holy is the slowest leveling spec.

### Cooldowns & utility

| Spell | Use |
|---|---|
| Fear Ward | Every Priest now has it. Put it on the tank before fear casts |
| Psychic Scream | Emergency escape. It can pull extra mobs, so watch the surroundings |
| Fade | Twice as strong. Use it after a big heal on a fresh pull |
| Shackle Undead | Crowd control in Scholomance, Stratholme and the [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) |
| Mind Control | PvP throwing, and some dungeon tricks |
| Mana Burn | PvP only |
| Divine Spirit | Baseline now. Keep it on casters and healers |

### Macros

Mouseover healing (no add-on needed):

```
#showtooltip
/cast [@mouseover,help,nodead][help,nodead][@player] Flash Heal
```

Self-shield without losing your target:

```
#showtooltip
/cast [@player] Power Word: Shield
```

Fear Ward on the focus (set the tank as focus):

```
#showtooltip
/cast [@focus,help][help][@player] Fear Ward
```

!!! note
    The modern `@` macro conditionals and focus targets are assumed to work, as they do in the current Classic clients. Forever's add-on and macro rules are on [Add-ons & UI](../../systems/addons.md).

---

## Leveling walkthrough 1–60

General advice:

- **Get a wand at level 5–13.** Wanding is your main mana-free damage until Penance or Shadowform. See the wand list in the 10–20 section.
- **Shield, DoT, wand.** Most kills before 30 are Power Word: Shield → Shadow Word: Pain → Mind Blast → wand. DoTs tag a mob instantly, so lead with SW:Pain when other players compete for it.
- **Drink, don't rest.** Buy water for your level every time you visit a town. Spirit regenerates mana outside the five-second rule.
- **Camping and rested XP:** a campfire with a Leatherworking Camp Tent gives rested XP. The Cozy Sleeping Bag scavenger hunt starts at level 14. See [Camping](../../systems/camping.md) and [Leveling](../../characters/leveling.md).
- **Quest XP beats dungeon mob XP.** Run dungeons for their quests.

### 1–10: starting zones

| Alliance | Horde |
|---|---|
| Human: Northshire → Elwynn Forest | Troll: Valley of Trials → Durotar |
| Dwarf, Gnome: Coldridge Valley → Dun Morogh | Undead: Deathknell → Tirisfal Glades |
| Night Elf: Shadowglen → Teldrassil | |

- **Train:** Smite and Lesser Heal (1), SW:Pain (4), Power Word: Shield (6), Renew and Fade (8), Mind Blast (10).
- Do the starting-zone quest chain, train at every level, and take the camping quest *The Great Outdoors* at about level 5.
- At **10**: your first race spell, your first class quest and your first talent point.
- Durotar, Teldrassil and Tirisfal have new quests and NPCs in Forever. Tirisfal gained **Shadowvale** and **Bandarion Keep** in its empty western strip.

Each race add-on has the step-by-step for its starting zone.

### 10–20

| Alliance | Horde |
|---|---|
| Westfall, Loch Modan, Darkshore | The Barrens, Silverpine Forest |
| Redridge Mountains (15+) | Stonetalon Mountains (15+) |

- **Train:** Inner Fire (12), Psychic Scream and Cure Disease (14), Heal (16), Dispel Magic (18).
- **Talents:** your first 10 points. Take Wand Specialization early if you lead with Discipline.
- **Wands** (Method and Warcraft Tavern; the lists differ):

| Wand | Level | Source |
|---|---|---|
| Lesser Magic Wand | 5 | Enchanting (craft it yourself or buy it) |
| Greater Magic Wand | 13 | Enchanting |
| Sizzle Stick | 15 | Wailing Caverns quest (Warcraft Tavern) |
| Gravestone Scepter | 18 | Blackfathom Deeps quest *Blackfathom Villainy* |
| Charred Wand | 19 | Hillsbrad quest *Dangerous!* (Method) |

- **Dungeons:** [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) (Ironforge, 13–20), Ragefire Chasm (13–19), [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) (Tirisfal, 15–22), The Deadmines and Wailing Caverns (17–25).
- **Library books:** start collecting class library books now. Turning in 10 unlocks a quest at level 20. Locations aren't documented on this wiki yet.

### 20–30

| Alliance | Horde |
|---|---|
| Wetlands, Duskwood, Ashenvale, Redridge | Hillsbrad Foothills, Ashenvale, Stonetalon, Thousand Needles (25+) |

- **Train at 20:** Flash Heal, Holy Fire, **Fear Ward**, **Devouring Plague**, Shackle Undead, Mind Soothe. This is a big training bill, so save for it.
- **At 20:** your second race spell, the second class quest, and the first library-book quest (10 books).
- **Talents:** 11 points opens tier 3 (Mind Flay for Shadow). At **25** you reach the 16-point gold tier: Soul Warding, Holy Binding or Vampiric Embrace.
- **Dungeons:** Shadowfang Keep, Blackfathom Deeps (Gravestone Scepter), the Stockade, and the new [Excavation Site: Wetlands](../../content/dungeons/excavation-site.md) (24–33).
- **Wands at 26–27:** *Dancing Flame* (Arathi quest *Final Passage*), *Wand of Eventide* (world drop), *Wand of Mana Concentration* (City of Dalaran quest *Arcanic Enigma*). *Unconfirmed: single-source each.*

### 30–40

| Alliance | Horde |
|---|---|
| Alterac Mountains (Dalaran), Arathi Highlands, Stranglethorn Vale, Desolace, Dustwallow (35+) | Arathi Highlands, Stranglethorn Vale, Desolace, Thousand Needles, Dustwallow (35+) |
| **Riverglades** (35+) from Farholde Keep | **Riverglades** (35+) from Rog'mar |

- **Train:** Divine Spirit, Prayer of Healing, Mind Control (30); **SW:Death** and Abolish Disease (32); Levitate (34).
- **Talents:** 21 points at 30 gives **Penance** for Discipline.
- **At 35:** the second library-book quest (20 books in total).
- **Riverglades** is new, contested and roughly Stranglethorn-sized. Reach it from Redridge, the Badlands, the Swamp of Sorrows, the Burning Steppes, or the Tanaris ferry. See [Zones](../../world/zones.md#riverglades).
- **Dungeons:** [City of Dalaran](../../content/dungeons/city-of-dalaran.md) (28–35; Horde are attacked on sight in Dalaran), Razorfen Kraul, Gnomeregan, Scarlet Monastery wings, [The Drowned City](../../content/dungeons/drowned-city.md) (35–42).
- Desolace centaur quests now need level 35. [Shen'dralas](../../world/zones.md#shendralas) lies beyond the Valley of Bones (level range unknown).

### 40–50

| Alliance | Horde |
|---|---|
| Riverglades, Badlands, Swamp of Sorrows, Feralas, Tanaris, Hinterlands | Riverglades, Badlands, Swamp of Sorrows, Feralas, Tanaris, Hinterlands |
| Searing Gorge (43+), Azshara and Felwood (45+) | Searing Gorge (43+), Azshara and Felwood (45+) |

- **At 40:** Apprentice Riding and your first mount (100g), **dual spec** (50g), Greater Heal. Shadow reaches **Shadowform**; Holy reaches **Prayer of Mending**.
- **At 45:** the third library-book quest (25 books in total).
- **Train:** Prayer of Fortitude (48).
- **Dungeons:** [Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md) (Riverglades, 40–47), Scarlet Armory and Cathedral, Razorfen Downs, Uldaman, Zul'Farrak, [Alcaz Prison](../../content/dungeons/alcaz-prison.md) (48–55).

### 50–60

| Alliance | Horde |
|---|---|
| Un'Goro (48+), Burning Steppes, Western Plaguelands, Azshara | Un'Goro (48+), Burning Steppes, Western Plaguelands, Azshara |
| Winterspring and Eastern Plaguelands (53+), Silithus (55+) | Winterspring and Eastern Plaguelands (53+), Silithus (55+) |

- **Train:** Prayer of Shadow Protection (56), Prayer of Spirit (60).
- **Azshara** has many new quests and the new [Blackmaw Hold](../../content/dungeons/blackmaw-hold.md) (55–60). Un'Goro's north holds [Shaper's Terrace](../../content/dungeons/shapers-terrace.md) (58–60).
- **Mount Hyjal** opens from Winterspring's Darkwhisper Gorge at 60. Its two raids open on 9 December.
- The Legacy class tiers award points at 25, 45 and 60 for the first Priest on your account.

---

## Dungeons

Priests are always welcome in groups. Forever's [group finder](../../content/dungeons/index.md#general-rules) lists groups but doesn't teleport you, and Meeting Stones don't summon.

**Healer tips**

- **Shield the tank before the pull** and pre-place Renew. With Soul Warding you can keep a shield on the tank almost permanently.
- **Fear Ward the tank** before fearing bosses. Every Priest has it now.
- **Fade is twice as strong.** If you pull aggro with a big heal, Fade and let the tank pick up.
- **Prayer of Healing heals the target's party.** In a five-player group that's still your group.
- **Drink between pulls** and tell the group when you're low.
- Method notes Shadow Priests can heal dungeons to 60 without respeccing, at worse mana efficiency. Dual spec at 40 makes this easier.

**Shadow tips**

- Shadow Affinity lowers your threat. Still, let the tank build threat before Mind Blast.
- Vampiric Embrace heals the party during its 30 s window. Use it on big pulls.
- Silence and Psychic Scream are emergency interrupts and CC. Scream can run mobs into other packs.

**Notable dungeons**

| Level | Dungeon | Priest notes |
|---|---|---|
| 13–20 | [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) | New. First dungeon for Alliance Priests |
| 15–22 | [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) | New. Undead mobs mean Shackle practice. Drops the Fermenter and Arcane Salvager camp blueprints |
| 18–26 | Deadmines, Wailing Caverns | Classic. Sizzle Stick wand quest in WC |
| 24–33 | [Excavation Site: Wetlands](../../content/dungeons/excavation-site.md) | New |
| 25–32 | Blackfathom Deeps | Gravestone Scepter quest |
| 28–35 | [City of Dalaran](../../content/dungeons/city-of-dalaran.md) | New. Wand of Mana Concentration quest (*single source*) |
| 35–42 | [The Drowned City](../../content/dungeons/drowned-city.md) | New |
| 40–47 | [Krol'dok Stronghold](../../content/dungeons/kroldok-stronghold.md) | New, in the Riverglades |
| 48–55 | [Alcaz Prison](../../content/dungeons/alcaz-prison.md) | New |
| 55–60 | [Blackmaw Hold](../../content/dungeons/blackmaw-hold.md) | New. Has a Barrow Deeps entrance |
| 58–60 | [Shaper's Terrace](../../content/dungeons/shapers-terrace.md), Scholomance, Stratholme | Shackle Undead is vital in Scholomance and Stratholme |

---

## Raid preparation

The launch raids open on **9 December 2026**: [The Barrow Deeps](../../content/raids/barrow-deeps.md) (10), [Hyjal Summit](../../content/raids/hyjal-summit.md) (20) and [Onyxia's Lair](../../content/raids/onyxias-lair.md) (40). Blizzard describes the difficulty as coming from preparation, not hundreds of attempts.

### Your role

| Raid | Healers | Priest focus |
|---|---|---|
| Barrow Deeps (10) | About 2–3 | Discipline or Holy on tanks. Every heal counts, so Penance plus shields is strong |
| Hyjal Summit (20) | About 4–5 | Holy for raid healing (Prayer of Mending, Prayer of Healing on any group). Shadow is a valid DPS slot |
| Onyxia's Lair (40) | Many | **Fear Ward** the main tank before Bellowing Roar in phase 3 (Classic-era fight). Fire resistance helps |

Healer counts above are general guidance, not published numbers.

### Pre-raid gear approach

Pre-raid lists for Forever haven't been published. Forever's dungeon items have unique, themed stats, so classic BiS lists don't carry over. Practical approach:

1. Run the **new level-60 dungeons** ([Blackmaw Hold](../../content/dungeons/blackmaw-hold.md), [Shaper's Terrace](../../content/dungeons/shapers-terrace.md)) and the classic 60s (Scholomance, Stratholme, Dire Maul, LBRS/UBRS). Each new-dungeon boss reportedly drops a guaranteed blue.
2. Take every **healing power** and **Intellect** upgrade (healer) or **hit and Shadow power** (Shadow) over raw Stamina.
3. Check PvP vendors. Honor buys blue and epic sets, and the new sets fill spec gaps.
4. Crafted gear: Tailoring has many new BoP patterns.
5. For Onyxia, start the **Drakefire Amulet** attunement early. It is not account-wide.

### Consumables

- Mana potions and the best water you can buy or a Mage can conjure.
- **Healing potions now come from First Aid**, not Alchemy.
- Flasks and elixirs from Alchemy; buff food from Cooking.
- Camp buffs work in the open world. Note that they **don't stack** with the matching class buff; the First Aid Kit duplicates Power Word: Fortitude, and the Tailoring Faction Banner duplicates Divine Spirit.
- World buffs from the Chronoboon Displacer are removed in dungeons and raids.

---

## PvP

Priests are strong healers and annoying casters in PvP: Fear Ward, Psychic Scream, Mana Burn, Mind Control and Dispel Magic all matter. Your race spell often matters too.

- **Battlegrounds:** Warsong Gulch (10v10), Arathi Basin (15v15), Alterac Valley (40v40) and the new **[Battle for the Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands)** (15v15, levels 30–60). Darkspear Islands has four bases and a central flag. Holding a base as a healer and shielding the flag carrier both work well.
- **Healer play:** stay at maximum range behind pillars and walls. Shield yourself when focused, Fade does nothing against players, and Psychic Scream is your best escape. Dispel enemy buffs (Blessing of Freedom, Power Infusion and similar).
- **Shadow play:** Silence, Psychic Scream and Mind Blast burst, then SW:Death to finish. Watch the SW:Death backlash.
- **Mind Control:** pull enemies off ledges or into your team. In Warsong Gulch you can control the flag carrier.
- **Fear Ward yourself** against Warlocks and Warriors before engaging.
- **Progression:** seasons reset ranks, Honor buys gear, and Rank Points come from battlegrounds and weekly tasks. See [PvP](../../content/pvp/index.md).

| Matchup | Notes (general guidance) |
|---|---|
| Warrior | Keep distance. Shield, Scream, wand or DoT. Fear Ward against Intimidating Shout |
| Rogue | Expect stuns. Keep Inner Fire up, Scream after the opener; Human, Dwarf and Undead racials help a lot here |
| Mage | Dispel Polymorph on allies; Mana Burn and Silence |
| Warlock | Fear Ward first, then Dispel and DoT. Undead Will of the Forsaken counters fear |
| Hunter | Get inside the dead zone or out of range. Mana Burn their mana pool |
| Paladin | Mana Burn and Dispel. Long fights favor them |
| Priest | Shadow wins on burst; Discipline wins long fights |

---

## Gear, stats & enchants

| Spec | Stat priority (Warcraft Tavern) |
|---|---|
| **Holy / Discipline** | Healing power > Intellect > MP5 > Spirit > Crit |
| **Shadow** | Hit (to cap) > Spell / Shadow power > Crit > Intellect > Spirit |
| **Leveling (any)** | Intellect and spell power > Stamina and Spirit > Armor |

- **Intellect** raises your mana pool and spell crit. Mental Strength now multiplies it.
- **Spirit** matters more while leveling (out-of-combat regeneration) and for Holy/Discipline through Meditation. Shadow shouldn't seek it.
- **Hit:** Holy Precision covers Holy hit. Shadow Focus gives Shadow hit, which lowers the hit gear Shadow needs. The exact cap hasn't been published.
- **Weapons:** wands until 60; then a caster staff, or a mace or dagger with an off-hand.

**Enchants:** Forever's Enchanting recipe list isn't fully documented. Look for Intellect, healing or spell power, Spirit and Stamina enchants on chest, bracers, cloak and weapon. Enchanting also gives spell power oils for weapons (Warcraft Tavern).

---

## Professions & Legacy { #professions-legacy }

### Professions

| Pick | Why |
|---|---|
| **Tailoring + Enchanting** | The classic Priest pair. Tailoring makes cloth leveling gear and many new BoP patterns. Enchanting makes your own wands (Lesser at 5, Greater at 13) and spell power oils. Method suggests learning both at launch for the self-made wand |
| **Herbalism + Alchemy** | Mana potions, flasks and elixirs for raid nights |
| **Herbalism + Skinning** | Least intrusive gold while leveling (Method) |

- **Secondary skills:** Cooking (food buffs and campfires), Fishing (crates and pearls). First Aid now makes **healing potions**, which is more useful than it used to be, though Method rates bandages as low value for Priests.
- Crafting professions also earn **Legacy Points** at 150, 225 and 300. See [Professions](../../characters/professions.md).

### Legacy talents

You can spend up to **16 points** per character. Good Priest picks:

| Talent | Tree | Why |
|---|---|---|
| **Well Rested** → **Talented** | Adventure | Faster rested XP, then earlier talent points. Big for a slow leveler |
| **Thrill of Adventure** | Adventure | Health and mana back on kills: less drinking |
| **Permanence** | Resourcefulness | Fortitude, Divine Spirit and Shadow Protection last longer |
| **Reagent Economy** | Resourcefulness | No reagents for Prayer of Fortitude, Prayer of Spirit or Prayer of Shadow Protection |
| **The Quick and the Dead** | Resourcefulness | Faster corpse runs |
| **Frequent Flier** | Adventure | Cheaper, faster flights |

See [Legacy System](../../characters/legacy.md).

---

## Hardcore notes

The [Hardcore](../../about/hardcore.md) ruleset arrives this winter. Priests are one of the safer Hardcore classes thanks to self-healing, but they are slow and squishy.

- **Always pre-shield.** Most deaths start with an unshielded pull.
- **Keep Psychic Scream for escapes,** and look around before you use it. Feared mobs can bring friends.
- **Fear Ward yourself** in areas with fearing mobs.
- **Don't use SW:Death** when your own health is low.
- **Know your race's panic button:** Desperate Prayer (Dwarf), Contingency Plan (Gnome), Divine Grace for a party member (Human), Elune's Grace (Night Elf), Rapid Regeneration (Troll), Will of the Forsaken (Undead).
- Keep healing potions (First Aid) and bandages.
- Dungeons give less mob XP. Group for quests rather than chain runs.

---

## Common mistakes / FAQ

??? question "Which spec should I level?"
    Shadow is the most common answer and the smoothest after about 28. Discipline is safer early and better if you heal dungeons. Holy is the slowest solo. Dual spec at 40 lets you keep a healer spec.

??? question "Do I need to be a specific race for Fear Ward now?"
    No. Fear Ward and Devouring Plague are baseline for every Priest at level 20.

??? question "Why doesn't my Prayer of Healing heal my own party?"
    In Forever it heals the **target's** party. Target someone in the group you want to heal.

??? question "Is Shadow wanted in raids?"
    Shadow Weaving no longer buffs other players, so Shadow earns its spot on damage. Shadowform's lower costs and doubled crit damage are meant to make that competitive. Early raid logs will tell.

??? question "Can I DPS in Shadowform and still heal?"
    No. Shadowform allows all non-healing spells.

??? question "Is Binding Heal in the game?"
    No. It was replaced by the passive Holy Binding before launch.

**Common mistakes**

- Skipping a wand before level 13.
- Using Mind Blast as your opener in a crowded area instead of SW:Pain, which tags instantly.
- Forgetting to re-buy water and training costs. Save money for level 20 and level 40.
- Raid-healing your own party with Prayer of Healing out of habit.
- Ignoring library books until 20.

---

## Sources

- Blizzard, *Class Deep Dives — Priest and Warrior*: <https://news.blizzard.com/en-us/article/24301514/world-of-warcraft-forever-class-deep-dives-priest-and-warrior>
- Warcraft Tavern, Priest guide: <https://www.warcrafttavern.com/forever/guides/priest/>
- Warcraft Tavern, Priest leveling guide: <https://www.warcrafttavern.com/forever/guides/priest-leveling/>
- Method, Priest leveling guide and talents: <https://www.method.gg/wow-forever/wow-forever-priest-leveling-guide-and-talents>
- Mobalytics, Priest guides and talent calculator: <https://mobalytics.gg/wow-forever/priest-guides>, <https://mobalytics.gg/wow-forever/priest-talent-calculator>
- Icy Veins, Holy and Discipline Priest guides: <https://www.icy-veins.com/wow-forever/holy-priest-healer-pve-guide>, <https://www.icy-veins.com/wow-forever/discipline-priest-healer-pve-guide>
- Zockify, Priest talent calculator: <https://www.zockify.com/forever/priest/>
- Wiki pages: [Priest](../../characters/classes/priest.md), [Races](../../characters/races.md), [Leveling](../../characters/leveling.md), [Legacy](../../characters/legacy.md), [Sources](../../sources.md)
