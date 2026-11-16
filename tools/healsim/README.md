# Healer model (WoW Forever)

Works out the best healing of every healer build at level 60: Priest, Paladin, Druid and Shaman, every race, 21 talent builds, with and without the best craftable healing gear. It also reports the damage each of those builds deals. Python 3.12, standard library only.

```bash
python tools/healsim/run.py                      # all builds, writes results and the wiki data (about 25 s)
python tools/healsim/run.py --classes druid --no-dps
python tools/healsim/builds.py                   # list the builds and check them against the talent trees
python -m unittest discover -s tools/healsim -p "test_*.py"
```

Output:

- `tools/healsim/results/healers.json`: one row per class, build, race and gear set, with the full result of every scenario and mode (cast mix, healing by source, mana flow, inputs and their source tags).
- `docs/assets/data/heal-sim.json`: the compact file that `docs/javascripts/heal-calc.js` draws on `docs/guides/healing-calculator.md`.

## Files

| File | What it holds |
|---|---|
| `model.py` | The linear program, the client data helpers, character stats, one kit per class, the solver and the off-DPS hook. |
| `builds.py` | The 21 builds as tree-valid talent orders, the races per class and `validate()`. |
| `run.py` | Runs everything in parallel processes and writes both JSON files. |
| `test_healsim.py` | Unit tests: the linear program, build validity, budgets, mode order, limits and determinism. |

The model reuses `tools/levelsim`: `core.py` for client data, base stats and characters, `gear.py` for gear (spec key `healer`) and the class modules for off-DPS.

## What it computes

For each build, race, gear set and scenario:

| Mode | Meaning |
|---|---|
| `max` | Highest healing per second with mana ignored, and the seconds until the mana bar is empty at that pace. |
| `fight` | Best healing per second that lasts a 300 s fight: full mana at the start, empty at the end. |
| `endless` | Best healing per second on regeneration alone. |

Scenarios: `tank` (one target takes all the damage) and `group` (a party of 5, everyone hurt).

## The model

It uses expected values, not Monte Carlo. Healing has no hit roll, and the only randomness is crits and procs, so averages lose little.

- **Actions.** Every castable rank of every healing spell is an action with a cast time, a net mana cost and an expected heal: `(base + coefficient × healing power) × talents × (1 + crit × (crit multiplier − 1))`. Heal-over-time spells count their full duration. Party heals count every target they hit in the scenario.
- **Linear program.** Variables are casts per second of each action, plus the share of time spent resting. It maximises healing per second subject to:
    - time: `Σ casts × cast time + rest ≤ 1`;
    - mana (not in `max`): `Σ casts × cost ≤ pool / fight + regen while casting + rest × (regen while resting − regen while casting) + other income`;
    - cooldowns (`casts ≤ 1 / cooldown`), one copy of a heal-over-time spell per target (`casts ≤ targets / duration`, summed over ranks), and links (Swiftmend needs a top-rank Rejuvenation or Regrowth).
    
    `lp_max` is a small dense simplex with Bland's rule.
- **Resting.** Time not spent casting regenerates at the full Spirit rate. The model assumes rest comes in blocks long enough to be outside the 5-second rule.
- **Mix-dependent effects.** These are solved by damped fixed-point iteration around the program: Nature's Grace uptime, the share of Holy Lights sped up by Infusion of Light, Litany of Light (the share of casts that follow a different spell), Renewed Hope (the share of heals on a Weakened Soul target), Riptide's Chain Heal bonus and Water Shield procs.
- **Cooldowns.** Used on cooldown from the pull and averaged over the fight: `floor(fight / cooldown) + 1` uses. In `endless` they are one use per cooldown.
- **Downranking.** All ranks are allowed. `top_rank_only` in the results repeats each number with only the highest rank of each spell.
- **Regeneration.** Spirit regen per 2 s: Priest `12.5 + Spirit / 4`, Paladin and Druid `15 + Spirit / 5`, Shaman `17 + Spirit / 5` (Classic). Meditation, Reverence, Reflection and Mindfulness keep a share while casting. Gear mana per 5 s always counts.
- **Off-DPS.** `off_dps` replaces `talents_at` in the class module of `tools/levelsim` with the build's talents, sets the gear to the healing set, runs each damage rotation of that class for 180 s and keeps the best.

## Builds

`python tools/healsim/builds.py` lists them. Each class has three healing builds and two or three hybrids (a damage or tank build that also heals). `validate()` checks 51 points, maximum ranks, the 5-points-per-row rule and talent prerequisites against `.research/talents` (local only; without it only the point total is checked).

## Known gaps (read before trusting a number)

- **No overhealing.** Every point of healing counts. This favours slow heals and heal-over-time spells more than real fights do.
- **Talent values** come from the launch tooltips, linear per rank (tag A), as in `tools/levelsim`.
- **Values not in the client** are in `CU_VALUES` in `model.py`, each with a tag and a note:
    - Holy Shock's cost at rank 3 (Classic).
    - Light's Vigil's heal at rank 3 and its coefficient (assumed).
    - Oath of Light's bonus for lower ranks (scaled by base heal).
    - Healing Stream, Mana Spring and Mana Tide Totem values (Classic or scaled). One water totem at a time: Healing Stream in `max`, Mana Spring otherwise.
    - Water Shield: one globe at most every 3.5 s.
    - Innervate: Classic. The Forever client does not list it for Druids.
    - Prayer of Mending heals 6 times in a group and once on a lone tank.
    - Chain Heal hits 3 targets at 100%, 50% and 25%.
    - Swiftmend consumes the heal-over-time spell (Classic). It is used on the last tick, so only Bloom is lost.
- **Coefficient penalty.** The client stores `cast time / 3.5` for every rank. The model applies the Classic penalty for spells learned before level 20 (3.75% per level). Forever may differ. If it has no penalty, rank 1 and 2 heals become the best sustained spells.
- **Racials.** Elune's Light, Berserking, Blood Fury and Eureka! are averaged over the fight. Blood Fury and Eureka! are assumed to affect healing. Read Leyline is not modelled.
- **Gear.** `gear.py` picks the healing set with rough stat weights (tag A), not a stat-weight solve. Crafting makes few rings, necks and trinkets.
- **Power Word: Shield** counts its absorb as healing. Divine Aegis counts too.
- **Holy Binding** counts in the group scenario only (the Priest is one of the five).
- **Not modelled:** movement, pushback, damage to the healer, dispels, threat, mana potions, runes, party buffs, Inspiration and Ancestral Healing armor, Lightwell, Lay on Hands, Seal of Light, Judgement of Wisdom, Desperate Prayer, Spirit of Redemption.
- **Circle of Healing, Lifebloom, Nourish, Earth Shield, Divine Light and Healing Rain** exist in the client with no trained rank. The model treats them as not learnable.
