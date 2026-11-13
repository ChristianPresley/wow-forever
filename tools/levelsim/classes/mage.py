"""Mage level simulator: Arcane, Fire and Frost, levels 1-60.

Spell values (base points, variance, per-level growth, coefficients, cast and
channel times, costs, cooldowns, categories) come from forever.json through
core. The Forever talent table in the client is incomplete (Missile Barrage,
Heating Up and Fingers of Frost are missing, and rank 1 rows of several talents
hold the max-rank value), so talent values per rank come from the Forever
launch tooltips (.research/talents/mage.json, rank 1 and max rank text), stored
in TALENT_VALUES below and tagged A (linear per rank between tooltip values).

The module also holds `CasterSim`, the event-driven caster engine shared with
classes/priest.py (cast times, GCD, channels, DoT ticks, mana, regen).

Server-side rules not in the client (tag in brackets):
- Spirit regen: 12.5 + Spirit/4 mana per 2 s tick, full outside the 5-second rule,
  talent fraction inside it (Classic) [CU].
- Evocation: level 20, 15% of max mana per 2 s for 8 s, 8 min cooldown. Not in the
  Forever client tables [CU].
- Arcane Blast: +12% of Intellect as spell damage per stack, cost +100% of base cost
  per stack, max 4 stacks, 18 s from the first stack (launch tooltip; aura 400573 is
  not in the client export) [CU].
- Arcane Power 15 s / 3 min, Presence of Mind 3 min (Classic; spells missing in
  client) [CU]. Ice Barrier frost bonus +15% for 1 min and +5% while shielded (the
  training target never breaks the shield) [CU].
- Ignite: rolling pool, 2 ticks over 4 s, refreshed by each new crit (Classic) [CU].
- Clearcasting and Missile Barrage roll once per cast, not per missile [A].
- Fingers of Frost: 15% per chill (Frostbolt, Frostfire Bolt) for 1/2 charges; each
  charge makes one spell treat the target as Frozen [A from tooltip].
- Blast Wave, Arcane Explosion, Frost Nova, Cone of Cold and Flamestrike are not
  used: they are close-range or AoE spells and the fight is one ranged target [A].
- Mana is spent when a cast starts; damage lands when it ends (no travel time) [A].
- Periodic damage does not crit [A]. GCD is 1.5 s and not hasted [CU].
"""
import core

CLASS = "mage"
SPECS = {"arcane": "Arcane", "fire": "Fire", "frost": "Frost"}

# ---------- Talents ----------

# Leveling order (= tree-valid order of each level 60 raid build in
# tools/talents/guides/mage.yml). Points are spent in this order from level 10.
BUILDS = {
    "arcane": [  # Arcane (raid) 38/10/3
        ("Improved Channeling", 5), ("Arcane Concentration", 5), ("Missile Barrage", 2),
        ("Arcane Subtlety", 2), ("Arcane Blast", 1), ("Arcane Impact", 3), ("Arcane Wrath", 1),
        ("Arcane Meditation", 3), ("Presence of Mind", 1), ("Arcane Mind", 5),
        ("Arcane Instability", 3), ("Arcane Power", 1), ("Arcane Geometry", 2),
        ("Improved Counterspell", 2), ("Arcane Shielding", 2), ("Incineration", 5),
        ("Accelerant", 5), ("Precision", 3)],
    "fire": [  # Fire (raid) 12/36/3
        ("Incineration", 5), ("Accelerant", 5), ("Ignite", 5), ("Pyroblast", 1),
        ("Burning Soul", 3), ("Improved Fire Blast", 2), ("Heating Up", 1), ("Improved Scorch", 3),
        ("Master of Elements", 3), ("Critical Mass", 3), ("Blast Wave", 1), ("Fire Power", 3),
        ("Combustion", 1), ("Precision", 3), ("Arcane Resilience", 3), ("Improved Channeling", 2),
        ("Arcane Concentration", 5), ("Missile Barrage", 2)],
    "frost": [  # Frost (raid) 15/5/31
        ("Improved Frostbolt", 5), ("Precision", 3), ("Frost Warding", 2), ("Ice Shards", 5),
        ("Improved Frost Nova", 2), ("Frost Channeling", 3), ("Ice Lance", 1), ("Arctic Reach", 2),
        ("Ice Block", 1), ("Shatter", 3), ("Cold Snap", 1), ("Fingers of Frost", 2),
        ("Ice Barrier", 1), ("Arcane Resilience", 3), ("Improved Channeling", 2),
        ("Arcane Concentration", 5), ("Missile Barrage", 2), ("Arcane Subtlety", 2),
        ("Magic Absorption", 1), ("Incineration", 5)],
}

# Value per rank from the Forever tooltips (rank 1 .. max). Tag A: linear per rank.
TALENT_VALUES = {
    "Arcane Concentration": [2, 4, 6, 8, 10],        # % Clearcasting
    "Missile Barrage": [(20, 10), (40, 20)],          # % from Arcane Blast, % from other bolts
    "Arcane Impact": [2, 4, 6],                       # % Arcane crit
    "Arcane Meditation": [17, 33, 50],                # % regen while casting
    "Arcane Mind": [(2, 20), (4, 40), (6, 60), (8, 80), (10, 100)],  # % Int, % Arcane crit bonus
    "Arcane Instability": [1, 2, 3],                  # % damage and crit
    "Incineration": [2, 4, 6, 8, 10],                 # % crit Fire Blast, Ice Lance, Arcane Blast, Scorch
    "Accelerant": [0.1, 0.2, 0.3, 0.4, 0.5],          # s off Fireball, Frostfire Bolt, Arcane Wrath
    "Ignite": [8, 16, 24, 32, 40],                    # % of crit over 4 s
    "Improved Fire Blast": [1, 2],                    # s off Fire Blast cooldown
    "Improved Scorch": [33.3, 66.7, 100],             # % chance per Scorch
    "Master of Elements": [10, 20, 30],               # % base cost refunded on Fire/Frost crit
    "Critical Mass": [2, 4, 6],                       # % Fire crit
    "Fire Power": [1, 2, 3],                          # % per own Fire effect, max 4 effects
    "Precision": [2, 4, 6],                           # % hit
    "Improved Frostbolt": [0.1, 0.2, 0.3, 0.4, 0.5],  # s off Frostbolt
    "Ice Shards": [20, 40, 60, 80, 100],              # % Frost crit bonus
    "Frost Channeling": [5, 10, 15],                  # % Frost cost
    "Shatter": [17, 33, 50],                          # % crit vs Frozen
    "Fingers of Frost": [1, 2],                       # charges per proc (15% chance)
}


def talents_at(spec, level):
    points = max(0, level - 9)
    out = {}
    for name, n in BUILDS[spec]:
        if points <= 0:
            break
        take = min(n, points)
        out[name] = out.get(name, 0) + take
        points -= take
    return out


def tv(talents, name, inputs):
    """Talent value at the spent rank (0 if not taken)."""
    r = talents.get(name, 0)
    if not r:
        return 0
    inputs[f"talent:{name}"] = "A"
    return TALENT_VALUES[name][r - 1]


# ---------- Spell data ----------

def _effects(spell):
    for e in spell["effects"]:
        yield e, spell
        if e.get("trigger"):
            for e2 in e["trigger"]["effects"]:
                yield e2, e["trigger"]


class Spell:
    """One rank of a spell resolved for a caster level (all values from forever.json)."""

    def __init__(self, s, level, base_mana):
        self.raw = s
        self.name = s["name"]
        lv = min(level, s["max_level"]) if s["max_level"] else level
        self.cast = s["cast_ms"] / 1000
        self.duration = max(0, s["duration_ms"]) / 1000
        self.cd = max(s["cooldown_ms"], s["category_cooldown_ms"]) / 1000
        self.category = s["category"] if s["category_cooldown_ms"] else None
        self.school = s["school_mask"]
        self.cost = core.cost(s, base_mana)[1]
        self.direct = self.dot = self.missile = None
        for e, owner in _effects(s):
            if e["Effect"] == core.SCHOOL_DAMAGE and self.direct is None:
                lo, hi = core.effect_range(e, lv, owner["spell_level"])
                if owner is not s:  # triggered per-tick damage (Arcane Missiles)
                    self.missile = (lo, hi, e["EffectBonusCoefficient"])
                else:
                    self.direct = (lo, hi, e["EffectBonusCoefficient"])
            elif e["Effect"] == core.APPLY_AURA and e["EffectAura"] in (core.PERIODIC_DAMAGE, core.PERIODIC_LEECH) and self.dot is None:
                period = e["EffectAuraPeriod"] / 1000
                self.dot = (core.effect_value(e, lv, owner["spell_level"]), period, e["EffectBonusCoefficient"])
            elif e["Effect"] == core.APPLY_AURA and e["EffectAura"] == 23:  # periodic trigger (missiles)
                self.missile_period = e["EffectAuraPeriod"] / 1000
        self.effects = s["effects"]

    @property
    def avg_direct(self):
        return (self.direct[0] + self.direct[1]) / 2 if self.direct else 0.0

    def dot_total(self, duration=None):
        if not self.dot:
            return 0.0
        d = duration if duration is not None else self.duration
        return self.dot[0] * int(round(d / self.dot[1]))


def spell(cls, name, level, base_mana, inputs, raw=None):
    s = raw or core.best_rank(cls, name, level)
    if not s:
        return None
    inputs[f"spell:{name}"] = "F"
    return Spell(s, level, base_mana)


# ---------- Shared caster engine ----------

REGEN_TICK = 2.0
GCD = 1.5
FIVE_SEC = 5.0


class CasterSim:
    """Event-driven single-target caster fight.

    Subclasses provide choose(), and may override dmg_mult(), crit_chance(),
    crit_bonus(), hit_bonus(), cost_of(), cast_time(), on_damage() and on_cast().
    """

    def __init__(self, sim, ch, inputs):
        self.sim, self.ch, self.inputs = sim, ch, inputs
        self.rng = sim.rng
        self.max_mana = ch.mana()
        self.mana = self.max_mana
        self.last_spend = -99.0
        self.regen_while_casting = 0.0  # fraction 0..1
        self.ready = {}                 # spell name or category -> time ready
        self.buffs = {}                 # name -> expiry
        self.dots = {}                  # key -> dict
        self.sp = 0.0                   # bonus spell damage
        self.racial = None
        inputs["regen:spirit"] = "CU"
        inputs["mana:int"] = "CU"

    # --- helpers
    @property
    def t(self):
        return self.sim.t

    def has(self, buff):
        return self.buffs.get(buff, -1) > self.t

    def cd_ready(self, sp):
        key = sp.category or sp.name
        return self.ready.get(key, 0) <= self.t + 1e-9

    def start_cd(self, sp, cd=None):
        key = sp.category or sp.name
        self.ready[key] = self.t + (sp.cd if cd is None else cd)

    def haste(self):
        h = self.ch.haste
        if self.has("racial_haste"):
            h *= 1 + self.racial[1] / 100
        return h

    def spend(self, amount):
        if amount > 0:
            self.mana -= amount
            self.last_spend = self.t

    # --- regen
    def regen(self):
        per = 12.5 + self.ch.spi / 4
        if self.t - self.last_spend < FIVE_SEC:
            per *= self.regen_while_casting
        self.mana = min(self.max_mana, self.mana + per)
        self.sim.at(self.t + REGEN_TICK, self.regen)

    # --- hooks
    def dmg_mult(self, sp, periodic):
        m = self.ch.dmg_mult
        if self.has("racial_direct") and not periodic:
            m *= 1 + self.racial[1] / 100
        return m

    def crit_chance(self, sp):
        return 0.0

    def crit_bonus(self, sp):
        """Extra crit damage bonus, as a fraction of the base bonus (1.0 = +100%)."""
        return 0.0

    def hit_bonus(self, sp):
        return 0.0

    def spell_power(self, sp):
        p = self.sp
        if self.has("racial_power"):
            p *= 1 + self.racial[1] / 100
        return p

    def on_damage(self, sp, amount, crit, periodic):
        pass

    # --- damage
    def crit_mult(self, sp):
        base = core.A("spell_crit_mult") - 1
        return 1 + base * (1 + self.crit_bonus(sp))

    def roll(self, sp, extra_crit=0.0):
        return core.spell_roll(self.rng, self.ch, extra_crit=self.crit_chance(sp) + extra_crit,
                               extra_hit=self.hit_bonus(sp))

    def hit_direct(self, sp, key=None, lohi=None, extra_crit=0.0, mult=1.0, extra_sp=0.0, outcome=None):
        lo, hi, coef = lohi or sp.direct
        res = outcome or self.roll(sp, extra_crit)
        if res == "miss":
            return res, 0.0
        amount = (self.rng.uniform(lo, hi) + coef * (self.spell_power(sp) + extra_sp)) * mult * self.dmg_mult(sp, False)
        if res == "crit":
            amount *= self.crit_mult(sp)
        self.sim.deal(key or sp.name, amount)
        self.on_damage(sp, amount, res == "crit", False)
        return res, amount

    def apply_dot(self, sp, key=None, duration=None, mult=1.0, on_tick=None):
        """Start or refresh a DoT. Ticks use multipliers at tick time."""
        key = key or sp.name
        dur = sp.duration if duration is None else duration
        base, period, coef = sp.dot
        ticks = int(round(dur / period))
        old = self.dots.get(key)
        gen = (old["gen"] + 1) if old else 1
        d = {"gen": gen, "left": ticks, "end": self.t + dur, "sp": sp, "mult": mult,
             "per_tick": base + coef * self.spell_power(sp), "on_tick": on_tick}
        self.dots[key] = d
        self.sim.at(self.t + period, self._tick, key, gen)

    def dot_up(self, key, margin=0.0):
        d = self.dots.get(key)
        return bool(d) and d["end"] - margin > self.t + 1e-9

    def _tick(self, key, gen):
        d = self.dots.get(key)
        if not d or d["gen"] != gen or d["left"] <= 0:
            return
        d["left"] -= 1
        sp = d["sp"]
        amount = d["per_tick"] * d["mult"] * self.dmg_mult(sp, True)
        self.sim.deal(key, amount)
        self.on_damage(sp, amount, False, True)
        if d["on_tick"]:
            d["on_tick"]()
        if d["left"] > 0:
            self.sim.at(self.t + sp.dot[1], self._tick, key, gen)
        else:
            del self.dots[key]

    # --- loop
    def start(self):
        rc = core.racial_cooldown(self.ch.race)
        if rc:
            self.racial = rc
            self.inputs[f"racial:{self.ch.race}"] = "F"
        self.sim.at(REGEN_TICK, self.regen)
        self.sim.at(0.0, self.act)

    def use_racial(self):
        if self.racial and self.ready.get("racial", 0) <= self.t:
            kind, _, dur, cd = self.racial
            if kind in ("haste", "direct", "power"):
                self.buffs["racial_" + kind] = self.t + dur
                self.ready["racial"] = self.t + cd

    def act(self):
        if self.t >= self.sim.end:
            return
        self.use_racial()
        lock = self.choose()
        self.sim.at(self.t + max(lock, 0.05), self.act)

    def choose(self):
        """Do one action; return seconds until the player is free again."""
        raise NotImplementedError


# ---------- Mage ----------

MAGE_SPELLS = ["Fireball", "Frostbolt", "Fire Blast", "Arcane Missiles", "Scorch", "Frostfire Bolt",
               "Arcane Blast", "Arcane Wrath", "Ice Lance", "Pyroblast", "Ice Barrier"]
TALENT_SPELLS = {"Arcane Blast", "Arcane Wrath", "Ice Lance", "Pyroblast", "Ice Barrier"}
FIRE, FROST, ARCANE = 4, 16, 64

EVOCATION = {"level": 20, "pct_per_tick": 15, "ticks": 4, "period": 2.0, "cd": 480}  # CU
AB_STACK = {"sp_pct_int": 12, "max": 4, "duration": 18}                          # CU
ARCANE_POWER = {"dmg": None, "dur": 15, "cd": 180}                                # CU (dmg/cost from client)
POM_CD = 180                                                                      # CU
ICE_BARRIER_FROST = 20                                                            # CU 15% + 5% while shielded


class MageSim(CasterSim):
    def __init__(self, sim, ch, spec, level, talents, inputs):
        super().__init__(sim, ch, inputs)
        self.spec, self.level, self.tal = spec, level, talents
        T = lambda n: tv(talents, n, inputs)  # noqa: E731
        self.T = T
        self.sp_ = {}
        for n in MAGE_SPELLS:
            if n in TALENT_SPELLS and not talents.get(n):
                continue
            s = spell(CLASS, n, level, ch.base_mana, inputs)
            if s:
                self.sp_[n] = s
        # Arcane Wrath: spell damage = X% of max mana (client effect index 1)
        aw = self.sp_.get("Arcane Wrath")
        self.aw_pct = next((e["EffectBasePointsF"] for e in aw.effects if e["EffectIndex"] == 1), 0) if aw else 0
        ice = self.sp_.get("Ice Lance")
        self.il_frozen = next((e["EffectBasePointsF"] for e in ice.effects if e["EffectIndex"] == 1), 0) if ice else 0
        # talent values
        self.cc_chance = T("Arcane Concentration")
        mb = T("Missile Barrage") or (0, 0)
        self.mb_ab, self.mb_other = mb
        self.regen_while_casting = T("Arcane Meditation") / 100
        self.ai_crit = T("Arcane Instability")
        self.ch.dmg_mult *= 1 + self.ai_crit / 100
        self.ch.spell_crit_bonus += self.ai_crit
        amind = T("Arcane Mind") or (0, 0)
        self.arcane_crit_bonus = amind[1] / 100
        self.ch.int *= 1 + amind[0] / 100
        self.max_mana = self.mana = ch.mana()
        self.hit = T("Precision")
        self.ap = talents.get("Arcane Power", 0) > 0
        self.pom = talents.get("Presence of Mind", 0) > 0
        self.combust = talents.get("Combustion", 0) > 0
        self.heating = talents.get("Heating Up", 0) > 0
        if self.ap:
            ap = core.talent(CLASS, "Arcane Power")["ranks"][0]["effects"]
            self.ap_dmg = ap[0]["EffectBasePointsF"]
            self.ap_cost = ap[1]["EffectBasePointsF"]
            inputs["talent:Arcane Power"] = "F"
            inputs["arcane_power_duration"] = "CU"
        if self.combust:
            c = core.talent(CLASS, "Combustion")["ranks"][0]
            self.comb_step = c["effects"][1]["trigger"]["effects"][0]["EffectBasePointsF"]
            cs = next(s for s in core.data()["classes"][CLASS]["spells"] if s["name"] == "Combustion")
            self.comb_charges = cs["proc"]["charges"]
            self.comb_cd = cs["category_cooldown_ms"] / 1000
            inputs["talent:Combustion"] = "F"
        # state
        self.cc = False
        self.cc_next = False
        self.mb = False
        self.ab_stacks, self.ab_end = 0, 0.0
        self.heat = 0
        self.comb_on, self.comb_crit, self.comb_hits = False, 0, 0
        self.scorch_stacks, self.scorch_end = 0, 0.0
        self.fof = 0
        self.frozen_cast = False
        self.ignite_pool, self.ignite_ticks, self.ignite_gen = 0.0, 0, 0
        self.evoc_ready = 0.0 if level >= EVOCATION["level"] else 1e9
        if level >= EVOCATION["level"]:
            inputs["evocation"] = "CU"
        if "Arcane Blast" in self.sp_:
            inputs["arcane_blast_stack"] = "CU"
        if "Ice Barrier" in self.sp_:
            inputs["ice_barrier_frost_bonus"] = "CU"

    # --- schools
    @staticmethod
    def is_(sp, school):
        return bool(sp.school & school)

    def ab_sp(self):
        if self.ab_stacks and self.ab_end > self.t:
            return self.ch.int * AB_STACK["sp_pct_int"] / 100 * self.ab_stacks
        self.ab_stacks = 0
        return 0.0

    def spell_power(self, sp):
        self.sp = self.ab_sp()
        return super().spell_power(sp)

    def fire_effects(self):
        n = sum(1 for k in ("Fireball", "Pyroblast") if self.dot_up(k))
        n += 1 if self.ignite_ticks > 0 else 0
        n += 1 if self.scorch_stacks and self.scorch_end > self.t else 0
        return min(4, n)

    def dmg_mult(self, sp, periodic):
        m = super().dmg_mult(sp, periodic)
        if self.has("arcane_power"):
            m *= 1 + self.ap_dmg / 100
        if self.is_(sp, FROST) and self.has("ice_barrier"):
            m *= 1 + ICE_BARRIER_FROST / 100
        if self.is_(sp, FIRE):
            if self.scorch_stacks and self.scorch_end > self.t:
                m *= 1 + 0.03 * self.scorch_stacks
            fp = self.T("Fire Power")
            if fp and sp.school == FIRE:
                m *= 1 + fp * self.fire_effects() / 100
        return m

    def crit_chance(self, sp):
        c = 0.0
        if self.is_(sp, ARCANE):
            c += self.T("Arcane Impact")
        if self.is_(sp, FIRE):
            c += self.T("Critical Mass")
            if self.comb_on:
                c += self.comb_step * self.comb_hits
        if sp.name in ("Fire Blast", "Ice Lance", "Arcane Blast", "Scorch"):
            c += self.T("Incineration")
        if self.frozen_cast:
            c += self.T("Shatter")
        return c

    def crit_bonus(self, sp):
        b = 0.0
        if self.is_(sp, ARCANE):
            b += self.arcane_crit_bonus
        if self.is_(sp, FROST):
            b += self.T("Ice Shards") / 100
        return b

    def hit_bonus(self, sp):
        return self.hit

    def cast_time(self, sp):
        c = sp.cast
        if sp.name in ("Fireball", "Frostfire Bolt", "Arcane Wrath"):
            c -= self.T("Accelerant")
        if sp.name == "Frostbolt":
            c -= self.T("Improved Frostbolt")
        if sp.name == "Pyroblast":
            c *= 1 - 0.25 * self.heat
        return max(0.0, c) / self.haste()

    def cost_of(self, sp):
        if self.cc:
            return 0.0
        c = sp.cost
        if sp.name == "Arcane Blast":
            c *= 1 + (self.ab_stacks if self.ab_end > self.t else 0)
        if self.is_(sp, FROST):
            c *= 1 - self.T("Frost Channeling") / 100
        if self.has("arcane_power"):
            c *= 1 + self.ap_cost / 100
        if self.has("racial_direct"):
            c *= 1 - self.racial[1] / 100
        return c

    # --- procs
    def on_damage(self, sp, amount, crit, periodic):
        if periodic or not crit:
            return
        if self.is_(sp, FIRE):
            ig = self.T("Ignite")
            if ig:
                self.add_ignite(amount * ig / 100)
            if self.heating and sp.name in ("Fireball", "Frostfire Bolt", "Fire Blast", "Scorch"):
                self.heat = min(3, self.heat + 1)
            if self.comb_on:
                self.comb_crit += 1
                if self.comb_crit >= self.comb_charges:
                    self.comb_on = False
        if self.is_(sp, FIRE) or self.is_(sp, FROST):
            moe = self.T("Master of Elements")
            if moe:
                self.mana = min(self.max_mana, self.mana + sp.cost * moe / 100)

    def add_ignite(self, amount):
        self.ignite_pool += amount
        self.ignite_ticks = 2
        self.ignite_gen += 1
        self.sim.at(self.t + 2.0, self._ignite_tick, self.ignite_gen)
        self.inputs["ignite_rolling"] = "CU"

    def _ignite_tick(self, gen):
        if gen != self.ignite_gen or self.ignite_ticks <= 0:
            return
        part = self.ignite_pool / self.ignite_ticks
        self.ignite_pool -= part
        self.ignite_ticks -= 1
        self.sim.deal("Ignite", part)  # Ignite is not modified again (Classic)
        if self.ignite_ticks > 0:
            self.sim.at(self.t + 2.0, self._ignite_tick, gen)

    def after_hit(self, sp, res):
        if res == "miss":
            return
        if self.cc_chance and self.rng.chance(self.cc_chance):
            self.cc_next = True
        if self.is_(sp, FIRE) and self.comb_on:
            self.comb_hits += 1
        if sp.name in ("Frostbolt", "Frostfire Bolt") and self.tal.get("Fingers of Frost") and self.rng.chance(15):
            self.fof = self.T("Fingers of Frost")
        if sp.name == "Scorch" and self.tal.get("Improved Scorch") and self.rng.chance(self.T("Improved Scorch")):
            self.scorch_stacks = min(5, (self.scorch_stacks if self.scorch_end > self.t else 0) + 1)
            self.scorch_end = self.t + 30
        if sp.name == "Arcane Blast" and self.mb_ab and self.rng.chance(self.mb_ab):
            self.mb = True
        if sp.name in ("Arcane Wrath", "Fireball", "Frostbolt", "Frostfire Bolt") and self.mb_other and self.rng.chance(self.mb_other):
            self.mb = True

    # --- casting
    def land(self, sp, frozen):
        """Resolve a single-hit spell (direct + optional DoT)."""
        self.frozen_cast = frozen
        mult = 1.0
        extra_sp = 0.0
        if sp.name == "Ice Lance" and frozen:
            mult *= 1 + self.il_frozen / 100
        if sp.name == "Arcane Wrath":
            extra_sp = self.max_mana * self.aw_pct / 100
        res, _ = self.hit_direct(sp, mult=mult, extra_sp=extra_sp)
        self.frozen_cast = False
        if res != "miss" and sp.dot:
            self.apply_dot(sp)
        self.after_hit(sp, res)
        if sp.name == "Arcane Blast":
            if self.ab_stacks == 0 or self.ab_end <= self.t:
                self.ab_stacks, self.ab_end = 0, self.t + AB_STACK["duration"]
            self.ab_stacks = min(AB_STACK["max"], self.ab_stacks + 1)
        if sp.name == "Ice Barrier":
            pass

    def cast(self, sp, instant=False):
        cost = self.cost_of(sp)
        self.spend(cost)
        self.cc_next = False
        self.cc = False
        frozen = False
        if self.fof > 0 and sp.direct:
            frozen = True
            self.fof -= 1
        if sp.name == "Pyroblast":
            ct = self.cast_time(sp)
            self.heat = 0
        else:
            ct = self.cast_time(sp)
        if instant:
            ct = 0.0
        if sp.cd:
            cd = sp.cd
            if sp.name == "Fire Blast":
                cd -= self.T("Improved Fire Blast")
            self.start_cd(sp, cd)
        self.sim.cast(sp.name)
        self.sim.at(self.t + ct, self.land_then_cc, sp, frozen)
        return max(GCD, ct)

    def land_then_cc(self, sp, frozen):
        self.land(sp, frozen)
        if self.cc_next:
            self.cc = True

    def cast_missiles(self, sp):
        barrage = self.mb
        self.mb = False
        cost = 0.0 if barrage else self.cost_of(sp)
        self.spend(cost)
        self.cc = False
        n = int(round(sp.duration / sp.missile_period))
        period = sp.missile_period * (0.5 if barrage else 1.0)
        self.sim.cast(sp.name)
        self.cc_next = False
        for i in range(1, n + 1):
            self.sim.at(self.t + period * i, self._missile, sp, i == n)
        return max(GCD, period * n)

    def _missile(self, sp, last):
        self.hit_direct(sp, lohi=sp.missile)
        if last:
            self.after_hit(sp, "hit")
            if self.cc_next:
                self.cc = True

    def evocate(self):
        e = EVOCATION
        self.evoc_ready = self.t + e["cd"]
        self.sim.cast("Evocation")
        for i in range(1, e["ticks"] + 1):
            self.sim.at(self.t + e["period"] * i, self._evoc_tick)
        return e["period"] * e["ticks"]

    def _evoc_tick(self):
        self.mana = min(self.max_mana, self.mana + self.max_mana * EVOCATION["pct_per_tick"] / 100)

    def value_rate(self, sp):
        """Static damage per second of cast time, used to pick the filler."""
        dmg = sp.avg_direct + sp.dot_total()
        if sp.missile:
            dmg = (sp.missile[0] + sp.missile[1]) / 2 * round(sp.duration / sp.missile_period)
            t = sp.duration
        else:
            t = max(GCD, self.cast_time(sp))
        m = self.dmg_mult(sp, False)
        if self.is_(sp, FROST) and not self.is_(sp, FIRE):
            m *= 1 + self.crit_bonus(sp) * 0.1
        return dmg * m / t

    def affordable(self, sp, cost=None):
        return self.mana >= (self.cost_of(sp) if cost is None else cost)

    def choose(self):
        S = self.sp_
        t = self.t
        # off-GCD cooldowns
        if self.ap and self.ready.get("ap", 0) <= t and self.mana > 0.3 * self.max_mana:
            self.buffs["arcane_power"] = t + ARCANE_POWER["dur"]
            self.ready["ap"] = t + ARCANE_POWER["cd"]
            self.sim.cast("Arcane Power")
        if self.combust and self.ready.get("comb", 0) <= t:
            self.comb_on, self.comb_crit, self.comb_hits = True, 0, 0
            self.ready["comb"] = t + self.comb_cd
            self.sim.cast("Combustion")
        # mana
        if self.mana < 0.12 * self.max_mana and self.evoc_ready <= t:
            return self.evocate()
        ib = S.get("Ice Barrier")
        if ib and not self.has("ice_barrier") and self.cd_ready(ib) and self.affordable(ib):
            self.spend(self.cost_of(ib))
            self.start_cd(ib)
            self.buffs["ice_barrier"] = t + ib.duration
            self.sim.cast("Ice Barrier")
            return GCD
        sc = S.get("Scorch")
        if sc and self.tal.get("Improved Scorch") and (self.scorch_stacks < 5 or self.scorch_end - t < 4 or self.scorch_end <= t) \
                and self.affordable(sc):
            return self.cast(sc)
        am = S.get("Arcane Missiles")
        if am and self.mb:
            return self.cast_missiles(am)
        il = S.get("Ice Lance")
        if il and self.fof > 0 and self.cd_ready(il) and self.affordable(il):
            return self.cast(il)
        py = S.get("Pyroblast")
        if py and self.heat >= 3 and self.affordable(py):
            return self.cast(py)
        aw = S.get("Arcane Wrath")
        if aw and self.cd_ready(aw) and self.affordable(aw):
            return self.cast(aw, instant=self.use_pom())
        fb = S.get("Fire Blast")
        if fb and self.cd_ready(fb) and self.affordable(fb) and not (self.fof and il):
            return self.cast(fb)
        ab = S.get("Arcane Blast")
        if ab:
            cost = self.cost_of(ab)
            reserve = (0.1 if self.evoc_ready <= t + 10 else 0.35) * self.max_mana
            if self.mana - cost >= reserve or (self.cc and self.mana >= 0):
                return self.cast(ab)
        # filler: best damage per cast second among known bolts
        cands = [S[n] for n in ("Fireball", "Frostbolt", "Frostfire Bolt", "Pyroblast") if n in S]
        if self.spec == "fire" and py and self.heating:
            cands = [c for c in cands if c.name != "Pyroblast"]
        if self.spec == "frost":
            cands = [c for c in cands if self.is_(c, FROST)] or cands
        if self.spec == "fire":
            cands = [c for c in cands if self.is_(c, FIRE)] or cands
        best = max(cands, key=self.value_rate)
        if self.affordable(best):
            return self.cast(best, instant=best.cast >= 3.5 and self.use_pom())
        cheap = [c for c in cands + ([sc] if sc else []) if self.affordable(c)]
        if cheap:
            return self.cast(max(cheap, key=self.value_rate))
        return 0.5  # wait for mana

    def use_pom(self):
        if self.pom and self.ready.get("pom", 0) <= self.t:
            self.ready["pom"] = self.t + POM_CD
            self.inputs["presence_of_mind_cd"] = "CU"
            self.sim.cast("Presence of Mind")
            return True
        return False


def make_character(race, level, talents):
    ch = core.Character(CLASS, race, level, talents)
    core.apply_passive_racials(ch, race)
    return ch


def simulate(spec, race, level, iterations, seed):
    talents = talents_at(spec, level)
    inputs = {}

    def build(sim):
        ch = make_character(race, level, talents)
        m = MageSim(sim, ch, spec, level, talents, inputs)
        inputs["base_stats"] = ch.stats_tag
        m.start()

    out = core.run_many(build, iterations, seed)
    out["inputs"] = dict(sorted(inputs.items()))
    for k in ("fight_seconds", "spell_hit_same_level", "spell_crit_mult", "base_spell_crit"):
        out["inputs"][k] = core.ASSUMPTIONS[k][1]
    return out
