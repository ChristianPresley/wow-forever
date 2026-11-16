"""Every healer build the model runs: 51 talent points each, listed in a tree-valid order.

A build is (id, name, role, note, {tree: [(talent, points), ...]}). `role` is "healer" for
builds whose first job is healing and "hybrid" for damage or tank builds that also heal.
validate() checks every build against the live Forever trees (.research/talents, local only).
"""
import json
from pathlib import Path

RESEARCH = Path(__file__).resolve().parents[2] / ".research" / "talents"

RACES = {
    "priest": ["human", "dwarf", "gnome", "nelf", "troll", "undead"],
    "paladin": ["human", "dwarf", "undead"],
    "druid": ["nelf", "sho", "tauren", "sws"],
    "shaman": ["dwarf", "orc", "troll", "tauren", "sws"],
}

_DISC20 = [("Twin Disciplines", 5), ("Mental Strength", 5), ("Mental Agility", 3), ("Inner Focus", 1),
           ("Meditation", 3), ("Improved Power Word: Shield", 3)]
_HOLY20 = [("Improved Renew", 3), ("Holy Specialization", 5), ("Divine Fury", 5), ("Inspiration", 3),
           ("Improved Healing", 3), ("Holy Binding", 1)]
_DISC31 = _DISC20 + [("Soul Warding", 1), ("Penance", 1), ("Renewed Hope", 5), ("Divine Aegis", 3), ("Power Infusion", 1)]
_PAL_HOLY31 = [("Spiritual Focus", 5), ("Healing Light", 3), ("Reverence", 2), ("Divine Favor", 1), ("Illumination", 5),
               ("Infusion of Light", 2), ("Oath of Light", 1), ("Divine Strength", 1), ("Holy Shock", 1),
               ("Boundless Light", 2), ("Divine Strength", 2), ("Holy Power", 5), ("Light's Vigil", 1)]
_PAL_HOLY20 = [("Spiritual Focus", 5), ("Healing Light", 3), ("Reverence", 2), ("Divine Favor", 1), ("Illumination", 5),
               ("Infusion of Light", 2), ("Oath of Light", 1), ("Divine Strength", 1)]
_DRU_RESTO20 = [("Heart of the Wild", 5), ("Naturalist", 5), ("Reflection", 3), ("Gift of Nature", 5), ("Bloom", 1),
                ("Nature's Focus", 1)]
_SHA_RESTO20 = [("Improved Healing Wave", 5), ("Tidal Focus", 5), ("Mindfulness", 3), ("Water Shield", 1),
                ("Ancestral Healing", 1), ("Tidal Mastery", 5)]

BUILDS = {
    "priest": [
        ("holy-pom", "Holy (Prayer of Mending)", "healer", "Deep Holy: Spiritual Guidance, Spiritual Healing and Prayer of Mending.",
         {"Discipline": [("Twin Disciplines", 5), ("Mental Strength", 5), ("Mental Agility", 3), ("Inner Focus", 1),
                         ("Meditation", 3), ("Improved Power Word: Shield", 2)],
          "Holy": _HOLY20 + [("Litany of Light", 2), ("Spirit of Redemption", 1), ("Spiritual Guidance", 5),
                             ("Spiritual Healing", 3), ("Prayer of Mending", 1)]}),
        ("holy-nova", "Deep Holy (Holy Nova)", "healer", "As much Holy as possible: adds Holy Nova for party healing, gives up Mental Agility and Inner Focus.",
         {"Discipline": [("Twin Disciplines", 5), ("Mental Strength", 5), ("Meditation", 3)],
          "Holy": [("Twilight Focus", 3)] + _HOLY20 + [("Holy Nova", 1), ("Holy Reach", 2), ("Litany of Light", 2),
                                                       ("Spirit of Redemption", 1), ("Spiritual Guidance", 5),
                                                       ("Spiritual Healing", 3), ("Prayer of Mending", 1)]}),
        ("holy-penance", "Holy / Penance", "healer", "Spiritual Guidance and Spiritual Healing with Penance from Discipline; no Prayer of Mending.",
         {"Discipline": _DISC20 + [("Penance", 1)],
          "Holy": _HOLY20 + [("Spiritual Guidance", 5), ("Spiritual Healing", 3), ("Litany of Light", 2)]}),
        ("disc-pi", "Discipline (Power Infusion)", "healer", "Deep Discipline: Penance, Renewed Hope, Divine Aegis and Power Infusion.",
         {"Discipline": _DISC31, "Holy": _HOLY20}),
        ("disc-guidance", "Discipline / Spiritual Guidance", "healer", "Penance and Renewed Hope with Spiritual Guidance; no Divine Aegis or Power Infusion.",
         {"Discipline": _DISC20 + [("Soul Warding", 1), ("Penance", 1), ("Renewed Hope", 4)],
          "Holy": _HOLY20 + [("Spiritual Guidance", 5)]}),
        ("disc-shadow", "Discipline / Shadow hybrid", "hybrid", "Deep Discipline with Shadow damage talents instead of Holy: the off-damage healer.",
         {"Discipline": _DISC31,
          "Shadow Magic": [("Shadow Focus", 5), ("Spirit Tap", 5), ("Improved Mind Blast", 5), ("Improved Shadow Word: Pain", 2),
                           ("Mind Flay", 1), ("Improved Mind Flay", 2)]}),
    ],
    "paladin": [
        ("holy-crit", "Holy (Light's Vigil) / Retribution", "healer", "Deep Holy with Divine Intellect, Benediction and Conviction for crit.",
         {"Holy": _PAL_HOLY31, "Protection": [("Divine Intellect", 5)],
          "Retribution": [("Benediction", 5), ("Conviction", 3), ("Improved Judgement", 2), ("Sanctified Judgement", 3),
                          ("Pursuit of Justice", 2)]}),
        ("holy-prot", "Holy (Light's Vigil) / Protection", "healer", "Deep Holy with 20 points of Protection for survival; no Conviction.",
         {"Holy": _PAL_HOLY31,
          "Protection": [("Divine Intellect", 5), ("Redoubt", 5), ("Guardian's Favor", 2), ("Precision", 3), ("Toughness", 5)]}),
        ("holy-deep", "Deep Holy (41 points)", "healer", "Every Holy talent that matters plus Improved Seals and Holy Conduit for damage.",
         {"Holy": [("Spiritual Focus", 5), ("Divine Strength", 5), ("Healing Light", 3), ("Reverence", 2), ("Improved Seals", 5),
                   ("Divine Favor", 1), ("Illumination", 5), ("Holy Conduit", 2), ("Infusion of Light", 2), ("Oath of Light", 1),
                   ("Divine Precision", 1), ("Holy Shock", 1), ("Boundless Light", 2), ("Holy Power", 5), ("Light's Vigil", 1)],
          "Protection": [("Divine Intellect", 5), ("Redoubt", 5)]}),
        ("ret-healer", "Retribution hybrid (battle healer)", "hybrid", "20 Holy for Illumination and Oath of Light, deep Retribution for damage.",
         {"Holy": _PAL_HOLY20,
          "Retribution": [("Benediction", 5), ("Conviction", 3), ("Improved Judgement", 2), ("Sanctified Judgement", 3),
                          ("Seal of Command", 1), ("Pursuit of Justice", 2), ("Two-Handed Weapon Specialization", 3),
                          ("Sacred Arbiter", 1), ("Vengeance", 3), ("Repentance", 1), ("Vindication", 1),
                          ("Champion of the Light", 5), ("Unsealed Wrath", 1)]}),
        ("prot-healer", "Protection hybrid (tank healer)", "hybrid", "20 Holy for Illumination and Oath of Light, deep Protection.",
         {"Holy": _PAL_HOLY20,
          "Protection": [("Divine Intellect", 5), ("Redoubt", 5), ("Precision", 3), ("Sacred Duty", 2), ("Templar's Bulwark", 1),
                         ("Shield Specialization", 2), ("Toughness", 2), ("Holy Shield", 1), ("Reckoning", 5),
                         ("Anticipation", 4), ("Shieldsworn", 1)]}),
    ],
    "druid": [
        ("resto-deep", "Deep Restoration (Wild Growth)", "healer", "5/0/46: the whole Restoration tree with Genesis.",
         {"Balance": [("Genesis", 5)],
          "Restoration": [("Nature's Focus", 5), ("Heart of the Wild", 5), ("Naturalist", 5), ("Reflection", 3), ("Subtlety", 3),
                          ("Gift of Nature", 5), ("Bloom", 1), ("Tranquil Spirit", 5), ("Improved Rejuvenation", 3),
                          ("Swiftmend", 1), ("Nature's Swiftness", 1), ("Living Spirit", 3), ("Improved Regrowth", 5),
                          ("Wild Growth", 1)]}),
        ("resto-splendor", "Restoration / Nature's Splendor", "healer", "11/0/40: longer HoTs and Nature's Majesty crit, still with Wild Growth.",
         {"Balance": [("Genesis", 5), ("Nature's Majesty", 2), ("Moonglow", 3), ("Nature's Splendor", 1)],
          "Restoration": _DRU_RESTO20 + [("Tranquil Spirit", 5), ("Improved Rejuvenation", 3), ("Swiftmend", 1),
                                         ("Nature's Swiftness", 1), ("Living Spirit", 3), ("Improved Regrowth", 5),
                                         ("Wild Growth", 1), ("Nature's Focus", 1)]}),
        ("resto-grace", "Regrowth / Nature's Grace", "healer", "21/0/30: Nature's Grace haste from Regrowth crits; no Wild Growth.",
         {"Balance": [("Genesis", 5), ("Nature's Majesty", 2), ("Moonglow", 3), ("Nature's Splendor", 1), ("Improved Moonfire", 2),
                      ("Nature's Reach", 2), ("Insect Swarm", 1), ("Improved Starfire", 4), ("Nature's Grace", 1)],
          "Restoration": _DRU_RESTO20 + [("Improved Rejuvenation", 3), ("Swiftmend", 1), ("Living Spirit", 1),
                                         ("Improved Regrowth", 5)]}),
        ("feral-healer", "Feral hybrid (Natural Instinct)", "hybrid", "0/22/29: Natural Instinct turns Intellect into healing; Cat Form for damage.",
         {"Feral Combat": [("Ferocity", 5), ("Furor", 5), ("Sharpened Claws", 2), ("Savage Fury", 2), ("Shredding Attacks", 3),
                           ("Predatory Strikes", 3), ("Natural Instinct", 2)],
          "Restoration": _DRU_RESTO20 + [("Improved Rejuvenation", 3), ("Swiftmend", 1), ("Living Spirit", 1),
                                         ("Improved Regrowth", 4)]}),
        ("balance-healer", "Balance hybrid (Moonkin)", "hybrid", "31/0/20: a Moonkin that leaves the form to heal.",
         {"Balance": [("Improved Wrath", 5), ("Genesis", 5), ("Nature's Majesty", 2), ("Moonglow", 3), ("Nature's Splendor", 1),
                      ("Improved Moonfire", 2), ("Vengeance", 5), ("Improved Starfire", 2), ("Nature's Grace", 1),
                      ("Moonfury", 4), ("Moonkin Form", 1)],
          "Restoration": _DRU_RESTO20}),
    ],
    "shaman": [
        ("resto-deep", "Deep Restoration (Riptide)", "healer", "0/10/41: Riptide, Mana Tide and Purification with Enhancement Intellect and crit.",
         {"Enhancement": [("Thundering Strikes", 5), ("Ancestral Knowledge", 5)],
          "Restoration": [("Improved Healing Wave", 5), ("Tidal Focus", 5), ("Mindfulness", 3), ("Totemic Focus", 3),
                          ("Ancestral Healing", 3), ("Water Shield", 1), ("Tidal Mastery", 5), ("Restorative Totems", 5),
                          ("Mana Tide Totem", 1), ("Healing Way", 3), ("Nature's Swiftness", 1), ("Purification", 5),
                          ("Riptide", 1)]}),
        ("resto-elemental", "Restoration / Elemental", "healer", "11/0/40: Riptide with Convection, Concussion and Elemental Focus for damage.",
         {"Elemental Combat": [("Convection", 5), ("Concussion", 5), ("Elemental Focus", 1)],
          "Restoration": [("Improved Healing Wave", 5), ("Tidal Focus", 5), ("Mindfulness", 3), ("Totemic Focus", 2),
                          ("Ancestral Healing", 3), ("Water Shield", 1), ("Tidal Mastery", 5), ("Restorative Totems", 5),
                          ("Mana Tide Totem", 1), ("Healing Way", 3), ("Nature's Swiftness", 1), ("Purification", 5),
                          ("Riptide", 1)]}),
        ("resto-quickness", "Restoration / Mental Quickness", "healer", "0/22/29: Mental Quickness turns Intellect into healing; no Riptide.",
         {"Enhancement": [("Thundering Strikes", 5), ("Ancestral Knowledge", 5), ("Mental Dexterity", 3),
                          ("Improved Lightning Shield", 2), ("Toughness", 5), ("Mental Quickness", 2)],
          "Restoration": [("Improved Healing Wave", 5), ("Tidal Focus", 5), ("Mindfulness", 3), ("Water Shield", 1),
                          ("Ancestral Healing", 1), ("Tidal Mastery", 5), ("Mana Tide Totem", 1), ("Healing Way", 3),
                          ("Nature's Swiftness", 1), ("Purification", 4)]}),
        ("enh-healer", "Enhancement hybrid", "hybrid", "0/31/20: a melee Shaman with Mental Quickness and 20 points of Restoration.",
         {"Enhancement": [("Thundering Strikes", 5), ("Ancestral Knowledge", 5), ("Mental Dexterity", 3),
                          ("Improved Lightning Shield", 2), ("Elemental Weapons", 3), ("Shamanistic Focus", 1),
                          ("Anticipation", 1), ("Flurry", 5), ("Stormstrike", 1), ("Mental Quickness", 2),
                          ("Improved Stormstrike", 2), ("Rage of the Farseer", 1)],
          "Restoration": _SHA_RESTO20}),
        ("ele-healer", "Elemental hybrid", "hybrid", "31/0/20: a lightning caster with 20 points of Restoration.",
         {"Elemental Combat": [("Convection", 5), ("Concussion", 5), ("Elemental Alacrity", 3), ("Reverberation", 5),
                               ("Elemental Focus", 1), ("Elemental Warding", 1), ("Call of Thunder", 1),
                               ("Lightning Overload", 3), ("Elemental Reach", 1), ("Elemental Fury", 5),
                               ("Lightning Mastery", 1)],
          "Restoration": _SHA_RESTO20}),
    ],
}


def flat(trees):
    out = {}
    for order in trees.values():
        for name, pts in order:
            out[name] = out.get(name, 0) + pts
    return out


def points(trees):
    return {tree: sum(p for _, p in order) for tree, order in trees.items()}


def validate():
    """Problems with the builds, as strings. Tree rules need .research/talents (skipped if absent)."""
    errs = []
    for cls, builds in BUILDS.items():
        path = RESEARCH / f"{cls}.json"
        trees = {t["name"]: {x["name"]: x for x in t["talents"]} for t in
                 json.loads(path.read_text(encoding="utf-8", errors="replace"))["trees"]} if path.exists() else None
        for bid, name, role, note, spec in builds:
            tag = f"{cls}/{bid}"
            total = sum(points(spec).values())
            if total != 51:
                errs.append(f"{tag}: {total} points, expected 51")
            if trees is None:
                continue
            for tree, order in spec.items():
                if tree not in trees:
                    errs.append(f"{tag}: unknown tree {tree}")
                    continue
                spent, have = 0, {}
                for tname, pts in order:
                    t = trees[tree].get(tname)
                    if not t:
                        errs.append(f"{tag}: {tname} is not in {tree}")
                        continue
                    if spent < 5 * (t["row"] - 1):
                        errs.append(f"{tag}: {tname} (row {t['row']}) taken with {spent} points in {tree}")
                    for req in t.get("requires", []):
                        if have.get(req, 0) < trees[tree][req]["max"]:
                            errs.append(f"{tag}: {tname} needs {req} at max rank first")
                    have[tname] = have.get(tname, 0) + pts
                    if have[tname] > t["max"]:
                        errs.append(f"{tag}: {tname} has {have[tname]} of {t['max']} ranks")
                    spent += pts
    return errs


if __name__ == "__main__":
    problems = validate()
    print("\n".join(problems) or "all builds valid")
    for cls, builds in BUILDS.items():
        for bid, name, role, note, spec in builds:
            print(f"{cls:8} {bid:16} {'/'.join(str(v) for v in points(spec).values()):9} {name}")
