"""Build docs/assets/data/icons.json: which original glyph each ability, talent, tree, stat and gear slot gets.

    python tools/icons/build.py

The glyphs are drawn for this site (tools/icons/glyphs.json, in the style of the class sigils in
overrides/.icons/codex). No game artwork is used. Each name gets a glyph for what it does and a
tint for its spell school:

- abilities: from the Forever client effects (heal, heal over time, party heal, absorb, damage,
  damage over time, weapon strike, mana, totem, dispel, control, shapeshift, resurrection, buff);
- talents: from the talent tooltip (keywords) and the school of its tree. Needs .research/talents
  (local only); without it only the client talents are mapped;
- trees, stats, gear slots and a few simulator source names: fixed tables below.

docs/javascripts/calc-table.js reads the file and puts the glyphs next to names in both calculators.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "tools" / "forever_data" / "forever.json"
RESEARCH = ROOT / ".research" / "talents"
SIGILS = ROOT / "overrides" / ".icons" / "codex"
OUT = ROOT / "docs" / "assets" / "data" / "icons.json"
OUT_ITEMS = ROOT / "docs" / "assets" / "data" / "icons-items.json"
GEAR = ROOT / "tools" / "forever_data" / "craftable_gear.json"
RECIPES = ROOT / "tools" / "professions" / "recipes"
CONTENT = ROOT / "docs" / "content"

CLASSES = ["warrior", "paladin", "hunter", "rogue", "priest", "shaman", "mage", "warlock", "druid"]
RACES = {"Human": "alliance", "Dwarf": "alliance", "Gnome": "alliance", "Night Elf": "alliance", "Skyborne (High Order)": "alliance",
         "High Order Skyborne": "alliance", "Orc": "horde", "Troll": "horde", "Tauren": "horde", "Undead": "horde",
         "Skyborne (Windshaper)": "horde", "Windshaper Skyborne": "horde", "Skyborne HO": "alliance", "Skyborne WS": "horde", "Alliance": "alliance", "Horde": "horde"}
PROFESSIONS = {"Alchemy": ("potion", "nature"), "Blacksmithing": ("anvil", "physical"), "Cooking": ("food", "fire"),
               "Enchanting": ("crystal", "arcane"), "Engineering": ("cog", "physical"), "First Aid": ("heal", "fire"),
               "Fishing": ("hook", "frost"), "Herbalism": ("herb", "nature"), "Leatherworking": ("hide", "physical"),
               "Mining": ("pick", "physical"), "Skinning": ("knife", "physical"), "Tailoring": ("needle", "arcane")}
QUALITY = {"Poor": "physical", "Common": "physical", "Uncommon": "nature", "Good": "nature", "Rare": "frost", "Superior": "frost",
           "Epic": "shadow", 1: "physical", 2: "nature", 3: "frost", 4: "shadow", 5: "fire"}
WEAPON_GLYPH = {"bow": "bow", "gun": "bow", "crossbow": "bow", "wand": "wand", "staff": "wand"}
JEWELRY = {"neck", "finger", "trinket"}

SCHOOLS = {1: "physical", 2: "holy", 4: "fire", 8: "nature", 16: "frost", 32: "shadow", 64: "arcane"}
PRIORITY = ["revive", "totem", "groupheal", "heal", "hot", "shield", "nuke", "dot", "strike", "mana", "cleanse",
            "control", "form", "armor", "buff", "utility"]
ACTIVE = {"revive", "totem", "groupheal", "heal", "hot", "shield", "nuke", "dot", "strike", "form", "mana", "cleanse", "control"}
# Names the rules get wrong (what the thing is known for, not what its first effect is).
OVERRIDES = {
    "Power Infusion": "buff", "Seal of Command": "strike", "Death Wish": "buff", "Bestial Wrath": "pet", "Divine Intervention": "shield",
    "Consecration": "nuke", "Hurricane": "nuke", "Entangling Roots": "control", "Nature's Grasp": "control", "Righteous Fury": "threat",
    "Charge": "strike", "Cheap Shot": "control", "Tiger's Fury": "buff", "Water Shield": "mana", "Fire Nova": "nuke",
    "Lightning Overload": "nuke", "Two-Handed Weapon Specialization": "strike", "Intercept": "strike", "Kidney Shot": "control", "Silent Resolve": "threat",
}
WEAPON = {17, 31, 58, 121}
CONTROL_AURAS = {5, 7, 12, 26, 27, 33}
GROUP_TARGETS = {20, 30, 31, 37, 132}
TREE_SCHOOL = {   # (class, tree) overrides, then tree name
    ("paladin", "Protection"): "holy", ("shaman", "Restoration"): "frost", ("druid", "Restoration"): "nature",
    "Discipline": "holy", "Holy": "holy", "Retribution": "holy", "Shadow Magic": "shadow", "Shadow": "shadow",
    "Affliction": "shadow", "Demonology": "shadow", "Destruction": "fire", "Fire": "fire", "Frost": "frost",
    "Arcane": "arcane", "Balance": "arcane", "Elemental Combat": "nature", "Elemental": "nature",
}
TREE_GLYPH = {
    "Discipline": "shield", "Holy": "heal", "Restoration": "hot", "Protection": "armor", "Feral Combat": "form",
    "Feral": "form", "Beast Mastery": "pet", "Marksmanship": "bow", "Survival": "bow", "Demonology": "pet",
    "Affliction": "dot", "Shadow Magic": "dot", "Shadow": "dot", "Enhancement": "strike", "Retribution": "strike",
    "Arms": "strike", "Fury": "strike", "Combat": "strike", "Assassination": "strike", "Subtlety": "utility",
}
FIXED = {   # stats, gear slots, cast-mix names and simulator sources
    "Healing power": ("heal", "holy"), "Healing": ("heal", "holy"), "Intellect": ("intellect", "arcane"), "Spirit": ("spirit", "frost"),
    "Spell crit": ("crit", "fire"), "Crit rating": ("crit", "fire"), "Mana per 5 seconds": ("mana", "frost"), "Mana per 5 s": ("mana", "frost"),
    "Haste": ("haste", "nature"), "Maximum mana": ("mana", "frost"), "Mana": ("mana", "frost"), "Health": ("health", "fire"),
    "Stamina": ("health", "fire"), "Strength": ("strike", "physical"), "Agility": ("haste", "physical"),
    "Regen casting": ("mana", "frost"), "Regen resting": ("mana", "frost"), "Spell power": ("nuke", "arcane"),
    "Spell damage": ("nuke", "arcane"), "Attack power": ("strike", "physical"), "Hit rating": ("crit", "physical"),
    "Head": ("gear", "physical"), "Shoulders": ("gear", "physical"), "Shoulder": ("gear", "physical"), "Back": ("gear", "physical"),
    "Chest": ("gear", "physical"), "Wrists": ("gear", "physical"), "Wrist": ("gear", "physical"), "Hands": ("gear", "physical"),
    "Waist": ("gear", "physical"), "Legs": ("gear", "physical"), "Feet": ("gear", "physical"), "Neck": ("gem", "arcane"),
    "Trinket": ("gem", "arcane"), "Finger": ("gem", "arcane"), "Main hand": ("strike", "physical"), "Off hand": ("armor", "physical"),
    "Ranged": ("bow", "physical"), "Sustained mix": ("time", "nature"), "Endless mix": ("spirit", "frost"), "Maximum mix": ("energy", "fire"),
    "Melee": ("strike", "physical"), "Melee (unarmed)": ("strike", "physical"), "Wand": ("wand", "arcane"), "Auto Shot": ("bow", "physical"),
    "Windfury": ("strike", "nature"), "Not casting": ("time", "frost"),
    "Ring": ("gem", "arcane"), "Rings": ("gem", "arcane"), "Trinkets": ("gem", "arcane"), "Cloak": ("gear", "physical"), "Shield": ("armor", "physical"),
    "Staff": ("strike", "physical"), "Polearm": ("strike", "physical"), "Sword": ("strike", "physical"), "Axe": ("strike", "physical"),
    "Mace": ("strike", "physical"), "Dagger": ("strike", "physical"), "Fist weapon": ("strike", "physical"), "Weapon": ("strike", "physical"),
    "Two-hand": ("strike", "physical"), "One-hand": ("strike", "physical"), "Bow": ("bow", "physical"), "Gun": ("bow", "physical"),
    "Crossbow": ("bow", "physical"), "Thrown": ("bow", "physical"), "Wand ": ("wand", "arcane"), "Rage": ("energy", "fire"), "Energy": ("energy", "holy"),
}


def classify_spell(s):
    """Glyph for one client spell row, from its effects (and one level of triggered spells)."""
    name, effs = s["name"], []
    for e in s["effects"]:
        effs.append(e)
        if e.get("trigger"):
            effs += e["trigger"]["effects"]
    kinds = {e["Effect"] for e in effs}
    auras = {e["EffectAura"] for e in effs if e["Effect"] in (6, 35)}
    if kinds & {18, 113} or re.search(r"Resurrect|Rebirth|Revive|Redemption|Ancestral Spirit|Reincarnation", name):
        return "revive"
    if "Totem" in name or re.match(r"Call of the (Elements|Ancestors|Spirits)|Totemic", name):
        return "totem"
    heal, hot = bool(kinds & {10, 67}), 8 in auras
    if heal or hot:
        group = any(e.get("ImplicitTarget_0") in GROUP_TARGETS or e.get("EffectChainTargets") for e in effs if e["Effect"] in (10, 6, 35)) or 35 in kinds
        return "groupheal" if group else ("heal" if heal else "hot")
    if 69 in auras:
        return "shield"
    if 2 in kinds:
        return "nuke"
    if auras & {3, 53}:
        return "dot"
    if kinds & WEAPON:
        return "strike"
    if kinds & {30, 137} or 24 in auras:
        return "mana"
    if 38 in kinds or re.match(r"(Cure|Abolish|Cleanse|Purify|Remove|Dispel|Purge)\b", name):
        return "cleanse"
    if auras & CONTROL_AURAS:
        return "control"
    if 36 in auras:
        return "form"
    if 22 in auras or re.search(r"Armor|Resistance|Protection|Shield|Skin", name):
        return "armor"
    if re.search(r"Weapon$", name):
        return "strike"
    if auras or re.match(r"(Blessing|Greater Blessing|Seal|Aspect|Mark|Gift|Prayer|Power Word|Arcane Intellect|Demon|Battle|Inner)", name) or "Aura" in name:
        return "buff"
    return "utility"


def classify_talent(text):
    """Glyph for a talent from its tooltip."""
    t = text.lower()
    rules = [
        (r"mana cost|mana regeneration|restore[sd]? .*mana|gain mana|of your (maximum )?mana", "mana"),
        (r"absorb", "shield"),
        (r"critical", "crit"),
        (r"cast(ing)? time|casting speed|attack speed|cooldown|global cooldown", "haste"),
        (r"\brange\b|radius", "range"),
        (r"periodic .*heal|heal.* over|healing over", "hot"),
        (r"\bheal(s|ed|ing)?\b", "heal"),
        (r"stun|fear|silence|immobil|root|incapacit|interrupt|disorient|snare|slow", "control"),
        (r"armor|damage taken|dodge|parry|block|resist|defense", "armor"),
        (r"intellect", "intellect"), (r"spirit", "spirit"), (r"stamina|health", "health"),
        (r"\brage\b|\benergy\b|combo point|focus", "energy"),
        (r"\bpet\b|demon|imp\b|felhunter|voidwalker|succubus", "pet"),
        (r"totem", "totem"),
        (r"periodic|over \d+ sec|bleed", "dot"),
        (r"melee|weapon|attack power|strike", "strike"),
        (r"damage", "nuke"),
        (r"threat", "threat"),
    ]
    for pattern, glyph in rules:
        if re.search(pattern, t):
            return glyph
    return "buff"


def tree_school(cls, tree):
    return TREE_SCHOOL.get((cls, tree)) or TREE_SCHOOL.get(tree) or "physical"


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    names, trees, by_class = {}, {}, {}
    for cls, c in data["classes"].items():
        mine = by_class.setdefault(cls, {})
        best = {}
        for s in c["spells"]:
            g = classify_spell(s)
            cur = best.get(s["name"])
            if cur is None or PRIORITY.index(g) < PRIORITY.index(cur[0]):
                best[s["name"]] = (g, SCHOOLS.get(s["school_mask"] & -s["school_mask"], "physical") if s["school_mask"] else "physical")
        for n, v in best.items():
            mine[n] = [OVERRIDES.get(n, v[0]), v[1]]
        # talents: live trees with tooltips when available, else the client's
        research = RESEARCH / f"{cls}.json"
        if research.exists():
            talents = [(tr["name"], t["name"], (t.get("rankmax") or t.get("rank1") or (t.get("text") or [""])[-1]))
                       for tr in json.loads(research.read_text(encoding="utf-8", errors="replace"))["trees"] for t in tr["talents"]]
        else:
            talents = [(t["tab"], t["name"], t["ranks"][0]["desc"]) for t in c["talents"]]
        for tree, tname, text in talents:
            school = tree_school(cls, tree)
            trees.setdefault(tree, [TREE_GLYPH.get(tree, "nuke" if school != "physical" else "strike"), school])
            if tname in OVERRIDES:
                mine[tname] = [OVERRIDES[tname], school]
            elif tname in best and best[tname][0] in ACTIVE:   # an active talent: keep the spell's own glyph
                mine[tname] = [best[tname][0], school if best[tname][1] == "physical" else best[tname][1]]
            else:
                mine[tname] = [classify_talent(text), school]
    for full in list(trees):          # "Feral Combat" is also written "Feral", "Elemental Combat" "Elemental"
        first = full.split()[0]
        if " " in full and first not in trees and first not in ("Beast",):
            trees[first] = trees[full]
    for n, v in FIXED.items():
        names[n] = list(v)
    # racial abilities: one glyph each, tinted by faction
    for race in data["races"].values():
        faction = RACES.get(race["name"]) or RACES.get(" ".join(reversed(race["name"].split(" ", 2)))) or "alliance"
        for r in race.get("racials", []):
            names[r["name"].split(" - ")[-1]] = [classify_talent(r.get("desc", "")), faction]
    for cls in CLASSES:
        names[cls.capitalize()] = ["class-" + cls, "c-" + cls]
    for race, faction in RACES.items():
        names[race] = ["class-" + faction, faction]
    for prof, v in PROFESSIONS.items():
        names[prof] = list(v)
    for kind, glyph, tint in (("dungeons", "dungeon", "physical"), ("raids", "raid", "fire"), ("pvp", "pvp", "fire")):
        for f in sorted((CONTENT / kind).glob("*.md")):
            title = re.search(r"^# (.+)$", f.read_text(encoding="utf-8"), re.M)
            if title:
                full = title.group(1).strip()
                # "Excavation Site: Wetlands" is also written "Excavation Site"; "The Barrow Deeps" also "Barrow Deeps"
                for alias in {full, full.split(":")[0].strip(), re.sub(r"^The ", "", full)}:
                    names[alias] = [glyph, tint]

    # crafted items and recipes: a second, larger file loaded only where items are listed
    items = {}
    for it in json.loads(GEAR.read_text(encoding="utf-8"))["items"]:
        w = it.get("weapon")
        glyph = (WEAPON_GLYPH.get(w["type"], "strike") if w else "gem" if it["slot"] in JEWELRY
                 else "armor" if it["slot"] == "shield" else "gear")
        if it.get("profession") == "engineering" and glyph == "gem":
            glyph = "cog"                      # an engineering trinket is a device, not jewelry
        if re.search(r"Bomb|Dynamite|Grenade|Mortar|Charge$", it["name"]):
            glyph = "nuke"
        items[it["name"]] = [glyph, QUALITY.get(it.get("quality"), "physical")]
    for f in sorted(RECIPES.glob("*.json")):
        doc = json.loads(f.read_text(encoding="utf-8"))
        prof = PROFESSIONS.get(doc.get("profession", "").title(), PROFESSIONS.get(f.stem.replace("-", " ").title(), ("buff", "physical")))
        for r in doc.get("recipes", []):
            n = r["name"]
            if n in items or n in names:
                continue
            if re.search(r"Potion|Elixir|Flask|Oil\b|Transmute|Philosopher", n):
                glyph = "potion"
            elif re.search(r"Arrow|Bullet|Shot\b|Shell\b|Quiver|Ammo", n):
                glyph = "bow"
            elif re.search(r"Shoulder|Boots|Gloves|Belt\b|Pants|Leggings|Tunic|Vest\b|Robe|Bracers|Helm|Cloak|Cape\b|Breastplate|Gauntlets|Mantle|Hood\b|Cap\b|Suit\b|Jerkin|Armor$|Bindings|Wristguards|Sash|Girdle|Legguards|Greaves|Sabatons|Shirt|Dress|Mask", n):
                glyph = "gear"
            elif re.search(r"Bomb|Dynamite|Grenade|Mortar|Charge$|Explosive", n):
                glyph = "nuke"
            elif re.search(r"Bag\b|Pouch|Satchel|Quiver", n):
                glyph = "needle"
            elif re.search(r"Bandage|Anti-Venom|Tourniquet", n):
                glyph = "heal"
            elif re.search(r"^Enchant |Wand\b|^Runed .* Rod$", n):
                glyph = "crystal" if n.startswith("Enchant ") else "wand"
            elif re.search(r"Bar\b|Ore\b|Smelt", n):
                glyph = "pick"
            elif re.search(r"Bolt of|Bag\b|Cloth", n):
                glyph = "needle"
            elif re.search(r"^((Light|Medium|Heavy|Thick|Rugged|Cured|Enchanted) )*(Leather|Hide)$|Armor Kit", n):
                glyph = "hide"
            else:
                glyph = prof[0]
            items[n] = [glyph, QUALITY.get(r.get("quality"), "physical")]
    glyphs = {k: v for k, v in json.loads((Path(__file__).parent / "glyphs.json").read_text(encoding="utf-8")).items() if not k.startswith("_")}
    sigils = {}
    for f in sorted(SIGILS.glob("*.svg")):
        inner = re.sub(r"<title>.*?</title>", "", re.search(r"<svg[^>]*>(.*)</svg>", f.read_text(encoding="utf-8"), re.S).group(1))
        sigils[f.stem] = inner.strip()
    every = [v for m in by_class.values() for v in m.values()]
    unknown = sorted({v[0] for v in list(names.values()) + every + list(trees.values()) + list(items.values())
                      if not v[0].startswith("class-")} - set(glyphs))
    if unknown:
        raise SystemExit(f"glyphs missing: {unknown}")
    OUT.write_text(json.dumps({"glyphs": glyphs, "sigils": sigils, "trees": trees, "names": dict(sorted(names.items())),
                               "classes": {c: dict(sorted(m.items())) for c, m in by_class.items()}},
                              separators=(",", ":")), encoding="utf-8")
    OUT_ITEMS.write_text(json.dumps({"names": dict(sorted(items.items()))}, separators=(",", ":")), encoding="utf-8")
    print(f"{len(items)} item and recipe names -> {OUT_ITEMS} ({OUT_ITEMS.stat().st_size // 1024} KB)")
    used = {}
    for v in list(names.values()) + every:
        used[v[0]] = used.get(v[0], 0) + 1
    print(f"{len(names)} general names, {len(every)} class names, {len(trees)} trees, {len(glyphs)} glyphs, {len(sigils)} sigils -> {OUT} ({OUT.stat().st_size // 1024} KB)")
    print(", ".join(f"{k} {n}" for k, n in sorted(used.items(), key=lambda kv: -kv[1])))


if __name__ == "__main__":
    main()
