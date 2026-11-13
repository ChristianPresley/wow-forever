"""Players and priority APLs for the physical specs. See README.md for the rules."""
from __future__ import annotations

from engine import (CRIT, DODGE, GLANCE, HIT, MISS, Dot, Swing, armor_multiplier,
                    ppm_chance, rage_from_damage, roll_white, roll_yellow)

LANDED = (HIT, CRIT, GLANCE)


class Player:
    cls = ""
    spec = ""
    gear_key = ""
    gcd_len_key = ("model", "gcd")
    melee = True

    def __init__(self, sim, d, race):
        self.sim, self.d, self.race = sim, d, race
        self.rng = sim.rng
        self.auras = {}           # name -> expiry time
        self.stacks = {}          # name -> stack count
        self.cds = {}             # name -> ready time
        self.gcd_until = 0.0
        self.cast_until = 0.0
        self.swings = []
        self.flurry = 0
        self.flurry_haste = 0.0
        self.totg_ready = 0.0
        self.last_mana_spend = -99.0
        self._stats()

    # ---------------------------------------------------------------- stats
    def g(self, key):
        return self.d("gear", self.gear_key, key)

    def _stats(self):
        d, r = self.d, self.race
        kings = 1 + d("buffs", "kings")
        motw = d("buffs", "motw")
        self.str = (self.g("str") + d("races", r, "str") + motw + d("buffs", "soe")) * kings
        self.agi = (self.g("agi") + d("races", r, "agi") + motw + d("buffs", "goa")) * kings
        self.int = (self.g("int") + d("races", r, "int") + motw + d("buffs", "arcane_int")) * kings
        self.hit = self.g("hit") + (d("racials", "dwarf_hit") if r == "dwarf" else 0)
        crit = d("model", "base_melee_crit") + self.g("crit")
        per = {"hunter": d("model", "agi_per_crit_hunter"), "rogue": d("model", "agi_per_crit_rogue")}
        crit += self.agi / per.get(self.cls, d("model", "agi_per_crit_default"))
        crit += d("buffs", "lotp") + d("buffs", "moonkin") - d("model", "crit_suppress")
        if r == "human":
            crit += d("racials", "human_crit")
        self.crit = crit
        self.base_haste = 1 + (d("racials", "skyborne_haste") if r in ("sho", "sws") else 0)
        armor = (d("model", "boss_armor") - d("buffs", "sunder") - d("buffs", "faerie_fire") - d("buffs", "cor"))
        self.armor_mul = armor_multiplier(armor, d("model", "armor_k"))
        self.ap_base = self.melee_ap() if self.melee else 0
        self.gcd_len = d(*self.gcd_len_key)

    def melee_ap(self):
        d = self.d
        ap = d(self.cls, "base_ap") + self.str * d(self.cls, "str_ap") + self.g("ap") + d("buffs", "might")
        if d("buffs", "battle_shout_raidwide") or self.cls == "warrior":
            ap += d("buffs", "battle_shout")
        return ap

    @property
    def ap(self):
        ap = self.ap_base + self.ap_bonus()
        if self.up("blood_fury"):
            ap *= 1 + self.d("racials", "orc_blood_fury")["ap_pct"]
        return ap

    def ap_bonus(self):
        return 0.0

    def crit_chance(self, hand="mh", ability=None):
        c = self.crit + self.crit_bonus(hand, ability)
        if self.up("elune"):
            c += self.d("racials", "nelf_elune")["crit"]
        return c

    def crit_bonus(self, hand, ability):
        return 0.0

    # ---------------------------------------------------------------- auras / cds
    def up(self, name):
        return self.auras.get(name, -1.0) > self.sim.t

    def remains(self, name):
        return max(0.0, self.auras.get(name, -1.0) - self.sim.t)

    def buff(self, name, dur, haste=False):
        self.auras[name] = self.sim.t + dur
        if haste:
            self.rescale()
            self.sim.after(dur, self._expire, name, self.auras[name])

    def _expire(self, name, when):
        if abs(self.auras.get(name, -1) - when) < 1e-9:
            self.rescale()

    def drop(self, name, haste=False):
        self.auras.pop(name, None)
        if haste:
            self.rescale()

    def ready(self, name):
        return self.cds.get(name, 0.0) <= self.sim.t + 1e-9

    def trigger(self, name, cd):
        self.cds[name] = self.sim.t + cd

    def gcd_ready(self):
        return self.sim.t + 1e-9 >= max(self.gcd_until, self.cast_until)

    def start_gcd(self, length=None):
        self.gcd_until = self.sim.t + (self.gcd_len if length is None else length)

    # ---------------------------------------------------------------- haste
    def haste(self, hand="mh", consume=False):
        h = self.base_haste * self.extra_haste(hand)
        if self.up("berserking"):
            h *= 1 + self.d("racials", "troll_berserking")["haste"]
        if hand != "ranged" and self.flurry > 0:
            h *= 1 + self.flurry_haste
            if consume:
                self.flurry -= 1
        return h

    def extra_haste(self, hand):
        return 1.0

    def rescale(self):
        for s in self.swings:
            s.rescale()

    # ---------------------------------------------------------------- damage
    def eureka_up(self):
        return self.race == "gnome" and self.up("eureka")

    def school_mult(self, school, periodic, name):
        m = 1.0
        d = self.d
        if school == "physical":
            if not periodic:
                m *= self.armor_mul
            m *= self.phys_mult(name)
        elif school == "holy":
            m *= self.holy_mult(name)
        else:
            m *= 1 + d("buffs", "coe")
            if school in ("shadow", "arcane"):
                m *= 1 + d("buffs", "cos")
        if not periodic and self.eureka_up() and name not in ("Melee", "Melee (off hand)", "Auto Shot", "Windfury Totem", "Windfury Weapon"):
            m *= 1 + d("racials", "gnome_eureka")["dmg"]
        return m * self.global_mult(name, school)

    def phys_mult(self, name):
        return 1.0

    def holy_mult(self, name):
        return 1.0

    def global_mult(self, name, school):
        return 1.0

    def deal(self, name, amount, school="physical", periodic=False):
        dmg = amount * self.school_mult(school, periodic, name)
        self.sim.dmg[name] += dmg
        self.sim.counts[name] += 1
        return dmg

    def weapon(self, hand):
        return self.g(hand)

    def weapon_dmg(self, hand, normalized=False, extra_ap=0.0):
        lo, hi, speed, wtype, _ = self.weapon(hand)
        if normalized:
            speed = {"2h": self.d("model", "norm_speed_2h"), "dagger": self.d("model", "norm_speed_dagger")}.get(
                wtype, self.d("model", "norm_speed_1h"))
        return self.rng.uniform(lo, hi) + (self.ap + extra_ap) / self.d("model", "ap_per_dps") * speed

    def avg_weapon_dmg(self, hand):
        lo, hi, speed, _, _ = self.weapon(hand)
        return (lo + hi) / 2 + self.ap / self.d("model", "ap_per_dps") * speed

    def miss_chance(self, hand, white):
        d = self.d
        m = d("model", "melee_miss") + (d("model", "dw_penalty") if white and self.dual_wield else 0)
        return max(0.0, m - self.hit - self.hand_hit(hand))

    def hand_hit(self, hand):
        return 0.0

    def dodge_chance(self):
        return self.d("model", "dodge")

    dual_wield = False

    def crit_mult(self, ability):
        return self.d("model", "melee_crit_mul")

    def white_outcome(self, hand):
        r = self.rng.random() * 100
        return roll_white(r, self.miss_chance(hand, True), self.dodge_chance(),
                          self.d("model", "glance_rate"), self.crit_chance(hand, None))

    def yellow_outcome(self, hand, ability, extra_crit=0.0):
        return roll_yellow(self.rng.random() * 100, self.rng.random() * 100, self.miss_chance(hand, False),
                           self.dodge_chance(), self.crit_chance(hand, ability) + extra_crit)

    def spell_outcome(self, school, extra_crit=0.0, crit_base=None):
        d = self.d
        hit = min(d("model", "spell_hit_cap"), d("model", "spell_hit") + self.hit)
        if self.rng.random() * 100 >= hit:
            return MISS
        c = (self.spell_crit() if crit_base is None else crit_base) + extra_crit
        return CRIT if self.rng.random() * 100 < c else HIT

    def spell_crit(self):
        return self.crit_chance()

    def white_amount(self, hand, outcome, base):
        if outcome == GLANCE:
            return base * self.d("model", "glance_dmg")
        if outcome == CRIT:
            return base * self.d("model", "melee_crit_mul")
        return base

    # ---------------------------------------------------------------- on-hit hooks
    def on_landed(self, hand, outcome, name, white):
        """Generic procs after any landed melee hit."""
        if self.race == "undead" and self.sim.t >= self.totg_ready:
            t = self.d("racials", "undead_totg")
            if self.rng.random() < t["chance"]:
                self.totg_ready = self.sim.t + t["icd"]
                self.deal("Touch of the Grave", self.d("model", "player_max_health") * t["pct_hp"], "shadow")

    # ---------------------------------------------------------------- racials
    def use_racials(self):
        d, r = self.d, self.race
        if r == "orc" and self.ready("blood_fury"):
            x = d("racials", "orc_blood_fury")
            self.trigger("blood_fury", x["cd"])
            self.buff("blood_fury", x["dur"])
        elif r == "troll" and self.ready("berserking"):
            x = d("racials", "troll_berserking")
            self.trigger("berserking", x["cd"])
            self.buff("berserking", x["dur"], haste=True)
        elif r == "nelf" and self.ready("elune"):
            x = d("racials", "nelf_elune")
            self.trigger("elune", x["cd"])
            self.buff("elune", x["dur"])
        elif r == "gnome" and self.ready("eureka") and self.eureka_allowed():
            x = d("racials", "gnome_eureka")
            self.trigger("eureka", x["cd"])
            self.buff("eureka", x["dur"])

    def eureka_allowed(self):
        return True

    def cost(self, base):
        if self.eureka_up():
            return base * (1 - self.d("racials", "gnome_eureka")["cost"])
        return base

    # ---------------------------------------------------------------- loop
    def start(self):
        self.setup()
        self.sim.at(0.0, self._heartbeat)

    def setup(self):
        pass

    def _heartbeat(self):
        self.think()
        self.sim.after(0.1, self._heartbeat)

    def think(self):
        pass

    def in_execute(self):
        return self.sim.t >= self.sim.fight * (1 - self.d("model", "execute_phase"))


# ======================================================================= MELEE
class MeleePlayer(Player):
    def setup(self):
        mh = self.weapon("mh")
        self.mh_swing = Swing(self, "mh", mh[2], self.swing)
        self.swings = [self.mh_swing]
        self.mh_swing.start(0.0)
        if self.dual_wield:
            oh = self.weapon("oh")
            self.oh_swing = Swing(self, "oh", oh[2], self.swing)
            self.swings.append(self.oh_swing)
            self.oh_swing.start(0.2)  # small desync, as players do not start both hands together (A)

    def melee_name(self, hand):
        return "Melee" if hand == "mh" else "Melee (off hand)"

    def swing(self, hand):
        if hand == "mh" and self.replace_swing():
            return
        self.white_attack(hand, self.melee_name(hand))

    def replace_swing(self):
        return False

    def white_attack(self, hand, name, extra_ap=0.0, extra=False):
        out = self.white_outcome(hand)
        if out in (MISS, DODGE):
            self.on_avoided(hand, out)
            return out
        base = self.weapon_dmg(hand, extra_ap=extra_ap) * self.hand_mult(hand)
        amt = self.white_amount(hand, out, base)
        dealt = self.deal(name, amt)
        self.on_white_landed(hand, out, dealt, extra)
        self.on_crit_check(out, hand, name)
        self.on_landed(hand, out, name, True)
        self.weapon_procs(hand, extra)
        return out

    def hand_mult(self, hand):
        return 1.0

    def on_avoided(self, hand, outcome):
        pass

    def on_white_landed(self, hand, outcome, dealt, extra):
        pass

    def on_crit_check(self, outcome, hand, name):
        if outcome == CRIT:
            self.on_crit(hand, name)

    def on_crit(self, hand, name):
        pass

    def weapon_procs(self, hand, extra):
        """Windfury Totem by default (main hand, not from extra attacks)."""
        if hand == "mh" and not extra and self.uses_wf_totem():
            d = self.d
            if self.rng.random() < d("buffs", "wf_totem_chance"):
                for _ in range(d("buffs", "wf_totem_attacks")):
                    self.white_attack("mh", "Windfury Totem", extra_ap=d("buffs", "wf_totem_ap"), extra=True)

    def uses_wf_totem(self):
        return True

    def special(self, name, base, hand="mh", school="physical", extra_crit=0.0, mult=1.0):
        out = self.yellow_outcome(hand, name, extra_crit)
        if out in (MISS, DODGE):
            self.on_avoided(hand, out)
            return out, 0.0
        amt = base * mult
        if out == CRIT:
            amt *= self.crit_mult(name)
        dealt = self.deal(name, amt, school)
        self.on_crit_check(out, hand, name)
        self.on_landed(hand, out, name, False)
        self.weapon_procs(hand, False)
        return out, dealt


# ---------------------------------------------------------------- Warrior
class Warrior(MeleePlayer):
    cls = "warrior"

    def __init__(self, sim, d, race):
        self.rage = 0.0
        super().__init__(sim, d, race)
        self.flurry_haste = 0.0
        self.deep = Dot(self, "Deep Wounds", "physical")

    def crit_mult(self, ability):
        return self.d("model", "melee_crit_mul") + self.impale

    impale = 0.0

    def gain(self, r):
        self.rage = min(self.d("rage", "max"), self.rage + r)

    def spend(self, r):
        self.rage -= r

    def on_white_landed(self, hand, outcome, dealt, extra):
        speed = self.weapon(hand)[2]
        r = rage_from_damage(self.d, dealt, speed, hand == "oh", outcome == CRIT)
        if hand == "oh" and self.dual_wield:
            r *= 1 + self.d("warrior", "dw_spec")["rage"]
        if self.up("reckless_swings") and self.stacks.get("reckless_swings", 0) > 0:
            r += self.d("warrior", "reckless_swings")["rage"]
            self.stacks["reckless_swings"] -= 1
        self.gain(r)

    def on_landed(self, hand, outcome, name, white):
        super().on_landed(hand, outcome, name, white)
        if self.rng.random() < self.d("warrior", "unbridled_wrath"):
            self.gain(1)

    def on_crit(self, hand, name):
        f = self.d("warrior", "flurry")
        if self.has_flurry:
            if self.flurry == 0:
                self.flurry = f["charges"]
                self.rescale()
            self.flurry = f["charges"]
        dw = self.d("warrior", "deep_wounds")
        total = dw["pct"] * self.avg_weapon_dmg("mh")
        self.deep.apply(total / dw["ticks"], dw["ticks"], dw["dur"] / dw["ticks"])

    has_flurry = False

    def phys_mult(self, name):
        m = 1.0
        if self.up("death_wish"):
            m *= 1 + self.d("warrior", "death_wish")["dmg"]
        return m

    def crit_bonus(self, hand, ability):
        c = self.d("warrior", "cruelty")
        if self.up("recklessness"):
            c += self.d("warrior", "recklessness")["crit"]
        return c

    def setup(self):
        super().setup()
        am = self.d("warrior", "anger_management")
        self.sim.after(am["every"], self._am)

    def _am(self):
        self.gain(self.d("warrior", "anger_management")["rage"])
        self.sim.after(self.d("warrior", "anger_management")["every"], self._am)

    def offgcd(self):
        d = self.d
        self.use_racials()
        br = d("warrior", "bloodrage")
        if self.ready("bloodrage") and self.rage <= 100 - br["now"] - 20:
            self.trigger("bloodrage", br["cd"])
            self.gain(br["now"])
            for i in range(1, br["dur"] + 1):
                self.sim.after(i, self.gain, br["over"] / br["dur"])
        if self.ready("death_wish") and self.rage >= d("warrior", "death_wish")["rage"]:
            x = d("warrior", "death_wish")
            self.trigger("death_wish", x["cd"])
            self.spend(x["rage"])
            self.buff("death_wish", x["dur"])
        if self.ready("recklessness"):
            x = d("warrior", "recklessness")
            self.trigger("recklessness", x["cd"])
            self.buff("recklessness", x["dur"])

    def heroic_strike_ok(self, threshold):
        return self.rage >= max(threshold, self.hs_cost())

    def hs_cost(self):
        d = self.d
        return self.cost(d("warrior", "heroic_strike")["rage"] - d("warrior", "imp_heroic_strike"))

    def heroic_strike(self):
        d = self.d
        self.spend(self.hs_cost())
        base = self.weapon_dmg("mh") + d("warrior", "heroic_strike")["flat"]
        self.special("Heroic Strike", base * self.hand_mult("mh"))

    def execute(self):
        d = self.d
        x = d("warrior", "execute")
        cost = self.cost(x["rage"] - d("warrior", "imp_execute"))
        extra = max(0.0, self.rage - cost)
        self.rage = 0.0  # a missed Execute still spends its rage (A)
        self.special("Execute", x["flat"] + x["per_rage"] * extra)
        self.start_gcd()


class Fury(Warrior):
    build = "17/34/0"
    spec = "Fury"
    gear_key = "fury"
    dual_wield = True
    has_flurry = True

    def __init__(self, sim, d, race):
        super().__init__(sim, d, race)
        self.flurry_haste = d("warrior", "flurry")["haste"]
        self.impale = d("warrior", "impale")  # Fury build takes Impale 2/2 in Arms

    def crit_bonus(self, hand, ability):
        return super().crit_bonus(hand, ability) + self.d("warrior", "berserker_stance_crit")

    def hand_hit(self, hand):
        return self.d("warrior", "furious_precision") if hand == "oh" else 0.0

    def hand_mult(self, hand):
        return 0.5 * (1 + self.d("warrior", "dw_spec")["dmg"]) if hand == "oh" else 1.0

    def replace_swing(self):
        if not self.in_execute() and self.heroic_strike_ok(50):
            self.heroic_strike()
            return True
        return False

    def think(self):
        d = self.d
        self.offgcd()
        if self.ready("berserker_rage") and self.rage <= 80:
            self.trigger("berserker_rage", d("warrior", "berserker_rage")["cd"])
            self.gain(d("warrior", "imp_berserker_rage"))
        if not self.gcd_ready():
            return
        bt, ww = d("warrior", "bloodthirst"), d("warrior", "whirlwind")
        if self.in_execute():
            if self.ready("bloodthirst") and self.rage >= self.cost(bt["rage"]) and self.rage < 40:
                return self._bt()
            if self.rage >= self.cost(d("warrior", "execute")["rage"] - d("warrior", "imp_execute")):
                return self.execute()
            return
        if self.ready("reckless_swings"):
            x = d("warrior", "reckless_swings")
            self.trigger("reckless_swings", x["cd"])
            self.buff("reckless_swings", x["dur"])
            self.stacks["reckless_swings"] = x["swings"]
            return self.start_gcd()
        if self.ready("bloodthirst") and self.rage >= self.cost(bt["rage"]):
            return self._bt()
        if self.ready("whirlwind") and self.rage >= self.cost(ww["rage"]) and self.cds.get("bloodthirst", 0) - self.sim.t > 1.0:
            iw = d("warrior", "imp_whirlwind")
            self.trigger("whirlwind", ww["cd"] - iw["cd"])
            self.spend(self.cost(ww["rage"]))
            self.special("Whirlwind", self.weapon_dmg("mh", normalized=True), mult=1 + iw["dmg"])
            return self.start_gcd()

    def _bt(self):
        bt = self.d("warrior", "bloodthirst")
        self.trigger("bloodthirst", bt["cd"])
        self.spend(self.cost(bt["rage"]))
        self.special("Bloodthirst", bt["ap"] * self.ap + bt["flat"])
        self.start_gcd()


class Arms(Warrior):
    build = "33/18/0"
    spec = "Arms"
    gear_key = "arms"

    def __init__(self, sim, d, race):
        super().__init__(sim, d, race)
        self.impale = d("warrior", "impale")
        self.rend = Dot(self, "Rend", "physical")
        self.op_until = -1.0

    def crit_bonus(self, hand, ability):
        c = super().crit_bonus(hand, ability) + self.d("warrior", "weaponmaster_axe_crit")
        if ability == "Overpower":
            c += self.d("warrior", "imp_overpower")
        return c

    def phys_mult(self, name):
        return super().phys_mult(name) * (1 + self.d("warrior", "two_hand_spec"))

    def on_avoided(self, hand, outcome):
        if outcome == DODGE:
            self.op_until = self.sim.t + self.d("warrior", "overpower")["window"]

    def on_white_landed(self, hand, outcome, dealt, extra):
        super().on_white_landed(hand, outcome, dealt, extra)
        if hand == "mh" and self.rend.up and self.rng.random() < self.d("warrior", "bloodthrill"):
            self.op_until = self.sim.t + self.d("warrior", "overpower")["window"]

    def replace_swing(self):
        if not self.in_execute() and self.heroic_strike_ok(60):
            self.heroic_strike()
            return True
        return False

    def think(self):
        d = self.d
        self.offgcd()
        if not self.gcd_ready():
            return
        ms, sl, op, rd = d("warrior", "mortal_strike"), d("warrior", "slam"), d("warrior", "overpower"), d("warrior", "rend")
        if self.ready("mortal_strike") and self.rage >= self.cost(ms["rage"]):
            self.trigger("mortal_strike", ms["cd"])
            self.spend(self.cost(ms["rage"]))
            self.special("Mortal Strike", self.weapon_dmg("mh", normalized=True) + ms["flat"])
            return self.start_gcd()
        if self.in_execute():
            if self.rage >= self.cost(d("warrior", "execute")["rage"] - d("warrior", "imp_execute")):
                return self.execute()
            return
        if not self.rend.up and self.rage >= self.cost(rd["rage"]):
            self.spend(self.cost(rd["rage"]))
            out, _ = self.special_apply("Rend")
            if out not in (MISS, DODGE):
                tick = rd["dmg"] * (1 + d("warrior", "imp_rend")) / rd["ticks"]
                self.rend.apply(tick, rd["ticks"], rd["dur"] / rd["ticks"])
            return self.start_gcd()
        if self.sim.t < self.op_until and self.ready("overpower") and self.rage >= self.cost(op["rage"]):
            self.trigger("overpower", op["cd"])
            self.op_until = -1
            self.spend(self.cost(op["rage"]))
            self.special("Overpower", self.weapon_dmg("mh", normalized=True) + op["flat"])
            return self.start_gcd()
        if self.ready("slam") and self.rage >= self.cost(sl["rage"]):
            isl = d("warrior", "imp_slam")
            self.trigger("slam", sl["cd"] - isl["cd"])
            self.spend(self.cost(sl["rage"]))
            cast = sl["cast"] - isl["cast"]
            self.cast_until = self.sim.t + cast
            self.start_gcd(self.gcd_len - isl["cast"])
            self.sim.after(cast, self._slam_land)

    def _slam_land(self):
        self.special("Slam", self.weapon_dmg("mh") + self.d("warrior", "slam")["flat"])

    def special_apply(self, name):
        out = self.yellow_outcome("mh", name)
        return out, 0.0


# ---------------------------------------------------------------- Rogue
class Rogue(MeleePlayer):
    cls = "rogue"
    gcd_len_key = ("model", "gcd_energy")
    dual_wield = True

    def __init__(self, sim, d, race):
        super().__init__(sim, d, race)
        self.max_energy = (d("energy", "max") + d("rogue", "vigor")) * (1 + (d("racials", "gnome_energy") if race == "gnome" else 0))
        self.energy = self.max_energy
        self.cp = 0
        self.deadly = Dot(self, "Deadly Poison", "nature")

    def melee_ap(self):
        return super().melee_ap() + self.agi * self.d("rogue", "agi_ap")

    def crit_mult(self, ability):
        m = self.d("model", "melee_crit_mul")
        if ability in ("Sinister Strike", "Mutilate", "Mutilate (off hand)"):
            m += self.d("rogue", "lethality")
        return m

    def crit_bonus(self, hand, ability):
        c = self.d("rogue", "malice")
        if self.weapon(hand)[4] == "dagger":
            c += self.dagger_crit()
        if ability and self.up("cold_blood") and ability in ("Sinister Strike", "Eviscerate", "Mutilate", "Mutilate (off hand)"):
            c += 100
        return c

    def dagger_crit(self):
        return 0.0

    def hand_hit(self, hand):
        return self.d("rogue", "precision")

    def dodge_chance(self):
        return max(0.0, self.d("model", "dodge") - self.d("rogue", "weapon_expertise"))

    def hand_mult(self, hand):
        return 0.5 * (1 + self.d("rogue", "dw_spec")) if hand == "oh" else 1.0

    def extra_haste(self, hand):
        h = 1.0
        if self.up("snd"):
            h *= 1 + self.d("rogue", "slice_and_dice")["haste"]
        if self.up("blade_flurry"):
            h *= 1 + self.d("rogue", "blade_flurry")["haste"]
        return h

    def setup(self):
        super().setup()
        self.sim.after(self.rng.random() * self.d("energy", "tick_interval"), self._energy_tick)

    def _energy_tick(self):
        e = self.d("energy", "tick") * (2 if self.up("adrenaline_rush") else 1)
        self.energy = min(self.max_energy, self.energy + e)
        self.sim.after(self.d("energy", "tick_interval"), self._energy_tick)

    def gain_energy(self, e):
        self.energy = min(self.max_energy, self.energy + e)

    def poison_chance_bonus(self):
        return 0.0

    def poison_mult(self):
        return 1.0

    def weapon_procs(self, hand, extra):
        super().weapon_procs(hand, extra)
        d = self.d
        if hand == "mh":
            ip = d("rogue", "instant_poison")
            if self.rng.random() < ip["chance"] + self.poison_chance_bonus():
                out = self.spell_outcome("nature")
                if out != MISS:
                    amt = (self.rng.uniform(ip["min"], ip["max"]) + ip["ap"] * self.ap) * self.poison_mult()
                    if out == CRIT:
                        amt *= d("rogue", "poison_crit_mul")
                    self.deal("Instant Poison", amt, "nature")
            hs = self.sword_extra()
            if hs and not extra and self.rng.random() < hs:
                self.white_attack("mh", "Hack and Slash", extra=True)
        else:
            dp = d("rogue", "deadly_poison")
            if self.rng.random() < dp["chance"] + self.poison_chance_bonus():
                if self.spell_outcome("nature", crit_base=-1) != MISS:
                    self.deadly.stacks = min(dp["stacks"], self.deadly.stacks + 1)
                    tick = (dp["dmg"] / dp["ticks"] + dp["ap"] * self.ap) * self.deadly.stacks * self.poison_mult()
                    self.deadly.apply(tick, dp["ticks"], dp["dur"] / dp["ticks"])

    def sword_extra(self):
        return 0.0

    def eviscerate(self):
        d = self.d
        cost = self.cost(d("rogue", "eviscerate_energy") - d("rogue", "flawless_execution") * self.flawless)
        if self.energy < cost:
            return False
        if self.ready("cold_blood") and self.cold_blood_talent:
            self.trigger("cold_blood", d("rogue", "cold_blood")["cd"])
            self.buff("cold_blood", 30)
        self.energy -= cost
        base = d("rogue", "eviscerate_cp")[self.cp] * self.rng.uniform(0.95, 1.05)
        mult = (1 + d("rogue", "coup_de_grace") * self.cdg) * (1 + d("rogue", "aggression") * self.aggr)
        out, _ = self.special("Eviscerate", base, mult=mult)
        self.drop("cold_blood")
        if out not in (MISS, DODGE):
            self.finisher_done()
        self.start_gcd()
        return True

    flawless = 0
    cdg = 1
    aggr = 0
    cold_blood_talent = True

    def slice_and_dice(self):
        d = self.d
        x = d("rogue", "slice_and_dice")
        cost = self.cost(x["energy"])
        if self.energy < cost:
            return False
        self.energy -= cost
        dur = (x["base"] + x["per_cp"] * self.cp) * (1 + d("rogue", "imp_snd"))
        self.buff("snd", dur, haste=True)
        self.finisher_done()
        self.start_gcd()
        return True

    def finisher_done(self):
        d = self.d
        cps = self.cp
        self.cp = 1 if self.rng.random() < d("rogue", "ruthlessness") else 0
        if self.relentless:
            rs = d("rogue", "relentless_strikes")
            if self.rng.random() < rs["per_cp"] * cps:
                self.gain_energy(rs["energy"])

    relentless = False

    def add_cp(self, n):
        self.cp = int(min(5, self.cp + n))

    def shank(self, gain):
        d = self.d
        x = d("rogue", "shank")
        cost = self.cost(x["energy"])
        if self.energy < cost:
            return False
        self.energy -= cost
        dmg = self.weapon_dmg("mh") * x["weapon"]
        crit = self.rng.random() * 100 < self.crit_chance("mh", "Shank")
        if crit:
            dmg *= self.crit_mult("Shank")
        self.deal("Shank", dmg)
        out = CRIT if crit else HIT
        self.on_landed("mh", out, "Shank", False)
        self.weapon_procs("mh", False)  # whether Shank applies poisons is unpublished (A: yes)
        self.gain_energy(gain)
        self.add_cp(d("rogue", "shank_cp"))
        self.start_gcd()
        return True

    def offgcd(self):
        self.use_racials()

    def eureka_allowed(self):
        return self.energy < 60


class Combat(Rogue):
    build = "16/35/0"
    spec = "Combat"
    gear_key = "combat"
    flawless = 1
    aggr = 1

    def dagger_crit(self):
        return self.d("rogue", "hack_and_slash")["dagger_crit"]

    def sword_extra(self):
        return self.d("rogue", "hack_and_slash")["sword_extra"]

    def think(self):
        d = self.d
        self.offgcd()
        bf = d("rogue", "blade_flurry")
        if self.ready("blade_flurry") and self.energy >= self.cost(bf["energy"]):
            self.trigger("blade_flurry", bf["cd"])
            self.energy -= self.cost(bf["energy"])
            self.buff("blade_flurry", bf["dur"], haste=True)
        if self.ready("adrenaline_rush") and self.energy < 50:
            ar = d("rogue", "adrenaline_rush")
            self.trigger("adrenaline_rush", ar["cd"])
            self.buff("adrenaline_rush", ar["dur"])
        if not self.gcd_ready():
            return
        if self.cp >= 1 and self.remains("snd") < 1.0:
            if self.slice_and_dice():
                return
            return
        if self.cp >= 5:
            if self.remains("snd") < 4 and self.slice_and_dice():
                return
            self.eviscerate()
            return
        x, fos = d("rogue", "shank"), d("rogue", "flash_of_steel")
        gain = x["gain"] + fos["gain"]
        if self.ready("shank") and self.energy <= self.max_energy - gain + 5:
            self.trigger("shank", x["cd"] - fos["cd"])
            if self.shank(gain):
                return
        ss = d("rogue", "sinister_strike")
        cost = self.cost(ss["energy"] - d("rogue", "efficient_strikes"))
        if self.energy >= cost:
            self.energy -= cost
            out, _ = self.special("Sinister Strike", self.weapon_dmg("mh", normalized=True) + ss["flat"],
                                  mult=1 + d("rogue", "aggression"))
            self.drop("cold_blood")
            if out not in (MISS, DODGE):
                self.add_cp(1)
            self.start_gcd()


class Mutilate(Rogue):
    build = "35/11/5"
    spec = "Mutilate"
    gear_key = "mutilate"
    relentless = True

    def poison_chance_bonus(self):
        b = self.d("rogue", "imp_poisons")
        if self.up("venom"):
            b += self.d("rogue", "venom")["chance"]
        return b

    def poison_mult(self):
        m = 1 + self.d("rogue", "vile_poisons")
        if self.up("venom"):
            m *= 1 + self.d("rogue", "venom")["dmg"]
        return m

    def crit_bonus(self, hand, ability):
        c = super().crit_bonus(hand, ability)
        if ability in ("Mutilate", "Mutilate (off hand)"):
            c += self.d("rogue", "puncturing_wounds_mut")
        return c

    def think(self):
        d = self.d
        self.offgcd()
        if not self.gcd_ready():
            return
        if self.cp >= 1 and self.remains("snd") < 1.0:
            self.slice_and_dice()
            return
        if self.cp >= 4:
            if self.remains("snd") < 4 and self.slice_and_dice():
                return
            self.eviscerate()
            return
        x = d("rogue", "shank")
        if self.ready("shank") and self.energy <= self.max_energy - x["gain"] + 5:
            self.trigger("shank", x["cd"])
            if self.shank(x["gain"]):
                self.buff("venom", d("rogue", "venom")["dur"])
                return
        m = d("rogue", "mutilate")
        cost = self.cost(m["energy"])
        if self.energy >= cost:
            self.energy -= cost
            mult = (1 + m["poisoned"] * (1 if self.deadly.up else 0)) * (1 + d("rogue", "opportunity"))
            # one avoidance roll for both hands, separate crit rolls (A)
            r = self.rng.random() * 100
            if r < self.miss_chance("mh", False) + self.dodge_chance():
                self.start_gcd()
                return
            crits = 0
            for hand, name in (("mh", "Mutilate"), ("oh", "Mutilate (off hand)")):
                dmg = (self.weapon_dmg(hand) * m["weapon"] + m["flat"]) * mult
                crit = self.rng.random() * 100 < self.crit_chance(hand, name)
                if crit:
                    dmg *= self.crit_mult(name)
                    crits += 1
                self.deal(name, dmg)
                self.on_landed(hand, CRIT if crit else HIT, name, False)
                self.weapon_procs(hand, False)
            self.drop("cold_blood")
            self.add_cp(m["cp"] + (d("rogue", "seal_fate") if crits else 0))
            self.start_gcd()


# ---------------------------------------------------------------- Paladin
class ManaMixin:
    def setup_mana(self, regen_casting=0.0):
        d = self.d
        self.max_mana = self.g("base_mana") + self.int * d("mana", "int_to_mana")
        self.mana = self.max_mana
        self.sim.after(self.rng.random() * 2.0, self._mana_tick)

    def regen_while_casting(self):
        return 0.0

    def _mana_tick(self):
        d = self.d
        spirit = (self.g("spirit") + d("buffs", "motw")) * (1 + d("buffs", "kings"))
        sp_regen = d("mana", "spirit_regen_base") + spirit / d("mana", "spirit_regen_div")
        if self.sim.t - self.last_mana_spend < d("mana", "five_second_rule"):
            sp_regen *= self.regen_while_casting()
        self.mana = min(self.max_mana, self.mana + sp_regen + d("mana", "bow_mp5") * 2 / 5)
        self.sim.after(2.0, self._mana_tick)

    def spend_mana(self, m):
        if self.mana < m:
            return False
        self.mana -= m
        self.last_mana_spend = self.sim.t
        return True


class Retribution(ManaMixin, MeleePlayer):
    build = "12/8/31"
    cls = "paladin"
    spec = "Retribution"
    gear_key = "ret"

    def setup(self):
        super().setup()
        self.setup_mana()
        self.seal_up = True  # sealed before the pull
        self.vengeance = 0
        self.sp = self.g("sp") + self.int * self.d("paladin", "champion_of_the_light")["int_sp"]

    def crit_bonus(self, hand, ability):
        return self.d("paladin", "conviction")

    def spell_crit(self):
        d = self.d
        c = self.g("crit") + self.int / d("paladin", "int_per_spell_crit") + d("buffs", "lotp") + d("buffs", "moonkin")
        c += d("paladin", "conviction") - d("model", "crit_suppress")
        if self.race == "human":
            c += d("racials", "human_crit")
        if self.up("elune"):
            c += d("racials", "nelf_elune")["crit"]
        return c

    def _veng(self):
        v = self.d("paladin", "vengeance")
        return 1 + v["per_stack"] * self.vengeance if self.up("vengeance") else 1.0

    def phys_mult(self, name):
        return (1 + self.d("paladin", "two_hand_spec")) * self._veng()

    def holy_mult(self, name):
        return (1 + self.d("paladin", "two_hand_spec")) * self._veng()

    def on_crit(self, hand, name):
        v = self.d("paladin", "vengeance")
        self.vengeance = min(v["stacks"], (self.vengeance if self.up("vengeance") else 0) + 1)
        self.buff("vengeance", v["dur"])

    def weapon_procs(self, hand, extra):
        if self.seal_up:
            s = self.d("paladin", "seal_of_command")
            if self.rng.random() < ppm_chance(s["ppm"], self.weapon("mh")[2]):
                base = (self.weapon_dmg("mh") * s["weapon"] + s["sp"] * self.sp) * (1 + self.d("paladin", "imp_seals"))
                out = self.yellow_outcome("mh", "Seal of Command")
                if out not in (MISS, DODGE):
                    if out == CRIT:
                        base *= self.d("model", "melee_crit_mul")
                        self.on_crit(hand, "Seal of Command")
                    self.deal("Seal of Command", base, "holy")
        super().weapon_procs(hand, extra)

    def think(self):
        d = self.d
        self.use_racials()
        if self.seal_up and self.ready("judgement"):
            j = d("paladin", "judgement_command")
            if self.spend_mana(j["mana"]):
                self.trigger("judgement", d("paladin", "judgement_cd") - d("paladin", "imp_judgement"))
                self.seal_up = False
                out = self.spell_outcome("holy")
                if out != MISS:
                    amt = (j["dmg"] + j["sp"] * self.sp) * (1 + d("paladin", "imp_seals"))
                    if out == CRIT:
                        amt *= d("model", "spell_crit_mul")
                        self.on_crit("mh", "Judgement of Command")
                    self.deal("Judgement of Command", amt, "holy")
                self.mana += d("paladin", "seal_of_command")["mana"] * d("paladin", "sanctified_judgement")
        if not self.gcd_ready():
            return
        how = d("paladin", "hammer_of_wrath")
        if self.in_execute() and self.ready("how") and self.mana >= how["mana"]:
            cast = max(0.0, how["cast"] - d("paladin", "champion_of_the_light")["how_cast"])
            self.spend_mana(self.cost(how["mana"] * (1 - d("paladin", "benediction"))))
            self.trigger("how", how["cd"])
            out = self.spell_outcome("holy")
            if out != MISS:
                amt = how["dmg"] + how["sp"] * self.sp
                if out == CRIT:
                    amt *= d("model", "spell_crit_mul")
                    self.on_crit("mh", "Hammer of Wrath")
                self.deal("Hammer of Wrath", amt, "holy")
            self.cast_until = self.sim.t + cast
            return self.start_gcd()
        if not self.seal_up:
            s = d("paladin", "seal_of_command")
            if self.spend_mana(s["mana"] * (1 - d("paladin", "benediction"))):
                self.seal_up = True
                self.start_gcd()


# ---------------------------------------------------------------- Shaman
class Enhancement(ManaMixin, MeleePlayer):
    build = "8/35/8"
    cls = "shaman"
    spec = "Enhancement"
    gear_key = "enh"

    def __init__(self, sim, d, race):
        super().__init__(sim, d, race)
        self.flurry_haste = d("shaman", "flurry")["haste"]

    def melee_ap(self):
        return super().melee_ap() + self.agi * self.d("shaman", "agi_ap") + self.int * self.d("shaman", "mental_dexterity")

    def setup(self):
        super().setup()
        self.setup_mana()
        self.sp = self.g("sp")

    def regen_while_casting(self):
        return self.d("shaman", "improved_stormstrike") if self.up("imp_ss") else 0.0

    def uses_wf_totem(self):
        return False  # own Windfury Weapon; the raid totem does not stack (one WF per weapon, A)

    def crit_bonus(self, hand, ability):
        c = self.d("shaman", "thundering_strikes")
        if self.up("ele_dev"):
            c += self.d("shaman", "elemental_devastation")["crit"]
        return c

    def extra_haste(self, hand):
        return 1 + self.d("shaman", "rage_of_the_farseer")["haste"] if self.up("farseer") else 1.0

    def spell_crit(self):
        d = self.d
        c = d("shaman", "base_spell_crit") + self.int / d("shaman", "int_per_spell_crit") + self.g("crit")
        c += d("buffs", "lotp") + d("buffs", "moonkin") - d("model", "crit_suppress")
        if self.up("elune"):
            c += d("racials", "nelf_elune")["crit"]
        return c

    def on_crit(self, hand, name):
        f = self.d("shaman", "flurry")
        if self.flurry == 0:
            self.flurry = f["charges"]
            self.rescale()
        self.flurry = f["charges"]

    def weapon_procs(self, hand, extra):
        if extra:
            return
        w = self.d("shaman", "windfury_weapon")
        if self.rng.random() < w["chance"]:
            ap = w["ap"] * (1 + self.d("shaman", "elemental_weapons"))
            for _ in range(w["attacks"]):
                self.white_attack("mh", "Windfury Weapon", extra_ap=ap, extra=True)

    def think(self):
        d = self.d
        self.use_racials()
        rf = d("shaman", "rage_of_the_farseer")
        if self.ready("farseer"):
            self.trigger("farseer", rf["cd"])
            self.buff("farseer", rf["dur"], haste=True)
        if not self.gcd_ready():
            return
        ss = d("shaman", "stormstrike")
        if self.ready("stormstrike") and self.spend_mana(self.cost(self.g("base_mana") * ss["mana_pct"])):
            self.trigger("stormstrike", ss["cd"])
            out, _ = self.special("Stormstrike", self.weapon_dmg("mh") * ss["weapon"])
            if out not in (MISS, DODGE):
                self.buff("ss_debuff", ss["dur"])
            self.buff("imp_ss", 15)
            return self.start_gcd()
        es = d("shaman", "earth_shock")
        cost = self.cost(es["mana"] * (1 - d("shaman", "convection")))
        if self.ready("shock") and self.up("ss_debuff") and self.mana >= cost + 0.15 * self.max_mana:
            self.spend_mana(cost)
            self.trigger("shock", es["cd"])
            out = self.spell_outcome("nature")
            if out != MISS:
                amt = (es["dmg"] + es["sp"] * self.sp) * (1 + ss["bonus"])
                if out == CRIT:
                    amt *= d("model", "spell_crit_mul")
                    ed = d("shaman", "elemental_devastation")
                    self.buff("ele_dev", ed["dur"])
                self.deal("Earth Shock", amt, "nature")
            self.drop("ss_debuff")
            return self.start_gcd()


# ---------------------------------------------------------------- Druid
class FeralCat(ManaMixin, MeleePlayer):
    build = "9/32/10"
    cls = "druid"
    spec = "Feral (Cat)"
    gear_key = "feral"
    gcd_len_key = ("model", "gcd_energy")

    def __init__(self, sim, d, race):
        super().__init__(sim, d, race)
        self.energy = d("energy", "max")
        self.cp = 0

    def melee_ap(self):
        d = self.d
        return (super().melee_ap() + self.agi * d("druid", "cat_agi_ap") + d("druid", "cat_flat_ap")
                + d("druid", "predatory_strikes"))

    def weapon(self, hand):
        dps = self.g("cat_weapon_dps")
        s = self.g("cat_speed")
        return [dps * s * 0.8, dps * s * 1.2, s, "cat", "cat"]  # +/-20% spread (A)

    def setup(self):
        super().setup()
        self.setup_mana()
        self.sim.after(self.rng.random() * self.d("energy", "tick_interval"), self._energy_tick)

    def _energy_tick(self):
        self.energy = min(self.d("energy", "max"), self.energy + self.d("energy", "tick"))
        self.sim.after(self.d("energy", "tick_interval"), self._energy_tick)

    def crit_bonus(self, hand, ability):
        return self.d("druid", "sharpened_claws")

    def phys_mult(self, name):
        if name not in ("Melee", "Windfury Totem") and self.d("buffs", "target_bleeding"):
            return 1 + self.d("druid", "rend_and_tear")
        return 1.0

    def think(self):
        d = self.d
        self.use_racials()
        sp = d("druid", "shifting_power")
        cost = self.g("base_mana") * sp["mana_pct"]
        if self.energy < 30 and self.ready("shifting_power") and self.mana >= cost:
            self.spend_mana(cost)
            self.trigger("shifting_power", sp["cd"])
            self.energy = min(d("energy", "max"), self.energy + sp["energy"])
        if not self.gcd_ready():
            return
        if self.cp >= 5:
            fb = d("druid", "ferocious_bite")
            c = self.cost(fb["energy"])
            if self.energy >= c:
                extra = self.energy - c
                self.energy -= c
                base = (fb["base_5cp"] * self.rng.uniform(0.9, 1.1) + fb["ap_5cp"] * self.ap) * (1 + fb["forever"])
                base += fb["per_energy"] * extra * (1 + fb["forever"])
                out, _ = self.special("Ferocious Bite", base)
                if out not in (MISS, DODGE):
                    self.cp = 0
                self.start_gcd()
            return
        sh = d("druid", "shred")
        c = self.cost(sh["energy"] - d("druid", "shredding_attacks"))
        if self.energy >= c:
            self.energy -= c
            avg = self.weapon_dmg("mh")
            out, _ = self.special("Shred", avg * sh["weapon"] + sh["flat"], mult=1 + d("druid", "savage_fury"))
            if out not in (MISS, DODGE):
                self.cp = int(min(5, self.cp + 1 + (d("druid", "blood_frenzy") if out == CRIT else 0)))
            self.start_gcd()


# ---------------------------------------------------------------- Hunter
class Marksmanship(ManaMixin, Player):
    build = "5/46/0"
    cls = "hunter"
    spec = "Marksmanship"
    gear_key = "hunter"
    melee = False
    pet = True

    def setup(self):
        d = self.d
        self.setup_mana()

        self.rap = (d("hunter", "base_rap") + self.agi * d("hunter", "agi_rap") + self.g("rap") + d("buffs", "trueshot")
                    + d("hunter", "hawk") + self.int * d("hunter", "careful_aim"))
        self.auto = Swing(self, "ranged", self.g("ranged")[2], self.auto_shot)
        self.swings = [self.auto]
        self.auto.start(0.0)
        self.serpent = Dot(self, "Serpent Sting", "nature")
        if self.pet:
            p = d("hunter", "pet")
            self.pet_swing = Swing(self, "pet", p["speed"], self.pet_attack)
            self.swings.append(self.pet_swing)
            self.pet_swing.start(0.5)
            self.sim.after(1.0, self._pet_special)

    @property
    def ap(self):
        r = self.rap
        if self.up("blood_fury"):
            r *= 1 + self.d("racials", "orc_blood_fury")["ap_pct"]
        return r

    def regen_while_casting(self):
        return self.d("hunter", "rapid_recuperation") if self.serpent.up else 0.0

    def crit_bonus(self, hand, ability):
        return self.d("hunter", "lethal_attacks")

    def crit_mult(self, ability):
        return self.d("model", "melee_crit_mul") + self.d("hunter", "mortal_shots")

    def haste(self, hand="mh", consume=False):
        if hand == "pet":
            return 1.0
        h = super().haste(hand, consume) * (1 + self.g("quiver_haste"))
        if self.up("rapid_fire"):
            h *= 1 + self.d("hunter", "rapid_fire")["haste"]
        if self.up("deadly_aspects"):
            h *= 1 + self.d("hunter", "deadly_aspects")["haste"]
        return h

    def global_mult(self, name, school):
        if name.startswith("Pet"):
            m = 1 + (self.d("racials", "orc_command") if self.race == "orc" else 0)
            return m
        m = 1 + self.d("hunter", "ranged_spec") if school == "physical" else 1.0
        if not self.pet:
            m *= 1 + self.d("hunter", "lone_wolf")
        return m

    def miss_chance(self, hand, white):
        return max(0.0, self.d("model", "melee_miss") - self.hit)

    def shot_base(self):
        lo, hi, speed, _, _ = self.g("ranged")
        return self.rng.uniform(lo, hi) + self.g("ammo_dps") * speed + self.ap / self.d("model", "ap_per_dps") * speed

    def shot(self, name, base, school="physical", mult=1.0):
        out = self.yellow_outcome("ranged", name)
        if out in (MISS, DODGE):
            return out
        amt = base * mult
        if out == CRIT:
            amt *= self.crit_mult(name)
        self.deal(name, amt, school)
        self.on_landed("ranged", out, name, False)
        return out

    def auto_shot(self, hand):
        if self.sim.t < self.cast_until - 1e-9:
            # the shot waits for the cast to finish, then fires (A)
            self.sim.at(self.cast_until, self.auto_shot, hand)
            return
        self.shot("Auto Shot", self.shot_base())
        da = self.d("hunter", "deadly_aspects")
        if self.rng.random() < da["chance"]:
            self.buff("deadly_aspects", da["dur"], haste=True)

    def pet_attack(self, hand):
        p = self.d("hunter", "pet")
        self.d("buffs", "pets_get_buffs")  # Forever: no player buffs on pets, so only the pet's own crit
        crit = p["crit"] - self.d("model", "crit_suppress")
        out = roll_white(self.rng.random() * 100, self.d("model", "melee_miss"), self.d("model", "dodge"),
                         self.d("model", "glance_rate"), crit)
        if out in (MISS, DODGE):
            return
        amt = self.white_amount("pet", out, self.rng.uniform(p["min"], p["max"]))
        self.deal("Pet melee", amt, "pet")

    def _pet_special(self):
        p = self.d("hunter", "pet")
        out = roll_yellow(self.rng.random() * 100, self.rng.random() * 100, self.d("model", "melee_miss"),
                          self.d("model", "dodge"), p["crit"] - self.d("model", "crit_suppress"))
        if out not in (MISS, DODGE):
            amt = p["special"] * (self.d("model", "melee_crit_mul") if out == CRIT else 1)
            self.deal("Pet special", amt, "pet")
        self.sim.after(p["special_every"], self._pet_special)

    def school_mult(self, school, periodic, name):
        if school == "pet":
            return self.armor_mul * self.global_mult(name, school)
        return super().school_mult(school, periodic, name)

    def mana_cost(self, base):
        return base * (1 - self.d("hunter", "efficiency"))

    def think(self):
        d = self.d
        self.use_racials()
        rf = d("hunter", "rapid_fire")
        if self.ready("rapid_fire"):
            self.trigger("rapid_fire", rf["cd"] - d("hunter", "rapid_killing_cd"))
            self.buff("rapid_fire", rf["dur"], haste=True)
        if not self.gcd_ready():
            return
        frac = self.mana / self.max_mana
        aim, sn = d("hunter", "aimed_shot"), d("hunter", "sniper_shot")
        if self.ready("aimed") and self.spend_mana(self.mana_cost(aim["mana"])):
            return self._cast("aimed", aim["cd"], aim["cast"], "Aimed Shot", aim["flat"], 1 + d("hunter", "barrage"))
        if self.ready("sniper") and frac > 0.25 and self.spend_mana(self.mana_cost(sn["mana"])):
            return self._cast("sniper", sn["cd"], sn["cast"], "Sniper Shot", sn["flat"], 1.0)
        ss = d("hunter", "serpent_sting")
        if not self.serpent.up and frac > 0.4 and self.spend_mana(self.mana_cost(ss["mana"])):
            if self.spell_outcome("nature", crit_base=-1) != MISS:
                tick = (ss["dmg"] / ss["ticks"] + ss["ap_tick"] * self.ap) * (1 + d("hunter", "imp_stings"))
                self.serpent.apply(tick, ss["ticks"], ss["dur"] / ss["ticks"])
            return self.start_gcd()
        ms = d("hunter", "multi_shot")
        if self.ready("multi") and frac > 0.5 and self.spend_mana(self.mana_cost(ms["mana"])):
            self.trigger("multi", ms["cd"])
            self.shot("Multi-Shot", self.shot_base() + ms["flat"], mult=1 + d("hunter", "barrage"))
            return self.start_gcd()
        ar = d("hunter", "arcane_shot")
        if self.ready("arcane") and frac > 0.5 and self.spend_mana(self.mana_cost(ar["mana"])):
            self.trigger("arcane", ar["cd"] - d("hunter", "imp_arcane_shot"))
            self.shot("Arcane Shot", ar["flat"] + ar["ap"] * self.ap, school="arcane")
            return self.start_gcd()

    def _cast(self, key, cd, cast, name, flat, mult):
        self.trigger(key, cd)
        self.cast_until = self.sim.t + cast
        self.start_gcd()
        self.sim.after(cast, lambda: self.shot(name, self.shot_base() + flat, mult=mult))


class MarksmanshipLoneWolf(Marksmanship):
    spec = "Marksmanship (Lone Wolf)"
    pet = False


SPECS = [Fury, Arms, Combat, Mutilate, Marksmanship, MarksmanshipLoneWolf, Retribution, Enhancement, FeralCat]
CLASS_NAMES = {"warrior": "Warrior", "rogue": "Rogue", "hunter": "Hunter", "paladin": "Paladin",
               "shaman": "Shaman", "druid": "Druid"}
