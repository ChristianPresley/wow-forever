"""Priest level simulator: Discipline (Smite/Penance), Holy (Smite/Holy Fire), Shadow.

Uses the caster engine in classes/mage.py (CasterSim). Spell values come from
forever.json through core. Talent values per rank come from the Forever launch
tooltips (.research/talents/priest.json), stored in TALENT_VALUES, tag A,
because the client talent table is incomplete (Power in Light, Twin Disciplines,
Improved Mind Flay and others are missing). Values the client does have
(Shadowform, Shadow Weaving step, Power Infusion, Inner Focus crit) are read
from it and tagged F.

Server-side rules not in the client (tag in brackets):
- Penance: 3 bolts over a 2 s channel (at 0, 1 and 2 s), 12 s cooldown from
  the client [CU for bolt count and timing].
- Shadow Word: Death: client damage is `damagepower * 346%`. damagepower uses the
  Season of Discovery level formula 9.456667 + 0.635108*L + 0.039995*L^2 [CU].
  Learned at level 32 by every Priest (wiki guide). Backlash is ignored: it hurts
  only the Priest.
- Devouring Plague is baseline at level 20 (wiki guide).
- Inner Focus: 3 min cooldown (Classic) [CU]. Used on the next Mind Blast or Smite.
- Improved Mind Flay: tick k deals (1+x)^k times the base tick [A].
- Twin Disciplines applies to instant spells (SW:Pain, Devouring Plague,
  SW:Death), not to channels (Mind Flay, Penance) [A].
- Spiritual Guidance: spell damage = 1..8% of Spirit, linear per rank [A].
- Starshards, Chastise, Shadowguard, Vampiric Embrace and Holy Nova (paid) are not
  used: racial, humanoid-only, self-buff, no damage, or AoE spells. Holy Nova is
  cast only when Searing Light makes it free [A].
- Spirit regen, 5-second rule, mana at cast start, no periodic crits: see mage.py.
"""
import core
from .mage import CasterSim, GCD, Spell, spell

CLASS = "priest"
SPECS = {"discipline": "Discipline", "holy": "Holy", "shadow": "Shadow"}

BUILDS = {
    "discipline": [  # Discipline (safe) leveling build, 51 points (Smite/Penance damage)
        ("Wand Specialization", 2), ("Twin Disciplines", 3), ("Holy Precision", 1), ("Mental Strength", 4),
        ("Improved Power Word: Shield", 3), ("Meditation", 2), ("Soul Warding", 1), ("Mental Agility", 3),
        ("Inner Focus", 1), ("Penance", 1), ("Power in Light", 5), ("Twin Disciplines", 2),
        ("Mental Strength", 1), ("Meditation", 1), ("Power Infusion", 1), ("Holy Specialization", 5),
        ("Divine Fury", 5), ("Holy Precision", 2), ("Twilight Focus", 3), ("Improved Renew", 2),
        ("Searing Light", 2), ("Holy Nova", 1)],
    "holy": [  # Holy damage build 0/31/20 for this simulator (no guide build is a Holy DPS build)
        ("Holy Specialization", 5), ("Divine Fury", 5), ("Twilight Focus", 3), ("Holy Nova", 1),
        ("Blessed Recovery", 1), ("Searing Light", 2), ("Holy Reach", 2), ("Improved Healing", 1),
        ("Spiritual Guidance", 5), ("Spiritual Healing", 3), ("Spirit of Redemption", 1),
        ("Litany of Light", 1), ("Prayer of Mending", 1), ("Twin Disciplines", 5), ("Holy Precision", 3),
        ("Mental Strength", 5), ("Mental Agility", 3), ("Inner Focus", 1), ("Meditation", 3)],
    "shadow": [  # Shadow Magic (raid) 20/0/31
        ("Shadow Focus", 5), ("Improved Mind Blast", 5), ("Improved Shadow Word: Pain", 2),
        ("Shadow Reach", 2), ("Mind Flay", 1), ("Improved Mind Flay", 2), ("Vampiric Embrace", 1),
        ("Shadow Weaving", 3), ("Devouring Contagion", 2), ("Silence", 1), ("Dark Inspiration", 1),
        ("Darkness", 5), ("Shadowform", 1), ("Twin Disciplines", 5), ("Silent Resolve", 3),
        ("Mental Strength", 5), ("Mental Agility", 3), ("Inner Focus", 1), ("Meditation", 3)],
}

TALENT_VALUES = {
    "Power in Light": [2, 4, 6, 8, 10],          # % Smite/Penance vs your HF or SW:P target
    "Twin Disciplines": [1, 2, 3, 4, 5],         # % instant spells
    "Holy Precision": [6, 12, 18],               # % Holy hit
    "Mental Strength": [2, 4, 6, 8, 10],         # % Int
    "Mental Agility": [3, 7, 10],                # % cost Smite, Holy Fire, instants
    "Meditation": [17, 33, 50],                  # % regen while casting
    "Holy Specialization": [1, 2, 3, 4, 5],      # % Holy crit
    "Divine Fury": [0.1, 0.2, 0.3, 0.4, 0.5],    # s off Smite, Holy Fire
    "Searing Light": [(2, 5), (5, 10)],          # % Holy damage, % free Holy Nova per HF tick
    "Spiritual Guidance": [1, 2.75, 4.5, 6.25, 8],  # % of Spirit as spell damage
    "Improved Healing": [5, 10, 15],             # % Penance cost
    "Shadow Focus": [1, 2, 3, 4, 5],             # % Shadow hit
    "Improved Mind Blast": [0.5, 1, 1.5, 2, 2.5],  # s off Mind Blast
    "Improved Shadow Word: Pain": [3, 6],        # s SW:P duration
    "Improved Mind Flay": [10, 20],              # % per tick over previous
    "Shadow Weaving": [33.3, 66.7, 100],         # % chance
    "Devouring Contagion": [25, 50],             # % DP cost
    "Darkness": [2, 4, 6, 8, 10],                # % Shadow damage
}

HOLY, SHADOW = 2, 32
PENANCE_BOLTS = (0.0, 1.0, 2.0)   # CU
INNER_FOCUS_CD = 180             # CU
SWD_LEVEL = 32
DP_LEVEL = 20


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


def damagepower(level):
    """Season of Discovery level-scaled base value (CU)."""
    return 9.456667 + 0.635108 * level + 0.039995 * level * level


def _client(name):
    return [s for s in core.data()["classes"][CLASS]["spells"] if s["name"] == name]


class PriestSim(CasterSim):
    def __init__(self, sim, ch, spec, level, talents, inputs):
        super().__init__(sim, ch, inputs)
        self.spec, self.level, self.tal = spec, level, talents
        self.T = lambda n: self._tv(n)
        bm = ch.base_mana
        S = {}
        for n in ("Smite", "Shadow Word: Pain", "Mind Blast", "Holy Fire"):
            s = spell(CLASS, n, level, bm, inputs)
            if s:
                S[n] = s
        if level >= DP_LEVEL:
            s = spell(CLASS, "Devouring Plague", level, bm, inputs)
            if s:
                S["Devouring Plague"] = s
                inputs["devouring_plague_baseline_20"] = "CU"
        if talents.get("Mind Flay"):
            s = spell(CLASS, "Mind Flay", level, bm, inputs)
            if s:
                S["Mind Flay"] = s
        if talents.get("Holy Nova"):
            s = spell(CLASS, "Holy Nova", level, bm, inputs, raw=self._holy_nova(level))
            if s:
                S["Holy Nova"] = s
        if level >= SWD_LEVEL:
            raw = _client("Shadow Word: Death")[0]
            s = Spell(raw, level, bm)
            e = s.direct
            dp = damagepower(level)
            var = next(x["Variance"] for x in raw["effects"] if x["Effect"] == core.SCHOOL_DAMAGE)
            avg = dp * next(x["EffectBasePointsF"] for x in raw["effects"] if x["Effect"] == core.SCHOOL_DAMAGE) / 100
            s.direct = (avg * (1 - var / 2), avg * (1 + var / 2), e[2])
            S["Shadow Word: Death"] = s
            inputs["spell:Shadow Word: Death"] = "F"
            inputs["swd_damagepower"] = "CU"
        if talents.get("Penance"):
            cast, bolt = self._penance(level)
            if cast:
                s = Spell(cast, level, bm)
                b = Spell(bolt, level, bm)
                s.direct = b.direct
                s.school = HOLY
                S["Penance"] = s
                inputs["spell:Penance"] = "F"
                inputs["penance_bolts"] = "CU"
        self.S = S
        # talents
        ms = self.T("Mental Strength")
        ch.int *= 1 + ms / 100
        self.max_mana = self.mana = ch.mana()
        self.regen_while_casting = self.T("Meditation") / 100
        sg = self.T("Spiritual Guidance")
        self.sp = ch.spi * sg / 100
        self.shadowform = bool(talents.get("Shadowform"))
        if self.shadowform:
            sf = _client("Shadowform")[0]["effects"]
            self.sf_dmg = sf[1]["EffectBasePointsF"]
            self.sf_cost = sf[3]["EffectBasePointsF"]
            self.sf_crit = sf[4]["EffectBasePointsF"]
            inputs["talent:Shadowform"] = "F"
        self.weave_step = 0
        if talents.get("Shadow Weaving"):
            w = _client("Shadow Weaving")[0]["effects"][0]
            self.weave_step = w["trigger"]["effects"][0]["EffectBasePointsF"]
            inputs["talent:Shadow Weaving step"] = "F"
        self.pi = bool(talents.get("Power Infusion"))
        if self.pi:
            p = _client("Power Infusion")[0]
            self.pi_spell = Spell(p, level, bm)
            self.pi_dmg = p["effects"][1]["EffectBasePointsF"]
            inputs["talent:Power Infusion"] = "F"
        self.inner_focus = bool(talents.get("Inner Focus"))
        if self.inner_focus:
            r = core.talent(CLASS, "Inner Focus")["ranks"][0]["effects"]
            self.if_crit = r[1]["EffectBasePointsF"]
            inputs["talent:Inner Focus"] = "F"
            inputs["inner_focus_cd"] = "CU"
        # state
        self.weave, self.weave_end = 0, 0.0
        self.if_on = False
        self.free_nova = False

    def _tv(self, name):
        r = self.tal.get(name, 0)
        if not r or name not in TALENT_VALUES:
            return 0
        self.inputs[f"talent:{name}"] = "A"
        v = TALENT_VALUES[name][r - 1]
        return v

    @staticmethod
    def _holy_nova(level):
        avail = [s for s in _client("Holy Nova") if 0 < s["base_level"] <= level
                 and any(e["Effect"] == core.SCHOOL_DAMAGE for e in s["effects"])]
        return max(avail, key=lambda s: s["base_level"]) if avail else None

    @staticmethod
    def _penance(level):
        rows = [s for s in _client("Penance") if 0 < s["base_level"] <= level]
        casts = [s for s in rows if s["costs"]]
        if not casts:
            return None, None
        c = max(casts, key=lambda s: s["base_level"])
        bolt = next(s for s in rows if s["base_level"] == c["base_level"] and not s["costs"]
                    and any(e["Effect"] == core.SCHOOL_DAMAGE for e in s["effects"]))
        return c, bolt

    # --- modifiers
    def is_(self, sp, school):
        return bool(sp.school & school)

    def instant(self, sp):
        return sp.name in ("Shadow Word: Pain", "Devouring Plague", "Shadow Word: Death", "Holy Nova")

    def dmg_mult(self, sp, periodic):
        m = super().dmg_mult(sp, periodic)
        if self.has("power_infusion"):
            m *= 1 + self.pi_dmg / 100
        if self.is_(sp, SHADOW):
            m *= 1 + self.T("Darkness") / 100
            if self.shadowform:
                m *= 1 + self.sf_dmg / 100
            if self.weave and self.weave_end > self.t:
                m *= 1 + self.weave_step * self.weave / 100
        if self.is_(sp, HOLY):
            sl = self.T("Searing Light")
            if sl:
                m *= 1 + sl[0] / 100
        if self.instant(sp):
            m *= 1 + self.T("Twin Disciplines") / 100
        if sp.name in ("Smite", "Penance") and (self.dot_up("Holy Fire") or self.dot_up("Shadow Word: Pain")):
            m *= 1 + self.T("Power in Light") / 100
        return m

    def crit_chance(self, sp):
        c = 0.0
        if self.is_(sp, HOLY):
            c += self.T("Holy Specialization")
        if self.if_on:
            c += self.if_crit
        return c

    def crit_bonus(self, sp):
        if self.shadowform and self.is_(sp, SHADOW):
            return self.sf_crit / 100
        return 0.0

    def hit_bonus(self, sp):
        h = 0.0
        if self.is_(sp, HOLY):
            h += self.T("Holy Precision")
        if self.is_(sp, SHADOW):
            h += self.T("Shadow Focus")
        return h

    def cost_of(self, sp):
        if self.if_on or (sp.name == "Holy Nova" and self.free_nova):
            return 0.0
        c = sp.cost
        if self.shadowform and self.is_(sp, SHADOW):
            c *= 1 + self.sf_cost / 100
        if sp.name in ("Smite", "Holy Fire") or self.instant(sp):
            c *= 1 - self.T("Mental Agility") / 100
        if sp.name == "Devouring Plague":
            c *= 1 - self.T("Devouring Contagion") / 100
        if sp.name == "Penance":
            c *= 1 - self.T("Improved Healing") / 100
        if self.has("racial_direct") and sp.name not in ("Shadow Word: Pain", "Devouring Plague"):
            c *= 1 - self.racial[1] / 100
        return c

    def cast_time(self, sp):
        c = sp.cast
        if sp.name in ("Smite", "Holy Fire"):
            c -= self.T("Divine Fury")
        return max(0.0, c) / self.haste()

    def on_damage(self, sp, amount, crit, periodic):
        pass

    def weave_roll(self, sp):
        if self.weave_step and self.is_(sp, SHADOW) and self.rng.chance(self.T("Shadow Weaving")):
            self.weave = min(5, (self.weave if self.weave_end > self.t else 0) + 1)
            self.weave_end = self.t + 15

    def hf_tick(self):
        sl = self.T("Searing Light")
        if sl and "Holy Nova" in self.S and self.rng.chance(sl[1]):
            self.free_nova = True

    # --- actions
    def begin(self, sp):
        self.spend(self.cost_of(sp))
        use_if = self.if_on
        self.if_on = False
        if sp.cd:
            cd = sp.cd
            if sp.name == "Mind Blast":
                cd -= self.T("Improved Mind Blast")
            self.start_cd(sp, cd)
        self.sim.cast(sp.name)
        return use_if

    def cast(self, sp):
        use_if = self.begin(sp)
        ct = self.cast_time(sp)
        self.sim.at(self.t + ct, self.land, sp, use_if)
        return max(GCD, ct)

    def land(self, sp, use_if):
        self.if_on = use_if
        res = "hit"
        if sp.direct:
            res, _ = self.hit_direct(sp)
        else:
            res = self.roll(sp)
        self.if_on = False
        if res == "miss":
            return
        if sp.dot:
            dur = sp.duration
            on_tick = None
            if sp.name == "Shadow Word: Pain":
                dur += self.T("Improved Shadow Word: Pain")
            if sp.name == "Holy Fire":
                on_tick = self.hf_tick
            self.apply_dot(sp, duration=dur, on_tick=on_tick)
        self.weave_roll(sp)

    def penance(self, sp):
        use_if = self.begin(sp)
        for i, dt in enumerate(PENANCE_BOLTS):
            self.sim.at(self.t + dt, self._bolt, sp, use_if and i == 0)
        return max(GCD, PENANCE_BOLTS[-1])

    def _bolt(self, sp, use_if):
        self.if_on = use_if
        self.hit_direct(sp)
        self.if_on = False

    def mind_flay(self, sp):
        self.begin(sp)
        res = self.roll(sp)
        base, period, coef = sp.dot
        n = int(round(sp.duration / period))
        step = self.T("Improved Mind Flay") / 100
        if res != "miss":
            for k in range(n):
                self.sim.at(self.t + period * (k + 1), self._flay, sp, (base + coef * self.sp) * (1 + step) ** k)
        return max(GCD, sp.duration / self.haste())

    def _flay(self, sp, amount):
        self.sim.deal("Mind Flay", amount * self.dmg_mult(sp, True))
        self.weave_roll(sp)

    def affordable(self, sp):
        return self.mana >= self.cost_of(sp)

    def choose(self):
        S, t = self.S, self.t
        if self.pi and self.ready.get("pi", 0) <= t and self.mana >= self.pi_spell.cost:
            self.spend(self.pi_spell.cost)
            self.ready["pi"] = t + self.pi_spell.cd
            self.buffs["power_infusion"] = t + self.pi_spell.duration
            self.sim.cast("Power Infusion")
        if self.inner_focus and self.ready.get("if", 0) <= t and not self.if_on:
            self.if_on = True
            self.ready["if"] = t + INNER_FOCUS_CD
            self.sim.cast("Inner Focus")
        order = []
        nova = S.get("Holy Nova")
        if nova and self.free_nova:
            order.append(nova)
        swp = S.get("Shadow Word: Pain")
        if swp and not self.dot_up("Shadow Word: Pain"):
            order.append(swp)
        if self.spec == "holy":
            hf = S.get("Holy Fire")
            if hf and not self.dot_up("Holy Fire", margin=self.cast_time(hf)):
                order.append(hf)
        dp = S.get("Devouring Plague")
        if dp and not self.dot_up("Devouring Plague"):
            order.append(dp)
        for n in ("Penance", "Mind Blast", "Shadow Word: Death"):
            s = S.get(n)
            if s and self.cd_ready(s):
                order.append(s)
        if "Mind Flay" in S:
            order.append(S["Mind Flay"])
        order.append(S["Smite"])
        for sp in order:
            if not self.affordable(sp):
                continue
            if sp.name == "Holy Nova":
                self.free_nova = False
                self.sim.cast("Holy Nova")
                self.hit_direct(sp)
                return GCD
            if sp.name == "Penance":
                return self.penance(sp)
            if sp.name == "Mind Flay":
                return self.mind_flay(sp)
            return self.cast(sp)
        return 0.5


def simulate(spec, race, level, iterations, seed):
    talents = talents_at(spec, level)
    inputs = {}

    def build(sim):
        ch = core.Character(CLASS, race, level, talents)
        core.apply_passive_racials(ch, race)
        p = PriestSim(sim, ch, spec, level, talents, inputs)
        inputs["base_stats"] = ch.stats_tag
        p.start()

    out = core.run_many(build, iterations, seed)
    out["inputs"] = dict(sorted(inputs.items()))
    for k in ("fight_seconds", "spell_hit_same_level", "spell_crit_mult", "base_spell_crit"):
        out["inputs"][k] = core.ASSUMPTIONS[k][1]
    return out
