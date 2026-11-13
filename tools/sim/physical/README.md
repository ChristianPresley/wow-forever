# Physical DPS simulator (WoW: Forever)

An event-driven Monte Carlo combat simulator for the physical raid DPS specs, run for every race each class can be. Python 3.12, standard library only.

```bash
python tools/sim/physical/run.py                         # 1000 x 180 s for all 66 spec/race pairs -> tools/sim/results/physical.json
python tools/sim/physical/run.py --only Fury --race orc -n 200 --fight 240 --seed 7 --out -
python tools/sim/physical/run.py --data what-if.json     # same run on an edited copy of data.json
python -m unittest discover -s tools/sim/physical        # 26 tests: attack table, rage/energy, procs, DoTs, swing timers, end to end
```

The full run takes about a minute on 8 cores. Seeds are derived from `--seed` and the spec/race name, so results are reproducible.

## Files

| File | What it is |
|---|---|
| `data.json` | Every numeric input. Each leaf is `[value, tag, source]`. Tags: **F** Forever, **FE** Forever estimate, **C** Classic checked, **CU** Classic unchecked, **A** assumption. Source keys are listed in `_sources`. |
| `engine.py` | Event queue, attack-table rolls, rage formula, swing timers with haste rescaling, DoTs, the `Data` wrapper that logs which inputs a spec read. |
| `specs.py` | Player stats, damage pipeline and one priority APL per spec. |
| `run.py` | CLI, iteration loop, statistics, JSON output. |
| `test_sim.py` | Unit tests. |

## Output

`tools/sim/results/physical.json` is a list with one object per spec + race, in the same shape as the casters file:

`class` (id), `class_name`, `spec`, `race` (id), `race_name`, `build`, `faction`, `dps_mean`, `dps_sd`, `ci95` (95% CI of the mean, 1.96 * sd / sqrt(n)), `iterations`, `fight_seconds`, `breakdown` (ability -> DPS), `data_confidence` and `input_tags`.

`data_confidence` is the share of the inputs that spec actually read during the run that are tagged F or FE. `input_tags` gives the full count per tag.

## Model

**Fight.** One target, level 63, fought from behind, for 180 s (configurable). The last 20% of the fight is the execute phase (A: boss health falls linearly). No movement, no downtime, no threat cap, no consumables.

**Event loop.** A heap of timed events: main-hand, off-hand, ranged and pet swing timers; energy, mana and Anger Management ticks; DoT ticks; Slam and shot casts; haste-buff expiries. An APL heartbeat runs every 0.1 s. GCD is 1.5 s (1.0 s for Rogue and Cat). Haste is not applied to the GCD.

**Swing timers.** The next swing is scheduled at `speed / haste`. When a haste buff starts or ends, the time left on the current swing is rescaled. Haste sources multiply (A: RankedBoost assumes `speed / (1 + haste)`; stacking is unpublished). Flurry gives 3 hasted swing intervals after a crit.

**Attack table** (`engine.roll_white`, `engine.roll_yellow`).
- White swings: one roll. Miss 8% (+19% when dual wielding), dodge 6.5%, glancing 40% at 65% damage, then crit, then hit. Crit is pushed off the table when the table is full.
- Special attacks: two rolls. Miss 8% and dodge 6.5% first, then a separate crit roll on the landed hit. No dual-wield penalty, no glancing.
- Hit from gear and talents is subtracted from miss and floored at 0. Parry and block do not apply (attacking from behind).
- Spells, poisons, Seal procs from Judgement and Earth Shock roll 83% + hit (cap 99%), then crit at x1.5.
- Crit: base 5% + Agility / (20, Rogue 29, Hunter 53) + gear + Leader of the Pack 3% + Moonkin Aura 3% + talents + racials - 1.8% suppression vs +3. Melee and ranged crits do x2.0 plus talent bonuses (Impale, Lethality, Mortal Shots).
- Armor: 3731 - Sunder 2250 - Faerie Fire 2000 - Curse of Recklessness 640 is below 0, so boss armor is 0 and physical damage is unmitigated. This follows from the Forever debuff values (Faerie Fire is -2000 in Forever). Bleeds ignore armor anyway.

**Stats.** Human gear totals from the calculator's gear profiles, plus Classic race offsets, plus raid buffs (Kings +10%, Mark of the Wild, Strength of Earth, Grace of Air, Arcane Brilliance). Melee AP uses the Classic class formulas plus gear AP, Blessing of Might 133 and Battle Shout 139. Battle Shout applies to **every** melee spec, because Forever made shouts raid-wide. Weapon damage is `uniform(min, max) + AP / 14 * speed`. Normalized abilities use 3.3 / 2.4 / 1.7.

**Rage** (`engine.rage_from_damage`). Forever says rage from damage dealt depends on weapon speed and crits give +75% rage, but publishes no formula. The simulator uses a TBC-shaped speed formula on the Classic conversion value c = 230.6:
`rage = 3.75 * damage / c + f * speed / 2`, with f = 3.5 for the main hand and 1.75 for the off hand, capped at `15 * damage / c`, then x1.75 on a crit.
This is tagged A. Setting `rage.model` to `"classic"` switches to `7.5 * damage / c` (Classic) with the same x1.75 on crits. Abilities and Heroic Strike do not generate rage from their damage. Other sources: Anger Management 1 per 3 s, Unbridled Wrath 60% for +1 per weapon hit, Dual Wield Specialization +50% off-hand rage, Bloodrage, Improved Berserker Rage +10, Reckless Swings +5 on the next 4 swings. No rage from damage taken (DPS is not tanking). Rage caps at 100.

**Energy.** 20 per 2 s tick (random phase), x2 under Adrenaline Rush. Max 100, +10 Vigor, +5% for Gnome (Expansive Mind). Shank refunds energy. Shifting Power converts mana to 40 energy.

**Mana.** Pool = base mana + 15 per Intellect. Every 2 s: spirit regen `15 + Spirit / 5` only outside the 5-second rule (or the talent share while casting: Rapid Recuperation, Improved Stormstrike), plus Blessing of Wisdom 40 mp5.

**Procs.** Windfury Totem (20% per landed main-hand hit, including specials, for one extra attack with +246 AP; extra attacks do not chain). Windfury Weapon (Enhancement only, replaces the totem: 20% for 2 extra attacks with +333 x 1.4 AP). Seal of Command 7 PPM (rolls the special-attack table). Instant Poison (main hand) and Deadly Poison (off hand, 5 stacks). Deep Wounds (60% of average main-hand damage over 12 s on any melee crit). Unbridled Wrath. Flurry. Vengeance (+3% per stack, 5 stacks). Hack and Slash sword extra attacks. Bloodthrill Overpower. Elemental Devastation. Deadly Aspects. Undead Touch of the Grave (20%, 15 s ICD, 5% of 4500 health as Shadow).

**DoT refresh.** A refresh resets the duration and tick value but keeps the running tick timer (A), so frequent Deep Wounds refreshes still tick every 3 s.

**Racials.** Human +1% crit. Dwarf +1% hit. Night Elf Elune's Light +10% crit 15 s / 3 min. Orc Blood Fury +10% (total) AP 15 s / 2 min, Command +5% pet damage. Troll Berserking +10% attack speed 15 s / 3 min. Skyborne +2% haste. Gnome Eureka! +10% damage and -10% cost on non-periodic abilities 8 s / 2 min (applied to rage and energy costs: the scope is a conflict in the sources), Expansive Mind +5% max energy. Tauren: no damage racial. Cooldown racials are used on cooldown from the pull (Rogue Gnomes wait until energy is below 60).

## APLs

**Fury (17/34/0, Persuader + Ironwood Blade, Berserker Stance).** Off GCD: racial, Bloodrage (rage <= 70), Death Wish, Recklessness (once, 30 min cooldown), Improved Berserker Rage (rage <= 80). GCD: Reckless Swings on cooldown > Bloodthirst > Whirlwind (if Bloodthirst is more than 1 s away). Heroic Strike replaces the main-hand swing at 50+ rage. Execute phase: Bloodthirst only below 40 rage, otherwise Execute with all rage.

**Arms (33/18/0, Forest Defender's Axe, Battle Stance).** Off GCD: same cooldowns. GCD: Mortal Strike > (execute phase: Execute) > Rend if missing (for Bloodthrill) > Overpower when enabled by a dodge or Bloodthrill > Slam on cooldown (1.0 s cast, does not reset the swing). Heroic Strike at 60+ rage. Whirlwind is not used (it needs Berserker Stance).

**Combat (16/35/0, sword main hand, dagger off hand).** Off GCD: racial, Blade Flurry, Adrenaline Rush (energy < 50). GCD: Slice and Dice at 1+ CP when it is about to drop > at 5 CP: refresh Slice and Dice if under 4 s, else Eviscerate (with Cold Blood) > Shank on cooldown when its 40 energy will not overcap > Sinister Strike.

**Mutilate (35/11/5, daggers).** Same, with Eviscerate at 4+ CP, Shank (25 energy, triggers Venom) and Mutilate as the builder (one avoidance roll for both hands, separate crit rolls, Seal Fate +1 CP if either hand crits).

**Marksmanship (5/46/0, Core Marksman Rifle), with a pet and with Lone Wolf.** Off GCD: racial, Rapid Fire. GCD: Aimed Shot (3 s cast) > Sniper Shot (4 s cast, mana > 25%) > Serpent Sting if missing (mana > 40%) > Multi-Shot (mana > 50%) > Arcane Shot (mana > 50%). Auto Shot waits for a cast to finish and then fires. Mana is the binding limit: Aimed Shot every 6 s alone outspends regen. The Lone Wolf row is the same build with no pet and +20% damage.

**Retribution (12/8/31, Forest Defender's Axe).** Seal of Command up from the pull. Judgement (off GCD) every 8 s, then reseal on the GCD. Hammer of Wrath (instant with Champion of the Light) on cooldown in the execute phase.

**Enhancement (8/35/8, Forest Defender's Axe).** Off GCD: racial, Rage of the Farseer. GCD: Stormstrike on cooldown > Earth Shock inside the Stormstrike debuff while mana stays above 15%.

**Feral Cat (9/32/10).** Off GCD: racial, Shifting Power when energy < 30 and mana allows. GCD: Ferocious Bite at 5 CP (Predatory Discipline: excess energy adds damage but is kept) > Shred.

## Results (1000 x 180 s, seed 1)

Race order within each spec, best first. The 95% CI half-width is at most about +-3.5 DPS, so races closer than about 5 DPS are statistically tied.

| Class | Spec | Races (DPS) | Data confidence |
|---|---|---|---|
| Rogue | Mutilate | Gnome 985 > Undead 984 > Skyborne (W) 982 > Skyborne (HO) 981 > Orc 976 > Night Elf 975 > Human 975 > Troll 974 > Dwarf 972 | 0.59 |
| Rogue | Combat | Gnome 908 > Skyborne (HO) 907 > Undead 906 > Skyborne (W) 904 > Orc 901 > Night Elf 900 > Troll 898 > Dwarf 897 > Human 896 | 0.55 |
| Warrior | Fury | Orc 855 > Undead 855 > Skyborne (W) 855 > Skyborne (HO) 854 > Troll 851 > Human 848 > Dwarf 848 > Gnome 846 > Tauren 844 > Night Elf 842 | 0.53 |
| Hunter | Marksmanship (Lone Wolf) | Skyborne (HO) 848 > Night Elf 847 > Skyborne (W) 846 > Human 843 > Dwarf 837 > Troll 832 > Orc 825 > Tauren 824 | 0.54 |
| Warrior | Arms | Undead 793 > Skyborne (HO) 792 > Orc 792 > Skyborne (W) 790 > Human 790 > Gnome 789 > Tauren 787 > Troll 786 > Dwarf 784 > Night Elf 783 | 0.63 |
| Hunter | Marksmanship (pet) | Skyborne (W) 769 > Night Elf 768 > Skyborne (HO) 768 > Human 766 > Dwarf 763 > Orc 757 > Troll 756 > Tauren 745 | 0.52 |
| Shaman | Enhancement | Skyborne (W) 647 > Dwarf 644 > Orc 642 > Troll 641 > Tauren 634 | 0.44 |
| Druid | Feral (Cat) | Night Elf 553 > Skyborne (HO) 552 > Skyborne (W) 552 > Tauren 547 | 0.50 |
| Paladin | Retribution | Undead 386 > Dwarf 382 > Human 379 | 0.47 |

Racial differences are small (1-3% within a spec). Spec gaps are much larger than race gaps, and they mostly come from assumed gear and unpublished ability values, so read the spec ranking as provisional.

## Sanity check against the analytic calculator

`docs/javascripts/dps-calc.js` (commit 05629e8), averaged over races:

| Spec | Sim | Calculator | Difference |
|---|---|---|---|
| Marksmanship (pet) | 761 | 792 | -4% |
| Enhancement | 642 | 597 | +7% |
| Retribution | 382 | 311 | +23% |
| Arms | 789 | 619 | +28% |
| Combat | 902 | 633 | +43% |
| Fury | 850 | 572 | +49% |
| Feral (Cat) | 551 | 309 | +78% |

The big differences were traced with `--data` what-if runs (Human, 300 iterations each, one input switched off):

- **Battle Shout is raid-wide in Forever**, but the calculator only gives it to Warriors. It is worth +45 DPS to Combat, +45 to Mutilate, +26 to Feral and +21 to Retribution here. This is probably a calculator bug.
- **Shank refunds energy.** With Flash of Steel 5/5, Shank gives 40 energy every 8 s, which is 5 energy per second on top of the 10 per second from ticks. The calculator counts 1.5 per second. Turning the refund off costs Combat 112 DPS.
- **Windfury Totem procs on every main-hand hit**, including Heroic Strike, Mortal Strike, Slam, Overpower and Sinister Strike, and each extra swing makes rage that becomes more Heroic Strikes. The calculator applies it to white swings only and gives none to Rogues or Cats. Switching it off costs Arms 158, Fury 106, Combat 82, Feral 56 and Retribution 53 DPS.
- **Execute phase.** The calculator has no Execute. The last 20% of the fight is worth +86 DPS to Fury, +38 to Arms and +22 to Retribution (Hammer of Wrath).
- **Fury** also gets Deep Wounds, Recklessness, Reckless Swings and real weapons (Persuader and Ironwood Blade instead of the calculator's assumed 2.6 s weapons), and is rarely rage-starved with the speed-based rage model. The Classic rage formula would add another +34 DPS.
- **Feral** also gets Shifting Power (+61 DPS: 40 energy per 8 s while mana lasts), Ferocious Bite, Rend and Tear (+15%, A: another raider keeps a bleed up) and Blood Frenzy extra combo points. The calculator models Shred spam only.
- **Marksmanship and Enhancement** agree within 10%. Hunters are mana-limited in the sim, which the calculator ignores, and that offsets the shots the calculator leaves out.

## Known gaps (what this sim does not know)

Every one of these is either tagged A/CU in `data.json` or not modeled at all.

- **Gear.** All stat totals except the Arms profile are assumptions copied from the calculator. Weapons are real Forever items (warcraftdb tooltips). Hit and crit ratings on Forever gear are not converted (no published conversion); the profiles use flat %.
- **Rage formula.** Shape and constants are assumed (see above). This is the largest single uncertainty for Warriors.
- **Unpublished Forever ability values**, filled from Classic: Eviscerate per-CP values, Ferocious Bite (Classic value, assumed AP part, +25%), Rend, Seal of Command (7 PPM, 70%, 20% SP), Judgement mana, Windfury Weapon (20%, +333 AP, 2 swings), Earth Shock, Multi-Shot, Execute per-rage, Deep Wounds including AP.
- **Not modeled:** Rip, Rake, Tiger's Fury, Omen of Clarity, powershifting (mechanics unpublished); Rupture, Garrote, Expose Armor; Unsealed Wrath (needs seal switching), Holy Strike / Sacred Arbiter, Consecration, Exorcism; Flame Shock, Maelstrom Weapon, Lightning Bolt weaving, Flametongue; Volley, Steady-style weaving, pet abilities beyond one special; Sweeping Strikes and Blade Flurry cleave (single target); Spearing Strike; Enrage (needs taking damage); trinkets, set bonuses, enchants, consumables and Crusader; Death Mark (Subtlety is not a raid build here).
- **Hunter pet.** No Forever or checked Classic pet data exists. The pet is a generic level-60 cat (A), with no player buffs (Forever). The pet build loses to Lone Wolf; treat the pet row as a lower bound.
- **Feral cat weapon.** Cat Form damage uses the calculator's 55 DPS at 1.0 s with a +-20% spread (CU/A).
- **Battle Shout, Blessing of Might, Hawk** are third-party Forever estimates (FE) or tooltip values; Battle Shout raid-wide is a Forever change (CC).
- **Talent builds** are read from the wiki's build links by name; the point-by-point parse of the link strings is approximate (`builds` entries in `data.json`).
- **Eureka!** class scope and resource, **Touch of the Grave** melee chance, **Blood Fury** base vs total AP: all conflicts, chosen as noted in `data.json`.
- **Boss.** Armor 3731 and dodge 6.5% are Classic unchecked values; with the Forever debuffs armor is 0 either way. No Forever data on glancing blows, crit suppression or crit multipliers.
