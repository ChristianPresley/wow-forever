"""Healer model for WoW Forever: every healing build of Priest, Paladin, Druid and Shaman at level 60.

It answers two questions for each build, race, gear set and scenario:
  - max:      the highest healing per second the build can put out, mana ignored;
  - fight:    the best healing per second that lasts a whole fight (FIGHT seconds, mana
              pool + regeneration, ending empty);
  - endless:  the best healing per second on regeneration alone (truly sustainable).

Method: expected values, not Monte Carlo. Every castable spell rank is an "action" with a
cast time, a net mana cost and an expected amount healed (average roll, healing power,
talents, crit). A small linear program picks how many casts per second of each action
maximise healing, subject to
  - time:     sum(casts * cast time) + rest <= 1;
  - mana:     sum(casts * cost) <= pool / fight + regen while casting + (regen gained by resting);
  - cooldowns and one-HoT-per-target limits; talent links (Swiftmend needs a Rejuvenation).
Effects that depend on the mix itself (Nature's Grace uptime, Infusion of Light, Litany of
Light, Renewed Hope, Riptide's Chain Heal bonus, Water Shield) are solved by damped fixed-point
iteration around the linear program. So the output is prescriptive: it is the cast mix.

Scenarios: "tank" (one target takes all the damage) and "group" (a 5-player party, all hurt).
Assumptions (tag A): no overhealing (every point of healing is needed), no movement, no
pushback, the healer is never interrupted, cooldowns are spread evenly over the fight.

Data: spell ranks, costs, cast times, coefficients and durations come from the Forever
client (tools/forever_data/forever.json, tag F) through tools/levelsim/core.py. Talent values
come from the Forever launch tooltips (.research/talents, tag A: linear per rank), as in
tools/levelsim. Gear is the best craftable healing set (tools/levelsim/gear.py, spec "healer").
Values the client does not ship are listed in CU_VALUES below.

Off-DPS: the same build, race and gear is run through its class module in tools/levelsim
(the damage rotations of that simulator, 180 s fight); the best rotation is reported.
"""
import importlib
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEVELSIM = HERE.parent / "levelsim"
if str(LEVELSIM) not in sys.path:
    sys.path.insert(0, str(LEVELSIM))

import core  # noqa: E402
import gear as gear_mod  # noqa: E402

LEVEL = 60
FIGHT = 300.0
GCD = 1.5
CRIT_MULT = 1.5
SCENARIOS = {"tank": 1, "group": 5}
MODES = ("max", "fight", "endless")
HEAL, AURA, PERIODIC_HEAL, ABSORB = 10, 6, 8, 69

# Values the Forever client does not ship: (value, tag, note).
CU_VALUES = {
    "holy_shock_cost": (325, "CU", "Holy Shock top-rank mana cost (Classic rank 3; the client has rank 1 only)"),
    "lights_vigil_heal": (614, "A", "Light's Vigil party heal at rank 3: the rank 1 tooltip (325-344) scaled by mana cost"),
    "lights_vigil_coef": (0.286, "A", "Light's Vigil healing coefficient (Prayer of Healing's)"),
    "oath_of_light": ({"Holy Light": 400, "Flash of Light": 115, "Holy Shock": 230}, "A", "Oath of Light bonus (tooltip), scaled down for lower ranks"),
    "healing_stream": (14, "CU", "Healing Stream Totem rank 5: healing per 2 s per party member (Classic)"),
    "mana_spring": (10, "CU", "Mana Spring Totem rank 4: mana per 2 s (Classic)"),
    "mana_tide": (600, "A", "Mana Tide Totem: mana per use (rank 1 tooltip 88 x 4 ticks, scaled like Classic ranks)"),
    "water_shield_icd": (3.5, "A", "Water Shield: one globe at most every 3.5 s, 2% of maximum mana each"),
    "innervate": (20, "CU", "Innervate: 20 s of 5x Spirit regeneration that continues while casting, 6 min cooldown (Classic)"),
    "blessing_of_wisdom": (None, "F", "Blessing of Wisdom on the Paladin (client value)"),
    "spirit_regen": (None, "CU", "Spirit regeneration per class (Classic formulas), 5-second rule"),
    "prayer_of_mending_jumps": (6, "A", "Prayer of Mending heals 6 times in a group (first target + 5 jumps), once on a lone tank"),
    "chain_heal_jumps": (1.75, "CU", "Chain Heal in a group: 3 targets at 100% / 50% / 25%"),
    "swiftmend": (None, "CU", "Swiftmend consumes the HoT (Classic); used on the last tick so no healing is lost"),
    "sub_level_20_penalty": (0.0375, "CU", "Spells learned before level 20 lose 3.75% of their coefficient per level below 20 (Classic)"),
    "racial_cooldowns": (None, "A", "Racial cooldowns are used on cooldown; Blood Fury and Eureka! are taken to affect healing"),
}

REGEN = {"priest": (12.5, 4), "paladin": (15, 5), "druid": (15, 5), "shaman": (17, 5)}   # per 2 s: a + Spirit / b (CU)
CAST_REGEN = {"priest": ("Meditation", 3, 0.5), "paladin": ("Reverence", 2, 0.3),
              "druid": ("Reflection", 3, 0.5), "shaman": ("Mindfulness", 3, 0.5)}
INT_TALENT = {"priest": "Mental Strength", "paladin": "Divine Intellect", "druid": "Heart of the Wild", "shaman": "Ancestral Knowledge"}
DPS_ROTATIONS = {"priest": ["holy", "discipline", "shadow"], "paladin": ["holy", "retribution"],
                 "druid": ["restoration", "balance", "feral"], "shaman": ["restoration", "enhancement"]}


# ---------- Linear program ----------

def lp_max(c, A, b):
    """Maximise c.x subject to A x <= b, x >= 0 (all b >= 0). Dense simplex, Bland's rule."""
    m, n = len(A), len(c)
    T = [[float(v) for v in A[i]] + [1.0 if j == i else 0.0 for j in range(m)] + [max(0.0, float(b[i]))] for i in range(m)]
    z = [-float(v) for v in c] + [0.0] * (m + 1)
    basis = list(range(n, n + m))
    for _ in range(20000):
        col = next((j for j in range(n + m) if z[j] < -1e-9), None)
        if col is None:
            break
        row, best = None, None
        for i in range(m):
            if T[i][col] > 1e-9:
                r = T[i][-1] / T[i][col]
                if best is None or r < best - 1e-12 or (abs(r - best) <= 1e-12 and basis[i] < basis[row]):
                    row, best = i, r
        if row is None:
            raise ValueError("unbounded linear program")
        p = T[row][col]
        T[row] = [v / p for v in T[row]]
        for i in range(m):
            f = T[i][col]
            if i != row and abs(f) > 1e-12:
                T[i] = [a - f * q for a, q in zip(T[i], T[row])]
        f = z[col]
        z = [a - f * q for a, q in zip(z, T[row])]
        basis[row] = col
    x = [0.0] * n
    for i, bi in enumerate(basis):
        if bi < n:
            x[bi] = T[i][-1]
    return x, z[-1]


# ---------- Client data helpers ----------

def trained(cls, name, paid=True):
    """Ranks of a class spell usable at level 60, lowest first (rows with a mana cost only)."""
    return [s for s in core.ranks(cls, name) if s["base_level"] <= LEVEL and (bool(s["costs"]) or not paid)]


def eff(s, kind):
    """First effect of a kind: 'direct', 'hot', 'absorb'."""
    for e in s["effects"]:
        if kind == "direct" and e["Effect"] == HEAL:
            return e
        if kind == "hot" and e["EffectAura"] == PERIODIC_HEAL:
            return e
        if kind == "absorb" and e["EffectAura"] == ABSORB:
            return e
    return None


def val(s, e):
    lv = min(LEVEL, s["max_level"]) if s["max_level"] else LEVEL
    return e["EffectBasePointsF"] + (e.get("EffectRealPointsPerLevel") or 0) * max(0, lv - s["spell_level"])


def coef(s, e):
    """Healing coefficient with the Classic penalty for spells learned before level 20 (CU):
    the client stores cast time / 3.5 with no penalty, the server applies it."""
    return e["EffectBonusCoefficient"] * (1 - 0.0375 * max(0, 20 - s["spell_level"]))


def mana_cost(s, base_mana):
    return core.cost(s, base_mana)[1]


def cd_of(s):
    return max(s["cooldown_ms"], s["category_cooldown_ms"]) / 1000


def label(s):
    return f"{s['name']} ({s['rank']})" if s.get("rank") else s["name"]


# ---------- Stats ----------

class Stats:
    """A level 60 healer: class, race, talents and gear resolved to the numbers the kits use."""

    def __init__(self, cls, race, talents, gear_mode):
        core.GEAR["mode"], core.GEAR["spec"] = gear_mode, "healer"
        ch = core.Character(cls, race, LEVEL, talents)
        core.apply_passive_racials(ch, race)
        self.cls, self.race, self.talents, self.ch = cls, race, talents, ch
        ch.int *= 1 + 0.10 * self.t(INT_TALENT[cls]) / 5
        if race == "human":
            ch.spi *= 1.10                                   # The Human Spirit (F)
        if cls == "druid":
            ch.spi *= 1 + 0.15 * self.t("Living Spirit") / 3
        self.int, self.spi = ch.int, ch.spi
        self.base_mana = ch.base_mana
        self.max_mana = ch.mana() * (1.05 if race == "gnome" else 1.0)   # Expansive Mind (F)
        self.crit = ch.spell_crit
        self.haste = ch.haste
        g = ch.gear["stats"] if ch.gear else {}
        self.hp = g.get("healing", 0) + g.get("sp", 0)
        self.mp5 = g.get("mp5", 0)
        a, b = REGEN[cls]
        self.spirit_ps = (a + self.spi / b) / 2
        name, mx, frac = CAST_REGEN[cls]
        self.cast_frac = frac * self.t(name) / mx
        self.heal_mult = self.cost_mult = 1.0

    def t(self, name):
        return self.talents.get(name, 0)

    @property
    def rf(self):          # mana per second while resting (outside the 5-second rule)
        return self.spirit_ps + self.mp5 / 5

    @property
    def rc(self):          # mana per second while casting
        return self.spirit_ps * self.cast_frac + self.mp5 / 5

    def summary(self):
        return {"int": round(self.int), "spi": round(self.spi), "mana": round(self.max_mana), "healing": round(self.hp),
                "crit": round(self.crit, 1), "mp5": self.mp5, "regen_cast": round(self.rc * 5, 1), "regen_rest": round(self.rf * 5, 1)}


def apply_racials(st, U):
    """Racial cooldowns averaged over the fight (A). U(cd) = uses per second."""
    st.crit_x, st.haste_x, st.heal_mult, st.cost_mult, st.hp_x = st.crit, st.haste, 1.0, 1.0, st.hp
    r = st.race
    if r == "nelf":
        st.crit_x += 10 * min(1.0, 15 * U(180))              # Elune's Light
    elif r == "troll":
        st.haste_x *= 1 + 0.10 * min(1.0, 15 * U(180))       # Berserking
    elif r == "orc":
        st.hp_x *= 1 + 0.10 * min(1.0, 15 * U(120))          # Blood Fury
    elif r == "gnome":
        up = min(1.0, 8 * U(120))                            # Eureka!
        st.heal_mult *= 1 + 0.10 * up
        st.cost_mult *= 1 - 0.10 * up


# ---------- Kits ----------

class Action:
    __slots__ = ("name", "spell", "time", "cost", "parts", "heal", "crit", "cap", "group")

    def __init__(self, name, spell, time, cost, parts, crit=0.0, cap=None, group=None):
        self.name, self.spell, self.time, self.cost = name, spell, time, max(0.0, cost)
        self.parts = {k: v for k, v in parts.items() if v > 0}
        self.heal = sum(self.parts.values())
        self.crit, self.cap, self.group = crit, cap, group


class Kit:
    def __init__(self, st, n):
        self.st, self.n = st, n
        self.actions, self.groups, self.links = [], {}, []
        self.income, self.time_tax, self.passive = 0.0, 0.0, {}
        self.tags = {"base_stats": st.ch.stats_tag.split("+")[0], "regen:spirit": "CU", "mana:int": "CU",
                     "no_overhealing": "A", "cooldowns_averaged": "A", "sub_level_20_penalty": "CU"}
        if st.ch.gear:
            self.tags["gear"] = "F"
            self.tags["gear:healer_weights"] = "A"

    def add(self, *a, **k):
        act = Action(*a, **k)
        if act.heal > 0:
            self.actions.append(act)
            self.tags["spell:" + act.spell] = self.tags.get("spell:" + act.spell, "F")
        return act

    def tal(self, name, mx=1):
        r = self.st.t(name)
        if r:
            self.tags["talent:" + name] = "A"
        return r / mx

    def rate(self, x, pred):
        return sum(v for a, v in zip(self.actions, x) if pred(a))

    def feedback(self, x):
        return {}


def _crit(pct):
    return max(0.0, min(1.0, pct / 100))


def priest(st, ctx, n, U, mode):
    k = Kit(st, n)
    T = k.tal
    hp = st.hp_x + st.spi * 0.25 * T("Spiritual Guidance", 5)
    mult = st.heal_mult * (1 + 0.10 * T("Spiritual Healing", 3))
    if T("Power Infusion"):
        mult *= 1 + 0.20 * min(1.0, 15 * U(180))
        k.income -= 0.20 * st.base_mana * U(180)
    crit = st.crit_x + 5 * T("Holy Specialization", 5)
    aegis = 0.15 * T("Divine Aegis", 3)
    ih = 1 - 0.15 * T("Improved Healing", 3)
    ma = 1 - 0.10 * T("Mental Agility", 3)
    td = 1 + 0.05 * T("Twin Disciplines", 5)
    fury = 0.5 * T("Divine Fury", 5)
    lit = 0.10 * T("Litany of Light", 2)
    rh = 10 * T("Renewed Hope", 5) * ctx.get("ws", 0.0)
    party = min(n, 5)

    def direct(s, e, m=1.0, extra=0.0, count=1):
        base = (val(s, e) + coef(s, e) * hp) * mult * m
        c = _crit(crit + extra)
        return base * (1 + c * (CRIT_MULT - 1)) * count, c * min(1200.0, aegis * base * CRIT_MULT) * count, c

    def cost(s, name, m=1.0):
        c = mana_cost(s, st.base_mana)
        return c * m * st.cost_mult - lit * c * ctx.get("lit:" + name, 0.0)

    for name, cut in (("Lesser Heal", 0.0), ("Heal", fury), ("Greater Heal", fury)):
        for s in trained("priest", name):
            h, a, c = direct(s, eff(s, "direct"), extra=rh)
            k.add(label(s), name, max(GCD, (s["cast_ms"] / 1000 - cut) / st.haste_x), cost(s, name, ih), {name: h, "Divine Aegis": a}, c)
    for s in trained("priest", "Flash Heal"):
        h, a, c = direct(s, eff(s, "direct"), extra=rh)
        bind = 0.5 * h * (n - 1) / n if T("Holy Binding") and n > 1 else 0.0   # heals the Priest too, when hurt
        k.add(label(s), "Flash Heal", max(GCD, s["cast_ms"] / 1000 / st.haste_x), cost(s, "Flash Heal"),
              {"Flash Heal": h, "Divine Aegis": a, "Holy Binding": bind}, c)
    for s in trained("priest", "Renew"):
        e = eff(s, "hot")
        ticks = round(s["duration_ms"] / e["EffectAuraPeriod"])
        h = (val(s, e) + coef(s, e) * hp) * ticks * mult * td * (1 + 0.15 * T("Improved Renew", 3))
        k.add(label(s), "Renew", GCD, cost(s, "Renew", ma), {"Renew": h}, group="Renew")
        k.groups["Renew"] = n / (s["duration_ms"] / 1000)
    for s in trained("priest", "Prayer of Healing"):
        h, a, c = direct(s, eff(s, "direct"), count=party)
        k.add(label(s), "Prayer of Healing", max(GCD, s["cast_ms"] / 1000 / st.haste_x), cost(s, "Prayer of Healing"),
              {"Prayer of Healing": h, "Divine Aegis": a}, c)
    sw = T("Soul Warding")
    for s in trained("priest", "Power Word: Shield"):
        e = eff(s, "absorb")
        h = (val(s, e) + coef(s, e) * hp) * (1 + 0.20 * T("Improved Power Word: Shield", 3))
        k.add(label(s), "Power Word: Shield", GCD, cost(s, "Power Word: Shield", ma * (1 - 0.15 * sw)),
              {"Power Word: Shield (absorb)": h}, group="Weakened Soul")
        # one shield per target per 15 s (Weakened Soul), and never faster than its own cooldown
        k.groups["Weakened Soul"] = min(n / 15.0, 1 / max(GCD, cd_of(s) - 4 * sw))
    if T("Penance"):
        cast = trained("priest", "Penance")[-1]
        bolt = next(s for s in trained("priest", "Penance", paid=False)
                    if s["base_level"] == cast["base_level"] and not s["costs"] and eff(s, "direct"))
        h, a, c = direct(bolt, eff(bolt, "direct"), extra=rh, count=3)
        k.add("Penance", "Penance", 2.0, cost(cast, "Penance", ih), {"Penance": h, "Divine Aegis": a}, c, cap=1 / (cd_of(cast)))
        k.tags["penance_bolts"] = "CU"
    if T("Prayer of Mending"):
        s = trained("priest", "Prayer of Mending")[-1]
        jumps = 1 if n == 1 else CU_VALUES["prayer_of_mending_jumps"][0]
        h, a, c = direct(s, s["effects"][0], m=td, count=jumps)
        k.add("Prayer of Mending", "Prayer of Mending", GCD, cost(s, "Prayer of Mending", ih * ma),
              {"Prayer of Mending": h, "Divine Aegis": a}, c, cap=1 / (cd_of(s)))
        k.tags["prayer_of_mending_jumps"] = "A"
    if T("Holy Nova"):
        rows = trained("priest", "Holy Nova", paid=False)
        cast = [s for s in rows if s["costs"]][-1]
        heal = [s for s in rows if not s["costs"] and eff(s, "direct") and s["base_level"] == cast["base_level"]][-1]
        h, a, c = direct(heal, eff(heal, "direct"), m=td, count=party)
        k.add("Holy Nova", "Holy Nova", GCD, cost(cast, "Holy Nova", ma), {"Holy Nova": h, "Divine Aegis": a}, c)
    if T("Inner Focus"):
        k.income += mana_cost(trained("priest", "Greater Heal")[-1], st.base_mana) * ih * U(180)
        k.tags["inner_focus_cd"] = "CU"

    def feedback(x):
        out = {"ws": min(1.0, k.rate(x, lambda a: a.group == "Weakened Soul") * 15 / n)}
        total = sum(x)
        for name in {a.spell for a in k.actions}:
            mine = k.rate(x, lambda a: a.spell == name)
            out["lit:" + name] = 1.0 if mine <= 1e-9 else min(1.0, (total - mine) / mine)
        return out
    k.feedback = feedback
    return k


def paladin(st, ctx, n, U, mode):
    k = Kit(st, n)
    T = k.tal
    hp = st.hp_x
    mult = st.heal_mult * (1 + 0.12 * T("Healing Light", 3))
    crit = st.crit_x + 6 * T("Conviction", 3)
    cm = 1 + (CRIT_MULT - 1) * (1 + 0.5 * T("Holy Power", 5))
    ill = 0.5 * T("Illumination", 5)
    oath = bool(T("Oath of Light"))
    on_oath = (1.0 if n == 1 else 1.0 / n) if oath else 0.0
    bonus = CU_VALUES["oath_of_light"][0]
    infused = 1.0 * T("Infusion of Light", 2) * ctx.get("iol", 0.0)
    party = min(n, 5)

    def direct(base, coef, name, top, extra=0.0, sure=False):
        b = (base + bonus[name] * on_oath * base / top + coef * hp) * mult
        c = 1.0 if sure else _crit(crit + extra)
        return b * (1 + c * (cm - 1)), c

    def cost(c0, c, m=1.0):
        return c0 * m * st.cost_mult - c * ill * c0

    hl = trained("paladin", "Holy Light")
    top = val(hl[-1], eff(hl[-1], "direct"))
    for s in hl:
        e = eff(s, "direct")
        h, c = direct(val(s, e), coef(s, e), "Holy Light", top)
        k.add(label(s), "Holy Light", max(GCD, (s["cast_ms"] / 1000 - infused) / st.haste_x), cost(mana_cost(s, st.base_mana), c), {"Holy Light": h}, c)
    if T("Divine Favor"):
        s, e = hl[-1], eff(hl[-1], "direct")
        h, c = direct(val(s, e), coef(s, e), "Holy Light", top, sure=True)
        c0 = mana_cost(s, st.base_mana)
        k.add("Divine Favor + " + label(s), "Holy Light", max(GCD, (s["cast_ms"] / 1000 - infused) / st.haste_x),
              cost(c0, 1.0) + 0.04 * st.base_mana, {"Holy Light": h}, 1.0, cap=U(120))
    fol = trained("paladin", "Flash of Light")
    top = val(fol[-1], eff(fol[-1], "direct"))
    for s in fol:
        e = eff(s, "direct")
        h, c = direct(val(s, e), coef(s, e), "Flash of Light", top)
        k.add(label(s), "Flash of Light", max(GCD, s["cast_ms"] / 1000 / st.haste_x), cost(mana_cost(s, st.base_mana), c), {"Flash of Light": h}, c)
    if T("Holy Shock"):
        s = [r for r in trained("paladin", "Holy Shock", paid=False) if eff(r, "direct")][-1]
        e = eff(s, "direct")
        extra = 30 * T("Boundless Light", 2) * (1 - on_oath if oath else 1.0)
        h, c = direct(val(s, e), coef(s, e), "Holy Shock", val(s, e), extra=extra)
        c0 = CU_VALUES["holy_shock_cost"][0]
        sc = cost(c0, c, 1 - 0.10 * T("Benediction", 5))
        k.add("Holy Shock", "Holy Shock", GCD, sc, {"Holy Shock": h}, c, cap=1 / 10.0)
        k.tags["holy_shock_cost"] = "CU"
        if T("Light's Vigil"):
            lv = trained("paladin", "Light's Vigil")[-1]
            vb = (CU_VALUES["lights_vigil_heal"][0] + CU_VALUES["lights_vigil_coef"][0] * hp) * mult
            vc = _crit(crit)
            k.add("Light's Vigil + Holy Shock", "Light's Vigil", max(GCD, lv["cast_ms"] / 1000 / st.haste_x) + GCD,
                  mana_cost(lv, st.base_mana) * st.cost_mult + sc,
                  {"Holy Shock": h, "Light's Vigil": vb * (1 + vc * (cm - 1)) * party}, c, cap=1 / (cd_of(lv)))
            k.tags["lights_vigil_heal"] = "A"
    bow = trained("paladin", "Blessing of Wisdom")[-1]["effects"][0]
    k.income += bow["EffectBasePointsF"] / (bow["EffectAuraPeriod"] / 1000)
    k.tags["blessing_of_wisdom_self"] = "F"
    if oath:
        k.income -= 0.08 * st.base_mana / 300
        k.tags["oath_of_light"] = "A"

    def feedback(x):
        procs = k.rate(x, lambda a: a.spell in ("Holy Shock", "Flash of Light", "Light's Vigil")) and \
            sum(v * a.crit for a, v in zip(k.actions, x) if a.spell in ("Holy Shock", "Flash of Light", "Light's Vigil"))
        casts = k.rate(x, lambda a: a.spell == "Holy Light")
        return {"iol": 1.0 if casts <= 1e-9 else min(1.0, procs / casts)}
    k.feedback = feedback
    return k


def druid(st, ctx, n, U, mode):
    k = Kit(st, n)
    T = k.tal
    hp = st.hp_x + st.int * 0.25 * T("Natural Instinct", 2)
    mult = st.heal_mult * (1 + 0.10 * T("Gift of Nature", 5))
    per = mult * (1 + 0.10 * T("Genesis", 5))
    crit = st.crit_x + 4 * T("Nature's Majesty", 2)
    grace = 0.10 * T("Nature's Grace") * ctx.get("ng", 0.0)
    haste, gcd = st.haste_x * (1 + grace), GCD * (1 - grace)
    nat = 0.5 * T("Naturalist", 5)
    splendor = T("Nature's Splendor")
    bloom = st.spi if T("Bloom") else 0.0
    party = min(n, 5)

    def direct(s, e, extra=0.0):
        c = _crit(crit + extra)
        return (val(s, e) + coef(s, e) * hp) * mult * (1 + c * (CRIT_MULT - 1)), c

    def hot(s, e, extra_s=0.0, m=1.0):
        ticks = round((s["duration_ms"] + extra_s * 1000) / e["EffectAuraPeriod"])
        return (val(s, e) + coef(s, e) * hp) * ticks * per * m

    def cost(s, m=1.0):
        return mana_cost(s, st.base_mana) * m * st.cost_mult

    ht = trained("druid", "Healing Touch")
    for s in ht:
        h, c = direct(s, eff(s, "direct"))
        k.add(label(s), "Healing Touch", max(gcd, (s["cast_ms"] / 1000 - nat) / haste), cost(s, 1 - 0.10 * T("Tranquil Spirit", 5)), {"Healing Touch": h}, c)
    if T("Nature's Swiftness"):
        s = ht[-1]
        h, c = direct(s, eff(s, "direct"))
        k.add("Nature's Swiftness + " + label(s), "Healing Touch", gcd, cost(s, 1 - 0.10 * T("Tranquil Spirit", 5)), {"Healing Touch": h}, c, cap=U(180))
    rg_top = rj_top = None
    for s in trained("druid", "Regrowth"):
        h, c = direct(s, eff(s, "direct"), extra=50 * T("Improved Regrowth", 5))
        dur = s["duration_ms"] / 1000 + 6 * splendor
        t = max(gcd, s["cast_ms"] / 1000 / haste)
        rg_top = k.add(label(s), "Regrowth", t, cost(s), {"Regrowth": h, "Regrowth (HoT)": hot(s, eff(s, "hot"), 6 * splendor), "Bloom": bloom}, c, group="Regrowth")
        k.add(label(s) + ", direct heal only", "Regrowth", t, cost(s), {"Regrowth": h}, c)
        k.groups["Regrowth"] = n / dur
    for s in trained("druid", "Rejuvenation"):
        dur = s["duration_ms"] / 1000 + 3 * splendor
        h = hot(s, eff(s, "hot"), 3 * splendor, 1 + 0.15 * T("Improved Rejuvenation", 3))
        rj_top = k.add(label(s), "Rejuvenation", gcd, cost(s), {"Rejuvenation": h, "Bloom": bloom}, group="Rejuvenation")
        k.groups["Rejuvenation"] = n / dur
    if T("Swiftmend") and rj_top:
        sm = k.add("Swiftmend", "Swiftmend", gcd, 0.20 * st.base_mana * st.cost_mult, {"Swiftmend": rj_top.parts["Rejuvenation"]}, cap=1 / 15.0)
        k.links.append({sm.name: 1.0, rj_top.name: -1.0, **({rg_top.name: -1.0} if rg_top else {})})
        if bloom:  # the consumed HoT does not expire, so its Bloom is lost
            sm.parts["Bloom (lost)"] = -bloom
            sm.heal -= bloom
        k.tags["swiftmend_consumes_hot"] = "CU"
    if T("Wild Growth"):
        for s in trained("druid", "Wild Growth"):
            e = eff(s, "hot")
            k.add(label(s), "Wild Growth", max(gcd, (s["cast_ms"] / 1000 - nat) / haste), cost(s), {"Wild Growth": hot(s, e) * party}, group="Wild Growth")
            k.groups["Wild Growth"] = 1 / (cd_of(s))
    tq = trained("druid", "Tranquility")
    if tq:
        s = tq[-1]
        e = next(x for x in s["effects"] if x["EffectAura"] == PERIODIC_HEAL)
        ticks = round(s["duration_ms"] / e["EffectAuraPeriod"])
        cd = cd_of(s) * (1 - 0.6 * T("Improved Tranquility", 2))
        k.add(label(s), "Tranquility", s["duration_ms"] / 1000, cost(s, 1 - 0.10 * T("Tranquil Spirit", 5)),
              {"Tranquility": (val(s, e) + coef(s, e) * hp) * ticks * per * party}, cap=U(cd))
    k.income += U(360) * CU_VALUES["innervate"][0] * st.spirit_ps * (5 - st.cast_frac)
    k.tags["innervate"] = "CU"

    def feedback(x):
        return {"ng": 1 - math.exp(-3 * sum(v * a.crit for a, v in zip(k.actions, x)))}
    k.feedback = feedback
    return k


def shaman(st, ctx, n, U, mode):
    k = Kit(st, n)
    T = k.tal
    hp = st.hp_x + st.int * 0.30 * T("Mental Quickness", 2)
    mult = st.heal_mult * (1 + 0.10 * T("Purification", 5))
    crit = st.crit_x + 5 * T("Thundering Strikes", 5) + 5 * T("Tidal Mastery", 5)
    cm = st.cost_mult * (1 - 0.05 * T("Tidal Focus", 5))
    party = min(n, 5)

    def direct(s, m=1.0):
        e = eff(s, "direct")
        c = _crit(crit)
        return (val(s, e) + coef(s, e) * hp) * mult * m * (1 + c * (CRIT_MULT - 1)), c

    hw = trained("shaman", "Healing Wave")
    way = 1 + 0.25 * T("Healing Way", 3)
    for s in hw:
        h, c = direct(s, way)
        k.add(label(s), "Healing Wave", max(GCD, (s["cast_ms"] / 1000 - 0.5 * T("Improved Healing Wave", 5)) / st.haste_x),
              mana_cost(s, st.base_mana) * cm, {"Healing Wave": h}, c)
    if T("Nature's Swiftness"):
        h, c = direct(hw[-1], way)
        k.add("Nature's Swiftness + " + label(hw[-1]), "Healing Wave", GCD, mana_cost(hw[-1], st.base_mana) * cm, {"Healing Wave": h}, c, cap=U(180))
    for s in trained("shaman", "Lesser Healing Wave"):
        h, c = direct(s)
        k.add(label(s), "Lesser Healing Wave", max(GCD, s["cast_ms"] / 1000 / st.haste_x), mana_cost(s, st.base_mana) * cm, {"Lesser Healing Wave": h}, c)
    rip = T("Riptide")
    jumps = 1.0 if n == 1 else (CU_VALUES["chain_heal_jumps"][0] if n >= 3 else 1.5)
    for s in trained("shaman", "Chain Heal"):
        h, c = direct(s)
        k.add(label(s), "Chain Heal", max(GCD, s["cast_ms"] / 1000 / st.haste_x), mana_cost(s, st.base_mana) * cm,
              {"Chain Heal": h * (jumps + 0.25 * rip * ctx.get("rip", 0.0))}, c)
    if n > 1:
        k.tags["chain_heal_jumps"] = "CU"
    if rip:
        s = trained("shaman", "Riptide")[-1]
        e = eff(s, "hot")
        ticks = round(s["duration_ms"] / e["EffectAuraPeriod"])
        k.add("Riptide", "Riptide", GCD, mana_cost(s, st.base_mana) * cm, {"Riptide": (val(s, e) + coef(s, e) * hp) * ticks * mult},
              cap=1 / (cd_of(s)))
    # One water totem at a time: Healing Stream when mana does not matter, Mana Spring otherwise (A).
    tot = 1 - 0.25 * T("Totemic Focus", 5)
    k.time_tax += GCD * U(300)
    if mode == "max":
        k.passive["Healing Stream Totem"] = CU_VALUES["healing_stream"][0] / 2 * (1 + 0.5 * T("Restorative Totems", 5)) * mult * party
        k.tags["healing_stream_totem"] = "CU"
    else:
        k.income += CU_VALUES["mana_spring"][0] / 2 * (1 + 0.25 * T("Restorative Totems", 5)) - 100 * tot * U(300)
        k.tags["mana_spring_totem"] = "CU"
    if T("Mana Tide Totem"):
        k.income += CU_VALUES["mana_tide"][0] * U(300)
        k.tags["mana_tide_totem"] = "A"
    if T("Water Shield"):
        k.income += min(ctx.get("crits", 0.0), 1 / CU_VALUES["water_shield_icd"][0]) * 0.02 * st.max_mana
        k.tags["water_shield"] = "A"

    def feedback(x):
        return {"rip": min(1.0, k.rate(x, lambda a: a.spell == "Riptide") * 15),
                "crits": sum(v * a.crit for a, v in zip(k.actions, x))}
    k.feedback = feedback
    return k


KITS = {"priest": priest, "paladin": paladin, "druid": druid, "shaman": shaman}


# ---------- Solve ----------

def uses(mode):
    """Uses per second of a cooldown: on cooldown from the pull in a fight, 1/cd when endless."""
    if mode == "endless":
        return lambda cd: 1.0 / max(cd, 1e-9)
    return lambda cd: (math.floor(FIGHT / max(cd, 1e-9)) + 1) / FIGHT


def _solve_once(k, st, mode):
    acts = k.actions
    n = len(acts)
    mana = mode != "max"
    nv = n + (1 if mana else 0)
    A, b = [[a.time for a in acts] + ([1.0] if mana else [])], [1.0 - k.time_tax]
    if mana:
        pool = st.max_mana / FIGHT if mode == "fight" else 0.0
        A.append([a.cost for a in acts] + [-(st.rf - st.rc)])
        b.append(max(0.0, pool + st.rc + k.income))
    for i, a in enumerate(acts):
        if a.cap is not None:
            A.append([1.0 if j == i else 0.0 for j in range(nv)])
            b.append(a.cap)
    for g, cap in k.groups.items():
        A.append([1.0 if j < n and acts[j].group == g else 0.0 for j in range(nv)])
        b.append(cap)
    for link in k.links:
        A.append([link.get(acts[j].name, 0.0) if j < n else 0.0 for j in range(nv)])
        b.append(0.0)
    x, obj = lp_max([a.heal for a in acts] + ([0.0] if mana else []), A, b)
    return x[:n], (x[n] if mana else 0.0), obj


def _top_ranks(k):
    """Keep only the highest rank of every spell (actions are added lowest rank first)."""
    last = {}
    for a in k.actions:
        last[re.sub(r" \(Rank \d+\)", "", a.name)] = a
    k.actions = [a for a in k.actions if last[re.sub(r" \(Rank \d+\)", "", a.name)] is a]


def solve(cls, race, talents, gear_mode, scenario, mode, iterations=40, top_only=False):
    """Best cast mix for one build. Returns hps, the mix, mana flow and the inputs used.
    top_only=True forbids downranking: only the highest rank of each spell may be cast."""
    st = Stats(cls, race, talents, gear_mode)
    U = uses(mode)
    apply_racials(st, U)
    n = SCENARIOS[scenario]
    ctx, best = {}, None
    for it in range(iterations):
        k = KITS[cls](st, ctx, n, U, mode)
        if top_only:
            _top_ranks(k)
        x, rest, obj = _solve_once(k, st, mode)
        new = k.feedback(x)
        # the last iterations are evaluated with the mix's own feedback, so the answer is self-consistent
        gap = max((abs(new[key] - ctx.get(key, 0.0)) for key in new), default=0.0)
        if it >= iterations // 2 and gap < 0.02 and (best is None or obj > best[0]):
            best = (obj, k, x, rest)
        w = 0.5 if it < iterations // 2 else 0.25
        ctx = {key: (1 - w) * ctx.get(key, 0.0) + w * v for key, v in new.items()}
    if best is None:
        best = (obj, k, x, rest)
    obj, k, x, rest = best
    hps = obj + sum(k.passive.values())
    mix, parts = [], dict(k.passive)
    for a, v in zip(k.actions, x):
        if v > 1e-7:
            mix.append({"name": a.name, "cpm": round(v * 60, 2), "hps": round(v * a.heal, 1), "time": round(v * a.time, 3),
                        "cost": round(a.cost, 1), "heal": round(a.heal, 1)})
            for p, h in a.parts.items():
                parts[p] = parts.get(p, 0.0) + v * h
    mix.sort(key=lambda m: -m["hps"])
    spend = sum(v * a.cost for a, v in zip(k.actions, x))
    regen = st.rc * (1 - rest) + st.rf * rest + k.income
    net = spend - regen
    out = {"hps": round(hps, 1), "mix": mix, "breakdown": {p: round(h, 1) for p, h in sorted(parts.items(), key=lambda kv: -kv[1]) if abs(h) >= 0.05},
           "rest": round(rest, 3), "mana_spent_ps": round(spend, 2), "mana_regen_ps": round(regen, 2),
           "oom_seconds": round(st.max_mana / net, 1) if net > 1e-6 else None,
           "hpm": round((hps - sum(k.passive.values())) / spend, 2) if spend > 1e-6 else None,
           "inputs": dict(sorted(k.tags.items())), "stats": st.summary()}
    return out


def evaluate(cls, race, talents, gear_mode):
    """All scenarios and modes for one build."""
    return {sc: {m: solve(cls, race, talents, gear_mode, sc, m) for m in MODES} for sc in SCENARIOS}


def gear_set(cls, gear_mode):
    if gear_mode != "crafted":
        return None
    sel = gear_mod.select(cls, "healer", LEVEL)
    return {"items": sel["items"], "enchants": sel["enchants"],
            "stats": {k: v for k, v in sel["stats"].items() if v and not k.startswith("res_")}}


def off_dps(cls, race, talents, gear_mode, iterations=30, seed=1):
    """Damage of the same build and gear in the level simulator: best damage rotation."""
    import classes  # noqa: F401
    mod = importlib.import_module(f"classes.{cls}")
    core.GEAR["mode"], core.GEAR["spec"] = gear_mode, "healer"
    orig = mod.talents_at
    mod.talents_at = lambda spec, level: dict(talents)
    best = None
    try:
        for rot in DPS_ROTATIONS[cls]:
            try:
                r = mod.simulate(rot, race, LEVEL, iterations, seed)
            except Exception as ex:  # a rotation that needs talents this build lacks
                r = None
                err = f"{type(ex).__name__}: {ex}"
                if best is None:
                    best = {"dps": 0.0, "rotation": rot, "breakdown": {}, "error": err}
            if r and (best is None or r["dps_mean"] > best["dps"]):
                best = {"dps": round(r["dps_mean"], 1), "rotation": mod.SPECS[rot],
                        "breakdown": {a: round(v, 1) for a, v in r["breakdown"].items() if v >= 0.05}}
    finally:
        mod.talents_at = orig
    return best
