/* Forever Codex calculator tables: shared behaviour for the DPS and healing calculators.
   Every table inside a .dps-calc block gets, without the calculators having to ask:
     - a caption and a labelled, keyboard-scrollable region;
     - column headers that sort on click (unless the calculator sorts the table itself);
     - a hover / focus description on headers that have one, plus a written column guide;
     - a header row that stays in view while the page scrolls;
     - a polite live message when the table is re-sorted or redrawn.
   The calculators redraw their tables on every filter change, so a MutationObserver
   re-applies all of this and restores the last sort. */
(function () {
  "use strict";

  // Header descriptions for tables that do not set their own (data-tip on the header).
  var TIPS = {
    "#": "Position in the current order.",
    "Class": "The character's class.",
    "Race": "The character's race. Each spec is run for every race its class can be.",
    "Spec": "The talent specialization.",
    "Spec (open for breakdown)": "The talent specialization. Open it to see damage by ability.",
    "Spec (click for the full build)": "The talent specialization. Select a row for its talents, gear, opening sequence and damage by source.",
    "DPS": "Estimated damage per second from the formula model, using the inputs further down the page.",
    "Estimated DPS": "Mean damage per second over the simulated fights. The ± value is the 95% confidence interval of the simulation, not the error of the estimate.",
    "Simulated DPS": "Mean damage per second at the chosen level and gear. The ± value is simulation noise only.",
    "vs previous level": "Change in DPS from the level before. A fall is shown in red.",
    "Chart": "Adds the row to the chart above the table, or removes it. Up to 6 rows.",
    "Level": "Character level.",
    "Change": "Change in DPS from the level before.",
    "Talent point": "The talent point spent at this level.",
    "Largest damage sources": "Share of the damage by source at this level.",
    "Adds": "DPS lost when the talent is removed from the build, as a share of the full build.",
    "Above noise": "Yes when the change is larger than the confidence interval of the simulation.",
    "Status": "What the simulator does with it.",
    "vs best race": "This race's damage relative to the best race of the same spec. 'best' marks the best race.",
    "Data confidence": "Share of the inputs this spec reads that are Forever values, not Classic values or assumptions.",
    "Slot": "The equipment slot.",
    "Item": "The crafted item chosen for the slot.",
    "Item level": "The item's level in the game data.",
    "Enchant": "The enchantment applied to the item, if any.",
    "Pace": "Which cast mix the row describes: sustained, endless or maximum.",
    "Spell": "The spell and rank cast."
  };
  var state = new WeakMap();     // persistent container -> { label, dir } of the last sort
  var sticky = [];               // tables whose header follows the scroll
  var live = null, announceTimer = 0;

  function text(el) { return (el.textContent || "").replace(/\s+/g, " ").trim(); }
  function announce(msg) {
    if (!live) {
      live = document.createElement("div");
      live.className = "fc-sr-only calc-live";
      live.setAttribute("role", "status");
      live.setAttribute("aria-live", "polite");
      document.body.appendChild(live);
    }
    clearTimeout(announceTimer);
    announceTimer = setTimeout(function () { live.textContent = msg; }, 150);
  }

  // The nearest heading before a table names it.
  function headingFor(node) {
    for (var n = node; n && n !== document.body; n = n.parentElement) {
      for (var p = n.previousElementSibling; p; p = p.previousElementSibling) {
        if (/^H[1-6]$/.test(p.tagName)) return text(p).replace(/[¶#]\s*$/, "").trim();
        var inner = p.querySelector && p.querySelector("h2, h3, h4, h5");
        if (inner && !p.matches(".dps-scroll, table")) { var hs = p.querySelectorAll("h2, h3, h4, h5"); return text(hs[hs.length - 1]).replace(/[¶#]\s*$/, "").trim(); }
      }
    }
    return "Results";
  }

  // ---------- sorting ----------
  function cellValue(td) {
    var t = text(td);
    if (!t || t === "–" || t === "-") return null;
    if (/^(best|tied)$/i.test(t)) return 0;
    if (/^(free|never)$/i.test(t)) return Infinity;
    var m = t.replace(/,/g, "").match(/^\s*([+\-−]?\d*\.?\d+)/);   // a number at the start only: "Heal (Rank 3)" is text
    return m ? parseFloat(m[1].replace("−", "-")) : NaN;
  }
  function groups(tbody) {     // a row plus any detail row that follows it
    var out = [];
    Array.prototype.forEach.call(tbody.children, function (tr) {
      if (tr.classList.contains("dps-spec-detail") && out.length) out[out.length - 1].push(tr); else out.push([tr]);
    });
    return out;
  }
  function sortBy(table, index, dir, quiet) {
    var tbody = table.tBodies[0];
    if (!tbody) return;
    var g = groups(tbody);
    var vals = g.map(function (rows) { var c = rows[0].children[index]; return c ? cellValue(c) : null; });
    var numeric = vals.filter(function (v) { return v !== null && !isNaN(v); }).length >= vals.filter(function (v) { return v !== null; }).length / 2;
    var keyed = g.map(function (rows, i) {
      var c = rows[0].children[index];
      return { rows: rows, v: numeric ? vals[i] : (c ? text(c).toLowerCase() : ""), i: i };
    });
    keyed.sort(function (a, b) {
      var bad = function (x) { return x.v === null || (numeric && isNaN(x.v)) || x.v === ""; };
      if (bad(a) || bad(b)) return bad(a) === bad(b) ? a.i - b.i : (bad(a) ? 1 : -1);      // empty cells last
      var d = numeric ? a.v - b.v : a.v.localeCompare(b.v);
      return (dir === "ascending" ? d : -d) || a.i - b.i;
    });
    keyed.forEach(function (k) { k.rows.forEach(function (tr) { tbody.appendChild(tr); }); });
    var heads = table.tHead.rows[0].cells;
    if (text(heads[0]) === "#") keyed.forEach(function (k, i) { if (k.rows[0].children[0]) k.rows[0].children[0].textContent = String(i + 1); });
    Array.prototype.forEach.call(heads, function (h, i) {
      if (i === index) h.setAttribute("aria-sort", dir); else h.removeAttribute("aria-sort");
      var b = h.querySelector(".calc-sort");
      if (b) b.classList.toggle("is-active", i === index);
    });
    if (!quiet) announce("Sorted by " + text(heads[index]) + ", " + dir + ".");
    return numeric;
  }
  function makeSortable(table, holder) {
    var heads = table.tHead.rows[0].cells;
    Array.prototype.forEach.call(heads, function (h, index) {
      var label = text(h);
      if (label === "#" || !label) return;
      var old = h.firstElementChild && h.children.length === 1 ? h.firstElementChild : null;
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "calc-sort" + (old && old.classList.contains("heal-tip") ? " heal-tip" : "");
      btn.textContent = label;
      var tip = (old && old.getAttribute("data-tip")) || h.getAttribute("data-tip");
      if (tip) btn.setAttribute("data-tip", tip);
      h.replaceChildren(btn);
      btn.addEventListener("click", function () {
        var cur = h.getAttribute("aria-sort"), first = cellValue(table.tBodies[0] && table.tBodies[0].rows[0] ? table.tBodies[0].rows[0].cells[index] : h);
        var dir = cur === "descending" ? "ascending" : cur === "ascending" ? "descending" : (first === null || isNaN(first) ? "ascending" : "descending");
        sortBy(table, index, dir);
        state.set(holder, { label: label, dir: dir });
      });
    });
    var last = state.get(holder);
    if (last) Array.prototype.forEach.call(heads, function (h, index) { if (text(h) === last.label) sortBy(table, index, last.dir, true); });
    else {      // the calculator drew it in some order: find the number column it is sorted by and mark it
      var rows = groups(table.tBodies[0]);
      for (var c = 1; c < heads.length && rows.length > 2; c++) {
        var vals = rows.map(function (r) { return r[0].children[c] ? cellValue(r[0].children[c]) : null; });
        if (vals.some(function (v) { return v === null || isNaN(v); }) || vals[0] === vals[vals.length - 1]) continue;
        if (vals.every(function (v, i) { return i === 0 || v <= vals[i - 1]; })) {
          heads[c].setAttribute("aria-sort", "descending");
          var b = heads[c].querySelector(".calc-sort");
          if (b) b.classList.add("is-active");
          break;
        }
      }
    }
  }

  // ---------- sticky header ----------
  function topOffset() {
    var off = 0;
    [".md-header", ".md-tabs"].forEach(function (sel) {
      var e = document.querySelector(sel);
      if (!e) return;
      var r = e.getBoundingClientRect();
      if (r.height && r.bottom > off && r.top <= 0.5 + off) off = r.bottom;
    });
    return off;
  }
  function place() {
    var off = topOffset();
    sticky = sticky.filter(function (t) { return t.isConnected; });
    sticky.forEach(function (table) {
      var r = table.getBoundingClientRect(), head = table.tHead, hh = head.offsetHeight;
      var y = Math.max(0, Math.min(off - r.top, r.height - hh * 2));
      var cells = head.rows[0].cells;
      for (var i = 0; i < cells.length; i++) cells[i].style.transform = y > 0 ? "translateY(" + Math.round(y) + "px)" : "";
      table.classList.toggle("is-stuck", y > 0);
    });
  }
  var ticking = false;
  // Next frame when the tab is visible; a timer as the fallback (animation frames never fire in a background tab).
  function frame(fn) { var done = false; function run() { if (!done) { done = true; fn(); } } requestAnimationFrame(run); setTimeout(run, 80); }
  function onScroll() { if (!ticking) { ticking = true; frame(function () { ticking = false; place(); }); } }

  // ---------- one table ----------
  function enhance(table) {
    if (table.dataset.calc || !table.tHead || !table.tHead.rows.length) return;
    table.dataset.calc = "1";
    var wrap = table.parentElement, holder = wrap && wrap.classList.contains("dps-scroll") ? wrap.parentElement : wrap;
    var nested = !!table.closest(".dps-spec");
    var heads = table.tHead.rows[0].cells;

    // header descriptions
    Array.prototype.forEach.call(heads, function (h) {
      var inner = h.firstElementChild;
      if (!(inner && inner.getAttribute("data-tip")) && !h.getAttribute("data-tip") && TIPS[text(h)]) h.setAttribute("data-tip", TIPS[text(h)]);
    });
    var guideRows = Array.prototype.map.call(heads, function (h) {
      var inner = h.firstElementChild, tip = (inner && inner.getAttribute("data-tip")) || h.getAttribute("data-tip");
      return tip ? [text(h), tip.replace(/ Click to sort by it\.$/, "")] : null;
    }).filter(Boolean);

    // a header sits over its column: right-aligned over numbers, left-aligned over text
    var firstRow = table.tBodies[0] && table.tBodies[0].rows[0];
    if (firstRow) Array.prototype.forEach.call(heads, function (h, i) {
      var c = firstRow.cells[i];
      h.classList.add(c && c.classList.contains("dps-num") ? "calc-num" : "calc-text");
    });

    // caption and scroll region
    var name = table.getAttribute("data-caption") || headingFor(wrap || table);
    var own = table.getAttribute("data-sort") === "own", editable = !!table.querySelector("input, select, textarea");
    var sortable = !editable && table.tBodies[0] && table.tBodies[0].rows.length > 1;
    if (!table.caption) {
      var cap = table.createCaption();
      cap.className = "fc-sr fc-sr-only";
      cap.textContent = name + (sortable ? ". Column headers are buttons that sort the table." : ".");
    }
    if (wrap && wrap.classList.contains("dps-scroll")) {
      wrap.setAttribute("role", "region");
      wrap.setAttribute("aria-label", name + " table");
      wrap.setAttribute("tabindex", "0");
    }

    if (sortable && !own) makeSortable(table, holder);
    else if (!own) Array.prototype.forEach.call(heads, function (h) {       // not sortable: still let the description take focus
      if (h.getAttribute("data-tip") && !h.firstElementChild) { h.setAttribute("tabindex", "0"); h.classList.add("heal-tip"); }
    });

    // written guide for the main tables (the hover text must not be the only place it lives)
    if (!nested && guideRows.length && wrap && !(wrap.nextElementSibling && wrap.nextElementSibling.classList.contains("calc-guide"))) {
      var d = document.createElement("details");
      d.className = "calc-guide";
      var sum = document.createElement("summary");
      sum.textContent = "How to read this table";
      var p = document.createElement("p");
      p.textContent = (sortable ? "Select a column header to sort by it; select it again to reverse the order. " : "") +
        "Point at or focus a header for its meaning. " + (table.querySelector(".dps-spec-btn") ? "Select a row's name to open its full details. " : "") +
        "The header row stays in view while you scroll.";
      var dl = document.createElement("dl");
      guideRows.forEach(function (g) {
        var dt = document.createElement("dt"), dd = document.createElement("dd");
        dt.textContent = g[0]; dd.textContent = g[1]; dl.appendChild(dt); dl.appendChild(dd);
      });
      d.appendChild(sum); d.appendChild(p); d.appendChild(dl);
      wrap.after(d);
    }

    if (!nested && table.tBodies[0] && table.tBodies[0].rows.length > 6) { table.classList.add("calc-sticky"); sticky.push(table); }
    if (!nested) announce(name + ": " + groups(table.tBodies[0]).length + " rows.");
  }
  function scan(root) {
    Array.prototype.forEach.call(root.querySelectorAll(".dps-filters"), function (f) {
      if (!f.getAttribute("role")) { f.setAttribute("role", "group"); f.setAttribute("aria-label", "Filters"); }
    });
    Array.prototype.forEach.call(root.querySelectorAll("table.dps-table, table.dps-inputs"), enhance);
    // a guide left behind by a table that was redrawn
    Array.prototype.forEach.call(root.querySelectorAll(".calc-guide"), function (g) {
      var prev = g.previousElementSibling;
      if (!prev || !prev.classList.contains("dps-scroll")) g.remove();
    });
    place();
  }

  var watched = new WeakSet();
  function onPage() {
    Array.prototype.forEach.call(document.querySelectorAll(".dps-calc"), function (root) {
      if (watched.has(root)) return;
      watched.add(root);
      var pending = false;
      new MutationObserver(function () {
        if (pending) return;
        pending = true;
        setTimeout(function () { pending = false; scan(root); }, 0);   // not requestAnimationFrame: that never fires in a background tab
      }).observe(root, { childList: true, subtree: true });
      scan(root);
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  if (window.document$ && typeof window.document$.subscribe === "function") window.document$.subscribe(onPage);
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", onPage);
  else onPage();
})();
