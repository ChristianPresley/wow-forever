"""Warrior: Arms, Fury and Protection, levels 1-60, naked (unarmed fist, no shield).

Spell values come from forever.json through core helpers. Talent values come from
the Forever client tooltip text (TOOLTIP below, tag F) because many client talent
ranks above 1 have no effect rows and `core.talent_points` scales them linearly.
Where that linear fallback disagrees with the max-rank tooltip, the tooltip wins:
Cruelty (linear 25 vs 5), Improved Rend (45 vs 35), Improved Execute (10 vs 5),
Improved Slam (25 s vs 5 s, and 5 ranks vs 2), Flurry (5 ranks vs 3),
Two-Handed Weapon Specialization (5 vs 3 ranks), Improved Berserker Rage
(20 vs 10 Rage). Talents that the client has under another name or not at all
(Bloodthrill, Reckless Swings, Furious Precision, Focused Rage, Improved Whirlwind,
Gore Drinker, Vanguard, Defiance, Master of Defense) use the tooltip only.

Server-side rules (not in the client), tagged:
- Rage from damage dealt: Classic 1.12 formula R = 15d/(4c) + f*s/2, f = 3.5,
  c = 0.0091107836 L^2 + 3.225598133 L + 4.2652911, capped at 15d/c (C).
  Forever: crits give 75% more Rage (A, the deep-dive headline gives no formula).
  Heroic Strike swings give no Rage (C).
- Attack power = 2*Str + 3*level - 20 (CU). Weapon damage adds AP/14 * speed;
  instant attacks use normalized speed 2.4 (CU).
- Bloodthirst = 45% AP + client base points (C: Wowhead Classic / Forever tooltip).
- Execute = client base + extra Rage * (3 per rank) (CU), usable in the last 20% of
  the fight (target health falls linearly, A).
- Deep Wounds: 20% per rank of average weapon damage over 12 s, ticks every 3 s,
  refreshed by each crit (tooltip, F; tick timing CU).
- Bloodrage: 10 Rage now + 10 over 10 s (CU). Overpower: usable 5 s after a dodge (CU).
- Slam resets the swing timer without Improved Slam (CU). Forever Slam cooldown 15 s (F).
- Enrage, Blood Craze, Revenge, Shield Slam, Shield Specialization, Bastion and the
  weapon-type talents do nothing: the target does not attack and there is no weapon
  or shield (A). Protection fights in Defensive Stance (client: -10% damage).
- Battle Shout is up at the pull (pre-buffed, A) and recast when it ends.
- Charge at the pull gives its client Rage (F) once known (level 4).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import core  # noqa: E402

CLASS = "warrior"
SPECS = {"arms": "Arms", "fury": "Fury", "protection": "Protection"}

# Max-rank tooltip values from the client talent text (.research/talents/warrior.json).
TOOLTIP = {
    "Improved Heroic Strike": (3, 3), "Improved Rend": (35, 3), "Improved Charge": (6, 2),
    "Improved Overpower": (50, 2), "Anger Management": (1, 1), "Deep Wounds": (60, 3),
    "Impale": (20, 2), "Bloodthrill": (20, 2), "Improved Slam": (5, 2),
    "Cruelty": (5, 5), "Unbridled Wrath": (60, 5), "Furious Precision": (10, 3),
    "Dual Wield Specialization": (25, 5), "Improved Execute": (5, 2),
    "Improved Berserker Rage": (10, 2), "Death Wish": (20, 1), "Improved Whirlwind": (2, 2),
    "Flurry": (30, 3), "Reckless Swings": (5, 1), "Improved Bloodrage": (50, 2),
    "Improved Thunder Clap": (6, 3), "Focused Rage": (3, 3), "Bastion": (10, 5),
    "Two-Handed Weapon Specialization": (6, 3), "Weaponmaster": (5, 5), "Enrage": (10, 5),
}

# Leveling orders: (talent, ranks) spent in order, one point per level from 10.
# Each ends in the spec's level 60 raid build in docs/guides/warrior/talents.md.
ORDERS = {
    "arms": [  # Arms (groups) leveling -> Arms (raid) 33/18/0
        ("Improved Rend", 3), ("Improved Heroic Strike", 2), ("Improved Overpower", 2),
        ("Improved Tactical Mastery", 3), ("Anger Management", 1), ("Deep Wounds", 3),
        ("Improved Charge", 1), ("Impale", 2), ("Two-Handed Weapon Specialization", 3),
        ("Sweeping Strikes", 1), ("Bloodthrill", 2), ("Weaponmaster", 2), ("Improved Slam", 2),
        ("Weaponmaster", 3), ("Mortal Strike", 1), ("Cruelty", 5), ("Unbridled Wrath", 5),
        ("Enrage", 5), ("Reckless Swings", 1), ("Improved Execute", 2), ("Improved Charge", 1),
        ("Improved Heroic Strike", 1)],
    "fury": [  # Fury (2 weapons) leveling -> Fury (raid) 17/34/0
        ("Cruelty", 5), ("Unbridled Wrath", 5), ("Enrage", 4), ("Furious Precision", 3),
        ("Dual Wield Specialization", 3), ("Death Wish", 1), ("Dual Wield Specialization", 2),
        ("Reckless Swings", 1), ("Improved Execute", 1), ("Flurry", 3), ("Improved Whirlwind", 2),
        ("Bloodthirst", 1), ("Improved Execute", 1), ("Improved Berserker Rage", 2),
        ("Improved Rend", 3), ("Improved Heroic Strike", 3), ("Improved Charge", 2),
        ("Improved Tactical Mastery", 3), ("Anger Management", 1), ("Deep Wounds", 3), ("Impale", 2)],
    "protection": [  # Protection (solo) leveling -> Protection (tank) 5/5/41
        ("Shield Specialization", 5), ("Improved Revenge", 3), ("Improved Bloodrage", 2),
        ("Master of Defense", 2), ("Improved Thunder Clap", 3), ("Vanguard", 1), ("Last Stand", 1),
        ("Defiance", 3), ("Focused Rage", 3), ("Concussion Blow", 1), ("Anticipation", 1),
        ("Bastion", 5), ("Shield Slam", 1), ("Cruelty", 5), ("Deflection", 5), ("Anticipation", 4),
        ("Improved Shield Bash", 2), ("Improved Shield Wall", 2), ("Improved Sunder Armor", 2)],
}


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


def rage_conv(level):
    return 0.0091107836 * level * level + 3.225598133 * level + 4.2652911


def _spell(name, level):
    return core.best_rank(CLASS, name, level)


def _cd(s, default=0.0):
    ms = s["cooldown_ms"] or s["category_cooldown_ms"]
    return ms / 1000 if ms else default


def _rage_cost(s):
    for c in s["costs"]:
        if c["PowerType"] == 1:
            return c["ManaCost"] / 10
    return 0.0


def _eff(s, effect):
    for e in s["effects"]:
        if e["Effect"] == effect:
            return e
    return None


def setup(spec, race, level):
    """Everything that does not change during a fight, plus the inputs/tags list."""
    tl = talents_at(spec, level)
    ch = core.Character(CLASS, race, level, tl)
    core.apply_passive_racials(ch, race)
    inp = {"base_stats": ch.stats_tag, "attack_power_formula": "CU", "rage_formula": "C",
           "rage_crit_bonus_75pct": "A", "unarmed_weapon": "CU", "normalized_speed_2.4": "CU",
           "fight_seconds": "A", "execute_phase_last_20pct": "A", "crit_per_agility": "F"}
    for n in tl:
        inp[f"talent:{n}"] = "F" if n in TOOLTIP else "F(no effect modeled)"
    p = {"level": level, "spec": spec, "tl": tl, "ch": ch, "inp": inp}
    w_avg, speed = core.unarmed_weapon(level)
    p["w_avg"], p["speed"] = w_avg, speed
    # Stance
    stance = "battle"
    if spec == "fury" and level >= 30:
        stance = "berserker"
    if spec == "protection" and level >= 10:
        stance = "defensive"
    p["stance"] = stance
    dmg_mult = 1.0
    if stance == "berserker":
        sp = _spell("Berserker Stance Passive", level)
        for e in sp["effects"]:
            if e["EffectAura"] == 290:
                ch.crit_bonus += e["EffectBasePointsF"]
        inp["Berserker Stance Passive"] = "F"
    if stance == "defensive":
        sp = _spell("Defensive Stance Passive", level)
        for e in sp["effects"]:
            if e["EffectAura"] == 79:
                dmg_mult *= 1 + e["EffectBasePointsF"] / 100
        inp["Defensive Stance Passive"] = "F"
    ch.crit_bonus += tal(tl, "Cruelty")
    p["dmg_mult"] = dmg_mult
    p["crit_mult_yellow"] = core.A("melee_crit_mult") + (core.A("melee_crit_mult") - 1) * tal(tl, "Impale") / 100
    p["focused"] = tal(tl, "Focused Rage")
    # Battle Shout AP
    bs = _spell("Battle Shout", level)
    p["bs_ap"] = core.effect_value(bs["effects"][0], level, bs["spell_level"]) if bs else 0.0
    p["bs_cost"] = _rage_cost(bs) if bs else 0
    if bs:
        inp["Battle Shout"] = "F"
    ch_spell = _spell("Charge", level)
    p["charge_rage"] = (_eff(ch_spell, 30)["EffectBasePointsF"] / 10 + tal(tl, "Improved Charge")) if ch_spell else 0.0
    if ch_spell:
        inp["Charge"] = "F"
    # Abilities known at this level, filtered by stance and spec
    ab = {}

    def add(key, name, need_talent=None, stances=None):
        s = _spell(name, level)
        if not s or (need_talent and not tl.get(need_talent)) or (stances and stance not in stances):
            return None
        ab[key] = s
        inp[name] = "F"
        return s

    add("hs", "Heroic Strike")
    add("rend", "Rend")
    add("op", "Overpower", stances=("battle",))
    add("ms", "Mortal Strike", need_talent="Mortal Strike")
    add("bt", "Bloodthirst", need_talent="Bloodthirst")
    add("ww", "Whirlwind", stances=("berserker",))
    add("slam", "Slam")
    add("exe", "Execute")
    add("tc", "Thunder Clap", stances=("battle", "defensive"))
    add("br", "Bloodrage")
    add("bzr", "Berserker Rage", stances=("berserker",))
    add("reck", "Recklessness", stances=("berserker",))
    if "exe" in ab and ab["exe"]["id"] == 20647:  # level-1 damage trigger, not the trained spell
        del ab["exe"]
    p["ab"] = ab
    if "exe" in ab:
        inp["execute_extra_rage_mult_CU"] = "CU"
        p["exe_rank"] = [s["id"] for s in core.ranks(CLASS, "Execute") if s["id"] != 20647].index(ab["exe"]["id"]) + 1
    if "bt" in ab:
        inp["bloodthirst_45pct_AP"] = "C"
    if "rend" in ab:
        r = ab["rend"]
        p["rend_tick"] = _eff(r, 6)["EffectBasePointsF"] * (1 + tal(tl, "Improved Rend") / 100)
        p["rend_dur"] = r["duration_ms"] / 1000
    if tl.get("Deep Wounds"):
        inp["deep_wounds_tick_3s"] = "CU"
    p["racial"] = core.racial_cooldown(race)
    if p["racial"]:
        inp[f"racial:{race}"] = "F"
    return p


def build(p):
    ch, tl, lv = p["ch"], p["tl"], p["level"]
    ab = p["ab"]
    conv = rage_conv(lv)
    speed0 = p["speed"]
    melee_mult = core.A("melee_crit_mult")
    flurry = tal(tl, "Flurry") / 100
    uw = tal(tl, "Unbridled Wrath")
    am = tal(tl, "Anger Management")
    dw_pct = tal(tl, "Deep Wounds") / 100
    bthrill = tal(tl, "Bloodthrill")
    rs_bonus = tal(tl, "Reckless Swings")
    islam = tal(tl, "Improved Slam")
    exe_red = tal(tl, "Improved Execute")
    hs_red = tal(tl, "Improved Heroic Strike")
    tc_red = tal(tl, "Improved Thunder Clap")
    iop = tal(tl, "Improved Overpower")
    dwish = tal(tl, "Death Wish") / 100
    ibzr = tal(tl, "Improved Berserker Rage")
    ibr = tal(tl, "Improved Bloodrage") / 100
    iww = tal(tl, "Improved Whirlwind")
    focused = p["focused"]

    def cost(key, extra_red=0.0):
        return max(0.0, _rage_cost(ab[key]) - extra_red - (focused if key not in ("br", "bzr", "reck") else 0))

    costs = {k: cost(k) for k in ab}
    if "hs" in ab:
        costs["hs"] = cost("hs", hs_red)
    if "exe" in ab:
        costs["exe"] = cost("exe", exe_red)
    if "tc" in ab:
        costs["tc"] = cost("tc", tc_red)
    cds = {k: _cd(ab[k]) for k in ab}
    if "slam" in ab:
        cds["slam"] = max(0.0, (cds["slam"] or 15.0) - islam)
        slam_cast = ab["slam"]["cast_ms"] / 1000 - 0.25 * min(2, tl.get("Improved Slam", 0))
    if "ww" in ab:
        cds["ww"] = max(0.0, (cds["ww"] or 10.0) - iww)
    flat = {}
    for k in ("hs", "slam", "ms", "op"):
        if k in ab:
            e = _eff(ab[k], core.WEAPON_DAMAGE_NOSCHOOL) or _eff(ab[k], core.NORMALIZED_WEAPON_DMG)
            flat[k] = e["EffectBasePointsF"] if e else 0.0
    bt_base = _eff(ab["bt"], core.SCHOOL_DAMAGE)["EffectBasePointsF"] if "bt" in ab else 0
    exe_base = _eff(ab["exe"], core.DUMMY)["EffectBasePointsF"] if "exe" in ab else 0
    exe_per = 3 * p.get("exe_rank", 0)
    tc_e = _eff(ab["tc"], core.SCHOOL_DAMAGE) if "tc" in ab else None
    racial = p["racial"]

    def fn(sim):
        rng = sim.rng
        end = sim.end
        st = {"rage": min(100.0, p["charge_rage"]), "gcd": 0.0, "next_swing": 0.0, "hs_q": False,
              "flurry": 0, "op_until": -1.0, "rend_until": -1.0, "dw_until": -1.0, "dw_tick": 0.0,
              "bs_until": 120.0 if p["bs_ap"] else -1, "dwish_until": -1.0, "reck_until": -1.0,
              "rs_charges": 0, "rs_until": -1.0, "racial_until": -1.0, "slam_busy": -1.0,
              "ready": {k: 0.0 for k in ab}, "rs_ready": 0.0, "dwish_ready": 0.0, "racial_ready": 0.0,
              "swing_id": 0}

        def ap():
            a = 2 * ch.str + 3 * lv - 20 + (p["bs_ap"] if sim.t < st["bs_until"] else 0)
            if racial and racial[0] == "power" and sim.t < st["racial_until"]:
                a *= 1 + racial[1] / 100
            return max(0.0, a)

        def mult(direct=True):
            m = p["dmg_mult"]
            if sim.t < st["dwish_until"]:
                m *= 1 + dwish
            if direct and racial and racial[0] == "direct" and sim.t < st["racial_until"]:
                m *= 1 + racial[1] / 100
            return m

        def crit_extra():
            x = 0.0
            if sim.t < st["reck_until"]:
                x += 100
            if racial and racial[0] == "crit" and sim.t < st["racial_until"]:
                x += racial[1]
            return x

        def weapon(norm=False):
            return p["w_avg"] * rng.uniform(0.8, 1.2) + ap() / 14 * (2.4 if norm else speed0)

        def add_rage(x):
            st["rage"] = min(100.0, st["rage"] + x)

        def rage_from(d, crit):
            r = 15 * d / (4 * conv) + 3.5 * speed0 / 2
            r = min(r, 15 * d / conv)
            if crit:
                r *= 1.75
            add_rage(r)

        def on_hit(outcome, white):
            if outcome == "crit":
                if flurry:
                    st["flurry"] = 3
                if dw_pct:
                    deep_wounds()
            if uw and white and rng.chance(uw):
                add_rage(1)
            if rs_bonus and st["rs_charges"] > 0 and sim.t < st["rs_until"]:
                st["rs_charges"] -= 1
                add_rage(rs_bonus)
            if outcome == "dodge" and "op" in ab:
                st["op_until"] = sim.t + 5.0
            if bthrill and white and outcome in ("hit", "crit", "glance") and "op" in ab \
                    and sim.t < st["rend_until"] and rng.chance(bthrill):
                st["op_until"] = sim.t + 5.0

        def deep_wounds():
            total = (p["w_avg"] + ap() / 14 * speed0) * dw_pct * mult(False)
            new = sim.t >= st["dw_until"]
            st["dw_until"] = sim.t + 12.0
            st["dw_tick"] = total / 4
            if new:
                sim.at(sim.t + 3.0, dw_tick)

        def dw_tick():
            if sim.t <= st["dw_until"] + 1e-9:
                sim.deal("Deep Wounds", st["dw_tick"])
                if sim.t + 3.0 <= st["dw_until"] + 1e-9:
                    sim.at(sim.t + 3.0, dw_tick)

        def rend_tick(until):
            if until == st["rend_until"] and sim.t <= until + 1e-9:
                sim.deal("Rend", p["rend_tick"] * mult(False))
                if sim.t + 3.0 <= until + 1e-9:
                    sim.at(sim.t + 3.0, rend_tick, until)

        def yellow(name, dmg, extra_crit=0.0, can_dodge=True):
            o = core.melee_roll(rng, ch, white=False, extra_crit=extra_crit + crit_extra())
            if o == "dodge" and not can_dodge:
                o = "hit"
            if o in ("miss", "dodge"):
                on_hit(o, False)
                return o
            if o == "crit":
                dmg *= p["crit_mult_yellow"]
            sim.deal(name, dmg * mult())
            on_hit(o, False)
            return o

        def swing(sid):
            if sid != st["swing_id"]:
                return
            if sim.t < st["slam_busy"]:
                return
            if st["hs_q"] and st["rage"] >= costs["hs"]:
                st["rage"] -= costs["hs"]
                st["hs_q"] = False
                sim.cast("Heroic Strike")
                yellow("Heroic Strike", weapon() + flat["hs"])
            else:
                st["hs_q"] = False
                o = core.melee_roll(rng, ch, white=True, extra_crit=crit_extra())
                if o not in ("miss", "dodge"):
                    d = weapon() * mult()
                    if o == "crit":
                        d *= melee_mult
                    elif o == "glance":
                        d *= core.A("glance_damage")
                    sim.deal("Melee", d)
                    rage_from(d, o == "crit")
                on_hit(o, True)
            schedule_swing()
            act()

        def schedule_swing():
            h = ch.haste
            if st["flurry"] > 0:
                h *= 1 + flurry
                st["flurry"] -= 1
            if racial and racial[0] == "haste" and sim.t < st["racial_until"]:
                h *= 1 + racial[1] / 100
            st["swing_id"] += 1
            st["next_swing"] = sim.t + speed0 / h
            sim.at(st["next_swing"], swing, st["swing_id"])

        def ready(k):
            return k in ab and sim.t >= st["ready"][k] and st["rage"] >= costs[k]

        def use(k, gcd=True):
            st["rage"] -= costs[k]
            st["ready"][k] = sim.t + cds[k]
            if gcd:
                st["gcd"] = sim.t + 1.5
                sim.at(st["gcd"], act)
            sim.cast(ab[k]["name"])

        def off_gcd():
            t = sim.t
            if racial and t >= st["racial_ready"]:
                st["racial_ready"] = t + racial[3]
                st["racial_until"] = t + racial[2]
                if racial[0] == "power":
                    add_rage(0)
            if "br" in ab and t >= st["ready"]["br"]:
                st["ready"]["br"] = t + cds["br"]
                gain = 10 * (1 + ibr)
                add_rage(gain)
                for i in range(1, 11):
                    sim.at(t + i, add_rage, 1 * (1 + ibr))
                sim.cast("Bloodrage")
            if "bzr" in ab and ibzr and t >= st["ready"]["bzr"]:
                st["ready"]["bzr"] = t + cds["bzr"]
                add_rage(ibzr)
                sim.cast("Berserker Rage")
            if rs_bonus and t >= st["rs_ready"]:
                st["rs_ready"] = t + 15.0
                st["rs_charges"], st["rs_until"] = 4, t + 8.0
                sim.cast("Reckless Swings")
            if dwish and t >= st["dwish_ready"] and st["rage"] >= 10:
                st["rage"] -= 10
                st["dwish_ready"], st["dwish_until"] = t + 180.0, t + 30.0
                sim.cast("Death Wish")
            if "reck" in ab and t >= st["ready"]["reck"]:
                st["ready"]["reck"] = t + cds["reck"]
                st["reck_until"] = t + ab["reck"]["duration_ms"] / 1000
                sim.cast("Recklessness")

        def act():
            t = sim.t
            off_gcd()
            if t < st["gcd"] or t < st["slam_busy"]:
                return
            execute_phase = t >= 0.8 * end
            spec = p["spec"]
            if p["bs_ap"] and t >= st["bs_until"] and st["rage"] >= p["bs_cost"]:
                st["rage"] -= p["bs_cost"]
                st["bs_until"] = t + 120.0
                st["gcd"] = t + 1.5
                sim.at(st["gcd"], act)
                sim.cast("Battle Shout")
                return
            if execute_phase and ready("exe"):
                extra = st["rage"] - costs["exe"]
                use("exe")
                st["rage"] = 0.0
                yellow("Execute", exe_base + extra * exe_per)
                return
            for k in ("bt", "ms"):
                if ready(k):
                    use(k)
                    d = ap() * 0.45 + bt_base if k == "bt" else weapon(True) + flat["ms"]
                    yellow(ab[k]["name"], d)
                    return
            if ready("ww"):
                use("ww")
                yellow("Whirlwind", weapon(True) * (1 + 0.15 * tl.get("Improved Whirlwind", 0)))
                return
            if ready("op") and t < st["op_until"]:
                use("op")
                st["op_until"] = -1
                yellow("Overpower", weapon(True) + flat["op"], extra_crit=iop, can_dodge=False)
                return
            if ready("slam") and spec == "arms" and (islam or "ms" not in ab):
                use("slam", gcd=False)
                cast = slam_cast
                st["gcd"] = t + max(1.0, cast)
                if not islam:
                    st["slam_busy"] = t + cast
                sim.at(t + cast, slam_land)
                return
            if ready("rend") and t >= st["rend_until"] and t < end - 6:
                use("rend")
                o = core.melee_roll(rng, ch, white=False)
                if o not in ("miss", "dodge"):
                    st["rend_until"] = t + p["rend_dur"]
                    sim.at(t + 3.0, rend_tick, st["rend_until"])
                else:
                    on_hit(o, False)
                return
            if ready("tc") and spec == "protection" and t >= st["ready"]["tc"]:
                use("tc")
                cds["tc"] = cds["tc"] or 0.0
                o = core.spell_roll(rng, ch, can_crit=False)
                if o != "miss":
                    d = tc_e["EffectBasePointsF"] * mult()
                    sim.deal("Thunder Clap", d)
                st["ready"]["tc"] = t + 4.0  # Classic 4 s cooldown (CU)
                return
            # Heroic Strike as a rage dump
            if "hs" in ab and not st["hs_q"]:
                big = [costs[k] for k in ("bt", "ms", "ww") if k in ab]
                reserve = max(big) if big else 0
                if execute_phase and "exe" in ab:
                    reserve = max(reserve, costs["exe"] + 15)
                if st["rage"] >= costs["hs"] + reserve:
                    st["hs_q"] = True
            # Nothing castable now: look again when the next cooldown ends
            nxt = [st["ready"][k] for k in ("bt", "ms", "ww", "slam") if k in ab and st["ready"][k] > t]
            if nxt:
                sim.at(min(nxt) + 1e-6, act)

        def slam_land():
            st["slam_busy"] = -1
            yellow("Slam", weapon() + flat["slam"])
            if not islam:
                schedule_swing()
            act()

        if am:
            def am_tick():
                add_rage(am)
                sim.at(sim.t + 3.0, am_tick)
            sim.at(3.0, am_tick)
        sim.at(0.0, swing, 0)
        sim.at(0.0, act)

    return fn


def simulate(spec, race, level, iterations, seed):
    p = setup(spec, race, level)
    out = core.run_many(build(p), iterations=iterations, seed=seed)
    out["inputs"] = p["inp"]
    return out
