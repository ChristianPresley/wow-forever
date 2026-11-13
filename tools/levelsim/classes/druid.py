"""Druid: Balance, Feral (Cat) and Restoration, levels 1-60.

Talent orders: docs/guides/druid/talents.md leveling builds Balance (caster) and
Feral (Bear, then Cat). Restoration has no published leveling order; this module fills the
Restoration (raid) level-60 build (5/0/46) tree row by row, with Genesis last.

Talent values come from the Forever tooltip text (.research/talents/druid.json, max-rank value
divided by max rank) and are tagged A, because the client's talent rows are stale.

Rotations (only abilities known at that level):
  Balance and Restoration (Restoration is scored on this damage rotation), caster form,
  Moonkin Form from 40 (Balance):
    Moonfire if not ticking > Insect Swarm if not ticking (talent) > filler, where the
    filler is Wrath or Starfire at any known rank, chosen by sustained damage over the
    remaining fight (mage.plan_options, A). Moonfire and Insect Swarm are cast when their
    damage net of the mana's value beats the alternative. When the best filler cannot be
    sustained the Druid casts until empty, then rests (unarmed melee, full regen) until
    95% mana or the casting share of the fight is covered. Clearcasting is spent on
    Starfire.
  Feral: levels 1-9 caster (Wrath, Moonfire); 10-19 Bear Form (auto-attack, Maul when rage
    allows); 20+ Cat Form from behind:
    Tiger's Fury > Shifting Power below 40 Energy > Rip at 5 combo points when it is not
    ticking and 10 s or more remain > Ferocious Bite at 5 combo points > Rake if not ticking >
    best builder (Shred or Claw, by damage per Energy).

Client data used: spell ranks, costs, cast times, coefficients, Rip/Ferocious Bite per-point
values, Tiger's Fury (+15% physical, 30 s), Shifting Power (40 Energy, 8 s), Moonkin aura
(+3% crit), Omen of Clarity (10 s internal cooldown).

Server-side rules and values not in the client (tags):
  - Attack power: caster/bear 2 x Strength - 20, Cat 2 x Strength + Agility - 20; Bear Form
    +30, Cat Form +40 (CU, Classic).
  - Form attacks use the unarmed fist damage rescaled to the form speed: Cat 1.0 s, Bear 2.5 s (A).
  - Rage: 7.5 x damage / rage conversion per melee hit (CU, Classic formula).
  - Energy 10 per second (core), Cat GCD 1.0 s (CU), Energy starts full (A).
  - Rip gets 6% of AP per combo point up to 4 over its duration; Ferocious Bite 3% of AP per
    combo point (CU, Classic 1.12).
  - Omen of Clarity: 10% per damaging spell, 2 procs per minute in melee (CU), 10 s internal
    cooldown (client); Moonkin Form doubles the chance (tooltip); known from level 20 (A).
  - Mana regen: 15 + Spirit/5 per 2 s outside the 5-second rule (CU); Reflection keeps a share.
  - Racials: Shadowmeld-type crit cooldown for Night Elves via core (crit +10% 15 s/3 min).
  - Out of mana or resting (Balance/Restoration): unarmed melee auto-attack in caster form,
    target in range (A); caster attack power 2 x Strength - 20 (CU). Downranked spells use
    their own max level for per-level growth (client max_level, F).
  - Gear (core.GEAR "crafted", gear.py): Str/Agi/Sta/Int/Spi/hit/crit through core.Character.
    Gear spell damage (generic + the spell's school) times the client coefficient
    (EffectBonusCoefficient, C) adds to Wrath, Starfire, Moonfire and Insect Swarm, also in
    the planner's expected values. Gear mp5 is regained every tick, also inside the
    5-second rule (C). Caster-form rest melee uses the equipped main-hand weapon and gear
    attack power (A). Bear/Cat: gear attack power adds to the form attack power and gear
    Str/Agi count through the form formula; form attacks keep the fist-based form weapon,
    as weapon damage does not apply in form (CU, Classic).
"""
import core

try:
    from .mage import plan_options
except ImportError:  # imported as a top-level module by the tests
    from mage import plan_options

CLASS = "druid"
SPECS = {"balance": "Balance", "feral": "Feral (Cat)", "restoration": "Restoration"}

_ORDERS = {
    "balance": [("Improved Wrath", 5), ("Nature's Majesty", 2), ("Improved Moonfire", 2), ("Moonglow", 1),
                ("Nature's Splendor", 1), ("Moonglow", 2), ("Nature's Reach", 2), ("Insect Swarm", 1),
                ("Vengeance", 4), ("Eclipse", 3), ("Vengeance", 1), ("Nature's Grace", 1), ("Moonfury", 5),
                ("Moonkin Form", 1), ("Improved Starfire", 5), ("Heart of the Wild", 5), ("Naturalist", 5),
                ("Genesis", 5)],
    "feral": [("Ferocity", 5), ("Thick Hide", 3), ("Feral Swiftness", 2), ("Sharpened Claws", 2),
              ("Savage Fury", 2), ("Feral Charge", 1), ("Blood Frenzy", 2), ("Predatory Strikes", 3),
              ("Leader of the Pack", 1), ("Predatory Discipline", 1), ("Natural Instinct", 2), ("Feral Instinct", 1),
              ("Rend and Tear", 5), ("Shifting Power", 1), ("Lacerate", 1), ("Primal Bite", 1),
              ("Heart of the Wild", 5), ("Naturalist", 5), ("Furor", 5), ("Shredding Attacks", 3)],
    "restoration": [("Heart of the Wild", 5), ("Naturalist", 5), ("Reflection", 3), ("Gift of Nature", 5),
                    ("Bloom", 1), ("Subtlety", 3), ("Improved Rejuvenation", 3), ("Swiftmend", 1),
                    ("Tranquil Spirit", 5), ("Nature's Swiftness", 1), ("Living Spirit", 3),
                    ("Improved Tranquility", 2), ("Improved Regrowth", 5), ("Wild Growth", 1),
                    ("Nature's Focus", 3), ("Genesis", 5)],
}

# Forever tooltip value per rank, tag A
_TT = {
    "Improved Wrath": 0.1, "Nature's Majesty": 2.0, "Improved Moonfire": 5.0, "Moonglow": 25.0 / 3,
    "Nature's Reach": 2.0, "Vengeance": 20.0, "Eclipse": 0.5 / 3, "Moonfury": 2.0, "Improved Starfire": 0.1,
    "Heart of the Wild": 2.0, "Naturalist": 2.0, "Genesis": 2.0, "Reflection": 50.0 / 3,
    "Ferocity": 1.0, "Sharpened Claws": 3.0, "Savage Fury": 5.0, "Blood Frenzy": 50.0,
    "Predatory Strikes": 50.0, "Leader of the Pack": 3.0, "Natural Instinct": 10.0, "Rend and Tear": 3.0,
    "Shredding Attacks": 6.0, "Natural Shapeshifter": 10.0,
}


def talents_at(spec, level):
    pts = max(0, min(level, 60) - 9)
    out = {}
    for name, n in _ORDERS[spec]:
        take = min(n, pts)
        if take <= 0:
            break
        out[name] = out.get(name, 0) + take
        pts -= take
    return out


def _rank(name, level):
    rs = [s for s in core.ranks(CLASS, name) if s["base_level"] <= level and s["costs"]]
    return rs[-1] if rs else None


def _ranks(name, level):
    """Every trained rank with a mana cost known at `level` (for downranking)."""
    return [s for s in core.ranks(CLASS, name) if s["base_level"] <= level and s["costs"]]


def _lv(spell, level):
    return min(level, spell["max_level"]) if spell.get("max_level") else level


def _rage_conv(level):
    return 0.0091107836 * level ** 2 + 3.225598133 * level + 4.2652911  # Classic (CU)


class Fight:
    def __init__(self, sim, spec, race, level, inputs):
        self.sim, self.spec, self.level, self.inp = sim, spec, level, inputs
        ch = self.ch = core.Character(CLASS, race, level, talents_at(spec, level))
        core.apply_passive_racials(ch, race)
        self.tv = tv = lambda n: ch.tr(n) * _TT.get(n, 0.0)
        ch.int *= 1 + tv("Heart of the Wild") / 100
        ch.hit += tv("Nature's Reach")
        ch.crit_bonus += tv("Nature's Majesty")
        ch.spell_crit_bonus += tv("Nature's Majesty")
        self.dmg_all = 1 + tv("Naturalist") / 100
        self.max_mana = self.mana = ch.mana()
        self.last_spend = -10.0
        self.busy = 0.0
        self.cd = {}
        self.buff = {}
        self.ooc_icd = -1.0
        self.clearcast = False
        self.speed_mult = 1.0
        self.extra_crit = 0.0
        if spec == "feral" and level >= 20:
            self.form = "cat"
        elif spec == "feral" and level >= 10:
            self.form = "bear"
        elif spec == "balance" and ch.tr("Moonkin Form"):
            self.form = "moonkin"
        else:
            self.form = "caster"
        self.ooc = level >= 20
        self.wavg, _ = core.unarmed_weapon(level)
        self.mp5 = ch.gear_stat("mp5")
        if ch.gear:
            inputs["gear"] = "F (crafted items)"
        inputs.update({"talents": "A (Forever tooltip)", "base_stats": ch.stats_tag, "spell_ranks": "F",
                       "mana_regen_spirit": "CU", "omen_of_clarity": "CU", "fight_seconds": "A"})
        if self.form in ("cat", "bear"):
            self.melee_setup()
        else:
            self.caster_setup()

    # ----- shared -----
    @property
    def t(self):
        return self.sim.t

    def spend(self, c):
        if c > 0:
            self.mana -= c
            self.last_spend = self.t

    def regen(self):
        base = 15 + self.ch.spi / 5
        frac = 1.0 if self.t - self.last_spend >= 5 else self.tv("Reflection") / 100
        self.mana = min(self.max_mana, self.mana + base * frac)
        if self.mp5:
            self.mana = min(self.max_mana, self.mana + self.mp5 * 2 / 5)
        self.sim.at(self.t + 2, self.regen)

    def ready(self, k):
        return self.cd.get(k, 0) <= self.t + 1e-9

    def after(self, dt):
        self.busy = self.t + dt
        self.sim.at(self.busy, self.act)

    def wait(self, extra=()):
        t = self.t
        nxt = [v for v in self.cd.values() if v > t] + [t + 0.5] + [x for x in extra if x > t + 1e-6]
        self.sim.at(min(x for x in nxt if x > t + 1e-6), self.act)

    def try_ooc(self, melee=False):
        if not self.ooc or self.t < self.ooc_icd:
            return
        p = 2 * self.speed / 60 * 100 if melee else 10.0
        if self.form == "moonkin":
            p *= 2
        if self.sim.rng.chance(p):
            self.clearcast = True
            self.ooc_icd = self.t + 10

    def racial(self):
        cd = core.racial_cooldown(self.ch.race)
        if not cd or cd[0] != "crit":
            return
        _, val, dur, every = cd
        self.extra_crit += val
        self.sim.at(self.t + dur, self.unracial, val)
        self.sim.at(self.t + every, self.racial)

    def unracial(self, val):
        self.extra_crit -= val

    def start(self):
        self.sim.at(2.0, self.regen)
        self.sim.at(0.0, self.racial)
        if self.form in ("cat", "bear"):
            self.sim.at(0.0, self.swing)
        self.sim.at(0.0, self.act)

    def act(self):
        if self.t < self.busy - 1e-9:
            return
        if self.form == "cat":
            return self.act_cat()
        if self.form == "bear":
            return self.act_bear()
        return self.act_caster()

    # ----- caster / Moonkin -----
    def caster_setup(self):
        ch, lv = self.ch, self.level
        self.wrath, self.sf, self.mf = _rank("Wrath", lv), _rank("Starfire", lv), _rank("Moonfire", lv)
        self.isw = None
        if ch.tr("Insect Swarm"):
            self.isw = _rank("Insect Swarm", lv) or core.talent(CLASS, "Insect Swarm")["ranks"][0]
        self.eclipse = 0
        self.eclipse_exp = -1.0
        self.mf_until = self.is_until = -1.0
        self.ng_until = -1.0
        self.wraths, self.sfs = _ranks("Wrath", lv), _ranks("Starfire", lv)
        self.resting = False
        self.next_swing = 0.0
        self.inp["mana_budget_rotation"] = "A"
        if self.form == "moonkin":
            mk = _rank("Moonkin Form", lv)
            self.spend(core.cost(mk, ch.base_mana)[1])
            aura = [e for e in mk["effects"] if e.get("trigger")][0]["trigger"]["effects"][0]
            ch.spell_crit_bonus += aura["EffectBasePointsF"]
            self.inp["moonkin_aura"] = "F"

    def spell_mult(self, school_periodic=False):
        m = self.dmg_all * (1 + self.tv("Moonfury") / 100)
        if school_periodic:
            m *= 1 + self.tv("Genesis") / 100
        return m

    def crit_mult(self):
        return 1 + (core.A("spell_crit_mult") - 1) * (1 + self.tv("Vengeance") / 100)

    def bonus(self, spell, e):
        """Gear bonus spell damage times the effect's coefficient (C); 0 when naked."""
        if not self.ch.gear:
            return 0
        return (e.get("EffectBonusCoefficient") or 0) * self.ch.gear_sp(core.SCHOOLS.get(spell["school_mask"]))

    def nuke(self, src, spell, mult=1.0, extra_crit=0.0, eff=None):
        e = eff or core.damage_effect(spell)
        lo, hi = core.effect_range(e, _lv(spell, self.level), spell["spell_level"])
        o = core.spell_roll(self.sim.rng, self.ch, extra_crit=extra_crit + self.extra_crit)
        if o == "miss":
            return
        d = (self.sim.rng.uniform(lo, hi) + self.bonus(spell, e)) * mult * self.spell_mult()
        if o == "crit":
            d *= self.crit_mult()
            if self.ch.tr("Nature's Grace"):
                self.ng_until = self.t + 3
        self.sim.deal(src, d)

    def cast_time(self, base):
        h = self.ch.haste * (1.1 if self.ng_until > self.t else 1.0)
        return base / h

    def gcd(self):
        return max(1.0, 1.5 / self.ch.haste / (1.1 if self.ng_until > self.t else 1.0))

    def dot(self, src, spell, dur, until_attr, mult):
        eff = [e for e in spell["effects"] if e["EffectAura"] == core.PERIODIC_DAMAGE][0]
        per = eff["EffectAuraPeriod"] / 1000
        tick = (eff["EffectBasePointsF"] + self.bonus(spell, eff)) * mult * self.spell_mult(True)
        until = self.t + dur
        setattr(self, until_attr, until)
        for i in range(1, int(dur / per + 1e-6) + 1):
            self.sim.at(self.t + i * per, self.tick, src, tick, until)

    def tick(self, src, amount, until):
        if self.t <= until + 1e-6:
            self.sim.deal(src, amount)

    def pay(self, spell, red=0.0, ooc=True):
        c = core.cost(spell, self.ch.base_mana)[1] * max(0.0, 1 - red / 100)
        if ooc and self.clearcast:
            self.clearcast = False
            return True
        if self.mana < c:
            return False
        self.spend(c)
        return True

    # ----- mana planning (A) -----
    def regen_full_ps(self):
        r = (15 + self.ch.spi / 5) / 2
        return r + self.mp5 / 5 if self.mp5 else r

    def regen_casting_ps(self):
        r = (15 + self.ch.spi / 5) / 2 * self.tv("Reflection") / 100
        return r + self.mp5 / 5 if self.mp5 else r

    def caster_ap(self):
        return max(0.0, 2 * self.ch.str - 20) + self.ch.gear_ap()

    def melee_dps(self):
        avg, speed = self.ch.weapon("mh")
        ap = self.caster_ap()
        return (avg + ap / 14 * speed) / speed * self.ch.haste * self.dmg_all * 0.85

    def exp_hit(self, spell, eff=None, mult=1.0, extra_crit=0.0):
        e = eff or core.damage_effect(spell)
        lo, hi = core.effect_range(e, _lv(spell, self.level), spell["spell_level"])
        crit = min(100.0, self.ch.spell_crit + extra_crit + self.extra_crit) / 100
        hit = min(99.0, core.A("spell_hit_same_level") + self.ch.hit) / 100
        return ((lo + hi) / 2 + self.bonus(spell, e)) * mult * self.spell_mult() * hit * (1 + crit * (self.crit_mult() - 1))

    def options(self, ecl):
        moonglow = self.tv("Moonglow")
        out = []
        for w in self.wraths:
            c = core.cost(w, self.ch.base_mana)[1] * max(0.0, 1 - (moonglow + 10 * self.ch.tr("Improved Wrath")) / 100)
            secs = max(self.gcd(), self.cast_time(w["cast_ms"] / 1000 - self.tv("Improved Wrath")))
            out.append((("Wrath", w), self.exp_hit(w), secs, c, self.mana >= c))
        for sf in self.sfs:
            c = core.cost(sf, self.ch.base_mana)[1] * max(0.0, 1 - moonglow / 100)
            secs = max(self.gcd(), self.cast_time(sf["cast_ms"] / 1000 - self.tv("Improved Starfire")
                                                 - (self.tv("Eclipse") if ecl else 0)))
            out.append((("Starfire", sf), self.exp_hit(sf), secs, c, self.mana >= c))
        return out

    def worth(self, dmg, cost, secs):
        """DoT check: damage net of the mana's value beats resting for the same time."""
        if self.mana < cost:
            return False
        if self.lam <= 0 or cost <= 0:
            return True
        base = self.melee_dps() + self.lam * self.regen_full_ps()
        return dmg - self.lam * (cost - self.regen_casting_ps() * secs) >= base * secs

    def melee_idle(self):
        """Unarmed auto-attack while out of mana or resting (A)."""
        self.inp["oom_weapon_melee" if self.ch.gear else "oom_unarmed_melee"] = "A"
        if self.next_swing <= self.t + 1e-9:
            avg, speed = self.ch.weapon("mh")
            o = core.melee_roll(self.sim.rng, self.ch, extra_crit=self.extra_crit)
            if o not in ("miss", "dodge"):
                d = (avg + self.caster_ap() / 14 * speed) * self.dmg_all
                if o == "crit":
                    d *= core.A("melee_crit_mult")
                elif o == "glance":
                    d *= core.A("glance_damage")
                self.sim.deal("Melee" if self.ch.gear else "Melee (unarmed)", d)
            self.next_swing = self.t + speed / self.ch.haste
        self.sim.at(self.t + min(0.5, max(0.05, self.next_swing - self.t)), self.act)

    def act_caster(self):
        t, ch = self.t, self.ch
        moonglow = self.tv("Moonglow")
        ecl = self.eclipse if self.eclipse_exp > t else 0
        opts = self.options(ecl)
        key, f, ok, need, self.lam = plan_options(opts, self.mana, 0.0, self.sim.end - t, self.regen_casting_ps(),
                                                  self.regen_full_ps(), self.melee_dps())
        if self.resting:
            if not (f >= 1.0 or self.mana >= min(0.95 * self.max_mana, need)):
                return self.melee_idle()
            self.resting = False
        gcd = self.gcd()
        if self.mf and self.mf_until <= t:
            imp = self.tv("Improved Moonfire")
            direct = [e for e in self.mf["effects"] if e["Effect"] == core.SCHOOL_DAMAGE][0]
            dot_e = [e for e in self.mf["effects"] if e["EffectAura"] == core.PERIODIC_DAMAGE][0]
            dur = self.mf["duration_ms"] / 1000 + (3 if ch.tr("Nature's Splendor") else 0)
            ticks = int(dur / (dot_e["EffectAuraPeriod"] / 1000) + 1e-6)
            dmg = self.exp_hit(self.mf, direct, 1 + imp / 100, imp) + \
                (dot_e["EffectBasePointsF"] + self.bonus(self.mf, dot_e)) * (1 + imp / 100) * self.spell_mult(True) * ticks
            c = core.cost(self.mf, ch.base_mana)[1] * max(0.0, 1 - moonglow / 100)
            if (self.clearcast or self.worth(dmg, c, gcd)) and self.pay(self.mf, moonglow):
                self.sim.cast("Moonfire")
                self.nuke("Moonfire", self.mf, 1 + imp / 100, imp, direct)
                self.dot("Moonfire (DoT)", self.mf, dur, "mf_until", 1 + imp / 100)
                self.try_ooc()
                return self.after(gcd)
        if self.isw and self.is_until <= t:
            dur = self.isw["duration_ms"] / 1000 + (2 if ch.tr("Nature's Splendor") else 0)
            dot_e = [e for e in self.isw["effects"] if e["EffectAura"] == core.PERIODIC_DAMAGE][0]
            dmg = (dot_e["EffectBasePointsF"] + self.bonus(self.isw, dot_e)) * self.spell_mult(True) * int(dur / (dot_e["EffectAuraPeriod"] / 1000) + 1e-6)
            c = core.cost(self.isw, ch.base_mana)[1] * max(0.0, 1 - moonglow / 100)
            if (self.clearcast or self.worth(dmg, c, gcd)) and self.pay(self.isw, moonglow):
                self.sim.cast("Insect Swarm")
                self.dot("Insect Swarm", self.isw, dur, "is_until", 1.0)
                self.try_ooc()
                return self.after(gcd)
        if self.clearcast and self.sf:
            key, ok = ("Starfire", self.sf), True
        elif key is not None and not ok:
            if f < 1.0:
                self.resting = True
                return self.melee_idle()
            aff = [o for o in opts if o[4]]
            key = max(aff, key=lambda o: o[1] / o[2])[0] if aff else None
        if key is None:
            return self.melee_idle()
        name, spell = key
        if name == "Starfire":
            if self.pay(spell, moonglow):
                base = spell["cast_ms"] / 1000 - self.tv("Improved Starfire")
                if ecl:
                    base -= self.tv("Eclipse")
                    self.eclipse -= 1
                cast = self.cast_time(base)
                self.sim.cast("Starfire")
                self.sim.at(t + cast, self.nuke, "Starfire", spell)
                self.try_ooc()
                return self.after(max(gcd, cast))
        else:
            if self.pay(spell, moonglow + 10 * ch.tr("Improved Wrath"), ooc=False):
                cast = self.cast_time(spell["cast_ms"] / 1000 - self.tv("Improved Wrath"))
                self.sim.cast("Wrath")
                self.sim.at(t + cast, self.nuke, "Wrath", spell)
                if ch.tr("Eclipse"):
                    self.eclipse = min(4, ecl + 2)
                    self.eclipse_exp = t + 15
                self.try_ooc()
                return self.after(max(gcd, cast))
        return self.melee_idle()

    # ----- Bear / Cat -----
    def melee_setup(self):
        ch, lv = self.ch, self.level
        cat = self.form == "cat"
        if cat:
            ch.str *= 1 + self.tv("Heart of the Wild") / 100
        ch.crit_bonus += self.tv("Sharpened Claws") + self.tv("Leader of the Pack")
        self.ap = 2 * ch.str - 20 + (ch.agi + 40 if cat else 30) + lv * self.tv("Predatory Strikes") / 100
        if ch.gear:
            self.ap += ch.gear_ap()
            self.inp["form_gear_ap"] = "CU"
        self.speed = 1.0 if cat else 2.5
        self.wdmg = self.wavg / 2.0 * self.speed  # fist damage rescaled to form speed (A)
        form = _rank("Cat Form" if cat else "Bear Form", lv)
        self.spend(core.cost(form, ch.base_mana)[1] * (1 - self.tv("Natural Shapeshifter") / 100))
        self.energy, self.e_t = 100.0, 0.0
        self.rage = 0.0
        self.cp = 0
        self.maul_q = False
        self.rip_until = self.rake_until = -1.0
        self.tf_until = -1.0
        r = lambda n: _rank(n, lv)
        self.claw, self.shred, self.rake = r("Claw"), r("Shred"), r("Rake")
        self.rip, self.fb, self.tf, self.maul = r("Rip"), r("Ferocious Bite"), None, r("Maul")
        tf = [s for s in core.ranks(CLASS, "Tiger's Fury") if s["base_level"] <= lv and s["cooldown_ms"]]
        self.tf = tf[-1] if tf else None
        self.sp_spell = core.ranks(CLASS, "Shifting Power")[0] if ch.tr("Shifting Power") else None
        self.inp.update({"form_attack_power": "CU", "form_weapon": "A", "rage_formula": "CU",
                         "energy_regen": core.ASSUMPTIONS["energy_per_sec"][1], "rip_bite_ap": "CU"})

    def en(self):
        return min(100.0, self.energy + core.A("energy_per_sec") * (self.t - self.e_t))

    def set_en(self, v):
        self.energy, self.e_t = min(100.0, v), self.t

    def phys_mult(self, ability=True):
        m = self.dmg_all
        if self.tf_until > self.t:
            m *= 1 + self.tf["effects"][0]["EffectBasePointsF"] / 100
        if ability and (self.rip_until > self.t or self.rake_until > self.t):
            m *= 1 + self.tv("Rend and Tear") / 100
        return m

    def hit_dmg(self, pct=1.0, flat=0.0):
        return (self.wdmg + self.ap / 14 * self.speed) * pct + flat

    def swing(self):
        o = core.melee_roll(self.sim.rng, self.ch, white=not self.maul_q, extra_crit=self.extra_crit)
        if self.maul_q:
            self.maul_q = False
            base = self.hit_dmg(1.0, self.maul["effects"][0]["EffectBasePointsF"]) * (1 + self.tv("Savage Fury") / 100)
            src = "Maul"
            self.sim.cast("Maul")
        else:
            base, src = self.hit_dmg(), "Melee"
        if o not in ("miss", "dodge"):
            d = base * self.phys_mult(src != "Melee")
            if o == "crit":
                d *= core.A("melee_crit_mult")
                if self.form == "bear" and self.ch.tr("Blood Frenzy"):
                    if self.sim.rng.chance(self.tv("Blood Frenzy")):
                        self.rage += 5
            elif o == "glance":
                d *= core.A("glance_damage")
            self.sim.deal(src, d)
            if self.form == "bear" and src == "Melee":
                self.rage = min(100.0, self.rage + 7.5 * d / _rage_conv(self.level))
            self.try_ooc(melee=True)
        self.sim.at(self.t + self.speed / self.ch.haste, self.swing)
        if self.form == "bear":
            self.act()

    def act_bear(self):
        if self.maul and not self.maul_q:
            c = self.maul["costs"][0]["ManaCost"] / 10
            if self.clearcast:
                self.clearcast = False
                self.maul_q = True
            elif self.rage >= c:
                self.rage -= c
                self.maul_q = True

    def ability(self, src, spell, pct_eff=True, cp_gain=True):
        """Weapon ability: pct% weapon damage plus flat (client effects)."""
        o = core.melee_roll(self.sim.rng, self.ch, white=False, extra_crit=self.extra_crit)
        self.sim.cast(src)
        if o in ("miss", "dodge"):
            return False
        effs = spell["effects"]
        flat = sum(e["EffectBasePointsF"] for e in effs if e["Effect"] == core.WEAPON_DAMAGE)
        pct = sum(e["EffectBasePointsF"] for e in effs if e["Effect"] == core.WEAPON_PERCENT_DAMAGE) / 100 or 1.0
        d = self.hit_dmg(pct, flat * pct) * self.phys_mult() * (1 + self.tv("Savage Fury") / 100)
        if o == "crit":
            d *= 1 + (core.A("melee_crit_mult") - 1) * (1 + self.tv("Natural Instinct") / 100)
        self.sim.deal(src, d)
        if cp_gain:
            self.cp = min(5, self.cp + 1 + (1 if o == "crit" and self.sim.rng.chance(self.tv("Blood Frenzy")) else 0))
        return True

    def energy_cost(self, spell, red=0.0):
        c = [x for x in spell["costs"] if x["PowerType"] == 3][0]["ManaCost"]
        return max(0.0, c - red)

    def spend_energy(self, c):
        if self.clearcast:
            self.clearcast = False
            return
        self.set_en(self.en() - c)

    def act_cat(self):
        t, ch, gcd = self.t, self.ch, 1.0
        e = self.en()
        remain = self.sim.end - t
        if self.tf and self.ready("tf"):
            self.cd["tf"] = t + self.tf["cooldown_ms"] / 1000
            self.tf_until = t + self.tf["duration_ms"] / 1000
            self.sim.cast("Tiger's Fury")
        if self.sp_spell and self.ready("sp") and e < 40:
            c = core.cost(self.sp_spell, ch.base_mana)[1] * (1 - self.tv("Natural Shapeshifter") / 100)
            if self.mana >= c:
                self.spend(c)
                self.cd["sp"] = t + self.sp_spell["cooldown_ms"] / 1000
                self.set_en(e + self.sp_spell["effects"][0]["EffectBasePointsF"])
                self.sim.cast("Shifting Power")
                return self.after(gcd)
        if self.cp >= 5:
            if self.rip and self.rip_until <= t and remain >= 10:
                c = self.energy_cost(self.rip)
                if self.clearcast or e >= c:
                    self.spend_energy(c)
                    return self.do_rip(gcd)
                return self.wait([t + (c - e) / core.A("energy_per_sec")])
            if self.fb:
                c = self.energy_cost(self.fb)
                if self.clearcast or e >= c:
                    return self.do_bite(e, c, gcd)
                return self.wait([t + (c - e) / core.A("energy_per_sec")])
        if self.rake and self.rake_until <= t and remain >= 6:
            c = self.energy_cost(self.rake, self.tv("Ferocity"))
            if self.clearcast or e >= c:
                self.spend_energy(c)
                self.sim.cast("Rake")
                if core.melee_roll(self.sim.rng, ch, white=False) not in ("miss", "dodge"):
                    eff = {x["Effect"]: x for x in self.rake["effects"]}
                    m = self.phys_mult() * (1 + self.tv("Savage Fury") / 100)
                    self.sim.deal("Rake", eff[core.SCHOOL_DAMAGE]["EffectBasePointsF"] * m)
                    dot = [x for x in self.rake["effects"] if x["EffectAura"] == core.PERIODIC_DAMAGE][0]
                    self.rake_until = t + self.rake["duration_ms"] / 1000
                    for i in range(1, int(self.rake["duration_ms"] / dot["EffectAuraPeriod"]) + 1):
                        self.sim.at(t + i * dot["EffectAuraPeriod"] / 1000, self.bleed, "Rake (DoT)",
                                    dot["EffectBasePointsF"] * m, self.rake_until)
                    self.cp = min(5, self.cp + 1)
                return self.after(gcd)
        # builder by damage per Energy
        best = None
        for spell, name, red in ((self.shred, "Shred", self.tv("Shredding Attacks")), (self.claw, "Claw", self.tv("Ferocity"))):
            if not spell:
                continue
            effs = spell["effects"]
            pct = sum(x["EffectBasePointsF"] for x in effs if x["Effect"] == core.WEAPON_PERCENT_DAMAGE) / 100
            flat = sum(x["EffectBasePointsF"] for x in effs if x["Effect"] == core.WEAPON_DAMAGE)
            c = self.energy_cost(spell, red)
            val = self.hit_dmg(pct, flat * pct) / max(c, 1)
            if best is None or val > best[0]:
                best = (val, spell, name, c)
        if best:
            _, spell, name, c = best
            if self.clearcast or e >= c:
                self.spend_energy(c)
                self.ability(name, spell)
                return self.after(gcd)
            return self.wait([t + (c - e) / core.A("energy_per_sec")])
        self.wait()

    def bleed(self, src, amount, until):
        if self.t <= until + 1e-6:
            self.sim.deal(src, amount)

    def do_rip(self, gcd):
        t = self.t
        self.sim.cast("Rip")
        if core.melee_roll(self.sim.rng, self.ch, white=False) in ("miss", "dodge"):
            return self.after(gcd)
        eff = self.rip["effects"][0]
        per = eff["EffectAuraPeriod"] / 1000
        n = int(self.rip["duration_ms"] / 1000 / per)
        tick = eff["EffectBasePointsF"] + eff["EffectPointsPerResource"] * self.cp
        tick += self.ap * 0.06 * min(self.cp, 4) / n
        self.rip_until = t + n * per
        m = self.phys_mult()
        for i in range(1, n + 1):
            self.sim.at(t + i * per, self.bleed, "Rip", tick * m, self.rip_until)
        self.cp = 0
        return self.after(gcd)

    def do_bite(self, e, c, gcd):
        self.sim.cast("Ferocious Bite")
        free = self.clearcast
        extra = max(0.0, e - (0 if free else c))
        o = core.melee_roll(self.sim.rng, self.ch, white=False, extra_crit=self.extra_crit)
        if free:
            self.clearcast = False
        if self.ch.tr("Predatory Discipline") or o in ("miss", "dodge"):
            self.set_en(e - (0 if free else c))
        else:
            self.set_en(0)
        if o not in ("miss", "dodge"):
            dmg_e, conv_e = self.fb["effects"][0], self.fb["effects"][1]
            lo, hi = core.effect_range(dmg_e, self.level, self.fb["spell_level"])
            d = self.sim.rng.uniform(lo, hi) + dmg_e["EffectPointsPerResource"] * self.cp
            d += self.ap * 0.03 * self.cp + extra * conv_e["EffectBasePointsF"] / 100
            d *= self.phys_mult()
            if o == "crit":
                d *= 1 + (core.A("melee_crit_mult") - 1) * (1 + self.tv("Natural Instinct") / 100)
            self.sim.deal("Ferocious Bite", d)
            self.cp = 0
        return self.after(gcd)


def simulate(spec, race, level, iterations, seed):
    inputs = {}

    def build(sim):
        Fight(sim, spec, race, level, inputs).start()

    r = core.run_many(build, iterations, seed)
    r["inputs"] = inputs
    return r
