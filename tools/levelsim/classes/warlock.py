"""Warlock: level-aware DPS for Affliction, Demonology and Destruction.

Spell values come from forever.json through core (ranks, effect base points,
per-level growth capped at the rank's max level, costs, cast times, cooldowns).

Talent values: the Forever client stores effect rows for rank 1 only, and for
many talents that rank-1 row holds the *max-rank* value (Suppression 5,
Improved Corruption 10%, Shadow Mastery 2...), or the talent is missing from the
client tree entirely (Pandemic, Malevolence, Demonic Knowledge, Shadow and
Flame, ...). `core.talent_points` would scale those wrongly, so every talent
value here is the per-rank value from the live talent tooltips
(.research/talents/warlock.json, rank 1 and max rank text), tag F (tooltip).

Server-side behaviour and assumptions (tag in `inputs`):
- Pets are not in the client. Imp Firebolt and Succubus Lash of Pain use Classic
  rank values (CU). Demon melee is a generic level-scaled hit (A, scaled from
  the level-60 tools/sim generic pet: 100 avg per 2.0 s swing at 60).
- Pet is summoned before the pull (A). Imp 1-9, Voidwalker 10-19, Succubus 20+
  (best damage of the demons); Destruction switches back to the Imp at 58 for
  Improved Imp. Demonology from 40 sacrifices the Succubus (+15% Fire) and
  keeps the Imp out with Demonic Pact, as in its raid build. The Felhunter
  (30) has no damage spell and is never the best choice.
- Soul shards are not limited (A): the fight starts with a full bag.
- Life Tap health is not limited (A, single 3-minute fight, no healing model).
- Mana regen: Classic warlock 8 + Spirit/5 per 2 s tick, only after 5 s
  without spending mana (CU).
- Periodic damage can crit (A: Pandemic raises the crit bonus of DoTs, so
  Forever DoTs crit).
- Wrack: client text, other Affliction DoTs tick 100% faster while it channels.
- Bane of Agony: total damage spread evenly over its ticks (the Classic ramp
  has the same total).
- No target health: execute effects (Decimation, Shadowburn shard on kill,
  Drain Soul kill) do nothing. AoE spells (Rain of Fire, Hellfire) are unused.
- Gear (core.GEAR "crafted", gear.py): Int/Spi/hit/crit come through core.Character;
  gear spell damage (generic + the spell's school) adds to the warlock's own spells
  through each spell's coefficient (F (crafted items)). Pets do not gain the warlock's
  gear spell damage (C).
"""
import core

CLASS = "warlock"
SPECS = {"affliction": "Affliction", "demonology": "Demonology", "destruction": "Destruction"}

# Leveling order (talent, points) ending in the level 60 raid build of docs/guides/warlock/talents.md.
ORDER = {
    # Affliction: Wrack (raid) 33/0/18. Wrack is the 31st point (level 40, when the spell unlocks).
    "affliction": [("Improved Corruption", 5), ("Suppression", 5), ("Pandemic", 3), ("Amplify Curse", 1),
                   ("Improved Life Tap", 1), ("Malevolence", 5), ("Siphon Life", 1), ("Soul Siphon", 3),
                   ("Nightfall", 1), ("Shadow Mastery", 5), ("Wrack", 1), ("Nightfall", 1), ("Improved Life Tap", 1),
                   ("Improved Shadow Bolt", 5), ("Bane", 5), ("Cataclysm", 3), ("Ruin", 5)],
    # Demonology: Fire (raid) 2/31/18.
    "demonology": [("Unholy Power", 5), ("Demonic Energies", 2), ("Fel Vitality", 3), ("Improved Imp", 3),
                   ("Master Summoner", 2), ("Demonic Sacrifice", 1), ("Demonic Brand", 3), ("Decimation", 2),
                   ("Soul Link", 1), ("Demonic Knowledge", 3), ("Master Demonologist", 5), ("Demonic Pact", 1),
                   ("Bane", 5), ("Cataclysm", 3), ("Aftermath", 2), ("Ruin", 5), ("Agonizing Flames", 3),
                   ("Improved Life Tap", 2)],
    # Destruction: raid and dungeons 14/4/33 (guide leveling route to 42, then the raid off-tree points).
    "destruction": [("Bane", 5), ("Cataclysm", 3), ("Aftermath", 2), ("Shadowburn", 1), ("Aftermath", 3),
                    ("Ruin", 1), ("Conflagrate", 1), ("Ruin", 2), ("Agonizing Flames", 3), ("Bane of Havoc", 1),
                    ("Fire and Brimstone", 3), ("Shadow and Flame", 5), ("Incinerate", 1), ("Ruin", 2),
                    ("Improved Corruption", 5), ("Suppression", 5), ("Improved Life Tap", 2), ("Pandemic", 2),
                    ("Unholy Power", 4)],
}

# Per-rank talent values from the live tooltips (rank 1 / max rank text). Tag F.
TT = {
    "Suppression": 1.0,               # % hit
    "Improved Corruption": (0.4, 0.02),  # cast -s, +dmg
    "Improved Life Tap": 0.10,
    "Pandemic": 1.0 / 3,               # +crit bonus fraction (100% at 3/3)
    "Malevolence": 1.0,                # % Shadow crit
    "Nightfall": 2.0,                  # % Shadow Trance chance
    "Soul Siphon": 0.04,               # per other Affliction effect (12% at 3/3, cap 36%)
    "Shadow Mastery": 0.02,
    "Improved Bane of Agony": 0.05,
    "Improved Drains": 0.20 / 3,
    "Amplify Curse": 0.50,
    "Improved Shadow Bolt": 0.04,      # Shadow taken for 12 s
    "Bane": (0.1, 0.4),                # SB/Immolate/Incinerate, Soul Fire cast -s
    "Cataclysm": 0.10 / 3,
    "Aftermath": 0.10,                 # Immolate initial damage
    "Ruin": 0.20,                      # crit bonus fraction (100% at 5/5)
    "Agonizing Flames": (10.0 / 3, 0.10 / 3),  # Searing Pain crit %, Destruction damage
    "Fire and Brimstone": 25.0 / 3,    # Conflagrate crit %
    "Shadow and Flame": 0.04,          # +dmg buff and 20%/rank Immolate not consumed
    "Unholy Power": 0.02,
    "Improved Imp": 0.10,
    "Improved Sayaad": 0.10,
    "Fel Vitality": 0.05,              # player max mana
    "Demonic Knowledge": 1.0 / 3,      # spell damage = level * this * rank
    "Master Demonologist": 0.02,
    "Soul Link": 0.03,
    "Demonic Sacrifice": 0.15,
    "Demonic Brand": 2,                # pet attacks branded per rank (6 at 3/3)
}

DESTRUCTION = {"Shadow Bolt", "Immolate", "Searing Pain", "Soul Fire", "Shadowburn", "Conflagrate", "Incinerate"}
DOT_CRIT_PANDEMIC = {"Corruption", "Bane of Agony", "Bane of Doom", "Drain Life", "Siphon Life", "Wrack"}

# Pets (not in the client). Classic ranks: (learned level, min, max).
FIREBOLT = [(1, 7, 10), (8, 14, 17), (18, 25, 29), (28, 36, 41), (38, 52, 59), (48, 68, 77), (58, 83, 97)]
LASH = [(20, 33), (28, 44), (36, 60), (44, 73), (52, 87), (60, 99)]
DEMON_MELEE = {"imp": 0.0, "voidwalker": 0.8, "succubus": 1.0, "felhunter": 0.9}
PET_HIT_PER_LEVEL = 100 / 60  # generic pet melee average hit per level, 2.0 s swing (A)


def talents_at(spec, level):
    pts, out = max(0, min(level, 60) - 9), {}
    for name, n in ORDER[spec]:
        for _ in range(n):
            if pts <= 0:
                return out
            out[name] = out.get(name, 0) + 1
            pts -= 1
    return out


def pet_for(spec, level):
    """(active pet, sacrificed pet or None)."""
    if spec == "demonology" and level >= 40:
        return "imp", "succubus"
    if level < 10:
        return "imp", None
    if level < 20:
        return "voidwalker", None
    if spec == "destruction" and level >= 58:
        return "imp", None
    return "succubus", None


class Warlock:
    def __init__(self, sim, spec, race, level):
        self.sim, self.spec, self.level = sim, spec, level
        self.t_ = talents_at(spec, level)
        self.ch = core.Character(CLASS, race, level, self.t_)
        core.apply_passive_racials(self.ch, race)
        self.race = race
        self.inp = {"base_stats": self.ch.stats_tag, "talents": "F", "pet_melee": "A", "imp_firebolt": "CU",
                    "lash_of_pain": "CU", "mana_regen": "CU", "unlimited_shards_and_health": "A", "dot_crit": "A"}
        self.ch.hit += self.tr("Suppression") * TT["Suppression"]
        self.max_mana = self.ch.mana() * (1 + self.tr("Fel Vitality") * TT["Fel Vitality"])
        self.mana = self.max_mana
        self.last_spend = -10.0
        self.pet, self.sacrificed = pet_for(spec, level)
        self.inp["pet"] = "A"
        self.sp = level * TT["Demonic Knowledge"] * self.tr("Demonic Knowledge") if self.pet else 0.0
        if self.ch.gear:
            self.inp["gear"] = "F (crafted items)"
        self.buffs = {}
        self.dots = {}
        self.cds = {}
        self.racial = core.racial_cooldown(race)
        self.trance = False
        self.amplify_ready = self.tr("Amplify Curse") > 0
        self.brand = 0
        self.wrack_until = -1.0

    def tr(self, n):
        return self.t_.get(n, 0)

    def spell(self, name):
        if name in ("Siphon Life", "Shadowburn", "Conflagrate", "Incinerate", "Wrack") and not self.tr(name):
            return None
        return core.best_rank(CLASS, name, self.level)

    def val(self, s, e):
        lv = min(self.level, s["max_level"]) if s["max_level"] else self.level
        return core.effect_value(e, lv, s["spell_level"]), core.effect_range(e, lv, s["spell_level"])

    def up(self, k):
        return self.buffs.get(k, -1) > self.sim.t

    # ---------- multipliers ----------
    def mult(self, name, school, pet=False):
        m = 1.0
        if self.racial and self.racial[0] == "power" and self.up("racial"):
            m *= 1 + self.racial[1] / 100
        if self.tr("Soul Link") and self.pet:
            m *= 1 + TT["Soul Link"]
        if school == "shadow":
            m *= 1 + self.tr("Shadow Mastery") * TT["Shadow Mastery"]
            if self.up("isb"):
                m *= 1 + self.tr("Improved Shadow Bolt") * TT["Improved Shadow Bolt"]
            if self.up("sf_shadow"):
                m *= 1 + self.tr("Shadow and Flame") * TT["Shadow and Flame"]
            if self.pet == "succubus":
                m *= 1 + self.tr("Master Demonologist") * TT["Master Demonologist"]
            if self.sacrificed == "imp" and self.tr("Demonic Sacrifice"):
                m *= 1 + TT["Demonic Sacrifice"]
        if school == "fire":
            if self.up("sf_fire"):
                m *= 1 + self.tr("Shadow and Flame") * TT["Shadow and Flame"]
            if self.pet == "imp":
                m *= 1 + self.tr("Master Demonologist") * TT["Master Demonologist"]
            if self.sacrificed == "succubus" and self.tr("Demonic Sacrifice"):
                m *= 1 + TT["Demonic Sacrifice"]
        if name in DESTRUCTION:
            m *= 1 + self.tr("Agonizing Flames") * TT["Agonizing Flames"][1]
        if name == "Corruption":
            m *= 1 + self.tr("Improved Corruption") * TT["Improved Corruption"][1]
        if name == "Bane of Agony":
            m *= 1 + self.tr("Improved Bane of Agony") * TT["Improved Bane of Agony"]
        if name in ("Drain Life", "Wrack"):
            if name == "Drain Life":
                m *= 1 + self.tr("Improved Drains") * TT["Improved Drains"]
            n = sum(1 for d in ("Corruption", "Siphon Life", "Bane of Agony") if self.dot_up(d))
            m *= 1 + n * self.tr("Soul Siphon") * TT["Soul Siphon"]
        return m

    def crit_chance(self, name, school):
        c = self.ch.spell_crit
        if school == "shadow":
            c += self.tr("Malevolence") * TT["Malevolence"]
        if name == "Searing Pain":
            c += self.tr("Agonizing Flames") * TT["Agonizing Flames"][0]
        if name == "Conflagrate":
            c += self.tr("Fire and Brimstone") * TT["Fire and Brimstone"]
        if self.racial and self.racial[0] == "crit" and self.up("racial"):
            c += self.racial[1]
        return c

    def crit_mult(self, name):
        bonus = core.A("spell_crit_mult") - 1
        f = 1.0
        if name in DESTRUCTION:
            f += self.tr("Ruin") * TT["Ruin"]
        if name in DOT_CRIT_PANDEMIC:
            f += self.tr("Pandemic") * TT["Pandemic"]
        return 1 + bonus * f

    def spw(self, school):
        """Spell power for the warlock's own spells: Demonic Knowledge plus gear."""
        return self.sp + self.ch.gear_sp(school)

    def school(self, s):
        return core.SCHOOLS.get(s["school_mask"], "shadow")

    # ---------- resources ----------
    def spend(self, amount):
        if amount > 0:
            self.mana -= amount
            self.last_spend = self.sim.t

    def regen(self):
        if self.sim.t - self.last_spend >= 5:
            self.mana = min(self.max_mana, self.mana + 8 + self.ch.spi / 5)
        self.sim.at(self.sim.t + 2, self.regen)

    def mana_cost(self, s):
        _, c = core.cost(s, self.ch.base_mana)
        if s["name"] in DESTRUCTION:
            c *= 1 - self.tr("Cataclysm") * TT["Cataclysm"]
        return c

    def haste(self):
        h = self.ch.haste
        if self.racial and self.racial[0] == "haste" and self.up("racial"):
            h *= 1 + self.racial[1] / 100
        return h

    def cast_time(self, s):
        c = max(0, s["cast_ms"]) / 1000
        n = s["name"]
        if n in ("Shadow Bolt", "Immolate", "Incinerate"):
            c -= self.tr("Bane") * TT["Bane"][0]
        if n == "Soul Fire":
            c -= self.tr("Bane") * TT["Bane"][1]
        if n == "Corruption":
            c -= self.tr("Improved Corruption") * TT["Improved Corruption"][0]
        if n == "Shadow Bolt" and self.trance:
            c = 0
        return max(0.0, c) / self.haste()

    def gcd(self):
        return max(1.0, 1.5 / self.haste())

    # ---------- damage ----------
    def direct(self, name, s, e, school, extra=1.0):
        rng = self.sim.rng
        out = core.spell_roll(rng, self.ch, self.crit_chance(name, school))
        self.sim.cast(name)
        if out == "miss":
            return out
        _, (lo, hi) = self.val(s, e)
        amt = (rng.uniform(lo, hi) + self.spw(school) * (e.get("EffectBonusCoefficient") or 0)) * self.mult(name, school) * extra
        if self.racial and self.racial[0] == "direct" and self.up("racial"):
            amt *= 1 + self.racial[1] / 100
        if out == "crit":
            amt *= self.crit_mult(name)
        self.sim.deal(name, amt)
        return out

    def dot_up(self, name, margin=0.0):
        d = self.dots.get(name)
        return bool(d) and d["end"] > self.sim.t + margin

    def apply_dot(self, name, s, e, school, scale=1.0):
        period = (e.get("EffectAuraPeriod") or 3000) / 1000
        ticks = max(1, round(s["duration_ms"] / 1000 / period))
        tick, _ = self.val(s, e)
        tick = (tick + self.spw(school) * (e.get("EffectBonusCoefficient") or 0)) * scale
        gen = self.dots.get(name, {}).get("gen", 0) + 1
        self.dots[name] = {"gen": gen, "left": ticks, "tick": tick, "period": period, "school": school,
                           "end": self.sim.t + ticks * period}
        self.sim.at(self.sim.t + self.tick_delay(name, period), self.dot_tick, name, gen)

    def tick_delay(self, name, period):
        if name in ("Corruption", "Siphon Life", "Bane of Agony") and self.wrack_until > self.sim.t:
            return period / 2
        return period

    def dot_tick(self, name, gen):
        d = self.dots.get(name)
        if not d or d["gen"] != gen or d["left"] <= 0:
            return
        d["left"] -= 1
        amt = d["tick"] * self.mult(name, d["school"])
        if self.sim.rng.chance(self.crit_chance(name, d["school"])):
            amt *= self.crit_mult(name)
        self.sim.deal(name, amt)
        if name == "Corruption" and self.tr("Nightfall") and self.sim.rng.chance(self.tr("Nightfall") * TT["Nightfall"]):
            self.trance = True
        if d["left"] > 0:
            delay = self.tick_delay(name, d["period"])
            d["end"] = self.sim.t + d["left"] * delay
            self.sim.at(self.sim.t + delay, self.dot_tick, name, gen)
        else:
            d["end"] = self.sim.t

    # ---------- pets ----------
    def pet_mult(self, school):
        m = 1 + self.tr("Unholy Power") * TT["Unholy Power"]
        if self.race == "orc":
            m *= 1 + core.RACIALS["orc"].get("pet", 0) / 100
        if self.tr("Soul Link"):
            m *= 1 + TT["Soul Link"]
        if self.pet == "imp" and school == "fire":
            m *= (1 + self.tr("Master Demonologist") * TT["Master Demonologist"]) * (1 + self.tr("Improved Imp") * TT["Improved Imp"])
        if self.pet == "succubus" and school == "shadow":
            m *= 1 + self.tr("Master Demonologist") * TT["Master Demonologist"]
        return m

    def brand_hit(self):
        if self.brand > 0 and self.up("brand"):
            self.brand -= 1
            k = self.level / 60  # scale the level-60 tooltip value (A)
            school = "shadow" if self.pet == "succubus" else "fire"
            amt = (self.sim.rng.uniform(65, 68) * k + 0.078 * self.sp) * self.pet_mult(school)
            self.sim.deal("Pet: Demonic Brand", amt)

    def imp_cast(self):
        rk = [r for r in FIREBOLT if r[0] <= self.level][-1]
        if core.spell_roll(self.sim.rng, _PetStats(), 0) != "miss":
            amt = (self.sim.rng.uniform(rk[1], rk[2]) + self.sp * 2.0 / 3.5) * self.pet_mult("fire")
            if self.sim.rng.chance(5.0):
                amt *= core.A("spell_crit_mult")
            self.sim.deal("Imp: Firebolt", amt)
            self.brand_hit()
        self.sim.at(self.sim.t + 2.0, self.imp_cast)

    def demon_swing(self):
        out = core.melee_roll(self.sim.rng, _PetStats(), white=True)
        if out not in ("miss", "dodge"):
            amt = PET_HIT_PER_LEVEL * self.level * DEMON_MELEE[self.pet] * self.sim.rng.uniform(0.85, 1.15)
            amt *= {"glance": core.A("glance_damage"), "crit": core.A("melee_crit_mult")}.get(out, 1.0)
            self.sim.deal(f"{self.pet.title()}: melee", amt * self.pet_mult("physical"))
            self.brand_hit()
        self.sim.at(self.sim.t + 2.0, self.demon_swing)

    def lash(self):
        rk = [r for r in LASH if r[0] <= self.level][-1]
        if core.spell_roll(self.sim.rng, _PetStats(), 0) != "miss":
            amt = (rk[1] + self.sp * 1.5 / 3.5) * (1 + self.tr("Improved Sayaad") * TT["Improved Sayaad"]) * self.pet_mult("shadow")
            if self.sim.rng.chance(5.0):
                amt *= core.A("spell_crit_mult")
            self.sim.deal("Succubus: Lash of Pain", amt)
        self.sim.at(self.sim.t + 12.0, self.lash)

    # ---------- rotation ----------
    def start(self):
        self.sim.at(0.0, self.regen)
        if self.pet == "imp":
            self.sim.at(0.0, self.imp_cast)
        elif self.pet:
            self.sim.at(0.5, self.demon_swing)
            if self.pet == "succubus" and self.level >= 20:
                self.sim.at(1.0, self.lash)
        self.sim.at(0.0, self.act)

    def ready(self, name):
        return self.cds.get(name, -1) <= self.sim.t

    def filler_value(self, name):
        """Expected damage per second of cast time for choosing the filler."""
        s = self.spell(name)
        if not s:
            return None, 0
        school = self.school(s)
        e = core.damage_effect(s)
        if name == "Wrack":
            per, _ = self.val(s, e)
            ticks = s["duration_ms"] / 1000
            dot_bonus = sum(d["tick"] / d["period"] for k, d in self.dots.items()
                            if k in ("Corruption", "Siphon Life", "Bane of Agony") and self.dot_up(k))
            return s, (per * self.mult(name, school) + dot_bonus)
        if name == "Drain Life":
            per, _ = self.val(s, e)
            return s, per / ((e.get("EffectAuraPeriod") or 1000) / 1000) * self.mult(name, school)
        avg, _ = self.val(s, e)
        crit = min(100, self.crit_chance(name, school)) / 100
        dmg = avg * self.mult(name, school) * (1 + crit * (self.crit_mult(name) - 1))
        if name == "Incinerate" and self.dot_up("Immolate"):
            dmg *= 1 + s["effects"][1]["EffectBasePointsF"] / 100
        v = dmg / max(self.gcd(), self.cast_time(s))
        if name == "Searing Pain" and self.tr("Demonic Brand") and self.pet:
            # Searing Pain as filler keeps the pet branded: count that pet damage too.
            v += (66.5 * self.level / 60 + 0.078 * self.sp) * self.pet_mult("fire") / 2.0
        return s, v

    def choose(self):
        """Priority list limited to spells known at this level."""
        t, remain = self.sim.t, self.sim.end - self.sim.t
        if self.racial and self.ready("racial"):
            return ("racial", None)
        if self.trance and self.spell("Shadow Bolt"):
            return ("Shadow Bolt", self.spell("Shadow Bolt"))
        for name in ("Death Coil", "Shadowburn"):
            s = self.spell(name)
            if s and self.ready(name):
                return (name, s)
        if self.spell("Conflagrate") and self.ready("Conflagrate") and self.dot_up("Immolate"):
            return ("Conflagrate", self.spell("Conflagrate"))
        bane = "Bane of Doom" if self.spec != "affliction" and self.spell("Bane of Doom") and remain >= 60 else "Bane of Agony"
        dots = [bane, "Corruption", "Siphon Life", "Immolate"]
        for name in dots:
            s = self.spell(name)
            if not s:
                continue
            ct = self.cast_time(s)
            if name == "Bane of Doom" and not self.ready(name):
                continue
            if not self.dot_up(name, ct) and remain > s["duration_ms"] / 2000 + ct:
                if name == "Bane of Doom" and self.dot_up("Bane of Agony"):
                    continue
                if name == "Bane of Agony" and self.dot_up("Bane of Doom"):
                    continue
                return (name, s)
        if self.spell("Soul Fire") and self.ready("Soul Fire"):
            return ("Soul Fire", self.spell("Soul Fire"))
        best, bv = None, 0
        for name in ("Shadow Bolt", "Searing Pain", "Incinerate", "Drain Life", "Wrack"):
            s, v = self.filler_value(name)
            if s and v > bv:
                best, bv = (name, s), v
        return best

    def act(self):
        sim = self.sim
        if sim.t >= sim.end:
            return
        pick = self.choose()
        if not pick:
            sim.at(sim.t + 1.0, self.act)
            return
        name, s = pick
        if name == "racial":
            self.buffs["racial"] = sim.t + self.racial[2]
            self.cds["racial"] = sim.t + self.racial[3]
            sim.at(sim.t, self.act)
            return
        cost = self.mana_cost(s)
        if cost > self.mana:
            lt = self.spell("Life Tap")
            if lt:
                gain, _ = self.val(lt, lt["effects"][0])
                gain = (gain + self.ch.spi) * (1 + self.tr("Improved Life Tap") * TT["Improved Life Tap"])
                self.mana = min(self.max_mana, self.mana + gain)
                sim.cast("Life Tap")
                sim.at(sim.t + self.gcd(), self.act)
            else:
                sim.at(sim.t + 1.0, self.act)  # wait for regen
            return
        self.spend(cost)
        ct = self.cast_time(s)
        if name in ("Drain Life", "Wrack"):
            ct = s["duration_ms"] / 1000
        cd = max(s["cooldown_ms"], s["category_cooldown_ms"]) / 1000
        if cd:
            self.cds[name] = sim.t + cd
        if name == "Wrack":
            self.wrack_until = sim.t + ct
            self.start_channel(name, s, ct)
        elif name == "Drain Life":
            self.start_channel(name, s, ct)
        else:
            sim.at(sim.t + ct, self.land, name, s)
        sim.at(sim.t + max(ct, self.gcd()), self.act)

    def start_channel(self, name, s, dur):
        e = core.damage_effect(s)
        per = (e.get("EffectAuraPeriod") or 1000) / 1000
        n = int(round(dur / per))
        if core.spell_roll(self.sim.rng, self.ch) == "miss":
            self.sim.cast(name)
            return
        self.sim.cast(name)
        tick, _ = self.val(s, e)
        tick += self.spw(self.school(s)) * (e.get("EffectBonusCoefficient") or 0)
        for i in range(1, n + 1):
            self.sim.at(self.sim.t + i * per, self.channel_tick, name, tick, "shadow")

    def channel_tick(self, name, tick, school):
        amt = tick * self.mult(name, school)
        if self.sim.rng.chance(self.crit_chance(name, school)):
            amt *= self.crit_mult(name)
        self.sim.deal(name, amt)
        if self.tr("Nightfall") and self.sim.rng.chance(self.tr("Nightfall") * TT["Nightfall"]):
            self.trance = True

    def land(self, name, s):
        school = self.school(s)
        if name == "Shadow Bolt":
            self.trance = False
            out = self.direct(name, s, core.damage_effect(s), school)
            if out == "crit" and self.tr("Improved Shadow Bolt"):
                self.buffs["isb"] = self.sim.t + 12
        elif name == "Immolate":
            if core.spell_roll(self.sim.rng, self.ch) == "miss":
                self.sim.cast(name)
                return
            de = [e for e in s["effects"] if e["Effect"] == core.SCHOOL_DAMAGE][0]
            self.direct(name, s, de, school, 1 + self.tr("Aftermath") * TT["Aftermath"])
            self.apply_dot(name, s, core.damage_effect(s), school)
        elif name in ("Corruption", "Bane of Agony", "Siphon Life", "Bane of Doom"):
            self.sim.cast(name)
            if core.spell_roll(self.sim.rng, self.ch) == "miss":
                return
            scale = 1.0
            if name == "Bane of Agony" and self.amplify_ready:
                scale, self.amplify_ready = 1 + TT["Amplify Curse"], False
                self.sim.at(self.sim.t + 180, self._amplify)
            if name in ("Bane of Agony", "Bane of Doom"):
                self.dots.pop("Bane of Doom" if name == "Bane of Agony" else "Bane of Agony", None)
            self.apply_dot(name, s, core.damage_effect(s), school, scale)
        elif name == "Conflagrate":
            self.direct(name, s, core.damage_effect(s), school)
            if self.tr("Shadow and Flame"):
                self.buffs["sf_shadow"] = self.sim.t + 20
            if not self.sim.rng.chance(self.tr("Shadow and Flame") * 20):
                self.dots.pop("Immolate", None)
        elif name == "Shadowburn":
            de = [e for e in s["effects"] if e["Effect"] == core.SCHOOL_DAMAGE][0]
            self.direct(name, s, de, school)
            if self.tr("Shadow and Flame"):
                self.buffs["sf_fire"] = self.sim.t + 20
        elif name == "Death Coil":
            e = [e for e in s["effects"] if e["EffectIndex"] == 0][0]
            self.direct(name, s, e, school)
        elif name == "Incinerate":
            extra = 1 + (s["effects"][1]["EffectBasePointsF"] / 100 if self.dot_up("Immolate") else 0)
            self.direct(name, s, core.damage_effect(s), school, extra)
        elif name == "Searing Pain":
            out = self.direct(name, s, core.damage_effect(s), school)
            if out != "miss" and self.tr("Demonic Brand") and self.pet:
                self.brand = TT["Demonic Brand"] * self.tr("Demonic Brand")
                self.buffs["brand"] = self.sim.t + 10
        else:
            self.direct(name, s, core.damage_effect(s), school)

    def _amplify(self):
        self.amplify_ready = True


class _PetStats:
    """Pet attack table input: no hit bonus, 5% crit (Classic pet base, CU)."""
    hit = 0.0
    melee_crit = 5.0
    spell_crit = 5.0


def simulate(spec, race, level, iterations=200, seed=1):
    holder = {}

    def build(sim):
        w = Warlock(sim, spec, race, level)
        w.start()
        holder["w"] = w

    out = core.run_many(build, iterations, seed)
    w = holder["w"]
    out["inputs"] = dict(w.inp)
    out["pet"] = w.pet
    out["sacrificed"] = w.sacrificed
    return out
