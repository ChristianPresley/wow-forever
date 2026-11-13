# Level-aware DPS simulator

Simulates the DPS of every class, spec (talent tree) and race at every level from 1 to 60. The character has no gear and fights a level-matched training target with no armor. It has every spell rank and talent point it can have at that level.

## Layout

- `core.py`: shared engine (data lookup, character, attack tables, event loop, racials, assumptions). Owned by the parent session; class modules must not change it. Ask for core changes instead.
- `base_stats.json`: base Strength, Agility, Stamina, Intellect and Spirit for each class, race and level. This is server-side data that the Forever client does not ship.
- `classes/<class>.py`: one module per class. It is the only file a class session edits, plus `classes/test_<class>.py`.
- `run.py`: runs every module and writes `results/levels.json`.

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
- **Take every spell value from `forever.json`** through `core.best_rank`, `core.damage_effect`, `core.effect_range` and `core.cost`. Never hard-code a number the client has.
- **Missing talent ranks:** use `core.talent_points`, which scales linearly from rank 1 and tags the result A.
- **Server-side behaviour** (scripted effects, proc rules, rage formula): if the client lacks it, use the Classic rule. Tag it, and list it in the module docstring.
- **Rotation:** each spec uses a priority list that only includes abilities known at that level.
- **Races:** simulate every race the class can be (`docs/characters/races.md`). Use `core.apply_passive_racials` and `core.racial_cooldown`.
- **Pets** (Hunter, Warlock) count toward DPS. Model them from client data where it exists.
- **Determinism:** the same seed gives the same result.
