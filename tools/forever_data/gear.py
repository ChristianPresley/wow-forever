"""Compile every profession-crafted item (and stat enchant) of the Forever client
into tools/forever_data/craftable_gear.json for the DPS simulator.

Usage:
    python tools/forever_data/gear.py [build]      # default: build pinned below

Reuses build.py's fetch/cache helpers. See GEAR.md for how stats, armor and
weapon damage are decoded (this client stores budget percentages, not values).
"""
import json
import math
import sys
from pathlib import Path

import build as B

HERE = Path(__file__).resolve().parent
DEFAULT_BUILD = "1.60.1.70938"
TABLES = [
    "SkillLine", "SkillLineAbility", "SpellName", "SpellEffect", "ItemSparse", "Item",
    "ItemEffect", "ItemXItemEffect", "SpellItemEnchantment", "RandPropPoints",
    "ItemArmorQuality", "ItemArmorTotal", "ItemArmorShield", "ArmorLocation",
    "ItemDamageOneHand", "ItemDamageOneHandCaster", "ItemDamageTwoHand",
    "ItemDamageTwoHandCaster", "ItemDamageRanged", "ItemDamageThrown", "ItemDamageWand",
]
PROFESSIONS = {164: "blacksmithing", 165: "leatherworking", 171: "alchemy",
               197: "tailoring", 202: "engineering", 333: "enchanting"}
# ItemModType ids (modern enum, as used by StatModifier_bonusStat_N)
STAT = {0: "mana", 1: "health", 3: "agi", 4: "str", 5: "int", 6: "spi", 7: "sta",
        12: "defense", 13: "dodge", 14: "parry", 15: "block", 16: "melee_hit", 17: "ranged_hit",
        18: "spell_hit", 19: "melee_crit", 20: "ranged_crit", 21: "spell_crit", 31: "hit",
        32: "crit", 35: "resilience", 36: "haste", 37: "expertise", 38: "ap", 39: "rap",
        41: "healing", 42: "spell_damage", 43: "mp5", 45: "sp", 46: "hp5", 47: "spell_pen",
        48: "block_value",
        # Forever/Classic-era extensions, identified from known items (see GEAR.md)
        50: "bonus_armor", 51: "res_fire", 52: "res_frost", 53: "res_holy", 54: "res_shadow",
        55: "res_nature", 56: "res_arcane", 84: "sp_holy", 85: "sp_fire", 86: "sp_nature",
        87: "sp_frost", 88: "sp_shadow", 89: "sp_arcane", 112: "skill_herbalism",
        113: "skill_mining"}
SLOT = {1: "head", 2: "neck", 3: "shoulder", 4: "shirt", 5: "chest", 6: "waist", 7: "legs",
        8: "feet", 9: "wrist", 10: "hands", 11: "finger", 12: "trinket", 13: "one_hand",
        14: "shield", 15: "ranged", 16: "back", 17: "two_hand", 18: "bag", 19: "tabard",
        20: "chest", 21: "main_hand", 22: "off_hand", 23: "held_in_off_hand", 24: "ammo",
        25: "thrown", 26: "ranged_right", 28: "relic"}
# RandPropPoints column per inventory type (TrinityCore GetRandomPropertyPointsSlot)
BUDGET_COL = {}
for c, invs in {0: (1, 4, 5, 7, 17, 20), 1: (3, 6, 8, 10, 12), 2: (2, 9, 11, 14, 16, 23),
                3: (13, 21, 22), 4: (15, 25, 26, 28)}.items():
    for i in invs:
        BUDGET_COL[i] = c
QUALITY_BUDGET = {2: "Good", 3: "Superior", 4: "Epic", 5: "Epic"}
ARMOR_SUB = {1: "cloth", 2: "leather", 3: "mail", 4: "plate", 6: "shield", 0: "misc",
             7: "libram", 8: "idol", 9: "totem"}
WEAPON_SUB = {0: "axe", 1: "axe2h", 2: "bow", 3: "gun", 4: "mace", 5: "mace2h", 6: "polearm",
              7: "sword", 8: "sword2h", 10: "staff", 13: "fist", 14: "misc", 15: "dagger",
              16: "thrown", 18: "crossbow", 19: "wand", 20: "fishing_pole"}
CLASS_BITS = {1: "warrior", 2: "paladin", 4: "hunter", 8: "rogue", 16: "priest",
              64: "shaman", 128: "mage", 256: "warlock", 1024: "druid"}
# Aura -> stat key for equip-spell resolution
SCHOOL_ALL_SPELL = 126


def aura_stat(e):
    """Return (key, amount) for a passive SpellEffect, or None if unknown."""
    a, m = int(e["EffectAura"] or 0), int(e["EffectMiscValue_0"] or 0)
    v = B.num(e["EffectBasePointsF"])
    if a == 13:  # MOD_DAMAGE_DONE
        if m & SCHOOL_ALL_SPELL == SCHOOL_ALL_SPELL:
            return "sp", v
        names = {2: "holy", 4: "fire", 8: "nature", 16: "frost", 32: "shadow", 64: "arcane"}
        return "sp_" + "_".join(n for b, n in names.items() if m & b) if m & 126 else "phys_dmg", v
    table = {135: "healing", 99: "ap", 124: "rap", 52: "crit", 57: "spell_crit", 54: "hit",
             55: "spell_hit", 47: "parry", 49: "dodge", 51: "block", 158: "block_value",
             71: "spell_crit_school", 34: "health", 35: "mana"}
    if a in table:
        return table[a], v
    if a == 85 and m == 0:
        return "mp5", v
    if a == 29:
        return {0: "str", 1: "agi", 2: "sta", 3: "int", 4: "spi", -1: "all_stats"}.get(m, f"stat{m}"), v
    if a == 30:
        return f"skill_{m}", v
    if a == 22:
        return f"resist_{m}", v
    if a == 189:
        return f"rating_mask_{m}", v
    return None


def skill(sla):
    """Skill to learn the recipe: SLA MinSkillLineRank is 1 for trained/plan recipes in this
    client, so use the orange (TrivialSkillLineRankLow) rank, which equals the classic
    requirement for nearly all recipes."""
    return max(int(sla["MinSkillLineRank"]), int(sla["TrivialSkillLineRankLow"] or 0))


def main():
    build = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_BUILD
    B.TABLES = TABLES
    cache = B.fetch(build)
    T = {t: B.load(cache, t) for t in TABLES}
    names = {r["ID"]: r["Name_lang"] for r in T["SpellName"]}
    effects = B.by([r for r in T["SpellEffect"] if r["DifficultyID"] == "0"], "SpellID")
    sparse = {r["ID"]: r for r in T["ItemSparse"]}
    item = {r["ID"]: r for r in T["Item"]}
    ieff = {r["ID"]: r for r in T["ItemEffect"]}
    item_effects = B.by(T["ItemXItemEffect"], "ItemID")
    rpp = {r["ID"]: r for r in T["RandPropPoints"]}
    aq = {r["ID"]: r for r in T["ItemArmorQuality"]}
    atot = {r["ID"]: r for r in T["ItemArmorTotal"]}
    ashield = {r["ID"]: r for r in T["ItemArmorShield"]}
    aloc = {r["ID"]: r for r in T["ArmorLocation"]}
    dmg = {t: {r["ID"]: r for r in T[t]} for t in TABLES if t.startswith("ItemDamage")}
    enchants = {r["ID"]: r for r in T["SpellItemEnchantment"]}
    unresolved = {}

    def spell_stats(sid):
        out, tags = {}, []
        for e in effects.get(sid, []):
            if e["Effect"] != "6":  # APPLY_AURA
                continue
            r = aura_stat(e)
            if r:
                out[r[0]] = out.get(r[0], 0) + r[1]
            else:
                tags.append(f"aura{e['EffectAura']}")
        return out, tags

    def armor(s, it, q, inv):
        il, sub = s["ItemLevel"], int(it["SubclassID"])
        if it["ClassID"] != "4" or q not in range(7):
            return 0
        if sub == 6:
            return int(ashield[il][f"Quality_{q}"]) if il in ashield else 0
        if inv in (16,):  # cloaks use cloth column
            sub = 1
        col = {1: "Cloth", 2: "Leather", 3: "Mail", 4: "Plate"}.get(sub)
        loc = aloc.get(str(5 if inv == 20 else inv))
        if not col or not loc or il not in atot:
            return 0
        lm = float(loc[{1: "Clothmodifier", 2: "Leathermodifier", 3: "Chainmodifier", 4: "Platemodifier"}[sub]])
        return int(float(atot[il][col]) * lm * float(aq[il][f"Qualitymod_{q}"]) + 0.5)

    def weapon(s, it, q, inv):
        if it["ClassID"] != "2":
            return None
        sub, il = int(it["SubclassID"]), s["ItemLevel"]
        caster = int(s["Flags_1"]) & 0x200
        if sub == 19:
            t = "ItemDamageWand"
        elif sub == 16:
            t = "ItemDamageThrown"
        elif sub in (2, 3, 18):
            t = "ItemDamageRanged"
        elif inv == 17:
            t = "ItemDamageTwoHandCaster" if caster else "ItemDamageTwoHand"
        else:
            t = "ItemDamageOneHandCaster" if caster else "ItemDamageOneHand"
        speed = int(s["ItemDelay"]) / 1000
        row = dmg[t].get(il)
        if not row or not speed:
            return None
        dps = float(row[f"Quality_{q}"])
        var = float(s["DmgVariance"])
        avg = dps * speed
        return {"min": int(avg * (1 - var / 2)), "max": int(avg * (1 + var / 2) + 0.5),
                "speed": speed, "dps": round(dps, 2), "type": WEAPON_SUB.get(sub, sub),
                "caster": bool(caster)}

    items, enchs, seen = [], [], set()
    for sla in T["SkillLineAbility"]:
        prof = PROFESSIONS.get(int(sla["SkillLine"]))
        if not prof:
            continue
        sid = sla["Spell"]
        for e in effects.get(sid, []):
            if e["Effect"] == "24" and e["EffectItemType"] in sparse:
                iid = e["EffectItemType"]
                s, it = sparse[iid], item.get(iid)
                if not it or it["ClassID"] not in ("2", "4") or (iid, sid) in seen:
                    continue
                inv = int(s["InventoryType"])
                if inv in (0, 18, 19, 24, 4):
                    continue
                seen.add((iid, sid))
                q = int(s["OverallQualityID"])
                il = s["ItemLevel"]
                col = BUDGET_COL.get(inv)
                budget = int(rpp[il][f"{QUALITY_BUDGET[q]}_{col}"]) if q in QUALITY_BUDGET and col is not None and il in rpp else 0
                stats, raw = {}, {}
                for n in range(10):
                    st = int(s[f"StatModifier_bonusStat_{n}"])
                    pct = int(s[f"StatPercentEditor_{n}"])
                    if st < 0 or not pct:
                        continue
                    key = STAT.get(st, f"stat{st}")
                    val = math.floor(pct * budget / 10000 + 0.5)
                    stats[key] = stats.get(key, 0) + val
                    raw[st] = pct
                eq = []
                for x in item_effects.get(iid, []):
                    ef = ieff.get(x["ItemEffectID"])
                    if not ef:
                        continue
                    trig = {0: "use", 1: "equip", 2: "proc"}.get(int(ef["TriggerType"]), ef["TriggerType"])
                    sp = ef["SpellID"]
                    entry = {"spell": int(sp), "name": names.get(sp, ""), "trigger": trig}
                    if trig == "equip":
                        res, tags = spell_stats(sp)
                        for k, v in res.items():
                            stats[k] = stats.get(k, 0) + v
                        if tags or not res:
                            entry["unresolved"] = tags or ["no_aura"]
                            unresolved[iid] = s["Display_lang"]
                        else:
                            entry["resolved"] = res
                    eq.append(entry)
                cls = int(s["AllowableClass"])
                sub = int(it["SubclassID"])
                items.append({
                    "id": int(iid), "name": s["Display_lang"], "quality": q, "ilvl": int(il),
                    "req_level": int(s["RequiredLevel"]), "slot": SLOT.get(inv, inv),
                    "armor_type": ARMOR_SUB.get(sub) if it["ClassID"] == "4" else None,
                    "armor": armor(s, it, q, inv), "weapon": weapon(s, it, q, inv),
                    "stats": stats, "stat_pct": raw, "equip_spells": eq,
                    "profession": prof, "skill": skill(sla),
                    "recipe_spell": int(sid),
                    "allowable_class": None if cls in (-1, 0) or cls & 1535 == 1535 else
                    [n for b, n in CLASS_BITS.items() if cls & b],
                })
            elif e["Effect"] == "53" and prof == "enchanting":
                en = enchants.get(e["EffectMiscValue_0"])
                if not en:
                    continue
                st = {}
                for n in range(3):
                    typ, amt, arg = int(en[f"Effect_{n}"]), int(en[f"EffectPointsMin_{n}"]), en[f"EffectArg_{n}"]
                    if typ == 5:
                        k = STAT.get(int(arg), f"stat{arg}")
                        st[k] = st.get(k, 0) + amt
                    elif typ == 3:
                        res, tags = spell_stats(arg)
                        for k, v in res.items():
                            st[k] = st.get(k, 0) + v
                        if tags:
                            st.setdefault("unresolved", []).extend(tags)
                    elif typ == 2:
                        st["weapon_dmg"] = st.get("weapon_dmg", 0) + amt
                    elif typ == 1:
                        st.setdefault("proc_spells", []).append(int(arg))
                    elif typ == 4:
                        st[f"resist_{arg}"] = amt
                if st:
                    enchs.append({"enchant_id": int(en["ID"]), "name": en["Name_lang"],
                                  "recipe_spell": int(sid), "recipe": names.get(sid, ""),
                                  "skill": skill(sla), "stats": st})
    items.sort(key=lambda x: (x["slot"] if isinstance(x["slot"], str) else "", x["ilvl"], x["id"]))
    out = {"build": build, "stat_ids": {str(k): v for k, v in STAT.items()},
           "notes": "stats decoded as round(StatPercentEditor*RandPropPoints[quality][slot]/10000); "
                    "hit/crit are ratings (see GEAR.md); enchants are separate.",
           "items": items, "enchants": enchs}
    p = HERE / "craftable_gear.json"
    p.write_text(json.dumps(out, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    print(f"wrote {p}: {len(items)} items, {len(enchs)} enchants, {len(unresolved)} with unresolved equip spells")
    if True:  # sanity summary
        from collections import defaultdict
        g = defaultdict(list)
        for x in items:
            g[(x["slot"], x["armor_type"] or (x["weapon"] or {}).get("type"))].append(x)
        for k in sorted(g, key=str):
            top = sorted(g[k], key=lambda x: -x["ilvl"])[:2]
            print(k, "|", "; ".join(f"{x['name']} i{x['ilvl']} q{x['quality']} {x['stats']}" for x in top))


if __name__ == "__main__":
    main()
