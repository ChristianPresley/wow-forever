"""Rogue: Assassination (Mutilate at 31+ points), Combat and Subtlety, levels 1-60, naked.

Spell values come from forever.json through core helpers. Talent values come from the
Forever client tooltip text (TOOLTIP, tag F) because many client talent ranks above 1
have no effect rows. Where `core.talent_points`' linear fallback disagrees with the
max-rank tooltip, the tooltip wins: Malice (linear 25 vs 5), Lethality (5 ranks/30 vs
2 ranks/20), Ruthlessness (180 vs 60), Efficient Strikes (10 vs 5), Opportunity (50 vs
20), Coup de Grace (60 vs 20), Aggression (6 vs 15), Improved Ambush (135 vs 45),
Initiative (300 vs 100), Vile Poisons (100 vs 20), Improved Poisons (50 vs 10),
Precision (5 ranks vs 3), Relentless Strikes (1 rank in the client, 5 in the tooltip).
Talents the client has under another name or not at all (Puncturing Wounds, Flash of
Steel, Boot Knife, Flawless Execution, Blood Splatter, Venom, Death Mark) use the
tooltip only.

Server-side rules and data the client lacks, tagged:
- Attack power = Str + Agi + 2*level - 20 (CU). Weapon damage adds AP/14 * speed;
  instant attacks use normalized speed 2.4 (CU).
- Weapon requirements are ignored so every spec can be simulated naked: Backstab,
  Ambush, Mutilate and poisons work with the unarmed fist (A). There is no off-hand, so
  Mutilate hits twice with the main-hand fist (A) and dual-wield talents do nothing.
- Energy 10/s (core CU), cap 100 + Vigor. Combo points capped at 5.
- Eviscerate adds 3% AP per combo point (CU). Rupture adds 4% AP per combo point over
  its duration (A). Garrote adds 18% AP over its duration (CU).
- Slice and Dice: 6 s + 3 s per combo point (CU). Rupture: 6 s + 2 s per combo point (CU).
- Shank (Forever): client spells 1329283/1329549 (F), trained at 24 and 44 (A, from
  Warcraft Tavern; the client has no trainer level).
- Poisons are not in the client (C, Wowhead Classic): Instant Poison from 20, 20% chance,
  Deadly Poison from 30 (Assassination only, for Mutilate's poisoned bonus), 30% chance,
  5 stacks over 12 s. Forever AP coefficients 0.01 / 0.009 (C, Warcraft Tavern).
- Death Mark: stores 12% of damage per combo point (Garrote/Rupture twice), cap
  (165 + 102 per extra point) + 4% AP per point, times 1 + crit (tooltip, F), for every rank (A).
- Openers: the fight starts from stealth. Ambush (or Garrote for Subtlety) once, with
  Premeditation when talented (A). Riposte, Setup, Remorseless Attacks, Improved Kidney
  Shot and Preparation do nothing here (the target does not attack or die) (A).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import core  # noqa: E402

CLASS = "rogue"
SPECS = {"assassination": "Assassination", "combat": "Combat", "subtlety": "Subtlety"}

TOOLTIP = {
    "Malice": (5, 5), "Ruthlessness": (60, 3), "Improved Slice and Dice": (45, 3), "Vigor": (10, 2),
    "Blood Splatter": (1, 1), "Lethality": (20, 2), "Vile Poisons": (20, 5), "Cold Blood": (1, 1),
    "Improved Poisons": (10, 5), "Relentless Strikes": (20, 5), "Venom": (30, 1), "Seal Fate": (100, 3),
    "Mutilate": (1, 1), "Coup de Grace": (20, 3), "Efficient Strikes": (5, 2), "Puncturing Wounds": (30, 3),
    "Precision": (3, 3), "Flawless Execution": (15, 1), "Weapon Expertise": (2, 2), "Aggression": (15, 3),
    "Blade Flurry": (20, 1), "Flash of Steel": (15, 5), "Adrenaline Rush": (100, 1),
    "Opportunity": (20, 5), "Improved Ambush": (45, 3), "Initiative": (100, 3), "Premeditation": (2, 1),
    "Serrated Blades": (30, 3), "Ghostly Strike": (125, 1), "Hemorrhage": (15, 1),
    "Boot Knife": (100, 5), "Death Mark": (1, 1),
}

ORDERS = {
    "assassination": [  # Assassination (daggers) leveling -> Assassination (Mutilate) 35/11/5
        ("Malice", 5), ("Ruthlessness", 3), ("Improved Slice and Dice", 2), ("Lethality", 2),
        ("Vigor", 2), ("Improved Slice and Dice", 1), ("Cold Blood", 1), ("Improved Poisons", 4),
        ("Venom", 1), ("Relentless Strikes", 4), ("Seal Fate", 3), ("Relentless Strikes", 1),
        ("Improved Poisons", 1), ("Mutilate", 1), ("Opportunity", 5), ("Coup de Grace", 3),
        ("Efficient Strikes", 2), ("Puncturing Wounds", 3), ("Precision", 3), ("Vile Poisons", 4)],
    "combat": [  # Combat (recommended) leveling -> Combat (raid) 16/35/0
        ("Efficient Strikes", 2), ("Coup de Grace", 3), ("Lightning Reflexes", 3), ("Precision", 3),
        ("Endurance", 2), ("Composure", 2), ("Flawless Execution", 1), ("Aggression", 3),
        ("Weapon Expertise", 1), ("Blade Flurry", 1), ("Hack and Slash", 5),
        ("Dual Wield Specialization", 2), ("Weapon Expertise", 1), ("Flash of Steel", 1),
        ("Adrenaline Rush", 1), ("Flash of Steel", 4), ("Malice", 5), ("Ruthlessness", 3),
        ("Improved Slice and Dice", 3), ("Vigor", 2), ("Lethality", 2), ("Cold Blood", 1)],
    "subtlety": [  # Subtlety (groups) leveling -> Subtlety (bleeds) 16/4/31
        ("Opportunity", 5), ("Camouflage", 3), ("Improved Ambush", 2), ("Serrated Blades", 3),
        ("Initiative", 2), ("Ghostly Strike", 1), ("Initiative", 1), ("Premeditation", 1),
        ("Elusiveness", 2), ("Hemorrhage", 1), ("Preparation", 1), ("Improved Ambush", 1),
        ("Dirty Deeds", 2), ("Boot Knife", 5), ("Death Mark", 1), ("Malice", 5), ("Ruthlessness", 3),
        ("Improved Slice and Dice", 2), ("Lethality", 2), ("Vigor", 2), ("Blood Splatter", 1),
        ("Cold Blood", 1), ("Coup de Grace", 2), ("Efficient Strikes", 2)],
}

# Classic poison ranks (level, avg damage): Wowhead Classic (C)
INSTANT_POISON = [(20, 22), (28, 34), (36, 50), (44, 76), (52, 105), (60, 130)]
DEADLY_POISON = [(30, 36), (38, 52), (46, 80), (54, 108), (60, 136)]  # per stack over 12 s
SHANK_LEVELS = [(24, 1329283), (44, 1329549)]


def talents_at(spec, level):
    pts = max(0, min(level, 60) - 9)
    out = {}
    for name, n in ORDERS[spec]:
        take = min(n, pts)
        if take <= 0:
            break
        out[name] = out.get(name, 0) + take
        pts -= take
    return out


def tal(talents, name):
    r = talents.get(name, 0)
    if not r:
        return 0.0
    v, mx = TOOLTIP[name]
    return v * min(r, mx) / mx


def _spell(name, level):
    return core.best_rank(CLASS, name, level)


def _eff(s, effect, aura=None):
    for e in s["effects"]:
        if e["Effect"] == effect and (aura is None or e["EffectAura"] == aura):
            return e
    return None


def _energy(s):
    for c in s["costs"]:
        if c["PowerType"] == 3:
            return float(c["ManaCost"])
    return 0.0


def _strike(s):
    """(flat bonus, weapon pct) from the client effects: (weapon + flat) * pct."""
    flat, pct = 0.0, 1.0
    for e in s["effects"]:
        if e["Effect"] in (core.NORMALIZED_WEAPON_DMG, core.WEAPON_DAMAGE_NOSCHOOL, core.WEAPON_DAMAGE):
            flat += e["EffectBasePointsF"]
        elif e["Effect"] == core.WEAPON_PERCENT_DAMAGE:
            pct = e["EffectBasePointsF"] / 100
    return flat, pct


def _rank_at(table, level):
    v = None
    for lv, x in table:
        if lv <= level:
            v = x
    return v


def setup(spec, race, level):
    tl = talents_at(spec, level)
    ch = core.Character(CLASS, race, level, tl)
    core.apply_passive_racials(ch, race)
    ch.crit_bonus += tal(tl, "Malice")
    ch.hit += tal(tl, "Precision")
    inp = {"base_stats": ch.stats_tag, "attack_power_formula": "CU", "energy_per_sec": "CU",
           "unarmed_weapon": "CU", "normalized_speed_2.4": "CU", "weapon_requirements_ignored": "A",
           "fight_seconds": "A", "crit_per_agility": "F"}
    for n in tl:
        inp[f"talent:{n}"] = "F" if n in TOOLTIP else "F(no effect modeled)"
    p = {"spec": spec, "level": level, "tl": tl, "ch": ch, "inp": inp}
    p["w_avg"], p["speed"] = core.unarmed_weapon(level)
    ab = {}
    for key, name in (("ss", "Sinister Strike"), ("bs", "Backstab"), ("evis", "Eviscerate"),
                      ("snd", "Slice and Dice"), ("rup", "Rupture"), ("amb", "Ambush"), ("gar", "Garrote")):
        s = _spell(name, level)
        if s:
            ab[key] = s
            inp[name] = "F"
    if tl.get("Mutilate"):
        # The client lists the two per-hand trigger spells under the same name; take the castable one.
        ab["mut"] = [s for s in core.ranks(CLASS, "Mutilate") if s["base_level"] <= level and s["costs"]][-1]
        inp["Mutilate"] = "F"
    if tl.get("Hemorrhage"):
        ab["hemo"] = _spell("Hemorrhage", level)
        inp["Hemorrhage"] = "F"
    if tl.get("Death Mark"):
        ab["dm"] = _spell("Death Mark", level)
        inp["Death Mark (tooltip)"] = "F"
    shank = None
    for lv, sid in SHANK_LEVELS:
        if level >= lv:
            shank = sid
    if shank:
        ab["shank"] = next(s for s in core.data()["classes"][CLASS]["spells"] if s["id"] == shank)
        inp["Shank"] = "F"
        inp["shank_train_level"] = "A"
    p["ab"] = ab
    p["ip"] = _rank_at(INSTANT_POISON, level)
    p["dp"] = _rank_at(DEADLY_POISON, level) if spec == "assassination" else None
    if p["ip"]:
        inp["Instant Poison"] = "C"
    if p["dp"]:
        inp["Deadly Poison"] = "C"
    p["racial"] = core.racial_cooldown(race)
    if p["racial"]:
        inp[f"racial:{race}"] = "F"
    return p


def build(p):
    ch, tl, lv, ab, spec = p["ch"], p["tl"], p["level"], p["ab"], p["spec"]
    speed0 = p["speed"]
    cm = core.A("melee_crit_mult")
    leth_mult = cm + (cm - 1) * tal(tl, "Lethality") / 100
    max_energy = 100 + tal(tl, "Vigor")
    ruth = tal(tl, "Ruthlessness")
    relentless = tal(tl, "Relentless Strikes")
    seal = tal(tl, "Seal Fate")
    isnd = tal(tl, "Improved Slice and Dice") / 100
    cdg = tal(tl, "Coup de Grace") / 100
    aggr = tal(tl, "Aggression") / 100
    opp = tal(tl, "Opportunity") / 100
    pw = tal(tl, "Puncturing Wounds")
    fe = tal(tl, "Flawless Execution")
    es = tal(tl, "Efficient Strikes")
    we = tal(tl, "Weapon Expertise")
    iamb = tal(tl, "Improved Ambush")
    init = tal(tl, "Initiative")
    serr = tal(tl, "Serrated Blades") / 100
    vile = tal(tl, "Vile Poisons") / 100
    ipois = tal(tl, "Improved Poisons")
    venom = tal(tl, "Venom") / 100
    fos = tal(tl, "Flash of Steel")
    boot = tal(tl, "Boot Knife")
    bsplat = tl.get("Blood Splatter", 0)
    racial = p["racial"]
    cost = {k: _energy(s) for k, s in ab.items()}
    if "ss" in cost:
        cost["ss"] -= es
    if "hemo" in cost:
        cost["hemo"] -= es
    if "evis" in cost:
        cost["evis"] -= fe
    if "gar" in cost:
        cost["gar"] -= 10 * tl.get("Dirty Deeds", 0)
    strike = {k: _strike(ab[k]) for k in ("ss", "bs", "amb", "hemo") if k in ab}
    if "mut" in ab:
        trig = [e["trigger"] for e in ab["mut"]["effects"] if e.get("trigger")]
        strike["mut"] = _strike(trig[0]) if trig else (0.0, 0.9)
        mut_poison = (_eff(ab["mut"], core.DUMMY) or {"EffectBasePointsF": 20})["EffectBasePointsF"] / 100
    if "shank" in ab:
        sk = ab["shank"]
        shank_pct = _strike(sk)[1]
        shank_energy = _eff(sk, 30)["EffectBasePointsF"] + fos
        shank_cd = sk["cooldown_ms"] / 1000 - 0.4 * tl.get("Flash of Steel", 0)
    evis = ab.get("evis")
    if evis:
        ee = _eff(evis, core.SCHOOL_DAMAGE)
    snd_haste = _eff(ab["snd"], core.APPLY_AURA, 319)["EffectBasePointsF"] / 100 if "snd" in ab else 0
    if "rup" in ab:
        re_ = _eff(ab["rup"], core.APPLY_AURA, core.PERIODIC_DAMAGE)
    if "gar" in ab:
        ge = _eff(ab["gar"], core.APPLY_AURA, core.PERIODIC_DAMAGE)
        gar_dur = ab["gar"]["duration_ms"] / 1000 + 9 * bsplat
        gar_ticks = int(gar_dur // 3)
    ip, dp = p["ip"], p["dp"]
    use_bs_builder = spec in ("assassination", "subtlety") and "bs" in ab

    def fn(sim):
        rng = sim.rng
        st = {"e": max_energy, "cp": 0, "gcd": 0.0, "snd": -1.0, "rup": -1.0, "gar": -1.0, "ar": -1.0,
              "bf": -1.0, "hemo": -1.0, "venom": -1.0, "racial_until": -1.0, "racial_ready": 0.0,
              "cb_ready": 0.0, "cb": False, "bf_ready": 0.0, "ar_ready": 0.0, "shank_ready": 0.0,
              "dm_ready": 0.0, "dm": None, "dp_stacks": 0, "dp_until": -1.0, "swing_id": 0,
              "stealth": True, "prem_ready": 0.0, "gs_ready": 0.0}

        def ap():
            a = ch.str + ch.agi + 2 * lv - 20
            if racial and racial[0] == "power" and sim.t < st["racial_until"]:
                a *= 1 + racial[1] / 100
            return max(0.0, a)

        def crit_extra():
            return racial[1] if racial and racial[0] == "crit" and sim.t < st["racial_until"] else 0.0

        def mult(direct=True):
            if direct and racial and racial[0] == "direct" and sim.t < st["racial_until"]:
                return 1 + racial[1] / 100
            return 1.0

        def weapon(norm=False):
            return p["w_avg"] * rng.uniform(0.8, 1.2) + ap() / 14 * (2.4 if norm else speed0)

        def deal(name, d, bleed=False):
            sim.deal(name, d)
            dm = st["dm"]
            if dm and sim.t <= dm[0]:
                dm[1] += d * (2 if bleed else 1)

        def roll(white, extra=0.0):
            o = core.melee_roll(rng, ch, white=white, extra_crit=extra + crit_extra())
            if o == "dodge" and we and rng.chance(we / core.A("dodge_same_level") * 100):
                o = "hit"
            return o

        def poison():
            if not ip and not dp:
                return
            ch_bonus = (20 if sim.t < st["venom"] else 0) + ipois
            pm = (1 + vile) * (1 + (venom if sim.t < st["venom"] else 0))
            if dp:
                if rng.chance(30 + ch_bonus):
                    if sim.t >= st["dp_until"]:
                        st["dp_stacks"] = 0
                        sim.at(sim.t + 3.0, dp_tick)
                    st["dp_stacks"] = min(5, st["dp_stacks"] + 1)
                    st["dp_until"] = sim.t + 12.0
            elif rng.chance(20 + ch_bonus):
                o = core.spell_roll(rng, ch, extra_crit=ch.melee_crit - ch.spell_crit)
                if o != "miss":
                    d = (ip + 0.01 * ap()) * pm * mult()
                    deal("Instant Poison", d * (core.A("spell_crit_mult") if o == "crit" else 1))

        def dp_tick():
            if sim.t <= st["dp_until"] + 1e-9 and st["dp_stacks"]:
                pm = (1 + vile) * (1 + (venom if sim.t < st["venom"] else 0))
                deal("Deadly Poison", (dp / 4 + 0.009 * ap()) * st["dp_stacks"] * pm, True)
                if sim.t + 3.0 <= st["dp_until"] + 1e-9:
                    sim.at(sim.t + 3.0, dp_tick)
            else:
                st["dp_stacks"] = 0

        def swing(sid):
            if sid != st["swing_id"]:
                return
            o = roll(True)
            if o not in ("miss", "dodge"):
                d = weapon() * mult()
                d *= cm if o == "crit" else (core.A("glance_damage") if o == "glance" else 1)
                deal("Melee", d)
                poison()
            h = ch.haste
            if sim.t < st["snd"]:
                h *= 1 + snd_haste
            if sim.t < st["bf"]:
                h *= 1.2
            if racial and racial[0] == "haste" and sim.t < st["racial_until"]:
                h *= 1 + racial[1] / 100
            st["swing_id"] += 1
            sim.at(sim.t + speed0 / h, swing, st["swing_id"])

        def regen():
            r = core.A("energy_per_sec") * 2 * (2 if sim.t < st["ar"] else 1)
            st["e"] = min(max_energy, st["e"] + r)
            sim.at(sim.t + 2.0, regen)
            act()

        def add_cp(n):
            st["cp"] = min(5, st["cp"] + n)

        def builder(key, name, dmg, extra_crit=0.0, crit_mult=None, cps=1):
            st["e"] -= cost[key]
            if st["cb"]:
                extra_crit += 100
                st["cb"] = False
            o = roll(False, extra_crit)
            sim.cast(name)
            if o in ("miss", "dodge"):
                st["e"] += cost[key] * 0.8  # Classic: 80% refund on miss/dodge (CU)
                return o
            d = dmg * mult()
            if o == "crit":
                d *= crit_mult or leth_mult
            deal(name, d)
            poison()
            add_cp(cps + (1 if o == "crit" and seal and rng.chance(seal) else 0))
            return o

        def finisher_common(cp):
            if relentless and rng.chance(relentless * cp):
                st["e"] = min(max_energy, st["e"] + 25)
            st["cp"] = 1 if ruth and rng.chance(ruth) else 0

        def gcd():
            st["gcd"] = sim.t + 1.0
            sim.at(st["gcd"], act)

        def rup_tick(until, tick):
            if until == st["rup"] and sim.t <= until + 1e-9:
                deal("Rupture", tick * (1.15 if sim.t < st["hemo"] else 1) * mult(False), True)
                if sim.t + 2.0 <= until + 1e-9:
                    sim.at(sim.t + 2.0, rup_tick, until, tick)

        def gar_tick(until, tick):
            if until == st["gar"] and sim.t <= until + 1e-9:
                deal("Garrote", tick * (1.15 if sim.t < st["hemo"] else 1) * mult(False), True)
                if sim.t + 3.0 <= until + 1e-9:
                    sim.at(sim.t + 3.0, gar_tick, until, tick)

        def dm_fire(rec):
            cp, stored, crit = rec[2], rec[1], ch.melee_crit / 100
            cap = (165 + 102 * (cp - 1) + 0.04 * cp * ap()) * (1 + crit)
            sim.deal("Death Mark", min(stored * 0.12 * cp * (1 + cdg), cap * (1 + cdg)))
            if st["dm"] is rec:
                st["dm"] = None

        def opener():
            st["stealth"] = False
            t = sim.t
            if tl.get("Premeditation"):
                add_cp(2)
                st["prem_ready"] = t + 120
                sim.cast("Premeditation")
            if spec == "subtlety" and "gar" in ab:
                st["e"] -= cost["gar"]
                sim.cast("Garrote")
                add_cp(1 + (1 if init and rng.chance(init) else 0))
                st["gar"] = t + gar_dur
                tick = (ge["EffectBasePointsF"] * (1 + opp) + 0.18 * ap() / gar_ticks)
                sim.at(t + 3.0, gar_tick, st["gar"], tick)
            elif "amb" in ab:
                fl, pct = strike["amb"]
                o = builder("amb", "Ambush", (weapon(True) + fl) * pct * (1 + opp), extra_crit=iamb, crit_mult=cm)
                if o not in ("miss", "dodge") and init and rng.chance(init):
                    add_cp(1)
            gcd()

        def act():
            t = sim.t
            if racial and t >= st["racial_ready"]:
                st["racial_ready"], st["racial_until"] = t + racial[3], t + racial[2]
            if t < st["gcd"]:
                return
            if st["stealth"]:
                return opener()
            if tl.get("Adrenaline Rush") and t >= st["ar_ready"]:
                st["ar_ready"], st["ar"] = t + 300, t + 15
                sim.cast("Adrenaline Rush")
            if tl.get("Cold Blood") and t >= st["cb_ready"] and st["cp"] >= 4:
                st["cb_ready"], st["cb"] = t + 180, True
                sim.cast("Cold Blood")
            e, cp = st["e"], st["cp"]
            if tl.get("Blade Flurry") and t >= st["bf_ready"] and e >= 25:
                st["e"] -= 25
                st["bf_ready"], st["bf"] = t + 120, t + 15
                sim.cast("Blade Flurry")
                return gcd()
            if "shank" in ab and t >= st["shank_ready"] and e >= cost["shank"] and cp < 5:
                st["e"] -= cost["shank"]
                st["shank_ready"] = t + shank_cd
                sim.cast("Shank")
                d = weapon() * shank_pct * mult()
                if rng.chance(ch.melee_crit + crit_extra()):
                    d *= cm
                deal("Shank", d)
                poison()
                st["e"] = min(max_energy, st["e"] + shank_energy)
                if venom:
                    st["venom"] = t + 6
                if boot and rng.chance(boot):
                    add_cp(2)
                return gcd()
            # Finishers
            if "snd" in ab and cp >= 1 and t >= st["snd"] and e >= cost["snd"] and (cp >= 2 or lv < 20):
                st["e"] -= cost["snd"]
                st["snd"] = t + (6 + 3 * cp) * (1 + isnd)
                sim.cast("Slice and Dice")
                finisher_common(cp)
                return gcd()
            if "dm" in ab and cp >= 5 and t >= st["dm_ready"] and e >= cost["dm"] and t < st["rup"]:
                st["e"] -= cost["dm"]
                st["dm_ready"] = t + 10
                rec = [t + 6, 0.0, cp]
                st["dm"] = rec
                sim.at(t + 6, dm_fire, rec)
                sim.cast("Death Mark")
                finisher_common(cp)
                return gcd()
            if "rup" in ab and spec == "subtlety" and cp >= 5 and t >= st["rup"] and e >= cost["rup"]:
                st["e"] -= cost["rup"]
                o = roll(False)
                sim.cast("Rupture")
                if o not in ("miss", "dodge"):
                    dur = 6 + 2 * cp + 6 * bsplat
                    n = int(dur // 2)
                    tick = (re_["EffectBasePointsF"] + re_["EffectPointsPerResource"] * cp + 0.04 * cp * ap() / n) * (1 + serr)
                    st["rup"] = t + dur
                    sim.at(t + 2.0, rup_tick, st["rup"], tick)
                    finisher_common(cp)
                return gcd()
            if evis and cp >= 5 and e >= cost["evis"]:
                st["e"] -= cost["evis"]
                extra = 100 if st["cb"] else 0
                st["cb"] = False
                o = roll(False, extra)
                sim.cast("Eviscerate")
                if o not in ("miss", "dodge"):
                    lo, hi = core.effect_range(ee, lv)
                    d = (rng.uniform(lo, hi) + ee["EffectPointsPerResource"] * cp + 0.03 * cp * ap()) \
                        * (1 + cdg) * (1 + aggr) * mult()
                    deal("Eviscerate", d * (cm if o == "crit" else 1))
                    finisher_common(cp)
                return gcd()
            if cp >= 5:
                return
            # Builders
            if "gs" not in st:
                pass
            if tl.get("Ghostly Strike") and t >= st["gs_ready"] and e >= 40:
                st["gs_ready"] = t + 20
                cost["gs"] = 40
                builder("gs", "Ghostly Strike", weapon(True) * 1.25)
                return gcd()
            if "mut" in ab and e >= cost["mut"]:
                fl, pct = strike["mut"]
                pois = 1 + mut_poison if st["dp_stacks"] > 0 and t < st["dp_until"] else 1
                st["e"] -= cost["mut"]
                sim.cast("Mutilate")
                crit_any = False
                hit_any = False
                for _ in range(2):
                    extra = tal(tl, "Puncturing Wounds") / 2 + (100 if st["cb"] else 0)
                    o = roll(False, extra)
                    if o in ("miss", "dodge"):
                        continue
                    hit_any = True
                    d = (weapon(True) + fl) * pct * (1 + opp) * pois * mult()
                    if o == "crit":
                        d *= leth_mult
                        crit_any = True
                    deal("Mutilate", d)
                    poison()
                st["cb"] = False
                if hit_any:
                    add_cp(2 + (1 if crit_any and seal and rng.chance(seal) else 0))
                else:
                    st["e"] += cost["mut"] * 0.8
                return gcd()
            if "hemo" in ab and e >= cost["hemo"] and t >= st["hemo"] and (t < st["rup"] or t < st["gar"]):
                fl, pct = strike["hemo"]
                if builder("hemo", "Hemorrhage", (weapon(True) + fl) * pct) not in ("miss", "dodge"):
                    st["hemo"] = t + 15
                return gcd()
            if use_bs_builder and "mut" not in ab and (e >= cost["bs"] or "hemo" in ab):
                if e < cost["bs"]:
                    return
                fl, pct = strike["bs"]
                o = builder("bs", "Backstab", (weapon(True) + fl) * pct * (1 + opp), extra_crit=pw)
                if o not in ("miss", "dodge") and pw and rng.chance(45 * tl.get("Puncturing Wounds", 0) / 3):
                    add_cp(1)
                return gcd()
            if "ss" in ab and e >= cost["ss"] and not use_bs_builder:
                fl, pct = strike["ss"]
                builder("ss", "Sinister Strike", (weapon(True) + fl) * pct * (1 + aggr))
                return gcd()

        sim.at(0.0, swing, 0)
        sim.at(0.0, act)
        sim.at(2.0, regen)

    return fn


def simulate(spec, race, level, iterations, seed):
    p = setup(spec, race, level)
    out = core.run_many(build(p), iterations=iterations, seed=seed)
    out["inputs"] = p["inp"]
    return out
