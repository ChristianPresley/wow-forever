# Level-aware DPS simulator

Simulates the DPS of every class, spec (talent tree) and race at every level from 1 to 60. The character has no gear and fights a level-matched training target with no armor. It has every spell rank and talent point it can have at that level.

## Layout

- `core.py`: shared engine (data lookup, character, attack tables, event loop, racials, assumptions). Owned by the parent session; class modules must not change it. Ask for core changes instead.
- `base_stats.json`: base Strength, Agility, Stamina, Intellect and Spirit for each class, race and level. This is server-side data that the Forever client does not ship.
- `classes/<class>.py`: one module per class. It is the only file a class session edits, plus `classes/test_<class>.py`.
- `gear.py`: best craftable gear for a class, spec and level.
- `run.py`: runs every module for every spec, race, level and gear mode, in parallel. It writes `results/levels.json`, `results/levels_crafted.json` and the build panel files in `docs/assets/data/specs/`.
- `publish.py`: compacts the results into `docs/assets/data/level-sim.json` for the wiki table and chart.
- `audit.py`: coverage audit. It writes `docs/assets/data/level-audit.json` for the wiki's coverage section.
- `test_audit.py`: fails when a cell of the matrix is missing, a damaging class spell is unaccounted for, or a build breaks its talent tree.

## Full rebuild

```bash
python tools/levelsim/run.py          # 20,160 cells, 100 fights each; two to three hours on 16 cores
python tools/levelsim/publish.py
python tools/levelsim/audit.py        # also removes each talent in turn at level 60
cd tools/levelsim && python -m pytest classes test_base_stats.py test_audit.py   # pytest: unittest discovery skips the function tests
```

Caster cells are the slow ones. Mage, Priest, Druid and Shaman casters and the Paladin run several rotation policies per cell and report the best (`best_policy` in `classes/mage.py`, `PLANS` in `classes/paladin.py`). To re-run some classes only, use `--classes mage,priest`: the rows are merged into the result files. Do not start two runs at once, because each rewrites those files when it ends.

Gear (`gear.py`) fills each slot by score. Two rules go beyond the stat weights: hit rating is not valued past the hit cap, and a Combat Rogue's main hand is scored on damage per hit as well as DPS.

## What "complete" means here

The matrix is complete: every class, talent tree, race the class can be, gear mode (none, best craftable) and level from 1 to 60. That is 27 specs, 168 spec and race pairs and 20,160 cells.

Inside a cell, the simulator runs **one talent order and one priority list** for the spec. It does not enumerate other talent allocations or other ability orders. The audit makes the edges visible instead:

- every damaging class spell in the client is used, tested and not chosen, or listed in `audit.EXCLUDED` with a reason. A spell that could add single-target damage and is not in a rotation is marked `untested`;
- every talent of every level 60 build is removed in turn, so a talent with no modelled effect shows as 0;
- talents that no build takes are listed per class;
- all 40 racials are listed in `core.RACIAL_STATUS` with what the simulator does with each.

## Class module contract

Each `classes/<class>.py` exposes:

```python
CLASS = "warrior"                      # key in forever.json
SPECS = {"arms": "Arms", "fury": "Fury", "protection": "Protection"}  # one entry per talent tree

def talents_at(spec: str, level: int) -> dict[str, int]:
    """Talent name -> rank spent at this level (level - 9 points from level 10).
    Follows a sensible leveling order for the spec, ending in its level 60 raid build."""

def simulate(spec: str, race: str, level: int, iterations: int, seed: int) -> dict:
    """Return core.run_many(...) output plus {"inputs": {name: tag}} listing every
    value used and its source tag (F, C, CU, A)."""
```

Rules:
- **Take every spell value from `forever.json`** through `core.best_rank`, `core.damage_effect`, `core.effect_range` and `core.cost`. Never hard-code a number the client has. Spells the server casts for a class spell (a seal's Judgement, Consecration ticks) and ranks the trainer table omits are in the class's `unlinked` list: read them with `core.unlinked(cls, id)` or `core.unlinked_named(cls, name)`.
- **Missing talent ranks:** use `core.talent_points`, which scales linearly from rank 1 and tags the result A.
- **Server-side behaviour** (scripted effects, proc rules, rage formula): if the client lacks it, use the Classic rule. Tag it, and list it in the module docstring.
- **Rotation:** each spec uses a priority list that only includes abilities known at that level.
- **Races:** simulate every race the class can be (`docs/characters/races.md`). Use `core.apply_passive_racials` and `core.racial_cooldown`.
  `core.apply_passive_racials` also handles The Human Spirit (Spirit), Expansive Mind (`ch.mana()`, `ch.resource_cap()` for rage and energy) and Touch of the Grave (a proc inside `Sim.deal`). Name pet damage sources with a `Pet:`-style prefix (`core.PET_PREFIXES`) so they do not trigger it.
- **Pets** (Hunter, Warlock) count toward DPS. Model them from client data where it exists.
- **Determinism:** the same seed gives the same result.
