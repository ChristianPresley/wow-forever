"""Best craftable gear for a class, spec and level.

Reads tools/forever_data/craftable_gear.json (Forever client item data, see GEAR.md)
and fills every slot with the crafted item (and Enchanting recipe) that scores best
for the spec, among items the character can use at that level.

Assumptions (tag A unless noted):
- Hit and crit ratings convert at 10 hit rating = 1% and 14 crit rating = 1%
  (inferred from known items in the Forever client, see GEAR.md).
- An Enchanting recipe is usable when its skill <= 5 * level (the profession cap
  pace while levelling) and its stats decode; procs are ignored.
- A non-unique crafted one-hander may be used in both hands.
- Slot scores use rough spec stat weights below, not a full stat-weight solve.
- Crafting produces almost no rings or necks and few trinkets; empty slots stay empty.
"""
import json
from functools import lru_cache
from pathlib import Path

GEAR_JSON = Path(__file__).resolve().parents[1] / "forever_data" / "craftable_gear.json"
HIT_RATING_PER_PCT = 10
CRIT_RATING_PER_PCT = 14

ARMOR = {  # (armor types before 40, from 40)
    "warrior": ({"cloth", "leather", "mail"}, {"cloth", "leather", "mail", "plate"}),
    "paladin": ({"cloth", "leather", "mail"}, {"cloth", "leather", "mail", "plate"}),
    "hunter": ({"cloth", "leather"}, {"cloth", "leather", "mail"}),
    "shaman": ({"cloth", "leather"}, {"cloth", "leather", "mail"}),
    "rogue": ({"cloth", "leather"},) * 2, "druid": ({"cloth", "leather"},) * 2,
    "mage": ({"cloth"},) * 2, "priest": ({"cloth"},) * 2, "warlock": ({"cloth"},) * 2,
}
WEAPONS = {  # Classic proficiencies (C)
    "warrior": {"axe", "sword", "mace", "dagger", "fist", "axe2h", "sword2h", "mace2h", "polearm", "staff", "gun", "bow", "crossbow", "thrown"},
    "paladin": {"axe", "sword", "mace", "axe2h", "sword2h", "mace2h", "polearm"},
    "hunter": {"axe", "sword", "dagger", "fist", "axe2h", "sword2h", "polearm", "staff", "gun", "bow", "crossbow"},
    "rogue": {"dagger", "sword", "mace", "fist", "gun", "bow", "crossbow", "thrown"},
    "shaman": {"axe", "mace", "dagger", "fist", "axe2h", "mace2h", "staff"},
    "druid": {"mace", "dagger", "fist", "mace2h", "staff", "polearm"},
    "priest": {"mace", "dagger", "staff", "wand"}, "mage": {"sword", "dagger", "staff", "wand"},
    "warlock": {"sword", "dagger", "staff", "wand"},
}
# Weapon layout per spec: "2h", "dw" (dual wield), "1h_shield", "caster" (staff or 1h + off-hand).
LAYOUT = {
    ("warrior", "arms"): "2h", ("warrior", "fury"): "dw", ("warrior", "protection"): "1h_shield",
    ("rogue", "assassination"): "dw", ("rogue", "combat"): "dw", ("rogue", "subtlety"): "dw",
    ("paladin", "retribution"): "2h", ("paladin", "holy"): "1h_shield", ("paladin", "protection"): "1h_shield",
    ("shaman", "enhancement"): "2h", ("hunter", "beast_mastery"): "2h", ("hunter", "marksmanship"): "2h",
    ("hunter", "survival"): "2h", ("druid", "feral"): "2h",
}
DAGGER_MH = {("rogue", "assassination"), ("rogue", "subtlety")}

PHYS = {"str": 2.0, "agi": 2.0, "ap": 1.0, "crit": 20 / CRIT_RATING_PER_PCT, "hit": 15 / HIT_RATING_PER_PCT, "sta": 0.05}
CASTER = {"sp": 1.0, "int": 0.6, "spi": 0.2, "crit": 10 / CRIT_RATING_PER_PCT, "hit": 12 / HIT_RATING_PER_PCT,
          "mp5": 1.5, "sta": 0.02}
SCHOOLS = {
    ("mage", "arcane"): {"arcane"}, ("mage", "fire"): {"fire"}, ("mage", "frost"): {"frost"},
    ("priest", "shadow"): {"shadow"}, ("priest", "holy"): {"holy", "shadow"}, ("priest", "discipline"): {"holy", "shadow"},
    ("warlock", "affliction"): {"shadow"}, ("warlock", "demonology"): {"shadow", "fire"}, ("warlock", "destruction"): {"fire", "shadow"},
    ("druid", "balance"): {"nature", "arcane"}, ("druid", "restoration"): {"nature", "arcane"},
    ("shaman", "elemental"): {"nature", "fire"}, ("shaman", "restoration"): {"nature", "fire"},
}


def weights(cls, spec):
    if (cls, spec) in SCHOOLS:
        return dict(CASTER)
    w = dict(PHYS)
    if cls in ("rogue", "hunter") or (cls, spec) == ("druid", "feral"):
        w["str"], w["agi"] = 1.0, 2.5
    elif cls in ("warrior", "paladin", "shaman"):
        w["str"], w["agi"] = 2.2, 1.2
    if cls == "hunter":
        w["rap"] = 1.0
    if cls == "paladin":
        w["sp"] = 0.4
    return w


@lru_cache(maxsize=None)
def _data():
    return json.loads(GEAR_JSON.read_text(encoding="utf-8"))


def _score(stats, w, schools):
    s = sum(w.get(k, 0) * v for k, v in stats.items() if isinstance(v, (int, float)))
    for sch in schools:  # a school bonus only helps that school's share of the spells
        s += w.get("sp", 0) * stats.get("sp_" + sch, 0) / len(schools)
    return s


def _wscore(item, w, schools, phys):
    s = _score(item["stats"], w, schools)
    wp = item.get("weapon")
    if wp and phys and not wp.get("caster"):
        s += wp["dps"] * 14  # 1 weapon DPS = 14 AP
    return s


ENCHANT_SLOTS = {"bracer": ["wrist"], "chest": ["chest"], "cloak": ["back"], "boots": ["feet"], "gloves": ["hands"],
                 "shield": ["shield"], "2h weapon": ["two_hand"], "weapon": ["one_hand", "main_hand", "two_hand"]}


@lru_cache(maxsize=None)
def select(cls, spec, level):
    """Return {"items": [...], "enchants": [...], "stats": totals, "mh", "oh", "ranged"}."""
    d = _data()
    w = weights(cls, spec)
    phys = (cls, spec) not in SCHOOLS
    schools = SCHOOLS.get((cls, spec), set())
    armor_ok = ARMOR[cls][1 if level >= 40 else 0]
    wpn_ok = WEAPONS[cls]
    usable = []
    for it in d["items"]:
        if it["req_level"] > level:
            continue
        ac = it.get("allowable_class")
        if ac and cls not in ac:
            continue
        wp = it.get("weapon")
        if wp:
            if wp["type"] not in wpn_ok:
                continue
        elif it["armor_type"] in ("cloth", "leather", "mail", "plate") and it["armor_type"] not in armor_ok:
            continue
        elif it["armor_type"] in ("idol", "libram", "totem", "shield", "misc") and it["slot"] in ("relic", "shield"):
            if it["slot"] == "shield" and cls not in ("warrior", "paladin", "shaman"):
                continue
            if it["slot"] == "relic":
                continue  # relic effects are spell modifiers, not stats
        usable.append(it)

    def best(slots, pred=lambda it: True):
        c = [it for it in usable if it["slot"] in slots and pred(it)]
        return max(c, key=lambda it: (_wscore(it, w, schools, phys), it["ilvl"]), default=None)

    chosen = {}
    for slot in ("head", "neck", "shoulder", "back", "chest", "wrist", "hands", "waist", "legs", "feet"):
        it = best({slot})
        if it:
            chosen[slot] = it
    trinkets = sorted((it for it in usable if it["slot"] == "trinket"), key=lambda it: -_score(it["stats"], w, schools))[:2]
    for i, it in enumerate(trinkets):
        if _score(it["stats"], w, schools) > 0:
            chosen[f"trinket{i + 1}"] = it

    layout = LAYOUT.get((cls, spec), "caster")
    melee = lambda it: not (it.get("weapon") or {}).get("caster") or not phys
    if layout == "2h":
        chosen["main_hand"] = best({"two_hand"}, melee)
    elif layout == "dw":
        dag = (lambda it: it["weapon"]["type"] == "dagger") if (cls, spec) in DAGGER_MH else (lambda it: True)
        chosen["main_hand"] = best({"one_hand", "main_hand"}, lambda it: dag(it) and melee(it))
        chosen["off_hand"] = best({"one_hand"}, melee)
    elif layout == "1h_shield":
        chosen["main_hand"] = best({"one_hand", "main_hand"})
        chosen["off_hand"] = best({"shield"})
    else:
        staff = best({"two_hand"})
        one, held = best({"one_hand", "main_hand"}), best({"held_in_off_hand"})
        pair = (_wscore(one, w, schools, False) if one else -1) + (_wscore(held, w, schools, False) if held else 0)
        if staff and _wscore(staff, w, schools, False) >= pair:
            chosen["main_hand"] = staff
        else:
            chosen["main_hand"], chosen["off_hand"] = one, held
    rng = best({"ranged_right", "thrown"})
    if rng:
        chosen["ranged"] = rng
    chosen = {k: v for k, v in chosen.items() if v}

    # Enchants: best usable stat enchant per enchantable slot.
    ench = []
    cap = 5 * level
    for key, slots in ENCHANT_SLOTS.items():
        tgt = next((s for s, it in chosen.items() if it["slot"] in slots), None)
        if not tgt or (key == "weapon" and chosen[tgt]["slot"] == "two_hand"):
            continue
        cands = [e for e in d["enchants"] if e["skill"] <= cap and e["stats"]
                 and e["recipe"].lower().startswith("enchant " + key + " ")]
        if key == "weapon":
            cands = [e for e in cands if not e["recipe"].lower().startswith("enchant 2h")]
        e = max(cands, key=lambda e: _score(e["stats"], w, schools), default=None)
        if e and _score(e["stats"], w, schools) > 0:
            ench.append({"slot": tgt, **e})
            if key == "weapon" and "off_hand" in chosen and chosen["off_hand"].get("weapon"):
                ench.append({"slot": "off_hand", **e})

    tot = {}
    for it in chosen.values():
        for k, v in it["stats"].items():
            tot[k] = tot.get(k, 0) + v
    for e in ench:
        for k, v in e["stats"].items():
            if isinstance(v, (int, float)):
                tot[k] = tot.get(k, 0) + v
    tot["sp_total"] = tot.get("sp", 0) + tot.get("spell_damage", 0)

    def wpn(slot):
        it = chosen.get(slot)
        if not it or not it.get("weapon"):
            return None
        wp = it["weapon"]
        return {"name": it["name"], "avg": (wp["min"] + wp["max"]) / 2, "min": wp["min"], "max": wp["max"],
                "speed": wp["speed"], "type": wp["type"]}

    return {"items": {s: {"id": it["id"], "name": it["name"], "ilvl": it["ilvl"]} for s, it in chosen.items()},
            "enchants": [{"slot": e["slot"], "name": e["name"]} for e in ench],
            "stats": tot, "mh": wpn("main_hand"), "oh": wpn("off_hand"), "ranged": wpn("ranged")}


def spell_power(g, school=None):
    st = g["stats"]
    return st.get("sp_total", 0) + (st.get("sp_" + school, 0) if school else 0)


if __name__ == "__main__":
    import sys
    cls, spec, lv = sys.argv[1], sys.argv[2], int(sys.argv[3])
    print(json.dumps(select(cls, spec, lv), indent=1))
