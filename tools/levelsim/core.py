"""Level-aware DPS simulator core for WoW Forever.

Shared by every class module in tools/levelsim/classes/. Pure standard library.

Scope (as requested): no gear and no enemy defenses beyond a level-matched
training target. A "naked" character of a given class, race and level, with
every spell rank and talent point available at that level, fights a target of
the same level for a fixed time. The result is the character's own DPS.

Data: tools/forever_data/forever.json (Forever client DB2, see build.py).
Anything the client does not contain is in ASSUMPTIONS below, each with a tag:
  F  = Forever client data      C  = Classic value (documented source)
  CU = Classic value, unchecked A  = assumption for this simulator
"""
import heapq
import json
import math
import random
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "tools" / "forever_data" / "forever.json"
BASE_STATS_PATH = Path(__file__).resolve().parent / "base_stats.json"

# Effect type ids (client SpellEffect.Effect)
SCHOOL_DAMAGE, DUMMY, APPLY_AURA, WEAPON_DAMAGE_NOSCHOOL, WEAPON_PERCENT_DAMAGE, NORMALIZED_WEAPON_DMG, WEAPON_DAMAGE = 2, 3, 6, 17, 31, 121, 58
# Aura type ids (client SpellEffect.EffectAura)
PERIODIC_DAMAGE, PERIODIC_LEECH = 3, 53
SCHOOLS = {1: "physical", 2: "holy", 4: "fire", 8: "nature", 16: "frost", 32: "shadow", 64: "arcane"}

ASSUMPTIONS = {
    "fight_seconds": (180, "A", "Fight length"),
    "target_level_delta": (0, "A", "Target level minus player level (no enemy defenses requested)"),
    "target_armor": (0, "A", "Target armor (no enemy defenses requested)"),
    "melee_miss_same_level": (5.0, "C", "Melee miss vs same-level target, % (warcraft.wiki.gg Hit)"),
    "dw_miss_penalty": (19.0, "C", "Extra white miss when dual wielding, %"),
    "dodge_same_level": (5.0, "CU", "Target dodge vs same level, % (attacks from behind: no parry/block)"),
    "glance_same_level": (10.0, "CU", "White hits that glance vs same level, %"),
    "glance_damage": (0.95, "CU", "Glancing damage multiplier vs same level"),
    "spell_hit_same_level": (96.0, "C", "Spell hit vs same-level target, %"),
    "melee_crit_mult": (2.0, "CU", "Melee/ranged crit multiplier"),
    "spell_crit_mult": (1.5, "CU", "Spell crit multiplier"),
    "base_spell_crit": (0.0, "A", "Base spell crit before Intellect, % (class-specific values are server-side)"),
    "energy_per_sec": (10.0, "CU", "Rogue/cat energy regen"),
    "unarmed": (True, "A", "No gear: melee uses the unarmed fist (level-scaled damage, 2.0 speed)"),
}


# Gear mode: "none" (naked) or "crafted" (best craftable gear, gear.py). Set by run.py.
GEAR = {"mode": "none", "spec": None}


def A(key):
    return ASSUMPTIONS[key][0]


@lru_cache(maxsize=1)
def data():
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def base_stats():
    """Base attributes per class, race and level (server-side, not in the client)."""
    if BASE_STATS_PATH.exists():
        return json.loads(BASE_STATS_PATH.read_text(encoding="utf-8"))
    return None


# ---------- Spell lookup ----------

@lru_cache(maxsize=None)
def ranks(cls, name):
    """All trained ranks of a class spell, ordered by level."""
    out = [s for s in data()["classes"][cls]["spells"] if s["name"] == name and s["base_level"] > 0]
    seen, uniq = set(), []
    for s in sorted(out, key=lambda s: (s["base_level"], s["id"])):
        if s["id"] not in seen:
            seen.add(s["id"])
            uniq.append(s)
    return uniq


def best_rank(cls, name, level):
    """Highest rank of a spell a character of `level` can use, or None."""
    avail = [s for s in ranks(cls, name) if s["base_level"] <= level]
    return avail[-1] if avail else None


@lru_cache(maxsize=None)
def talent(cls, name):
    for t in data()["classes"][cls]["talents"]:
        if t["name"] == name:
            return t
    raise KeyError(f"{cls} talent {name!r} not found")


def talent_points(cls, name, rank, effect_index=0):
    """Effect base points of a talent at `rank` (1-based).

    The Forever client omits effect rows for many talent ranks above 1 (they are
    served by the game server). Missing ranks are scaled linearly from rank 1,
    the standard Classic pattern, and reported as an assumption.
    """
    if rank <= 0:
        return 0.0, "F"
    t = talent(cls, name)
    r = t["ranks"][min(rank, len(t["ranks"])) - 1]
    effs = [e for e in r["effects"] if e["EffectIndex"] == effect_index]
    if effs:
        return float(effs[0]["EffectBasePointsF"]), "F"
    first = [e for e in t["ranks"][0]["effects"] if e["EffectIndex"] == effect_index]
    if not first:
        return 0.0, "A"
    return float(first[0]["EffectBasePointsF"]) * rank, "A"


def max_rank(cls, name):
    return len(talent(cls, name)["ranks"])


def damage_effect(spell):
    """First damaging effect of a spell, resolved through trigger spells."""
    for e in spell["effects"]:
        if e["Effect"] == SCHOOL_DAMAGE or (e["Effect"] == APPLY_AURA and e["EffectAura"] in (PERIODIC_DAMAGE, PERIODIC_LEECH)):
            return e
        if e.get("trigger"):
            inner = damage_effect(e["trigger"])
            if inner:
                return inner
    return None


def effect_value(e, level, spell_level=0):
    """Average base points of an effect at caster level (client formula: base + per-level growth)."""
    growth = e.get("EffectRealPointsPerLevel") or 0
    base = e["EffectBasePointsF"] + growth * max(0, level - spell_level)
    return base


def effect_range(e, level, spell_level=0):
    base = effect_value(e, level, spell_level)
    var = e.get("Variance") or 0
    return base * (1 - var / 2), base * (1 + var / 2)


def cost(spell, base_mana):
    for c in spell["costs"]:
        if c["PowerCostPct"]:
            return c["PowerType"], base_mana * c["PowerCostPct"] / 100
        if c["ManaCost"]:
            return c["PowerType"], c["ManaCost"]
    return None, 0


# ---------- Character ----------

class Character:
    """A naked character of class, race and level, with talents and racials."""

    def __init__(self, cls, race, level, talents=None, racials=()):
        self.cls, self.race, self.level = cls, race, level
        self.talents = talents or {}
        self.racials = set(racials)
        exp = data()["classes"][cls]["expected"].get(str(level)) or {}
        self.base_mana = exp.get("base_mana", 0)
        self.crit_per_agi = exp.get("crit_per_agility", 0) * 100       # % crit per point (F)
        self.spell_crit_per_int = exp.get("spell_crit_per_intellect", 0) * 100  # (F)
        bs = base_stats()
        st = None
        if bs:
            st = bs.get(cls, {}).get(race, {}).get(str(level))
        self.stats_tag = "C" if st else "A"
        if not st:
            st = {"str": 20 + level * 1.5, "agi": 20 + level * 1.0, "sta": 20 + level * 1.5, "int": 20 + level, "spi": 20 + level}
        self.str, self.agi, self.sta, self.int, self.spi = (st[k] for k in ("str", "agi", "sta", "int", "spi"))
        self.hit = 0.0
        self.crit_bonus = 0.0
        self.spell_crit_bonus = 0.0
        self.haste = 1.0
        self.dmg_mult = 1.0
        self.ap_mult = 1.0
        self.sp = 0.0
        # Gear (see gear.py). run.py sets GEAR["mode"] and GEAR["spec"] before each simulate().
        # Base stats, hit and crit are applied here; modules add ch.gear AP, spell power and weapons.
        self.gear = None
        if GEAR["mode"] == "crafted" and GEAR["spec"]:
            import gear as _gear
            self.gear = _gear.select(cls, GEAR["spec"], level)
            gs = self.gear["stats"]
            self.str += gs.get("str", 0)
            self.agi += gs.get("agi", 0)
            self.sta += gs.get("sta", 0)
            self.int += gs.get("int", 0)
            self.spi += gs.get("spi", 0)
            self.hit += gs.get("hit", 0) / _gear.HIT_RATING_PER_PCT
            self.crit_bonus += gs.get("crit", 0) / _gear.CRIT_RATING_PER_PCT
            self.spell_crit_bonus += gs.get("crit", 0) / _gear.CRIT_RATING_PER_PCT
            self.stats_tag += "+gear"

    def gear_stat(self, key, default=0):
        return self.gear["stats"].get(key, default) if self.gear else default

    def gear_ap(self):
        return self.gear_stat("ap")

    def gear_rap(self):
        return self.gear_stat("rap")

    def gear_sp(self, school=None):
        """Bonus spell damage from gear, plus the school-specific part if given."""
        if not self.gear:
            return 0
        import gear as _gear
        return _gear.spell_power(self.gear, school)

    def weapon(self, hand="mh"):
        """(average damage, speed) of the equipped weapon in hand mh/oh/ranged, or
        the unarmed fist for mh/oh when nothing is equipped there; None for ranged."""
        w = self.gear and self.gear.get(hand)
        if w and w["type"] != "wand" or (w and hand == "ranged"):
            return w["avg"], w["speed"]
        if hand == "ranged":
            return None
        if hand == "oh" and self.gear and self.gear.get("mh") and not self.gear.get("oh"):
            return None  # two-hander or shield: no off-hand weapon
        return unarmed_weapon(self.level)

    def tr(self, name):
        return self.talents.get(name, 0)

    @property
    def melee_crit(self):
        return self.agi * self.crit_per_agi + self.crit_bonus

    @property
    def spell_crit(self):
        return A("base_spell_crit") + self.int * self.spell_crit_per_int + self.spell_crit_bonus

    def mana(self):
        return self.base_mana + self.int * 15 - 280 + 20 if self.base_mana else 0  # Classic Int->mana (CU)


def unarmed_weapon(level):
    """Unarmed fist damage (Classic: 1-2 at level 1 scaling with level), speed 2.0. (CU)"""
    lo = 1 + level * 0.43
    hi = 2 + level * 0.82
    return (lo + hi) / 2, 2.0


# ---------- Rolls ----------

class Rng:
    def __init__(self, seed):
        self.r = random.Random(seed)

    def chance(self, pct):
        return self.r.random() * 100 < pct

    def uniform(self, lo, hi):
        return self.r.uniform(lo, hi)


def melee_roll(rng, ch, white=True, dual_wield=False, extra_crit=0.0):
    """Single-roll attack table vs a same-level target from behind.
    Returns 'miss' | 'dodge' | 'glance' | 'crit' | 'hit'."""
    miss = max(0.0, A("melee_miss_same_level") + (A("dw_miss_penalty") if white and dual_wield else 0) - ch.hit)
    dodge = A("dodge_same_level")
    glance = A("glance_same_level") if white else 0
    crit = max(0.0, ch.melee_crit + extra_crit)
    x = rng.r.random() * 100
    for outcome, w in (("miss", miss), ("dodge", dodge), ("glance", glance), ("crit", crit)):
        if x < w:
            return outcome
        x -= w
    return "hit"


def spell_roll(rng, ch, extra_crit=0.0, extra_hit=0.0, can_crit=True):
    if not rng.chance(min(99.0, A("spell_hit_same_level") + ch.hit + extra_hit)):
        return "miss"
    if can_crit and rng.chance(ch.spell_crit + extra_crit):
        return "crit"
    return "hit"


# ---------- Event loop ----------

class Sim:
    """Minimal discrete-event loop. Class modules schedule callbacks and record damage."""

    def __init__(self, seed, fight=None):
        self.rng = Rng(seed)
        self.t = 0.0
        self.end = fight or A("fight_seconds")
        self.q = []
        self.n = 0
        self.damage = {}
        self.casts = {}

    def at(self, t, fn, *args):
        self.n += 1
        heapq.heappush(self.q, (t, self.n, fn, args))

    def deal(self, source, amount):
        if amount > 0:
            self.damage[source] = self.damage.get(source, 0.0) + amount

    def cast(self, name):
        self.casts[name] = self.casts.get(name, 0) + 1

    def run(self):
        while self.q:
            t, _, fn, args = heapq.heappop(self.q)
            if t > self.end:
                break
            self.t = t
            fn(*args)
        return sum(self.damage.values()) / self.end


def run_many(build_fn, iterations=200, seed=1, fight=None):
    """build_fn(sim) sets up one fight. Returns mean, sd, ci95 and breakdown."""
    vals, breakdown = [], {}
    for i in range(iterations):
        sim = Sim(seed + i, fight)
        build_fn(sim)
        vals.append(sim.run())
        for k, v in sim.damage.items():
            breakdown[k] = breakdown.get(k, 0.0) + v / sim.end
    n = len(vals)
    mean = sum(vals) / n
    sd = math.sqrt(sum((v - mean) ** 2 for v in vals) / max(1, n - 1))
    half = 1.96 * sd / math.sqrt(n)
    return {"dps_mean": round(mean, 2), "dps_sd": round(sd, 2), "ci95": [round(mean - half, 2), round(mean + half, 2)],
            "iterations": n, "breakdown": {k: round(v / n, 2) for k, v in sorted(breakdown.items(), key=lambda kv: -kv[1])}}


# ---------- Racials (Forever client / Wowhead Forever values) ----------

RACIALS = {
    "human": {"crit": 1.0},
    "dwarf": {"hit": 1.0},
    "nelf": {"cd": ("crit", 10.0, 15, 180)},
    "sho": {"haste": 2.0},
    "sws": {"haste": 2.0},
    "orc": {"cd": ("power", 10.0, 15, 120), "pet": 5.0},
    "troll": {"cd": ("haste", 10.0, 15, 180)},
    "gnome": {"cd": ("direct", 10.0, 8, 120)},
    "tauren": {}, "undead": {},
}
RACE_LEVEL = {"nelf": 1, "orc": 1, "troll": 1, "gnome": 1}  # racials are known from level 1 in Forever (A)


def apply_passive_racials(ch, race):
    r = RACIALS[race]
    ch.crit_bonus += r.get("crit", 0)
    ch.spell_crit_bonus += r.get("crit", 0)
    ch.hit += r.get("hit", 0)
    ch.haste *= 1 + r.get("haste", 0) / 100


def racial_cooldown(race):
    return RACIALS[race].get("cd")
