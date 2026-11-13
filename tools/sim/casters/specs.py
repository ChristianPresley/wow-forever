"""Spec models and priority APLs. Each class reads its numbers from data.json
through the Caster helpers (g / sv / tv), so every value it uses is tagged."""
from __future__ import annotations

from engine import Caster

DESTRO = {"shadow_bolt", "immolate", "conflagrate", "incinerate", "shadowburn", "searing_pain", "soul_fire"}


def avg_roll(sim, spell):
    return sim.rng.uniform(sim.sv(spell, "min"), sim.sv(spell, "max"))


# =====================================================================
# Mage
# =====================================================================
class Mage(Caster):
    cls = "mage"

    def setup_mage(self):
        self.extra_hit += self.tv("precision_hit")
        self.ac = self.tv("arcane_concentration")
        self.mb_ab = self.tv("missile_barrage_ab")
        self.mb_other = self.tv("missile_barrage_other")
        self.mb_speed = self.tv("missile_barrage_speed")
        am = "arcane_missiles"
        self.reg(am, "arcane", label="Arcane Missiles")
        self.am = (self.sv(am, "tick"), self.sv(am, "ticks"), self.sv(am, "coef_tick"), self.sv(am, "mana"), self.sv(am, "cast"))
        self.evo = (self.sv("evocation", "cd"), self.sv("evocation", "dur"), self.sv("evocation", "pct_per_tick"))
        self.reg("evocation", "arcane", label="Evocation")

    def proc_cc(self):
        if self.rng.random() < self.ac:
            self.buffs["cc"] = self.t + 15.0

    def proc_mb(self, chance):
        if self.rng.random() < chance:
            self.buffs["mb"] = self.t + 15.0  # duration not published (A)

    def cast_am(self):
        tick, ticks, coef, mana, cast = self.am
        free = self.up("mb")
        if free:
            del self.buffs["mb"]
            cost = 0.0
            dur = cast * (1 - self.mb_speed)
        else:
            if self.mana < self.peek_cost("arcane_missiles", mana):
                return False
            cost = self.cost("arcane_missiles", mana)
            dur = cast
        dur /= self.haste()

        def on_tick(i):
            r = self.direct("arcane_missiles", tick, coef)
            if r and r[0]:
                self.on_crit("arcane_missiles", r[1])
            if i == 1 and r is not None:
                self.proc_cc()
        return self.start_channel("arcane_missiles", dur, ticks, on_tick, cost)

    def cast_evocation(self):
        cd, dur, pct = self.evo
        self.cds["evocation"] = self.t + cd
        ticks = int(round(dur / 2))
        return self.start_channel("evocation", dur, ticks, lambda i: self.gain(pct * self.max_mana), 0.0)

    def want_evocation(self, threshold):
        return self.mana < threshold * self.max_mana and self.cd_ready("evocation") and self.fight - self.t > 15

    def on_crit(self, name, amt):
        pass


class Fire(Mage):
    spec = "Fire"
    build = "12/36/3"

    def setup(self):
        self.setup_mage()
        tv = self.tv
        self.crit_mass = tv("critical_mass")
        self.incin = tv("incineration")
        self.ignite_pct = tv("ignite")
        self.accel = tv("accelerant")
        self.fb_cd = self.sv("fire_blast", "cd") - tv("improved_fire_blast")
        self.scorch_stack, self.scorch_max, self.scorch_dur = tv("improved_scorch_stack"), tv("improved_scorch_max"), tv("improved_scorch_dur")
        self.heat = tv("heating_up")
        self.moe = tv("master_of_elements")
        self.fp, self.fp_max = tv("fire_power"), tv("fire_power_max")
        self.comb_step, self.comb_cd = tv("combustion_crit"), tv("combustion_cd")
        for n, lab in (("fireball", "Fireball"), ("scorch", "Scorch"), ("fire_blast", "Fire Blast"), ("pyroblast", "Pyroblast")):
            self.reg(n, "fire", label=lab)
        self.reg("fireball_dot", "fire", True, "Fireball (DoT)")
        self.reg("pyro_dot", "fire", True, "Pyroblast (DoT)")
        self.fbd = (self.sv("fireball", "dot_total"), self.sv("fireball", "dot_ticks"), self.sv("fireball", "dot_coef_tick"))
        self.pyd = (self.sv("pyroblast", "dot_total"), self.sv("pyroblast", "dot_ticks"), self.sv("pyroblast", "dot_coef_tick"))
        self.scorch_stacks = 0
        self.heating = 0
        self.comb_on = False
        self.comb_bonus = 0.0
        self.comb_crits = 0
        self.ign_pool = 0.0
        self.ign_ticks = 0
        self.ign_gen = 0
        self.ign_end = -1.0

    # ----- modifiers -----
    def crit_extra(self, name):
        c = 0.0
        if self.S[name]["school"] == "fire":
            c += self.crit_mass
            if self.comb_on and not self.S[name]["periodic"]:
                c += self.comb_bonus
        if name in ("fire_blast", "scorch"):
            c += self.incin
        return c

    def fire_effects(self):
        n = (self.ign_end > self.t) + (self.dot_rem("fireball_dot") > 0) + (self.dot_rem("pyro_dot") > 0) + self.up("imp_scorch")
        return min(self.fp_max, self.fp * n)

    def spec_mult(self, name, periodic):
        if self.S[name]["school"] != "fire":
            return 1.0
        m = 1 + self.fire_effects()
        if self.up("imp_scorch"):
            m *= 1 + self.scorch_stack * self.scorch_stacks
        return m

    def spec_off_gcd(self):
        if self.cd_ready("combustion") and not self.comb_on:
            self.comb_on, self.comb_bonus, self.comb_crits = True, self.comb_step, 0
            self.cds["combustion"] = self.t + self.comb_cd
            self.casts["Combustion"] += 1

    # ----- Ignite: rolling pool, 2 ticks over 4 s, refreshed by each crit -----
    def add_ignite(self, amt):
        if self.ign_end <= self.t:
            self.ign_pool = 0.0
        self.ign_pool += amt
        self.ign_ticks = 2
        self.ign_gen += 1
        self.ign_end = self.t + 4.0
        self.at(self.t + 2.0, self._ignite_tick, self.ign_gen)

    def _ignite_tick(self, gen):
        if gen != self.ign_gen:
            return
        a = self.ign_pool / self.ign_ticks
        self.ign_pool -= a
        self.ign_ticks -= 1
        self.deal("Ignite", a)
        if self.ign_ticks > 0:
            self.at(self.t + 2.0, self._ignite_tick, gen)
        else:
            self.ign_end = self.t

    def on_crit(self, name, amt):
        if self.S[name]["school"] == "fire":
            self.add_ignite(self.ignite_pct * amt)

    def fire_hit(self, name, base, coef, base_cost):
        r = self.direct(name, base, coef)
        if r is None:
            return None
        crit, amt = r
        if self.comb_on:
            if crit:
                self.comb_crits += 1
                if self.comb_crits >= 3:
                    self.comb_on = False
            self.comb_bonus += self.comb_step
        if crit:
            self.on_crit(name, amt)
            self.gain(self.moe * base_cost)
            if name in ("fireball", "fire_blast", "scorch"):
                self.heating = min(3, self.heating + 1)
        self.proc_cc()
        return r

    # ----- spells -----
    def _cast(self, name, cast, finish):
        base = self.sv(name, "mana")
        if self.mana < self.peek_cost(name, base):
            return False
        return self.start_cast(name, cast / self.haste() if cast > 0 else 0, lambda: finish(base), self.cost(name, base))

    def cast_fireball(self):
        def fin(bc):
            r = self.fire_hit("fireball", avg_roll(self, "fireball"), self.sv("fireball", "coef"), bc)
            if r is not None:
                tot, n, c = self.fbd
                self.apply_dot("fireball_dot", tot / n + c * self.spell_power(), n, 8.0 / n, False)
            self.proc_mb(self.mb_other)
        return self._cast("fireball", self.sv("fireball", "cast") - self.accel, fin)

    def cast_scorch(self):
        def fin(bc):
            r = self.fire_hit("scorch", avg_roll(self, "scorch"), self.sv("scorch", "coef"), bc)
            if r is not None:
                self.scorch_stacks = min(self.scorch_max, (self.scorch_stacks if self.up("imp_scorch") else 0) + 1)
                self.buffs["imp_scorch"] = self.t + self.scorch_dur
        return self._cast("scorch", self.sv("scorch", "cast"), fin)

    def cast_fire_blast(self):
        def fin(bc):
            self.fire_hit("fire_blast", avg_roll(self, "fire_blast"), self.sv("fire_blast", "coef"), bc)
        ok = self._cast("fire_blast", 0, fin)
        if ok:
            self.cds["fire_blast"] = self.t + self.fb_cd
        return ok

    def cast_pyroblast(self, precast=False):
        stacks = self.heating
        cast = self.sv("pyroblast", "cast") * (1 - self.heat * stacks)

        def fin(bc):
            r = self.fire_hit("pyroblast", avg_roll(self, "pyroblast"), self.sv("pyroblast", "coef"), bc)
            if r is not None:
                tot, n, c = self.pyd
                self.apply_dot("pyro_dot", tot / n + c * self.spell_power(), n, 12.0 / n, False)
        if precast:
            base = self.sv("pyroblast", "mana")
            self.pay(base)
            self.casts["Pyroblast"] += 1
            fin(base)
            return True
        ok = self._cast("pyroblast", cast, fin)
        if ok:
            self.heating = 0
        return ok

    def precast(self):
        self.cast_pyroblast(precast=True)  # WT-FIRE: pre-cast Pyroblast

    def apl(self):
        if self.want_evocation(0.10):
            return self.cast_evocation()
        sc = self.sv("scorch", "cast") / self.haste()
        if (self.scorch_stacks < self.scorch_max or not self.up("imp_scorch")
                or self.remaining("imp_scorch") < sc + 4.0):
            if self.cast_scorch():
                return True
        if self.heating >= 3 and self.cast_pyroblast():
            return True
        if self.up("mb") and self.cast_am():
            return True
        if self.cd_ready("fire_blast") and self.cast_fire_blast():
            return True
        return self.cast_fireball() or self.cast_scorch()


class Frost(Mage):
    spec = "Frost"
    build = "15/5/31"

    def setup(self):
        self.setup_mage()
        tv = self.tv
        self.shards = tv("ice_shards")
        self.fchan = tv("frost_channeling")
        self.shatter = tv("shatter")
        self.fof_p, self.fof_n = tv("fingers_of_frost"), tv("fingers_of_frost_charges")
        self.ifb = tv("improved_frostbolt")
        self.incin = self.D.get("talents.mage.incineration")
        self.ib = (self.sv("ice_barrier", "mana"), self.sv("ice_barrier", "dur"), self.sv("ice_barrier", "frost_bonus"),
                   self.sv("ice_barrier", "hold_bonus") * self.sv("ice_barrier", "hold_share"))
        self.reg("frostbolt", "frost", label="Frostbolt")
        self.reg("ice_lance", "frost", label="Ice Lance")
        self.reg("ice_barrier", "frost", label="Ice Barrier")
        self.fof = 0
        self.frozen_now = False

    def crit_extra(self, name):
        c = 0.0
        if name == "ice_lance":
            c += self.incin
        if self.frozen_now:
            c += self.shatter
        return c

    def crit_mult(self, name, periodic):
        if self.S[name]["school"] == "frost":
            return 1 + (self.base_crit_mult - 1) * (1 + self.shards)
        return self.base_crit_mult

    def spec_mult(self, name, periodic):
        if self.S[name]["school"] == "frost" and self.up("ice_barrier"):
            return 1 + self.ib[2] + self.ib[3]
        return 1.0

    def cost_mult(self, name):
        return 1 - self.fchan if self.S.get(name, {}).get("school") == "frost" else 1.0

    def _frozen_cast(self, name, fn):
        self.frozen_now = self.fof > 0
        if self.fof > 0:
            self.fof -= 1
        r = fn()
        self.frozen_now = False
        return r

    def cast_frostbolt(self):
        base = self.sv("frostbolt", "mana")
        if self.mana < self.peek_cost("frostbolt", base):
            return False

        def fin():
            r = self._frozen_cast("frostbolt", lambda: self.direct("frostbolt", avg_roll(self, "frostbolt"), self.sv("frostbolt", "coef")))
            if r is not None:
                self.proc_cc()
                if self.rng.random() < self.fof_p:
                    self.fof = self.fof_n
            self.proc_mb(self.mb_other)
        cast = (self.sv("frostbolt", "cast") - self.ifb) / self.haste()
        return self.start_cast("frostbolt", cast, fin, self.cost("frostbolt", base))

    def cast_ice_lance(self):
        base = self.sv("ice_lance", "mana")
        if self.mana < self.peek_cost("ice_lance", base):
            return False

        def fin():
            frozen = self.fof > 0
            mult = self.sv("ice_lance", "frozen_mult") if frozen else 1.0
            r = self._frozen_cast("ice_lance", lambda: self.direct("ice_lance", avg_roll(self, "ice_lance"), self.sv("ice_lance", "coef"), mult=mult))
            if r is not None:
                self.proc_cc()
        self.cds["fire_blast"] = self.t + self.sv("ice_lance", "cd")  # shared cooldown
        return self.start_cast("ice_lance", 0, fin, self.cost("ice_lance", base))

    def cast_barrier(self):
        mana, dur, _b, _h = self.ib
        if self.mana < mana:
            return False
        return self.start_cast("ice_barrier", 0, lambda: self.buffs.__setitem__("ice_barrier", self.t + dur), mana)

    def precast(self):
        self.buffs["ice_barrier"] = self.ib[1] + 0.0  # shield cast before the pull
        self.pay(self.ib[0])
        self.casts["Ice Barrier"] += 1

    def apl(self):
        if self.want_evocation(0.08):
            return self.cast_evocation()
        if self.remaining("ice_barrier") < 1.0 and self.cast_barrier():
            return True
        if self.fof > 0 and self.cd_ready("fire_blast") and self.cast_ice_lance():
            return True
        if self.up("mb") and self.cast_am():
            return True
        return self.cast_frostbolt()


class Arcane(Mage):
    spec = "Arcane"
    build = "38/10/3"

    def setup(self):
        self.setup_mage()
        tv = self.tv
        self.int_mult *= 1 + tv("arcane_mind_int")
        self.mind_crit = tv("arcane_mind_crit")
        self.impact = tv("arcane_impact")
        self.instab = tv("arcane_instability")
        self.regen_cast = tv("arcane_meditation")
        self.ap, self.ap_dur, self.ap_cd = tv("arcane_power"), tv("arcane_power_dur"), tv("arcane_power_cd")
        self.pom_cd = tv("presence_of_mind_cd")
        self.incin = tv("incineration")
        self.accel = tv("accelerant")
        self.reg("arcane_blast", "arcane", label="Arcane Blast")
        self.reg("arcane_wrath", "arcane", label="Arcane Wrath")
        self.ab_pct = self.sv("arcane_blast", "mana_pct_base")
        self.ab_max = self.sv("arcane_blast", "stack_max")
        self.ab_dur = self.sv("arcane_blast", "stack_dur")
        self.ab_int = self.sv("arcane_blast", "int_per_stack")
        self.aw_mm = self.sv("arcane_wrath", "max_mana_sp")
        self.ab_stacks = 0

    def stacks(self):
        return self.ab_stacks if self.up("ab") else 0

    def sp_extra(self):
        return self.int * self.ab_int * self.stacks()

    def crit_extra(self, name):
        c = self.instab
        if self.S[name]["school"] == "arcane":
            c += self.impact
        if name == "arcane_blast":
            c += self.incin
        return c

    def crit_mult(self, name, periodic):
        if self.S[name]["school"] == "arcane":
            return 1 + (self.base_crit_mult - 1) * (1 + self.mind_crit)
        return self.base_crit_mult

    def spec_mult(self, name, periodic):
        m = 1 + self.instab / 100.0
        if self.up("arcane_power"):
            m *= 1 + self.ap
        return m

    def cost_mult(self, name):
        return 1 + self.ap if self.up("arcane_power") else 1.0

    def spec_off_gcd(self):
        if self.cd_ready("arcane_power") and self.mana > 0.5 * self.max_mana:
            self.buffs["arcane_power"] = self.t + self.ap_dur
            self.cds["arcane_power"] = self.t + self.ap_cd
            self.casts["Arcane Power"] += 1

    def ab_cost(self):
        return self.ab_pct * self.base_mana * (1 + self.stacks())

    def cast_ab(self):
        base = self.ab_cost()
        if self.mana < self.peek_cost("arcane_blast", base):
            return False

        def fin():
            r = self.direct("arcane_blast", avg_roll(self, "arcane_blast"), self.sv("arcane_blast", "coef"))
            self.ab_stacks = min(self.ab_max, self.stacks() + 1)
            self.buffs["ab"] = self.t + self.ab_dur
            if r is not None:
                self.proc_cc()
            self.proc_mb(self.mb_ab)
        return self.start_cast("arcane_blast", self.sv("arcane_blast", "cast") / self.haste(), fin, self.cost("arcane_blast", base))

    def cast_aw(self):
        base = self.sv("arcane_wrath", "mana")
        if self.mana < self.peek_cost("arcane_wrath", base):
            return False
        cast = (self.sv("arcane_wrath", "cast") - self.accel) / self.haste()
        if self.cd_ready("pom"):
            self.cds["pom"] = self.t + self.pom_cd
            self.casts["Presence of Mind"] += 1
            cast = 0

        def fin():
            r = self.direct("arcane_wrath", avg_roll(self, "arcane_wrath"), self.sv("arcane_wrath", "coef"),
                            sp_extra=self.aw_mm * self.max_mana)
            if r is not None:
                self.proc_cc()
            self.proc_mb(self.mb_other)
        self.cds["arcane_wrath"] = self.t + self.sv("arcane_wrath", "cd")
        return self.start_cast("arcane_wrath", cast, fin, self.cost("arcane_wrath", base))

    def apl(self):
        if not self.up("arcane_power") and self.want_evocation(0.15):
            return self.cast_evocation()
        if self.cd_ready("arcane_wrath") and self.cast_aw():
            return True
        if self.up("mb") and self.cast_am():
            return True
        cost = self.peek_cost("arcane_blast", self.ab_cost())
        if self.up("arcane_power") or self.mana - cost > 0.35 * self.max_mana:
            if self.cast_ab():
                return True
        # Conserve: Arcane Missiles lets the Arcane Blast stacks fall off.
        return self.cast_am() or self.cast_ab()


# =====================================================================
# Warlock
# =====================================================================
class Warlock(Caster):
    cls = "warlock"
    pandemic = 0.0
    ruin = 0.0

    def setup_lock(self):
        self.ilt = self.tv("improved_life_tap")
        self.lt = (self.sv("life_tap", "base"), self.sv("life_tap", "spirit_coef"))
        self.reg("life_tap", "shadow", label="Life Tap")

    def life_tap(self):
        def fin():
            self.gain((self.lt[0] + self.lt[1] * self.spirit) * (1 + self.ilt))
        return self.start_cast("life_tap", 0, fin, 0.0)

    def crit_mult(self, name, periodic):
        if periodic:
            return 1 + (self.base_crit_mult - 1) * (1 + self.pandemic)
        if name in DESTRO:
            return 1 + (self.base_crit_mult - 1) * (1 + self.ruin)
        return self.base_crit_mult

    def dot_spell(self, name, label, extra=1.0, can_crit=True, key=None):
        """Instant or cast DoT from data (total, ticks, interval, coef_tick). Hit rolled on application."""
        tot, n, iv, c = self.sv(name, "total"), self.sv(name, "ticks"), self.sv(name, "interval"), self.sv(name, "coef_tick")
        self.reg(name, self.D._node(f"spells.{name}.school"), True, label)

        def fin():
            if self.roll_hit(name):
                self.apply_dot(key or name, tot / n + c * self.spell_power(), n, iv, can_crit, extra=extra)
                self.on_dot_applied(name)
            else:
                self.casts[label + " (miss)"] += 1
        return fin

    def on_dot_applied(self, name):
        pass

    def cast_dot(self, name, label, cast=0.0, extra=1.0):
        base = self.sv(name, "mana")
        self.reg(name, self.D._node(f"spells.{name}.school"), True, label)
        if self.mana < self.peek_cost(name, base):
            return False
        return self.start_cast(name, cast / self.haste() if cast > 0 else 0, self.dot_spell(name, label, extra), self.cost(name, base))


class Affliction(Warlock):
    spec = "Affliction (Wrack)"
    build = "33/0/18"

    def setup(self):
        self.setup_lock()
        tv = self.tv
        self.extra_hit += tv("suppression_hit")
        self.impcorr = tv("improved_corruption")
        self.amp, self.amp_cd = tv("amplify_curse"), tv("amplify_curse_cd")
        self.pandemic = tv("pandemic")
        self.ruin = tv("ruin")
        self.malev = tv("malevolence")
        self.nf, self.nf_dur = tv("nightfall"), tv("nightfall_dur")
        self.siphon_step, self.siphon_max = tv("soul_siphon"), tv("soul_siphon_max")
        self.smast = tv("shadow_mastery")
        self.isb, self.isb_dur = tv("improved_shadow_bolt"), tv("improved_shadow_bolt_dur")
        self.bane = tv("bane")
        self.cata = tv("cataclysm")
        self.reg("shadow_bolt", "shadow", label="Shadow Bolt")
        self.reg("wrack", "shadow", True, "Wrack")
        for n, lab in (("corruption", "Corruption"), ("agony", "Bane of Agony"), ("siphon_life", "Siphon Life")):
            self.reg(n, "shadow", True, lab)
        self.wr = (self.sv("wrack", "tick"), self.sv("wrack", "ticks"), self.sv("wrack", "coef_tick"),
                   self.sv("wrack", "mana"), self.sv("wrack", "cast"), self.sv("wrack", "dot_bonus"))

    def crit_extra(self, name):
        return self.malev if self.S[name]["school"] == "shadow" else 0.0

    def spec_mult(self, name, periodic):
        m = 1 + self.smast
        if self.up("isb"):
            m *= 1 + self.isb
        if name == "corruption":
            m *= 1 + self.impcorr
        return m

    def dot_mult(self, key):
        return 1 + self.wr[5] if self.up("wrack") and key in ("corruption", "agony", "siphon_life") else 1.0

    def cost_mult(self, name):
        return 1 - self.cata if name in DESTRO else 1.0

    def on_tick(self, key, crit, amt):
        if key == "corruption":
            self.roll_nightfall()

    def roll_nightfall(self):
        if self.rng.random() < self.nf:
            self.buffs["nightfall"] = self.t + self.nf_dur

    def cast_sb(self):
        base = self.sv("shadow_bolt", "mana")
        if self.mana < self.peek_cost("shadow_bolt", base):
            return False
        instant = self.up("nightfall")
        if instant:
            del self.buffs["nightfall"]

        def fin():
            r = self.direct("shadow_bolt", avg_roll(self, "shadow_bolt"), self.sv("shadow_bolt", "coef"))
            if r and r[0]:
                self.buffs["isb"] = self.t + self.isb_dur
        cast = 0 if instant else (self.sv("shadow_bolt", "cast") - self.bane) / self.haste()
        return self.start_cast("shadow_bolt", cast, fin, self.cost("shadow_bolt", base))

    def others(self):
        return sum(1 for k in ("corruption", "agony", "siphon_life") if self.dot_rem(k) > 0)

    def cast_wrack(self):
        tick, ticks, coef, mana, cast, _b = self.wr
        if self.mana < self.peek_cost("wrack", mana):
            return False
        dur = cast / self.haste()
        cost = self.cost("wrack", mana)
        landed = self.roll_hit("wrack")
        if landed:
            self.buffs["wrack"] = self.t + dur
        else:
            self.casts["Wrack (miss)"] += 1

        def on_tick(i):
            if not landed:
                return
            siphon = 1 + min(self.siphon_max, self.siphon_step * self.others())
            self.direct("wrack", tick, coef, mult=siphon, periodic=True, hit_rolled=True)
            self.roll_nightfall()
        return self.start_channel("wrack", dur, ticks, on_tick, cost)

    def apl(self):
        if self.dot_rem("agony") < 2.0:
            extra = 1.0
            if self.cd_ready("amplify"):
                extra = 1 + self.amp
            if self.cast_dot("agony", "Bane of Agony", extra=extra):
                if extra > 1:
                    self.cds["amplify"] = self.t + self.amp_cd
                    self.casts["Amplify Curse"] += 1
                return True
        if self.dot_rem("corruption") < 3.0 and self.cast_dot("corruption", "Corruption", cast=self.sv("corruption", "cast") - 2.0):
            return True
        if self.dot_rem("siphon_life") < 3.0 and self.cast_dot("siphon_life", "Siphon Life"):
            return True
        if self.up("nightfall") and self.cast_sb():
            return True
        if self.mana < 0.35 * self.max_mana:
            return self.life_tap()
        return self.cast_wrack() or self.life_tap()


class Destruction(Warlock):
    spec = "Destruction"
    build = "14/4/33"

    def setup(self):
        self.setup_lock()
        tv = self.tv
        self.extra_hit += tv("suppression_hit")
        self.impcorr = tv("improved_corruption")
        self.pandemic = tv("pandemic_destro")
        self.ruin = tv("ruin")
        self.bane = tv("bane")
        self.cata = tv("cataclysm")
        self.after = tv("aftermath_destro")
        self.agon = tv("agonizing_flames")
        self.fnb = tv("fire_and_brimstone")
        self.snf, self.snf_dur = tv("shadow_and_flame"), tv("shadow_and_flame_dur")
        for n, sch, lab in (("immolate", "fire", "Immolate"), ("conflagrate", "fire", "Conflagrate"),
                            ("incinerate", "fire", "Incinerate"), ("shadowburn", "shadow", "Shadowburn")):
            self.reg(n, sch, label=lab)
        self.reg("immolate_dot", "fire", True, "Immolate (DoT)")
        self.reg("corruption", "shadow", True, "Corruption")

    def crit_extra(self, name):
        return self.fnb if name == "conflagrate" else 0.0

    def spec_mult(self, name, periodic):
        m = 1.0
        if name in DESTRO or name == "immolate_dot":
            m *= 1 + self.agon
        if name == "corruption":
            m *= 1 + self.impcorr
        sch = self.S[name]["school"]
        if sch == "fire" and self.up("snf_fire"):
            m *= 1 + self.snf
        if sch == "shadow" and self.up("snf_shadow"):
            m *= 1 + self.snf
        return m

    def cost_mult(self, name):
        return 1 - self.cata if name in DESTRO else 1.0

    def _cast(self, name, cast, fin):
        base = self.sv(name, "mana")
        if self.mana < self.peek_cost(name, base):
            return False
        return self.start_cast(name, cast / self.haste() if cast > 0 else 0, fin, self.cost(name, base))

    def cast_immolate(self):
        def fin():
            r = self.direct("immolate", self.sv("immolate", "direct"), self.sv("immolate", "coef"), mult=1 + self.after)
            if r is not None:
                n, iv = self.sv("immolate", "ticks"), self.sv("immolate", "interval")
                self.apply_dot("immolate_dot", self.sv("immolate", "total") / n + self.sv("immolate", "coef_tick") * self.spell_power(), n, iv, True)
        return self._cast("immolate", self.sv("immolate", "cast") - self.bane, fin)

    def cast_conflag(self):
        def fin():
            r = self.direct("conflagrate", avg_roll(self, "conflagrate"), self.sv("conflagrate", "coef"))
            if r is not None:
                self.buffs["snf_shadow"] = self.t + self.snf_dur  # Shadow and Flame 5/5 keeps Immolate (TT)
        ok = self._cast("conflagrate", 0, fin)
        if ok:
            self.cds["conflagrate"] = self.t + self.sv("conflagrate", "cd")
        return ok

    def cast_shadowburn(self):
        def fin():
            r = self.direct("shadowburn", avg_roll(self, "shadowburn"), self.sv("shadowburn", "coef"))
            if r is not None:
                self.buffs["snf_fire"] = self.t + self.snf_dur
        ok = self._cast("shadowburn", 0, fin)
        if ok:
            self.cds["shadowburn"] = self.t + self.sv("shadowburn", "cd")
        return ok

    def cast_incinerate(self):
        def fin():
            bonus = 1 + self.sv("incinerate", "immolate_bonus") if self.dot_rem("immolate_dot") > 0 else 1.0
            self.direct("incinerate", avg_roll(self, "incinerate"), self.sv("incinerate", "coef"), mult=bonus)
        return self._cast("incinerate", self.sv("incinerate", "cast") - self.bane, fin)

    def apl(self):
        h = self.haste()
        if self.dot_rem("immolate_dot") < (self.sv("immolate", "cast") - self.bane) / h and self.cast_immolate():
            return True
        if self.cd_ready("conflagrate") and self.dot_rem("immolate_dot") > 0 and self.cast_conflag():
            return True
        if self.cd_ready("shadowburn") and self.cast_shadowburn():
            return True
        if self.dot_rem("corruption") < 3.0 and self.cast_dot("corruption", "Corruption"):
            return True
        if self.mana < 0.25 * self.max_mana:
            return self.life_tap()
        return self.cast_incinerate() or self.life_tap()


class Demonology(Warlock):
    spec = "Demonology"
    build = "2/31/18"

    def setup(self):
        self.setup_lock()
        tv = self.tv
        self.mana_mult *= 1 + tv("fel_vitality")
        self.extra_sp += tv("demonic_knowledge")
        self.dk = tv("demonic_knowledge")
        self.ruin = tv("ruin")
        self.bane = tv("bane")
        self.cata = tv("cataclysm")
        self.after = tv("aftermath_demo")
        self.agon = tv("agonizing_flames")
        self.sac = tv("demonic_sacrifice_fire")
        self.md = tv("master_demonologist")
        self.link = tv("soul_link")
        self.unholy = tv("unholy_power")
        self.impimp = tv("improved_imp")
        self.brand_n, self.brand_dmg, self.brand_sp, self.brand_dur = (tv("demonic_brand_charges"), tv("demonic_brand_dmg"),
                                                                      tv("demonic_brand_sp"), tv("demonic_brand_dur"))
        self.deci_cut, self.deci_bonus, self.deci_speed, self.deci_dur = (tv("decimation_cd_cut"), tv("decimation_bonus"),
                                                                          tv("decimation_speed"), tv("decimation_dur"))
        for n, sch, lab in (("immolate", "fire", "Immolate"), ("searing_pain", "fire", "Searing Pain"),
                            ("soul_fire", "fire", "Soul Fire")):
            self.reg(n, sch, label=lab)
        self.reg("immolate_dot", "fire", True, "Immolate (DoT)")
        self.reg("corruption", "shadow", True, "Corruption")
        self.reg("agony", "shadow", True, "Bane of Agony")
        self.reg("doom", "shadow", True, "Bane of Doom")
        self.reg("imp_firebolt", "fire", label="Imp: Firebolt")
        self.reg("brand", "fire", label="Demonic Brand")
        self.imp = (self.sv("imp_firebolt", "min"), self.sv("imp_firebolt", "max"), self.sv("imp_firebolt", "cast"),
                    self.sv("imp_firebolt", "owner_sp_share"), self.sv("imp_firebolt", "coef"), self.sv("imp_firebolt", "base_crit"))
        self.imp_scale = self.sv("imp_firebolt", "calibration")
        self.brand_left = 0

    def crit_extra(self, name):
        return self.agon * 100 if name == "searing_pain" else 0.0

    def spec_mult(self, name, periodic):
        m = 1 + self.link
        if self.S[name]["school"] == "fire":
            m *= (1 + self.sac) * (1 + self.md)
        if name in DESTRO or name == "immolate_dot":
            m *= 1 + self.agon
        if name in ("shadow_bolt", "searing_pain") and self.hp() < 0.35:
            m *= 1 + self.deci_bonus
        return m

    def cost_mult(self, name):
        return 1 - self.cata if name in DESTRO else 1.0

    # ----- the Imp (kept out with Demonic Pact; Sayaad sacrificed) -----
    def _imp(self):
        lo, hi, cast, share, coef, crit = self.imp
        if self.rng.random() < self.hit_p("imp_firebolt"):
            pet_sp = share * self.spell_power() + self.dk
            m = (self.debuff("fire") * (1 + self.impimp) * (1 + self.unholy) * (1 + self.md) * (1 + self.link)
                 * self.pet_mult_race * self.imp_scale)
            amt = (self.rng.uniform(lo, hi) + coef * pet_sp) * m
            if self.rng.random() * 100 < crit:
                amt *= self.base_crit_mult
            self.deal("Imp: Firebolt", amt)
            if self.brand_left > 0 and self.up("brand"):
                self.brand_left -= 1
                self.deal("Demonic Brand", (self.brand_dmg + self.brand_sp * self.spell_power()) * self.debuff("fire")
                          * (1 + self.md) * (1 + self.link) * self.pet_mult_race)
        self.at(self.t + cast, self._imp)

    def _cast(self, name, cast, fin):
        base = self.sv(name, "mana")
        if self.mana < self.peek_cost(name, base):
            return False
        return self.start_cast(name, cast / self.haste() if cast > 0 else 0, fin, self.cost(name, base))

    def soul_fire_hit(self):
        self.direct("soul_fire", avg_roll(self, "soul_fire"), self.sv("soul_fire", "coef"))

    def precast(self):
        self.at(self.t, self._imp)
        self.pay(self.sv("soul_fire", "mana"))
        self.casts["Soul Fire"] += 1
        self.soul_fire_hit()  # WT-DEMO: open with Soul Fire landing on the pull
        self.cds["soul_fire"] = self.t + self.sv("soul_fire", "cd") * (1 - self.deci_cut)

    def cast_searing(self):
        def fin():
            r = self.direct("searing_pain", avg_roll(self, "searing_pain"), self.sv("searing_pain", "coef"))
            if r is not None:
                self.buffs["brand"] = self.t + self.brand_dur
                self.brand_left = self.brand_n
                if self.hp() < 0.35:
                    self.buffs["decimation"] = self.t + self.deci_dur
        return self._cast("searing_pain", self.sv("searing_pain", "cast"), fin)

    def cast_soul_fire(self):
        # Bane 5/5 takes 2 s off Soul Fire (4x its 0.5 s Shadow Bolt value), then Decimation -40%.
        cast = (self.sv("soul_fire", "cast") - 4 * self.bane) * (1 - self.deci_speed)
        ok = self._cast("soul_fire", cast, self.soul_fire_hit)
        if ok:
            self.cds["soul_fire"] = self.t + self.sv("soul_fire", "cd") * (1 - self.deci_cut)
        return ok

    def cast_immolate(self):
        def fin():
            r = self.direct("immolate", self.sv("immolate", "direct"), self.sv("immolate", "coef"), mult=1 + self.after)
            if r is not None:
                n, iv = self.sv("immolate", "ticks"), self.sv("immolate", "interval")
                self.apply_dot("immolate_dot", self.sv("immolate", "total") / n + self.sv("immolate", "coef_tick") * self.spell_power(), n, iv, True)
        return self._cast("immolate", self.sv("immolate", "cast") - self.bane, fin)

    def cast_doom(self):
        base = self.sv("doom", "mana")
        if self.mana < self.peek_cost("doom", base):
            return False
        delay = self.sv("doom", "delay")

        def fin():
            if self.roll_hit("doom"):
                self.apply_dot("doom", self.sv("doom", "total") + self.sv("doom", "coef") * self.spell_power(), 1, delay, True)
            else:
                self.casts["Bane of Doom (miss)"] += 1
        self.cds["doom"] = self.t + self.sv("doom", "cd")
        return self.start_cast("doom", 0, fin, self.cost("doom", base))

    def apl(self):
        if (not self.up("brand") or self.brand_left == 0) and self.cast_searing():
            return True
        left = self.fight - self.t
        if self.dot_rem("doom") <= 0:
            if left >= self.sv("doom", "delay") and self.cd_ready("doom"):
                if self.cast_doom():
                    return True
            elif left < self.sv("doom", "delay") and self.dot_rem("agony") < 2.0 and self.cast_dot("agony", "Bane of Agony"):
                return True
        if self.dot_rem("immolate_dot") < (self.sv("immolate", "cast") - self.bane) / self.haste() and self.cast_immolate():
            return True
        if self.up("decimation") and self.cd_ready("soul_fire") and self.cast_soul_fire():
            return True
        if self.dot_rem("corruption") < 3.0 and self.cast_dot("corruption", "Corruption", cast=self.sv("corruption", "cast")):
            return True
        if self.mana < 0.30 * self.max_mana:
            return self.life_tap()
        return self.cast_searing() or self.life_tap()


# =====================================================================
# Priest
# =====================================================================
class Shadow(Caster):
    cls = "priest"
    spec = "Shadow"
    build = "20/0/31"
    INSTANT = {"swp", "devouring_plague", "swd", "vampiric_embrace"}

    def setup(self):
        tv = self.tv
        self.int_mult *= 1 + tv("mental_strength")
        self.extra_hit += tv("shadow_focus_hit")
        self.regen_cast = tv("meditation")
        self.twin = tv("twin_disciplines")
        self.agility = tv("mental_agility")
        self.if_crit, self.if_cd = tv("inner_focus_crit"), tv("inner_focus_cd")
        self.imb = tv("improved_mind_blast")
        self.swp_extra = tv("improved_swp_ticks")
        self.imf = tv("improved_mind_flay")
        self.weave, self.weave_max, self.weave_dur = tv("shadow_weaving"), tv("shadow_weaving_max"), tv("shadow_weaving_dur")
        self.contagion = tv("devouring_contagion")
        self.dark = tv("darkness")
        self.sf_dmg, self.sf_cost, self.sf_crit = tv("shadowform_dmg"), tv("shadowform_cost"), tv("shadowform_crit")
        for n, lab, per in (("mind_blast", "Mind Blast", False), ("mind_flay", "Mind Flay", True), ("swp", "Shadow Word: Pain", True),
                            ("devouring_plague", "Devouring Plague", True), ("swd", "Shadow Word: Death", False),
                            ("vampiric_embrace", "Vampiric Embrace", False)):
            self.reg(n, "shadow", per, lab)
        self.weave_n = 0
        self.if_on = False

    def add_weave(self):
        # Shadow Weaving 3/3: 100% chance per landed Shadow spell (TT)
        self.weave_n = min(self.weave_max, (self.weave_n if self.up("weave") else 0) + 1)
        self.buffs["weave"] = self.t + self.weave_dur

    def spec_mult(self, name, periodic):
        m = (1 + self.sf_dmg) * (1 + self.dark)
        if self.up("weave"):
            m *= 1 + self.weave * self.weave_n
        if name in self.INSTANT:
            m *= 1 + self.twin
        return m

    def crit_extra(self, name):
        return self.if_crit if (self.if_on and name == "mind_blast") else 0.0

    def crit_mult(self, name, periodic):
        return 1 + (self.base_crit_mult - 1) * (1 + self.sf_crit)

    def cost_mult(self, name):
        m = 1 - self.sf_cost
        if name in self.INSTANT:
            m *= 1 - self.agility
        if name == "devouring_plague":
            m *= 1 - self.contagion
        return m

    def _cast(self, name, cast, fin):
        base = self.sv(name, "mana")
        if self.mana < self.peek_cost(name, base):
            return False
        return self.start_cast(name, cast / self.haste() if cast > 0 else 0, fin, self.cost(name, base))

    def cast_mb(self, precast=False):
        use_if = self.cd_ready("inner_focus")

        def fin():
            self.if_on = use_if
            r = self.direct("mind_blast", avg_roll(self, "mind_blast"), self.sv("mind_blast", "coef"))
            self.if_on = False
            if r is not None:
                self.add_weave()
        self.cds["mind_blast"] = self.t + self.sv("mind_blast", "cd") - self.imb
        if use_if:
            self.cds["inner_focus"] = self.t + self.if_cd
            self.casts["Inner Focus"] += 1
            self.buffs["cc"] = self.t + 30  # free spell
        if precast:
            self.pay(self.cost("mind_blast", self.sv("mind_blast", "mana")))
            self.casts["Mind Blast"] += 1
            fin()
            return True
        return self._cast("mind_blast", self.sv("mind_blast", "cast"), fin)

    def cast_dot(self, name, extra_ticks=0):
        def fin():
            if self.roll_hit(name):
                n = self.sv(name, "ticks") + extra_ticks
                per = self.sv(name, "total") / self.sv(name, "ticks") + self.sv(name, "coef_tick") * self.spell_power()
                self.apply_dot(name, per, n, self.sv(name, "interval"), False)
                self.add_weave()
            else:
                self.casts[self.S[name]["label"] + " (miss)"] += 1
        return self._cast(name, 0, fin)

    def cast_swd(self):
        def fin():
            # Early Demise is not in the 20/0/31 raid build, so no execute crit bonus.
            r = self.direct("swd", avg_roll(self, "swd"), self.sv("swd", "coef"))
            if r is not None:
                self.add_weave()
        self.cds["swd"] = self.t + self.sv("swd", "cd")
        return self._cast("swd", 0, fin)

    def cast_ve(self):
        dur = self.sv("vampiric_embrace", "dur")
        base = self.sv("vampiric_embrace", "mana")
        return self.start_cast("vampiric_embrace", 0, lambda: self.buffs.__setitem__("ve", self.t + dur), self.cost("vampiric_embrace", base))

    def cast_mf(self):
        base = self.sv("mind_flay", "mana")
        if self.mana < self.peek_cost("mind_flay", base):
            return False
        n = self.sv("mind_flay", "ticks")
        per = self.sv("mind_flay", "total") / n
        coef = self.sv("mind_flay", "coef_tick")
        landed = self.roll_hit("mind_flay")
        if landed:
            self.add_weave()
        else:
            self.casts["Mind Flay (miss)"] += 1

        def on_tick(i):
            if landed:
                self.direct("mind_flay", per, coef, mult=1 + self.imf * (i - 1), periodic=True, hit_rolled=True, can_crit=False)
        return self.start_channel("mind_flay", self.sv("mind_flay", "cast") / self.haste(), n, on_tick, self.cost("mind_flay", base))

    def precast(self):
        self.cast_mb(precast=True)  # WT-SP opener: pre-cast Mind Blast

    def apl(self):
        if not self.up("ve") and self.cast_ve():
            return True
        if self.dot_rem("swp") < 1.5 and self.cast_dot("swp", self.swp_extra):
            return True
        if self.cd_ready("devouring_plague") and self.cast_dot("devouring_plague"):
            self.cds["devouring_plague"] = self.t + self.sv("devouring_plague", "cd")
            return True
        if self.cd_ready("mind_blast") and self.cast_mb():
            return True
        if self.cd_ready("swd") and self.cast_swd():
            return True
        return self.cast_mf()


# =====================================================================
# Druid
# =====================================================================
class Balance(Caster):
    cls = "druid"
    spec = "Balance"
    build = "36/0/15"

    def setup(self):
        tv = self.tv
        self.int_mult *= 1 + tv("heart_of_the_wild")
        self.extra_hit += tv("natures_reach")
        self.extra_crit += tv("natures_majesty")
        self.regen_cast = tv("reflection")
        self.nat = tv("naturalist")
        self.moonfury = tv("moonfury")
        self.veng = tv("vengeance")
        self.imf = tv("improved_moonfire")
        self.moonglow = tv("moonglow")
        self.iw_cast, self.iw_mana = tv("improved_wrath_cast"), tv("improved_wrath_mana")
        self.isf = tv("improved_starfire")
        self.ng, self.ng_dur = tv("natures_grace"), tv("natures_grace_dur")
        self.ecl, self.ecl_dur = tv("eclipse"), tv("eclipse_dur")
        self.mf_extra, self.is_extra = tv("splendor_mf_ticks"), tv("splendor_is_ticks")
        self.omen = self.sv("omen", "chance") * 2  # Moonkin Form doubles Omen (TT)
        for n, sch, lab, per in (("starfire", "arcane", "Starfire", False), ("wrath", "nature", "Wrath", False),
                                 ("moonfire", "arcane", "Moonfire", False), ("moonfire_dot", "arcane", "Moonfire (DoT)", True),
                                 ("insect_swarm", "nature", "Insect Swarm", True)):
            self.reg(n, sch, per, lab)
        self.charges = 0

    def spec_mult(self, name, periodic):
        m = (1 + self.nat) * (1 + self.moonfury)
        if name in ("moonfire", "moonfire_dot"):
            m *= 1 + self.imf
        return m

    def crit_extra(self, name):
        return self.imf * 100 if name == "moonfire" else 0.0

    def crit_mult(self, name, periodic):
        return 1 + (self.base_crit_mult - 1) * (1 + self.veng)

    def cost_mult(self, name):
        m = 1 - self.moonglow
        if name == "wrath":
            m *= 1 - self.iw_mana
        return m

    def haste_extra(self):
        return 1 + self.ng if self.up("ng") else 1.0

    def after_cast(self, r):
        if r is not None and r[0]:
            self.buffs["ng"] = self.t + self.ng_dur
        if self.rng.random() < self.omen:
            self.buffs["cc"] = self.t + 15.0

    def _cast(self, name, cast, fin):
        base = self.sv(name, "mana")
        if self.mana < self.peek_cost(name, base):
            return False
        return self.start_cast(name, cast / self.haste() if cast > 0 else 0, fin, self.cost(name, base))

    def cast_starfire(self):
        cast = self.sv("starfire", "cast") - self.isf
        if self.up("eclipse") and self.charges > 0:
            cast -= self.ecl
            used = True
        else:
            used = False

        def fin():
            self.after_cast(self.direct("starfire", avg_roll(self, "starfire"), self.sv("starfire", "coef")))
        ok = self._cast("starfire", cast, fin)
        if ok and used:
            self.charges -= 1
        return ok

    def cast_wrath(self):
        def fin():
            self.after_cast(self.direct("wrath", avg_roll(self, "wrath"), self.sv("wrath", "coef")))
            self.charges = min(4, (self.charges if self.up("eclipse") else 0) + 2)
            self.buffs["eclipse"] = self.t + self.ecl_dur
        return self._cast("wrath", self.sv("wrath", "cast") - self.iw_cast, fin)

    def cast_moonfire(self):
        def fin():
            r = self.direct("moonfire", avg_roll(self, "moonfire"), self.sv("moonfire", "coef"))
            if r is not None:
                n = self.sv("moonfire", "ticks")
                per = self.sv("moonfire", "total") / n + self.sv("moonfire", "coef_tick") * self.spell_power()
                self.apply_dot("moonfire_dot", per, n + self.mf_extra, self.sv("moonfire", "interval"), False)
            self.after_cast(r)
        return self._cast("moonfire", 0, fin)

    def cast_swarm(self):
        def fin():
            if self.roll_hit("insect_swarm"):
                n = self.sv("insect_swarm", "ticks")
                per = self.sv("insect_swarm", "total") / n + self.sv("insect_swarm", "coef_tick") * self.spell_power()
                self.apply_dot("insect_swarm", per, n + self.is_extra, self.sv("insect_swarm", "interval"), False)
            else:
                self.casts["Insect Swarm (miss)"] += 1
            if self.rng.random() < self.omen:
                self.buffs["cc"] = self.t + 15.0
        return self._cast("insect_swarm", 0, fin)

    def apl(self):
        if self.dot_rem("moonfire_dot") < 1.0 and self.cast_moonfire():
            return True
        if self.dot_rem("insect_swarm") < 1.0 and self.cast_swarm():
            return True
        if self.up("cc"):
            return self.cast_starfire()
        if self.up("eclipse") and self.charges > 0:
            return self.cast_starfire()
        return self.cast_wrath() or self.cast_starfire()


# =====================================================================
# Shaman
# =====================================================================
class Elemental(Caster):
    cls = "shaman"
    spec = "Elemental"
    build = "31/9/11"

    def setup(self):
        tv = self.tv
        self.int_mult *= 1 + tv("ancestral_knowledge")
        self.extra_hit += tv("tidal_focus_hit")
        self.regen_cast = tv("mindfulness")
        self.conv = tv("convection")
        self.conc = tv("concussion")
        self.alac = tv("elemental_alacrity")
        self.focus = tv("elemental_focus")
        self.cot = tv("call_of_thunder")
        self.lo = tv("lightning_overload")
        self.ef = tv("elemental_fury")
        self.lm_cast, self.lm_dur, self.lm_cd = tv("lightning_mastery_cast"), tv("lightning_mastery_dur"), tv("lightning_mastery_cd")
        self.ws_pct, self.ws_max = tv("water_shield_pct"), tv("water_shield_globes")
        self.reg("lightning_bolt", "nature", label="Lightning Bolt")
        self.reg("chain_lightning", "nature", label="Chain Lightning")
        self.reg("overload", "nature", label="Lightning Overload")
        self.reg("water_shield", "nature", label="Water Shield")
        self.globes = self.ws_max

    def spec_mult(self, name, periodic):
        return 1 + self.conc

    def crit_extra(self, name):
        return self.cot

    def crit_mult(self, name, periodic):
        return 1 + (self.base_crit_mult - 1) * (1 + self.ef)

    def cost_mult(self, name):
        return 1 - self.conv

    def spec_off_gcd(self):
        if self.cd_ready("lightning_mastery"):
            self.buffs["lm"] = self.t + self.lm_dur
            self.cds["lightning_mastery"] = self.t + self.lm_cd
            self.casts["Lightning Mastery"] += 1

    def on_hit(self, r):
        if r is not None and r[0] and self.globes > 0:
            self.globes -= 1
            self.gain(self.ws_pct * self.max_mana)

    def lb_base(self):
        return avg_roll(self, "lightning_bolt")

    def bolt(self, name, base, coef):
        r = self.direct(name, base, coef)
        self.on_hit(r)
        if self.rng.random() < self.lo:
            self.on_hit(self.direct("overload", base, coef, mult=0.5))
        if self.rng.random() < self.focus:
            self.buffs["cc"] = self.t + 15.0

    def cast_lb(self):
        base = self.sv("lightning_bolt", "mana")
        if self.mana < self.peek_cost("lightning_bolt", base):
            return False
        cast = self.sv("lightning_bolt", "cast") - self.alac - (self.lm_cast if self.up("lm") else 0)
        return self.start_cast("lightning_bolt", cast / self.haste(),
                               lambda: self.bolt("lightning_bolt", self.lb_base(), self.sv("lightning_bolt", "coef")),
                               self.cost("lightning_bolt", base))

    def cast_cl(self):
        base = self.sv("lightning_bolt", "mana") * self.sv("chain_lightning", "mana_ratio")
        if self.mana < self.peek_cost("chain_lightning", base) or self.mana < 0.3 * self.max_mana:
            return False
        ratio = self.sv("chain_lightning", "lb_ratio")
        cast = (self.sv("chain_lightning", "cast") - self.alac) / self.haste()
        if not self.up("lm"):
            self.cds["chain_lightning"] = self.t + self.sv("chain_lightning", "cd")
        return self.start_cast("chain_lightning", cast,
                               lambda: self.bolt("chain_lightning", self.lb_base() * ratio, self.sv("chain_lightning", "coef")),
                               self.cost("chain_lightning", base))

    def cast_ws(self):
        def fin():
            self.globes = self.ws_max
        return self.start_cast("water_shield", 0, fin, self.sv("water_shield", "mana"))

    def apl(self):
        if self.globes == 0 and self.cast_ws():
            return True
        if (self.cd_ready("chain_lightning") or self.up("lm")) and self.cast_cl():
            return True
        return self.cast_lb()


SPECS = [Fire, Frost, Arcane, Affliction, Destruction, Demonology, Shadow, Balance, Elemental]
