"""Event-driven combat engine for the physical DPS specs of WoW Forever.

Standard library only. One `Sim` is one fight: a priority queue of timed
events (swings, resource ticks, DoT ticks, aura expiries, an APL heartbeat).
Every number comes from data.json through `Data`, which records which inputs
a spec read so the result can report its share of Forever-tagged inputs.
"""
from __future__ import annotations

import heapq
import json
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TAGS = ("F", "FE", "C", "CU", "A")
FOREVER_TAGS = ("F", "FE")

MISS, DODGE, GLANCE, CRIT, HIT = "miss", "dodge", "glance", "crit", "hit"


# ---------------------------------------------------------------- data access
class Data:
    """Wraps data.json. `d("a", "b")` returns the value of leaf a.b and logs its tag."""

    def __init__(self, raw: dict):
        self.raw = raw
        self.used: dict[str, str] = {}

    @classmethod
    def load(cls, path: str | None = None) -> "Data":
        with open(path or os.path.join(HERE, "data.json"), encoding="utf-8") as f:
            return cls(json.load(f))

    def __call__(self, *path: str):
        node = self.raw
        for p in path:
            node = node[p]
        if not (isinstance(node, list) and len(node) == 3 and node[1] in TAGS):
            raise KeyError(f"{'.'.join(path)} is not a tagged leaf")
        self.used[".".join(path)] = node[1]
        return node[0]

    def fresh(self) -> "Data":
        return Data(self.raw)

    def confidence(self) -> float:
        if not self.used:
            return 0.0
        return sum(1 for t in self.used.values() if t in FOREVER_TAGS) / len(self.used)

    def tag_counts(self) -> dict:
        out = {t: 0 for t in TAGS}
        for t in self.used.values():
            out[t] += 1
        return out


def iter_leaves(node, path=()):
    """Yield (path, leaf) for every tagged leaf (used by tests)."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k.startswith("_"):
                continue
            yield from iter_leaves(v, path + (k,))
    else:
        yield path, node


# ---------------------------------------------------------------- pure math
def roll_white(r: float, miss: float, dodge: float, glance: float, crit: float) -> str:
    """One-roll table for white swings. All chances in percent, r in [0, 100)."""
    edge = max(0.0, miss)
    if r < edge:
        return MISS
    edge += max(0.0, dodge)
    if r < edge:
        return DODGE
    edge += max(0.0, glance)
    if r < edge:
        return GLANCE
    edge += max(0.0, crit)
    if r < edge:
        return CRIT
    return HIT


def roll_yellow(r1: float, r2: float, miss: float, dodge: float, crit: float) -> str:
    """Two-roll table for special attacks: avoidance first, then crit on a landed hit."""
    if r1 < max(0.0, miss):
        return MISS
    if r1 < max(0.0, miss) + max(0.0, dodge):
        return DODGE
    return CRIT if r2 < crit else HIT


def white_table_shares(miss, dodge, glance, crit) -> dict:
    """Expected shares of the one-roll table (crit is pushed off the table first)."""
    out = {}
    left = 100.0
    for k, v in ((MISS, miss), (DODGE, dodge), (GLANCE, glance), (CRIT, crit)):
        v = min(max(0.0, v), left)
        out[k] = v / 100
        left -= v
    out[HIT] = left / 100
    return out


def rage_from_damage(d: Data, dmg: float, speed: float, offhand: bool, crit: bool) -> float:
    """Rage from a white hit. Forever: weapon-speed based, crits +75% (no published formula)."""
    c = d("rage", "c_level60")
    if dmg <= 0:
        return 0.0
    if d("rage", "model") == "classic":
        r = d("rage", "classic_factor") * dmg / c
    else:
        f = d("rage", "speed_hit_factor_oh") if offhand else d("rage", "speed_hit_factor_mh")
        r = d("rage", "speed_damage_factor") * dmg / c + f * speed / 2
        r = min(r, d("rage", "cap_factor") * dmg / c)
    if crit:
        r *= 1 + d("rage", "crit_bonus")
    return r


def ppm_chance(ppm: float, speed: float) -> float:
    return ppm * speed / 60.0


def armor_multiplier(armor: float, k: float) -> float:
    armor = max(0.0, armor)
    return 1 - min(0.75, armor / (armor + k))


# ---------------------------------------------------------------- simulation
class Sim:
    def __init__(self, fight: float, rng):
        self.t = 0.0
        self.fight = fight
        self.rng = rng
        self._q = []
        self._seq = 0
        self.dmg = defaultdict(float)
        self.counts = defaultdict(int)

    def at(self, t, fn, *args):
        self._seq += 1
        heapq.heappush(self._q, (t, self._seq, fn, args))

    def after(self, dt, fn, *args):
        self.at(self.t + dt, fn, *args)

    def run(self, player):
        player.start()
        while self._q:
            t, _, fn, args = heapq.heappop(self._q)
            if t > self.fight:
                break
            self.t = t
            fn(*args)
        return sum(self.dmg.values()) / self.fight


class Swing:
    """An auto-attack timer. Haste changes rescale the time left on the current swing."""

    def __init__(self, player, hand, speed, fn):
        self.p, self.hand, self.speed, self.fn = player, hand, speed, fn
        self.token = 0
        self.next = 0.0
        self.h = 1.0

    def start(self, delay=0.0):
        self.h = self.p.haste(self.hand)
        self._schedule(delay)

    def _schedule(self, delay):
        self.token += 1
        self.next = self.p.sim.t + delay
        self.p.sim.at(self.next, self._fire, self.token)

    def _fire(self, token):
        if token != self.token:
            return
        self.fn(self.hand)
        self.h = self.p.haste(self.hand, consume=True)
        self._schedule(self.speed / self.h)

    def rescale(self):
        h = self.p.haste(self.hand)
        if abs(h - self.h) < 1e-12:
            return
        left = max(0.0, self.next - self.p.sim.t) * self.h / h
        self.h = h
        self._schedule(left)

    def delay_to(self, t):
        if self.next < t:
            self._schedule(t - self.p.sim.t)


class Dot:
    """A periodic effect; reapplying restarts it with the new tick value."""

    def __init__(self, player, name, school):
        self.p, self.name, self.school = player, name, school
        self.token = 0
        self.ticks_left = 0
        self.tick_dmg = 0.0
        self.stacks = 0

    @property
    def up(self):
        return self.ticks_left > 0

    def apply(self, tick_dmg, ticks, interval):
        """Apply or refresh. A refresh resets the duration and tick value but keeps the
        running tick timer, so frequent refreshes never starve the ticks (A)."""
        running = self.ticks_left > 0
        self.tick_dmg, self.ticks_left, self.interval = tick_dmg, ticks, interval
        if not running:
            self.token += 1
            self.p.sim.after(interval, self._tick, self.token)

    def _tick(self, token):
        if token != self.token or self.ticks_left <= 0:
            return
        self.ticks_left -= 1
        self.p.deal(self.name, self.tick_dmg, self.school, periodic=True)
        if self.ticks_left > 0:
            self.p.sim.after(self.interval, self._tick, token)
        else:
            self.stacks = 0
