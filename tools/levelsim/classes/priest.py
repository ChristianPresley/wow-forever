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
- Shadow Word: Death: damage is Metabot's 434-462 at level 56 [F, MB]. The client
  value is `damagepower * 346%`, a level-scaled base, so other levels scale that
  range by the Season of Discovery damagepower curve
  9.456667 + 0.635108*L + 0.039995*L^2 relative to level 56 [CU].
  Learned at level 32 by every Priest (wiki guide). Backlash is ignored: it hurts
  only the Priest.
- Devouring Plague is baseline at level 20 (wiki guide).
- Inner Focus: 3 min cooldown (Classic) [CU]. The free cast goes to the spell that gains
  most from it (`focus_target`) [A]: for a spell the rotation casts anyway that is the mana
  saved at the plan's mana price, for a spell too expensive to cast otherwise (Devouring
  Plague without Devouring Contagion) it is the whole cast, plus the crit bonus on direct
  damage. The plan itself is made at normal costs. Holy and Shadow use this rule.
  Discipline keeps the older one (the next spell in the rotation's order is free, in
  practice Shadow Word: Pain): the new rule was better for it on average but 2.3% worse
  for a Human at level 60 in crafted gear.
- Improved Mind Flay: tick k deals (1+x)^k times the base tick [A].
- Twin Disciplines applies to instant spells (SW:Pain, Devouring Plague,
  SW:Death), not to channels (Mind Flay, Penance) [A].
- Spiritual Guidance: spell damage = 1..8% of Spirit, linear per rank [A].
- Race-locked spells [F]: the client's `race_mask` on a class spell names the races that
  learn it (`race_open`; 0 or -1 is every race, and the two Skyborne races have no bit, so
  they learn no race-locked spell). Every spell the rotation loads is checked against it.
  Starshards is the only locked one it casts: Night Elf only, an instant Arcane DoT, 6 ticks
  in 6 s, 30 s cooldown, learned at level 10. The other locked Priest spells (Touch of
  Weakness, Shadowguard, Hex of Weakness, Chastise, Desperate Prayer, Feedback, Divine
  Grace, Elune's Grace) are not rotation spells. It is the most mana-efficient spell a Night Elf Priest
  has, so every spec casts it on cooldown; Twin Disciplines and Mental Agility apply
  (instant spell) [A].
- Saving mana for the better spell [A] (`PriestSim.held`): when mana is short, a spell waits
  if paying for it would leave too little, with the regeneration until then, for a cooldown
  or DoT spell with more damage per mana that is ready before the mana is back. Without it
  a Night Elf out of mana spent what trickled in on Shadow Word: Pain just before Starshards
  came off cooldown, and some levels lost 2 to 3% against the level before. A DoT's expected
  damage counts only the ticks before the fight ends.
- Chastise, Shadowguard, Touch of Weakness, Vampiric Embrace and Holy Nova (paid) are not
  used: humanoid-only, reactive, self-buff, no damage, or AoE spells. Holy Nova is cast
  only when Searing Light makes it free [A]; the plan counts those free Novas (and their
  GCDs) in Holy Fire's value.
- Spells the plan knows and seldom or never casts at level 60, because they lose on damage
  per mana with the client's numbers (checked by forcing each into the rotation, which
  lowered DPS by 2 to 13%): Mind Blast for Shadow (4.8 damage per mana against 7.5 for Mind
  Flay and 12 for Shadow Word: Death), Penance for Discipline (0.85 to 1.2 against 3.5 to
  4.3 for Shadow Word: Death), top-rank Smite for Discipline and Holy (1.3 to 1.4; the wand
  does more for the mana). Holy Fire is cast by Holy once Holy Nova is known. A Priest who
  runs dry in 40 s of Smite therefore plays Shadow Word: Death and Pain, Mind Blast or
  Holy Fire on cooldown and the wand in between.
- Divine Fury (Discipline, 5 points for Holy Specialization's tree position): it adds
  nothing. It makes rank 2 Smite a 1.5 s cast, which the plan then casts instead of wanding
  during Power Infusion, and that lost 1.5%. The "plan+lean" policy (below) never casts a
  filler, so it is the same with and without the talent, and is the best one here.
- Spirit regen, 5-second rule, mana at cast start, no periodic crits: see mage.py.
- Third mana policy, "plan+swing" [A]: the plan charges a cooldown spell its whole cast time
  against the wand or melee damage of resting. In the fight the swing timer runs on during
  the cast, so an instant between two wand shots delays the next shot by about half a
  swing only. Under this policy a cooldown or DoT spell is credited with the swing damage
  it does not displace (`swing_overlap`): in the plan for the resting share of the time, in
  the choice when the Priest is resting. It is a policy and not the rule because it is
  better where the wand carries the rotation (Discipline in crafted gear, low-level Shadow:
  up to 13%) and up to 6% worse elsewhere (it casts Mind Blast where the mana was better
  kept for Mind Flay).
- Fourth mana policy, "plan+wand" [A]: "plan+swing" with no filler while mana is short. The
  plan prices a filler by its own damage and mana, but chain-casting it also delays every
  cooldown spell by half a cast on average and takes the wand shots that fit between
  instants. Where a cheap low-rank Smite only just beats the wand in the plan (Discipline in
  crafted gear from the mid-30s) wanding between cooldown spells is 1 to 4% better in the
  fight; for Shadow, whose Mind Flay clearly beats the wand, it is worse. `simulate` reports
  the best of the four (`POLICIES`).
- Why several policies [A]: the plan's mana price is too low when resting is interrupted
  often, so a spell that ties with resting in the plan can lose in the fight, and a new rank,
  a talent or a gear change tips the tie. With "plan" and "simple" alone ten level-to-level
  drops of 2 to 3% remained (the same at 1,000 fights, so not sampling noise); with the four
  policies a sweep of every spec, race, gear mode and level from 5 to 60 has none above 2%.
  Three talents still lost 0.5 to 1.5% at 60 in crafted gear with those four (Divine Fury
  and Holy Specialization for Discipline, Holy Nova for Holy): each made the plan trade wand
  time for a cheap Smite or a free Holy Nova that did less in the fight. A Priest with the
  talent can always play as if it were not there, so two more policies do that: "plan+lean"
  (cooldown and DoT spells and the wand, no filler, planned without a filler) and "+nonova"
  for Holy (the free Holy Nova is left unused). With them no talent lowers DPS.
- Mana-aware rotation [A] (mage.CasterSim.plan and best_policy, see mage.py; the text
  below describes the older rule, which is one of the policies tried): the filler (Smite or Mind Flay) is
  chosen by spell AND rank from every rank known at that level, by sustained damage
  over the remaining fight; when the best option cannot be sustained the Priest casts
  until empty, then rests (unarmed melee, full Spirit regen). SW:Pain, Holy Fire,
  Devouring Plague, Penance, Mind Blast and SW:Death are cast when they fit the mana
  budget or are at least as mana-efficient as the filler.
- Out of mana or resting: unarmed melee auto-attack, target in range [A]; attack
  power = Strength - 10 [CU].
- Gear (core.GEAR "crafted"): spell damage (generic + school), mp5 and the OOM wand /
  weapon melee are handled by mage.CasterSim (see mage.py); Mind Flay ticks include
  gear spell damage too.
"""
import core
from . import mage
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
FOCUS_FIRST_SPELL = ("discipline",)  # specs whose Inner Focus goes to the next spell cast (A, see docstring)
SWD_LEVEL = 32
# Mana policies tried per cell; the best is reported (A). "plan" and "simple" are mage.py's.
# "plan+swing" is the plan with one more rule: a cooldown spell cast while resting is credited
# with the wand or melee damage it does not displace (PriestSim.swing_overlap).
# "plan+wand" is "plan+swing" without a filler while mana is short: the Priest wands between
# cooldown spells instead of alternating filler casts and rests.
# "plan+lean" never casts a filler: cooldown and DoT spells, and the wand in between.
# "+nonova" leaves a free Holy Nova (Searing Light) unused; it is tried only for a Priest
# who has the talent and casts Holy Fire, which is Holy (`policies_for`).
# The last two exist because a talent must not lower DPS: a Priest can always play as if a
# faster or stronger Smite, or a free Holy Nova, were not there.
POLICIES = ("plan", "plan+swing", "plan+wand", "plan+lean", "simple")
NOVA_POLICIES = ("plan+nonova", "plan+swing+nonova")


def policies_for(talents, spec="holy"):
    nova = spec == "holy" and talents.get("Holy Nova") and talents.get("Searing Light")
    return POLICIES + (NOVA_POLICIES if nova else ())


POLICY = {"mode": "plan"}
# cooldown and DoT spells cast besides the filler (Holy Fire by Holy only)
NUKES = ("Shadow Word: Pain", "Devouring Plague", "Starshards", "Penance", "Mind Blast", "Shadow Word: Death", "Holy Fire")
# F: bit of each race in a class spell's race_mask (the Skyborne races, sho and sws, have none)
RACE_BIT = {"human": 1, "orc": 2, "dwarf": 4, "nelf": 8, "undead": 16, "tauren": 32, "gnome": 64, "troll": 128}


def race_open(row, race):
    """True when the race can learn the spell: no race mask (0 or -1) or the race's bit set."""
    mask = row.get("race_mask") or 0
    return mask <= 0 or bool(mask & RACE_BIT.get(race, 0))


def learn(name, level, race, base_mana, inputs):
    """The best rank known at this level, or None when the level or the race rules it out."""
    row = core.best_rank(CLASS, name, level)
    if not row or not race_open(row, race):
        return None
    if (row.get("race_mask") or 0) > 0:
        inputs[f"race_lock:{name}"] = "F"
    return spell(CLASS, name, level, base_mana, inputs, raw=row)
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


SWD_MB = (434, 462, 56)   # Metabot min, max, level [F]


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
        for n in ("Smite", "Shadow Word: Pain", "Mind Blast", "Holy Fire", "Starshards"):
            s = learn(n, level, ch.race, bm, inputs)
            if s:
                S[n] = s
        if level >= DP_LEVEL:
            s = learn("Devouring Plague", level, ch.race, bm, inputs)
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
            f = damagepower(level) / damagepower(SWD_MB[2])
            s.direct = (SWD_MB[0] * f, SWD_MB[1] * f, e[2])
            S["Shadow Word: Death"] = s
            inputs["spell:Shadow Word: Death"] = "F"
            inputs["swd_damage_metabot"] = "F"
            inputs["swd_level_scaling"] = "CU"
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
        # every known rank of the fillers, for mana-aware downranking (A)
        self.ranks_ = {}
        for n in ("Smite", "Mind Flay"):
            if n in S:
                rs = [Spell(r, level, bm) for r in core.ranks(CLASS, n) if r["base_level"] <= level and r["costs"]]
                self.ranks_[n] = rs or [S[n]]
        inputs["mana_budget_rotation"] = "A"
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
        rules = POLICY["mode"].split("+")[1:]
        self.swing = bool({"swing", "wand", "lean"} & set(rules))
        self.wand_first = "wand" in rules
        self.always_lean = "lean" in rules
        self.skip_nova = "nonova" in rules
        self.idle = self.rest_share = 0.0   # chance that a cooldown spell is cast between swings

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
        return sp.name in ("Shadow Word: Pain", "Devouring Plague", "Shadow Word: Death", "Holy Nova", "Starshards")

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
        if sl and "Holy Nova" in self.S and not self.skip_nova and self.rng.chance(sl[1]):
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
                self.sim.at(self.t + period * (k + 1), self._flay, sp, (base + coef * (self.sp + self.gear_sp_of(sp))) * (1 + step) ** k)
        return max(GCD, sp.duration / self.haste())

    def _flay(self, sp, amount):
        self.sim.deal("Mind Flay", amount * self.dmg_mult(sp, True))
        self.weave_roll(sp)

    def affordable(self, sp):
        return self.mana >= self.cost_of(sp)

    # --- mana planning (A)
    def exec_time(self, sp):
        if sp.name == "Mind Flay":
            return max(GCD, sp.duration / self.haste())
        if sp.name == "Penance":
            return max(GCD, PENANCE_BOLTS[-1])
        return max(GCD, self.cast_time(sp))

    def exp_damage(self, sp):
        """Expected damage of one cast (average roll + spell power, hit and crit folded in)."""
        p = self.spell_power(sp)
        direct = (sp.avg_direct + sp.direct[2] * p) if sp.direct else 0.0
        if sp.name == "Penance":
            direct *= len(PENANCE_BOLTS)
        dot = 0.0
        if sp.dot:
            base, period, coef = sp.dot
            n = int(round(sp.duration / period))
            if sp.name == "Shadow Word: Pain":
                n = int(round((sp.duration + self.T("Improved Shadow Word: Pain")) / period))
            if sp.name == "Mind Flay":
                step = self.T("Improved Mind Flay") / 100
                dot = (base + coef * p) * sum((1 + step) ** k for k in range(n))
            else:
                # only the ticks that land before the fight ends
                left = self.sim.end - self.t - self.cast_time(sp)
                n = max(0, min(n, int(left / period + 1e-9)))
                dot = (base + coef * p) * n
        crit = min(100.0, self.ch.spell_crit + self.crit_chance(sp)) / 100
        hit = min(99.0, core.A("spell_hit_same_level") + self.ch.hit + self.hit_bonus(sp)) / 100
        m = self.dmg_mult(sp, False)
        return hit * m * (direct * (1 + crit * (self.crit_mult(sp) - 1)) + dot)

    def option(self, sp):
        c = self.cost_of(sp)  # 0 under Inner Focus
        dmg, secs = self.exp_damage(sp), self.exec_time(sp)
        nova, sl = self.S.get("Holy Nova"), self.T("Searing Light")
        if sp.name == "Holy Fire" and nova and sl and sp.dot and not self.skip_nova:
            # Searing Light: each Holy Fire tick may make one Holy Nova free; it takes a GCD (A)
            n = int(round(sp.duration / sp.dot[1])) * sl[1] / 100
            dmg += n * self.exp_damage(nova)
            secs += n * GCD
        if self.swing and self.idle > 0 and sp.name in NUKES:
            dmg += self.idle * self.melee_dps() * self.swing_overlap(secs)
        return (sp, dmg, secs, c, self.mana >= c)

    def swing_overlap(self, secs):
        """Seconds of a cast that cost no wand or melee damage when it is cast between swings
        (A). The swing timer runs on during the cast, so the next swing is late only by what
        the cast overruns it: with the cast starting at a random point of the swing, a cast of
        s seconds (at most one swing, w) delays it by s * s / (2 * w) on average."""
        w = (self.wand["speed"] if self.wand else self.ch.weapon("mh")[1]) / self.haste()
        s = min(secs, w)
        return s - s * s / (2 * w)

    def focus_target(self, cands):
        """The spell that gains most from Inner Focus (A). A free cast is worth its damage
        (with the crit bonus) over what the same time earns otherwise, less what the spell
        would have earned anyway at its normal cost and the plan's mana price: for a spell
        the rotation casts in any case that is the mana saved, for one too expensive to
        cast it is the whole cast."""
        lam = self.lam
        alt = self.melee_dps() + lam * self.rest_gain
        for _, d, secs, c, _ in self._opts:
            alt = max(alt, (d - lam * c) / secs)
        best, best_gain = None, None
        for sp in cands:
            self.if_on = False
            _, d0, secs, c0, _ = self.option(sp)
            self.if_on = True
            gain = self.option(sp)[1] - secs * alt - max(0.0, d0 - lam * c0 - secs * alt)
            if best is None or gain > best_gain + 1e-9:
                best, best_gain = sp, gain
        return best

    def nuke_pool(self):
        out = []
        for name in NUKES:
            if name == "Holy Fire" and self.spec != "holy":
                continue
            sp = self.S.get(name)
            if not sp:
                continue
            period = sp.cd
            if name == "Mind Blast":
                period -= self.T("Improved Mind Blast")
            if sp.dot:
                dur = sp.duration + (self.T("Improved Shadow Word: Pain") if name == "Shadow Word: Pain" else 0)
                period = max(period, dur)
            out.append((sp, period))
        return out

    def held(self, sp):
        """Keep the mana for a better spell (A). When mana is short, `sp` waits if paying for it
        would leave too little, with the regeneration until then, for a cooldown or DoT spell
        that gives more damage per mana and is ready, or will be, before the mana is back."""
        c = self.cost_of(sp)
        if c <= 0 or self.lam <= 0:
            return False
        dpm = self.option(sp)[1] / c
        rf = self.regen_full_ps()
        for other, _ in self.nuke_pool():
            if other is sp:
                continue
            _, d2, _, c2, _ = self.option(other)
            if c2 <= 0 or d2 / c2 <= dpm:
                continue
            if other.dot and not other.cd:
                d = self.dots.get(other.name)
                wait = max(0.0, d["end"] - self.t) if d else 0.0
            else:
                wait = max(0.0, self.ready.get(other.category or other.name, 0) - self.t)
            if self.mana - c + rf * wait < c2:
                return True
        return False

    def cast_any(self, sp):
        if sp.name == "Penance":
            return self.penance(sp)
        if sp.name == "Mind Flay":
            return self.mind_flay(sp)
        return self.cast(sp)

    def choose(self):
        S, t = self.S, self.t
        if self.pi and self.ready.get("pi", 0) <= t and self.mana >= self.pi_spell.cost and not self.resting:
            self.spend(self.pi_spell.cost)
            self.ready["pi"] = t + self.pi_spell.cd
            self.buffs["power_infusion"] = t + self.pi_spell.duration
            self.sim.cast("Power Infusion")
        if self.inner_focus and self.ready.get("if", 0) <= t and not self.if_on:
            self.if_on = True
            self.ready["if"] = t + INNER_FOCUS_CD
            self.sim.cast("Inner Focus")
        nova = S.get("Holy Nova")
        if nova and self.free_nova:
            self.free_nova = False
            self.sim.cast("Holy Nova")
            self.hit_direct(nova)
            return GCD
        # Holy and Shadow plan at normal costs and Inner Focus picks its spell below (focus_target).
        # Discipline keeps the older rule: everything is free while it is up, first spell in order.
        focus = self.if_on and self.spec not in FOCUS_FIRST_SPELL
        if focus:
            self.if_on = False
        opts = [self.option(r) for rs in self.ranks_.values() for r in rs]
        if self.always_lean:
            # no filler in this rotation, so none in the plan's mana price either: a talent
            # that improves the filler then changes nothing here
            opts = []
        self.idle = self.rest_share
        fill, f, ok, need = self.plan(opts, no_filler=self.always_lean)
        self.rest_share = 1.0 - f
        if focus:
            self.if_on = True
        if self.resting and self.rest_done(f, need):
            self.resting = False
        lean = self.always_lean or ((self.lean or (self.wand_first and f < 1.0)) and not self.if_on)
        # the plan counts a cooldown spell as cast between swings for the resting share of the
        # time; the choice below knows whether it is
        self.idle = 1.0 if self.resting or lean else 0.0
        order = []
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
        for n in ("Starshards", "Penance", "Mind Blast", "Shadow Word: Death"):
            s = S.get(n)
            if s and self.cd_ready(s):
                order.append(s)
        if focus:
            sp = self.focus_target(order + [o[0] for o in opts])
            if sp is not None:
                return self.cast_any(sp)
        for sp in order:
            if self.efficient(sp, fill, resting=self.resting or lean) and not self.held(sp):
                return self.cast_any(sp)
        if self.resting or lean:
            return self.melee_idle()
        if fill is not None and not ok:
            if f < 1.0:
                self.resting = True
                return self.melee_idle()
            aff = [o for o in opts if o[4]]
            fill = max(aff, key=lambda o: o[1] / o[2])[0] if aff else None
        if fill is not None:
            return self.cast_any(fill)
        return self.melee_idle()


def best_policy(run, modes=None):
    """run() -> core.run_many output under the current POLICY. Returns the best of `modes`
    (POLICIES when not given)."""
    best = None
    for mode in modes or POLICIES:
        POLICY["mode"], mage.POLICY["mode"] = mode, mode.partition("+")[0]
        try:
            out = run()
        finally:
            POLICY["mode"] = mage.POLICY["mode"] = "plan"
        if best is None or out["dps_mean"] > best["dps_mean"]:
            best = out
            best["mana_policy"] = mode
    return best


def simulate(spec, race, level, iterations, seed):
    talents = talents_at(spec, level)
    inputs = {}

    def build(sim):
        ch = core.Character(CLASS, race, level, talents)
        core.apply_passive_racials(ch, race)
        p = PriestSim(sim, ch, spec, level, talents, inputs)
        inputs["base_stats"] = ch.stats_tag
        p.start()

    out = best_policy(lambda: core.run_many(build, iterations, seed), policies_for(talents, spec))
    inputs["mana_policy_best_of"] = "A"
    out["inputs"] = dict(sorted(inputs.items()))
    for k in ("fight_seconds", "spell_hit_same_level", "spell_crit_mult", "base_spell_crit"):
        out["inputs"][k] = core.ASSUMPTIONS[k][1]
    return out
