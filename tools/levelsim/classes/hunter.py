"""Hunter: level-aware DPS for Beast Mastery, Marksmanship and Survival, naked or in
crafted gear (core.GEAR, see "Gear" below).

No gear means no ranged weapon and no ammo. In the client, Auto Shot, Serpent
Sting, Arcane Shot, Multi-Shot, Aimed Shot, Volley and Sniper Shot require an
equipped bow, gun or crossbow, and Raptor Strike and Wing Clip require an
equipped melee weapon (SpellEquippedItems, tag F). A naked Hunter therefore:
- auto-attacks in melee with the unarmed fist (`core.unarmed_weapon`),
- uses the abilities with no weapon requirement: Mongoose Bite (after a dodge),
  Strider Kick (talent), Summon Hawk (talent), Immolation/Explosive Trap and
  Hunter's Mark,
- and fights with a pet from level 10.

Talent values: the client stores effect rows for rank 1 only, and the rank-1
row often holds the max-rank value (Unleashed Fury 20, Ferocity 16, Endurance
Training 15...); many Forever talents are missing from the client tree
(Focused Fire, Careful Aim, Lone Wolf, Predator's Edge, ...). So every talent
value is the per-rank value from the live tooltips
(.research/talents/hunter.json rank 1 / max rank text), tag F (tooltip).

Server-side behaviour and assumptions (tag in `inputs`):
- Attack power (Classic, C): melee AP = 2*level + Str + Agi - 20,
  ranged AP = 2*level + 2*Agi - 10.
- Pet: not in the client. A generic cat: 2.0 s melee for 100/60 * level
  average, plus a special (Claw) every 4 s for 115/60 * level, 5% crit
  (A, scaled from the level-60 tools/sim generic pet). Summoned before the pull.
- Hawks: the dive-bomb is client data ($s1 + 5% RAP). The hawk then attacks
  for 18 s; that follow-up is server-side: A, one hit every 2.0 s for half the
  dive-bomb damage. At most 2 hawks.
- Traps are placed under the target and trigger at once (A). The trap with the best
  damage per mana is used, since a naked Hunter is mana-bound (A).
- The target is a tracked creature type, so Improved Tracking applies (A).
- Counterattack needs a parry, and the training target does not attack: unused.
- Deadly Aspects procs from Auto Shot (no ranged weapon) or with Aspect of the
  Beast (not a trained spell in the client): no effect.
- Mana regen: Classic Hunter 15 + Spirit/5 per 2 s tick after 5 s without
  spending mana (CU). Viper Sting drains the target, not a Hunter mana
  source, and needs a ranged weapon: not modelled. No drinking.
- Gear (core.GEAR "crafted", gear.py): gear stats come through core.Character;
  gear "+attack power" adds to melee AP and "+ranged attack power" to RAP only
  (Classic, C; tag "gear": F (crafted items)). With a bow, gun or crossbow the
  Hunter stands at range: Auto Shot, Aspect of the Hawk, Hunter's Mark, Rapid Fire,
  Serpent Sting, Aimed Shot (talent; the client has rank 1 only, F), Multi-Shot and
  Arcane Shot from forever.json, plus pet, hawks and traps; no melee. Sniper Shot
  and Volley's damage are not in the client: unused.
  Ranged rules: weapon min-max + RAP/14 * weapon speed (C); Multi-Shot and Aimed
  Shot use normalized speed 2.8 (CU); the ranged roll is the yellow melee table
  (miss, dodge, crit; no glancing, no parry, CU), with ch.hit and melee crit (C);
  Serpent Sting cannot crit (CU); no ammo damage (A); Auto Shot keeps firing
  through casts (A). Tooltip talents (F): Mortal Shots +6% crit damage bonus per
  rank, Ranged Weapon Specialization +1%/rank weapon shots, Barrage +5%/rank
  Multi/Aimed, Improved Arcane Shot -0.3 s/rank, Improved Serpent Sting +2%/rank,
  Improved Stings +20%/3 per rank, Rapid Killing -60 s Rapid Fire per rank,
  Deadly Aspects 2%/rank Auto Shot chance for +30% ranged speed for 12 s,
  Efficiency also on shots and stings.
- Lone Wolf (Marksmanship 42+): the sim runs with and without the pet and
  reports the better (`pet` in the result).
"""
import core

CLASS = "hunter"
SPECS = {"beast_mastery": "Beast Mastery", "marksmanship": "Marksmanship", "survival": "Survival"}

# Leveling order (talent, points) ending in the level 60 build of docs/guides/hunter/talents.md.
ORDER = {
    # Beast Mastery 31/20/0 (leveling route = dungeon/raid build).
    "beast_mastery": [("Deadly Aspects", 5), ("Focused Fire", 2), ("Endurance Training", 3), ("Bestial Swiftness", 1),
                      ("Unleashed Fury", 4), ("Summon Hawk", 1), ("Unleashed Fury", 1), ("Ferocity", 3),
                      ("Intimidation", 1), ("Ferocity", 2), ("Bestial Discipline", 2), ("Frenzy", 5),
                      ("Bestial Wrath", 1), ("Lethal Attacks", 5), ("Careful Aim", 5), ("Efficiency", 5),
                      ("Mortal Shots", 5)],
    # Marksmanship raid 5/46/0 (guide leveling route to 41, then the raid build's picks).
    "marksmanship": [("Lethal Attacks", 5), ("Careful Aim", 5), ("Rapid Killing", 2), ("Improved Arcane Shot", 3),
                     ("Trueshot Aura", 1), ("Mortal Shots", 5), ("Rapid Recuperation", 2), ("Barrage", 2),
                     ("Ranged Weapon Specialization", 5), ("Sniper Shot", 1), ("Barrage", 1), ("Lone Wolf", 1),
                     ("Improved Arcane Shot", 2), ("Improved Stings", 3), ("Improved Serpent Sting", 5),
                     ("Hawk Eye", 3), ("Deadly Aspects", 5)],
    # Survival melee 5/10/36.
    "survival": [("Improved Tracking", 5), ("Savage Strikes", 2), ("Survivalist", 3), ("Deterrence", 1),
                 ("Surefooted", 3), ("Survivalist", 1), ("Counterattack", 1), ("Predator's Edge", 4),
                 ("Strider Kick", 1), ("Predator's Edge", 1), ("Expose Prey", 2), ("Resourcefulness", 1),
                 ("Lightning Reflexes", 5), ("Lacerating Strikes", 1), ("Resourcefulness", 1),
                 ("Survivalist's Discipline", 1), ("Clever Traps", 2), ("Survivalist's Discipline", 1),
                 ("Lethal Attacks", 5), ("Careful Aim", 5), ("Deadly Aspects", 5)],
}

# Per-rank values from the live tooltips. Tag F.
TT = {
    "Focused Fire": 0.01, "Unleashed Fury": 0.03, "Ferocity": 2.0, "Frenzy": 20.0, "Bestial Discipline": 0.25,
    "Lethal Attacks": 1.0, "Careful Aim": 0.20, "Efficiency": 0.03, "Trueshot Aura": 20, "Lone Wolf": 0.20,
    "Improved Tracking": 0.01, "Savage Strikes": 2.0, "Surefooted": 1.0, "Predator's Edge": 0.06,
    "Expose Prey": 5.0, "Resourcefulness": 0.30, "Survivalist's Discipline": 0.20, "Clever Traps": 0.15,
    "Lightning Reflexes": 0.03, "Lacerating Strikes": 0.40,
    "Mortal Shots": 0.06, "Ranged Weapon Specialization": 0.01, "Barrage": 0.05, "Improved Arcane Shot": 0.3,
    "Improved Serpent Sting": 0.02, "Improved Stings": 0.20 / 3, "Rapid Killing": 60, "Deadly Aspects": 2.0,
}
RANGED_NORMALIZED_SPEED = 2.8          # Classic normalized ranged speed (CU)
DEADLY_ASPECTS = (0.30, 12)            # tooltip: +30% ranged attack speed for 12 s (F)
BESTIAL_WRATH = (0.50, 18, 120)        # tooltip: +50% for 18 s, 2 min (F)
FRENZY = (0.30, 8)                     # tooltip: +30% attack speed for 8 s (F)
INTIMIDATION_CD = 60                   # tooltip (F)
PET_HIT, PET_SPECIAL, PET_SPEED, PET_SPECIAL_EVERY, PET_CRIT = 100 / 60, 115 / 60, 2.0, 4.0, 5.0  # A
HAWK_FOLLOWUP = (2.0, 0.5, 18)         # A: every 2 s, 50% of dive damage, 18 s (duration from tooltip)
MB_WINDOW = 5.0                        # Classic: Mongoose Bite usable 5 s after a dodge (CU)
NORMALIZED_SPEED = 2.4                 # Classic normalized speed of a one-hand weapon/fist (CU)
LACERATE_TICKS = 7                     # 21 s, 3 s ticks (A)


def talents_at(spec, level):
    pts, out = max(0, min(level, 60) - 9), {}
    for name, n in ORDER[spec]:
        for _ in range(n):
            if pts <= 0:
                return out
            out[name] = out.get(name, 0) + 1
            pts -= 1
    return out


class _PetStats:
    hit = 0.0

    def __init__(self, crit):
        self.melee_crit = crit


class Hunter:
    def __init__(self, sim, spec, race, level, use_pet=True):
        self.sim, self.spec, self.level, self.race = sim, spec, level, race
        self.t_ = talents_at(spec, level)
        ch = self.ch = core.Character(CLASS, race, level, self.t_)
        core.apply_passive_racials(ch, race)
        ch.agi *= 1 + self.tr("Lightning Reflexes") * TT["Lightning Reflexes"]
        ch.crit_bonus += self.tr("Lethal Attacks") * TT["Lethal Attacks"]
        ch.hit += self.tr("Surefooted") * TT["Surefooted"]
        self.inp = {"base_stats": ch.stats_tag, "talents": "F", "attack_power": "C", "unarmed": "CU",
                    "pet": "A", "hawk_followup": "A", "traps_trigger_at_once": "A", "mana_regen": "CU",
                    "weapon_requirements": "F", "improved_tracking_applies": "A"}
        self.pet = use_pet and level >= 10
        ca = ch.int * self.tr("Careful Aim") * TT["Careful Aim"]
        self.ap = 2 * level + ch.str + ch.agi - 20 + ca + ch.gear_ap()
        self.rap = 2 * level + 2 * ch.agi - 10 + ca + ch.gear_ap() + ch.gear_rap()  # Classic: +AP gear counts for ranged too (C)
        self.rw = ch.gear["ranged"] if ch.gear else None
        self.rapid_pct = 0.0
        self.next_act = 1.5
        if ch.gear:
            self.inp["gear"] = "F (crafted items)"
        if self.rw:
            self.inp.update({"ranged_attack_table": "CU", "ranged_normalized_speed_2.8": "CU", "no_ammo": "A",
                             "auto_shot_through_casts": "A"})
        self.max_mana = ch.mana()
        self.mana = self.max_mana
        self.last_spend = -10.0
        self.buffs, self.cds = {}, {}
        self.racial = core.racial_cooldown(race)
        self.mb_until = -1.0
        self.hawks = []
        self.intim = False
        self.lacerate_gen = 0
        self.weapon_avg, self.speed = ch.weapon("mh")

    def tr(self, n):
        return self.t_.get(n, 0)

    def spell(self, name):
        if name in ("Summon Hawk", "Strider Kick") and not self.tr(name):
            return None
        return core.best_rank(CLASS, name, self.level)

    def up(self, k):
        return self.buffs.get(k, -1) > self.sim.t

    def ready(self, k):
        return self.cds.get(k, -1) <= self.sim.t

    # ---------- multipliers ----------
    def player_mult(self):
        m = 1 + self.tr("Improved Tracking") * TT["Improved Tracking"]
        if self.pet:
            m *= 1 + self.tr("Focused Fire") * TT["Focused Fire"]
        elif self.tr("Lone Wolf"):
            m *= 1 + TT["Lone Wolf"]
        if self.racial and self.racial[0] in ("power", "direct") and self.up("racial"):
            m *= 1 + self.racial[1] / 100
        return m

    def pet_mult(self, hawk=False):
        m = 1 + self.tr("Unleashed Fury") * TT["Unleashed Fury"]
        if not hawk:
            m *= 1 + self.tr("Focused Fire") * TT["Focused Fire"]
            if self.up("bw"):
                m *= 1 + BESTIAL_WRATH[0]
        if self.race == "orc":
            m *= 1 + core.RACIALS["orc"].get("pet", 0) / 100
        return m

    def crit_extra(self):
        return self.racial[1] if self.racial and self.racial[0] == "crit" and self.up("racial") else 0.0

    def haste(self):
        h = self.ch.haste
        if self.racial and self.racial[0] == "haste" and self.up("racial"):
            h *= 1 + self.racial[1] / 100
        return h

    # ---------- resources ----------
    def cost(self, s, melee=False, trap=False, shot=False):
        _, c = core.cost(s, self.ch.base_mana)
        if melee or shot:
            c *= 1 - self.tr("Efficiency") * TT["Efficiency"]
        if melee or trap:
            c *= 1 - self.tr("Resourcefulness") * TT["Resourcefulness"]
        return c

    def spend(self, c):
        if c > 0:
            self.mana -= c
            self.last_spend = self.sim.t

    def regen(self):
        tick = 15 + self.ch.spi / 5
        if self.sim.t - self.last_spend < 5:
            frac = self.tr("Bestial Discipline") * TT["Bestial Discipline"]
            if self.up("resourceful"):
                frac = max(frac, 0.5)
            tick *= frac
        self.mana = min(self.max_mana, self.mana + tick)
        self.sim.at(self.sim.t + 2, self.regen)

    # ---------- player melee ----------
    def swing(self):
        out = core.melee_roll(self.sim.rng, self.ch, white=True, extra_crit=self.crit_extra())
        if out == "dodge":
            self.mb_until = self.sim.t + MB_WINDOW
        if out not in ("miss", "dodge"):
            amt = (self.weapon_avg * self.sim.rng.uniform(0.8, 1.2) + self.ap / 14 * self.speed) * self.player_mult()
            amt *= {"glance": core.A("glance_damage"), "crit": core.A("melee_crit_mult")}.get(out, 1.0)
            self.sim.deal("Melee", amt)
            self.expose_prey()
        self.sim.at(self.sim.t + self.speed / self.haste(), self.swing)

    def expose_prey(self):
        if self.tr("Expose Prey") and self.up("mark") and self.sim.rng.chance(self.tr("Expose Prey") * TT["Expose Prey"]):
            self.mb_until = self.sim.t + 10

    def yellow(self, name, base):
        sv = self.tr("Savage Strikes") * TT["Savage Strikes"]
        out = core.melee_roll(self.sim.rng, self.ch, white=False, extra_crit=sv + self.crit_extra())
        self.sim.cast(name)
        if out == "dodge":
            self.mb_until = self.sim.t + MB_WINDOW
        if out in ("miss", "dodge"):
            return 0.0
        amt = base * self.player_mult()
        if out == "crit":
            amt *= core.A("melee_crit_mult") + self.tr("Predator's Edge") * TT["Predator's Edge"]
            if self.tr("Resourcefulness") and self.sim.rng.chance(50 * self.tr("Resourcefulness")):
                self.buffs["resourceful"] = self.sim.t + 30
        self.sim.deal(name, amt)
        self.expose_prey()
        return amt

    def lacerate(self, dmg):
        self.lacerate_gen += 1
        per = dmg * TT["Lacerating Strikes"] / LACERATE_TICKS
        for i in range(1, LACERATE_TICKS + 1):
            self.sim.at(self.sim.t + 3 * i, self._lac_tick, self.lacerate_gen, per)

    def _lac_tick(self, gen, per):
        if gen == self.lacerate_gen:
            self.sim.deal("Lacerating Strikes", per)

    # ---------- ranged (gear) ----------
    def rhaste(self):
        h = self.haste()
        if self.up("rapid"):
            h *= 1 + self.rapid_pct
        if self.up("da"):
            h *= 1 + DEADLY_ASPECTS[0]
        return h

    def shot(self, name, base, weapon=True, cast=True):
        out = core.melee_roll(self.sim.rng, self.ch, white=False, extra_crit=self.crit_extra())
        if cast:
            self.sim.cast(name)
        if out in ("miss", "dodge"):
            return 0.0
        amt = base * self.player_mult()
        if weapon:
            amt *= 1 + self.tr("Ranged Weapon Specialization") * TT["Ranged Weapon Specialization"]
        if out == "crit":
            cm = core.A("melee_crit_mult")
            amt *= cm + (cm - 1) * self.tr("Mortal Shots") * TT["Mortal Shots"]
        self.sim.deal(name, amt)
        return amt

    def rweapon(self, normalized=False):
        rw = self.rw
        return self.sim.rng.uniform(rw["min"], rw["max"]) + self.rap_now() / 14 * (
            RANGED_NORMALIZED_SPEED if normalized else rw["speed"])

    def auto_shot(self):
        self.shot("Auto Shot", self.rweapon(), cast=False)
        if self.tr("Deadly Aspects") and self.up("aspect") and \
                self.sim.rng.chance(self.tr("Deadly Aspects") * TT["Deadly Aspects"]):
            self.buffs["da"] = self.sim.t + DEADLY_ASPECTS[1]
        self.sim.at(self.sim.t + self.rw["speed"] / self.rhaste(), self.auto_shot)

    def do_rapid(self):
        s = self.spell("Rapid Fire")
        if not s or not self.ready("rapid") or not self.pay(s):
            return False
        self.rapid_pct = s["effects"][0]["EffectBasePointsF"] / 100
        self.buffs["rapid"] = self.sim.t + s["duration_ms"] / 1000
        self.cds["rapid"] = self.sim.t + s["category_cooldown_ms"] / 1000 - self.tr("Rapid Killing") * TT["Rapid Killing"]
        self.sim.cast("Rapid Fire")
        return False  # off the global cooldown

    def do_sting(self):
        s = self.spell("Serpent Sting")
        if not s or self.up("sting") or self.sim.t > self.sim.end - 6 or not self.pay(s, shot=True):
            return False
        self.sim.cast("Serpent Sting")
        e = s["effects"][0]
        per = (e.get("EffectAuraPeriod") or 3000) / 1000
        n = int(round(s["duration_ms"] / 1000 / per))
        self.buffs["sting"] = self.sim.t + n * per
        out = core.melee_roll(self.sim.rng, self.ch, white=False)
        if out in ("miss", "dodge"):
            self.buffs["sting"] = -1
            return True
        tick = e["EffectBasePointsF"] * (1 + self.tr("Improved Serpent Sting") * TT["Improved Serpent Sting"]) \
            * (1 + self.tr("Improved Stings") * TT["Improved Stings"]) * self.player_mult()
        for i in range(1, n + 1):
            self.sim.at(self.sim.t + i * per, self.sim.deal, "Serpent Sting", tick)
        return True

    def do_aimed(self):
        if not self.tr("Aimed Shot"):
            return False
        s = core.talent(CLASS, "Aimed Shot")["ranks"][0]
        if not self.ready("ms") or not self.pay(s, shot=True):
            return False
        self.cds["ms"] = self.sim.t + s["category_cooldown_ms"] / 1000
        cast = s["cast_ms"] / 1000
        self.next_act = max(1.5, cast)
        bonus = s["effects"][0]["EffectBasePointsF"]
        mult = 1 + self.tr("Barrage") * TT["Barrage"]
        self.sim.at(self.sim.t + cast, lambda: self.shot("Aimed Shot", (self.rweapon(True) + bonus) * mult))
        return True

    def do_multi(self):
        s = self.spell("Multi-Shot")
        if not s or not self.ready("ms") or not self.pay(s, shot=True):
            return False
        self.cds["ms"] = self.sim.t + s["category_cooldown_ms"] / 1000
        bonus = s["effects"][0]["EffectBasePointsF"]
        self.shot("Multi-Shot", (self.rweapon(True) + bonus) * (1 + self.tr("Barrage") * TT["Barrage"]))
        return True

    def do_arcane(self):
        s = self.spell("Arcane Shot")
        if not s or not self.ready("arcane") or not self.pay(s, shot=True):
            return False
        self.cds["arcane"] = self.sim.t + s["category_cooldown_ms"] / 1000 \
            - self.tr("Improved Arcane Shot") * TT["Improved Arcane Shot"]
        self.shot("Arcane Shot", s["effects"][0]["EffectBasePointsF"], weapon=False)
        return True

    # ---------- pet ----------
    def pet_stats(self, extra=0.0):
        return _PetStats(PET_CRIT + self.tr("Ferocity") * TT["Ferocity"] + extra)

    def pet_hit(self, label, avg, white):
        extra = 100.0 if self.intim else 0.0
        out = core.melee_roll(self.sim.rng, self.pet_stats(extra), white=white)
        if out in ("miss", "dodge"):
            return
        self.intim = False
        amt = avg * self.sim.rng.uniform(0.85, 1.15) * self.pet_mult()
        amt *= {"glance": core.A("glance_damage"), "crit": core.A("melee_crit_mult")}.get(out, 1.0)
        self.sim.deal(label, amt)
        if out == "crit" and self.tr("Frenzy") and self.sim.rng.chance(self.tr("Frenzy") * TT["Frenzy"]):
            self.buffs["frenzy"] = self.sim.t + FRENZY[1]

    def pet_swing(self):
        self.pet_hit("Pet: melee", PET_HIT * self.level, True)
        spd = PET_SPEED / (1 + FRENZY[0] if self.up("frenzy") else 1)
        self.sim.at(self.sim.t + spd, self.pet_swing)

    def pet_special(self):
        self.pet_hit("Pet: Claw", PET_SPECIAL * self.level, False)
        self.sim.at(self.sim.t + PET_SPECIAL_EVERY, self.pet_special)

    # ---------- hawks ----------
    def hawk_damage(self, s):
        dive = s["effects"][0]["EffectBasePointsF"] + self.rap_now() * s["effects"][3]["EffectBasePointsF"] / 100
        return dive

    def rap_now(self):
        r = self.rap
        if self.up("aspect"):
            a = self.spell("Aspect of the Hawk")
            r += a["effects"][0]["EffectBasePointsF"]
        if self.up("mark"):
            m = self.spell("Hunter's Mark")
            r += m["effects"][1]["EffectBasePointsF"]
        if self.tr("Trueshot Aura"):
            r += TT["Trueshot Aura"]
        return r

    def hawk_strike(self, label, amt):
        out = core.melee_roll(self.sim.rng, self.pet_stats(), white=False)
        if out in ("miss", "dodge"):
            return
        amt *= self.pet_mult(hawk=True)
        if out == "crit":
            amt *= core.A("melee_crit_mult")
        self.sim.deal(label, amt)

    # ---------- rotation ----------
    def start(self):
        sim = self.sim
        sim.at(0.0, self.regen)
        if self.rw:
            sim.at(0.0, self.auto_shot)
        else:
            sim.at(0.0, self.swing)
        if self.pet:
            sim.at(0.2, self.pet_swing)
            sim.at(1.0, self.pet_special)
        sim.at(0.0, self.act)

    def trap(self):
        """Best fire trap known: (name, effect spell, place spell, expected damage, damage per mana)."""
        best = None
        for name in ("Immolation Trap", "Explosive Trap"):
            rs = [r for r in core.ranks(CLASS, name) if r["base_level"] <= self.level]
            if not rs:
                continue
            lv = max(r["base_level"] for r in rs)
            eff = [r for r in rs if r["base_level"] == lv and any(e["Effect"] in (2, 6, 27) for e in r["effects"])]
            place = [r for r in rs if r["base_level"] == lv and any(e["Effect"] == 104 for e in r["effects"])]
            if not eff or not place:
                continue
            # A naked Hunter is mana-bound (Summon Hawk competes for the same mana),
            # so rank traps by damage per mana, not raw damage (A).
            total = self.trap_total(eff[0])
            value = total / max(1.0, self.cost(place[0], trap=True))
            if not best or value > best[4]:
                best = (name, eff[0], place[0], total, value)
        return best

    def trap_total(self, s):
        tot = 0.0
        for e in s["effects"]:
            if e["Effect"] == 2:
                tot += e["EffectBasePointsF"]
            elif e["Effect"] in (6, 27):
                per = (e.get("EffectAuraPeriod") or 0) / 1000 or (2.0 if e["Effect"] == 27 else 3.0)
                tot += e["EffectBasePointsF"] * max(1, round((s["duration_ms"] or 20000) / 1000 / per))
        return tot

    def act(self):
        sim = self.sim
        if sim.t >= sim.end:
            return
        gcd = 1.5
        if self.racial and self.ready("racial"):
            self.buffs["racial"] = sim.t + self.racial[2]
            self.cds["racial"] = sim.t + self.racial[3]
        if self.tr("Bestial Wrath") and self.pet and self.ready("bw"):
            self.buffs["bw"] = sim.t + BESTIAL_WRATH[1]
            self.cds["bw"] = sim.t + BESTIAL_WRATH[2]
            sim.cast("Bestial Wrath")
        if self.tr("Intimidation") and self.pet and self.ready("intim"):
            self.intim = True
            self.cds["intim"] = sim.t + INTIMIDATION_CD
            sim.cast("Intimidation")
        if self.rw:
            self.do_rapid()
        for name, fn in self.priority():
            self.next_act = gcd
            if fn():
                sim.at(sim.t + self.next_act, self.act)
                return
        sim.at(sim.t + 0.5, self.act)

    def priority(self):
        if self.rw:
            return [("Aspect of the Hawk", self.do_aspect), ("Hunter's Mark", self.do_mark),
                    ("Summon Hawk", self.do_hawk), ("Serpent Sting", self.do_sting),
                    ("Aimed Shot", self.do_aimed), ("Multi-Shot", self.do_multi),
                    ("Arcane Shot", self.do_arcane), ("Trap", self.do_trap)]
        return [("Aspect of the Hawk", self.do_aspect), ("Hunter's Mark", self.do_mark),
                ("Mongoose Bite", self.do_mb), ("Summon Hawk", self.do_hawk),
                ("Strider Kick", self.do_kick), ("Trap", self.do_trap)]

    def pay(self, s, **kw):
        c = self.cost(s, **kw)
        if c > self.mana:
            return False
        self.spend(c)
        return True

    def do_aspect(self):
        s = self.spell("Aspect of the Hawk")
        if not s or not (self.tr("Summon Hawk") or self.rw) or self.up("aspect") or not self.pay(s):
            return False
        self.buffs["aspect"] = 1e9
        self.sim.cast("Aspect of the Hawk")
        return True

    def do_mark(self):
        s = self.spell("Hunter's Mark")
        if not s or not (self.tr("Summon Hawk") or self.tr("Expose Prey") or self.rw) or self.up("mark") \
                or not self.pay(s):
            return False
        self.buffs["mark"] = self.sim.t + s["duration_ms"] / 1000
        self.sim.cast("Hunter's Mark")
        return True

    def do_mb(self):
        s = self.spell("Mongoose Bite")
        if not s or self.mb_until < self.sim.t or not self.ready("mb") or not self.pay(s, melee=True):
            return False
        self.mb_until = -1
        self.cds["mb"] = self.sim.t + s["category_cooldown_ms"] / 1000
        base = self.weapon_avg + self.ap / 14 * NORMALIZED_SPEED + s["effects"][0]["EffectBasePointsF"]
        dmg = self.yellow("Mongoose Bite", base)
        if dmg and self.tr("Lacerating Strikes"):
            self.lacerate(dmg)
        return True

    def do_kick(self):
        s = self.spell("Strider Kick")
        if not s or not self.ready("kick") or not self.pay(s, melee=True):
            return False
        self.cds["kick"] = self.sim.t + s["cooldown_ms"] / 1000
        pct = s["effects"][1]["EffectBasePointsF"] / 100
        self.yellow("Strider Kick", (self.weapon_avg + self.ap / 14 * self.speed) * pct)
        return True

    def do_hawk(self):
        s = self.spell("Summon Hawk")
        if not s or not self.ready("hawk"):
            return False
        self.hawks = [h for h in self.hawks if h > self.sim.t]
        if len(self.hawks) >= s["effects"][2]["EffectBasePointsF"] or not self.pay(s):
            return False
        self.cds["hawk"] = self.sim.t + s["category_cooldown_ms"] / 1000
        self.sim.cast("Summon Hawk")
        dive = self.hawk_damage(s)
        self.hawk_strike("Hawk: dive", dive)
        every, frac, dur = HAWK_FOLLOWUP
        self.hawks.append(self.sim.t + dur)
        for i in range(1, int(dur / every) + 1):
            self.sim.at(self.sim.t + i * every, self.hawk_strike, "Hawk: attacks", dive * frac)
        return True

    def do_trap(self):
        tr = self.trap()
        if not tr or not self.ready("trap"):
            return False
        name, eff, place = tr[:3]
        if not self.pay(place, trap=True):
            return False
        cd = place["category_cooldown_ms"] / 1000 * (1 - self.tr("Survivalist's Discipline") * TT["Survivalist's Discipline"])
        self.cds["trap"] = self.sim.t + cd
        self.sim.cast(name)
        if core.spell_roll(self.sim.rng, self.ch, can_crit=False) == "miss":
            return True
        mult = self.player_mult() * (1 + self.tr("Clever Traps") * TT["Clever Traps"])
        for e in eff["effects"]:
            if e["Effect"] == 2:
                self.sim.deal(name, e["EffectBasePointsF"] * mult)
            elif e["Effect"] in (6, 27):
                per = (e.get("EffectAuraPeriod") or 0) / 1000 or (2.0 if e["Effect"] == 27 else 3.0)
                n = max(1, round((eff["duration_ms"] or 20000) / 1000 / per))
                for i in range(1, n + 1):
                    self.sim.at(self.sim.t + i * per, self.sim.deal, name, e["EffectBasePointsF"] * mult)
        return True


def _run(spec, race, level, iterations, seed, use_pet):
    holder = {}

    def build(sim):
        h = Hunter(sim, spec, race, level, use_pet)
        h.start()
        holder["h"] = h

    out = core.run_many(build, iterations, seed)
    out["inputs"] = dict(holder["h"].inp)
    out["pet"] = holder["h"].pet
    return out


def simulate(spec, race, level, iterations=200, seed=1):
    out = _run(spec, race, level, iterations, seed, True)
    if talents_at(spec, level).get("Lone Wolf"):
        alone = _run(spec, race, level, iterations, seed, False)
        if alone["dps_mean"] > out["dps_mean"]:
            out = alone
    return out
