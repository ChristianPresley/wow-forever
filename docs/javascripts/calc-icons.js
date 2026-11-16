/* Forever Codex icons, on every page.
   Puts a small original glyph next to ability, talent, tree, stat, gear slot, item, profession,
   race, class, dungeon and raid names: in the DPS and healing calculators (which redraw, so they
   are watched) and in the written pages (bold names, talent nodes, table cells, headings, chips).
   Each page title also gets the emblem of its section. The glyphs are drawn for this site
   (tools/icons/glyphs.json) and tinted by spell school; no game artwork is used.
   docs/assets/data/icons.json (tools/icons/build.py) says which glyph each name gets.
   Icons are decoration: they are hidden from assistive technology and never replace a name. */
(function () {
  "use strict";
  var SCRIPT_SRC = document.currentScript ? document.currentScript.src : "";
  var NS = "http://www.w3.org/2000/svg";
  var data = null, loading = null, itemsLoaded = false;
  // Where names appear. Each entry: selector, and how to read the name from the element.
  var TARGETS = [
    "table.heal-ledger tbody td:first-child", ".dps-spec table tbody td:first-child", ".dps-spec li", ".dps-breakdown li",
    ".heal-hero-cols li strong", ".heal-chip > span:first-child", ".dps-spec-btn", "details.dps-breakdown > summary", ".dps-spec-trees h5"
  ].join(", ");

  function sprite() {
    if (document.getElementById("gi-sprite")) return;
    var svg = document.createElementNS(NS, "svg");
    svg.id = "gi-sprite";
    svg.setAttribute("aria-hidden", "true");
    svg.style.display = "none";
    var html = "";
    Object.keys(data.glyphs).forEach(function (k) {
      var g = data.glyphs[k];
      html += '<symbol id="gi-' + k + '" viewBox="0 0 24 24">' +
        (g.s ? '<path fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" d="' + g.s + '"/>' : "") +
        (g.f ? '<path fill="currentColor" d="' + g.f + '"/>' : "") + "</symbol>";
    });
    Object.keys(data.sigils).forEach(function (k) { html += '<symbol id="gi-class-' + k + '" viewBox="0 0 24 24">' + data.sigils[k] + "</symbol>"; });
    svg.innerHTML = html;
    document.body.appendChild(svg);
  }
  function icon(glyph, tint) {
    var svg = document.createElementNS(NS, "svg");
    svg.setAttribute("class", "gi gi--" + tint);
    svg.setAttribute("viewBox", "0 0 24 24");
    svg.setAttribute("aria-hidden", "true");
    svg.setAttribute("focusable", "false");
    var use = document.createElementNS(NS, "use");
    use.setAttribute("href", "#gi-" + glyph);
    svg.appendChild(use);
    return svg;
  }
  // Put a glyph at the start of an element. A word joiner after it keeps the first word on the glyph's line.
  // The glyph goes inside a no-wrap span with the first word, so a line break can never leave it
  // alone above its name. It goes down to the first text: in "<td><a>Name</a></td>" it sits in the link.
  function firstNode(el) {
    var n = el.firstChild;
    while (n && n.nodeType === 3 && !n.nodeValue.trim()) n = n.nextSibling;
    return n;
  }
  function prefix(el, glyph, tint) {
    var svg = icon(glyph, tint), node = el, first = firstNode(el);
    while (first && first.nodeType === 1 && /^(A|STRONG|B|EM|SPAN)$/.test(first.tagName) && !/pill|fc-sr|dps-spec-t|twemoji/.test(first.getAttribute("class") || "")) {
      node = first;
      first = firstNode(node);
    }
    var keep = document.createElement("span");
    keep.className = "gi-keep";
    keep.appendChild(svg);
    if (first && first.nodeType === 3) {
      var m = first.nodeValue.match(/^(\s*)(\S+)([\s\S]*)$/);
      if (m) { keep.appendChild(document.createTextNode(m[2])); first.nodeValue = m[3]; }
    }
    node.insertBefore(keep, first || null);
    return svg;
  }
  // Name tables. A class page reads only that class's abilities and talents, so a name that another
  // class also uses (Precision, Subtlety, Charge) cannot bring the wrong glyph. Other pages and the
  // calculators read every class.
  var merged = null;
  function everyClass() {
    if (!merged) {
      merged = {};
      Object.keys(data.classes || {}).forEach(function (c) {
        var m = data.classes[c];
        Object.keys(m).forEach(function (k) { if (!merged[k]) merged[k] = m[k]; });
      });
    }
    return merged;
  }
  function find(name, cls, everywhere) {
    var items = data.items || {};
    if (everywhere) return data.names[name] || everyClass()[name] || items[name] || null;
    if (cls && data.classes && data.classes[cls]) return data.classes[cls][name] || data.names[name] || items[name] || null;
    // profession pages list items, not abilities: "Nightfall" there is an axe, not a Warlock talent
    if (/(^|\/)professions\//.test(location.pathname)) return items[name] || data.names[name] || null;
    return data.names[name] || items[name] || null;
  }

  // "Greater Heal (Rank 5): 21.6 casts/min" -> Greater Heal; "Deep Wounds 3" -> Deep Wounds;
  // "Divine Favor + Holy Light (Rank 9)" -> Holy Light; "Power Word: Shield (absorb)" -> Power Word: Shield.
  function lookup(text) {
    var t = text.replace(/\s+/g, " ").replace(/^[\d.]+ ?s?\s+(?=[A-Z])/, "").trim();
    var cuts = [t], i = t.indexOf(": ");
    while (i >= 0) { cuts.push(t.slice(0, i)); i = t.indexOf(": ", i + 1); }
    cuts.push(t.split(" · ")[0]);
    for (var c = cuts.length - 1; c >= 0; c--) cuts.push.apply(cuts, cuts[c].split(" + "));
    var best = null;
    cuts.forEach(function (raw) {
      var forms = [raw, raw.replace(/, direct heal only$/, "")];
      forms.push(forms[1].replace(/ \(Rank \d+\)$/, ""));
      forms.push(forms[2].replace(/ \([^)]*\)$/, ""));
      forms.push(forms[3].replace(/ \d+(\/\d+)?$/, ""));
      forms.forEach(function (f) { if (find(f, null, true) && (!best || f.length > best.length)) best = f; });
    });
    return best ? find(best, null, true) : null;
  }
  function tree(text) {
    var found = null;
    Object.keys(data.trees).forEach(function (k) { if (text.indexOf(k) >= 0 && (!found || k.length > found.length)) found = k; });
    return found ? data.trees[found] : null;
  }

  // ---------- written pages ----------
  var SECTION = [   // first match wins: path prefix -> glyph, tint
    ["professions/alchemy", "potion", "nature"], ["professions/blacksmithing", "anvil", "physical"], ["professions/cooking", "food", "fire"],
    ["professions/enchanting", "crystal", "arcane"], ["professions/engineering", "cog", "physical"], ["professions/first-aid", "heal", "fire"],
    ["professions/fishing", "hook", "frost"], ["professions/herbalism", "herb", "nature"], ["professions/leatherworking", "hide", "physical"],
    ["professions/mining", "pick", "physical"], ["professions/skinning", "knife", "physical"], ["professions/tailoring", "needle", "arcane"],
    ["professions", "anvil", "physical"], ["content/dungeons", "dungeon", "physical"], ["content/raids", "raid", "fire"], ["content/pvp", "pvp", "fire"],
    ["content", "dungeon", "physical"], ["world", "compass", "nature"], ["systems/camping", "tent", "nature"], ["systems/economy", "coin", "holy"],
    ["systems", "cog", "physical"], ["characters/professions", "anvil", "physical"], ["characters", "person", "arcane"],
    ["guides/dps-calculator", "nuke", "fire"], ["guides/healing-calculator", "heal", "holy"], ["guides", "person", "arcane"],
    ["about-this-wiki", "people", "frost"], ["about", "info", "frost"], ["community", "people", "frost"], ["sources", "intellect", "arcane"], ["tags", "intellect", "arcane"]
  ];
  function pagePath() {
    var base = new URL("..", SCRIPT_SRC || location.href).pathname;          // site root, from the script's own URL
    return location.pathname.indexOf(base) === 0 ? location.pathname.slice(base.length) : location.pathname.replace(/^\//, "");
  }
  // A whole name only: "Flash Heal", "Flash Heal (Rank 7)" or "Deep Wounds 3", never a sentence that starts with one.
  function exact(text, cls) {
    var t = text.replace(/\s+/g, " ").replace(/[¶#]$/, "").trim();
    if (!t || t.length > 48) return null;
    var forms = [t, t.replace(/ \((Rank|makes) \d+\)$/, ""), t.replace(/ \d+(\/\d+)?$/, "")];
    for (var i = 0; i < forms.length; i++) { var hit = find(forms[i], cls); if (hit) return hit; }
    return null;
  }
  // Bold text that starts its block is a label ("**Fear Ward** is baseline"); bold text later in a sentence is prose.
  function leads(el) {
    for (var n = el.previousSibling; n; n = n.previousSibling) {
      if (n.nodeType === 3 ? n.nodeValue.trim() : !/^(BR|SVG|svg)$/.test(n.nodeName)) return false;
    }
    return true;
  }
  function ownText(el) {      // the element's name: its text without a trailing pill, note or permalink
    var out = "";
    for (var n = el.firstChild; n; n = n.nextSibling) {
      if (n.nodeType === 3) out += n.nodeValue;
      else if (n.nodeType === 1 && /^(A|EM|B|STRONG|SPAN)$/.test(n.tagName) && !/pill|headerlink|fc-sr|fc-rank|gi/.test(n.getAttribute("class") || "")) out += n.textContent;
      else if (out.trim()) break;
    }
    return out;
  }
  function decoratePage() {
    if (!data) return;
    sprite();
    var content = document.querySelector(".md-content .md-typeset");
    if (!content || content.dataset.giPage) return;
    content.dataset.giPage = "1";
    var h1 = content.querySelector("h1");
    var after = h1 && h1.nextElementSibling;
    while (after && after.tagName === "HR") after = after.nextElementSibling;
    var ownSigil = after && after.matches(".fc-meta") && after.querySelector(".fc-sigil");
    if (h1 && !h1.querySelector(".gi") && !ownSigil && !content.querySelector(".fc-hero")) {
      var path = pagePath();
      for (var i = 0; i < SECTION.length; i++) {
        if (path === SECTION[i][0] || path.indexOf(SECTION[i][0] + "/") === 0) { prefix(h1, SECTION[i][1], SECTION[i][2]).classList.add("gi--emblem"); break; }
      }
    }
    var sel = "strong, .tt-name, td, th, h2, h3, h4, .fc-chip, dt, li > a:only-child";
    var cm = pagePath().match(/^guides\/([a-z]+)\//), cls = cm && data.classes && data.classes[cm[1]] ? cm[1] : null;
    Array.prototype.forEach.call(content.querySelectorAll(sel), function (el) {
      // not in calculators (they redraw), code, page meta, pills (they carry their own marker) or cards that already have an icon
      if (el.dataset.gi || el.closest(".dps-calc, pre, code, .fc-pagemeta, .gi-off, .md-nav, .pill, .fc-class-card")) return;
      el.dataset.gi = "1";
      if (el.querySelector(".gi, svg, img")) return;
      if (el.parentElement && el.parentElement.querySelector(":scope > .twemoji, :scope > svg")) return;      // it already has an icon beside it
      if (/^(TD|TH|LI|DT)$/.test(el.tagName) && el.querySelector("strong:not(.pill), .tt-name")) return;      // the inner name gets it
      if (el.tagName === "STRONG" && (el.closest("h1, h2, h3, h4, .tt-name, .fc-chip") || !leads(el))) return;
      if (el.tagName === "A" && !leads(el)) return;
      var own = ownText(el), hit = exact(own, cls);
      if (hit) { prefix(el, hit[0], hit[1]); return; }
      // "Seal of Fury, Righteous Fury": a plain list of names gets one glyph per name
      if (!el.children.length && own.indexOf(", ") > 0) {
        var parts = own.split(", ").map(function (p) { return p.trim(); }), hits = parts.map(function (p) { return exact(p, cls); });
        if (hits.every(Boolean)) {
          el.textContent = "";
          parts.forEach(function (p, i) {
            var keep = document.createElement("span"), cut = p.indexOf(" ") < 0 ? p.length : p.indexOf(" ");
            keep.className = "gi-keep";
            keep.appendChild(icon(hits[i][0], hits[i][1]));
            keep.appendChild(document.createTextNode(p.slice(0, cut)));
            el.appendChild(keep);
            el.appendChild(document.createTextNode(p.slice(cut) + (i < parts.length - 1 ? ", " : "")));
          });
        }
      }
    });
    Array.prototype.forEach.call(content.querySelectorAll("table"), function (table) {
      if (table.closest(".dps-calc") || !table.tBodies[0]) return;
      var rows = table.tBodies[0].rows, cols = rows.length ? rows[0].cells.length : 0;
      for (var c = 0; c < cols; c++) {
        var got = [], cells = 0;
        for (var r = 0; r < rows.length; r++) {
          var cell = rows[r].cells[c];
          if (!cell || !cell.textContent.trim() || cell.colSpan > 1) continue;
          cells++;
          var g = cell.querySelector(".gi");
          if (g) got.push(g);
        }
        if (cells < 3 || !got.length) continue;
        var kinds = {};
        got.forEach(function (g) { kinds[g.firstChild.getAttribute("href")] = 1; });
        // a few icons scattered down a column, or the same icon on every row, tell the reader nothing
        if (got.length < cells * 0.6 || (Object.keys(kinds).length === 1 && got.length >= 3)) {
          got.forEach(function (g) {
            var keep = g.parentNode;
            g.remove();
            if (keep.classList && keep.classList.contains("gi-keep")) keep.replaceWith.apply(keep, Array.prototype.slice.call(keep.childNodes));
          });
        }
      }
    });
    Array.prototype.forEach.call(content.querySelectorAll(".pill"), function (el) {
      if (el.dataset.gi || el.closest(".dps-calc")) return;
      el.dataset.gi = "1";
      var m = (el.className || "").match(/pill--([a-z]+)/);
      if (m && data.sigils[m[1]] && !el.querySelector("svg")) el.insertBefore(icon("class-" + m[1], "class"), el.firstChild);
    });
  }

  function decorate(root) {
    if (!data) return;
    sprite();
    Array.prototype.forEach.call(root.querySelectorAll(TARGETS), function (el) {
      if (el.dataset.gi) return;
      el.dataset.gi = "1";
      if (el.querySelector(".gi") || (el.tagName === "TD" && el.querySelector("button, .pill"))) return;
      if (el.tagName === "LI" && el.querySelector("strong") && el.closest(".heal-hero-cols")) return;
      var text = el.textContent || "";
      // build and spec names: the talent tree they are named after, else the spell or talent in the name
      var hit = el.matches(".dps-spec-btn, summary, h5") ? (tree(text) || lookup(text.split(/ \/ | \(/)[0]) || lookup(text)) : lookup(text);
      if (!hit) return;
      prefix(el, hit[0], hit[1]);
    });
    // class pills get the site's own class sigil
    Array.prototype.forEach.call(root.querySelectorAll(".pill"), function (el) {
      if (el.dataset.gi) return;
      el.dataset.gi = "1";
      var m = (el.className || "").match(/pill--([a-z]+)/);
      if (!m || !data.sigils[m[1]]) return;
      var svg = icon("class-" + m[1], "class");
      el.insertBefore(svg, el.firstChild);
    });
  }

  var watched = new WeakSet();
  function onPage() {
    function get(file) {
      return fetch(new URL("../assets/data/" + file, SCRIPT_SRC || location.href).href)
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); });
    }
    if (!loading) {
      loading = get("icons.json").then(function (d) { data = d; })
        .catch(function () { data = null; });       // no icons is fine: the names are all still there
    }
    // item and recipe names are a larger file: only fetched where items are listed
    var wantItems = /professions|equipment|calculator|economy|items/.test(location.pathname);
    var ready = !wantItems || itemsLoaded ? loading : loading.then(function () {
      return get("icons-items.json").then(function (d) {
        itemsLoaded = true;
        if (data) data.items = d.names;
      }).catch(function () {});
    });
    ready.then(function () {
      decoratePage();
      Array.prototype.forEach.call(document.querySelectorAll(".dps-calc"), function (root) {
        if (!watched.has(root)) {
          watched.add(root);
          var pending = false;
          new MutationObserver(function () {
            if (pending) return;
            pending = true;
            setTimeout(function () { pending = false; decorate(root); }, 0);
          }).observe(root, { childList: true, subtree: true });
        }
        decorate(root);
      });
    });
  }
  if (window.document$ && typeof window.document$.subscribe === "function") window.document$.subscribe(onPage);
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", onPage);
  else onPage();
})();
