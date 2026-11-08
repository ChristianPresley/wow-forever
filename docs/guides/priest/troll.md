---
tags:
  - Priest
  - Troll
  - Horde
---

# Troll Priest

!!! tip "Add-on"
    Read with the [Priest guide](index.md).

## Why this combo

Troll Priest is a Classic combination and **not new**. Its Priest spells, **Hex of Weakness** and **Shadowguard**, are unchanged and rated weak by Warcraft Tavern. The race itself carries the combo: **Berserking** is +10% cast speed on demand, and the new **Rapid Regeneration** heals half your health over 6 s out of combat, which cuts downtime a lot while leveling.

**Best for:** Horde raid healers and Shadow DPS who want a haste cooldown, and players who want fast leveling downtime.

## Racials in practice

| Racial | Type | PvE | PvP | Rating |
|---|---|---|---|---|
| **Berserking** | Active | **+10% cast speed for 15 s.** More Greater Heals in a crisis, or more Mind Flay ticks and Mind Blasts in a burn | Burst | **5/5**{ .stars .s5 } |
| **Rapid Regeneration** *(new)* | Active | Regenerates **50% of max health over 6 s**; any action cancels it. Use it instead of eating after a fight | Only to top up out of combat | **4/5**{ .stars .s4 } leveling |
| **Beast Slaying** | Passive | Extra damage against Beasts (value not given on this wiki). Many leveling quests are beasts | Druid forms aren't Beasts (*Classic-era*) | **3/5**{ .stars .s3 } leveling |
| **Regeneration** | Passive | +20% health regen, part of it in combat | Small | **2/5**{ .stars .s2 } |

**Priest spells unique to Trolls**

| Spell | Level | Effect (Classic-era) | Use |
|---|---|---|---|
| **Hex of Weakness** | (Classic spell) | Weakens the target's damage and the healing it receives | PvP against melee; marginal in PvE |
| **Shadowguard** | (Classic spell) | A self-buff that deals Shadow damage to attackers with each hit, using charges | A little extra damage while leveling, especially when mobs reach you |

Blizzard lists both as unchanged from Classic, without levels. Expect them at the race-spell levels of 10 and 20.

**Macros**

Berserking with a big heal:

```
#showtooltip Greater Heal
/cast Berserking
/cast [@mouseover,help,nodead][help][@player] Greater Heal
```

Rapid Regeneration after a fight (it cancels if you act, so don't spam):

```
#showtooltip Rapid Regeneration
/cast [nocombat] Rapid Regeneration
```

!!! note
    It isn't documented whether Rapid Regeneration can be cast in combat. The `[nocombat]` guard stops you wasting it.

## Starting zone walkthrough (1–~12)

Trolls start in the **Valley of Trials**, Durotar, with Orcs. Blizzard says the Valley of Trials got **new NPCs, quests, profession hooks and "small moments"**. Quest names below are Classic-era and may differ.

1. **Level 1–2:** take *Your Place in the World* and the opening quests from the den. Kill boars and scorpids. The Priest trainer is in the **Den** (Classic: Ken'jai).
2. **Level 2–5:** the quilboar *Sarkoth*, *Vile Familiars* and the cactus apples. Train **Shadow Word: Pain** at 4.
3. **Level 5:** take **The Great Outdoors** and learn Cooking. Kill **Yarrog Baneshadow** in the cave for the Burning Blade medallion.
4. **Level 6:** **Power Word: Shield**. Head toward **Sen'jin Village**, the Darkspear home on the coast.
5. **Level 6–10:** Sen'jin and **Razor Hill**: the Echo Isles, Thunder Ridge, the Skull Rock Burning Blade, and Tiragarde Keep. Sen'jin has early class trainers (Classic-era).
6. **Level 10:** learn your first race spell and first talent, and take the class quest. Full training is in **Orgrimmar** in the **Valley of Spirits**.
7. **Level 10–12:** finish Durotar, then cross west into **the Barrens** at the Crossroads.

## Route to 60 from Orgrimmar

| Levels | Zones | Hub / flight path |
|---|---|---|
| 10–20 | The Barrens | The Crossroads; Durotar Supply and Logistics camp to the west |
| 13–19 | Ragefire Chasm (Orgrimmar) | — |
| 15–25 | Stonetalon Mountains, Silverpine Forest (via the Undercity zeppelin), Wailing Caverns | Sun Rock Retreat, the Sepulcher |
| 15–22 | [Ruins of Lordaeron](../../content/dungeons/ruins-of-lordaeron.md) (Tirisfal) | — |
| 20–30 | Ashenvale, Hillsbrad Foothills, Thousand Needles | Splintertree Post, Tarren Mill, Freewind Post |
| 30–40 | Desolace, Stranglethorn Vale, Arathi Highlands, Dustwallow | Shadowprey Village, Grom'gol, Hammerfall, Brackenwall |
| 35–45 | **Riverglades** (through the Swamp of Sorrows or Badlands) | **Rog'mar** (flights to Stonard, Hammerfall, Kargath, Flame Crest) |
| 40–50 | Tanaris, Feralas, Hinterlands, Badlands, Azshara (45+), Felwood | Gadgetzan, Camp Mojache, Revantusk Village |
| 50–60 | Un'Goro, Burning Steppes, Plaguelands, Winterspring, Silithus | Flame Crest, the Bulwark, Everlook |
| 60 | Mount Hyjal (from Winterspring) | Tainted Foothills |

- **Class trainers:** Valley of Spirits, Orgrimmar.
- Horde players are **attacked on sight in Dalaran** and can't earn Kirin Tor reputation, so skip the City of Dalaran quest hubs.
- Stranglethorn's new [Drowned City](../../content/dungeons/drowned-city.md) and the troll-themed Zul'Farrak are on your route.

## Faction-specific notes

- **Mount:** raptors at 40 (100g). Honored with **Darkspear Trolls** gives 10% off.
- **Reputation:** Darkspear Trolls is your home faction. The new **Darkspear Raiders** battleground faction ([Darkspear Islands](../../content/pvp/battlegrounds.md#darkspear-islands)) is separate. Its Exalted rewards include a tabard and a Legacy Point.
- **Lore:** Darkspear priests honor the loa as well as the Light and shadow; the Echo Isles and Sen'jin are your people's home.
- **PvP vendor:** Hall of Legends, Orgrimmar.

## Verdict

**The Horde raid-healer and Shadow pick.** Berserking is the best throughput racial a Priest can get, and Rapid Regeneration makes leveling smoother. The Troll Priest spells are weak, so you're choosing the race for its racials, not its Priest kit. Pick Undead instead for Will of the Forsaken in PvP.
