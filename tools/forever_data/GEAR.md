# Craftable gear (`craftable_gear.json`)

Built by `python tools/forever_data/gear.py [build]` (default build 1.60.1.70938). It reuses
`build.py`'s `fetch`/`load` helpers and caches the extra DB2 tables in `cache/<build>/`.

Output: `{build, stat_ids, notes, items[], enchants[]}`. 1280 items (weapons and armor
created by a SkillLineAbility recipe of Blacksmithing 164, Leatherworking 165, Alchemy 171,
Tailoring 197, Engineering 202 or Enchanting 333; there is no Jewelcrafting) and 180
enchant recipes with stats.

## Finding crafted items
- Recipe = `SkillLineAbility.Spell` under a profession SkillLine. The created item is the
  `SpellEffect` with `Effect == 24` (CREATE_ITEM), `EffectItemType` = item ID.
- Enchants: `SpellEffect.Effect == 53` (ENCHANT_ITEM), `EffectMiscValue_0` = SpellItemEnchantment ID.
- `skill`: `MinSkillLineRank` is 1 for nearly every recipe in this client, so the orange rank
  (`TrivialSkillLineRankLow`) is used. That can be up to about 20 above the classic learn
  requirement. For example, Arcanite Reaper is 320 here, while the plans need 300 (the plans item's
  `ItemSparse.RequiredSkillRank`).
- Bags, shirts, tabards, ammo and items that are not weapons or armor are skipped.

## Stat encoding (this client has no flat stat values)
`ItemSparse` has `StatModifier_bonusStat_N` (ItemModType) and `StatPercentEditor_N`
(budget share x 10000), but no `bonusAmount`. The value is:

    stat = round(StatPercentEditor * RandPropPoints[ilvl].<Quality>_<col> / 10000)

- Quality is `OverallQualityID` (2 = Good, 3 = Superior, 4/5 = Epic).
- `col` is the budget slot: 0 = head/chest/robe/legs/2H; 1 = shoulder/waist/feet/hands/trinket;
  2 = neck/wrist/finger/back/shield/off-hand; 3 = 1H/MH/OH weapons; 4 = ranged/thrown/relic.
- The raw percentages are kept in `stat_pct`.

Armor is computed the same way: `ItemArmorTotal[ilvl].<type> * ArmorLocation[invtype] *
ItemArmorQuality[ilvl].Qualitymod_q`. Robes use the chest row, and cloaks use the cloth
column. Shields use `ItemArmorShield`.

Weapon damage: `dps = ItemDamage<OneHand|TwoHand|...Caster|Ranged|Thrown|Wand>[ilvl].Quality_q`.
The caster tables apply when `Flags_1 & 0x200`. With `speed = ItemDelay / 1000` and
`v = DmgVariance`:
- `min = floor(dps * speed * (1 - v/2))`
- `max = round(dps * speed * (1 + v/2))`

Hit and crit are **ratings** (ItemModType 31 and 32). Known items match classic percentages at
TBC level-60 rates: 14 crit rating = 1% and 10 hit rating = 1%. The simulator must convert them.
The rates are inferred, not read from client data (they live in GameTables, which are not on
wago db2).

Forever-specific stat IDs were identified from known items:
- 50 = bonus armor
- 51–56 = fire, frost, holy, shadow, nature and arcane resistance
- 84–89 = holy, fire, nature, frost, shadow and arcane spell damage (Shadow Gown, Pearly Gown, ...)
- 112 and 113 = herbalism and mining skill

Still unknown and left as `statNNN`:
- 83 (Molten Heart of the Mountain)
- 90 (Huge Thorium Battleaxe, possibly axe skill)
- 124 (Obsidian belts and shield)
- 132 (Gnomish Universal Remote)

## Verification
| Item | Forever decode | Classic |
|---|---|---|
| Arcanite Reaper (i63, q3) | 153–256, 3.80, +13 Sta, +62 AP | 153–256, 3.80, +13 Sta, +62 AP |
| Lionheart Helm (i61, q4) | 565 armor, +18 Str, 28 crit rating (2%), 20 hit rating (2%) | 565, +18 Str, 2% crit, 2% hit |
| Robe of the Archmage | 96 armor, +12 Int, +40 SP, 14 crit rating (1%) | 96, +12 Int, +40 spell dmg, 1% crit |
| Bloodvine Goggles | 20 hit (2%), 14 crit (1%), 9 mp5 | same |

Note that Arcanite Reaper is quality 3 (rare) in this client.

## Equip spells and gaps
- `ItemXItemEffect` -> `ItemEffect` gives the spells, with trigger use, equip or proc.
- Passive equip auras are resolved through `SpellEffect`. Handled auras: 13 damage done, 135
  healing, 99/124 AP/RAP, 52/57 crit, 54/55 hit, 85 mp5, 29 stat, 30 skill, 22 resistance.
- Almost every plain stat is already in ItemSparse, so only one equip spell resolved (Dark
  Leather Gloves, skill). 49 items have an equip spell tagged `unresolved` (aura type listed):
  mostly 42 (proc trigger), 4 (dummy) and 107 (spell modifier). Weapon procs such as Nightfall,
  Arcanite Champion and Blood Talon carry no stats and need modelling in the sim.
- Enchants decode SpellItemEnchantment effects: 5 = stat, 3 = equip spell, 2 = weapon damage,
  1 = proc (`proc_spells`), 4 = resistance. 29 enchants include a proc or unresolved part.
  Some names contain `$k1` placeholders, but the amounts are correct.
- Not handled: random-suffix items, set bonuses, and server-side hotfixes.
