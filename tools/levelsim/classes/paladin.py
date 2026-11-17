"""Paladin: Holy, Protection and Retribution, levels 1-60.

Talent orders: docs/guides/paladin/talents.md leveling builds
(Retribution (solo), Protection (dungeons), Holy (dungeon healer)); each ends in a 51-point build.

Talent values: the Forever client ships stale talent rows for most Paladin talents
(for example Conviction has 5 ranks of 5% in the client, 3 ranks of 2% in the game).
Talent values therefore come from the Forever tooltip text at max rank
(.research/talents/paladin.json, divided by max rank) and are tagged A.

Rotation (all specs, only abilities known at that level):
  1. Seal of the plan if missing or about to expire.
  2. Hammer of Wrath in the last 20% of the fight (target health assumed linear).
  3. Judgement on cooldown (Swift Judgement too, Protection).
  4. Holy Shock on cooldown (Holy, from 30).
  5. Holy Strike on cooldown.
  6. Unsealed Wrath (Retribution 40+): with 3 stored stacks, switch between Seal of Command
     and Seal of Righteousness so the next hit releases the 3 stored seal procs.
  7. Consecration.
  Auto-attack throughout. Holy and Protection are scored on this same damage rotation.

Mana (A): the Paladin runs out of mana in most cells, so the order above is not enough.
  - Seal upkeep and Holy Strike always come first (Holy Strike does several times more damage
    per mana than anything else, and the seal carries Judgement).
  - The other spells (Judgement, Hammer of Wrath, Holy Shock, the Unsealed Wrath twist,
    Consecration) are ranked by expected damage per mana (`Fight.rank_by_mana`). One of them is
    cast only with mana beyond what the seal, Holy Strike and the better-ranked spells need for
    the rest of the fight (`Fight.reserve`). Where Sanctified Judgement returns more mana than
    Judgement costs (3 ranks, Seal of Righteousness or Seal of Fury), Judgement is always cast.
  - The mana regeneration counted on is what the fight has regenerated so far, starting from an
    estimate (`Fight.regen_rate`).
  - 5-second rule: when the mana cannot keep a spell on cooldown to the end of the fight, the
    spell is cast only right after another one (normally Holy Strike), so the two share one
    5-second window. A cast on its own is counted with the regeneration it stops
    (`Fight.may`). Hammer of Wrath and the twist do not wait.
  Without these rules the Holy Shock talent lowered Holy DPS by 2.4% at level 60 (it does
  less than half the damage per mana of Judgement) and Improved Judgement lowered it by 1.2%
  (Judgements 8 s apart fall between Holy Strikes, so nothing regenerates in full).

Seal plans (A): keep Seal of Command up and twist (Unsealed Wrath), keep it up without twisting,
  stay on Seal of Righteousness, or stay on Seal of Fury. Which is best depends on the weapon
  and the mana the build has, so `simulate` runs each plan that applies and reports the best
  (`seal_plan`).
  Seal of Fury (level 10) adds a fixed Holy amount to each hit (its trigger spell, F), where
  Seal of Righteousness scales with weapon speed; its Judgement of Fury is the weaker one. The
  plan runs when the Fury hit is the larger one: with fast weapons and with the fist. Effect 2
  of each seal rank names its Judgement of Fury (F; ranks 1 and 2 are among the client's
  unlinked spells, `core.unlinked`), so the plan can start at level 10. The absorb shield and
  the taunt do nothing against the training target.

Not used: Exorcism and Holy Wrath (Undead/Demon targets only; the target is a training dummy),
Seal of the Crusader (would cost a GCD and seal uptime; small gain), Holy Shield and Reckoning
(no attacks against the paladin).
Hammer of the Righteous (level 40, one-hand weapon): the client gives Holy damage equal to
3 times the weapon's damage per second for 6% of base mana, on the cooldown category of Holy
Strike (2404, 6 s). Read as the weapon alone, in crafted gear it hits for 77 / 115 / 177 at
level 40 / 50 / 60, where Holy Strike hits for 108 / 151 / 256 at a quarter of the mana. Used
in place of Holy Strike it gains Holy 2 to 4 DPS for 8 to 12 mana per second (0.25 to 0.41
damage per mana, where the worst spell in the rotation gives 0.76 or more and the mana is
already short), and it loses DPS for Protection, whose Holy Strike has the same 6 s cooldown
(Shieldsworn). Retribution uses a two-hander and the naked character has no weapon. So it is
never the better button against one target; it is an area attack (up to 4 targets). Whether
the server adds attack power to "damage per second" is not in the client.

Server-side rules and values not in the client (tags):
  - Attack power = 2 x Strength + 3 x level - 20 (CU, Classic Paladin).
  - Seal of Righteousness per-hit damage: the tooltip range interpolated for a 2.0 s weapon (A).
  - Seal of Command: 7 procs per minute (CU), so 23.3% per 2.0 s swing.
  - Judgement of Command (F, rank 1 at every level): effect 2 of the talent's seal (20375, the
    only rank the talent has) names dummy spell 20425, whose effect names damage spell 20467:
    97 + 5.6 per level from 20 to its maximum level 28, coefficient 0.429 (`_judgement_of`).
    The Forever tooltip agrees ("136 to 148 if the target is stunned"). Half of it applies to
    a target that is not stunned (F, tooltip "$/2;"): 46 to 51 at level 20, 68 to 74 from 28.
    The client also has Judgement of Command ranks 2 to 5 (20963-20966: 153, 214, 274, 356
    base). Each is named only by a Seal of Command rank 2 to 5 (20915, 20918, 20919, 20920, at
    110 to 210 mana), and no trainer, talent or other spell gives a Paladin those seal ranks
    (they are among the unlinked spells). So they are not used: a Forever Paladin has the
    rank 1 seal at 60, and that seal judges with rank 1.
  - Consecration damage (F): the tooltip of each trained rank names its tick spell
    (1280345-1280349, unlinked): "$<tick>m1 * 8 Holy damage ... to enemies who enter the area.
    The first $s3 enemies ... take an additional $<tick>m2 * 8". The tick spell's first damage
    effect hits every enemy; its second, which carries the 0.042 coefficient, is the bonus for
    the first 4 enemies ($s3: effect 3 of the trained rank). Against the one training target
    both apply, so `consecration_tick` sums them: 2+4, 3+7, 6+11, 8+20, 12+27 per tick. One
    tick per second of the rank's 8 s, so 48/80/136/224/312 in total (Classic:
    64/120/192/280/384). 8 s cooldown (F).
  - Holy Shock (F): the cast spell of each rank carries the mana cost and the 10 s cooldown,
    the damage spell of the same level the damage: level 30 (1311606, 160 mana, 129 to 139),
    40 (the talent's own row, 225), 48 (20929, 275) and 56 (20930, 325). The level 30, 48 and
    56 cast spells and the level 30 damage spell are unlinked spells (`_holy_shock`).
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
import re

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


DUMMY = 3  # spell effect that only carries a value, here the id of another spell

TWO_HAND = {"axe2h", "sword2h", "mace2h", "polearm", "staff"}


# Seal plans. simulate() runs each one that applies (plans_for) and reports the best, because
# which is best depends on the weapon and the mana the build has (A).
PLANS = ("command_twist", "command", "righteousness", "fury")
SEAL_NAMES = {"SoR": "Seal of Righteousness", "SoC": "Seal of Command", "SoF": "Seal of Fury"}
FIVE_SECOND_RULE = 5.0  # seconds after a mana cost before full regeneration returns (CU)
REGEN_ESTIMATE_WEIGHT = 15.0  # seconds of fight the starting regeneration estimate counts for (A)


def _by_id(spell_id):
    """A client spell of the class: a trained or talent-linked one, else an unlinked one."""
    for s in core.data()["classes"][CLASS]["spells"]:
        if s["id"] == spell_id:
            return s
    return core.unlinked(CLASS, spell_id)


def _judgement_of(seal):
    """The Judgement damage spell of a seal rank (F), or None if the client data lacks it.

    Effect 2 of a seal carries a spell id. For Seal of Fury that is the damage spell; for Seal
    of Command it is a dummy spell whose effect carries the id of the damage spell."""
    ids = [int(e["EffectBasePointsF"]) for e in seal["effects"] if e.get("EffectIndex", 0) == 2]
    s = _by_id(ids[0]) if ids else None
    if s and not _has_dmg(s) and s["effects"] and s["effects"][0]["Effect"] == DUMMY:
        s = _by_id(int(s["effects"][0]["EffectBasePointsF"]))
    return s if s and _has_dmg(s) else None


def _holy_shock(level):
    """(cast spell, damage spell) of the Holy Shock rank a Paladin of `level` has, or None (F).

    The cast spell has the mana cost and the cooldown, the damage spell of the same level the
    damage. The level 40 cast spell is the talent's own row; the others are unlinked spells."""
    named = core.unlinked_named(CLASS, "Holy Shock")
    casts = [s for s in named if s["costs"]] + core.talent(CLASS, "Holy Shock")["ranks"]
    casts = sorted((s for s in casts if 0 < s["base_level"] <= level), key=lambda s: s["base_level"])
    if not casts:
        return None
    for s in core.ranks(CLASS, "Holy Shock") + named:
        if s["base_level"] == casts[-1]["base_level"] and _has_dmg(s):
            return casts[-1], s
    return None


def consecration_tick(spell):
    """(Holy damage, spell power coefficient) of one tick of a Consecration rank on one target,
    or None if the client data lacks it.

    The rank's tooltip names its tick spell ("$1280345m1 ... $1280345m2"). That spell has two
    damage effects: the first hits every enemy, the second is the bonus for the first enemies
    to enter (4 of them: effect 3 of the rank). The fight has one target, so both apply (F)."""
    named = re.search(r"\$(\d+)m1", spell["desc"])
    tick = core.unlinked(CLASS, int(named.group(1))) if named else None
    hits = [e for e in tick["effects"] if e["Effect"] == core.SCHOOL_DAMAGE] if tick else []
    if not hits:
        return None
    return sum(e["EffectBasePointsF"] for e in hits), sum(e["EffectBonusCoefficient"] for e in hits)


def _fury_hit(seal):
    """The per-hit Holy damage effect of a Seal of Fury rank (its trigger spell of the same name)."""
    for e in seal["effects"]:
        trig = e.get("trigger")
        if trig and trig["name"] == "Seal of Fury":
            return core.damage_effect(trig)
    return None


class Fight:
    def __init__(self, sim, spec, race, level, inputs, plan="command_twist"):
        self.sim, self.spec, self.level, self.inp = sim, spec, level, inputs
        self.plan = plan
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
        self.regen_seen = 0.0
        self.busy = 0.0
        self.cd = {}
        self.veng = (0, -1.0)  # stacks, expiry
        self.seal = None
        self.seal_exp = -1.0
        self.stored = (None, 0, -1.0)  # Unsealed Wrath: seal, stacks, expiry
        self.sor = _rank("Seal of Righteousness", level, lambda s: bool(s["costs"]))
        self.jor = _rank("Judgement of Righteousness", level)
        # Seal of Command: the one rank of the talent, and the Judgement that rank names (rank 1).
        self.soc = core.talent(CLASS, "Seal of Command")["ranks"][0] if ch.tr("Seal of Command") else None
        self.joc = _judgement_of(self.soc) if self.soc else None
        if plan in ("righteousness", "fury") or not self.joc:
            self.soc = None
        # Seal of Fury: the trained rank, its per-hit spell and the Judgement it names.
        self.sof = self.sof_hit = self.jof = None
        sof = _rank("Seal of Fury", level)
        if sof and _judgement_of(sof) and _fury_hit(sof):
            self.sof, self.sof_hit, self.jof = sof, _fury_hit(sof), _judgement_of(sof)
        self.main = "SoF" if plan == "fury" and self.sof else "SoC" if self.soc else "SoR"
        self.judgement = _rank("Judgement", level)
        self.hstrike = _rank("Holy Strike", level)
        self.consec = _rank("Consecration", level)
        self.consec_tick = consecration_tick(self.consec) if self.consec else None
        if self.consec_tick:
            period = next(e["EffectAuraPeriod"] for e in self.consec["effects"] if e["EffectAuraPeriod"])
            self.consec_ticks = int(self.consec["duration_ms"] / period)
            self.consec_period = period / 1000
            self.consec_cd = self.consec["category_cooldown_ms"] / 1000
        else:
            self.consec = None
        self.how = _rank("Hammer of Wrath", level)
        self.hshock_spell, self.hshock_rank = (ch.tr("Holy Shock") and _holy_shock(level)) or (None, None)
        self.hshock = bool(self.hshock_spell)
        self.unsealed = bool(ch.tr("Unsealed Wrath")) and plan == "command_twist"
        self.swift = bool(ch.tr("Swift Judgement"))
        inputs.update({"talents": "A (Forever tooltip)", "attack_power_formula": "CU", "unarmed_weapon": "CU",
                       "base_stats": ch.stats_tag, "mana_regen_spirit": "CU", "spell_ranks": "F",
                       "seal_of_righteousness_per_hit": "A", "blessing_of_might": "F"})
        self.rank_by_mana()

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
    def sor_hit(self):
        s = core.effect_value(self.sor["effects"][0], self.level, self.sor["spell_level"])
        per = s / 87 + (s / 25 - s / 87) * (self.speed - 1.5) / 2.3
        return per + self.sor["effects"][0]["EffectBonusCoefficient"] * self.ch.sp

    def fury_hit(self):
        e = self.sof_hit
        return core.effect_value(e, self.level, self.level) + e["EffectBonusCoefficient"] * self.ch.sp

    def seal_spell(self, which):
        return {"SoR": self.sor, "SoC": self.soc, "SoF": self.sof}[which]

    def judge_range(self, seal):
        """(low, high, coefficient) of the Judgement of a seal."""
        spell = {"SoC": self.joc, "SoF": self.jof, "SoR": self.jor}[seal]
        e = spell["effects"][0]
        lv = min(self.level, spell["max_level"]) if seal != "SoR" and spell["max_level"] else self.level
        lo, hi = core.effect_range(e, lv, spell["spell_level"])
        if seal == "SoC":  # the full amount needs a stunned target; the training target never is
            lo, hi = lo / 2, hi / 2
        return lo, hi, e["EffectBonusCoefficient"]

    def seal_proc(self, seal):
        imp = 1 + self.tv("Improved Seals") / 100
        if seal == "SoR":
            self.holy("Seal of Righteousness", self.sor_hit() * imp, roll=False)
        elif seal == "SoF":
            self.holy("Seal of Fury", self.fury_hit() * imp, roll=False)
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
        self.regen_seen += base * frac
        self.sim.at(self.t + 2, self.regen)

    def ready(self, k):
        return self.cd.get(k, 0) <= self.t + 1e-9

    def cast_seal(self, which):
        c = self.instant_cost(self.seal_spell(which))
        if self.mana < c:
            return False
        self.spend(c)
        self.seal, self.seal_exp = which, self.t + 30
        self.sim.cast(SEAL_NAMES[which])
        return True

    def judge(self, key):
        imp = 1 + self.tv("Improved Seals") / 100
        lo, hi, coef = self.judge_range(self.seal)
        self.holy("Judgement", (self.sim.rng.uniform(lo, hi) + coef * self.ch.sp) * imp)
        if self.ch.tr("Sanctified Judgement"):
            r = self.ch.tr("Sanctified Judgement")
            if self.sim.rng.chance(r / 3 * 100):
                self.mana += core.cost(self.seal_spell(self.seal), self.ch.base_mana)[1] * r * 0.2
        self.sim.cast(key)

    def act(self):
        if self.t < self.busy - 1e-9:
            return
        ch, t, gcd = self.ch, self.t, 1.5
        want = self.main
        # 1. seal
        if self.seal_exp - t < 1.5:
            if self.cast_seal(want if not (self.unsealed and self.seal_exp > t) else self.seal or want):
                return self.after(gcd)
        # 2. Hammer of Wrath (execute phase)
        if self.how and t >= 0.8 * self.sim.end and self.ready("how"):
            c = self.how_cost()
            if self.may("how", c):
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
            if self.may("judgement", c):
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
            c = self.hshock_cost()
            if self.may("hshock", c):
                self.spend(c)
                self.cd["hshock"] = t + self.hshock_cd()
                e = core.damage_effect(self.hshock_rank)
                lo, hi = core.effect_range(e, self.level, self.hshock_rank["spell_level"])
                self.sim.cast("Holy Shock")
                self.holy("Holy Shock", self.sim.rng.uniform(lo, hi) + e["EffectBonusCoefficient"] * ch.sp)
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
                if self.may("twist", self.instant_cost(self.seal_spell(other))):
                    self.cast_seal(other)
                    return self.after(gcd)
        # 7. Consecration
        if self.consec and self.ready("consec"):
            c = self.instant_cost(self.consec, self.tv("Holy Conduit"))
            if self.may("consec", c):
                self.spend(c)
                self.cd["consec"] = t + self.consec_cd
                base, coef = self.consec_tick
                for i in range(1, self.consec_ticks + 1):
                    self.sim.at(t + i * self.consec_period, self.holy, "Consecration", base + coef * ch.sp, False)
                self.sim.cast("Consecration")
                return self.after(gcd)
        # nothing: wake at the next cooldown or regen
        nxt = [v for v in self.cd.values() if v > t] + [t + 1.0, self.seal_exp - 1.4]
        if self.how and t < 0.8 * self.sim.end:
            nxt.append(0.8 * self.sim.end)
        self.sim.at(min(x for x in nxt if x > t + 1e-6), self.act)

    def hshock_cost(self):
        return self.instant_cost(self.hshock_spell)

    def hshock_cd(self):
        return self.hshock_spell["category_cooldown_ms"] / 1000

    def how_cost(self):
        return core.cost(self.how, self.ch.base_mana)[1] * (1 - self.tv("Holy Conduit") / 100)

    def rank_by_mana(self):
        """Expected damage per point of mana of each optional spell (A), best first.

        The Paladin runs out of mana in most cells, so a spell is cast only with mana beyond
        what the spells that do more damage per mana need for the rest of the fight (`reserve`).
        Seal upkeep and Holy Strike are always reserved: the seal carries Judgement, and Holy
        Strike does several times more damage per mana than anything else."""
        ch, sp = self.ch, self.ch.sp
        hit = min(99.0, core.A("spell_hit_same_level") + ch.hit) / 100
        avg = hit * (1 + ch.spell_crit / 100 * (core.A("spell_crit_mult") - 1))
        mean = lambda e, spell: sum(core.effect_range(e, self.level, spell["spell_level"])) / 2
        val = {}
        if self.judgement:
            lo, hi, coef = self.judge_range(self.main)
            r = ch.tr("Sanctified Judgement")
            back = r / 3 * core.cost(self.seal_spell(self.main), ch.base_mana)[1] * r * 0.2
            self.judge_net = self.instant_cost(self.judgement) - back
            val["judgement"] = (((lo + hi) / 2 + coef * sp) * (1 + self.tv("Improved Seals") / 100) * avg, self.judge_net)
        if self.hshock:
            e = core.damage_effect(self.hshock_rank)
            val["hshock"] = ((mean(e, self.hshock_rank) + e["EffectBonusCoefficient"] * sp) * avg, self.hshock_cost())
        if self.how:
            e = self.how["effects"][0]
            val["how"] = ((mean(e, self.how) + e["EffectBonusCoefficient"] * sp) * avg, self.how_cost())
        if self.unsealed and self.soc:
            # A twist releases 3 stored procs of the other seal: Seal of Command and
            # Seal of Righteousness in turn.
            trig = self.soc["effects"][0]["trigger"]["effects"][0]
            soc = self.white_dmg() * trig["EffectBasePointsF"] / 100 + trig["EffectBonusCoefficient"] * sp
            land = 1 - (max(0.0, core.A("melee_miss_same_level") - ch.hit) + core.A("dodge_same_level")) / 100
            soc *= 7 * self.speed / 60 * land * (1 + ch.melee_crit / 100 * (core.A("melee_crit_mult") - 1))
            self.twist_cost = (self.instant_cost(self.sor) + self.instant_cost(self.soc)) / 2
            val["twist"] = (1.5 * (soc + self.sor_hit()) * (1 + self.tv("Improved Seals") / 100), self.twist_cost)
        if self.consec:
            base, coef = self.consec_tick
            val["consec"] = (self.consec_ticks * (base + coef * sp), self.instant_cost(self.consec, self.tv("Holy Conduit")))
        self.per_mana = {k: (d / c if c > 0 else float("inf")) for k, (d, c) in val.items()}
        self.order = sorted(val, key=lambda k: -self.per_mana[k])

    def need(self, key, rem, extra=0.0):
        """Mana one optional spell uses in the remaining `rem` seconds if cast on cooldown
        (`extra`: more mana per cast)."""
        if key == "judgement":
            cd = self.judgement["cooldown_ms"] / 1000 - self.tv("Improved Judgement")
            return (self.judge_net + extra) * rem / max(1.5, cd)
        if key == "hshock":
            return (self.hshock_cost() + extra) * rem / self.hshock_cd()
        if key == "twist":  # after every third swing
            return self.twist_cost * rem / (3 * self.speed / self.ch.haste + 1.5)
        if key == "consec":
            return (self.instant_cost(self.consec, self.tv("Holy Conduit")) + extra) * rem / self.consec_cd
        end = self.sim.end  # Hammer of Wrath: the execute phase only
        window = min(rem, end - max(self.t, 0.8 * end))
        return self.how_cost() * (int(window / 6) + 1 if window > 0 else 0)

    def reserve(self, key):
        """Mana to keep back when casting optional spell `key`: what the rest of the fight needs
        for seal upkeep, Holy Strike and every optional spell with more damage per mana (A)."""
        t, end = self.t, self.sim.end
        rem = max(0.0, end - t)
        nxt = max(t, self.seal_exp - 1.5)  # seal upkeep: the casts still to come
        need = self.instant_cost(self.seal_spell(self.main)) * (int((end - nxt) / 28.5) + 1 if nxt < end else 0)
        if self.hstrike:
            need += self.instant_cost(self.hstrike) * rem / max(1.5, 10 - self.tv("Shieldsworn"))
        for k in self.order:
            if k == key:
                break
            need += self.need(k, rem)
        return max(0.0, need - self.regen_rate(key) * rem)

    def regen_rate(self, key):
        """Mana per second to count on for the rest of the fight (A): what the fight has
        regenerated so far. It starts from an estimate: Holy Strike and the optional spells
        chained onto it (1.5 s each) keep the 5-second rule running for part of each Holy Strike
        cooldown, the rest of the time regenerates in full."""
        chained = self.order.index(key) + 1 if self.hstrike else 0  # this spell and the better ones
        cycle = 10 - self.tv("Shieldsworn") if self.hstrike else self.judgement["cooldown_ms"] / 1000
        free = max(0.0, 1 - (FIVE_SECOND_RULE + 1.5 * chained) / cycle)
        kept = self.tv("Reverence") / 100
        estimate = (15 + self.ch.spi / 5) / 2 * (kept + (1 - kept) * free)
        return (estimate * REGEN_ESTIMATE_WEIGHT + self.regen_seen) / (REGEN_ESTIMATE_WEIGHT + self.t)

    def may(self, key, c):
        """Whether optional spell `key` (mana cost c) may be cast now."""
        if key == "judgement" and self.judge_net <= 0:
            return self.mana >= c  # Sanctified Judgement returns more than it costs here
        spare = self.mana - c - self.reserve(key)
        if spare < 0:
            return False
        if not self.hstrike or key in ("twist", "how"):
            return True  # the twist and the execute phase cannot wait
        # A cast on its own stops full regeneration for 5 s more (the 5-second rule).
        broken = FIVE_SECOND_RULE * (15 + self.ch.spi / 5) / 2 * (1 - self.tv("Reverence") / 100)
        if spare >= self.need(key, max(0.0, self.sim.end - self.t), broken):
            return True
        # Not enough mana to keep this spell on cooldown to the end: cast it only right after
        # another spell (one 5-second-rule window instead of two), unless Holy Strike is far away.
        return self.t - self.last_spend <= 1.5 + 1e-6 or self.cd.get("hstrike", 0) - self.t > FIVE_SECOND_RULE

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


def plans_for(spec, race, level):
    """The seal plans worth running for a cell."""
    t = talents_at(spec, level)
    plans = list(PLANS[:3] if t.get("Seal of Command") else PLANS[2:3])
    if "command" in plans and not t.get("Unsealed Wrath"):
        plans.remove("command_twist")  # without the talent it is the same as "command"
    f = Fight(None, spec, race, level, {}, "fury")
    if f.sof and f.fury_hit() > f.sor_hit():  # its Judgement is the weaker one, so it needs the stronger hit
        plans.append("fury")
    return plans


def simulate(spec, race, level, iterations, seed):
    inputs = {}

    plans = plans_for(spec, race, level)
    r = None
    for plan in plans:
        def build(sim, plan=plan):
            Fight(sim, spec, race, level, inputs, plan).start()
        out = core.run_many(build, iterations, seed)
        if r is None or out["dps_mean"] > r["dps_mean"]:
            r = out
            r["seal_plan"] = plan
    if len(plans) > 1:
        inputs["seal_plan_best_of"] = "A"
    inputs.update({"sor_seal_of_command_ppm": "CU", "judgement_of_command": "F (rank 1, the talent's seal)",
                   "consecration_damage": "F", "holy_shock_ranks": "F",
                   "damage_per_mana_reserve": "A", "five_second_rule_chaining": "A", "seal_of_fury": "F",
                   "holy_strike_cooldown": "A", "hammer_of_wrath_cooldown": "CU", "fight_seconds": "A"})
    r["inputs"] = inputs
    return r
