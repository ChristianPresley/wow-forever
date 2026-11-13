"""Extract WoW Forever client data (DB2 tables) for the DPS simulator.

Source: wago.tools public DB2 CSV export of the Forever client (product "wowf").
    https://wago.tools/db2/<Table>/csv?build=<build>

Usage:
    python tools/forever_data/build.py            # latest wowf build
    python tools/forever_data/build.py 1.60.1.70938

Raw CSVs are cached in tools/forever_data/cache/<build>/ (gitignored).
The compiled, committed output is tools/forever_data/forever.json:
  classes, races, racials, talents (with rank spell ids), class spells with every
  rank (level, cost, cast time, cooldown, duration, effects with base points,
  variance, per-level growth, SP/AP coefficients, aura period), proc rates and
  per-level class tables (crit per Agility, spell crit per Intellect, base mana).

Client data is not the whole game: server-side scripts, combat formulas, base
attributes per level and hotfixes are not in these files.
"""
import csv
import json
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
TABLES = [
    "ChrClasses", "ChrRaces", "ChrRaceRacialAbility", "PlayerExpectedStat", "RaceStat",
    "Talent", "TalentTab", "SkillLine", "SkillLineAbility", "SpellLevels", "Spell", "SpellName",
    "SpellMisc", "SpellCastTimes", "SpellDuration", "SpellCooldowns", "SpellPower",
    "SpellCategories", "SpellAuraOptions", "SpellProcsPerMinute", "SpellEffect",
    "SpellClassOptions", "SpellRange", "SpellShapeshift", "SpellEquippedItems",
]
CLASS_MASK = {1: "warrior", 2: "paladin", 3: "hunter", 4: "rogue", 5: "priest",
              7: "shaman", 8: "mage", 9: "warlock", 11: "druid"}
PLAYER_RACES = {1: "human", 2: "orc", 3: "dwarf", 4: "nelf", 5: "undead", 6: "tauren",
                7: "gnome", 8: "troll"}


def http_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "forever-codex-data-builder"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def fetch(build):
    cache = HERE / "cache" / build
    cache.mkdir(parents=True, exist_ok=True)
    for t in TABLES:
        p = cache / f"{t}.csv"
        if p.exists() and p.stat().st_size > 0:
            continue
        url = f"https://wago.tools/db2/{t}/csv?build={build}"
        req = urllib.request.Request(url, headers={"User-Agent": "forever-codex-data-builder"})
        with urllib.request.urlopen(req, timeout=120) as r:
            p.write_bytes(r.read())
        print("fetched", t)
    return cache


def load(cache, t):
    with open(cache / f"{t}.csv", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def num(x):
    try:
        f = float(x)
        return int(f) if f.is_integer() else round(f, 6)
    except (TypeError, ValueError):
        return x


def by(rows, key):
    out = defaultdict(list)
    for r in rows:
        out[r[key]].append(r)
    return out


def main():
    build = sys.argv[1] if len(sys.argv) > 1 else http_json("https://wago.tools/api/builds/wowf/latest")["version"]
    cache = fetch(build)
    T = {t: load(cache, t) for t in TABLES}

    names = {r["ID"]: r["Name_lang"] for r in T["SpellName"]}
    desc = {r["ID"]: r for r in T["Spell"]}
    misc = {r["SpellID"]: r for r in T["SpellMisc"] if r["DifficultyID"] == "0"}
    cast = {r["ID"]: r for r in T["SpellCastTimes"]}
    dur = {r["ID"]: r for r in T["SpellDuration"]}
    rng = {r["ID"]: r for r in T["SpellRange"]}
    levels = {r["SpellID"]: r for r in T["SpellLevels"] if r["DifficultyID"] == "0"}
    cds = {r["SpellID"]: r for r in T["SpellCooldowns"] if r["DifficultyID"] == "0"}
    cats = {r["SpellID"]: r for r in T["SpellCategories"] if r["DifficultyID"] == "0"}
    auraopt = {r["SpellID"]: r for r in T["SpellAuraOptions"] if r["DifficultyID"] == "0"}
    ppm = {r["ID"]: r for r in T["SpellProcsPerMinute"]}
    power = by(T["SpellPower"], "SpellID")
    effects = by([r for r in T["SpellEffect"] if r["DifficultyID"] == "0"], "SpellID")
    classopt = {r["SpellID"]: r for r in T["SpellClassOptions"]}
    shapes = {r["SpellID"]: r for r in T["SpellShapeshift"]}
    equip = {r["SpellID"]: r for r in T["SpellEquippedItems"]}

    def spell(sid, depth=0):
        sid = str(sid)
        if sid == "0":
            return None
        m = misc.get(sid, {})
        c = cast.get(m.get("CastingTimeIndex", "0"), {})
        d = dur.get(m.get("DurationIndex", "0"), {})
        lv = levels.get(sid, {})
        cd = cds.get(sid, {})
        ao = auraopt.get(sid, {})
        effs = []
        for e in sorted(effects.get(sid, []), key=lambda e: int(e["EffectIndex"])):
            eff = {k: num(e[k]) for k in (
                "EffectIndex", "Effect", "EffectAura", "EffectBasePointsF", "Variance",
                "EffectRealPointsPerLevel", "EffectBonusCoefficient", "BonusCoefficientFromAP",
                "EffectAuraPeriod", "EffectAmplitude", "EffectChainTargets", "EffectTriggerSpell",
                "EffectPointsPerResource", "EffectMechanic", "ImplicitTarget_0")}
            eff["MiscValue"] = [num(e["EffectMiscValue_0"]), num(e["EffectMiscValue_1"])]
            eff["ClassMask"] = [num(e[f"EffectSpellClassMask_{i}"]) for i in range(4)]
            if depth < 1 and eff["EffectTriggerSpell"]:
                eff["trigger"] = spell(eff["EffectTriggerSpell"], depth + 1)
            effs.append(eff)
        out = {
            "id": int(sid), "name": names.get(sid, ""), "rank": desc.get(sid, {}).get("NameSubtext_lang", ""),
            "desc": desc.get(sid, {}).get("Description_lang", ""),
            "base_level": num(lv.get("BaseLevel", 0)), "spell_level": num(lv.get("SpellLevel", 0)),
            "max_level": num(lv.get("MaxLevel", 0)),
            "cast_ms": num(c.get("Base", 0)), "duration_ms": num(d.get("Duration", 0)),
            "duration_per_level": num(d.get("DurationPerLevel", 0)), "max_duration_ms": num(d.get("MaxDuration", 0)),
            "cooldown_ms": num(cd.get("RecoveryTime", 0)), "category_cooldown_ms": num(cd.get("CategoryRecoveryTime", 0)),
            "gcd_ms": num(cd.get("StartRecoveryTime", 0)),
            "category": num(cats.get(sid, {}).get("Category", 0)),
            "school_mask": num(m.get("SchoolMask", 0)),
            "range_max": num(rng.get(m.get("RangeIndex", "0"), {}).get("RangeMax_0", 0)),
            "attributes": [num(m.get(f"Attributes_{i}", 0)) for i in range(17)],
            "costs": [{k: num(p[k]) for k in ("PowerType", "ManaCost", "ManaCostPerLevel", "PowerCostPct", "ManaPerSecond")}
                      for p in sorted(power.get(sid, []), key=lambda p: int(p["OrderIndex"]))],
            "proc": {"chance": num(ao.get("ProcChance", 0)), "charges": num(ao.get("ProcCharges", 0)),
                     "stacks": num(ao.get("CumulativeAura", 0)), "icd_ms": num(ao.get("ProcCategoryRecovery", 0)),
                     "ppm": num(ppm.get(ao.get("SpellProcsPerMinuteID", "0"), {}).get("BaseProcRate", 0)),
                     "type_mask": [num(ao.get("ProcTypeMask_0", 0)), num(ao.get("ProcTypeMask_1", 0))]} if ao else None,
            "class_set": num(classopt.get(sid, {}).get("SpellClassSet", 0)),
            "class_mask": [num(classopt.get(sid, {}).get(f"SpellClassMask_{i}", 0)) for i in range(4)] if sid in classopt else None,
            "shapeshift_mask": num(shapes[sid]["ShapeshiftMask_0"]) if sid in shapes else 0,
            "equip": {k: num(equip[sid][k]) for k in ("EquippedItemClass", "EquippedItemSubclass", "EquippedItemInvTypes")} if sid in equip else None,
            "effects": effs,
        }
        return out

    # Class skill lines and the spells they teach.
    skill = {r["ID"]: r for r in T["SkillLine"]}
    class_spells = defaultdict(dict)
    for r in T["SkillLineAbility"]:
        sl = skill.get(r["SkillLine"])
        if not sl or sl["CategoryID"] != "7" or sl["DisplayName_lang"].startswith("Pet"):
            continue
        mask = int(r["ClassMask"] or 0)
        owners = [c for cid, c in CLASS_MASK.items() if mask & (1 << (cid - 1))] if mask else []
        if not owners:
            continue
        s = spell(r["Spell"])
        if not s or not s["name"]:
            continue
        s["skill_line"] = sl["DisplayName_lang"]
        s["acquire"] = num(r["AcquireMethod"])
        s["supersedes"] = num(r["SupercedesSpell"])
        for o in owners:
            class_spells[o][r["Spell"]] = s

    tabs = {r["ID"]: r for r in T["TalentTab"]}
    talents = defaultdict(list)
    for t in T["Talent"]:
        tab = tabs.get(t["TabID"])
        if not tab:
            continue
        mask = int(tab["ClassMask"] or 0)
        cls = next((c for cid, c in CLASS_MASK.items() if mask & (1 << (cid - 1))), None)
        if not cls:
            continue
        ranks = [int(t[f"SpellRank_{i}"]) for i in range(9) if int(t[f"SpellRank_{i}"] or 0)]
        talents[cls].append({
            "id": int(t["ID"]), "tab": tab["Name_lang"], "tab_order": num(tab["OrderIndex"]),
            "tier": num(t["TierID"]), "column": num(t["ColumnIndex"]),
            "prereq": [num(t[f"PrereqTalent_{i}"]) for i in range(3) if int(t[f"PrereqTalent_{i}"] or 0)],
            "name": names.get(str(ranks[0]), "") if ranks else "",
            "ranks": [spell(sid) for sid in ranks],
        })

    expected = defaultdict(dict)
    for r in T["PlayerExpectedStat"]:
        cls = CLASS_MASK.get(int(r["ClassID"]))
        if cls and r["ContentSetID"] == "0":
            expected[cls][int(r["Level"])] = {
                "base_mana": num(r["BaseMana"]), "hp_per_stamina": num(r["HPPerStamina"]),
                "crit_per_agility": num(r["CritPerAgility"]), "spell_crit_per_intellect": num(r["SpellCritPerIntellect"]),
            }

    races = {}
    for r in T["ChrRaces"]:
        races[r["ID"]] = {"id": int(r["ID"]), "file": r["ClientFileString"], "name": r["Name_lang"]}
    racials = defaultdict(list)
    for r in T["ChrRaceRacialAbility"]:
        racials[r["ChrRacesID"]].append({"name": r["Name_lang"], "desc": r["Description_lang"]})

    out = {
        "source": f"wago.tools DB2 export, product wowf, build {build}",
        "build": build,
        "classes": {c: {"spells": sorted(class_spells[c].values(), key=lambda s: (s["name"], s["base_level"])),
                        "talents": sorted(talents[c], key=lambda t: (t["tab_order"], t["tier"], t["column"])),
                        "expected": expected[c]} for c in CLASS_MASK.values()},
        "races": {rid: dict(r, racials=racials.get(rid, [])) for rid, r in races.items() if racials.get(rid)},
        "race_stat": [{k: num(v) for k, v in r.items()} for r in T["RaceStat"]],
    }
    dest = HERE / "forever.json"
    dest.write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    for c, d in out["classes"].items():
        print(f"{c:8} spells={len(d['spells']):4} talents={len(d['talents']):3} levels={len(d['expected'])}")
    print("races with racials:", ", ".join(r["name"] for r in out["races"].values()))
    print(f"wrote {dest.relative_to(HERE.parents[1])} ({dest.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
