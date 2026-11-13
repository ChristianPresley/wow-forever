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
- Mana-aware rotation [A] (`plan_options`, shared with priest, druid, shaman): the
  filler spell AND rank are chosen from every rank known at that level. With M = mana
  + expected cooldown mana (Evocation) and R = remaining fight time, an option with
  damage/s d and mana/s m can be cast a fraction f of the remaining time, where
  f = 1 if m <= M/R + regen while casting, else f = (M/R + rf) / (m - rc + rf)
  (rf, rc = regen outside / inside the 5-second rule); the rest of the time the
  character auto-attacks unarmed and regenerates at the full rate. The caster takes
  the option with the highest f*d + (1-f)*melee dps. When that option has f < 1 and
  is not affordable, it rests (melee, full regen) until mana is 95% full or the
  option becomes sustainable to the end of the fight (cast-until-empty, then rest:
  how a player levels without consumables). The plan also gives the marginal
  damage of a mana point (lam; with slack, the damage/mana slope to the next stronger
  option). Cooldown nukes and DoTs (Fire Blast, Arcane Wrath, Arcane Blast; the Priest's
  DoTs and shocks) are cast when damage - lam * net mana beats resting for the same
  time and, when mana-bound, their damage per mana is at least 90% of the filler's.
  Spell values for planning are expectations (average roll, spell power, hit, crit);
  Clearcasting, Master of Elements and Missile Barrage adjust cost/value.
- Out of mana, or resting, the caster melees unarmed (core.unarmed_weapon,
  core.melee_roll; the target is assumed to be in melee range) [A]. Mage and Priest
  attack power = Strength - 10 [CU, Classic].
- Gear (core.GEAR "crafted", gear.py): Int/Spi/hit/crit come through core.Character.
  Gear spell damage (generic + the spell's school; the best school for multi-school
  spells) adds to every spell's bonus damage, also in the planner's expected values
  (DoT ticks included for the gear part) [C coefficients from the data, no extra
  low-level penalty]. Gear mp5 is regained every tick, also inside the 5-second rule
  [C]. Out of mana / resting the caster shoots an equipped wand (min..max at its
  speed, spell hit roll, ranged (melee) crit chance at the melee crit multiplier,
  not scaled by spell power) [CU]; without a wand it melees with the equipped
  main-hand weapon and gear attack power [A].
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


# ---------- Mana planning (shared by priest, druid, shaman) ----------

def plan_options(opts, mana, extra, remaining, rc, rf, melee_dps):
    """Pick the option with the best sustained damage over the rest of the fight (A).

    opts: (key, damage, seconds, cost, affordable). Returns (key, f, affordable, need):
    f is the fraction of the remaining time the option can be cast (the rest is spent
    auto-attacking unarmed at the full regen rate rf, outside the 5-second rule) and
    need is the mana that casting it for f of the remaining time uses up, and lam is
    the marginal damage of one mana point (0 when mana is not binding).
    """
    R = max(1.0, remaining)
    inflow = max(0.0, mana + extra) / R
    best = None
    for key, dmg, secs, c, ok in opts:
        d, m = dmg / secs, c / secs
        if m <= inflow + rc + 1e-9:
            f = 1.0
        else:
            f = max(0.0, min(1.0, (inflow + rf) / (m - rc + rf)))
        v = f * d + (1 - f) * melee_dps
        if best is None or v > best[0] + 1e-9:
            lam = max(0.0, d - melee_dps) / (m - rc + rf) if f < 1.0 else 0.0
            best = (v, key, f, ok, f * R * max(0.0, m - rc), lam, d, m)
    if best is None:
        return None, 0.0, False, 0.0, 0.0
    if best[2] >= 1.0:
        # Sustainable with slack: a mana point is worth the damage/mana slope to the next
        # stronger (costlier) option, i.e. what spending it elsewhere gives up.
        d0, m0 = best[6], best[7]
        slopes = [(dmg / secs - d0) / (c / secs - m0) for _, dmg, secs, c, _ in opts
                  if c / secs > m0 + 1e-9 and dmg / secs > d0]
        best = best[:5] + (max(slopes, default=0.0),)
    return best[1:6]


# ---------- Shared caster engine ----------

REGEN_TICK = 2.0
GCD = 1.5
FIVE_SEC = 5.0
DPM_FLOOR = 0.9  # A: mana-bound cooldown spells need >= 90% of the filler damage per mana


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
        self.resting = False
        self.next_swing = 0.0
        self.lam = 0.0
        self.wand = ch.gear["ranged"] if ch.gear and (ch.gear.get("ranged") or {}).get("type") == "wand" else None
        self.mp5 = ch.gear_stat("mp5")
        if ch.gear:
            inputs["gear"] = "F (crafted items)"
            if self.mp5:
                inputs["regen:gear_mp5"] = "C"
            inputs["oom_wand" if self.wand else "oom_weapon_melee"] = "CU" if self.wand else "A"
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
        if self.mp5:
            per += self.mp5 * REGEN_TICK / 5
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

    def gear_sp_of(self, sp):
        """Gear bonus spell damage for this spell (generic + its school; best school
        for multi-school spells)."""
        if not self.ch.gear:
            return 0
        schools = [n for m, n in core.SCHOOLS.items() if sp.school & m] or [None]
        return max(self.ch.gear_sp(s) for s in schools)

    def spell_power(self, sp):
        p = self.sp + self.gear_sp_of(sp) if self.ch.gear else self.sp
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

    # --- mana planning (A)
    def regen_casting_ps(self):
        """Mana per second regained while casting (inside the 5-second rule)."""
        r = (12.5 + self.ch.spi / 4) / REGEN_TICK * self.regen_while_casting
        return r + self.mp5 / 5 if self.mp5 else r

    def regen_full_ps(self):
        r = (12.5 + self.ch.spi / 4) / REGEN_TICK
        return r + self.mp5 / 5 if self.mp5 else r

    def extra_mana(self):
        """Expected mana from cooldowns (Evocation) in the remaining fight."""
        return 0.0

    def budget(self):
        """Sustainable mana per second if casting nonstop to the end of the fight."""
        rem = max(1.0, self.sim.end - self.t)
        return (max(0.0, self.mana) + self.extra_mana()) / rem + self.regen_casting_ps()

    def melee_dps(self):
        if self.wand:
            w = self.wand
            hit = min(99.0, core.A("spell_hit_same_level") + self.ch.hit) / 100
            crit = min(100.0, self.ch.melee_crit) / 100
            return w["avg"] / w["speed"] * self.ch.haste * self.ch.dmg_mult * hit * (1 + crit * (core.A("melee_crit_mult") - 1))
        avg, speed = self.ch.weapon("mh")
        return (avg + self.melee_ap() / 14 * speed) / speed * self.ch.haste * self.ch.dmg_mult * 0.85

    def plan(self, opts):
        """Returns (key, f, affordable, need); stores the mana value self.lam."""
        out = plan_options(opts, self.mana, self.extra_mana(), self.sim.end - self.t,
                           self.regen_casting_ps(), self.regen_full_ps(), self.melee_dps())
        self.lam = out[4]
        return out[:4]

    def rest_done(self, f, need):
        """Stop resting at 95% mana, or once mana covers the casting share of the fight."""
        return f >= 1.0 or self.mana >= min(0.95 * self.max_mana, need)

    def efficient(self, sp, ref=None):
        """Cast a cooldown/DoT spell if its damage, net of the value of the mana it uses
        (self.lam from the last plan), beats resting or the filler for the same time."""
        c = self.cost_of(sp)
        if self.mana < c:
            return False
        if c <= 0 or self.lam <= 0:
            return True
        _, dmg, secs, ec, _ = self.option(sp)
        base = self.melee_dps() + self.lam * self.regen_full_ps()
        if dmg - self.lam * (ec - self.regen_casting_ps() * secs) < base * secs:
            return False
        if ref is not None and ec > 0:
            # mana-bound: also require close to the filler's damage per mana (A, 90%)
            _, rd, _, rc_, _ = self.option(ref)
            if rc_ > 0 and dmg / ec < DPM_FLOOR * rd / rc_:
                return False
        return True

    def melee_ap(self):
        return max(0.0, self.ch.str - 10) + self.ch.gear_ap()  # Classic Mage/Priest attack power (CU)

    def wand_idle(self):
        """Shoot the wand while out of mana / resting (CU). Returns seconds to wait."""
        w = self.wand
        nxt = self.next_swing
        if nxt <= self.t + 1e-9:
            if core.spell_roll(self.rng, self.ch, can_crit=False) != "miss":
                d = self.rng.uniform(w["min"], w["max"]) * self.ch.dmg_mult
                if self.rng.chance(self.ch.melee_crit):
                    d *= core.A("melee_crit_mult")
                self.sim.deal("Wand", d)
            self.next_swing = nxt = self.t + w["speed"] / self.haste()
        return min(0.5, max(0.05, nxt - self.t))

    def melee_idle(self):
        """Auto-attack (wand, else melee) while out of mana (A). Returns seconds to wait."""
        if self.wand:
            return self.wand_idle()
        if not self.ch.gear:
            self.inputs["oom_unarmed_melee"] = "A"
        nxt = self.next_swing
        if nxt <= self.t + 1e-9:
            avg, speed = self.ch.weapon("mh")
            o = core.melee_roll(self.rng, self.ch)
            if o not in ("miss", "dodge"):
                d = (avg + self.melee_ap() / 14 * speed) * self.ch.dmg_mult
                if o == "crit":
                    d *= core.A("melee_crit_mult")
                elif o == "glance":
                    d *= core.A("glance_damage")
                self.sim.deal("Melee" if self.ch.gear else "Melee (unarmed)", d)
            self.next_swing = nxt = self.t + speed / self.haste()
        return min(0.5, max(0.05, nxt - self.t))

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
FILLERS = ["Fireball", "Frostbolt", "Frostfire Bolt", "Arcane Missiles", "Scorch", "Pyroblast"]
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
        # every known rank of the filler spells, for mana-aware downranking (A)
        self.ranks_ = {}
        for n in FILLERS:
            if n in self.sp_:
                rs = [Spell(r, level, ch.base_mana) for r in core.ranks(CLASS, n)
                      if r["base_level"] <= level and r["costs"]]
                self.ranks_[n] = rs or [self.sp_[n]]
        inputs["mana_budget_rotation"] = "A"
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

    def exec_time(self, sp):
        return sp.duration if sp.missile else max(GCD, self.cast_time(sp))

    def exp_damage(self, sp):
        """Expected damage of one cast (average roll + spell power, hit and crit folded in)."""
        p = self.spell_power(sp)
        if sp.missile:
            n = round(sp.duration / sp.missile_period)
            dmg = ((sp.missile[0] + sp.missile[1]) / 2 + sp.missile[2] * p) * n
        else:
            dmg = sp.avg_direct + (sp.direct[2] * p if sp.direct else 0.0) + sp.dot_total()
            if sp.dot and self.ch.gear:  # gear spell power on the DoT ticks (A)
                dmg += sp.dot[2] * self.gear_sp_of(sp) * int(round(sp.duration / sp.dot[1]))
        crit = min(100.0, self.ch.spell_crit + self.crit_chance(sp)) / 100
        hit = min(99.0, core.A("spell_hit_same_level") + self.ch.hit + self.hit_bonus(sp)) / 100
        return dmg * self.dmg_mult(sp, False) * hit * (1 + crit * (self.crit_mult(sp) - 1))

    def value_rate(self, sp):
        """Expected damage per second of cast time."""
        return self.exp_damage(sp) / self.exec_time(sp)

    def option(self, sp):
        """Planner option with proc-adjusted value (A): Clearcasting makes the next spell
        free, Master of Elements refunds part of the cost on crits, Missile Barrage gives
        a free Arcane Missiles."""
        c = self.cost_of(sp)
        dmg = self.exp_damage(sp)
        eff = c * (1 - self.cc_chance / 100)
        moe = self.T("Master of Elements")
        if moe and (self.is_(sp, FIRE) or self.is_(sp, FROST)):
            crit = min(100.0, self.ch.spell_crit + self.crit_chance(sp)) / 100
            eff -= sp.cost * moe / 100 * crit
        mb = self.mb_other if sp.name in ("Fireball", "Frostbolt", "Frostfire Bolt") else 0
        am = self.ranks_.get("Arcane Missiles")
        secs = self.exec_time(sp)
        if mb and am:  # the free Missiles also take (half) channel time
            dmg += mb / 100 * self.exp_damage(am[-1])
            secs += mb / 100 * am[-1].duration * 0.5
        return (sp, dmg, secs, max(0.0, eff), self.mana >= c)

    def extra_mana(self):
        rem = self.sim.end - self.t
        wait = max(0.0, self.evoc_ready - self.t)
        if wait > rem - 8:
            return 0.0
        n = 1 + int((rem - 8 - wait) // EVOCATION["cd"])
        return n * self.max_mana * EVOCATION["pct_per_tick"] / 100 * EVOCATION["ticks"]

    def affordable(self, sp, cost=None):
        return self.mana >= (self.cost_of(sp) if cost is None else cost)

    def filler(self):
        """Mana-aware filler (A): spell and rank by sustained damage, see plan_options.
        Returns (spell, f, affordable)."""
        names = [n for n in self.ranks_ if not (n == "Pyroblast" and self.heating)]
        pref = names
        if self.spec == "frost":
            pref = [n for n in names if self.is_(self.sp_[n], FROST)] or names
        elif self.spec == "fire":
            pref = [n for n in names if self.is_(self.sp_[n], FIRE)] or names
        return self.plan([self.option(r) for n in pref for r in self.ranks_[n]])

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
        fill, f, ok, need = self.filler()
        if self.resting:
            if not self.rest_done(f, need):
                return self.melee_idle()
            self.resting = False
        if fill is not None and not ok and f < 1.0:
            if self.evoc_ready <= t:
                return self.evocate()
            self.resting = True
            return self.melee_idle()
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
            return self.cast_missiles(max(self.ranks_.get("Arcane Missiles", [am]), key=self.value_rate))
        il = S.get("Ice Lance")
        if il and self.fof > 0 and self.cd_ready(il) and self.affordable(il):
            return self.cast(il)
        py = S.get("Pyroblast")
        if py and self.heat >= 3 and self.affordable(py):
            return self.cast(py)
        aw = S.get("Arcane Wrath")
        if aw and self.cd_ready(aw) and self.efficient(aw, fill):
            return self.cast(aw, instant=self.use_pom())
        fb = S.get("Fire Blast")
        if fb and self.cd_ready(fb) and not (self.fof and il) and self.efficient(fb, fill):
            return self.cast(fb)
        ab = S.get("Arcane Blast")
        if ab and (self.cc or self.efficient(ab, fill)):
            return self.cast(ab)
        if fill is not None and not ok:  # sustainable but short right now: best affordable
            aff = [self.option(r) for rs in self.ranks_.values() for r in rs]
            fill = max((o for o in aff if o[4]), key=lambda o: o[1] / o[2], default=(None,))[0]
        if fill is not None:
            if fill.missile:
                return self.cast_missiles(fill)
            return self.cast(fill, instant=fill.cast >= 3.5 and self.use_pom())
        return self.melee_idle()

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
