# Base stats (`base_stats.json`)

Base Strength, Agility, Stamina, Intellect and Spirit with no gear or buffs, for every
class/race pair in `run.py`'s `CLASS_RACES`, levels 1-60. Shape:
`{class: {race: {"<level>": {"str","agi","sta","int","spi"}}}}`, plus a `_source` key.

Tags: **F** Forever client, **C** Classic 1.12 server data, **A** assumption.

| Part | Tag | Source |
|---|---|---|
| Forever client check | F | `RaceStat` (build 1.60.1.70938) has one unknown column, and it is 0 for every race. It holds no stats. Base attributes are server-side. |
| Classic class/race pairs | C | `player_levelstats` from [cmangos classic-db](https://github.com/cmangos/classic-db) (`ClassicDB_1_12_1_z2815`, GPL-2.0). Only the numbers are stored. |
| New Forever pairs (Undead Paladin, Dwarf Shaman, Gnome Priest, Human Hunter, Orc Mage, Troll Warlock) | A | The class's Classic curve for one race, minus that race's level-1 offset from Human, plus the target race's offset. In Classic, base stats are a race base plus a class curve, so this holds when Forever keeps that model. |
| Skyborne (`sho`, `sws`), all classes | A | Night Elf offsets from Human, with Str set to Human +5. This follows the published Forever fix: Tauren Warrior is +5 Str vs Human, and the same fix applies to both Skyborne. There is no published Skyborne table. |
| Undead Mage level 1 Int/Spi | A | cmangos lists Int 27 / Spi 21, which looks swapped (Undead is Int -2, Spi +5 vs Human). Stored as Int 21 / Spi 27. |
| Tauren fix | C | Classic Tauren Warrior is already +5 Str vs Human, so no change was needed. |

Race offsets come from Warrior at level 1, which every race can play.

## Gaps
- No Forever table has been published. Other pre-launch base-stat corrections ("every race") are unknown and not applied.
- Skyborne Agi/Sta/Int/Spi are assumed equal to Night Elf.

Test: `python -m pytest tools/levelsim/test_base_stats.py` (run from `tools/levelsim`, or with it on `sys.path`).
