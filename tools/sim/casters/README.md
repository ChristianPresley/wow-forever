# Caster DPS simulator (WoW Forever)

An event-driven Monte Carlo combat simulator for the caster raid DPS specs, run for every race each class can be. Python 3.12, standard library only.

```bash
python tools/sim/casters/run.py                         # 1000 x 180 s fights, all 48 pairs, writes results
python tools/sim/casters/run.py -n 200 --fight 300 --seed 7
python tools/sim/casters/run.py --spec Fire --race troll -v --no-write   # breakdown, casts, mana
python -m unittest discover -s tools/sim/casters -p "test_*.py"
```

Output: `tools/sim/results/casters.json`, a list of
`{class, spec, race, dps_mean, dps_sd, ci95, iterations, fight_seconds, breakdown: {ability: dps}, data_confidence}`
plus extra fields `race_name`, `build`, `casts_per_fight` and `mana_left_pct`. `race` uses the race ids of `docs/javascripts/dps-calc.js`. `data_confidence` is the share of the data values a spec actually read that are tagged F or FE.

## Files

| File | What it holds |
|---|---|
| `data.json` | Every number. Each leaf is `[value, tag, source]`. Tags: **F** Forever, **FE** Forever estimate, **C** Classic checked, **CU** Classic unchecked, **A** assumption. `_sources` expands the source keys. |
| `engine.py` | Event queue, stats, hit/crit rolls, DoTs, channels, casting, GCD, mana. |
| `specs.py` | One class per spec: talents, procs and the priority APL. |
| `run.py` | Runs iterations (in parallel processes), aggregates, writes the JSON. |
| `test_sim.py` | Unit tests: tagging, hit/crit, DoT ticks and refresh, mana and regen, procs, end-to-end reproducibility. |

## The model

- **Time.** A priority queue of events: cast finishes, DoT ticks, channel ticks, 2 s mana ticks (random phase), racial cooldowns, the Imp's attacks. The player acts when free. The APL picks one action. Casts occupy `max(cast / haste, GCD)`. The GCD is 1.5 s / haste, floor 1.0 s. A 50 ms reaction delay follows each action.
- **Rolls.** Each direct hit, each Arcane Missile, each Lightning Overload rolls hit, then crit. DoTs and channels roll hit once on application. DoT ticks and Wrack ticks roll crit (Warlock only). Spell hit = 83% + gear + talents + racial, capped at 99%. Crit = class base + Int / ratio + gear + LotP 3 + Moonkin 3 − 1.8 suppression + talents + racials. Crit multiplier 1.5, raised by Ice Shards, Arcane Mind, Ruin, Pandemic, Shadowform, Vengeance and Elemental Fury.
- **Damage.** `(base roll + coefficient × spell power) × multipliers`. Multipliers: Curse of the Elements 10% on all magic (Curse of Shadow 10% on Shadow/Arcane is treated as the same 10%, not stacked), talents, procs and debuffs (Improved Scorch stacks, Shadow Weaving stacks, Improved Shadow Bolt, Fire Power counting your own Fire effects on the target, Wrack's +10% to other Shadow DoTs, Shadow and Flame, Soul Siphon), Eureka! (non-periodic only).
- **DoTs.** Damage per tick is snapshotted at application. Multipliers apply at tick time. A refresh drops the remaining ticks and restarts the timer (Classic rule). Haste does not speed up ticks. Channels are hasted.
- **Mana.** Max mana = base + Int conversion (first 20 Int give 1, then 15 each). Spirit regen per 2 s tick (Classic class formulas), stopped for 5 s after spending, except for the regen-while-casting talents. Blessing of Wisdom and Mana Spring always tick. Major Mana Potion when the deficit is at least 2250 (2 min cooldown). Evocation (mages), Life Tap = (424 + Spirit) × 1.2 (warlocks), Water Shield crits (shaman), Master of Elements (fire). Clearcasting, Omen and Elemental Focus make the next spell free.
- **Target.** A level 63 boss whose health falls linearly from 100% to 0% over the fight. This drives Decimation's below-35% phase.
- **Racials.** Blood Fury, Berserking, Elune's Light and Eureka! are used on cooldown from the pull. Passives: Ruthless, The Human Spirit, Artisan's Precision, Wind Blessed and Command (Imp damage). Race Intellect offsets come from the calculator.

## APLs and builds

Builds are the raid builds in `docs/guides/<class>/talents.md`.

| Spec | Build | Priority |
|---|---|---|
| Fire | 12/36/3 | Pre-cast Pyroblast. Evocation below 10% mana → Scorch to 5 Improved Scorch stacks, or to refresh with under 4 s left → Pyroblast at 3 Heating Up stacks (1.5 s) → Arcane Missiles on Missile Barrage → Fire Blast on cooldown → Fireball. Combustion on cooldown. |
| Frost | 15/5/31 | Ice Barrier pre-pull and on expiry → Ice Lance with Fingers of Frost → Arcane Missiles on Missile Barrage → Frostbolt. Evocation below 8%. |
| Arcane | 38/10/3 | Arcane Power when ready above 50% mana → Arcane Wrath on cooldown (with Presence of Mind) → Arcane Missiles on Missile Barrage → Arcane Blast while Arcane Power is up or mana stays above 35% → otherwise paid Arcane Missiles, which lets Arcane Blast stacks fall off. Evocation below 15%. |
| Affliction (Wrack) | 33/0/18 | Bane of Agony (Amplify Curse on cooldown) → Corruption → Siphon Life (each refreshed in the last tick) → Shadow Bolt on Nightfall → Life Tap below 35% → Wrack. Wrack is never clipped. |
| Destruction | 14/4/33 | Immolate → Conflagrate (keeps Immolate) → Shadowburn → Corruption → Life Tap below 25% → Incinerate. |
| Demonology | 2/31/18 | Imp out, Sayaad sacrificed (Demonic Pact). Pre-pull Soul Fire → Searing Pain to keep Demonic Brand → Bane of Doom with at least 60 s left (else Agony) → Immolate → Soul Fire during Decimation → Corruption → Life Tap below 30% → Searing Pain. |
| Shadow | 20/0/31 | Pre-cast Mind Blast. Vampiric Embrace → Shadow Word: Pain → Devouring Plague on cooldown → Mind Blast (Inner Focus on cooldown) → Shadow Word: Death → Mind Flay, never clipped. |
| Balance | 36/0/15 | Moonfire → Insect Swarm → Starfire on Omen of Clarity → Starfire while Eclipse charges remain → Wrath (gives 2 charges). This is the 2 Starfire : 1 Wrath cycle. |
| Elemental | 31/9/11 | Lightning Mastery on cooldown → Water Shield when the globes are used up → Chain Lightning on cooldown above 30% mana → Lightning Bolt. |

## Comparison with the analytic calculator

Mean over races, seed 1, 1000 × 180 s. Calculator values come from `dps-calc.js` with the same gear and buffs.

| Spec | Sim | Calc | Diff | Why |
|---|---|---|---|---|
| Frost | 505 | 453 | +12% | The sim adds Missile Barrage Arcane Missiles (~100 DPS) and Fingers of Frost Ice Lances. The calculator models only Frostbolt. |
| Shadow | 501 | 514 | −2% | Close. The sim pays GCDs for Vampiric Embrace and misses Mind Flay ticks along with the cast. |
| Balance | 487 | 437 | +11% | Eclipse (2.5 s Starfires), Nature's Grace and Omen of Clarity are not in the calculator. |
| Arcane | 470 | 394 | +19% | The calculator models Arcane Blast spam only. In the sim, Arcane Wrath alone gives ~180 DPS. The sim is mana bound (3% left at the end). |
| Destruction | 450 | 396 | +14% | The calculator uses a Shadow Bolt filler. The sim uses the guide rotation: Incinerate (+25% on Immolate), Shadowburn, Corruption, Shadow and Flame. |
| Affliction | 434 | 407 | +7% | Soul Siphon, Wrack's DoT bonus and Nightfall are modelled tick by tick. |
| Fire | 433 | 452 | −4% | The sim runs out of mana (1.4% left; Fireball is 410 mana). The calculator has no mana. |
| Elemental | 411 | 450 | −9% | Out of mana again (2.8% left). The calculator assumes endless 2.5 s Lightning Bolts. |
| Demonology | 619 | — | new | Not in the calculator. About 30% of it is the Imp and Demonic Brand, both built on assumed pet numbers (see gaps). |

Race ranking differs from the calculator for mana-bound specs (Fire, Arcane, Elemental). There, Gnome (+4 Int and Eureka!'s −10% cost) or Dwarf come out on top, and Troll's Berserking is worth less than its −4 Int because extra haste only empties the mana bar sooner.

## Known gaps (read before trusting a number)

- **Coefficients.** Forever coefficients are unknown, except Shadow Bolt 0.857 (Wowhead Forever). Every other coefficient is Classic (C/CU) or a cast-time rule (A) for new spells: Arcane Blast, Arcane Wrath, Ice Lance, Incinerate, Shadow Word: Death. Forever base damage is much lower than Classic, so the coefficients may have been raised. If so, every spec here is under-valued, the high-spell-power specs most.
- **Gear.** Int 260, SP 380, 6% hit, 4% crit and Spirit 120 are all assumptions (A), shared with the calculator. No mp5. No set bonuses, trinkets or on-use items.
- **Demons.** Imp Firebolt damage, cast time and how much of your spell power it gets (15% assumed) are not published. WT-DEMO says demons do about 1/5 of a Warlock's damage; here it is ~30%, so Demonology is likely overstated. Affliction and Destruction run with no demon damage.
- **Conflicts resolved one way.**
  - Wrack is a 6 s channel with "+10% to your other Shadow DoTs" (tooltip). WT-AFF says it makes ticks go at double speed instead.
  - Arcane Blast gives 12% of Int per stack and applies to all spells.
  - Starfire uses Metabot's 490–576 (pre-launch notes say +40%).
  - Wrath 86–96 is very low vs Classic.
  - Lightning Bolt is Classic rank 10 (419–485 assumed, 3.0 s cast).
  - Chain Lightning is 145% of a Lightning Bolt, costs 225% of its mana, 6 s cooldown.
  - Eureka! applies to all classes.
  - Elemental Fury is +100%.
  - Spell crit suppression (1.8%) is applied to match the calculator. Classic did not suppress spell crit.
- **Not modelled.**
  - Partial resists and boss resistances.
  - Movement, target swaps, add phases, the 10 Nov 2026 Warlock hotfix values.
  - Soul Shard limits: Shadowburn on cooldown assumes enough shards.
  - Dark/Demonic Runes, Ice Barrier breaking (assumed to hold), Shadow Word: Death backlash.
  - Bane of Havoc and multi-target.
  - Curse duty for warlocks (the raid curse is assumed to come from someone else).
  - Pushback.
  - DoT clipping by channels: dots are refreshed in their last tick and can fall off during a 6 s Wrack.
- **Fixed constants.** Proc durations that are not published are 15 s (Missile Barrage, Clearcasting); Omen of Clarity is 6% per cast, doubled by Moonkin Form. Vampiric Embrace and Water Shield cost a GCD but no mana.
- **Race stats.** Only Int offsets (from the calculator) and Human +10% Spirit. Skyborne Int is assumed equal to Night Elf.

Every one of these is a tagged entry in `data.json` or a named branch in `specs.py`. Change the value and rerun.
