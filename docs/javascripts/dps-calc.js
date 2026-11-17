/* Forever Codex DPS calculator.
   Steady-state expected-damage model for every race + DPS spec pair.
   Every input carries a source tag:
     F  = Forever value (Wowhead Forever, Blizzard notes, client tooltips)
     FE = Forever estimate (third-party, "not yet tested")
     C  = Classic 1.12 value checked on Wowhead Classic / warcraft.wiki.gg
     CU = Classic value not checked against a page
     A  = assumption made for this calculator (no source)
   Research notes live in .research/dps/*.md. */
(function () {
  "use strict";
  var SCRIPT_SRC = document.currentScript ? document.currentScript.src : "";

  // ---------- Inputs ----------
  // Global combat model. Every row: [value, tag, note]
  var MODEL = {
    fight:        [180, "A", "Fight length in seconds"],
    bossLevel:    [63, "C", "Boss level (warcraft.wiki.gg Glancing blow)"],
    bossArmor:    [3731, "CU", "Boss armor before debuffs"],
    meleeMiss:    [8, "C", "Melee miss vs level 63 at 300 skill, %"],
    dwPenalty:    [19, "C", "Extra white miss when dual wielding, %"],
    dodge:        [6.5, "CU", "Boss dodge, % (attacks from behind)"],
    glanceRate:   [40, "C", "White swings that glance, %"],
    glanceDmg:    [65, "C", "Glancing damage, % of normal"],
    critSuppress: [1.8, "CU", "Crit lost against a +3 boss, %"],
    spellHit:     [83, "C", "Base spell hit vs +3 boss, % (wiki page says 85: conflict)"],
    meleeCritMul: [2.0, "CU", "Melee crit multiplier"],
    spellCritMul: [1.5, "CU", "Spell crit multiplier"],
    baseMeleeCrit:[5, "CU", "Base melee crit before Agility, %"]
  };

  // Raid buffs and debuffs (on/off + value).
  var BUFFS = {
    might:     [true, 133, "F", "Blessing of Might, melee AP"],
    shout:     [true, 139, "FE", "Battle Shout, melee AP (raid-wide)"],
    kings:     [true, 10, "F", "Blessing of Kings, % all stats"],
    motw:      [true, 16, "F", "Mark/Gift of the Wild, all stats"],
    soe:       [true, 53, "F", "Strength of Earth Totem, Strength"],
    goa:       [true, 89, "F", "Grace of Air Totem, Agility"],
    wfTotem:   [true, 246, "F", "Windfury Totem: 20% for 1 extra attack with +AP on main-hand hits, specials included (all melee)"],
    lotp:      [true, 3, "F", "Leader of the Pack, % crit (all)"],
    moonkin:   [true, 3, "F", "Moonkin Aura, % crit (all, stacks with LotP)"],
    ai:        [true, 31, "F", "Arcane Brilliance, Intellect"],
    trueshot:  [true, 100, "F", "Trueshot Aura, ranged AP"],
    coe:       [true, 10, "F", "Curse of the Elements, % magic damage taken"],
    cos:       [true, 10, "F", "Curse of Shadow, % Shadow and Arcane damage taken"],
    sunder:    [true, 2250, "F", "Sunder Armor x5, armor removed"],
    ff:        [true, 2000, "F", "Faerie Fire, armor removed"],
    cor:       [true, 640, "F", "Curse of Recklessness, armor removed"]
  };

  // Race stat offsets versus Human (Classic race modifiers, Forever Tauren fix).
  // Skyborne have no published table: assumed equal to Night Elf.
  var RACES = {
    human:   { name: "Human", faction: "A", str: 0, agi: 0, int: 0, tag: "CU" },
    dwarf:   { name: "Dwarf", faction: "A", str: 2, agi: -4, int: -1, tag: "CU" },
    gnome:   { name: "Gnome", faction: "A", str: -5, agi: 3, int: 4, tag: "CU" },
    nelf:    { name: "Night Elf", faction: "A", str: -3, agi: 5, int: 0, tag: "CU" },
    sho:     { name: "Skyborne (High Order)", faction: "A", str: -3, agi: 5, int: 0, tag: "A" },
    orc:     { name: "Orc", faction: "H", str: 3, agi: -3, int: -3, tag: "CU" },
    troll:   { name: "Troll", faction: "H", str: 1, agi: 2, int: -4, tag: "CU" },
    tauren:  { name: "Tauren", faction: "H", str: 5, agi: -5, int: -5, tag: "F" },
    undead:  { name: "Undead", faction: "H", str: -1, agi: -2, int: -2, tag: "CU" },
    sws:     { name: "Skyborne (Windshaper)", faction: "H", str: -3, agi: 5, int: 0, tag: "A" }
  };

  // Racial effects (Wowhead Forever, patch 1.60.1).
  var RACIALS = {
    human:  [["crit", 1, 0, 0, "Ruthless +1% crit"]],
    dwarf:  [["hit", 1, 0, 0, "Artisan's Precision +1% hit"]],
    gnome:  [["direct", 10, 8, 120, "Eureka! +10% non-periodic damage, 8 s / 2 min (class scope: conflict)"]],
    nelf:   [["crit", 10, 15, 180, "Elune's Light +10% crit, 15 s / 3 min"]],
    sho:    [["haste", 2, 0, 0, "Wind Blessed +2% haste"]],
    sws:    [["haste", 2, 0, 0, "Wind Blessed +2% haste"]],
    orc:    [["power", 10, 15, 120, "Blood Fury +10% AP and spell power, 15 s / 2 min"], ["pet", 5, 0, 0, "Command +5% pet damage"]],
    troll:  [["haste", 10, 15, 180, "Berserking +10% haste, 15 s / 3 min"]],
    tauren: [],
    undead: []
  };

  // Which races each class can be (docs/characters/races.md matrix).
  var CLASS_RACES = {
    warrior: ["human", "dwarf", "gnome", "nelf", "sho", "orc", "troll", "tauren", "undead", "sws"],
    paladin: ["human", "dwarf", "undead"],
    hunter:  ["human", "dwarf", "nelf", "sho", "orc", "troll", "tauren", "sws"],
    rogue:   ["human", "dwarf", "gnome", "nelf", "sho", "orc", "troll", "undead", "sws"],
    priest:  ["human", "dwarf", "gnome", "nelf", "troll", "undead"],
    shaman:  ["dwarf", "orc", "troll", "tauren", "sws"],
    mage:    ["human", "gnome", "sho", "orc", "troll", "undead"],
    warlock: ["human", "gnome", "orc", "troll", "undead"],
    druid:   ["nelf", "sho", "tauren", "sws"]
  };

  // Gear profiles: total character stats for a Human in pre-raid gear (raids open 2026-12-09).
  // These are ASSUMPTIONS unless noted; edit them to match real gear.
  var GEAR = {
    melee2h: { str: 277, agi: 181, int: 40, ap: 114, hit: 9, crit: 7.5, mh: [203, 3.3], tag: "FE",
      note: "Kami-Labs Arms pre-raid totals (157 Str, 101 Agi, 114 AP, 9% hit, 7.5% crit) + Classic Warrior base; Forest Defender's Axe 162-244, 3.3 (warcraftdb)" },
    meleeDw: { str: 260, agi: 200, int: 40, ap: 120, hit: 9, crit: 7, mh: [120, 2.6], oh: [95, 2.6], tag: "A",
      note: "Assumed Fury pre-raid totals; one-hand weapons assumed" },
    rogue:   { str: 130, agi: 330, int: 40, ap: 120, hit: 7, crit: 6, mh: [118, 2.7], oh: [70, 1.8], tag: "A",
      note: "Assumed Combat pre-raid totals; sword main hand, fast off hand" },
    hunter:  { str: 70, agi: 330, int: 120, ap: 0, rap: 160, hit: 7, crit: 4, ranged: [118, 3.0], ammo: 20, tag: "A",
      note: "Assumed MM pre-raid totals; ranged weapon and ammo assumed" },
    ret:     { str: 260, agi: 110, int: 150, ap: 90, sp: 60, hit: 6, crit: 6, mh: [203, 3.3], tag: "A",
      note: "Assumed Ret pre-raid totals; Forest Defender's Axe (warcraftdb)" },
    enh:     { str: 230, agi: 120, int: 160, ap: 110, sp: 60, hit: 6, crit: 5, mh: [203, 3.3], tag: "A",
      note: "Assumed Enhancement pre-raid totals; Forest Defender's Axe (warcraftdb)" },
    cat:     { str: 160, agi: 260, int: 120, ap: 120, hit: 7, crit: 6, tag: "A",
      note: "Assumed Feral pre-raid totals" },
    caster:  { int: 260, sp: 380, hit: 6, crit: 4, tag: "A",
      note: "Assumed caster pre-raid totals (spell power, % hit, % crit from gear)" }
  };

  // Ability values. [value, tag]
  var V = {
    bt:        [[0.45, 30], "F", "Bloodthirst 45% AP + 30, 6 s"],
    ms:        [160, "F", "Mortal Strike normalized weapon + 160, 6 s"],
    slam:      [87, "F", "Slam weapon + 87, 15 s cd"],
    hs:        [157, "F", "Heroic Strike +157"],
    execute:   [[600, 15, 20], "F", "Execute 600 + 15 per extra rage; 20 extra rage per cast assumed (A)"],
    execPhase: [20, "A", "Execute phase, % of the fight (boss below 20% health)"],
    ww:        [10, "C", "Whirlwind normalized weapon, 10 s (8 s with Improved Whirlwind)"],
    deathWish: [20, "F", "Death Wish +20% physical, 30 s / 3 min"],
    ss:        [68, "C", "Sinister Strike normalized + 68, 40 energy after Efficient Strikes"],
    evisc:     [958, "CU", "Eviscerate 5 CP average"],
    snd:       [30, "C", "Slice and Dice +30% attack speed"],
    instPois:  [[0.2, 88], "F", "Instant Poison VI 20% for 76-100 (AP scaling unknown)"],
    deadly:    [[92, 12, 5], "F", "Deadly Poison V 92 over 12 s, 5 stacks"],
    aimed:     [1260, "FE", "Aimed Shot +1260 (Classic +600, Forever +110%)"],
    multi:     [150, "C", "Multi-Shot +150, 10 s"],
    arcaneShot:[183, "C", "Arcane Shot 183, 6 s"],
    petShare:  [20, "A", "Hunter pet as % of hunter damage (no Forever pet data)"],
    soc:       [[7, 0.7], "CU", "Seal of Command 7 PPM, 70% weapon damage"],
    judge:     [74, "F", "Judgement of Command 74 Holy (tooltip), 8 s"],
    stormstrike:[1.5, "F", "Stormstrike 150% weapon, 6 s"],
    wfWeapon:  [[0.2, 2, 333], "CU", "Windfury Weapon 20%, 2 extra attacks (Forever), +333 AP"],
    earthShock:[[517, 0.386], "C", "Earth Shock 517 + 0.386 SP"],
    lb:        [[452, 0.857, 2.5], "CU", "Lightning Bolt Classic r10 average, 2.5 s with talents (Forever value unclear)"],
    shred:     [[2.0, 80], "F", "Shred 200% weapon + 80, 42 energy"],
    catWeapon: [55, "CU", "Cat form base weapon DPS-equivalent at 1.0 speed"],
    fireball:  [[483, 60, 1.0, 3.0], "F", "Fireball 425-541 + 60 DoT, 3.0 s; coefficient 1.0 is Classic"],
    frostbolt: [[475, 0.814, 2.5], "F", "Frostbolt 457-493, 2.5 s; coefficient 0.814 is Classic"],
    arcaneBlast:[[236, 0.429, 1.5], "F", "Arcane Blast 218-254, 1.5 s; coefficient assumed 1.5/3.5"],
    shadowBolt:[[277.5, 0.857, 2.5], "F", "Shadow Bolt 263-292, SP mod 0.857 (Wowhead Forever)"],
    corruption:[[438, 18, 1.2], "F", "Corruption 438 over 18 s; 0.2 SP per tick (client)"],
    agony:     [[552, 24, 1.596], "F", "Bane of Agony 552 over 24 s; 0.133 SP per tick (client)"],
    siphon:    [[410, 30, 0.5], "F", "Siphon Life 410 over 30 s; 0.05 SP per tick (client)"],
    wrack:     [[60.2, 0.2002], "F", "Wrack 60.2 dps + 0.2002 SP per second (client, after the 10 November hotfix)"],
    immolate:  [[158, 275, 15, 0.2, 0.65], "F", "Immolate 158 + 275 over 15 s"],
    conflag:   [[282, 10, 0.429], "F", "Conflagrate 251-313, 10 s"],
    mindFlay:  [[390, 3, 0.45], "F", "Mind Flay 390 over 3 s"],
    mindBlast: [[485, 5.5, 0.429], "F", "Mind Blast 472-498, 5.5 s cd"],
    swp:       [[762, 24, 1.0], "F", "Shadow Word: Pain 762, 24 s with talent"],
    dp:        [[848, 24, 0.5], "F", "Devouring Plague 848 over 24 s, 24 s cd"],
    swd:       [[448, 18, 0.429], "F", "Shadow Word: Death 434-462, 18 s cd"],
    starfire:  [[533, 1.0, 2.6], "F", "Starfire 490-576; ~2.6 s with talents and Eclipse"],
    moonfire:  [[135, 240, 15, 0.15, 0.52], "F", "Moonfire 124-146 + 240 over 15 s"],
    swarm:     [[186, 14, 0.76], "F", "Insect Swarm 186 over 14 s"]
  };

  var SPECS = [
    { id: "fury", cls: "warrior", name: "Fury", build: "17/34/0", gear: "meleeDw" },
    { id: "arms", cls: "warrior", name: "Arms", build: "33/18/0", gear: "melee2h" },
    { id: "combat", cls: "rogue", name: "Combat", build: "16/35/0", gear: "rogue" },
    { id: "mm", cls: "hunter", name: "Marksmanship", build: "5/46/0", gear: "hunter" },
    { id: "ret", cls: "paladin", name: "Retribution", build: "12/8/31", gear: "ret" },
    { id: "enh", cls: "shaman", name: "Enhancement", build: "8/35/8", gear: "enh" },
    { id: "ele", cls: "shaman", name: "Elemental", build: "31/9/11", gear: "caster" },
    { id: "feral", cls: "druid", name: "Feral (Cat)", build: "9/32/10", gear: "cat" },
    { id: "balance", cls: "druid", name: "Balance", build: "36/0/15", gear: "caster" },
    { id: "fire", cls: "mage", name: "Fire", build: "12/36/3", gear: "caster" },
    { id: "frost", cls: "mage", name: "Frost", build: "15/5/31", gear: "caster" },
    { id: "arcane", cls: "mage", name: "Arcane", build: "38/10/3", gear: "caster" },
    { id: "affli", cls: "warlock", name: "Affliction (Wrack)", build: "33/0/18", gear: "caster" },
    { id: "destro", cls: "warlock", name: "Destruction", build: "14/4/33", gear: "caster" },
    { id: "shadow", cls: "priest", name: "Shadow", build: "20/0/31", gear: "caster" }
  ];

  // Inputs each spec depends on, for the confidence column.
  var DEPS = {
    fury: ["bt", "hs", "ww", "deathWish"], arms: ["ms", "slam", "hs", "ww", "deathWish"],
    combat: ["ss", "evisc", "snd", "instPois", "deadly"], mm: ["aimed", "multi", "arcaneShot", "petShare"],
    ret: ["soc", "judge"], enh: ["stormstrike", "wfWeapon", "earthShock"], ele: ["lb"],
    feral: ["shred", "catWeapon"], balance: ["starfire", "moonfire", "swarm"],
    fire: ["fireball"], frost: ["frostbolt"], arcane: ["arcaneBlast"],
    affli: ["corruption", "agony", "siphon", "wrack", "shadowBolt"], destro: ["shadowBolt", "immolate", "conflag"],
    shadow: ["mindFlay", "mindBlast", "swp", "dp", "swd"]
  };

  // Int per 1% spell crit and base spell crit (Classic, unchecked).
  var SPELLCRIT = { mage: [59.5, 0.2], warlock: [60.6, 1.7], priest: [59.2, 0.8], druid: [60, 1.8], shaman: [59.2, 2.3], paladin: [54, 0] };
  // Agility per 1% melee crit (RankedBoost Forever estimate).
  var AGICRIT = { hunter: 53, rogue: 29 };

  // ---------- Engine ----------
  function m(k) { return MODEL[k][0]; }
  function b(k) { return BUFFS[k][0] ? BUFFS[k][1] : 0; }
  function v(k) { return V[k][0]; }
  // Execute phase: the last part of the fight swaps fillers for Execute on every free GCD (A).
  function withExecute(normal, base, freeGcdShare, y) {
    var e = v("execute"), f = v("execPhase") / 100;
    var exec = (e[0] + e[1] * e[2]) * y.avg * freeGcdShare / 1.5;
    return normal * (1 - f) + (base + exec) * f;
  }
  function clamp(x, lo, hi) { return Math.max(lo, Math.min(hi, x)); }

  // Average uptime of a cooldown used on cooldown from the pull.
  function uptime(dur, cd) {
    var T = m("fight"); if (!cd) return 1; var t = 0, up = 0;
    while (t < T) { up += Math.min(dur, T - t); t += cd; }
    return up / T;
  }

  function stats(spec, raceId, st) {
    var g = GEAR[spec.gear], r = RACES[raceId], kings = 1 + b("kings") / 100;
    var s = {
      str: ((g.str || 0) + r.str + b("motw") + b("soe")) * kings,
      agi: ((g.agi || 0) + r.agi + b("motw") + b("goa")) * kings,
      int: ((g.int || 0) + r.int + b("motw") + b("ai")) * kings,
      hit: (g.hit || 0) + (st.hit || 0),
      critBonus: (st.crit || 0) + b("lotp") + b("moonkin") - m("critSuppress"),
      haste: 1 + (st.haste || 0) / 100,
      powerMul: 1 + (st.power || 0) / 100,
      directMul: 1 + (st.direct || 0) / 100,
      petMul: 1 + (st.pet || 0) / 100,
      sp: (g.sp || 0)
    };
    var cls = spec.cls;
    // Melee AP (warcraft.wiki.gg, Classic formulas)
    var ap;
    if (cls === "warrior" || cls === "paladin") ap = 180 + s.str * 2 - 20;
    else if (cls === "rogue" || cls === "shaman") ap = 120 + s.str + s.agi * 2 - 20;
    else if (cls === "hunter") ap = 120 + s.str + s.agi - 20;
    else if (cls === "druid") ap = 180 + s.str * 2 - 20 + s.agi + 12 + 90; // cat form: + Agi + 12, Predatory Strikes 150% of level
    else ap = s.str * 2 - 20;
    ap += (g.ap || 0) + b("might");
    ap += b("shout"); // shouts are raid-wide in Forever (F)
    if (spec.id === "enh") ap += s.int * 1.5; // Mental Dexterity (F)
    s.ap = ap * s.powerMul;
    s.rap = (120 + s.agi * 2 - 20 + (g.rap || 0) + b("trueshot") + 120) * s.powerMul; // + Aspect of the Hawk (FE)
    var agiPer = AGICRIT[cls] || 20;
    s.meleeCrit = m("baseMeleeCrit") + s.agi / agiPer + (g.crit || 0) + s.critBonus;
    var sc = SPELLCRIT[cls] || [60, 1];
    s.spellCrit = sc[1] + s.int / sc[0] + (g.crit || 0) + s.critBonus;
    s.sp = s.sp * s.powerMul;
    var red = b("sunder") + b("ff") + b("cor");
    var armor = Math.max(0, m("bossArmor") - red);
    s.armorMul = 1 - armor / (armor + 5500);
    return s;
  }

  // Melee outcome table. Returns average multiplier on a hit.
  function whiteMul(s, dw, critMul) {
    var miss = clamp(m("meleeMiss") + (dw ? m("dwPenalty") : 0) - s.hit, 0, 100) / 100;
    var dodge = m("dodge") / 100, glance = m("glanceRate") / 100;
    var crit = clamp(s.meleeCrit / 100, 0, 1 - miss - dodge - glance);
    var hit = 1 - miss - dodge - glance - crit;
    return { avg: hit + crit * critMul + glance * m("glanceDmg") / 100, crit: crit };
  }
  function yellowMul(s, critMul, extraCrit) {
    var miss = clamp(m("meleeMiss") - s.hit, 0, 100) / 100, dodge = m("dodge") / 100;
    var crit = clamp((s.meleeCrit + (extraCrit || 0)) / 100, 0, 1);
    var land = 1 - miss - dodge;
    return { avg: land * (1 - crit + crit * critMul), crit: crit * land, land: land };
  }
  function spellMul(s, critMul, extraCrit, extraHit) {
    var hit = clamp(m("spellHit") + s.hit + (extraHit || 0), 0, 99) / 100;
    var crit = clamp((s.spellCrit + (extraCrit || 0)) / 100, 0, 1);
    return hit * (1 - crit + crit * critMul);
  }
  function spellHitOnly(s, extraHit) { return clamp(m("spellHit") + s.hit + (extraHit || 0), 0, 99) / 100; }
  function flurryHaste(critChance, pct) { return 1 + pct / 100 * (1 - Math.pow(1 - critChance, 3)); }

  var MODELS = {
    fury: function (s) {
      var g = GEAR.meleeDw, cm = m("meleeCritMul");
      var y = yellowMul(s, cm + 0.2 * 0 , 5), w = whiteMul(s, true, cm);
      var crit = s.meleeCrit / 100 + 0.05;
      var haste = s.haste * flurryHaste(crit, 30);
      var mhAvg = g.mh[0] + s.ap / 14 * g.mh[1], ohAvg = (g.oh[0] + s.ap / 14 * g.oh[1]) * 0.5 * 1.25;
      var mhSw = haste / g.mh[1], ohSw = haste / g.oh[1];
      var hsShare = 0.5; // share of MH swings turned into Heroic Strike (A)
      var white = mhSw * (1 - hsShare) * mhAvg * w.avg + ohSw * ohAvg * w.avg;
      var hs = mhSw * hsShare * (mhAvg + v("hs")) * y.avg;
      var bt = (v("bt")[0] * s.ap + v("bt")[1]) * y.avg / 6;
      var ww = (g.mh[0] + s.ap / 14 * 2.4) * y.avg / 8;
      var wf = b("wfTotem") ? mhSw * 0.2 * (g.mh[0] + (s.ap + b("wfTotem")) / 14 * g.mh[1]) * w.avg : 0;
      var dw = 1 + v("deathWish") / 100 * uptime(30, 180);
      var whiteAll = mhSw * mhAvg * w.avg + ohSw * ohAvg * w.avg; // no Heroic Strike while executing
      return withExecute(white + hs + bt + ww + wf, whiteAll + bt + wf, 0.75, y) * dw * s.armorMul * s.directMul; // Bloodthirst keeps 1 GCD in 4
    },
    arms: function (s) {
      var g = GEAR.melee2h, cm = m("meleeCritMul");
      var y = yellowMul(s, cm + 0.2), w = whiteMul(s, false, cm);
      var haste = s.haste * flurryHaste(s.meleeCrit / 100, 30);
      var avg = g.mh[0] + s.ap / 14 * g.mh[1], norm = g.mh[0] + s.ap / 14 * 3.3;
      var sw = haste / g.mh[1], hsShare = 0.3;
      var white = sw * (1 - hsShare) * avg * w.avg, hs = sw * hsShare * (avg + v("hs")) * y.avg;
      var ms = (norm + v("ms")) * y.avg / 6, slam = (avg + v("slam")) * y.avg / 15, ww = norm * y.avg / 10;
      var wf = b("wfTotem") ? sw * 0.2 * (g.mh[0] + (s.ap + b("wfTotem")) / 14 * g.mh[1]) * w.avg : 0;
      var critsPerSec = sw * w.crit + (1 / 6 + 1 / 15 + 1 / 10) * y.crit;
      var deep = 0.6 * g.mh[0] / 12 * (1 - Math.exp(-critsPerSec * 12)); // Deep Wounds 60% avg weapon over 12 s (F)
      var dw = 1 + v("deathWish") / 100 * uptime(30, 180);
      var phys = withExecute(white + hs + ms + slam + ww + wf, sw * avg * w.avg + ms + wf, 0.75, y); // Mortal Strike keeps 1 GCD in 4
      return (phys * s.armorMul + deep) * 1.06 * dw * s.directMul; // Two-Handed Spec +6% (F)
    },
    combat: function (s) {
      var g = GEAR.rogue, cm = m("meleeCritMul");
      var y = yellowMul(s, cm + 0.2), w = whiteMul(s, true, cm);
      var haste = s.haste * (1 + v("snd") / 100) * (1 + 0.2 * uptime(15, 120)); // Blade Flurry
      var mhAvg = g.mh[0] + s.ap / 14 * g.mh[1], ohAvg = (g.oh[0] + s.ap / 14 * g.oh[1]) * 0.5 * 1.5;
      var white = (haste / g.mh[1] * mhAvg + haste / g.oh[1] * ohAvg) * w.avg;
      var ssDmg = (g.mh[0] + s.ap / 14 * 2.4 + v("ss")) * 1.15 * y.avg;
      var energy = 10 + (25 + 15 - 5) / (10 - 2); // regen + Shank r2 (+25, 5 cost, 10 s) with Flash of Steel 5/5 (+15, -2 s cd) (F)
      var cycleE = 5 * 40 + 20, cycleT = cycleE / energy; // 5 SS + Eviscerate
      var evis = v("evisc") * 1.15 * 1.2 * y.avg;
      var special = (5 * ssDmg + evis) / cycleT;
      var wf = b("wfTotem") ? (haste / g.mh[1] + 5 / cycleT) * 0.2 * (g.mh[0] + (s.ap + b("wfTotem")) / 14 * g.mh[1]) * w.avg : 0; // procs from main-hand swings and Sinister Strike (F)
      var hits = (haste / g.mh[1] + haste / g.oh[1]) * (1 - m("meleeMiss") / 100);
      var pois = hits * 0.5 * v("instPois")[0] * v("instPois")[1] * spellHitOnly(s) + v("deadly")[0] / v("deadly")[1] * v("deadly")[2] * spellHitOnly(s);
      return ((white + special + wf) * s.armorMul + pois) * s.directMul;
    },
    mm: function (s) {
      var g = GEAR.hunter, cm = m("meleeCritMul");
      var y = yellowMul(s, cm + 0.3, 0);
      var speed = g.ranged[1] / (s.haste * 1.15); // Quick Shots average (A)
      var shot = g.ranged[0] + g.ammo * g.ranged[1] + s.rap / 14 * g.ranged[1];
      var auto = shot / speed * y.avg;
      var aimed = (shot + v("aimed")) * 1.15 * y.avg / 9, multi = (shot + v("multi")) * 1.15 * y.avg / 10;
      var arc = (v("arcaneShot") + s.rap * 0.15) / 6 * y.avg;
      var own = (auto + aimed + multi) * s.armorMul + arc;
      return (own + own * v("petShare") / 100 * s.petMul) * s.directMul;
    },
    ret: function (s) {
      var g = GEAR.ret, cm = m("meleeCritMul");
      var conv = 6, w;
      s.meleeCrit += conv;
      w = whiteMul(s, false, cm);
      var y = yellowMul(s, cm);
      var sw = s.haste / g.mh[1], avg = g.mh[0] + s.ap / 14 * g.mh[1];
      var white = sw * avg * w.avg;
      var soc = sw * (v("soc")[0] * g.mh[1] / 60) * avg * v("soc")[1] * y.avg * 1.15 + sw * 0;
      var judge = (v("judge") + s.sp * 0.43) * spellMul(s, m("spellCritMul"), conv) / 8;
      var veng = 1 + 0.15 * (1 - Math.exp(-sw * w.crit * 30));
      var wf = b("wfTotem") ? sw * 0.2 * (g.mh[0] + (s.ap + b("wfTotem")) / 14 * g.mh[1]) * w.avg : 0;
      return ((white + wf) * s.armorMul + soc + judge) * veng * 1.06 * s.directMul; // SoC is Holy: no armor
    },
    enh: function (s) {
      var g = GEAR.enh, cm = m("meleeCritMul");
      var w = whiteMul(s, false, cm), y = yellowMul(s, cm);
      var haste = s.haste * flurryHaste(s.meleeCrit / 100, 30);
      var sw = haste / g.mh[1], avg = g.mh[0] + s.ap / 14 * g.mh[1];
      var wfv = v("wfWeapon"), wfAvg = g.mh[0] + (s.ap + wfv[2] * 1.4) / 14 * g.mh[1];
      var white = sw * avg * w.avg, wf = sw * wfv[0] * wfv[1] * wfAvg * y.avg;
      var ss = (g.mh[0] + s.ap / 14 * 3.3) * 1.5 * y.avg / 6;
      var es = (v("earthShock")[0] + v("earthShock")[1] * s.sp) * 1.2 * spellMul(s, m("spellCritMul")) / 6 * (1 + b("coe") / 100);
      return ((white + wf + ss) * s.armorMul + es) * s.directMul;
    },
    ele: function (s) {
      var lb = v("lb"), crit = 1.5 + 0.5; // Elemental Fury: +100% of the bonus
      var cast = lb[2] / s.haste;
      var dmg = (lb[0] + lb[1] * s.sp) * 1.05 * spellMul(s, crit, 5) * 1.15; // Concussion, Call of Thunder, Overload 30% x 50%
      return dmg / cast * (1 + b("coe") / 100) * s.directMul;
    },
    feral: function (s) {
      var cm = m("meleeCritMul"), w = whiteMul(s, false, cm), y = yellowMul(s, cm);
      var avg = v("catWeapon") + s.ap / 14;
      var white = s.haste * avg * w.avg;
      var shred = (avg * v("shred")[0] + v("shred")[1]) * 1.1 * y.avg;
      var special = shred * 10 / 42; // energy-limited Shred spam, finishers folded in (A)
      var wf = b("wfTotem") ? (s.haste + 10 / 42) * 0.2 * (v("catWeapon") + (s.ap + b("wfTotem")) / 14) * w.avg : 0; // claws count as a main hand (A)
      return (white + special + wf) * s.armorMul * s.directMul;
    },
    balance: function (s) {
      var sf = v("starfire"), crit = 2.0, mul = 1.1 * (1 + b("coe") / 100);
      var mf = v("moonfire"), is = v("swarm");
      var dotTime = 2 * 1.5 / s.haste;
      var mfDps = ((mf[0] + mf[3] * s.sp) * spellMul(s, crit) + (mf[1] + mf[4] * s.sp) * spellHitOnly(s)) / mf[2] * 1.1;
      var isDps = (is[0] + is[2] * s.sp) * spellHitOnly(s) / is[1];
      var sfDps = (sf[0] + sf[1] * s.sp) * spellMul(s, crit) / (sf[2] / s.haste);
      var fill = 1 - dotTime / 14;
      return (mfDps + isDps + sfDps * fill) * mul * s.directMul;
    },
    fire: function (s) {
      var f = v("fireball"), crit = s.spellCrit + 6;
      var mul = 1.12 * 1.15 * (1 + b("coe") / 100); // Fire Power, Improved Scorch 5 stacks (self), CoE
      var hitc = spellHitOnly(s, 6), cr = clamp(crit / 100, 0, 1);
      var direct = (f[0] + f[2] * s.sp) * hitc * (1 + cr * 0.5) * (1 + cr * 0.4); // Ignite 40%
      var dps = (direct + f[1] * hitc) / (f[3] / s.haste) * 0.92; // 8% of casts are Scorch refreshes (A)
      return dps * mul * s.directMul;
    },
    frost: function (s) {
      var f = v("frostbolt"), mul = 1.2 * (1 + b("coe") / 100); // Ice Barrier +15% +5%
      var dmg = (f[0] + f[1] * s.sp) * spellMul(s, 2.0, 0, 6);
      return dmg / (f[2] / s.haste) * mul * s.directMul;
    },
    arcane: function (s) {
      var a = v("arcaneBlast"), mul = (1 + 0.3 * uptime(15, 180)) * 1.03 * (1 + b("coe") / 100);
      var spStack = s.int * 0.12 * 2.5; // average 2.5 stacks of +12% Int as spell damage
      var dmg = (a[0] + a[1] * (s.sp + spStack)) * spellMul(s, 1.5 + 0.5, 6, 6);
      return dmg / (a[2] / s.haste) * mul * s.directMul;
    },
    affli: function (s) {
      var shadow = 1.1 * (1 + b("cos") / 100), crit = 1.5 + 0.5, h = spellHitOnly(s, 5);
      var cor = v("corruption"), ag = v("agony"), si = v("siphon"), wr = v("wrack");
      var dots = ((cor[0] + cor[2] * s.sp) / cor[1] * 1.1 + (ag[0] * 1.1 + ag[2] * s.sp) / ag[1] + (si[0] + si[2] * s.sp) / si[1]) * h * (1 + clamp((s.spellCrit + 5) / 100, 0, 1) * (crit - 1) * 0.5);
      var gcdShare = 3 * 1.5 / s.haste / 20;
      var wrack = (wr[0] + wr[1] * s.sp) * h * 1.36 * s.haste;
      var nf = 0.04 * (6 / 3 + 1) / 3 * (v("shadowBolt")[0] + v("shadowBolt")[1] * s.sp) * spellMul(s, 2.0, 5, 5);
      // While Wrack channels, the three DoTs tick twice as often and keep their duration
      return (dots * (2 - gcdShare) + wrack * (1 - gcdShare) + nf) * shadow;
    },
    destro: function (s) {
      var sb = v("shadowBolt"), im = v("immolate"), cf = v("conflag"), crit = 2.0;
      var sbDps = (sb[0] + sb[1] * s.sp) * spellMul(s, crit) / (sb[2] / s.haste);
      var isb = 1 + 0.2 * (1 - Math.pow(1 - clamp(s.spellCrit / 100, 0, 1), 4));
      var fire = (1 + b("coe") / 100) * 1.1 * 1.2;
      var imm = ((im[0] * 1.5 + im[3] * s.sp) * spellMul(s, crit) + (im[1] + im[4] * s.sp) * spellHitOnly(s)) / im[2];
      var cfd = (cf[0] + cf[2] * s.sp) * spellMul(s, crit, 25) / cf[1];
      var castShare = 1 - (2 / s.haste / im[2] + 1.5 / s.haste / cf[1]);
      return (sbDps * castShare * isb * 1.1 * (1 + b("cos") / 100) + (imm + cfd) * fire) * s.directMul;
    },
    shadow: function (s) {
      var mul = 1.1 * 1.1 * 1.1 * (1 + b("cos") / 100), h = spellHitOnly(s, 5), crit = 2.0;
      var mf = v("mindFlay"), mb = v("mindBlast"), pw = v("swp"), dp = v("dp"), sd = v("swd");
      var mbD = (mb[0] + mb[2] * s.sp) * spellMul(s, crit, 0, 5) / mb[1];
      var sdD = (sd[0] + sd[2] * s.sp) * spellMul(s, crit, 0, 5) / sd[1];
      var pwD = (pw[0] + pw[2] * s.sp) * h / pw[1], dpD = (dp[0] + dp[2] * s.sp) * h / dp[1];
      var busy = (1.5 / mb[1] + 1.5 / sd[1] + 1.5 / dp[1] + 1.5 / pw[1]) / s.haste;
      var mfD = (mf[0] + mf[2] * s.sp) * h / (mf[1] / s.haste) * 1.1;
      return (mbD + sdD + pwD + dpD + mfD * (1 - busy)) * mul * s.directMul;
    }
  };

  // DPS for one spec + race, blending racial cooldown uptime.
  function dps(spec, raceId) {
    var rac = RACIALS[raceId] || [], states = [{ w: 1, st: {} }];
    rac.forEach(function (r) {
      var kind = r[0], val = r[1], dur = r[2], cd = r[3], u = dur ? uptime(dur, cd) : 1;
      if (kind === "direct" && spec.id === "affli") val = val * 0.15; // mostly periodic damage
      var next = [];
      states.forEach(function (x) {
        var on = Object.assign({}, x.st); on[kind] = (on[kind] || 0) + val;
        next.push({ w: x.w * u, st: on });
        if (u < 1) next.push({ w: x.w * (1 - u), st: x.st });
      });
      states = next;
    });
    var total = 0;
    states.forEach(function (x) { total += x.w * MODELS[spec.id](stats(spec, raceId, x.st)); });
    return total;
  }

  function confidence(spec) {
    var tags = DEPS[spec.id].map(function (k) { return V[k][1]; });
    tags.push(GEAR[spec.gear].tag);
    var score = { F: 1, FE: 0.7, C: 0.5, CU: 0.3, A: 0 }, sum = 0;
    tags.forEach(function (t) { sum += score[t]; });
    return sum / tags.length;
  }

  function results() {
    var rows = [];
    SPECS.forEach(function (spec) {
      CLASS_RACES[spec.cls].forEach(function (r) {
        rows.push({ spec: spec, race: r, dps: dps(spec, r), conf: confidence(spec) });
      });
    });
    var bestBySpec = {};
    rows.forEach(function (x) { bestBySpec[x.spec.id] = Math.max(bestBySpec[x.spec.id] || 0, x.dps); });
    rows.forEach(function (x) { x.vsBest = x.dps / bestBySpec[x.spec.id] - 1; });
    return rows.sort(function (a, c) { return c.dps - a.dps; });
  }

  // ---------- UI ----------
  var TAGNAME = { F: "Forever", FE: "Forever est.", C: "Classic", CU: "Classic, unchecked", A: "Assumption" };
  var CLSNAME = { warrior: "Warrior", paladin: "Paladin", hunter: "Hunter", rogue: "Rogue", priest: "Priest", shaman: "Shaman", mage: "Mage", warlock: "Warlock", druid: "Druid" };
  function el(tag, attrs, kids) {
    var e = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) { if (k === "text") e.textContent = attrs[k]; else e.setAttribute(k, attrs[k]); });
    (kids || []).forEach(function (c) { if (c) e.appendChild(c); });
    return e;
  }
  function tagEl(t) { return el("span", { "class": "dps-tag dps-tag--" + t.toLowerCase(), title: TAGNAME[t], text: TAGNAME[t] }); }

  function render(root) {
    var state = { cls: [], faction: "all", race: "all", q: "", best: false }, ff = null, FF = window.ForeverFilters;
    var out = root.querySelector("[data-dps-results]");
    var filters = root.querySelector("[data-dps-filters]");

    function draw() {
      var all = results(), rows = all.filter(function (x) {
        return FF.match(state.cls, x.spec.cls) && FF.match(state.faction, RACES[x.race].faction) && FF.match(state.race, x.race) &&
          FF.text(state.q, [CLSNAME[x.spec.cls], x.spec.name, x.spec.id, RACES[x.race].name]);
      });
      if (state.best) {
        var seen = {}; rows = rows.filter(function (x) { if (seen[x.spec.id]) return false; seen[x.spec.id] = 1; return true; });
      }
      if (ff) ff.count(rows.length, state.best ? new Set(all.map(function (x) { return x.spec.id; })).size : all.length, state.best ? "specs" : "spec and race pairs");
      var top = rows.length ? rows[0].dps : 1;
      var tbody = el("tbody");
      rows.forEach(function (x, i) {
        var bar = el("span", { "class": "dps-bar", style: "--v:" + (x.dps / top * 100).toFixed(1) + "%" });
        var conf = Math.round(x.conf * 100);
        tbody.appendChild(el("tr", {}, [
          el("td", { text: String(i + 1) }),
          el("td", {}, [el("span", { "class": "pill pill--" + x.spec.cls, text: CLSNAME[x.spec.cls] })]),
          el("td", { text: x.spec.name }),
          el("td", { text: RACES[x.race].name }),
          el("td", { "class": "dps-num" }, [bar, el("strong", { text: Math.round(x.dps).toLocaleString() })]),
          el("td", { "class": "dps-num", text: x.vsBest === 0 ? "best" : (Math.abs(x.vsBest) < 0.0005 ? "tied" : (x.vsBest * 100).toFixed(1) + "%") }),
          el("td", { "class": "dps-num", title: "Share of this spec's inputs that are Forever-sourced", text: conf + "%" })
        ]));
      });
      var table = el("table", { "class": "dps-table" }, [
        el("thead", {}, [el("tr", {}, ["#", "Class", "Spec", "Race", "DPS", "vs best race", "Data confidence"].map(function (h) { return el("th", { scope: "col", text: h }); }))]),
        tbody
      ]);
      out.replaceChildren(el("div", { "class": "dps-scroll" }, [table]));
    }

    ff = FF.build(state, [
      { type: "chips", key: "cls", label: "Class", all: "All classes", pills: true, options: Object.keys(CLSNAME).map(function (c) { return [c, CLSNAME[c]]; }) },
      { type: "choice", key: "faction", label: "Faction", options: [["all", "Both"], ["A", "Alliance"], ["H", "Horde"]] },
      { type: "select", key: "race", label: "Race", options: [["all", "All races"]].concat(Object.keys(RACES).map(function (r) { return [r, RACES[r].name]; })) },
      { type: "search", key: "q", label: "Search", placeholder: "Spec, class or race" },
      { type: "toggle", key: "best", label: "Best race of each spec only" }
    ], draw, { label: "Filter the quick estimate" });
    filters.replaceChildren(ff.el);

    // Editable inputs
    function numInput(row, idx, onChange) {
      var i = el("input", { type: "number", step: "any", value: String(row[idx]) });
      i.addEventListener("input", function () { var n = parseFloat(i.value); if (!isNaN(n)) { onChange(n); draw(); } });
      return i;
    }
    function named(input, name) {      // a programmatic label: the visible name is in the neighbouring cell
      var target = input && input.matches && input.matches("input") ? input : input && input.querySelector ? input.querySelector("input") : null;
      if (target && !target.getAttribute("aria-label")) target.setAttribute("aria-label", name);
      return input;
    }
    var mTable = el("tbody");
    Object.keys(MODEL).forEach(function (k) {
      var row = MODEL[k];
      mTable.appendChild(el("tr", {}, [el("td", { text: row[2] }), el("td", {}, [named(numInput(row, 0, function (n) { row[0] = n; }), row[2])]), el("td", {}, [tagEl(row[1])])]));
    });
    var bTable = el("tbody");
    Object.keys(BUFFS).forEach(function (k) {
      var row = BUFFS[k], cb = el("input", { type: "checkbox", "aria-label": row[3] });
      cb.checked = row[0]; cb.addEventListener("change", function () { row[0] = cb.checked; draw(); });
      bTable.appendChild(el("tr", {}, [el("td", {}, [cb]), el("td", { text: row[3] }), el("td", {}, [named(numInput(row, 1, function (n) { row[1] = n; }), row[3] + ", value")]), el("td", {}, [tagEl(row[2])])]));
    });
    var vTable = el("tbody");
    Object.keys(V).forEach(function (k) {
      var row = V[k], val = row[0];
      var input = Array.isArray(val) ? el("code", { text: JSON.stringify(val) }) : named(numInput(row, 0, function (n) { row[0] = n; }), row[2]);
      vTable.appendChild(el("tr", {}, [el("td", { text: row[2] }), el("td", {}, [input]), el("td", {}, [tagEl(row[1])])]));
    });
    var gTable = el("tbody");
    Object.keys(GEAR).forEach(function (k) {
      var g = GEAR[k], fields = el("div", { "class": "dps-gear" });
      ["str", "agi", "int", "ap", "sp", "hit", "crit"].forEach(function (f) {
        if (g[f] === undefined) return;
        var i = el("input", { type: "number", step: "any", value: String(g[f]), "aria-label": k + " " + f });
        i.addEventListener("input", function () { var n = parseFloat(i.value); if (!isNaN(n)) { g[f] = n; draw(); } });
        fields.appendChild(el("label", {}, [el("span", { text: f }), i]));
      });
      gTable.appendChild(el("tr", {}, [el("td", { text: k }), el("td", {}, [fields, el("small", { text: g.note })]), el("td", {}, [tagEl(g.tag)])]));
    });
    function tbl(head, body) { return el("div", { "class": "dps-scroll" }, [el("table", { "class": "dps-inputs" }, [el("thead", {}, [el("tr", {}, head.map(function (h) { return el("th", { scope: "col", text: h }); }))]), body])]); }
    function box(title, content) {
      var t = content.querySelector && content.querySelector("table");
      if (t) t.setAttribute("data-caption", title + " inputs");
      return el("details", { "class": "note" }, [el("summary", { text: title }), content]);
    }
    var inputs = root.querySelector("[data-dps-inputs]");
    if (inputs) inputs.replaceChildren(
      box("Combat model", tbl(["Input", "Value", "Source"], mTable)),
      box("Raid buffs and debuffs", tbl(["On", "Buff or debuff", "Value", "Source"], bTable)),
      box("Gear profiles", tbl(["Profile", "Stats (Human totals)", "Source"], gTable)),
      box("Ability values", tbl(["Ability", "Value", "Source"], vTable)));
    draw();
  }

  // ---------- Simulated results (tools/sim, published by tools/sim/publish.py) ----------
  var simCache = null;
  function renderSim(box) {
    var url = new URL("../assets/data/sim-results.json", SCRIPT_SRC || location.href).href;
    var load = simCache ? Promise.resolve(simCache) : fetch(url).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); });
    load.then(function (rows) {
      simCache = rows;
      var state = { cls: [], faction: "all", race: "all", q: "", best: false }, ff = null, FF = window.ForeverFilters;
      var filters = el("div", { "class": "dps-filters" }), out = el("div");
      function draw() {
        var list = rows.filter(function (x) {
          var f = RACES[x.race] ? RACES[x.race].faction : "";
          return FF.match(state.cls, x.class) && FF.match(state.faction, f) && FF.match(state.race, x.race) &&
            FF.text(state.q, [CLSNAME[x.class], x.spec, x.build, x.race_name, RACES[x.race] && RACES[x.race].name]);
        });
        var best = {};
        rows.forEach(function (x) { var k = x.class + x.spec; best[k] = Math.max(best[k] || 0, x.dps_mean); });
        if (state.best) { var seen = {}; list = list.filter(function (x) { var k = x.class + x.spec; if (seen[k]) return false; seen[k] = 1; return true; }); }
        if (ff) ff.count(list.length, state.best ? Object.keys(best).length : rows.length, state.best ? "specs" : "spec and race pairs");
        var top = list.length ? list[0].dps_mean : 1, tbody = el("tbody");
        list.forEach(function (x, i) {
          var vs = x.dps_mean / best[x.class + x.spec] - 1, half = (x.ci95[1] - x.ci95[0]) / 2;
          var parts = Object.keys(x.breakdown).map(function (k) { return [k, x.breakdown[k]]; }).sort(function (a, c) { return c[1] - a[1]; });
          var det = el("details", { "class": "dps-breakdown" }, [el("summary", { text: x.spec })].concat([el("ul", {}, parts.map(function (p) {
            return el("li", { text: p[0] + ": " + Math.round(p[1]) + " DPS (" + Math.round(p[1] / x.dps_mean * 100) + "%)" });
          }))]));
          tbody.appendChild(el("tr", {}, [
            el("td", { text: String(i + 1) }),
            el("td", {}, [el("span", { "class": "pill pill--" + x.class, text: CLSNAME[x.class] || x.class })]),
            el("td", {}, [det]),
            el("td", { text: x.race_name || (RACES[x.race] && RACES[x.race].name) || x.race }),
            el("td", { "class": "dps-num" }, [el("span", { "class": "dps-bar", style: "--v:" + (x.dps_mean / top * 100).toFixed(1) + "%" }), el("strong", { text: Math.round(x.dps_mean).toLocaleString() }), el("small", { text: " ±" + half.toFixed(1) })]),
            el("td", { "class": "dps-num", text: Math.abs(vs) < 1e-9 ? "best" : (Math.abs(vs) < 0.0005 ? "tied" : (vs * 100).toFixed(1) + "%") }),
            el("td", { "class": "dps-num", text: Math.round(x.data_confidence * 100) + "%" })
          ]));
        });
        out.replaceChildren(el("div", { "class": "dps-scroll" }, [el("table", { "class": "dps-table" }, [
          el("thead", {}, [el("tr", {}, ["#", "Class", "Spec (open for breakdown)", "Race", "Estimated DPS", "vs best race", "Data confidence"].map(function (h) { return el("th", { scope: "col", text: h }); }))]), tbody])]));
      }
      ff = FF.build(state, [
        { type: "chips", key: "cls", label: "Class", all: "All classes", pills: true, options: Object.keys(CLSNAME).map(function (c) { return [c, CLSNAME[c]]; }) },
        { type: "choice", key: "faction", label: "Faction", options: [["all", "Both"], ["A", "Alliance"], ["H", "Horde"]] },
        { type: "select", key: "race", label: "Race", options: [["all", "All races"]].concat(Object.keys(RACES).map(function (r) { return [r, RACES[r].name]; })) },
        { type: "search", key: "q", label: "Search", placeholder: "Spec, class or race" },
        { type: "toggle", key: "best", label: "Best race of each spec only" }
      ], draw, { label: "Filter the simulated raid estimates" });
      filters.replaceChildren(ff.el);
      var r0 = rows[0] || {};
      box.replaceChildren(el("p", { "class": "dps-meta", text: rows.length + " spec and race pairs, " + (r0.iterations ? r0.iterations.toLocaleString("en-US") : "?") + " simulated fights of " + (r0.fight_seconds || "?") + " s each. ± is the 95% confidence interval of the simulation, not the error of the estimate." }), filters, out);
      draw();
    }).catch(function () { box.replaceChildren(el("p", { text: "The simulated estimates could not be loaded." })); });
  }

  // ---------- Build panel: full character for one row (tools/levelsim/spec_export.py) ----------
  var specCache = {};
  var SLOT_ORDER = ["head", "neck", "shoulder", "back", "chest", "wrist", "hands", "waist", "legs", "feet", "trinket1", "trinket2", "main_hand", "off_hand", "ranged"];
  var SLOT_NAME = { head: "Head", neck: "Neck", shoulder: "Shoulder", back: "Back", chest: "Chest", wrist: "Wrist", hands: "Hands", waist: "Waist", legs: "Legs", feet: "Feet", trinket1: "Trinket", trinket2: "Trinket", main_hand: "Main hand", off_hand: "Off hand", ranged: "Ranged" };
  var STAT_NAME = { str: "Strength", agi: "Agility", sta: "Stamina", int: "Intellect", spi: "Spirit", ap: "Attack power", rap: "Ranged attack power", sp_total: "Spell damage", hit: "Hit rating", crit: "Crit rating", mp5: "Mana per 5 s", defense: "Defense", dodge: "Dodge rating", parry: "Parry rating", block: "Block rating", healing: "Healing" };
  function specFile(x, gear) {
    var key = x.class + "-" + x.spec + "-" + gear;
    if (!specCache[key]) {
      var url = new URL("../assets/data/specs/" + key + ".json", SCRIPT_SRC || location.href).href;
      specCache[key] = fetch(url).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); });
    }
    return specCache[key];
  }
  function section(title, kids) { return el("section", { "class": "dps-spec-sec" }, [el("h4", { text: title })].concat(kids)); }
  // Charts and the level-by-level table of one class, spec, race and gear mode (all 60 levels of the build file).
  function acrossLevels(x, doc, level, gear, series) {
    var N = doc.names, lvls = Object.keys(doc.levels).map(Number).sort(function (a, b) { return a - b; });
    var per = lvls.map(function (lv) { return doc.levels[String(lv)].races[x.race] || { dps: null, ci: null, dmg: {} }; });
    var kids = [];
    // 1. this build with and without crafted gear
    var lines = [];
    if (series.crafted) lines.push({ name: "Best craftable gear", values: series.crafted, slot: 0 });
    if (series.none) lines.push({ name: "No gear", values: series.none, slot: 1 });
    var lineBox = el("div");
    kids.push(el("h5", { text: "DPS at every level" }), lineBox);
    // 2. damage by source: the five largest sources over all levels, the rest as "Other"
    var sum = {};
    per.forEach(function (r) { Object.keys(r.dmg).forEach(function (k) { sum[k] = (sum[k] || 0) + r.dmg[k]; }); });
    var order = Object.keys(sum).sort(function (a, b) { return sum[b] - sum[a]; }), top = order.slice(0, order.length > 6 ? 5 : 6), rest = order.slice(top.length);
    var stack = top.map(function (k, i) { return { name: N[k], slot: i, values: per.map(function (r) { return r.dmg[k] || 0; }) }; });
    if (rest.length) stack.push({ name: "Other (" + rest.length + " sources)", slot: 5, values: per.map(function (r) { return rest.reduce(function (s, k) { return s + (r.dmg[k] || 0); }, 0); }) });
    var stackBox = el("div");
    kids.push(el("h5", { text: "Damage by source at every level (" + (gear === "crafted" ? "best craftable gear" : "no gear") + ")" }), stackBox);
    // 3. the same numbers as a table: one row per level, with the talent point spent at that level
    function flat(lv) { var out = {}, t = doc.levels[String(lv)].talents; Object.keys(t).forEach(function (tree) { Object.keys(t[tree]).forEach(function (n) { out[n] = t[tree][n]; }); }); return out; }
    var prevT = {}, body = el("tbody");
    lvls.forEach(function (lv, i) {
      var r = per[i], cur = flat(lv), gained = Object.keys(cur).filter(function (n) { return cur[n] > (prevT[n] || 0); }).map(function (n) { return n + " " + cur[n]; });
      prevT = cur;
      var prev = i ? per[i - 1].dps : null, ch = prev ? (r.dps / prev - 1) * 100 : null;
      var parts = Object.keys(r.dmg).map(function (k) { return [N[k], r.dmg[k]]; }).sort(function (a, b) { return b[1] - a[1]; });
      var tot = parts.reduce(function (s, p) { return s + p[1]; }, 0) || 1;
      body.appendChild(el("tr", lv === level ? { "class": "is-open" } : {}, [
        el("td", { "class": "dps-num", text: String(lv) }),
        el("td", { "class": "dps-num" }, [el("strong", { text: r.dps == null ? "–" : r.dps.toFixed(1) }), el("small", { text: r.ci == null ? "" : " ±" + r.ci.toFixed(1) })]),
        el("td", { "class": "dps-num" + (ch == null ? "" : ch < 0 ? " dps-down" : ""), text: ch == null ? "–" : (ch >= 0 ? "+" : "") + ch.toFixed(1) + "%" }),
        el("td", { text: gained.join(", ") }),
        el("td", { text: parts.slice(0, 4).map(function (p) { return p[0] + " " + Math.round(p[1] / tot * 100) + "%"; }).join(", ") })]));
    });
    var tbl = el("table", { "class": "dps-inputs", "data-caption": "Level-by-level breakdown" }, [
      el("thead", {}, [el("tr", {}, ["Level", "DPS", "Change", "Talent point", "Largest damage sources"].map(function (h) { return el("th", { scope: "col", text: h }); }))]), body]);
    kids.push(el("details", { "class": "dps-levels" }, [el("summary", { text: "Level-by-level breakdown (all " + lvls.length + " levels)" }), el("div", { "class": "dps-scroll" }, [tbl])]));
    var sec = section("Across levels " + lvls[0] + "–" + lvls[lvls.length - 1], kids);
    // draw once the section is in the page, so the charts can measure their width
    setTimeout(function () {
      if (!window.ForeverCharts) return;
      window.ForeverCharts.draw(lineBox, { label: "DPS at every level, with and without crafted gear", x: lvls, xLabel: "Level", unit: "DPS", series: lines, marker: level });
      window.ForeverCharts.draw(stackBox, { label: "Damage by source at every level", x: lvls, xLabel: "Level", unit: "DPS", series: stack, stacked: true, marker: level });
    }, 0);
    return sec;
  }

  function specPanel(x, level, gear, series) {
    var box = el("div", { "class": "dps-spec" }, [el("p", { text: "Loading the build…" })]);
    specFile(x, gear).then(function (doc) {
      var L = doc.levels[String(level)], R = L && L.races[x.race];
      if (!R) { box.replaceChildren(el("p", { text: "No build data for this level." })); return; }
      var N = doc.names, raceName = (RACES[x.race] && RACES[x.race].name) || x.race;
      var kids = [el("p", { "class": "dps-spec-head" }, [
        el("strong", { text: "Level " + level + " " + raceName + " " + (CLSNAME[x.class] || x.class) + ", " + doc.spec_name }),
        el("span", { text: " · " + (gear === "crafted" ? "best craftable gear" : "no gear") + " · " + R.dps.toFixed(1) + " DPS (" + doc.iterations + " fights of " + doc.fight_seconds + " s)" })])];
      kids.push(acrossLevels(x, doc, level, gear, series || {}));
      // Talents
      var trees = Object.keys(L.talents).sort(function (p, q) { return L.points[q] - L.points[p]; });
      var pts = trees.map(function (t) { return L.points[t]; });
      kids.push(section("Talents" + (trees.length ? " (" + pts.join("/") + ")" : ""), trees.length ? [el("div", { "class": "dps-spec-trees" }, trees.map(function (t) {
        return el("div", {}, [el("h5", { text: t + " · " + L.points[t] }), el("ul", {}, Object.keys(L.talents[t]).map(function (n) { return el("li", { text: n + " " + L.talents[t][n] }); }))]);
      }))] : [el("p", { text: "No talent points before level 10." })]));
      // Gear
      if (L.gear) {
        var rowsG = SLOT_ORDER.filter(function (s) { return L.gear.items[s]; }).map(function (s) {
          var it = L.gear.items[s], ench = L.gear.enchants.filter(function (e) { return e.slot === s; }).map(function (e) { return e.name.indexOf("$") < 0 ? e.name : e.name.replace(/\+?\$k\d+\s*/, "") + " (amount not in client text)"; }).join(", ");
          return el("tr", {}, [el("td", { text: SLOT_NAME[s] || s }), el("td", { text: it.name }), el("td", { "class": "dps-num", text: String(it.ilvl) }), el("td", { text: ench })]);
        });
        var st = L.gear.stats, statTxt = Object.keys(STAT_NAME).filter(function (k) { return st[k]; }).map(function (k) { return STAT_NAME[k] + " " + st[k]; });
        Object.keys(st).filter(function (k) { return k.indexOf("sp_") === 0 && k !== "sp_total"; }).forEach(function (k) { statTxt.push(k.slice(3) + " spell damage " + st[k]); });
        kids.push(section("Gear", [el("div", { "class": "dps-scroll" }, [el("table", { "class": "dps-inputs" }, [
          el("thead", {}, [el("tr", {}, ["Slot", "Item", "Item level", "Enchant"].map(function (h) { return el("th", { scope: "col", text: h }); }))]),
          el("tbody", {}, rowsG)])]), el("p", { "class": "dps-meta", text: "Gear totals: " + statTxt.join(", ") + ". Empty slots have no craftable item." })]));
      } else {
        kids.push(section("Gear", [el("p", { text: "None: fights unarmed and unarmored." })]));
      }
      // Opening sequence
      var tl = R.tl, seq = [];
      for (var i = 0; i < tl.length; i += 2) seq.push(el("li", {}, [el("span", { "class": "dps-spec-t", text: (tl[i] / 10).toFixed(1) + " s" }), document.createTextNode(" " + N[tl[i + 1]])]));
      kids.push(section("Opening sequence", seq.length ? [el("ol", { "class": "dps-spec-seq" }, seq), el("p", { "class": "dps-meta", text: "The first " + seq.length + " abilities used in one simulated fight. White swings and automatic attacks are not listed." })] : [el("p", { text: "Auto-attacks only." })]));
      // Ability use and damage
      var cpm = Object.keys(R.cpm).map(function (k) { return [N[k], R.cpm[k]]; }).sort(function (a, b) { return b[1] - a[1]; });
      var dmg = Object.keys(R.dmg).map(function (k) { return [N[k], R.dmg[k]]; }).sort(function (a, b) { return b[1] - a[1]; });
      var tot = dmg.reduce(function (s, p) { return s + p[1]; }, 0) || 1;
      kids.push(el("div", { "class": "dps-spec-trees" }, [
        section("Casts per minute", [el("ul", {}, cpm.map(function (p) { return el("li", { text: p[0] + ": " + p[1] }); }))]),
        section("Damage by source", [el("ul", {}, dmg.map(function (p) { return el("li", { text: p[0] + ": " + p[1].toFixed(1) + " DPS (" + Math.round(p[1] / tot * 100) + "%)" }); }))])]));
      box.replaceChildren.apply(box, kids);
    }).catch(function () { box.replaceChildren(el("p", { text: "The build details could not be loaded." })); });
    return box;
  }

  // ---------- Level-by-level simulation (tools/levelsim, published by tools/levelsim/publish.py) ----------
  function renderLevels(box) {
    var url = new URL("../assets/data/level-sim.json", SCRIPT_SRC || location.href).href;
    fetch(url).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (data) {
      var levels = data.levels, rows = data.rows, MAXPIN = 6;
      var hasCrafted = rows.some(function (x) { return x.gear === "crafted"; });
      var state = { cls: [], level: levels[levels.length - 1], best: false, gear: hasCrafted ? "crafted" : "none", faction: "all", race: "all", q: "" };
      var pins = [];      // rows picked with Compare: { key, slot }; empty means the chart follows the top of the table
      var byKey = {};
      function keyOf(x) { return x.class + "|" + x.spec + "|" + x.race; }
      function nameOf(x) { return x.spec_name + " " + (CLSNAME[x.class] || x.class) + " · " + ((RACES[x.race] && RACES[x.race].name) || x.race); }
      rows.forEach(function (x) { byKey[keyOf(x) + "|" + (x.gear || "none")] = x; });
      var ff = null, FF = window.ForeverFilters, chart = null;
      var filters = el("div", { "class": "dps-filters" }), out = el("div");
      var chartBox = el("div"), trajSub = el("p"), clearBtn = el("button", { type: "button", "class": "dps-linkbtn", text: "Follow the top rows" });
      var numbers = el("div", { "class": "dps-scroll" });
      var traj = el("div", { "class": "dps-traj" }, [
        el("div", { "class": "dps-traj-head" }, [el("div", {}, [el("h3", { text: "DPS across levels " + levels[0] + "–" + levels[levels.length - 1] }), trajSub]), clearBtn]),
        chartBox,
        el("details", {}, [el("summary", { text: "Level-by-level numbers for the charted rows" }), numbers])]);
      clearBtn.addEventListener("click", function () { pins = []; draw(); });

      function drawChart(list) {
        var shown;
        if (pins.length) {
          shown = pins.map(function (p) { return { x: byKey[p.key + "|" + state.gear], slot: p.slot }; }).filter(function (p) { return p.x; });
        } else {      // no picks yet: the best row of each of the first four specs in the table
          var seenSpec = {}; shown = [];
          list.forEach(function (x) { var k = x.class + x.spec; if (seenSpec[k] || shown.length >= 4) return; seenSpec[k] = 1; shown.push({ x: x, slot: shown.length }); });
        }
        var on = {}; shown.forEach(function (p) { on[keyOf(p.x)] = 1; });
        var ctxSeen = {}, context = [];
        list.forEach(function (x) { var k = x.class + x.spec; if (ctxSeen[k] || on[keyOf(x)]) return; ctxSeen[k] = 1; context.push({ name: nameOf(x), values: x.dps, context: true }); });
        var series = shown.map(function (p) { return { name: nameOf(p.x), short: p.x.spec_name + " · " + ((RACES[p.x.race] && RACES[p.x.race].name) || p.x.race), values: p.x.dps, slot: p.slot }; }).concat(context);
        var gearTxt = state.gear === "crafted" ? "best craftable gear" : "no gear";
        trajSub.textContent = (pins.length ? "Your " + shown.length + " picked row" + (shown.length === 1 ? "" : "s") : "The best race of the top " + shown.length + " specs in the table") +
          ", " + gearTxt + ". Pick up to " + MAXPIN + " rows with Compare. The gold line marks level " + state.level + ".";
        clearBtn.disabled = !pins.length;
        var opts = { label: "Simulated DPS at every level for the charted rows", x: levels, xLabel: "Level", unit: "DPS", series: series, marker: state.level,
          note: context.length ? "Grey lines: the best race of the other " + context.length + " specs that match the filters." : "" };
        if (window.ForeverCharts) { if (chart) chart.update(opts); else chart = window.ForeverCharts.draw(chartBox, opts); }
        // the same numbers as a table
        var body = el("tbody");
        levels.forEach(function (lv, i) {
          body.appendChild(el("tr", lv === state.level ? { "class": "is-open" } : {}, [el("td", { "class": "dps-num", text: String(lv) })].concat(shown.map(function (p) {
            var v = p.x.dps[i], c = p.x.ci[i];
            return el("td", { "class": "dps-num" }, [el("strong", { text: v == null ? "–" : v.toFixed(1) }), el("small", { text: c == null ? "" : " ±" + c.toFixed(1) })]);
          }))));
        });
        numbers.replaceChildren(el("table", { "class": "dps-inputs", "data-caption": "DPS at every level for the charted rows" }, [
          el("thead", {}, [el("tr", {}, [el("th", { scope: "col", text: "Level" })].concat(shown.map(function (p) { return el("th", { scope: "col", text: nameOf(p.x) }); })))]), body]));
      }

      function draw() {
        var li = levels.indexOf(state.level);
        var list = rows.filter(function (x) { return x.dps[li] != null && (x.gear || "none") === state.gear && FF.match(state.cls, x.class) &&
          FF.match(state.faction, RACES[x.race] ? RACES[x.race].faction : "") && FF.match(state.race, x.race) &&
          FF.text(state.q, [CLSNAME[x.class], x.spec_name, x.spec, RACES[x.race] && RACES[x.race].name]); })
          .sort(function (a, b) { return b.dps[li] - a.dps[li]; });
        var best = {};
        list.forEach(function (x) { var k = x.class + x.spec; best[k] = Math.max(best[k] || 0, x.dps[li]); });
        if (state.best) { var seen = {}; list = list.filter(function (x) { var k = x.class + x.spec; if (seen[k]) return false; seen[k] = 1; return true; }); }
        if (ff) ff.count(list.length, state.best ? new Set(rows.filter(function (x) { return (x.gear || "none") === state.gear; }).map(function (x) { return x.class + x.spec; })).size
          : rows.filter(function (x) { return (x.gear || "none") === state.gear && x.dps[li] != null; }).length, state.best ? "specs" : "spec and race pairs");
        drawChart(list);
        var pinned = {}; pins.forEach(function (p) { pinned[p.key] = 1; });
        var top = list.length ? list[0].dps[li] : 1, tbody = el("tbody");
        list.forEach(function (x, i) {
          var d = x.dps[li], vs = d / best[x.class + x.spec] - 1, prev = li > 0 ? x.dps[li - 1] : null, gain = prev ? (d / prev - 1) * 100 : null;
          var btn = el("button", { type: "button", "class": "dps-spec-btn", "aria-expanded": "false", text: x.spec_name });
          var isPin = !!pinned[keyOf(x)];
          var pin = el("button", { type: "button", "class": "dps-pin", "aria-pressed": isPin ? "true" : "false", "aria-label": (isPin ? "On chart: " : "Compare: ") + nameOf(x) + (isPin ? ". Remove it from the chart" : ". Add it to the chart"), text: isPin ? "On chart" : "Compare" });
          if (!isPin && pins.length >= MAXPIN) pin.disabled = true;
          pin.addEventListener("click", function (ev) {
            ev.stopPropagation();
            var k = keyOf(x), at = -1;
            pins.forEach(function (p, n) { if (p.key === k) at = n; });
            if (at >= 0) pins.splice(at, 1);
            else if (pins.length < MAXPIN) { var used = {}; pins.forEach(function (p) { used[p.slot] = 1; }); var slot = 0; while (used[slot]) slot++; pins.push({ key: k, slot: slot }); }      // a picked row keeps its colour
            draw();
          });
          var tr = el("tr", { "class": "dps-spec-row" });
          var detail = null;
          function toggle() {
            if (detail) { detail.remove(); detail = null; btn.setAttribute("aria-expanded", "false"); tr.classList.remove("is-open"); return; }
            var both = {}; ["crafted", "none"].forEach(function (g) { var o = byKey[keyOf(x) + "|" + g]; if (o) both[g] = o.dps; });
            detail = el("tr", { "class": "dps-spec-detail" }, [el("td", { colspan: "8" }, [specPanel(x, state.level, x.gear || "none", both)])]);
            tr.after(detail); btn.setAttribute("aria-expanded", "true"); tr.classList.add("is-open");
          }
          btn.addEventListener("click", function (ev) { ev.stopPropagation(); toggle(); });
          tr.addEventListener("click", toggle);
          tbody.appendChild(tr);
          [
            el("td", { text: String(i + 1) }),
            el("td", {}, [el("span", { "class": "pill pill--" + x.class, text: CLSNAME[x.class] || x.class })]),
            el("td", {}, [btn]),
            el("td", { text: (RACES[x.race] && RACES[x.race].name) || x.race }),
            el("td", { "class": "dps-num" }, [el("span", { "class": "dps-bar", style: "--v:" + (d / top * 100).toFixed(1) + "%" }), el("strong", { text: d.toFixed(1) }), el("small", { text: " ±" + (x.ci[li] || 0).toFixed(1) })]),
            el("td", { "class": "dps-num", text: Math.abs(vs) < 1e-9 ? "best" : (Math.abs(vs) < 0.0005 ? "tied" : (vs * 100).toFixed(1) + "%") }),
            el("td", { "class": "dps-num" + (gain != null && gain < 0 ? " dps-down" : ""), text: gain == null ? "–" : (gain >= 0 ? "+" : "") + gain.toFixed(1) + "%" }),
            el("td", {}, [pin])
          ].forEach(function (td) { tr.appendChild(td); });
        });
        out.replaceChildren(el("div", { "class": "dps-scroll" }, [el("table", { "class": "dps-table" }, [
          el("thead", {}, [el("tr", {}, ["#", "Class", "Spec (click for the full build)", "Race", "Simulated DPS", "vs best race", "vs previous level", "Chart"].map(function (h) { return el("th", { scope: "col", text: h }); }))]), tbody])]));
      }
      ff = FF.build(state, [
        { type: "range", key: "level", label: "Level", values: levels },
        { type: "choice", key: "gear", label: "Gear", options: (hasCrafted ? [["crafted", "Best craftable"]] : []).concat([["none", "No gear"]]) },
        { type: "chips", key: "cls", label: "Class", all: "All classes", pills: true, options: Object.keys(CLSNAME).map(function (c) { return [c, CLSNAME[c]]; }) },
        { type: "choice", key: "faction", label: "Faction", options: [["all", "Both"], ["A", "Alliance"], ["H", "Horde"]] },
        { type: "select", key: "race", label: "Race", options: [["all", "All races"]].concat(Object.keys(RACES).map(function (r) { return [r, RACES[r].name]; })) },
        { type: "search", key: "q", label: "Search", placeholder: "Spec, class or race" },
        { type: "toggle", key: "best", label: "Best race of each spec only" }
      ], draw, { label: "Filter DPS by level" });
      filters.replaceChildren(ff.el);
      box.replaceChildren(el("p", { "class": "dps-meta", text: rows.length / (hasCrafted ? 2 : 1) + " class, spec and race series, levels " + levels[0] + "–" + levels[levels.length - 1] + ", " + (hasCrafted ? "with and without crafted gear, " : "") + (data.iterations || "?") + " simulated fights per point. ± is simulation noise only." }), filters, traj, out);
      draw();
    }).catch(function () { box.replaceChildren(el("p", { text: "The level simulation could not be loaded." })); });
  }

  // ---------- Coverage audit (tools/levelsim/audit.py) ----------
  var STATUS = { used: "Used", tested: "Tested, not chosen", starved: "In rotation, never cast", multi: "Left out: several targets", reactive: "Left out: target must act", kill: "Left out: needs a kill",
    type: "Left out: creature type", utility: "Left out: utility", talent: "Left out: talent not taken", form: "Left out: form or weapon", untested: "Not tested", unaccounted: "Unaccounted" };
  function renderAudit(box) {
    var url = new URL("../assets/data/level-audit.json", SCRIPT_SRC || location.href).href;
    fetch(url).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (A) {
      function num(n) { return n.toLocaleString("en-US"); }
      function tile(k, v, s) { return el("div", { "class": "dps-audit-tile" }, [el("span", { text: k }), el("strong", { text: v }), el("small", { text: s })]); }
      function tbl(caption, head, bodyRows) {
        return el("div", { "class": "dps-scroll" }, [el("table", { "class": "dps-inputs", "data-caption": caption }, [
          el("thead", {}, [el("tr", {}, head.map(function (h) { return el("th", { scope: "col", text: h }); }))]), el("tbody", {}, bodyRows)])]);
      }
      function fold(title, kids) { return el("details", { "class": "note" }, [el("summary", { text: title })].concat(kids)); }
      function tag(text, cls) { return el("span", { "class": "dps-tag" + (cls ? " dps-tag--" + cls : ""), text: text }); }
      var M = A.matrix, counts = { used: 0, tested: 0, out: 0, untested: 0, unaccounted: 0 }, spellRows = [];
      Object.keys(A.abilities).forEach(function (cls) {
        A.abilities[cls].spells.forEach(function (sp) {
          var st = sp.status;
          counts[st === "used" || st === "tested" || st === "unaccounted" ? st : st === "untested" || st === "starved" ? "untested" : "out"]++;
          spellRows.push(el("tr", {}, [
            el("td", {}, [el("span", { "class": "pill pill--" + cls, text: CLSNAME[cls] || cls })]), el("td", { text: sp.name }), el("td", { "class": "dps-num", text: String(sp.learned) }),
            el("td", {}, [tag(STATUS[st] || st, st === "used" || st === "tested" ? "ok" : st === "untested" || st === "starved" || st === "unaccounted" ? "gap" : "")]),
            el("td", { text: st === "used" ? "From level " + sp.first_used + ": " + sp.specs.join(", ") : (A.reasons[st] || "") })]));
        });
      });
      var totalSpells = spellRows.length, T = A.talents || {}, tRows = [], tCount = 0, tMeasurable = 0, tLower = 0, never = [];
      Object.keys(T).forEach(function (cls) {
        T[cls].specs.forEach(function (sp) {
          sp.talents.slice().sort(function (a, b) { return (b.adds_pct || 0) - (a.adds_pct || 0); }).forEach(function (t) {
            tCount++; if (t.measurable) tMeasurable++; if (t.measurable && t.adds_pct < 0) tLower++;
            tRows.push(el("tr", {}, [
              el("td", {}, [el("span", { "class": "pill pill--" + cls, text: CLSNAME[cls] || cls })]), el("td", { text: sp.spec_name }), el("td", { text: t.talent }),
              el("td", { text: t.tree }), el("td", { "class": "dps-num", text: String(t.rank) }),
              el("td", { "class": "dps-num" + (t.adds_pct != null && t.adds_pct < 0 && t.measurable ? " dps-down" : "") }, [
                el("span", { "class": "dps-bar", style: "--v:" + Math.max(0, Math.min(100, (t.adds_pct || 0) * 4)).toFixed(1) + "%" }),
                el("strong", { text: t.adds_pct == null ? "–" : (t.adds_pct >= 0 ? "+" : "") + t.adds_pct.toFixed(1) + "%" })]),
              el("td", { text: t.measurable ? "Yes" : "No" })]));
          });
        });
        never.push(el("li", {}, [el("strong", { text: (CLSNAME[cls] || cls) + " (" + T[cls].never_taken.length + " of " + T[cls].tree_size + "): " }), document.createTextNode(T[cls].never_taken.join(", "))]));
      });
      var rRows = [], rModelled = 0, rTotal = 0;
      Object.keys(A.racials).forEach(function (race) {
        A.racials[race].forEach(function (r) {
          rTotal++; if (r.status !== "none") rModelled++;
          rRows.push(el("tr", {}, [el("td", { text: (RACES[race] && RACES[race].name) || race }), el("td", { text: r.name }),
            el("td", {}, [tag(r.status === "modelled" ? "Modelled" : r.status === "partial" ? "Partly modelled" : "No damage effect", r.status === "modelled" ? "ok" : r.status === "partial" ? "gap" : "")]),
            el("td", { text: r.note })]));
        });
      });
      var dipRows = A.dips.map(function (d) {
        return el("tr", {}, [el("td", {}, [el("span", { "class": "pill pill--" + d["class"], text: CLSNAME[d["class"]] || d["class"] })]), el("td", { text: d.spec }),
          el("td", { text: d.gear === "crafted" ? "Best craftable" : "No gear" }), el("td", { "class": "dps-num", text: (d.level - 1) + " to " + d.level }),
          el("td", { "class": "dps-num dps-down", text: d.worst_pct.toFixed(1) + "%" }), el("td", { "class": "dps-num", text: String(d.races) })]);
      });
      var complete = M.cells_present === M.cells_expected && !M.not_positive.length;
      box.replaceChildren(
        el("div", { "class": "dps-audit-tiles" }, [
          tile("Cells simulated", num(M.cells_present) + " of " + num(M.cells_expected), complete ? "No cell is missing and every one has a positive DPS." : (M.missing.length + " missing, " + M.not_positive.length + " without damage.")),
          tile("Combinations", num(M.series), M.specs + " specs × the races of each class (" + M.class_race_pairs + " class and race pairs) × " + M.gear_modes.length + " gear modes, each at " + M.levels + " levels."),
          tile("Damaging class spells", counts.used + " of " + totalSpells + " used", counts.tested + " tested and not chosen, " + counts.out + " left out for a stated reason, " + counts.untested + " not tested or never cast" + (counts.unaccounted ? ", " + counts.unaccounted + " unaccounted" : "") + "."),
          tile("Talents tested", tCount ? num(tCount) : "–", tCount ? (tMeasurable - tLower) + " add DPS, " + (tCount - tMeasurable) + " change nothing above the noise, and " + tLower + " lower it: the build does better without them." : "Run audit.py with talents."),
          tile("Racials", rModelled + " of " + rTotal + " modelled", (rTotal - rModelled) + " have no effect on damage against one training target.")]),
        fold("Abilities: every damaging class spell and what the simulator does with it", [tbl("Damaging class spells", ["Class", "Spell", "Learned", "Status", "Detail"], spellRows)]),
        fold("Talents: what each talent adds to its level 60 build", [
          el("p", { text: "Each talent of each level 60 build is removed in turn and the fight is run again with the same random seeds (" + (A.talent_iterations || "?") + " fights, best craftable gear, first race of the class). Adds is the DPS lost without the talent. A talent marked No has no modelled effect on this fight, or one smaller than the noise. Removing a talent that unlocks another one leaves the other in place, so the number is that talent alone. A red negative number means DPS rises without the talent. That points at a rotation that uses the talent badly, and it is a known defect of this model." }),
          tbl("Talent contribution", ["Class", "Spec", "Talent", "Tree", "Rank", "Adds", "Above noise"], tRows)]),
        fold("Talents that no simulated build takes", [el("p", { text: "Each spec runs one talent order. These talents are in the trees but in none of the 27 orders, so they are not tested." }), el("ul", {}, never)]),
        fold("Racials: all " + rTotal + " and their status", [tbl("Racials", ["Race", "Racial", "Status", "Note"], rRows)]),
        fold("Level-to-level drops (" + A.dips.length + ")", [
          el("p", { text: "Places where DPS falls by more than 5% and more than the noise from one level to the next. A drop usually means a new spell rank or item changes the rotation or the mana budget. Each one is worth a look." }),
          dipRows.length ? tbl("Level-to-level drops", ["Class", "Spec", "Gear", "Levels", "Largest drop", "Races"], dipRows) : el("p", { text: "None." })]));
    }).catch(function () { box.replaceChildren(el("p", { text: "The coverage audit could not be loaded." })); });
  }

  function onPage() {
    var lv = document.querySelector("[data-dps-levels]");
    if (lv && !lv.dataset.ready) { lv.dataset.ready = "1"; renderLevels(lv); }
    var root = document.getElementById("dps-calc");
    if (root && !root.dataset.ready) { root.dataset.ready = "1"; render(root); }
    var sim = document.querySelector("[data-dps-sim]");
    if (sim && !sim.dataset.ready) { sim.dataset.ready = "1"; renderSim(sim); }
    var au = document.querySelector("[data-dps-audit]");
    if (au && !au.dataset.ready) { au.dataset.ready = "1"; renderAudit(au); }
  }
  window.ForeverDps = { results: results, MODEL: MODEL, BUFFS: BUFFS, V: V, GEAR: GEAR };
  if (window.document$ && typeof window.document$.subscribe === "function") window.document$.subscribe(onPage);
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", onPage);
  else onPage();
})();
