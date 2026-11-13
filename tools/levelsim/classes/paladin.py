"""Paladin: Holy, Protection and Retribution, levels 1-60.

Talent orders: docs/guides/paladin/talents.md leveling builds
(Retribution (solo), Protection (dungeons), Holy (dungeon healer)); each ends in a 51-point build.

Talent values: the Forever client ships stale talent rows for most Paladin talents
(for example Conviction has 5 ranks of 5% in the client, 3 ranks of 2% in the game).
Talent values therefore come from the Forever tooltip text at max rank
(.research/talents/paladin.json, divided by max rank) and are tagged A.

Rotation (all specs, only abilities known at that level):
  1. Seal (Righteousness; Command from 20 for Retribution) if missing or about to expire.
  2. Hammer of Wrath in the last 20% of the fight (target health assumed linear).
  3. Judgement on cooldown (Swift Judgement too, Protection).
  4. Holy Shock on cooldown (Holy, from 30).
  5. Holy Strike on cooldown.
  6. Unsealed Wrath (Retribution 40+): with 3 stored stacks, switch between Seal of Command
     and Seal of Righteousness so the next hit releases the 3 stored seal procs.
  7. Consecration while mana is above 40% (keeps mana for seals, Judgement and Hammer of Wrath).
  Auto-attack throughout. Holy and Protection are scored on this same damage rotation.

Not used: Exorcism and Holy Wrath (Undead/Demon targets only; the target is a training dummy),
Seal of the Crusader (would cost a GCD and seal uptime; small gain), Holy Shield and Reckoning
(no attacks against the paladin), Seal of Fury (its Holy damage is small without a shield).

Server-side rules and values not in the client (tags):
  - Attack power = 2 x Strength + 3 x level - 20 (CU, Classic Paladin).
  - Seal of Righteousness per-hit damage: the tooltip range interpolated for a 2.0 s weapon (A).
  - Seal of Command: 7 procs per minute (CU), so 23.3% per 2.0 s swing.
  - Judgement of Command: 46-50 Holy, coefficient 0.429 (CU, Classic rank 1; the client has
    only the talent rank, so it does not scale with level).
  - Consecration damage: Classic ranks 64/120/192/280/384 over 8 s, 8 s cooldown,
    coefficient 0.042 per tick (CU); the client points to a missing spell.
  - Hammer of Wrath cooldown 6 s (CU). Holy Strike cooldown 10 s (A: Shieldsworn says
    -4 s gives "Holy Strike each 6 s").
  - Mana regen: 15 + Spirit/5 per 2 s outside the 5-second rule (CU); Reverence keeps a share.
  - Seals and Holy Strike work with the unarmed fist (A, no gear requested). Two-Handed Weapon
    Specialization gives nothing unarmed (A).
  - Blessing of Might is on the paladin before the pull (A).
  - Gear (core.GEAR "crafted", gear.py): gear stats come through core.Character; gear
    "+attack power" adds to AP and gear spell damage (generic + Holy) adds to the
    Champion of the Light spell power (F (crafted items)). The weapon's average damage and
    speed replace the fist; Holy Strike uses the weapon type's normalized speed (1.7
    dagger, 2.4 one-hand, 3.3 two-hand, CU). With a two-hander, Two-Handed Weapon
    Specialization adds 2% weapon damage per rank (CU, Classic).
"""
import core

CLASS = "paladin"
SPECS = {"holy": "Holy", "protection": "Protection", "retribution": "Retribution"}

# Leveling orders (one point per entry repeat), docs/guides/paladin/talents.md
_ORDERS = {
    "retribution": [("Benediction", 5), ("Conviction", 3), ("Improved Judgement", 2), ("Seal of Command", 1),
                    ("Sanctified Judgement", 3), ("Pursuit of Justice", 2), ("Two-Handed Weapon Specialization", 3),
                    ("Sacred Arbiter", 1), ("Vengeance", 3), ("Vindication", 1), ("Repentance", 1),
                    ("Champion of the Light", 5), ("Unsealed Wrath", 1), ("Divine Strength", 5),
                    ("Improved Seals", 5), ("Holy Conduit", 2), ("Divine Intellect", 5), ("Precision", 3)],
    "protection": [("Redoubt", 5), ("Precision", 3), ("Sacred Duty", 2), ("Templar's Bulwark", 1),
                   ("Shield Specialization", 2), ("Toughness", 2), ("Swift Judgement", 1),
                   ("Improved Righteous Fury", 3), ("Anticipation", 1), ("Holy Shield", 1), ("Reckoning", 4),
                   ("Iron Creed", 3), ("Reckoning", 1), ("Anticipation", 1), ("Shieldsworn", 1), ("Anticipation", 3),
                   ("Divine Intellect", 5), ("Benediction", 5), ("Conviction", 3), ("Improved Judgement", 2),
                   ("Toughness", 2)],
    "holy": [("Divine Strength", 5), ("Improved Seals", 5), ("Holy Conduit", 2), ("Reverence", 2),
             ("Divine Favor", 1), ("Oath of Light", 1), ("Illumination", 4), ("Holy Shock", 1), ("Illumination", 1),
             ("Healing Light", 3), ("Holy Power", 5), ("Light's Vigil", 1), ("Boundless Light", 2),
             ("Infusion of Light", 2), ("Benediction", 5), ("Conviction", 3), ("Improved Judgement", 2),
             ("Divine Intellect", 5), ("Spiritual Focus", 1)],
}

# Forever tooltip value per rank (max-rank text / max rank), tag A
_TT = {
    "Divine Strength": 2.0, "Divine Intellect": 2.0, "Improved Seals": 3.0, "Holy Conduit": 20.0,
    "Reverence": 15.0, "Precision": 1.0, "Benediction": 2.0, "Improved Judgement": 1.0, "Conviction": 2.0,
    "Sanctified Judgement": 20.0, "Vengeance": 1.0, "Champion of the Light": 12.0, "Sacred Arbiter": 20.0,
    "Shieldsworn": 4.0, "Two-Handed Weapon Specialization": 0.0,
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


def _rank(name, level, pred=None):
    """Highest usable rank; skips client duplicates (heal halves, no-cost copies)."""
    rs = [s for s in core.ranks(CLASS, name) if s["base_level"] <= level and (pred is None or pred(s))]
    return rs[-1] if rs else None


def _has_dmg(s):
    return any(e["Effect"] == core.SCHOOL_DAMAGE for e in s["effects"])


CONSECRATION_CU = {20: 64, 30: 120, 40: 192, 50: 280, 60: 384}


TWO_HAND = {"axe2h", "sword2h", "mace2h", "polearm", "staff"}


class Fight:
    def __init__(self, sim, spec, race, level, inputs):
        self.sim, self.spec, self.level, self.inp = sim, spec, level, inputs
        t = talents_at(spec, level)
        ch = self.ch = core.Character(CLASS, race, level, t)
        core.apply_passive_racials(ch, race)
        tv = lambda n: ch.tr(n) * _TT.get(n, 0.0)
        self.tv = tv
        ch.str *= 1 + tv("Divine Strength") / 100
        ch.int *= 1 + tv("Divine Intellect") / 100
        ch.hit += tv("Precision")
        ch.crit_bonus += tv("Conviction")
        ch.spell_crit_bonus += tv("Conviction")
        ch.sp = ch.int * tv("Champion of the Light") / 100 + ch.gear_sp("holy")
        bom = _rank("Blessing of Might", level)
        self.ap = 2 * ch.str + 3 * level - 20 + (bom["effects"][0]["EffectBasePointsF"] if bom else 0) + ch.gear_ap()
        self.wavg, self.speed = ch.weapon("mh")
        mh = ch.gear["mh"] if ch.gear else None
        two_hand = bool(mh and mh["type"] in TWO_HAND)
        self.norm = 1.7 if mh and mh["type"] == "dagger" else 3.3 if two_hand else 2.4
        self.wmult = 1 + 2 * ch.tr("Two-Handed Weapon Specialization") / 100 if two_hand else 1.0
        if ch.gear:
            inputs.update({"gear": "F (crafted items)", "normalized_speed_by_weapon_type": "CU"})
            if two_hand:
                inputs["two_handed_weapon_specialization_2pct"] = "CU"
        self.max_mana = self.mana = ch.mana()
        self.last_spend = -10.0
        self.busy = 0.0
        self.cd = {}
        self.veng = (0, -1.0)  # stacks, expiry
        self.seal = None
        self.seal_exp = -1.0
        self.stored = (None, 0, -1.0)  # Unsealed Wrath: seal, stacks, expiry
        self.sor = _rank("Seal of Righteousness", level, lambda s: bool(s["costs"]))
        self.jor = _rank("Judgement of Righteousness", level)
        self.soc = core.talent(CLASS, "Seal of Command")["ranks"][0] if ch.tr("Seal of Command") else None
        self.judgement = _rank("Judgement", level)
        self.hstrike = _rank("Holy Strike", level)
        self.consec = _rank("Consecration", level)
        self.how = _rank("Hammer of Wrath", level)
        self.hshock = bool(ch.tr("Holy Shock"))
        self.hshock_rank = _rank("Holy Shock", level, _has_dmg)
        self.unsealed = bool(ch.tr("Unsealed Wrath"))
        self.swift = bool(ch.tr("Swift Judgement"))
        inputs.update({"talents": "A (Forever tooltip)", "attack_power_formula": "CU", "unarmed_weapon": "CU",
                       "base_stats": ch.stats_tag, "mana_regen_spirit": "CU", "spell_ranks": "F",
                       "seal_of_righteousness_per_hit": "A", "blessing_of_might": "F"})

    # ----- helpers -----
    @property
    def t(self):
        return self.sim.t

    def instant_cost(self, spell, extra=0.0):
        _, c = core.cost(spell, self.ch.base_mana)
        return c * (1 - (self.tv("Benediction") + extra) / 100)

    def spend(self, c):
        self.mana -= c
        if c > 0:
            self.last_spend = self.t

    def vmult(self):
        st, ex = self.veng
        return 1 + (st * self.tv("Vengeance") / 100 if ex > self.t else 0)

    def on_crit(self):
        if self.ch.tr("Vengeance"):
            st, ex = self.veng
            self.veng = (min(5, (st if ex > self.t else 0) + 1), self.t + 30)

    def white_dmg(self, normalized=False):
        return (self.wavg + self.ap / 14 * (self.norm if normalized else self.speed)) * self.wmult

    def holy(self, src, amount, roll=True, melee_crit=False):
        """Holy damage with Improved Seals applied by caller where relevant."""
        if roll:
            if melee_crit:
                o = core.melee_roll(self.sim.rng, self.ch, white=False)
                if o in ("miss", "dodge"):
                    return
                mult = core.A("melee_crit_mult") if o == "crit" else 1.0
            else:
                o = core.spell_roll(self.sim.rng, self.ch)
                if o == "miss":
                    return
                mult = core.A("spell_crit_mult") if o == "crit" else 1.0
            if o == "crit":
                self.on_crit()
        else:
            mult = 1.0
        self.sim.deal(src, amount * mult * self.vmult())

    # ----- seals -----
    def seal_proc(self, seal):
        imp = 1 + self.tv("Improved Seals") / 100
        if seal == "SoR":
            s = core.effect_value(self.sor["effects"][0], self.level, self.sor["spell_level"])
            per = s / 87 + (s / 25 - s / 87) * (self.speed - 1.5) / 2.3
            per += self.sor["effects"][0]["EffectBonusCoefficient"] * self.ch.sp
            self.holy("Seal of Righteousness", per * imp, roll=False)
        elif seal == "SoC":
            if self.sim.rng.chance(7 * self.speed / 60 * 100):
                trig = self.soc["effects"][0]["trigger"]["effects"][0]
                dmg = self.white_dmg() * trig["EffectBasePointsF"] / 100 + trig["EffectBonusCoefficient"] * self.ch.sp
                self.holy("Seal of Command", dmg * imp, melee_crit=True)

    def melee_landed(self):
        if self.seal_exp <= self.t:
            return
        if self.unsealed:
            s, n, ex = self.stored
            if s and s != self.seal and n and ex > self.t:
                for _ in range(n):
                    self.seal_proc(s)
                n = 0
            if s != self.seal:
                n = 0
            self.stored = (self.seal, min(3, n + 1), self.t + 15)
        self.seal_proc(self.seal)

    # ----- events -----
    def swing(self):
        o = core.melee_roll(self.sim.rng, self.ch, white=True)
        d = self.white_dmg() * self.vmult()
        if o == "crit":
            d *= core.A("melee_crit_mult")
            self.on_crit()
        elif o == "glance":
            d *= core.A("glance_damage")
        if o not in ("miss", "dodge"):
            self.sim.deal("Melee", d)
            self.melee_landed()
        self.sim.at(self.t + self.speed / self.ch.haste, self.swing)

    def regen(self):
        base = 15 + self.ch.spi / 5
        frac = 1.0 if self.t - self.last_spend >= 5 else self.tv("Reverence") / 100
        self.mana = min(self.max_mana, self.mana + base * frac)
        self.sim.at(self.t + 2, self.regen)

    def ready(self, k):
        return self.cd.get(k, 0) <= self.t + 1e-9

    def cast_seal(self, which):
        sp = self.sor if which == "SoR" else self.soc
        c = self.instant_cost(sp)
        if self.mana < c:
            return False
        self.spend(c)
        self.seal, self.seal_exp = which, self.t + 30
        self.sim.cast("Seal of Righteousness" if which == "SoR" else "Seal of Command")
        return True

    def judge(self, key):
        imp = 1 + self.tv("Improved Seals") / 100
        seal_spell = self.sor if self.seal == "SoR" else self.soc
        if self.seal == "SoR":
            e = self.jor["effects"][0]
            lo, hi = core.effect_range(e, self.level, self.jor["spell_level"])
            dmg = self.sim.rng.uniform(lo, hi) + e["EffectBonusCoefficient"] * self.ch.sp
        else:
            dmg = self.sim.rng.uniform(46, 50) + 0.429 * self.ch.sp
        self.holy("Judgement", dmg * imp)
        if self.ch.tr("Sanctified Judgement"):
            r = self.ch.tr("Sanctified Judgement")
            if self.sim.rng.chance(r / 3 * 100):
                self.mana += core.cost(seal_spell, self.ch.base_mana)[1] * r * 0.2
        self.sim.cast(key)

    def act(self):
        if self.t < self.busy - 1e-9:
            return
        ch, t, gcd = self.ch, self.t, 1.5
        reserve = 0.0
        if self.judgement:
            reserve = self.instant_cost(self.judgement) + self.instant_cost(self.sor)
        want = "SoC" if self.soc else "SoR"
        # 1. seal
        if self.seal_exp - t < 1.5:
            if self.cast_seal(want if not (self.unsealed and self.seal_exp > t) else self.seal or want):
                return self.after(gcd)
        # 2. Hammer of Wrath (execute phase)
        if self.how and t >= 0.8 * self.sim.end and self.ready("how"):
            c = core.cost(self.how, ch.base_mana)[1] * (1 - self.tv("Holy Conduit") / 100)
            if self.mana >= c:
                self.spend(c)
                cast = max(0.0, self.how["cast_ms"] / 1000 - 0.2 * ch.tr("Champion of the Light")) / ch.haste
                self.cd["how"] = t + 6
                e = self.how["effects"][0]
                lo, hi = core.effect_range(e, self.level, self.how["spell_level"])
                dmg = self.sim.rng.uniform(lo, hi) + e["EffectBonusCoefficient"] * ch.sp
                self.sim.cast("Hammer of Wrath")
                self.sim.at(t + cast, self.holy, "Hammer of Wrath", dmg)
                return self.after(max(gcd, cast))
        # 3. Judgement
        if self.judgement and self.seal_exp > t and self.ready("judgement"):
            c = self.instant_cost(self.judgement)
            if self.mana >= c:
                self.spend(c)
                self.cd["judgement"] = t + self.judgement["cooldown_ms"] / 1000 - self.tv("Improved Judgement")
                self.judge("Judgement")
                return self.after(gcd)
        if self.swift and self.seal_exp > t and self.ready("swift"):
            self.cd["swift"] = t + 60
            self.judge("Swift Judgement")
            return self.after(gcd)
        # 4. Holy Shock
        if self.hshock and self.ready("hshock"):
            c = self.instant_cost(core.talent(CLASS, "Holy Shock")["ranks"][0])
            if self.mana >= c + reserve:
                self.spend(c)
                self.cd["hshock"] = t + 10
                if self.hshock_rank:
                    e = core.damage_effect(self.hshock_rank)
                    lo, hi = core.effect_range(e, self.level, self.hshock_rank["spell_level"])
                else:
                    lo, hi = 129, 139  # tooltip at talent level (A)
                self.sim.cast("Holy Shock")
                self.holy("Holy Shock", self.sim.rng.uniform(lo, hi) + 0.429 * ch.sp)
                return self.after(gcd)
        # 5. Holy Strike
        if self.hstrike and self.ready("hstrike"):
            c = self.instant_cost(self.hstrike)
            if self.mana >= c:
                self.spend(c)
                self.cd["hstrike"] = t + 10 - self.tv("Shieldsworn")
                self.holy_strike()
                return self.after(gcd)
        # 6. Unsealed Wrath twist
        if self.unsealed and self.soc:
            s, n, ex = self.stored
            if s == self.seal and n >= 3 and ex > t:
                other = "SoR" if self.seal == "SoC" else "SoC"
                if self.mana >= self.instant_cost(self.sor if other == "SoR" else self.soc) + reserve:
                    self.cast_seal(other)
                    return self.after(gcd)
        # 7. Consecration
        if self.consec and self.ready("consec"):
            c = self.instant_cost(self.consec, self.tv("Holy Conduit"))
            if self.mana >= max(c + 2 * reserve, 0.4 * self.max_mana):
                self.spend(c)
                self.cd["consec"] = t + 8
                tot = max(v for k, v in CONSECRATION_CU.items() if k <= self.level)
                for i in range(1, 9):
                    self.sim.at(t + i, self.holy, "Consecration", tot / 8 + 0.042 * ch.sp, False)
                self.sim.cast("Consecration")
                return self.after(gcd)
        # nothing: wake at the next cooldown or regen
        nxt = [v for v in self.cd.values() if v > t] + [t + 1.0, self.seal_exp - 1.4]
        if self.how and t < 0.8 * self.sim.end:
            nxt.append(0.8 * self.sim.end)
        self.sim.at(min(x for x in nxt if x > t + 1e-6), self.act)

    def holy_strike(self):
        r = core.melee_roll(self.sim.rng, self.ch, white=False)
        self.sim.cast("Holy Strike")
        if r in ("miss", "dodge"):
            return
        effs = {e["Effect"]: e for e in self.hstrike["effects"]}
        pct = effs[core.WEAPON_PERCENT_DAMAGE]["EffectBasePointsF"] / 100
        he = effs[core.NORMALIZED_WEAPON_DMG]
        lo, hi = core.effect_range(he, self.level, self.hstrike["spell_level"])
        mult = (core.A("melee_crit_mult") if r == "crit" else 1.0) * self.vmult() * (1 + self.tv("Sacred Arbiter") / 100)
        if r == "crit":
            self.on_crit()
        self.sim.deal("Holy Strike", (self.white_dmg(True) * pct + self.sim.rng.uniform(lo, hi) + 0.429 * self.ch.sp) * mult)
        self.melee_landed()

    def after(self, dt):
        self.busy = self.t + dt
        self.sim.at(self.busy, self.act)

    def start(self):
        self.sim.at(0.0, self.swing)
        self.sim.at(2.0, self.regen)
        self.sim.at(0.0, self.act)


def simulate(spec, race, level, iterations, seed):
    inputs = {}

    def build(sim):
        Fight(sim, spec, race, level, inputs).start()

    r = core.run_many(build, iterations, seed)
    inputs.update({"sor_seal_of_command_ppm": "CU", "judgement_of_command": "CU", "consecration_damage": "CU",
                   "holy_strike_cooldown": "A", "hammer_of_wrath_cooldown": "CU", "fight_seconds": "A"})
    r["inputs"] = inputs
    return r
