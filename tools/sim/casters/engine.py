"""Event-driven combat core for the WoW Forever caster simulator.

One `Caster` instance simulates one fight. Time advances through a priority
queue of events (cast finishes, DoT ticks, channel ticks, mana ticks, racial
cooldowns, pet attacks). The player acts whenever it is free (`ready`): the
spec's APL picks one action, which occupies the player for the cast time or
the GCD, whichever is longer. Every hit, crit and proc is rolled with the
fight's own `random.Random`, so a seed reproduces a fight exactly.

Standard library only.
"""
from __future__ import annotations

import heapq
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOREVER_TAGS = {"F", "FE"}
MAGIC = {"fire", "frost", "arcane", "shadow", "nature", "holy"}


class Data:
    """Reads data.json. Every leaf is [value, tag, source]; reads are recorded
    so a spec's `data_confidence` is the Forever share of what it actually used."""

    def __init__(self, path: Path | str | None = None):
        with open(path or HERE / "data.json", encoding="utf-8") as f:
            self.raw = json.load(f)
        self.used: dict[str, str] = {}

    def _node(self, path: str):
        n = self.raw
        for k in path.split("."):
            n = n[k]
        return n

    def has(self, path: str) -> bool:
        try:
            self._node(path)
            return True
        except KeyError:
            return False

    def get(self, path: str):
        node = self._node(path)
        if not (isinstance(node, list) and len(node) == 3):
            raise ValueError(f"{path} is not a [value, tag, source] leaf")
        value, tag, _src = node
        self.used[path] = tag
        return value

    def opt(self, path: str, default=0):
        return self.get(path) if self.has(path) else default

    def confidence(self) -> float:
        if not self.used:
            return 0.0
        return sum(1 for t in self.used.values() if t in FOREVER_TAGS) / len(self.used)


class Dot:
    __slots__ = ("gen", "ticks_left", "interval", "amount", "end", "can_crit", "label", "name", "extra")

    def __init__(self):
        self.gen = 0
        self.ticks_left = 0
        self.end = -1.0


class Caster:
    cls = ""
    spec = ""
    build = ""

    def __init__(self, race: str, data: Data, rng, fight: float = 180.0):
        self.D = data
        self.rng = rng
        self.race = race
        self.fight = float(fight)
        self.t = 0.0
        self._q: list = []
        self._seq = 0
        self.dmg: dict[str, float] = defaultdict(float)
        self.casts: dict[str, int] = defaultdict(int)
        self.buffs: dict[str, float] = {}
        self.cds: dict[str, float] = {}
        self.dots: dict[str, Dot] = {}
        self.S: dict[str, dict] = {}
        self.busy_until = 0.0
        self.last_spend = -100.0
        self.mana_spent = 0.0
        self.mana_gained = 0.0
        # Talent hooks a spec's setup() may change before stats are derived.
        self.int_mult = 1.0
        self.mana_mult = 1.0
        self.extra_hit = 0.0
        self.extra_crit = 0.0
        self.extra_sp = 0.0
        self.regen_cast = 0.0
        self.setup()
        self._derive()

    # ---------- data helpers ----------
    def g(self, path):
        return self.D.get(path)

    def sv(self, spell, field):
        return self.D.get(f"spells.{spell}.{field}")

    def tv(self, field):
        return self.D.get(f"talents.{self.cls}.{field}")

    def reg(self, name, school, periodic=False, label=None):
        self.S[name] = {"school": school, "periodic": periodic, "label": label or name}

    def _race(self, key, default=0):
        return self.D.opt(f"races.{self.race}.{key}", default)

    # ---------- stats ----------
    def _derive(self):
        D = self.D
        c = f"classes.{self.cls}"
        kings = 1 + D.get("buffs.kings")
        self.int = (D.get("gear.int") + self._race("int") + D.get("buffs.int_ai") + D.get("buffs.motw")) * kings * self.int_mult
        self.spirit = ((D.get("gear.spirit") + D.get("buffs.motw") + D.get("buffs.divine_spirit")) * kings
                       * (1 + self._race("spirit_mult")))
        self.base_mana = D.get(f"{c}.base_mana")
        i = self.int
        self.max_mana = (self.base_mana + min(20.0, i) + 15 * max(0.0, i - 20)) * self.mana_mult
        self.mana = self.max_mana
        self.hit_cap = D.get("model.spell_hit_cap")
        self.hit = D.get("model.spell_hit_base") + D.get("gear.hit") + self._race("hit") + self.extra_hit
        self.crit = (D.get(f"{c}.base_crit") + i / D.get(f"{c}.int_per_crit") + D.get("gear.crit")
                     + D.get("buffs.lotp") + D.get("buffs.moonkin") - D.get("model.crit_suppression")
                     + self._race("crit") + self.extra_crit)
        self.sp = D.get("gear.sp") + self.extra_sp
        self.base_crit_mult = D.get("model.spell_crit_mult")
        self.haste_base = 1 + self._race("haste")
        self.gcd_base = D.get("model.gcd")
        self.gcd_min = D.get("model.gcd_min")
        self.fsr = D.get("model.five_second_rule")
        self.tick_len = D.get("model.regen_tick")
        self.delay = D.get("model.reaction_delay")
        self.regen = D.get(f"{c}.regen_base") + self.spirit / D.get(f"{c}.regen_div")
        self.mp2 = (D.get("buffs.wisdom_mp5") + D.get("gear.mp5")) * self.tick_len / 5 + D.get("buffs.mana_spring_2s")
        self.coe = D.get("buffs.coe")
        self.cos = D.get("buffs.cos")
        self.pot = (D.get("consumables.mana_potion_min"), D.get("consumables.mana_potion_max"),
                    D.get("consumables.mana_potion_cd"))
        r = f"races.{self.race}"
        self.racials = []
        for key in ("blood_fury", "berserking", "elune", "eureka"):
            if D.has(f"{r}.{key}"):
                self.racials.append((key, D.get(f"{r}.{key}"), D.get(f"{r}.{key}_dur"), D.get(f"{r}.{key}_cd")))
        self.racial_val = {k: v for k, v, _d, _c in self.racials}
        self.pet_mult_race = 1 + self._race("command")

    # ---------- event queue ----------
    def at(self, t, fn, *args):
        self._seq += 1
        heapq.heappush(self._q, (t, self._seq, fn, args))

    def run(self) -> float:
        self.at(self.rng.random() * self.tick_len, self._regen_tick)
        for key, val, dur, cd in self.racials:
            self.at(0.0, self._use_racial, key, dur, cd)
        self.at(0.0, self._begin)
        q = self._q
        while q:
            t, _s, fn, args = heapq.heappop(q)
            if t > self.fight:
                break
            self.t = t
            fn(*args)
        return sum(self.dmg.values())

    def _begin(self):
        self.precast()
        self.ready()

    def _use_racial(self, key, dur, cd):
        self.buffs[key] = self.t + dur
        self.casts[key] += 1
        self.at(self.t + cd, self._use_racial, key, dur, cd)

    # ---------- buffs and cooldowns ----------
    def up(self, b) -> bool:
        return self.buffs.get(b, -1.0) > self.t

    def remaining(self, b) -> float:
        return max(0.0, self.buffs.get(b, -1.0) - self.t)

    def cd_ready(self, n) -> bool:
        return self.cds.get(n, 0.0) <= self.t + 1e-9

    def hp(self) -> float:
        """Target health fraction: linear from 100% at pull to 0% at fight end."""
        return max(0.0, 1.0 - self.t / self.fight)

    # ---------- formulas ----------
    def haste(self) -> float:
        h = self.haste_base * self.haste_extra()
        if self.up("berserking"):
            h *= 1 + self.racial_val["berserking"]
        return h

    def gcd(self) -> float:
        return max(self.gcd_min, self.gcd_base / self.haste())

    def spell_power(self) -> float:
        sp = self.sp
        if self.up("blood_fury"):
            sp *= 1 + self.racial_val["blood_fury"]
        return sp + self.sp_extra()

    def crit_pct(self, name) -> float:
        c = self.crit + self.crit_extra(name)
        if self.up("elune"):
            c += self.racial_val["elune"]
        return c

    def hit_p(self, name) -> float:
        return min(self.hit_cap, self.hit + self.hit_extra(name)) / 100.0

    def debuff(self, school) -> float:
        if school not in MAGIC:
            return 1.0
        v = self.coe
        if school in ("shadow", "arcane"):
            v = max(v, self.cos)  # one curse per warlock; the two never stack on one school (A)
        return 1 + v

    def mult(self, name, periodic) -> float:
        m = self.debuff(self.S[name]["school"]) * self.spec_mult(name, periodic)
        if not periodic and self.up("eureka"):
            m *= 1 + self.racial_val["eureka"]
        return m

    def cost(self, name, base) -> float:
        """Mana cost after talents; consumes Clearcasting. Call only when casting."""
        if base <= 0:
            return 0.0
        if self.up("cc"):
            del self.buffs["cc"]
            return 0.0
        c = base * self.cost_mult(name)
        if self.up("eureka") and not self.S.get(name, {}).get("periodic"):
            c *= 1 - self.racial_val["eureka"]
        return c

    def peek_cost(self, name, base) -> float:
        if base <= 0 or self.up("cc"):
            return 0.0
        c = base * self.cost_mult(name)
        if self.up("eureka") and not self.S.get(name, {}).get("periodic"):
            c *= 1 - self.racial_val["eureka"]
        return c

    # ---------- damage ----------
    def deal(self, label, amt):
        self.dmg[label] += amt

    def roll_hit(self, name) -> bool:
        return self.rng.random() < self.hit_p(name)

    def roll_crit(self, name, bonus=0.0) -> bool:
        return self.rng.random() * 100 < self.crit_pct(name) + bonus

    def direct(self, name, base, coef, label=None, sp_extra=0.0, crit_bonus=0.0, mult=1.0,
               periodic=False, hit_rolled=False, can_crit=True):
        """Roll hit and crit for one damage event. Returns None on a miss, else (crit, amount)."""
        if not hit_rolled and not self.roll_hit(name):
            self.casts[(label or self.S[name]["label"]) + " (miss)"] += 1
            return None
        amt = (base + coef * (self.spell_power() + sp_extra)) * self.mult(name, periodic) * mult
        crit = can_crit and self.roll_crit(name, crit_bonus)
        if crit:
            amt *= self.crit_mult(name, periodic)
        self.deal(label or self.S[name]["label"], amt)
        return crit, amt

    def apply_dot(self, key, per_tick, ticks, interval, can_crit, label=None, name=None, extra=1.0):
        """(Re)apply a DoT: a refresh drops the old ticks and restarts the timer (Classic rule).
        `per_tick` is snapshotted (base + coefficient x spell power at application)."""
        d = self.dots.get(key)
        if d is None:
            d = self.dots[key] = Dot()
        d.gen += 1
        d.ticks_left = ticks
        d.interval = interval
        d.amount = per_tick
        d.end = self.t + ticks * interval
        d.can_crit = can_crit
        d.name = name or key
        d.label = label or self.S[d.name]["label"]
        d.extra = extra
        self.at(self.t + interval, self._dot_tick, key, d.gen)

    def _dot_tick(self, key, gen):
        d = self.dots[key]
        if d.gen != gen:
            return
        amt = d.amount * self.mult(d.name, True) * d.extra * self.dot_mult(key)
        crit = False
        if d.can_crit and self.roll_crit(d.name):
            amt *= self.crit_mult(d.name, True)
            crit = True
        self.deal(d.label, amt)
        d.ticks_left -= 1
        if d.ticks_left > 0:
            self.at(self.t + d.interval, self._dot_tick, key, gen)
        else:
            d.end = self.t
        self.on_tick(key, crit, amt)

    def dot_rem(self, key) -> float:
        d = self.dots.get(key)
        return max(0.0, d.end - self.t) if d else 0.0

    # ---------- actions ----------
    def pay(self, cost):
        if cost > 0:
            self.mana -= cost
            self.mana_spent += cost
            self.last_spend = self.t

    def gain(self, amt):
        new = min(self.max_mana, self.mana + amt)
        self.mana_gained += new - self.mana
        self.mana = new

    def start_cast(self, name, cast_time, on_finish, cost):
        """cast_time is already hasted; 0 means instant (resolves now, GCD only)."""
        self.pay(cost)
        self.casts[self.S[name]["label"] if name in self.S else name] += 1
        g = self.gcd()
        if cast_time <= 0:
            self.busy_until = self.t + g
            on_finish()
        else:
            self.busy_until = self.t + max(cast_time, g)
            self.at(self.t + cast_time, on_finish)
        self.at(self.busy_until + self.delay, self.ready)
        return True

    def start_channel(self, name, duration, ticks, on_tick, cost, gcd=True):
        self.pay(cost)
        self.casts[self.S[name]["label"] if name in self.S else name] += 1
        self.busy_until = self.t + max(duration, self.gcd() if gcd else 0)
        iv = duration / ticks
        for i in range(1, ticks + 1):
            self.at(self.t + i * iv, on_tick, i)
        self.at(self.busy_until + self.delay, self.ready)
        return True

    def ready(self):
        if self.t + 1e-9 < self.busy_until:
            return
        self._off_gcd()
        if not self.apl():
            self.busy_until = self.t + 0.25
            self.at(self.t + 0.25, self.ready)

    def _off_gcd(self):
        lo, hi, cd = self.pot
        if self.max_mana - self.mana >= hi and self.cd_ready("potion") and self.t > 0:
            self.gain(self.rng.uniform(lo, hi))
            self.cds["potion"] = self.t + cd
            self.casts["Major Mana Potion"] += 1
        self.spec_off_gcd()

    def _regen_tick(self):
        casting = self.t - self.last_spend < self.fsr
        self.gain(self.regen * (self.regen_cast if casting else 1.0) + self.mp2)
        self.at(self.t + self.tick_len, self._regen_tick)

    # ---------- spec hooks (override) ----------
    def setup(self):
        pass

    def precast(self):
        pass

    def apl(self) -> bool:
        return False

    def spec_off_gcd(self):
        pass

    def crit_extra(self, name) -> float:
        return 0.0

    def hit_extra(self, name) -> float:
        return 0.0

    def spec_mult(self, name, periodic) -> float:
        return 1.0

    def crit_mult(self, name, periodic) -> float:
        return self.base_crit_mult

    def cost_mult(self, name) -> float:
        return 1.0

    def haste_extra(self) -> float:
        return 1.0

    def sp_extra(self) -> float:
        return 0.0

    def dot_mult(self, key) -> float:
        return 1.0

    def on_tick(self, key, crit, amt):
        pass
