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
    shout:     [true, 139, "FE", "Battle Shout, melee AP"],
    kings:     [true, 10, "F", "Blessing of Kings, % all stats"],
    motw:      [true, 16, "F", "Mark/Gift of the Wild, all stats"],
    soe:       [true, 53, "F", "Strength of Earth Totem, Strength"],
    goa:       [true, 89, "F", "Grace of Air Totem, Agility"],
    wfTotem:   [true, 246, "F", "Windfury Totem: 20% for 1 extra attack with +AP (2H and main hand)"],
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
    corruption:[[438, 18, 1.0], "F", "Corruption 438 over 18 s; coefficient Classic"],
    agony:     [[552, 24, 1.0], "F", "Bane of Agony 552 over 24 s; coefficient Classic"],
    siphon:    [[410, 30, 0.5], "F", "Siphon Life 410 over 30 s; coefficient Classic"],
    wrack:     [[86, 0.286], "F", "Wrack 86 dps + 0.286 SP per second"],
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
    if (cls === "warrior") ap += b("shout");
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
      return (white + hs + bt + ww + wf) * dw * s.armorMul * s.directMul;
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
      return ((white + hs + ms + slam + ww + wf) * s.armorMul + deep) * 1.06 * dw * s.directMul; // Two-Handed Spec +6% (F)
    },
    combat: function (s) {
      var g = GEAR.rogue, cm = m("meleeCritMul");
      var y = yellowMul(s, cm + 0.2), w = whiteMul(s, true, cm);
      var haste = s.haste * (1 + v("snd") / 100) * (1 + 0.2 * uptime(15, 120)); // Blade Flurry
      var mhAvg = g.mh[0] + s.ap / 14 * g.mh[1], ohAvg = (g.oh[0] + s.ap / 14 * g.oh[1]) * 0.5 * 1.5;
      var white = (haste / g.mh[1] * mhAvg + haste / g.oh[1] * ohAvg) * w.avg;
      var ssDmg = (g.mh[0] + s.ap / 14 * 2.4 + v("ss")) * 1.15 * y.avg;
      var energy = 10 + 15 / 10; // regen + Shank refund approx (A)
      var cycleE = 5 * 40 + 20, cycleT = cycleE / energy; // 5 SS + Eviscerate
      var evis = v("evisc") * 1.15 * 1.2 * y.avg;
      var special = (5 * ssDmg + evis) / cycleT;
      var hits = (haste / g.mh[1] + haste / g.oh[1]) * (1 - m("meleeMiss") / 100);
      var pois = hits * 0.5 * v("instPois")[0] * v("instPois")[1] * spellHitOnly(s) + v("deadly")[0] / v("deadly")[1] * v("deadly")[2] * spellHitOnly(s);
      return ((white + special) * s.armorMul + pois) * s.directMul;
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
      var conv = 6, w = whiteMul(s, false, cm);
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
      var g = GEAR.cat, cm = m("meleeCritMul"), w = whiteMul(s, false, cm), y = yellowMul(s, cm);
      var avg = v("catWeapon") + s.ap / 14;
      var white = s.haste * avg * w.avg;
      var shred = (avg * v("shred")[0] + v("shred")[1]) * 1.1 * y.avg;
      var special = shred * 10 / 42; // energy-limited Shred spam, finishers folded in (A)
      return (white + special) * s.armorMul * s.directMul;
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
      return (dots + wrack * (1 - gcdShare) + nf) * shadow;
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
    var state = { cls: "all", faction: "all", best: false };
    var out = root.querySelector("[data-dps-results]");
    var filters = root.querySelector("[data-dps-filters]");

    function draw() {
      var rows = results().filter(function (x) {
        return (state.cls === "all" || x.spec.cls === state.cls) && (state.faction === "all" || RACES[x.race].faction === state.faction);
      });
      if (state.best) {
        var seen = {}; rows = rows.filter(function (x) { if (seen[x.spec.id]) return false; seen[x.spec.id] = 1; return true; });
      }
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
          el("td", { "class": "dps-num", text: x.vsBest === 0 ? "best" : (x.vsBest * 100).toFixed(1) + "%" }),
          el("td", { "class": "dps-num", title: "Share of this spec's inputs that are Forever-sourced", text: conf + "%" })
        ]));
      });
      var table = el("table", { "class": "dps-table" }, [
        el("thead", {}, [el("tr", {}, ["#", "Class", "Spec", "Race", "DPS", "vs best race", "Data confidence"].map(function (h) { return el("th", { scope: "col", text: h }); }))]),
        tbody
      ]);
      out.replaceChildren(el("div", { "class": "dps-scroll" }, [table]));
    }

    function select(label, key, opts) {
      var s = el("select", { "aria-label": label });
      opts.forEach(function (o) { s.appendChild(el("option", { value: o[0], text: o[1] })); });
      s.addEventListener("change", function () { state[key] = s.value; draw(); });
      return el("label", {}, [el("span", { text: label }), s]);
    }
    var bestBox = el("input", { type: "checkbox" });
    bestBox.addEventListener("change", function () { state.best = bestBox.checked; draw(); });
    filters.replaceChildren(
      select("Class", "cls", [["all", "All classes"]].concat(Object.keys(CLSNAME).map(function (c) { return [c, CLSNAME[c]]; }))),
      select("Faction", "faction", [["all", "Both"], ["A", "Alliance"], ["H", "Horde"]]),
      el("label", { "class": "dps-check" }, [bestBox, el("span", { text: "Best race per spec only" })])
    );

    // Editable inputs
    function numInput(row, idx, onChange) {
      var i = el("input", { type: "number", step: "any", value: String(row[idx]) });
      i.addEventListener("input", function () { var n = parseFloat(i.value); if (!isNaN(n)) { onChange(n); draw(); } });
      return i;
    }
    var mTable = el("tbody");
    Object.keys(MODEL).forEach(function (k) {
      var row = MODEL[k];
      mTable.appendChild(el("tr", {}, [el("td", { text: row[2] }), el("td", {}, [numInput(row, 0, function (n) { row[0] = n; })]), el("td", {}, [tagEl(row[1])])]));
    });
    var bTable = el("tbody");
    Object.keys(BUFFS).forEach(function (k) {
      var row = BUFFS[k], cb = el("input", { type: "checkbox", "aria-label": row[3] });
      cb.checked = row[0]; cb.addEventListener("change", function () { row[0] = cb.checked; draw(); });
      bTable.appendChild(el("tr", {}, [el("td", {}, [cb]), el("td", { text: row[3] }), el("td", {}, [numInput(row, 1, function (n) { row[1] = n; })]), el("td", {}, [tagEl(row[2])])]));
    });
    var vTable = el("tbody");
    Object.keys(V).forEach(function (k) {
      var row = V[k], val = row[0];
      var input = Array.isArray(val) ? el("code", { text: JSON.stringify(val) }) : numInput(row, 0, function (n) { row[0] = n; });
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
    function box(title, content) { return el("details", { "class": "note" }, [el("summary", { text: title }), content]); }
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
      var state = { cls: "all", faction: "all", best: false };
      var filters = el("div", { "class": "dps-filters" }), out = el("div");
      function draw() {
        var list = rows.filter(function (x) {
          var f = RACES[x.race] ? RACES[x.race].faction : "";
          return (state.cls === "all" || x.class === state.cls) && (state.faction === "all" || f === state.faction);
        });
        var best = {};
        rows.forEach(function (x) { var k = x.class + x.spec; best[k] = Math.max(best[k] || 0, x.dps_mean); });
        if (state.best) { var seen = {}; list = list.filter(function (x) { var k = x.class + x.spec; if (seen[k]) return false; seen[k] = 1; return true; }); }
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
      function select(label, key, opts) {
        var s = el("select", { "aria-label": label });
        opts.forEach(function (o) { s.appendChild(el("option", { value: o[0], text: o[1] })); });
        s.addEventListener("change", function () { state[key] = s.value; draw(); });
        return el("label", {}, [el("span", { text: label }), s]);
      }
      var cb = el("input", { type: "checkbox" });
      cb.addEventListener("change", function () { state.best = cb.checked; draw(); });
      filters.replaceChildren(
        select("Class", "cls", [["all", "All classes"]].concat(Object.keys(CLSNAME).map(function (c) { return [c, CLSNAME[c]]; }))),
        select("Faction", "faction", [["all", "Both"], ["A", "Alliance"], ["H", "Horde"]]),
        el("label", { "class": "dps-check" }, [cb, el("span", { text: "Best race per spec only" })]));
      var r0 = rows[0] || {};
      box.replaceChildren(el("p", { "class": "dps-meta", text: rows.length + " spec and race pairs, " + (r0.iterations || "?") + " simulated fights of " + (r0.fight_seconds || "?") + " s each. ± is the 95% confidence interval of the simulation, not the error of the estimate." }), filters, out);
      draw();
    }).catch(function () { box.replaceChildren(el("p", { text: "The simulated estimates could not be loaded." })); });
  }

  // ---------- Level-by-level simulation (tools/levelsim, published by tools/levelsim/publish.py) ----------
  function renderLevels(box) {
    var url = new URL("../assets/data/level-sim.json", SCRIPT_SRC || location.href).href;
    fetch(url).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (data) {
      var levels = data.levels, rows = data.rows;
      var hasCrafted = rows.some(function (x) { return x.gear === "crafted"; });
      var state = { cls: "all", level: levels[levels.length - 1], best: true, gear: hasCrafted ? "crafted" : "none" };
      var filters = el("div", { "class": "dps-filters" }), out = el("div");
      function draw() {
        var li = levels.indexOf(state.level);
        var list = rows.filter(function (x) { return x.dps[li] != null && (x.gear || "none") === state.gear && (state.cls === "all" || x.class === state.cls); })
          .sort(function (a, b) { return b.dps[li] - a.dps[li]; });
        var best = {};
        list.forEach(function (x) { var k = x.class + x.spec; best[k] = Math.max(best[k] || 0, x.dps[li]); });
        if (state.best) { var seen = {}; list = list.filter(function (x) { var k = x.class + x.spec; if (seen[k]) return false; seen[k] = 1; return true; }); }
        var top = list.length ? list[0].dps[li] : 1, tbody = el("tbody");
        list.forEach(function (x, i) {
          var d = x.dps[li], vs = d / best[x.class + x.spec] - 1;
          var parts = Object.keys(x.breakdown).map(function (k) { return [k, x.breakdown[k]]; }).sort(function (a, c) { return c[1] - a[1]; });
          var tot = parts.reduce(function (s, p) { return s + p[1]; }, 0) || 1;
          var det = el("details", { "class": "dps-breakdown" }, [el("summary", { text: x.spec_name })].concat([el("ul", {}, parts.map(function (p) {
            return el("li", { text: p[0] + ": " + Math.round(p[1] / tot * 100) + "% at level " + levels[levels.length - 1] });
          }))]));
          tbody.appendChild(el("tr", {}, [
            el("td", { text: String(i + 1) }),
            el("td", {}, [el("span", { "class": "pill pill--" + x.class, text: CLSNAME[x.class] || x.class })]),
            el("td", {}, [det]),
            el("td", { text: (RACES[x.race] && RACES[x.race].name) || x.race }),
            el("td", { "class": "dps-num" }, [el("span", { "class": "dps-bar", style: "--v:" + (d / top * 100).toFixed(1) + "%" }), el("strong", { text: d.toFixed(1) }), el("small", { text: " ±" + (x.ci[li] || 0).toFixed(1) })]),
            el("td", { "class": "dps-num", text: Math.abs(vs) < 1e-9 ? "best" : (Math.abs(vs) < 0.0005 ? "tied" : (vs * 100).toFixed(1) + "%") })
          ]));
        });
        out.replaceChildren(el("div", { "class": "dps-scroll" }, [el("table", { "class": "dps-table" }, [
          el("thead", {}, [el("tr", {}, ["#", "Class", "Spec (open for ability share)", "Race", "Simulated DPS", "vs best race"].map(function (h) { return el("th", { scope: "col", text: h }); }))]), tbody])]));
      }
      var cls = el("select", { "aria-label": "Class" });
      [["all", "All classes"]].concat(Object.keys(CLSNAME).map(function (c) { return [c, CLSNAME[c]]; })).forEach(function (o) { cls.appendChild(el("option", { value: o[0], text: o[1] })); });
      cls.addEventListener("change", function () { state.cls = cls.value; draw(); });
      var lvl = el("input", { type: "range", min: String(levels[0]), max: String(levels[levels.length - 1]), value: String(state.level), "aria-label": "Level" });
      var lvlText = el("strong", { text: String(state.level) });
      lvl.addEventListener("input", function () { state.level = parseInt(lvl.value, 10); lvlText.textContent = lvl.value; draw(); });
      var cb = el("input", { type: "checkbox" }); cb.checked = true;
      cb.addEventListener("change", function () { state.best = cb.checked; draw(); });
      var gsel = el("select", { "aria-label": "Gear" });
      [["crafted", "Best craftable gear"], ["none", "No gear"]].forEach(function (o) { if (o[0] === "none" || hasCrafted) gsel.appendChild(el("option", { value: o[0], text: o[1] })); });
      gsel.value = state.gear;
      gsel.addEventListener("change", function () { state.gear = gsel.value; draw(); });
      filters.replaceChildren(
        el("label", {}, [el("span", { text: "Gear" }), gsel]),
        el("label", {}, [el("span", { text: "Class" }), cls]),
        el("label", {}, [el("span", { text: "Level " }), lvlText, lvl]),
        el("label", { "class": "dps-check" }, [cb, el("span", { text: "Best race per spec only" })]));
      box.replaceChildren(el("p", { "class": "dps-meta", text: rows.length / (hasCrafted ? 2 : 1) + " class, spec and race series, levels " + levels[0] + "–" + levels[levels.length - 1] + ", " + (data.iterations || "?") + " simulated fights per point. ± is simulation noise only." }), filters, out);
      draw();
    }).catch(function () { box.replaceChildren(el("p", { text: "The level simulation could not be loaded." })); });
  }

  function onPage() {
    var lv = document.querySelector("[data-dps-levels]");
    if (lv && !lv.dataset.ready) { lv.dataset.ready = "1"; renderLevels(lv); }
    var root = document.getElementById("dps-calc");
    if (root && !root.dataset.ready) { root.dataset.ready = "1"; render(root); }
    var sim = document.querySelector("[data-dps-sim]");
    if (sim && !sim.dataset.ready) { sim.dataset.ready = "1"; renderSim(sim); }
  }
  window.ForeverDps = { results: results, MODEL: MODEL, BUFFS: BUFFS, V: V, GEAR: GEAR };
  if (window.document$ && typeof window.document$.subscribe === "function") window.document$.subscribe(onPage);
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", onPage);
  else onPage();
})();
