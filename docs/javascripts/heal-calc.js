/* Forever Codex healing calculator (docs/guides/healing-calculator.md).
   Renders docs/assets/data/heal-sim.json, written by tools/healsim/run.py.
   Every number is model output: see tools/healsim/README.md for the method and its gaps. */
(function () {
  "use strict";
  var SCRIPT_SRC = document.currentScript ? document.currentScript.src : "";
  var CLSNAME = { priest: "Priest", paladin: "Paladin", druid: "Druid", shaman: "Shaman" };
  var RACENAME = { human: "Human", dwarf: "Dwarf", gnome: "Gnome", nelf: "Night Elf", sho: "High Order Skyborne",
    sws: "Windshaper Skyborne", orc: "Orc", troll: "Troll", tauren: "Tauren", undead: "Undead" };
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
  function section(title, kids) { return el("section", { "class": "dps-spec-sec" }, [el("h4", { text: title })].concat(kids)); }

  function render(box, data) {
    var N = data.names, builds = {}, fight = data.fight_seconds;
    data.builds.forEach(function (b) { builds[b["class"] + "/" + b.id] = b; });
    var state = { cls: "all", scen: "tank", gear: "crafted", role: "all", sort: "fight", best: true };
    var controls = el("div", { "class": "dps-filters" });
    var picks = el("div", { "class": "heal-picks" });
    var meta = el("p", { "class": "dps-meta" });
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
      var items = o.mix.map(function (m) { return el("li", { text: N[m[0]] + ": " + num(m[1], 1) + " casts/min, " + num(m[2], 1) + " HPS" }); });
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
      kids.push(el("p", { "class": "dps-meta", text: "Data confidence: " + Math.round(x.share * 100) + "% of the inputs this build read are Forever client values; the rest are Classic rules or assumptions." }));
      return el("div", { "class": "dps-spec" }, kids);
    }

    function draw() {
      var list = pool().sort(function (a, b) { return value(b, state.sort) - value(a, state.sort); });
      var all = list.slice();
      if (state.best) { var seen = {}; list = list.filter(function (x) { var k = x["class"] + x.build; if (seen[k]) return false; seen[k] = 1; return true; }); }
      var top = list.length ? value(list[0], state.sort) || 1 : 1;

      // Best picks for the current filters.
      function bestBy(key) { return all.slice().sort(function (a, b) { return value(b, key) - value(a, key); })[0]; }
      var cards = [["Most healing in the fight", "total", "healing", 0], ["Best healing per mana", "hpm", "per mana", 2], ["Longest at maximum pace", "empty", "s until empty", 1],
        ["Best endless healing", "endless", "HPS", 1], ["Highest healing", "max", "HPS", 1], ["Most off-damage", "dps", "DPS", 1]];
      picks.replaceChildren.apply(picks, all.length ? cards.map(function (c) {
        var x = bestBy(c[1]);
        return el("div", { "class": "heal-pick" }, [el("span", { "class": "heal-pick-k", text: c[0] }), el("strong", { text: num(value(x, c[1]), c[3]) + " " + c[2] }),
          el("span", { text: buildOf(x).name }), el("span", { "class": "dps-meta", text: RACENAME[x.race] + " " + CLSNAME[x["class"]] })]);
      }) : []);

      var body = el("tbody");
      list.forEach(function (x, i) {
        var b = buildOf(x), R = x.r[state.scen];
        var btn = el("button", { type: "button", "class": "dps-spec-btn", "aria-expanded": "false", text: b.name });
        var tr = el("tr", { "class": "dps-spec-row" }), detail = null;
        function toggle() {
          if (detail) { detail.remove(); detail = null; tr.classList.remove("is-open"); btn.setAttribute("aria-expanded", "false"); return; }
          detail = el("tr", { "class": "dps-spec-detail" }, [el("td", { colspan: "12" }, [panel(x)])]);
          tr.after(detail); tr.classList.add("is-open"); btn.setAttribute("aria-expanded", "true");
        }
        btn.addEventListener("click", function (ev) { ev.stopPropagation(); toggle(); });
        tr.addEventListener("click", toggle);
        var bar = el("span", { "class": "dps-bar", "aria-hidden": "true" });
        bar.style.setProperty("--v", Math.round(value(x, state.sort) / top * 100) + "%");
        [el("td", { "class": "dps-num", text: String(i + 1) }), el("td", { text: CLSNAME[x["class"]] }),
          el("td", {}, [btn, b.role === "hybrid" ? el("span", { "class": "dps-tag", text: "hybrid" }) : null]),
          el("td", { text: RACENAME[x.race] }),
          el("td", { "class": "dps-num" }, [bar, num(R.fight.hps, 1)]), numCell(total(x)), numCell(R.fight.hpm, 2), numCell(R.max.oom, 1),
          el("td", { "class": "dps-num", text: num(sustain(x), 1) + "%" }), numCell(R.endless.hps, 1), numCell(R.max.hps, 1),
          numCell(x.dps ? x.dps.dps : null)
        ].forEach(function (td) { tr.appendChild(td); });
        body.appendChild(tr);
      });
      holder.replaceChildren(el("table", { "class": "dps-table" }, [
        el("thead", {}, [el("tr", {}, ["#", "Class", "Build (click for the full build)", "Race", "Sustained HPS", "Total healing in the fight", "Healing per mana", "Seconds until empty", "Sustain", "Endless HPS", "Maximum HPS", "Off-DPS"]
          .map(function (h) { return el("th", { scope: "col", text: h }); }))]), body]));
      meta.textContent = list.length + " of " + data.rows.filter(function (x) { return x.gear === state.gear; }).length + " race and build pairs shown. Level " + data.level +
        ", " + (state.scen === "tank" ? "one target taking all the damage" : "a party of 5, everyone hurt") + ". Sustained = a " + Math.round(fight / 60) +
        "-minute fight that ends on empty mana. Healing per mana is for the sustained mix. Seconds until empty is at maximum pace. Sustain = sustained healing as a share of maximum. Off-DPS = the same build and gear dealing damage for " + Math.round(data.dps_fight_seconds / 60) + " minutes.";
    }

    function select(labelText, key, opts) {
      var s = el("select");
      opts.forEach(function (o) { s.appendChild(el("option", { value: o[0], text: o[1] })); });
      s.value = state[key];
      s.addEventListener("change", function () { state[key] = s.value; draw(); });
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

  function onPage() {
    var box = document.querySelector("[data-heal-sim]");
    if (!box || box.dataset.ready) return;
    box.dataset.ready = "1";
    var url = new URL("../assets/data/heal-sim.json", SCRIPT_SRC || location.href).href;
    fetch(url).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (data) { render(box, data); })
      .catch(function () { box.replaceChildren(el("p", { text: "The healing simulation could not be loaded." })); });
  }
  if (window.document$ && typeof window.document$.subscribe === "function") window.document$.subscribe(onPage);
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", onPage);
  else onPage();
})();
