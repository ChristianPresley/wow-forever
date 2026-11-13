"""Shaman: Elemental, Enhancement and Restoration, levels 1-60.

Talent orders: docs/guides/shaman/talents.md leveling builds Elemental (ranged) and
Enhancement (fast and safe). Restoration has no published leveling order; this module fills the
Restoration (healer) level-60 build (0/10/41) tree row by row, then Enhancement.

Talent values come from the Forever tooltip text (.research/talents/shaman.json, max-rank value
divided by max rank) and are tagged A, because the client's talent rows are stale.

Rotations (only abilities known at that level):
  Elemental and Restoration (Restoration is scored on this damage rotation), at range, no melee:
    Searing Totem kept up > Lightning Mastery (40) > Flame Shock if not ticking >
    Chain Lightning on cooldown > Lightning Bolt.
  Enhancement, in melee:
    Searing Totem kept up > Rage of the Farseer > Stormstrike > Lightning Bolt at 5 Maelstrom
    Weapon stacks > Flame Shock if not ticking > Earth Shock while mana is above 50%.
  Before Earth Shock (level 4) every spec casts Lightning Bolt; Enhancement only when no melee
  ability is ready and mana is above 60%.
  Buffs before the pull: Windfury Weapon on the main hand from 30 (Enhancement); Strength of
  Earth Totem; Windfury Totem (32, non-Enhancement) or Grace of Air Totem (42, Enhancement).

Client data used: spell ranks, costs, cast times, coefficients, Lightning Overload copies (the
no-cost duplicate ranks), Stormstrike (150% weapon, 6 s, +20% next Lightning Bolt/Chain
Lightning/Earth Shock), Rage of the Farseer (+30% attack speed, 25 s, 3 min), Searing Totem
duration. `core.best_rank` returns the Overload copy for Lightning Bolt/Chain Lightning, so this
module picks ranks that have a mana cost.

Server-side rules and values not in the client (tags):
  - Attack power = 2 x Strength + 2 x level - 20 (CU, Classic Shaman).
  - Searing Totem: Classic damage 9-11/13-17/19-25/26-34/33-45/40-54 every 2.5 s (CU); it can
    crit with the shaman's spell crit (A).
  - Windfury Weapon: 20% per landed hit (client tooltip), 2 extra attacks (A: Forever "adds an
    additional weapon swing"), extra AP 46/119/249/333 (CU, Classic ranks). Windfury Totem:
    20%, 2 extra attacks (A), AP 122/229/315 (CU). Extra attacks cannot proc Windfury (CU).
    Imbues work on the unarmed fist (A, no gear requested).
  - Strength of Earth 10/20/36/61/77 Strength, Grace of Air 43/67/77 Agility (CU, Classic).
  - Chain Lightning and shock cooldowns 6 s (CU); single target, so Chain Lightning hits once.
  - Maelstrom Weapon chance: 10 procs per minute (A; Forever only says the chance was doubled).
  - Water Shield: a spell crit returns 2% of max mana at most every 3.5 s (client values, A rule).
  - Mana regen: 17 + Spirit/5 per 2 s outside the 5-second rule (CU); Mindfulness and
    Improved Stormstrike keep a share while casting.
  - Racials: Blood Fury +10% AP and spell power, Berserking +10% attack and cast speed (core).
"""
import core

CLASS = "shaman"
SPECS = {"elemental": "Elemental", "enhancement": "Enhancement", "restoration": "Restoration"}

_ORDERS = {
    "elemental": [("Concussion", 5), ("Elemental Alacrity", 3), ("Convection", 2), ("Elemental Focus", 1),
                  ("Convection", 3), ("Call of Flame", 1), ("Earthbound", 1), ("Eye of the Storm", 3),
                  ("Call of Flame", 1), ("Call of Thunder", 1), ("Lightning Overload", 3), ("Call of Flame", 1),
                  ("Elemental Fury", 5), ("Lightning Mastery", 1), ("Tidal Focus", 5), ("Mindfulness", 3),
                  ("Totemic Focus", 2), ("Water Shield", 1), ("Thundering Strikes", 5), ("Ancestral Knowledge", 4)],
    "enhancement": [("Thundering Strikes", 5), ("Mental Dexterity", 3), ("Ancestral Knowledge", 2),
                    ("Shamanistic Focus", 1), ("Elemental Weapons", 3), ("Ancestral Knowledge", 1), ("Stormstrike", 1),
                    ("Flurry", 5), ("Spirit Weapons", 1), ("Improved Stormstrike", 2), ("Mental Quickness", 2),
                    ("Maelstrom Weapon", 5), ("Rage of the Farseer", 1), ("Improved Ghost Wolf", 2),
                    ("Ancestral Knowledge", 2), ("Tidal Focus", 5), ("Mindfulness", 3), ("Totemic Focus", 2),
                    ("Water Shield", 1), ("Concussion", 4)],
    "restoration": [("Improved Healing Wave", 5), ("Tidal Focus", 5), ("Mindfulness", 3), ("Healing Focus", 3),
                    ("Water Shield", 1), ("Ancestral Healing", 3), ("Tidal Mastery", 5), ("Restorative Totems", 5),
                    ("Mana Tide Totem", 1), ("Healing Way", 3), ("Nature's Swiftness", 1), ("Purification", 5),
                    ("Riptide", 1), ("Thundering Strikes", 5), ("Ancestral Knowledge", 5)],
}

# Forever tooltip value per rank, tag A
_TT = {
    "Concussion": 1.0, "Convection": 2.0, "Elemental Alacrity": 0.5 / 3, "Call of Flame": 5.0,
    "Call of Thunder": 5.0, "Lightning Overload": 10.0, "Elemental Fury": 20.0, "Tidal Focus": 1.0,
    "Mindfulness": 50.0 / 3, "Totemic Focus": 5.0, "Thundering Strikes": 1.0, "Ancestral Knowledge": 2.0,
    "Mental Dexterity": 50.0, "Shamanistic Focus": 45.0, "Elemental Weapons": 40.0 / 3, "Flurry": 6.0,
    "Mental Quickness": 15.0, "Maelstrom Weapon": 4.0, "Improved Stormstrike": 50.0,
}

SEARING_CU = {10: (9, 11), 20: (13, 17), 30: (19, 25), 40: (26, 34), 50: (33, 45), 60: (40, 54)}
WF_WEAPON_AP_CU = {30: 46, 40: 119, 50: 249, 60: 333}
WF_TOTEM_AP_CU = {32: 122, 42: 229, 52: 315}
SOE_CU = {10: 10, 24: 20, 38: 36, 52: 61, 60: 77}
GOA_CU = {42: 43, 56: 67, 60: 77}


def _tier(table, level, default=None):
    ks = [k for k in table if k <= level]
    return table[max(ks)] if ks else default


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


def _rank(name, level, paid=True):
    """Highest rank with (paid=True) or without (Overload copy) a mana cost."""
    rs = [s for s in core.ranks(CLASS, name) if s["base_level"] <= level and bool(s["costs"]) == paid]
    return rs[-1] if rs else None


class Fight:
    def __init__(self, sim, spec, race, level, inputs):
        self.sim, self.spec, self.level, self.inp = sim, spec, level, inputs
        ch = self.ch = core.Character(CLASS, race, level, talents_at(spec, level))
        core.apply_passive_racials(ch, race)
        self.tv = tv = lambda n: ch.tr(n) * _TT.get(n, 0.0)
        self.enh = spec == "enhancement"
        ch.int *= 1 + tv("Ancestral Knowledge") / 100
        ch.hit += tv("Tidal Focus")
        ch.crit_bonus += tv("Thundering Strikes")
        ch.spell_crit_bonus += tv("Thundering Strikes")
        ch.str += _tier(SOE_CU, level, 0)
        self.wf_weapon = self.enh and level >= 30
        if self.enh:
            ch.agi += _tier(GOA_CU, level, 0)
        self.wf_totem_ap = 0 if (self.wf_weapon or self.enh) else _tier(WF_TOTEM_AP_CU, level, 0)
        ch.sp = ch.int * tv("Mental Quickness") / 100
        self.base_ap = 2 * ch.str + 2 * level - 20 + ch.int * tv("Mental Dexterity") / 100
        self.wavg, self.speed = core.unarmed_weapon(level)
        self.max_mana = self.mana = ch.mana()
        self.last_spend = -10.0
        self.busy = 0.0
        self.cd = {}
        self.buff = {}
        self.ap_mult = 1.0
        self.sp_mult = 1.0
        self.speed_mult = 1.0
        self.flurry = 0
        self.mw = 0
        self.mw_exp = -1.0
        self.ss_charge = -1.0
        self.clearcast = False
        self.fs_until = -1.0
        self.totem_until = -1.0
        self.ws_icd = -1.0
        self.lb, self.lbo = _rank("Lightning Bolt", level), _rank("Lightning Bolt", level, False)
        self.cl, self.clo = _rank("Chain Lightning", level), _rank("Chain Lightning", level, False)
        self.es = _rank("Earth Shock", level)
        self.fs = _rank("Flame Shock", level)
        self.st = _rank("Searing Totem", level)
        self.ss = core.talent(CLASS, "Stormstrike")["ranks"][0] if ch.tr("Stormstrike") else None
        self.rof = _rank("Rage of the Farseer", 60) if ch.tr("Rage of the Farseer") else None
        inputs.update({"talents": "A (Forever tooltip)", "attack_power_formula": "CU", "unarmed_weapon": "CU",
                       "base_stats": ch.stats_tag, "spell_ranks": "F", "overload_ranks": "F",
                       "mana_regen_spirit": "CU", "searing_totem_damage": "CU", "shock_cooldown": "CU",
                       "totem_buffs": "CU", "fight_seconds": "A"})
        if self.enh:
            inputs.update({"windfury_weapon_ap": "CU", "windfury_extra_attacks": "A", "maelstrom_ppm": "A",
                           "stormstrike": "F", "imbue_on_unarmed": "A"})

    @property
    def t(self):
        return self.sim.t

    # ----- stats -----
    @property
    def ap(self):
        return self.base_ap * self.ap_mult

    @property
    def sp(self):
        return self.ch.sp * self.sp_mult

    def haste(self):
        return self.ch.haste * self.speed_mult

    def spend(self, c):
        if c > 0:
            self.mana -= c
            self.last_spend = self.t

    def cost(self, spell, red=0.0):
        return core.cost(spell, self.ch.base_mana)[1] * max(0.0, 1 - red / 100)

    def crit_mult(self):
        return 1 + (core.A("spell_crit_mult") - 1) * (1 + self.tv("Elemental Fury") / 100)

    # ----- damage -----
    def spell_hit(self, src, spell, mult=1.0, extra_crit=0.0, direct=True):
        e = core.damage_effect(spell)
        lo, hi = core.effect_range(e, self.level, spell["spell_level"])
        o = core.spell_roll(self.sim.rng, self.ch, extra_crit=extra_crit)
        if o == "miss":
            return False
        d = (self.sim.rng.uniform(lo, hi) + e["EffectBonusCoefficient"] * self.sp) * mult
        if o == "crit":
            d *= self.crit_mult()
            if self.ch.tr("Water Shield") and self.t >= self.ws_icd:
                self.ws_icd = self.t + 3.5
                self.mana = min(self.max_mana, self.mana + 0.02 * self.max_mana)
        self.sim.deal(src, d)
        return True

    def bolt(self, name, spell, ospell, ss_bonus):
        mult = (1 + self.tv("Concussion") / 100) * ss_bonus
        crit = self.tv("Call of Thunder")
        self.spell_hit(name, spell, mult, crit)
        if ospell and self.sim.rng.chance(self.tv("Lightning Overload")):
            self.spell_hit("Lightning Overload", ospell, mult, crit)

    def take_ss(self):
        if self.ss_charge > self.t:
            self.ss_charge = -1.0
            return 1.2
        return 1.0

    def melee_dmg(self, normalized=False, extra_ap=0.0):
        return self.wavg + (self.ap + extra_ap) / 14 * (2.4 if normalized else self.speed)

    def melee(self, src, base_fn, white, can_wf=True, extra_ap=0.0):
        o = core.melee_roll(self.sim.rng, self.ch, white=white)
        if o in ("miss", "dodge"):
            return
        d = base_fn(extra_ap)
        if o == "crit":
            d *= core.A("melee_crit_mult")
            if self.ch.tr("Flurry"):
                if self.flurry == 0:
                    self.speed_mult *= 1 + self.tv("Flurry") / 100
                self.flurry = 3
        elif o == "glance":
            d *= core.A("glance_damage")
        self.sim.deal(src, d)
        if self.ch.tr("Maelstrom Weapon") and self.sim.rng.chance(10 * self.speed / 60 * 100):
            self.mw = min(5, (self.mw if self.mw_exp > self.t else 0) + 1)
            self.mw_exp = self.t + 30
        if can_wf:
            if self.wf_weapon and self.sim.rng.chance(20):
                ap = _tier(WF_WEAPON_AP_CU, self.level) * (1 + self.tv("Elemental Weapons") / 100)
                for _ in range(2):
                    self.melee("Windfury", lambda x: self.melee_dmg(extra_ap=x), True, False, ap)
            elif self.wf_totem_ap and self.sim.rng.chance(20):
                for _ in range(2):
                    self.melee("Windfury", lambda x: self.melee_dmg(extra_ap=x), True, False, self.wf_totem_ap)

    # ----- events -----
    def swing(self):
        if self.flurry:
            self.flurry -= 1
            if self.flurry == 0:
                self.speed_mult /= 1 + self.tv("Flurry") / 100
        self.melee("Melee", lambda x: self.melee_dmg(extra_ap=x), True)
        self.sim.at(self.t + self.speed / self.haste(), self.swing)

    def regen(self):
        base = 17 + self.ch.spi / 5
        if self.t - self.last_spend >= 5:
            frac = 1.0
        else:
            frac = self.tv("Mindfulness") / 100
            if self.buff.get("iss", -1) > self.t:
                frac += self.tv("Improved Stormstrike") / 100
        self.mana = min(self.max_mana, self.mana + base * min(1.0, frac))
        self.sim.at(self.t + 2, self.regen)

    def totem_tick(self, until):
        if self.t > until:
            return
        lo, hi = _tier(SEARING_CU, self.level)
        o = core.spell_roll(self.sim.rng, self.ch)
        if o != "miss":
            d = self.sim.rng.uniform(lo, hi) * (1 + self.tv("Call of Flame") / 100)
            self.sim.deal("Searing Totem", d * (self.crit_mult() if o == "crit" else 1))
        self.sim.at(self.t + 2.5, self.totem_tick, until)

    def fs_tick(self, until, tick):
        if self.t <= until + 1e-6:
            self.sim.deal("Flame Shock", tick)

    def racial(self):
        cd = core.racial_cooldown(self.ch.race)
        if not cd:
            return
        kind, val, dur, every = cd
        if kind == "power":
            self.ap_mult *= 1 + val / 100
            self.sp_mult *= 1 + val / 100
            self.sim.at(self.t + dur, self.unbuff, "power", val)
        elif kind == "haste":
            self.speed_mult *= 1 + val / 100
            self.sim.at(self.t + dur, self.unbuff, "haste", val)
        else:
            return
        self.sim.at(self.t + every, self.racial)

    def unbuff(self, kind, val):
        if kind == "power":
            self.ap_mult /= 1 + val / 100
            self.sp_mult /= 1 + val / 100
        elif kind in ("haste", "rof"):
            self.speed_mult /= 1 + val / 100

    def ready(self, k):
        return self.cd.get(k, 0) <= self.t + 1e-9

    def after(self, dt):
        self.busy = self.t + dt
        self.sim.at(self.busy, self.act)

    def can(self, c):
        if self.clearcast:
            return True
        return self.mana >= c

    def pay(self, c, damage_spell=True):
        if self.clearcast and damage_spell:
            self.clearcast = False
            return
        self.spend(c)

    def after_damage_spell(self):
        if self.ch.tr("Elemental Focus") and self.sim.rng.chance(10):
            self.clearcast = True

    def act(self):
        if self.t < self.busy - 1e-9:
            return
        t, gcd, ch = self.t, 1.5 / self.haste(), self.ch
        gcd = max(1.0, gcd)
        shock_red = self.tv("Convection") + self.tv("Shamanistic Focus")
        # Searing Totem
        if self.st and self.totem_until <= t:
            c = self.cost(self.st, self.tv("Totemic Focus"))
            if self.mana >= c:
                self.spend(c)
                self.totem_until = t + self.st["duration_ms"] / 1000
                self.sim.cast("Searing Totem")
                self.sim.at(t + 0.5, self.totem_tick, self.totem_until)
                return self.after(gcd)
        if self.enh:
            if self.rof and self.ready("rof"):
                self.cd["rof"] = t + self.rof["cooldown_ms"] / 1000
                v = self.rof["effects"][0]["EffectBasePointsF"]
                self.speed_mult *= 1 + v / 100
                self.sim.at(t + self.rof["duration_ms"] / 1000, self.unbuff, "rof", v)
                self.sim.cast("Rage of the Farseer")
            if self.ss and self.ready("ss"):
                c = self.cost(self.ss)
                if self.mana >= c:
                    self.spend(c)
                    self.cd["ss"] = t + self.ss["cooldown_ms"] / 1000
                    self.sim.cast("Stormstrike")
                    pct = [e for e in self.ss["effects"] if e["Effect"] == core.WEAPON_PERCENT_DAMAGE][0]["EffectBasePointsF"]
                    self.melee("Stormstrike", lambda x: self.melee_dmg(True) * pct / 100, False)
                    self.ss_charge = t + 12
                    if ch.tr("Improved Stormstrike"):
                        self.buff["iss"] = t + 15
                    return self.after(gcd)
            if self.lb and self.mw >= 5 and self.mw_exp > t and ch.tr("Maelstrom Weapon"):
                red = self.tv("Maelstrom Weapon") * 5
                c = self.cost(self.lb, self.tv("Convection") + red)
                if self.can(c):
                    self.pay(c)
                    self.mw = 0
                    cast = self.lb["cast_ms"] / 1000 * max(0.0, 1 - red / 100) / self.haste()
                    self.sim.cast("Lightning Bolt")
                    self.sim.at(t + cast, self.bolt, "Lightning Bolt", self.lb, self.lbo, self.take_ss())
                    self.after_damage_spell()
                    return self.after(max(gcd, cast))
        else:
            if ch.tr("Lightning Mastery") and self.ready("lm"):
                self.cd["lm"] = t + 180
                self.buff["lm"] = t + 15
                self.sim.cast("Lightning Mastery")
        # Flame Shock
        if self.fs and self.fs_until <= t and self.ready("shock"):
            c = self.cost(self.fs, shock_red)
            if self.can(c) and (not self.enh or self.mana >= 0.3 * self.max_mana):
                self.pay(c)
                self.cd["shock"] = t + 6
                self.sim.cast("Flame Shock")
                mult = 1 + self.tv("Call of Flame") / 100
                self.spell_hit("Flame Shock", self.fs, mult)
                dot = [e for e in self.fs["effects"] if e["EffectAura"] == core.PERIODIC_DAMAGE][0]
                dur = self.fs["duration_ms"] / 1000 + 3 * ch.tr("Call of Flame")
                per = dot["EffectAuraPeriod"] / 1000
                tick = (dot["EffectBasePointsF"] + dot["EffectBonusCoefficient"] * self.sp) * mult
                self.fs_until = t + dur
                for i in range(1, int(dur / per + 1e-6) + 1):
                    self.sim.at(t + i * per, self.fs_tick, self.fs_until, tick)
                self.after_damage_spell()
                return self.after(gcd)
        if self.enh:
            if self.es and self.ready("shock") and self.mana >= 0.5 * self.max_mana:
                c = self.cost(self.es, shock_red)
                self.pay(c)
                self.cd["shock"] = t + 6
                self.sim.cast("Earth Shock")
                self.spell_hit("Earth Shock", self.es, (1 + self.tv("Concussion") / 100) * self.take_ss())
                self.after_damage_spell()
                return self.after(gcd)
            if not self.es and self.lb and self.mana >= 0.6 * self.max_mana:
                return self.cast_bolt(t, gcd, self.lb, self.lbo, "Lightning Bolt")
        else:
            if self.cl and (self.ready("cl") or self.buff.get("lm", -1) > t):
                c = self.cost(self.cl, self.tv("Convection"))
                if self.can(c):
                    self.cd["cl"] = t + 6
                    return self.cast_bolt(t, gcd, self.cl, self.clo, "Chain Lightning", c)
            if self.lb:
                c = self.cost(self.lb, self.tv("Convection"))
                if self.can(c):
                    return self.cast_bolt(t, gcd, self.lb, self.lbo, "Lightning Bolt", c)
        nxt = [v for v in self.cd.values() if v > t] + [t + 1.0, self.totem_until, self.fs_until]
        self.sim.at(min(x for x in nxt if x > t + 1e-6), self.act)

    def cast_bolt(self, t, gcd, spell, ospell, name, c=None):
        if c is None:
            c = self.cost(spell, self.tv("Convection"))
            if not self.can(c):
                return self.after(1.0)
        self.pay(c)
        cast = spell["cast_ms"] / 1000
        if name == "Lightning Bolt":
            cast -= self.tv("Elemental Alacrity") + (0.5 if self.buff.get("lm", -1) > t else 0)
        else:
            cast -= self.tv("Elemental Alacrity")
        cast = max(1.0, cast / self.haste())
        self.sim.cast(name)
        self.sim.at(t + cast, self.bolt, name, spell, ospell, self.take_ss())
        self.after_damage_spell()
        return self.after(max(gcd, cast))

    def start(self):
        if self.enh:
            self.sim.at(0.0, self.swing)
        self.sim.at(2.0, self.regen)
        self.sim.at(0.0, self.racial)
        self.sim.at(0.0, self.act)


def simulate(spec, race, level, iterations, seed):
    inputs = {}

    def build(sim):
        Fight(sim, spec, race, level, inputs).start()

    r = core.run_many(build, iterations, seed)
    r["inputs"] = inputs
    return r
