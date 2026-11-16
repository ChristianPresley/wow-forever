/* Forever Codex healing calculator (docs/guides/healing-calculator.md).
   Renders docs/assets/data/heal-sim.json, written by tools/healsim/run.py.
   Every number is model output: see tools/healsim/README.md for the method and its gaps. */
(function () {
  "use strict";
  var SCRIPT_SRC = document.currentScript ? document.currentScript.src : "";
  var CLSNAME = { priest: "Priest", paladin: "Paladin", druid: "Druid", shaman: "Shaman" };
  var RACENAME = { human: "Human", dwarf: "Dwarf", gnome: "Gnome", nelf: "Night Elf", sho: "Skyborne (High Order)",
    sws: "Skyborne (Windshaper)", orc: "Orc", troll: "Troll", tauren: "Tauren", undead: "Undead" };
  var MODES = [["fight", "Sustained"], ["endless", "Endless"], ["max", "Maximum"]];
  var SLOT_ORDER = ["head", "neck", "shoulder", "back", "chest", "wrist", "hands", "waist", "legs", "feet", "trinket1", "trinket2", "main_hand", "off_hand", "ranged"];
  var SLOT_NAME = { head: "Head", neck: "Neck", shoulder: "Shoulders", back: "Back", chest: "Chest", wrist: "Wrists", hands: "Hands", waist: "Waist",
    legs: "Legs", feet: "Feet", trinket1: "Trinket", trinket2: "Trinket", main_hand: "Main hand", off_hand: "Off hand", ranged: "Ranged" };
  var STAT_NAME = { healing: "Healing", sp: "Spell power", spell_damage: "Spell damage", int: "Intellect", spi: "Spirit", sta: "Stamina", crit: "Crit rating", mp5: "Mana per 5 s" };

  function el(tag, attrs, kids) {
    var n = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === "text") n.textContent = attrs[k]; else n.setAttribute(k, attrs[k]);
    });
    (kids || []).forEach(function (c) { if (c) n.appendChild(typeof c === "string" ? document.createTextNode(c) : c); });
    return n;
  }
  function num(v, d) { return v == null ? "–" : v.toLocaleString("en-US", { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 }); }
  function numCell(v, d) { return el("td", { "class": "dps-num", text: num(v, d) }); }
  // Column header with a hover / focus description, and optionally a click-to-sort button.
  function th(label, tip, sort) {
    var inner = sort ? el("button", { type: "button", "class": "heal-sort" + (sort.active ? " is-active" : "") + (sort && sort.active && sort.dir === "ascending" ? " is-asc" : ""), text: label }) : el("span", { text: label });
    if (tip) { inner.setAttribute("data-tip", tip); inner.classList.add("heal-tip"); if (!sort) inner.setAttribute("tabindex", "0"); }
    if (sort) inner.addEventListener("click", sort.go);
    var h = el("th", { scope: "col" }, [inner]);
    if (sort && sort.active) h.setAttribute("aria-sort", sort.dir || "descending");
    return h;
  }
  // One floating tooltip for every [data-tip] element (tables scroll sideways, so a CSS-only tooltip would be clipped).
  var tipBox = null;
  function showTip(target) {
    if (!tipBox) { tipBox = el("div", { "class": "heal-tipbox", role: "tooltip", id: "heal-tipbox" }); document.body.appendChild(tipBox); }
    tipBox.textContent = target.getAttribute("data-tip");
    tipBox.hidden = false;
    target.setAttribute("aria-describedby", "heal-tipbox");
    var r = target.getBoundingClientRect(), w = tipBox.offsetWidth, hgt = tipBox.offsetHeight;
    var left = Math.max(8, Math.min(window.innerWidth - w - 8, r.left + r.width / 2 - w / 2));
    var top = r.bottom + 8 + hgt > window.innerHeight ? r.top - hgt - 8 : r.bottom + 8;
    tipBox.style.left = left + "px";
    tipBox.style.top = Math.max(8, top) + "px";
  }
  function hideTip() { if (tipBox) tipBox.hidden = true; }
  function tipTarget(ev) { return ev.target && ev.target.closest ? ev.target.closest("[data-tip]") : null; }
  if (!window.__healTips) {
    window.__healTips = true;
    document.addEventListener("mouseover", function (ev) { var t = tipTarget(ev); if (t) showTip(t); });
    document.addEventListener("mouseout", function (ev) { if (tipTarget(ev)) hideTip(); });
    document.addEventListener("focusin", function (ev) { var t = tipTarget(ev); if (t) showTip(t); });
    document.addEventListener("focusout", hideTip);
    document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") hideTip(); });
    window.addEventListener("scroll", hideTip, true);
  }
  var TIP = {
    rank: "Position in the current sort order.",
    build: "The talent build. Click a row for its talents, cast mixes, sustain breakouts and gear.",
    race: "Race of the character. Each build is run for every race its class can be.",
    fight: "Sustained HPS: the most healing per second that lasts the whole 5-minute fight, starting on full mana and ending on empty.",
    total: "Total healing in the fight: sustained HPS times the 300 seconds of the fight.",
    hpm: "Healing per mana: healing bought by each point of mana with the sustained cast mix.",
    empty: "Seconds until empty: how long a full mana bar lasts when casting the maximum mix without stopping.",
    sustain: "Sustain: sustained HPS as a percentage of maximum HPS. The share of full output that survives a whole fight.",
    endless: "Endless HPS: the most healing per second on mana regeneration alone. This mix never runs out of mana.",
    max: "Maximum HPS: the most healing per second with mana ignored.",
    dps: "Off-DPS: the same build in the same healing gear dealing damage for 3 minutes with its best damage rotation."
  };

  function section(title, kids) { return el("section", { "class": "dps-spec-sec" }, [el("h4", { text: title })].concat(kids)); }

  function render(box, data) {
    var N = data.names, builds = {}, fight = data.fight_seconds;
    data.builds.forEach(function (b) { builds[b["class"] + "/" + b.id] = b; });
    var state = { cls: "all", scen: "tank", gear: "crafted", role: "all", sort: "fight", best: false, dir: "descending" };
    var controls = el("div", { "class": "dps-filters" });
    var picks = el("div", { "class": "heal-picks" });
    var meta = el("p", { "class": "dps-meta", role: "status" });
    var holder = el("div", { "class": "dps-scroll" });

    function buildOf(x) { return builds[x["class"] + "/" + x.build]; }
    // Sustain: the share of a build's maximum healing that it can keep up for the whole fight.
    function sustain(x) { var R = x.r[state.scen]; return R.max.hps ? R.fight.hps / R.max.hps * 100 : 0; }
    // The three sustain stats: total healing in the fight, healing per mana, seconds until the mana bar is empty.
    function total(x) { return x.r[state.scen].fight.hps * fight; }
    function hpm(x) { return x.r[state.scen].fight.hpm || 0; }
    function empty(x) { return x.r[state.scen].max.oom || 0; }
    function value(x, key) {
      var R = x.r[state.scen];
      return key === "dps" ? (x.dps ? x.dps.dps : 0) : key === "sustain" ? sustain(x) : key === "total" ? total(x) : key === "hpm" ? hpm(x) :
        key === "empty" ? empty(x) : R[key].hps;
    }
    function table(head, rows) {
      return el("div", { "class": "dps-scroll" }, [el("table", { "class": "dps-table" }, [
        el("thead", {}, [el("tr", {}, head.map(function (h) { return el("th", { scope: "col", text: h }); }))]),
        el("tbody", {}, rows.map(function (r) { return el("tr", {}, r.map(function (c, i) { return i ? el("td", { "class": "dps-num", text: c }) : el("td", { text: c }); })); }))])]);
    }
    function pool() {
      return data.rows.filter(function (x) {
        return x.gear === state.gear && (state.cls === "all" || x["class"] === state.cls) &&
          (state.role === "all" || buildOf(x).role === state.role);
      });
    }

    function mixList(o) {
      var items = o.mix.filter(function (m) { return m[1] >= 0.05; }).map(function (m) { return el("li", { text: N[m[0]] + ": " + num(m[1], 1) + " casts/min, " + num(m[2], 1) + " HPS" }); });
      if (o.rest > 0.005) items.push(el("li", { text: "Not casting (regenerating mana): " + Math.round(o.rest * 100) + "% of the time" }));
      return el("ul", {}, items);
    }

    function panel(x) {
      var b = buildOf(x), R = x.r[state.scen], kids = [];
      var trees = Object.keys(b.talents);
      kids.push(el("p", { "class": "dps-spec-head" }, [el("strong", { text: RACENAME[x.race] + " " + CLSNAME[x["class"]] + ", " + b.name }),
        " · level " + data.level + " · " + (state.scen === "tank" ? "one target" : "party of 5") + " · " + (x.gear === "crafted" ? "best craftable healing gear" : "no gear")]));
      kids.push(el("p", { "class": "dps-meta", text: b.note }));
      kids.push(section("Talents (" + trees.map(function (t) { return b.points[t]; }).join("/") + ")", [el("div", { "class": "dps-spec-trees" }, trees.map(function (t) {
        return el("div", {}, [el("h5", { text: t + " · " + b.points[t] }), el("ul", {}, Object.keys(b.talents[t]).map(function (n) { return el("li", { text: n + " " + b.talents[t][n] }); }))]);
      }))]));
      var st = x.stats;
      kids.push(section("Character", [el("ul", {}, [
        "Healing power " + num(st.healing) + ", Intellect " + num(st.int) + ", Spirit " + num(st.spi) + ", spell crit " + num(st.crit, 1) + "% before talents",
        "Mana " + num(st.mana) + "; regeneration " + num(st.regen_cast, 0) + " per 5 s while casting, " + num(st.regen_rest, 0) + " per 5 s while resting"
      ].map(function (t) { return el("li", { text: t }); }))]));
      var F = R.fight, E = R.endless, M = R.max, pool = st.mana;
      var PACES = [["Sustained mix", F], ["Endless mix", E], ["Maximum mix", M]];
      function lasts(o) { return o.oom == null ? Infinity : o.oom; }
      function secs(o) { var t = lasts(o); return t === Infinity ? "never" : num(t, 1) + " s"; }
      // 1. Total healing in the fight
      kids.push(section("Sustain stat 1: total healing in the fight: " + num(total(x)), [
        el("p", { "class": "dps-meta", text: "Healing delivered over the " + num(fight) + " s fight at each pace. The maximum mix stops when mana runs out." }),
        table(["Pace", "HPS while casting", "Seconds it lasts", "Total healing in the fight", "Share of sustained"], PACES.map(function (pc) {
          var o = pc[1], t = Math.min(fight, lasts(o)), tot = o.hps * t;
          return [pc[0], num(o.hps, 1), num(t, 1), num(tot), num(tot / (F.hps * fight) * 100, 1) + "%"];
        })),
        el("h5", { text: "Sustained mix, by spell" }),
        table(["Spell", "Casts in the fight", "Healing per cast", "Total healing", "Share"], F.mix.map(function (m) {
          return [N[m[0]], num(m[1] * fight / 60, 1), num(m[4], 1), num(m[2] * fight), num(m[2] / F.hps * 100, 1) + "%"];
        }))]));
      // 2. Healing per mana
      kids.push(section("Sustain stat 2: healing per mana: " + num(F.hpm, 2), [
        el("p", { "class": "dps-meta", text: "Healing bought by each point of mana spent." }),
        table(["Pace", "Healing per mana", "HPS", "Mana spent per second"], PACES.map(function (pc) {
          return [pc[0], num(pc[1].hpm, 2), num(pc[1].hps, 1), num(pc[1].spend, 2)];
        })),
        el("h5", { text: "Sustained mix, by spell" }),
        table(["Spell", "Healing per mana", "Healing per cast", "Mana per cast", "Mana in the fight", "Share of mana"], F.mix.map(function (m) {
          var mana = m[1] / 60 * m[3];
          return [N[m[0]], m[3] > 0 ? num(m[4] / m[3], 2) : "free", num(m[4], 1), num(m[3], 1), num(mana * fight), F.spend ? num(mana / F.spend * 100, 1) + "%" : "–"];
        }))]));
      // 3. Seconds until empty
      kids.push(section("Sustain stat 3: seconds until empty: " + secs(M) + " at maximum pace", [
        el("p", { "class": "dps-meta", text: "How long a full mana bar of " + num(pool) + " lasts at each pace: mana bar divided by the net drain." }),
        table(["Pace", "Mana spent per second", "Mana regenerated per second", "Net drain per second", "Seconds until empty", "Time not casting"], PACES.map(function (pc) {
          var o = pc[1];
          return [pc[0], num(o.spend, 2), num(o.regen, 2), num(Math.max(0, o.spend - o.regen), 2), secs(o), Math.round(o.rest * 100) + "%"];
        })),
        el("p", { "class": "dps-meta", text: "Sustain: " + num(sustain(x), 1) + "% of maximum healing lasts the whole fight; " + num(M.hps ? E.hps / M.hps * 100 : 0, 1) + "% lasts forever." })]));
      var titles = { fight: "Sustained: best cast mix for a " + Math.round(fight / 60) + "-minute fight", endless: "Endless: best cast mix on regeneration alone",
        max: "Maximum: highest healing per second, mana ignored" };
      MODES.forEach(function (m, i) {
        var o = R[m[0]];
        var facts = [num(o.hps) + " HPS", "spends " + num(o.spend, 1) + " mana/s, regains " + num(o.regen, 1)];
        if (o.hpm != null) facts.push(num(o.hpm, 1) + " healing per mana");
        if (m[0] === "max" && o.oom != null) facts.push("out of mana after " + num(o.oom) + " s");
        if (m[0] !== "max") facts.push("top ranks only: " + num(x.top[state.scen][m[0] === "fight" ? 1 : 2]) + " HPS");
        kids.push(section(titles[m[0]], [el("p", { "class": "dps-meta", text: facts.join(" · ") }), mixList(o)]));
      });
      var src = R.fight.src, tot = src.reduce(function (s, p) { return s + Math.max(0, p[1]); }, 0) || 1;
      kids.push(section("Sustained healing by source", [el("ul", {}, src.map(function (p) {
        return el("li", { text: N[p[0]] + ": " + num(p[1], 1) + " HPS (" + Math.round(p[1] / tot * 100) + "%)" });
      }))]));
      if (x.dps) {
        var dt = x.dps.src.reduce(function (s, p) { return s + p[1]; }, 0) || 1;
        kids.push(section("Off-damage: " + num(x.dps.dps, 1) + " DPS with the " + x.dps.rot + " damage rotation", [el("ul", {}, x.dps.src.map(function (p) {
          return el("li", { text: N[p[0]] + ": " + num(p[1], 1) + " DPS (" + Math.round(p[1] / dt * 100) + "%)" });
        }))]));
      }
      var g = x.gear === "crafted" ? data.gear[x["class"]] : null;
      if (g) {
        var rowsG = SLOT_ORDER.filter(function (s) { return g.items[s]; }).map(function (s) {
          var ench = g.enchants.filter(function (e) { return e.slot === s; }).map(function (e) { return e.name.indexOf("$") < 0 ? e.name : "Healing and spell damage"; }).join(", ");
          return el("tr", {}, [el("td", { text: SLOT_NAME[s] }), el("td", { text: g.items[s].name }), numCell(g.items[s].ilvl), el("td", { text: ench || "–" })]);
        });
        var statTxt = Object.keys(STAT_NAME).filter(function (k) { return g.stats[k]; }).map(function (k) { return STAT_NAME[k] + " " + g.stats[k]; });
        kids.push(section("Gear (best craftable for healing)", [el("div", { "class": "dps-scroll" }, [el("table", { "class": "dps-table" }, [
          el("thead", {}, [el("tr", {}, ["Slot", "Item", "Item level", "Enchant"].map(function (h) { return el("th", { scope: "col", text: h }); }))]),
          el("tbody", {}, rowsG)])]), el("p", { "class": "dps-meta", text: "Gear totals: " + statTxt.join(", ") + "." })]));
      }
      kids.push(el("p", { "class": "dps-meta", text: "Data confidence: " + Math.round(x.share * 100) + "% of the inputs this build reads are Forever client values; the rest are Classic rules or assumptions." }));
      return el("div", { "class": "dps-spec" }, kids);
    }

    function draw() {
      var sign = state.dir === "ascending" ? -1 : 1;
      var list = pool().sort(function (a, b) { return sign * (value(b, state.sort) - value(a, state.sort)); });
      var all = list.slice();
      if (state.best) { var seen = {}; list = list.filter(function (x) { var k = x["class"] + x.build; if (seen[k]) return false; seen[k] = 1; return true; }); }
      var top = Math.max.apply(null, list.map(function (x) { return value(x, state.sort); }).concat([0])) || 1;

      // Best picks for the current filters.
      function bestBy(key) { return all.slice().sort(function (a, b) { return value(b, key) - value(a, key); })[0]; }
      var cards = [["Most healing in the fight", "total", "healing", 0], ["Best healing per mana", "hpm", "per mana", 2], ["Longest at maximum pace", "empty", "s until empty", 1],
        ["Best endless healing", "endless", "HPS", 1], ["Highest maximum healing", "max", "HPS", 1], ["Most off-damage", "dps", "DPS", 1]];
      picks.replaceChildren.apply(picks, all.length ? cards.map(function (c) {
        var x = bestBy(c[1]);
        return el("div", { "class": "heal-pick" }, [el("span", { "class": "heal-pick-k", text: c[0] }), el("strong", { text: num(value(x, c[1]), c[3]) + " " + c[2] }),
          el("span", { text: buildOf(x).name }), el("span", { "class": "dps-meta", text: RACENAME[x.race] + " " + CLSNAME[x["class"]] })]);
      }) : []);

      // Same shape as the DPS by level table: class pill, build, race, one main column with a bar
      // (the metric the table is sorted by), then the other headline numbers.
      var LABEL = { fight: "Sustained HPS", total: "Total healing in the fight", hpm: "Healing per mana", empty: "Seconds until empty",
        sustain: "Sustain (% of maximum)", endless: "Endless HPS", max: "Maximum HPS", dps: "Off-DPS" };
      var DIGITS = { fight: 1, total: 0, hpm: 2, empty: 1, sustain: 1, endless: 1, max: 1, dps: 1 };
      var UNIT = { empty: " s", sustain: "%" };
      // Short headers and whole numbers for the side columns keep the build names on one or two lines.
      var SHORT = { fight: "Sustained HPS", hpm: "Per mana", empty: "Empty in", max: "Max HPS", dps: "Off-DPS" };
      var SIDE_DIGITS = { fight: 1, hpm: 2, empty: 1, max: 0, dps: 0 };
      function show(x, key, side) { return num(value(x, key), side ? SIDE_DIGITS[key] : DIGITS[key]) + (UNIT[key] || ""); }
      var side = ["fight", "hpm", "empty", "max", "dps"].filter(function (k) { return k !== state.sort; });
      var span = String(5 + side.length);
      var body = el("tbody");
      list.forEach(function (x, i) {
        var b = buildOf(x);
        var btn = el("button", { type: "button", "class": "dps-spec-btn", "aria-expanded": "false", text: b.name });
        var tr = el("tr", { "class": "dps-spec-row" }), detail = null;
        function toggle() {
          if (detail) { detail.remove(); detail = null; tr.classList.remove("is-open"); btn.setAttribute("aria-expanded", "false"); return; }
          detail = el("tr", { "class": "dps-spec-detail" }, [el("td", { colspan: span }, [panel(x)])]);
          tr.after(detail); tr.classList.add("is-open"); btn.setAttribute("aria-expanded", "true");
        }
        btn.addEventListener("click", function (ev) { ev.stopPropagation(); toggle(); });
        tr.addEventListener("click", toggle);
        var bar = el("span", { "class": "dps-bar", "aria-hidden": "true" });
        bar.style.setProperty("--v", (value(x, state.sort) / top * 100).toFixed(1) + "%");
        [el("td", { text: String(i + 1) }),
          el("td", {}, [el("span", { "class": "pill pill--" + x["class"], text: CLSNAME[x["class"]] })]),
          el("td", {}, [btn]),
          el("td", { text: RACENAME[x.race] }),
          el("td", { "class": "dps-num" }, [bar, el("strong", { text: show(x, state.sort) })])
        ].concat(side.map(function (k) { return el("td", { "class": "dps-num", text: show(x, k, true) }); }))
          .forEach(function (td) { tr.appendChild(td); });
        body.appendChild(tr);
      });
      function sorter(k) {
        return { active: k === state.sort, dir: state.dir, go: function () {
          state.dir = k === state.sort && state.dir === "descending" ? "ascending" : "descending";
          state.sort = k; controls.querySelectorAll("select")[4].value = k; draw();
        } };
      }
      holder.replaceChildren(el("table", { "class": "dps-table heal-table", "data-sort": "own",
        "data-caption": "Healing by build and race, " + (state.scen === "tank" ? "one target" : "party of 5") + ", sorted by " + LABEL[state.sort] + ", " + state.dir }, [
        el("thead", {}, [el("tr", {}, [th("#", TIP.rank), th("Class"), th("Build (click for the full build)", TIP.build), th("Race", TIP.race),
          th(LABEL[state.sort], TIP[state.sort], sorter(state.sort))]
          .concat(side.map(function (k) { return th(SHORT[k], TIP[k] + " Click to sort by it.", sorter(k)); })))]), body]));
      meta.textContent = list.length + " of " + data.rows.filter(function (x) { return x.gear === state.gear; }).length + " race and build pairs shown. Level " + data.level +
        ", " + (state.scen === "tank" ? "one target taking all the damage" : "a party of 5, everyone hurt") + ". Sustained = a " + Math.round(fight / 60) +
        "-minute fight that ends on empty mana. The first number column is the one the table is sorted by. Healing per mana is for the sustained mix. Seconds until empty is at maximum pace. Off-DPS = the same build and gear dealing damage for " + Math.round(data.dps_fight_seconds / 60) + " minutes.";
    }

    function select(labelText, key, opts) {
      var s = el("select");
      opts.forEach(function (o) { s.appendChild(el("option", { value: o[0], text: o[1] })); });
      s.value = state[key];
      s.addEventListener("change", function () { state[key] = s.value; if (key === "sort") state.dir = "descending"; draw(); });
      return el("label", {}, [labelText, s]);
    }
    var cb = el("input", { type: "checkbox" });
    cb.checked = state.best;
    cb.addEventListener("change", function () { state.best = cb.checked; draw(); });
    [select("Class", "cls", [["all", "All healing classes"]].concat(Object.keys(CLSNAME).map(function (c) { return [c, CLSNAME[c]]; }))),
      select("Healing", "scen", [["tank", "One target (tank)"], ["group", "Party of 5"]]),
      select("Gear", "gear", [["crafted", "Best craftable gear"], ["none", "No gear"]]),
      select("Builds", "role", [["all", "Healers and hybrids"], ["healer", "Healers only"], ["hybrid", "Hybrids only"]]),
      select("Sort by", "sort", [["fight", "Sustained healing"], ["total", "Total healing in the fight"], ["hpm", "Healing per mana"], ["empty", "Seconds until empty"], ["sustain", "Sustain %"], ["endless", "Endless healing"], ["max", "Maximum healing"], ["dps", "Off-damage"]]),
      el("label", { "class": "dps-check" }, [cb, "Best race only"])
    ].forEach(function (c) { controls.appendChild(c); });
    box.replaceChildren(controls, picks, meta, holder);
    draw();
  }

  // ---------- Ledger: every talent, ability and stat (docs/assets/data/heal-ledger.json) ----------
  function signed(v, d) { return (v > 0 ? "+" : "") + num(v, d == null ? 1 : d); }
  function ledgerTable(cols, rows, cls) {
    return el("div", { "class": "dps-scroll" }, [el("table", { "class": "dps-table heal-ledger " + (cls || "") }, [
      el("thead", {}, [el("tr", {}, cols.map(function (c) { return th(c[0], c[1]); }))]),
      el("tbody", {}, rows)])]);
  }
  function td(text, cls) { return el("td", { "class": cls == null ? "dps-num" : cls, text: String(text) }); }   // "" = a text cell
  function barCell(text, share, strong) {
    var bar = el("span", { "class": "dps-bar", "aria-hidden": "true" });
    bar.style.setProperty("--v", Math.max(0, Math.min(100, share * 100)).toFixed(1) + "%");
    return el("td", { "class": "dps-num" }, [bar, strong ? el("strong", { text: text }) : text]);
  }
  function renderLedger(box, data) {
    var state = { cls: "priest", scen: "tank", ranks: false, zero: true };
    var controls = el("div", { "class": "dps-filters" }), out = el("div");
    var DPS_NOISE = 3, MODE_NAME = { max: "maximum", fight: "sustained", endless: "endless" };

    function kpi(label, value, unit, sub, share, tip) {
      var kids = [el("span", { "class": "heal-kpi-k heal-tip", "data-tip": tip, tabindex: "0", text: label }),
        el("span", { "class": "heal-kpi-v" }, [el("strong", { text: value }), el("small", { text: " " + unit })])];
      if (share != null) {
        var m = el("span", { "class": "heal-meter", "aria-hidden": "true" }); m.style.setProperty("--v", (share * 100).toFixed(1) + "%"); kids.push(m);
      }
      kids.push(el("span", { "class": "heal-kpi-s", text: sub }));
      return el("div", { "class": "heal-kpi" }, kids);
    }
    function chip(label, value) { return el("span", { "class": "heal-chip" }, [el("span", { text: label }), el("strong", { text: value })]); }

    function overview(c, sc) {
      var base = c.base[sc], st = c.stats, mx = base[0] || 1;
      var pts = Object.keys(c.points).map(function (t) { return c.points[t] + " " + t; }).join(" / ");
      var hp = c.weights.filter(function (w) { return w.key === "healing"; })[0].d[sc][1] || 1;
      var stats = c.weights.filter(function (w) { return w.key !== "healing" && w.d[sc][1] > 0; })
        .sort(function (a, b) { return b.d[sc][1] - a.d[sc][1]; }).slice(0, 3);
      var tal = c.talents.slice().sort(function (a, b) { return b.d[sc][1] - a.d[sc][1]; }).slice(0, 3);
      var dmg = c.talents.filter(function (t) { return t.dps != null && t.dps >= DPS_NOISE; }).sort(function (a, b) { return b.dps - a.dps; }).slice(0, 3);
      var hero = el("section", { "class": "heal-hero heal-hero--" + state.cls, "aria-label": CLSNAME[state.cls] + " overview" }, [
        el("div", { "class": "heal-hero-head" }, [
          el("span", { "class": "pill pill--" + state.cls, text: CLSNAME[state.cls] }),
          el("div", {}, [el("p", { "class": "heal-hero-title", text: c.build_name }),
            el("p", { "class": "heal-hero-sub", text: RACENAME[c.race] + " · " + pts + " · best craftable healing gear · " + (sc === "tank" ? "one target" : "party of 5") })])]),
        el("p", { "class": "heal-hero-note", text: c.note }),
        el("div", { "class": "heal-kpis" }, [
          kpi("Sustained", num(base[1], 1), "HPS", num(base[1] / mx * 100, 1) + "% of maximum, for 5 minutes", base[1] / mx, TIP.fight),
          kpi("Endless", num(base[2], 1), "HPS", num(base[2] / mx * 100, 1) + "% of maximum, forever", base[2] / mx, TIP.endless),
          kpi("Maximum", num(base[0], 1), "HPS", "mana ignored", 1, TIP.max),
          kpi("Off-damage", num(c.dps, 1), "DPS", "same build and gear", null, TIP.dps)]),
        el("div", { "class": "heal-chips" }, [chip("Health", num(st.health)), chip("Mana", num(st.mana)), chip("Healing power", num(st.healing)),
          chip("Intellect", num(st.int)), chip("Spirit", num(st.spi)), chip("Spell crit", num(st.crit, 1) + "%"),
          chip("Regen casting", num(st.regen_cast, 0) + " / 5 s"), chip("Regen resting", num(st.regen_rest, 0) + " / 5 s")]),
        el("div", { "class": "heal-hero-cols" }, [
          el("div", {}, [el("h4", { text: "Best stats for sustained healing" }), el("ol", {}, stats.map(function (w) {
            return el("li", {}, [el("strong", { text: w.label }), " · " + (w.unit === "point" ? "one point" : w.unit) + " is worth " + num(w.d[sc][1] / hp, 1) + " healing power"]);
          }))]),
          el("div", {}, [el("h4", { text: "Most valuable healing talents" }), el("ol", {}, tal.map(function (t) {
            return el("li", {}, [el("strong", { text: t.name }), " · " + signed(t.d[sc][1]) + " sustained HPS"]);
          }))]),
          el("div", {}, [el("h4", { text: "Most valuable damage talents" }), el("ol", {}, dmg.map(function (t) {
            return el("li", {}, [el("strong", { text: t.name }), " · " + signed(t.dps) + " DPS"]);
          }))])])]);
      return hero;
    }

    function draw() {
      var c = data.classes[state.cls], sc = state.scen, kids = [overview(c, sc)];

      // Stats
      var hp = c.weights.filter(function (w) { return w.key === "healing"; })[0].d[sc];
      var topW = Math.max.apply(null, c.weights.map(function (w) { return w.d[sc][1]; })) || 1;
      kids.push(el("h3", { text: "Stats: healing gained per point" }));
      kids.push(ledgerTable([["Stat"], ["One point is", "The amount of the stat that the other columns are measured for."],
        ["Sustained HPS", "Sustained healing per second gained from one more point of the stat."],
        ["Worth in healing power", "How many points of healing power give the same sustained gain as one point of this stat."],
        ["Endless HPS", "Endless healing per second gained from one more point."], ["Maximum HPS", "Maximum healing per second gained from one more point."]],
      c.weights.map(function (w) {
        var d = w.d[sc];
        return el("tr", {}, [td(w.label, ""), td(w.unit), barCell(signed(d[1], 3), d[1] / topW, true), td(hp[1] ? num(d[1] / hp[1], 2) : "–"), td(signed(d[2], 3)), td(signed(d[0], 3))]);
      })));
      if (c.armor_buff && c.armor_buff.fight && sc === "tank") {
        var ab = c.armor_buff;
        kids.push(el("p", { "class": "dps-meta", text: ab.fight.talent + " armor buff uptime on the tank: " + Math.round(ab.fight.uptime * 100) + "% sustained, " +
          Math.round(ab.endless.uptime * 100) + "% endless, " + Math.round(ab.max.uptime * 100) + "% at maximum pace." }));
      }

      // Abilities
      kids.push(el("h3", { text: "Healing abilities" }));
      var acts = c.abilities.filter(function (a) { return a[sc] != null; }), last = {};
      acts.forEach(function (a) { last[a.spell + "|" + a.name.replace(/ \(Rank \d+\)/, "")] = a.name; });
      function usedIn(a) { return a.used.filter(function (u) { return u.indexOf(sc + "/") === 0; }).map(function (u) { return MODE_NAME[u.split("/")[1]]; }); }
      var shown = acts.filter(function (a) { return state.ranks || usedIn(a).length || last[a.spell + "|" + a.name.replace(/ \(Rank \d+\)/, "")] === a.name; });
      var topHps = Math.max.apply(null, shown.map(function (a) { return a[sc] / a.time; })) || 1;
      kids.push(el("p", { "class": "dps-meta", text: shown.length + " of " + acts.length + " castable ranks shown" + (state.ranks ? "." : ": the top rank of each spell and every rank a best mix uses.") }));
      kids.push(ledgerTable([["Ability"], ["Seconds per cast", "Time one cast takes: cast time or the 1.5 s global cooldown, whichever is longer."],
        ["Mana", "Mana per cast after talents and expected refunds."], ["Healing per cast", "Expected healing of one cast: average roll, healing power, talents and crit. Party heals count every target hit."],
        ["HPS while casting", "Healing per cast divided by seconds per cast: output if this were cast back to back."],
        ["Healing per mana", "Healing per cast divided by mana per cast."], ["Limit per minute", "Most casts per minute a cooldown or a one-per-target rule allows."],
        ["Best mix", "Which of the three optimal cast mixes use this rank."]],
      shown.map(function (a) {
        var used = usedIn(a);
        return el("tr", { "class": used.length ? "" : "heal-dim" }, [td(a.name, ""), td(num(a.time, 2)), td(num(a.cost, 0)), td(num(a[sc], 0)),
          barCell(num(a[sc] / a.time, 0), a[sc] / a.time / topHps), td(a.cost > 0 ? num(a[sc] / a.cost, 2) : "free"), td(a.cap == null ? "–" : num(a.cap, 2)),
          el("td", {}, used.length ? used.map(function (u) { return el("span", { "class": "dps-tag dps-tag--f", text: u }); }) : ["–"])]);
      }), "heal-abilities"));
      var o = c.other;
      kids.push(el("details", { "class": "heal-other" }, [el("summary", { text: "Other trained abilities (" + (o.healing_support.length + o.damage.length + o.utility.length) + ")" }),
        el("p", {}, [el("strong", { text: "Supporting the healing model: " }), o.healing_support.join(", ") || "none"]),
        el("p", {}, [el("strong", { text: "Used by the damage simulator: " }), o.damage.join(", ") || "none"]),
        el("p", {}, [el("strong", { text: "No healing or damage output, so nothing to calculate: " }), o.utility.join(", ")])]));

      // Talents
      kids.push(el("h3", { text: "Talents: value at maximum rank" }));
      var trees = [], topT = Math.max.apply(null, c.talents.map(function (t) { return t.d[sc][1]; })) || 1;
      c.talents.forEach(function (t) { if (trees.indexOf(t.tree) < 0) trees.push(t.tree); });
      function effect(t) { var d = t.d[sc]; return Math.abs(d[0]) >= 0.5 || Math.abs(d[1]) >= 0.5 || Math.abs(d[2]) >= 0.5; }
      function damage(t) { return t.dps != null && Math.abs(t.dps) >= DPS_NOISE; }
      trees.forEach(function (tree) {
        var all = c.talents.filter(function (t) { return t.tree === tree; }).sort(function (a, b) { return a.row - b.row; });
        var ts = all.filter(function (t) { return state.zero || effect(t) || damage(t); });
        kids.push(el("h4", { text: tree + " · " + (c.points[tree] || 0) + " points in the reference build" + (ts.length < all.length ? " · " + (all.length - ts.length) + " hidden" : "") }));
        kids.push(ledgerTable([["Talent"], ["Build", "Ranks the reference build has in this talent, out of its maximum."],
          ["Sustained HPS", "Sustained healing with the talent at maximum rank minus the same healer without it."],
          ["Endless HPS", "The same comparison for endless healing."], ["Maximum HPS", "The same comparison for maximum healing."],
          ["Off-DPS", "Damage per second with the talent minus without it. Changes under 3 DPS are simulator noise and show as 0."],
          ["What it does", "The talent's tooltip at maximum rank."]],
        ts.map(function (t) {
          var d = t.d[sc], h = effect(t), g = damage(t);
          var note = h || g ? "" : (t.heal ? "Calculated; worth nothing to this build. " : t.dmg ? "No measurable output change. " : "No healing or damage output: survival, control or utility. ");
          function v(x) { return h && Math.abs(x) >= 0.05 ? el("td", { "class": "dps-num " + (x > 0 ? "heal-pos" : "heal-neg"), text: signed(x) }) : el("td", { "class": "dps-num heal-zero", text: "0" }); }
          return el("tr", { "class": h || g ? "" : "heal-dim" }, [td(t.name, "heal-talent"), el("td", { "class": "dps-num" }, [t.ref ? el("span", { "class": "dps-tag", text: t.ref + "/" + t.max }) : "0/" + t.max]),
            h && d[1] > 0 ? barCell(signed(d[1]), d[1] / topT, true) : v(d[1]), v(d[2]), v(d[0]),
            t.dps == null ? td("–") : g ? el("td", { "class": "dps-num " + (t.dps > 0 ? "heal-pos" : "heal-neg"), text: signed(t.dps) }) : el("td", { "class": "dps-num heal-zero", text: "0" }),
            el("td", { "class": "heal-ledger-text", text: note + t.text })]);
        }), "heal-talents"));
      });
      out.replaceChildren.apply(out, kids);
    }
    function select(labelText, key, opts) {
      var s = el("select");
      opts.forEach(function (o) { s.appendChild(el("option", { value: o[0], text: o[1] })); });
      s.value = state[key];
      s.addEventListener("change", function () { state[key] = s.value; draw(); });
      return el("label", {}, [labelText, s]);
    }
    function check(labelText, key) {
      var cb = el("input", { type: "checkbox" });
      cb.checked = state[key];
      cb.addEventListener("change", function () { state[key] = cb.checked; draw(); });
      return el("label", { "class": "dps-check" }, [cb, labelText]);
    }
    controls.appendChild(select("Class", "cls", Object.keys(data.classes).map(function (k) { return [k, CLSNAME[k]]; })));
    controls.appendChild(select("Healing", "scen", [["tank", "One target (tank)"], ["group", "Party of 5"]]));
    controls.appendChild(check("Show every spell rank", "ranks"));
    controls.appendChild(check("Show talents with no effect", "zero"));
    box.replaceChildren(controls, out);
    draw();
  }

  function load(selector, file, draw, failText) {
    var box = document.querySelector(selector);
    if (!box || box.dataset.ready) return;
    box.dataset.ready = "1";
    var url = new URL("../assets/data/" + file, SCRIPT_SRC || location.href).href;
    fetch(url).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (data) { draw(box, data); })
      .catch(function () { box.replaceChildren(el("p", { text: failText })); });
  }
  function onPage() {
    load("[data-heal-sim]", "heal-sim.json", render, "The healing simulation could not be loaded.");
    load("[data-heal-ledger]", "heal-ledger.json", renderLedger, "The talent, ability and stat values could not be loaded.");
  }
  if (window.document$ && typeof window.document$.subscribe === "function") window.document$.subscribe(onPage);
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", onPage);
  else onPage();
})();
