# Human Priest

!!! tip "Add-on"
    Read with the [Priest guide](index.md).

## Why this combo

Human Priest is a classic Alliance pick and **not a new combination**. It is the most straightforward healer in the game: Humans gain extra Spirit and crit, a stun breaker, and **Divine Grace**, a new emergency heal for someone else. Stormwind is also the most central Alliance capital, with the Stormwind Harbor boat to Auberdine and easy reach of the new Riverglades through Redridge.

**Best for:** Holy or Discipline healers, Alliance PvP healers, and players who want the gentlest start.

## Racials in practice

| Racial | Type | PvE | PvP | Rating |
|---|---|---|---|---|
| **Will to Survive** *(new)* | Active | Rarely needed; breaks a stun from a mob during a bad pull | Top-tier. Breaks Rogue openers, Hammer of Justice, Charge stuns | ★★★★★ PvP / ★★ PvE |
| **Perception** | Active | Spots stealthed mobs in some dungeons | Finds Rogues and Druids before they open on you | ★★★ |
| **Ruthless** *(new)* | Passive | +1% crit: more Inspiration, Divine Aegis and Renewed Hope procs for healers; more damage for Shadow | Same | ★★★★ |
| **The Human Spirit** | Passive | **+10% Spirit** (was 5%). Faster mana between pulls while leveling; more in-combat regen through Meditation | Longer fights | ★★★★ |

**Priest spells unique to Humans**

| Spell | Level | Effect | Use |
|---|---|---|---|
| **Divine Grace** *(new)* | 10 | Instantly heals a friendly target below 50% health and **removes Weakened Soul**. Not on yourself. 5-minute cooldown | Emergency tank save. Removing Weakened Soul lets a Discipline Priest re-shield right away |
| **Feedback** | (Classic spell) | Classic-era: punishes casters who hit you by draining their mana | Situational PvP |

Warcraft Tavern rates Divine Grace as decent for shield-focused healers. It can't save *you*, so it's a group tool.

**Macros**

Break a stun and shield yourself in one press:

```
#showtooltip Will to Survive
/cast Will to Survive
/cast [@player] Power Word: Shield
```

Divine Grace then shield the same target (Discipline):

```
#showtooltip Divine Grace
/cast [@mouseover,help,nodead][help] Divine Grace
/cast [@mouseover,help,nodead][help] Power Word: Shield
```

!!! note
    Whether Will to Survive and Divine Grace share the global cooldown isn't documented. If the second line doesn't fire, press the macro twice.

## Starting zone walkthrough (1–~12)

Humans start at **Northshire Abbey** in Elwynn Forest. Quest names below are from Classic; Northshire wasn't on Blizzard's list of reworked starting zones, but small changes are possible.

1. **Level 1–2:** take the opening quest from the Marshal outside the abbey and kill wolves and kobolds in the valley. The Priest trainer is inside **Northshire Abbey** (Classic: Priestess Anetta). Learn your spells there at every even level.
2. **Level 2–4:** the vineyard and kobold mine quests. Train **Shadow Word: Pain** at 4 and start opening with it.
3. **Level 5:** pick up **The Great Outdoors** for camping, and learn Cooking. Head toward **Goldshire**. Learn Tailoring and Enchanting in Stormwind or Goldshire if you plan to make your own **Lesser Magic Wand**.
4. **Level 6:** train **Power Word: Shield**. Pre-shield every pull from now on.
5. **Level 6–10:** Elwynn's Goldshire quests: Fargodeep Mine, the Stonefield and Maclure farms, the Eastvale logging camp, and the murlocs of Crystal Lake.
6. **Level 8:** Renew and Fade.
7. **Level 10:** visit a Priest trainer in Goldshire or the **Cathedral of Light** in Stormwind. Learn **Mind Blast**, **Divine Grace** and your first talent point. Pick up the level-10 class quest (Warcraft Tavern says class quests come at 10 and 20).
8. **Level 10–12:** finish Elwynn (Hogger, the Brackwell pumpkin patch), then move to **Westfall**, or **Loch Modan** through Dun Morogh.

## Route to 60 from Stormwind

| Levels | Zones | Hub / flight path |
|---|---|---|
| 10–15 | Westfall (or Loch Modan) | Sentinel Hill |
| 15–20 | Redridge Mountains | Lakeshire; Three Corners supply camp (Azeroth Commerce Authority) |
| 18–24 | The Deadmines; [Hall of Thanes](../../content/dungeons/hall-of-thanes.md) from Ironforge | — |
| 18–30 | Darkshore (boat from Stormwind Harbor), Duskwood, Wetlands, Ashenvale | Darkshire, Menethil Harbor, Astranaar |
| 30–40 | Alterac Mountains (Dalaran), Arathi Highlands, Stranglethorn Vale, Desolace | Refuge Pointe, Booty Bay, Nijel's Point |
| 35–45 | **Riverglades** (from Redridge) | **Farholde Keep** (flights to Lakeshire, Thelsamar, Morgan's Vigil) |
| 40–50 | Dustwallow Marsh, Feralas, Tanaris, Hinterlands, Badlands, Swamp of Sorrows | Theramore, Feathermoon, Gadgetzan, Aerie Peak |
| 50–60 | Un'Goro, Azshara, Burning Steppes, Western and Eastern Plaguelands, Winterspring, Silithus | Marshal's Refuge, Chillwind Camp, Everlook |
| 60 | Mount Hyjal (from Winterspring) | Tainted Foothills |

- **Class trainers:** the Cathedral of Light in Stormwind, plus Goldshire and Northshire for early ranks.
- **Boats:** Stormwind Harbor ↔ Auberdine is new. The Menethil → Southshore → Auberdine loop is also new. See [Travel](../../world/travel.md).
- **PvP vendor:** Champion's Hall, Stormwind.

## Faction-specific notes

- **Mount:** Stormwind horses at 40 (100g with Apprentice Riding). Honored with Stormwind gives 10% off.
- **Reputation:** Stormwind is your home faction. The Diplomacy racial is gone; take the Legacy talent *Diplomat* if you want faster reputation.
- **Dalaran:** Alliance can earn **Kirin Tor** reputation; the [City of Dalaran](../../content/dungeons/city-of-dalaran.md) dungeon is there.
- **Riverglades** is Stormwind's lost frontier: Sunnyglade was a Stormwind town burned in the First War, and the Brotherhood of the Horse at Farholde Keep are its descendants. A Human Priest fits the story well.
- **Lore:** Stormwind's Cathedral of Light and the Church of the Holy Light lead Alliance priesthood.

## Verdict

**The safe, strong default for Alliance healers.** +10% Spirit and +1% crit help every spec, Will to Survive is one of the best PvP racials in the game, and Divine Grace adds a real tank save for Discipline. Pick Night Elf or Gnome instead if you want more burst damage or self-protection, or Dwarf for Stoneform.
