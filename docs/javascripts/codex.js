/* Forever Codex: small progressive enhancements (vanilla, no dependencies).
   Global listeners are bound once; per-page work runs on every page view,
   including navigation.instant swaps, via document$.subscribe.
   Everything here is optional: without JS the pages are complete. */
(function () {
  "use strict";

  /* ---------- helpers ---------- */
  var store = (function () {
    try { var k = "fc:probe"; localStorage.setItem(k, k); localStorage.removeItem(k); return localStorage; }
    catch (e) { return null; }
  })();
  function load(key, fallback) {
    if (!store) return fallback;
    try { var v = store.getItem(key); return v == null ? fallback : JSON.parse(v); } catch (e) { return fallback; }
  }
  function save(key, value) {
    if (!store) return;
    try { if (value == null) store.removeItem(key); else store.setItem(key, JSON.stringify(value)); } catch (e) { /* quota or privacy mode */ }
  }
  function h(tag, attrs, kids) {
    var n = document.createElement(tag);
    for (var a in attrs || {}) {
      if (a === "text") n.textContent = attrs[a];
      else if (a === "class") n.className = attrs[a];
      else if (attrs[a] !== false && attrs[a] != null) n.setAttribute(a, attrs[a] === true ? "" : attrs[a]);
    }
    (kids || []).forEach(function (k) { if (k) n.appendChild(typeof k === "string" ? document.createTextNode(k) : k); });
    return n;
  }
  /* Heading text without the ¶ permalink or anything we injected */
  function textOf(node) {
    var c = node.cloneNode(true);
    c.querySelectorAll(".headerlink, .fc-inject").forEach(function (x) { x.remove(); });
    return c.textContent.replace(/\s+/g, " ").trim();
  }
  function slug(s) { return s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 48); }
  function isTyping(e) {
    var t = e.target;
    return !!t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName));
  }
  function content() { return document.querySelector(".md-content__inner"); }

  /* Short messages: Material's own snackbar (alert$) if present, else a polite live region */
  var live;
  function announce(msg) {
    if (window.alert$ && typeof window.alert$.next === "function") { window.alert$.next(msg); return; }
    if (!live) { live = h("div", { class: "fc-sr-only", role: "status", "aria-live": "polite" }); document.body.appendChild(live); }
    live.textContent = ""; setTimeout(function () { live.textContent = msg; }, 50);
  }

  var narrow = window.matchMedia("(max-width: 59.984375em)"); /* below this Material moves the TOC into the drawer */
  var phone = window.matchMedia("(max-width: 44.984375em)");
  var canPopover = typeof HTMLElement !== "undefined" && HTMLElement.prototype.hasOwnProperty("popover");

  /* ---------- keyboard shortcuts ---------- */
  /* WCAG 2.1.4: single-character shortcuts can be switched off (setting in the ? dialog).
     When off, a window capture listener swallows them before Material's handler sees them. */
  var keysOn = load("fc:keys", true) !== false;
  var SINGLE = "fs/pn,.?t";

  window.addEventListener("keydown", function (e) {
    if (keysOn || e.ctrlKey || e.metaKey || e.altKey || isTyping(e)) return;
    if (e.key && e.key.length === 1 && SINGLE.indexOf(e.key) > -1) e.stopImmediatePropagation();
  }, true);

  function openSearch() {
    var toggle = document.querySelector('[data-md-toggle="search"]');
    if (!toggle) return false;
    toggle.checked = true;
    toggle.dispatchEvent(new Event("change"));
    var input = document.querySelector(".md-search__input");
    if (input) setTimeout(function () { input.focus(); }, 0);
    return true;
  }

  /* WCAG 1.4.13: Esc hides an open glossary tooltip without moving focus or the pointer */
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    document.querySelectorAll(".md-tooltip2").forEach(function (t) { t.classList.add("fc-tip-off"); });
  });
  ["focusin", "mouseover"].forEach(function (type) {
    document.addEventListener(type, function (e) {
      if (e.target.closest && e.target.closest("abbr")) return;
      document.querySelectorAll(".md-tooltip2.fc-tip-off").forEach(function (t) { t.classList.remove("fc-tip-off"); });
    }, { passive: true });
  });

  document.addEventListener("keydown", function (e) {
    /* Ctrl/Cmd+K opens search, matching the docs-site convention */
    if ((e.ctrlKey || e.metaKey) && !e.altKey && e.key && e.key.toLowerCase() === "k") {
      if (openSearch()) e.preventDefault();
      return;
    }
    if (!keysOn || e.ctrlKey || e.metaKey || e.altKey || isTyping(e) || e.defaultPrevented) return;
    if (document.querySelector('[data-md-toggle="search"]:checked')) return;
    if (e.key === "?") { e.preventDefault(); openKeys(); }
    else if (e.key === "t") { if (openContents()) e.preventDefault(); }
  });

  var keysDialog;
  function row(keys, what) {
    var dt = h("dt");
    keys.forEach(function (k, i) {
      if (i) dt.appendChild(document.createTextNode(" or "));
      k.split("+").forEach(function (part, j) {
        if (j) dt.appendChild(document.createTextNode("+"));
        dt.appendChild(h("kbd", { text: part }));
      });
    });
    return [dt, h("dd", { text: what })];
  }
  function openKeys() {
    if (!keysDialog) {
      var mac = /Mac|iPhone|iPad/.test(navigator.platform || "");
      var mod = mac ? "⌘" : "Ctrl";
      var list = h("dl", { class: "fc-keys__list" });
      [
        [[mod + "+K", "/", "S", "F"], "Search the wiki"],
        [["↑", "↓"], "Move through search results"],
        [["Enter"], "Open the selected result"],
        [["N", "."], "Next page"],
        [["P", ","], "Previous page"],
        [["T"], "Jump to a section on this page"],
        [["?"], "Show this list"],
        [["Esc"], "Close search or this dialog"]
      ].forEach(function (r) { row(r[0], r[1]).forEach(function (n) { list.appendChild(n); }); });
      var toggle = h("input", { type: "checkbox", id: "fc-keys-toggle" });
      toggle.checked = keysOn;
      toggle.addEventListener("change", function () {
        keysOn = toggle.checked; save("fc:keys", keysOn ? null : false);
      });
      var close = h("button", { type: "button", class: "fc-keys__close md-button", text: "Close", autofocus: true });
      keysDialog = h("dialog", { class: "fc-keys md-typeset", "aria-labelledby": "fc-keys-title" }, [
        h("h2", { id: "fc-keys-title", text: "Keyboard shortcuts" }),
        list,
        h("p", { class: "fc-keys__setting" }, [toggle, " ", h("label", { for: "fc-keys-toggle", text: "Single-key shortcuts (letters, / and ?)" })]),
        h("p", { class: "fc-keys__note", text: mod + "+K always works. Turn single keys off if they clash with your screen reader or voice control." }),
        close
      ]);
      close.addEventListener("click", function () { keysDialog.close(); });
      keysDialog.addEventListener("click", function (e) { if (e.target === keysDialog) keysDialog.close(); }); /* backdrop */
      document.body.appendChild(keysDialog);
    }
    if (typeof keysDialog.showModal === "function" && !keysDialog.open) keysDialog.showModal();
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(".fc-keys-open");
    if (b) { e.preventDefault(); openKeys(); }
  });

  /* ---------- "On this page" jump menu (phones and tablets) ---------- */
  var otp; /* { wrap, button, current, panel, list, items:[{h, a}] } */
  function buildContents(root) {
    if (!canPopover) return;
    if (!otp) {
      var panel = h("div", { id: "fc-otp-panel", class: "fc-otp__panel md-typeset", popover: "auto", "aria-label": "On this page" });
      var current = h("span", { class: "fc-otp__current" });
      var button = h("button", { type: "button", class: "fc-otp__button", popovertarget: "fc-otp-panel", "aria-haspopup": "true" }, [
        h("span", { class: "fc-otp__label", text: "On this page" }), current
      ]);
      var list = h("ol", { class: "fc-otp__list" });
      panel.appendChild(h("p", { class: "fc-otp__title", "aria-hidden": "true", text: "On this page" }));
      panel.appendChild(list);
      var wrap = h("div", { class: "fc-otp", hidden: true }, [button, panel]);
      document.body.appendChild(wrap);
      var returnTo = null;
      panel.addEventListener("beforetoggle", function (e) {
        if (e.newState === "open") returnTo = panel.contains(document.activeElement) ? null : document.activeElement;
        else if (panel.contains(document.activeElement) && returnTo === document.body) setTimeout(function () { button.focus(); }, 0);
      });
      panel.addEventListener("toggle", function (e) {
        button.setAttribute("aria-expanded", e.newState === "open" ? "true" : "false");
        if (e.newState === "open") {
          var a = list.querySelector('[aria-current="location"]') || list.querySelector("a");
          if (a) { a.focus(); a.scrollIntoView({ block: "nearest" }); }
        }
      });
      panel.addEventListener("click", function (e) {
        if (e.target.closest("a")) panel.hidePopover();
      });
      otp = { wrap: wrap, button: button, current: current, panel: panel, list: list, items: [] };
      window.addEventListener("scroll", onScroll, { passive: true });
    }
    otp.list.textContent = "";
    otp.items = [];
    var heads = root ? root.querySelectorAll("h2[id], h3[id]") : [];
    var h2s = 0;
    heads.forEach(function (hd) {
      if (hd.closest("details, .md-dialog, .fc-otp, .tabbed-block:not(:first-of-type)")) return;
      if (hd.tagName === "H2") h2s++;
      var a = h("a", { href: "#" + hd.id, text: textOf(hd) });
      var li = h("li", { class: hd.tagName === "H3" ? "fc-otp__sub" : null }, [a]);
      otp.list.appendChild(li);
      otp.items.push({ h: hd, a: a });
    });
    otp.h2s = root && root.querySelector(".fc-hero") ? 0 : h2s; /* the home page is a hub, not a long read */
    placeContents();
    try { otp.panel.hidePopover(); } catch (e) { /* not open */ }
    onScroll();
  }
  var ticking = false;
  function onScroll() {
    if (ticking || !otp || otp.wrap.hidden) return;
    ticking = true;
    requestAnimationFrame(function () {
      ticking = false;
      var active = null, limit = Math.max(110, window.innerHeight * .3);
      for (var i = 0; i < otp.items.length; i++) {
        if (otp.items[i].h.getBoundingClientRect().top < limit) active = otp.items[i]; else break;
      }
      otp.items.forEach(function (it) {
        if (it === active) it.a.setAttribute("aria-current", "location"); else it.a.removeAttribute("aria-current");
      });
      otp.current.textContent = active ? textOf(active.h) : "";
    });
  }
  /* Shown when the page has 3+ sections and no visible TOC sidebar: phones, and "hide: toc" pages */
  function placeContents() {
    if (!otp) return;
    var side = document.querySelector(".md-sidebar--secondary");
    var tocShown = !narrow.matches && side && !side.hidden && getComputedStyle(side).display !== "none";
    otp.wrap.hidden = otp.h2s < 3 || !!tocShown;
  }
  narrow.addEventListener && narrow.addEventListener("change", function () { placeContents(); onScroll(); });
  /* "t": open the jump menu on small screens, or focus the active TOC link on desktop */
  function openContents() {
    if (otp && !otp.wrap.hidden) { otp.panel.showPopover(); return true; }
    var a = document.querySelector(".md-sidebar--secondary .md-nav__link--active") ||
            document.querySelector(".md-sidebar--secondary .md-nav__link");
    if (a && a.offsetParent) { a.focus(); return true; }
    return false;
  }

  /* ---------- copy link to section + arrival highlight ---------- */
  function flash(id) {
    var t = id && document.getElementById(decodeURIComponent(id));
    if (!t || !/^H[1-6]$/.test(t.tagName)) return;
    t.classList.remove("fc-flash");
    void t.offsetWidth; /* restart the animation */
    t.classList.add("fc-flash");
    setTimeout(function () { t.classList.remove("fc-flash"); }, 1600);
  }
  document.addEventListener("click", function (e) {
    /* navigation.instant rewrites hrefs to absolute URLs, so compare paths rather than "#..." */
    var a = e.target.closest && e.target.closest("a[href*='#']");
    if (!a || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey) return;
    if (a.pathname !== location.pathname || a.origin !== location.origin || a.hash.length < 2) return;
    var id = a.hash.slice(1);
    if (a.classList.contains("headerlink") && navigator.clipboard && window.isSecureContext) {
      var url = location.origin + location.pathname + a.hash;
      navigator.clipboard.writeText(url).then(function () { announce("Link to section copied"); }, function () {});
    }
    setTimeout(function () { flash(id); }, 30);
  }, true); /* capture: runs before navigation.instant handles the click */
  window.addEventListener("hashchange", function () { flash(location.hash.slice(1)); });

  function labelPermalinks(root) {
    root.querySelectorAll(".headerlink").forEach(function (a) {
      var hd = a.parentElement;
      if (!hd || a.hasAttribute("aria-label")) return;
      a.setAttribute("aria-label", "Copy link to section: " + textOf(hd));
      a.setAttribute("title", "Copy link to this section");
    });
  }

  /* ---------- progress: tick off leveling steps (saved per page in localStorage) ---------- */
  var ROUTE_TABLE = /^(levels?)$/i, ROUTE_COL = /^(zones?|zone\(s\)|where)\b/i;
  function initProgress(root) {
    var key = "fc:done:" + location.pathname;
    var state = load(key, {});
    var tracked = [];
    function track(id, el, setDone) {
      tracked.push({ id: id, el: el, set: setDone });
      setDone(!!state[id]);
    }
    function commit(id, on) {
      if (on) state[id] = 1; else delete state[id];
      save(key, Object.keys(state).length ? state : null);
      updateBar();
    }

    /* 1. Markdown task lists: "- [ ] Train Defensive Stance" */
    root.querySelectorAll(".task-list-item > .task-list-control > input[type=checkbox]").forEach(function (box) {
      var li = box.closest(".task-list-item");
      var label = textOf(li);
      var id = "t:" + slug(label);
      if (box.checked && !(id in state)) state[id] = 1; /* author-ticked [x] */
      box.disabled = false;
      box.setAttribute("aria-label", label);
      track(id, li, function (on) { box.checked = on; li.classList.toggle("fc-is-done", on); });
      box.addEventListener("change", function () { li.classList.toggle("fc-is-done", box.checked); commit(id, box.checked); });
    });

    /* 2. Route tables: first column "Level(s)", second "Zone(s)"/"Where" */
    root.querySelectorAll("table").forEach(function (table) {
      var ths = table.querySelectorAll("thead th");
      if (ths.length < 2 || !ROUTE_TABLE.test(textOf(ths[0])) || !ROUTE_COL.test(textOf(ths[1]))) return;
      if (table.classList.contains("fc-route")) return;
      table.classList.add("fc-route");
      ths[0].parentElement.insertBefore(h("th", { class: "fc-inject fc-route__check" }, [h("span", { class: "fc-sr-only", text: "Done" })]), ths[0]);
      table.querySelectorAll("tbody tr").forEach(function (tr) {
        var cells = tr.children;
        if (!cells.length) return;
        var label = textOf(cells[0]) + ", " + (cells[1] ? textOf(cells[1]) : "");
        var id = "r:" + slug(label);
        var box = h("input", { type: "checkbox", "aria-label": "Done: level " + label });
        tr.insertBefore(h("td", { class: "fc-inject fc-route__check" }, [box]), cells[0]);
        track(id, tr, function (on) { box.checked = on; tr.classList.toggle("fc-is-done", on); });
        box.addEventListener("change", function () { tr.classList.toggle("fc-is-done", box.checked); commit(id, box.checked); });
      });
    });

    /* 3. Leveling brackets: every H3 under the "Leveling walkthrough" H2, and .steps list items */
    var lev = root.querySelector("h2[id^='leveling']");
    var brackets = [];
    for (var n = lev && lev.nextElementSibling; n && n.tagName !== "H2"; n = n.nextElementSibling) {
      if (n.tagName === "H3" && n.id) brackets.push(n);
    }
    root.querySelectorAll(".route > h3[id]").forEach(function (hd) { if (brackets.indexOf(hd) < 0) brackets.push(hd); });
    brackets.forEach(addSectionToggle);
    root.querySelectorAll(".steps > ol > li").forEach(function (li, i) {
      var label = textOf(li).slice(0, 80);
      var id = "s:" + i + ":" + slug(label);
      var btn = h("button", { type: "button", class: "fc-inject fc-done", "aria-pressed": "false" }, [
        h("span", { class: "fc-done__text", text: "Done" }), h("span", { class: "fc-sr-only", text: ": step " + (i + 1) })
      ]);
      li.appendChild(btn);
      wire(btn, id, li);
    });
    function addSectionToggle(hd) {
      var id = "h:" + hd.id;
      var btn = h("button", { type: "button", class: "fc-done", "aria-pressed": "false" }, [
        h("span", { class: "fc-done__text", text: "Done" }), h("span", { class: "fc-sr-only", text: ": " + textOf(hd) })
      ]);
      hd.insertAdjacentElement("afterend", h("p", { class: "fc-inject fc-done-row" }, [btn]));
      wire(btn, id, hd);
    }
    function wire(btn, id, el) {
      track(id, el, function (on) { btn.setAttribute("aria-pressed", on ? "true" : "false"); el.classList.toggle("fc-is-done", on); });
      btn.addEventListener("click", function () {
        var on = btn.getAttribute("aria-pressed") !== "true";
        btn.setAttribute("aria-pressed", on ? "true" : "false");
        el.classList.toggle("fc-is-done", on);
        commit(id, on);
      });
    }

    if (!tracked.length) return;
    /* A small summary + reset, placed before the first tracked item's block */
    var meter = h("progress", { max: String(tracked.length), value: "0", "aria-hidden": "true" });
    var count = h("span", { class: "fc-progress__count" });
    var reset = h("button", { type: "button", class: "fc-progress__reset", text: "Clear ticks" });
    var bar = h("div", { class: "fc-inject fc-progress" }, [
      h("span", { class: "fc-progress__label", text: "Your progress" }), meter, count, reset,
      h("span", { class: "fc-progress__hint", text: "Saved in this browser only" })
    ]);
    function updateBar() {
      var done = tracked.filter(function (t) { return state[t.id]; }).length;
      meter.value = done;
      count.textContent = done + " of " + tracked.length + " ticked";
      reset.hidden = !done;
    }
    reset.addEventListener("click", function () {
      if (!window.confirm("Clear all ticks on this page?")) return;
      state = {}; save(key, null);
      tracked.forEach(function (t) { t.set(false); });
      updateBar(); announce("Ticks cleared");
      count.tabIndex = -1; count.focus(); /* the reset button just hid itself */
    });
    var first = tracked.reduce(function (a, t) {
      return a.compareDocumentPosition(t.el) & Node.DOCUMENT_POSITION_PRECEDING ? t.el : a;
    }, tracked[0].el);
    var anchor = lev && root.contains(lev) && lev.compareDocumentPosition(first) & Node.DOCUMENT_POSITION_FOLLOWING ? lev : null;
    var block = anchor || first.closest("table, ul, ol, h3") || first;
    while (block.parentElement && block.parentElement !== root && !block.parentElement.classList.contains("tabbed-block")) block = block.parentElement;
    if (anchor) anchor.insertAdjacentElement("afterend", bar); else block.insertAdjacentElement("beforebegin", bar);
    updateBar();
  }

  /* ---------- guides hub: faction / role / race filter ---------- */
  var FACTION = {
    human: "alliance", dwarf: "alliance", gnome: "alliance", "night-elf": "alliance", "skyborne-high-order": "alliance",
    orc: "horde", troll: "horde", tauren: "horde", undead: "horde", "skyborne-windshaper": "horde"
  };
  var RACES = [["human", "Human"], ["dwarf", "Dwarf"], ["gnome", "Gnome"], ["night-elf", "Night Elf"], ["skyborne-high-order", "Skyborne (High Order)"],
    ["orc", "Orc"], ["troll", "Troll"], ["tauren", "Tauren"], ["undead", "Undead"], ["skyborne-windshaper", "Skyborne (Windshaper)"]];
  function combo(a) {
    var m = a.pathname.match(/\/guides\/([a-z-]+)\/([a-z-]+)\/?$/);
    return m ? { cls: m[1], race: m[2] } : null;
  }
  function initFilter(root) {
    var grid = root.querySelector(".fc-class-card");
    if (!grid || grid.previousElementSibling && grid.previousElementSibling.classList.contains("fc-filter")) return;
    var cards = Array.prototype.slice.call(grid.querySelectorAll(":scope > ul > li"));
    var roles = {}; /* class slug -> {tank, heal, dps} */
    cards.forEach(function (li) {
      var link = li.querySelector("a[href]");
      var m = link && link.pathname.match(/\/guides\/([a-z-]+)\/?$/);
      if (!m) return;
      li.dataset.cls = m[1];
      var r = li.dataset.roles || ""; /* authors may set data-roles="tank heal dps" */
      if (!r) {
        var strong = Array.prototype.find.call(li.querySelectorAll("strong"), function (s) { return !s.querySelector("a"); });
        var t = strong ? strong.textContent : "";
        r = [/\bTank/i.test(t) && "tank", /\bHeal/i.test(t) && "heal", /\bDPS\b/.test(t) && "dps"].filter(Boolean).join(" ");
      }
      roles[m[1]] = r;
    });
    if (!Object.keys(roles).length) return;

    function radio(name, value, label, checked) {
      var id = "fc-f-" + name + "-" + value;
      return h("span", { class: "fc-filter__opt" }, [
        h("input", { type: "radio", name: "fc-" + name, id: id, value: value, checked: checked }),
        h("label", { for: id, text: label })
      ]);
    }
    function check(value, label) {
      var id = "fc-f-role-" + value;
      return h("span", { class: "fc-filter__opt" }, [
        h("input", { type: "checkbox", name: "fc-role", id: id, value: value }), h("label", { for: id, text: label })
      ]);
    }
    var select = h("select", { id: "fc-f-race", name: "fc-race" }, [h("option", { value: "", text: "Any race" })].concat(
      RACES.map(function (r) { return h("option", { value: r[0], text: r[1] }); })));
    var status = h("p", { class: "fc-filter__status", role: "status" });
    var reset = h("button", { type: "button", class: "fc-filter__reset", text: "Show all" });
    var form = h("form", { class: "fc-inject fc-filter", "aria-label": "Filter guides" }, [
      h("fieldset", {}, [h("legend", { text: "Faction" }), radio("faction", "", "Both", true), radio("faction", "alliance", "Alliance"), radio("faction", "horde", "Horde")]),
      h("fieldset", {}, [h("legend", { text: "Role" }), check("tank", "Tank"), check("heal", "Healer"), check("dps", "DPS")]),
      h("p", { class: "fc-filter__race" }, [h("label", { for: "fc-f-race", text: "Race" }), select]),
      h("div", { class: "fc-filter__foot" }, [status, reset])
    ]);
    form.addEventListener("submit", function (e) { e.preventDefault(); });
    grid.insertAdjacentElement("beforebegin", form);

    /* Other blocks on the hub that follow the same filter */
    var raceItems = [];
    var browse = root.querySelector("h2[id^='browse-by-race']");
    for (var n = browse && browse.nextElementSibling; n && n.tagName !== "H2"; n = n.nextElementSibling) {
      if (n.tagName === "UL") n.querySelectorAll(":scope > li").forEach(function (li) { raceItems.push({ li: li, list: n }); });
    }
    var matrix = root.querySelector(".fc-matrix table");

    function read() {
      var f = form.querySelector("input[name=fc-faction]:checked");
      return {
        faction: f ? f.value : "",
        roles: Array.prototype.map.call(form.querySelectorAll("input[name=fc-role]:checked"), function (c) { return c.value; }),
        race: select.value
      };
    }
    function roleOk(cls, s) {
      return !s.roles.length || s.roles.some(function (r) { return (" " + roles[cls] + " ").indexOf(" " + r + " ") > -1; });
    }
    function raceOk(race, s) {
      return (!s.faction || FACTION[race] === s.faction) && (!s.race || race === s.race);
    }
    function apply(fromUser) {
      var s = read(), classes = 0, guides = 0;
      var active = !!(s.faction || s.roles.length || s.race);
      root.classList.toggle("fc-filtering", active);
      cards.forEach(function (li) {
        var cls = li.dataset.cls; if (!cls) return;
        var shown = 0;
        li.querySelectorAll("a.fc-chip").forEach(function (a) {
          var c = combo(a); if (!c) return;
          var ok = raceOk(c.race, s); a.hidden = !ok; if (ok) shown++;
        });
        var vis = roleOk(cls, s) && shown > 0;
        li.hidden = !vis;
        if (vis) { classes++; guides += shown; }
      });
      var lists = new Map();
      raceItems.forEach(function (it) {
        var any = 0, race = null;
        it.li.querySelectorAll("a.fc-chip").forEach(function (a) {
          var c = combo(a); if (!c) return; race = c.race;
          var ok = roleOk(c.cls, s); a.hidden = !ok; if (ok) any++;
        });
        var vis = !race || (raceOk(race, s) && any > 0);
        it.li.hidden = !vis;
        lists.set(it.list, (lists.get(it.list) || 0) + (vis ? 1 : 0));
      });
      lists.forEach(function (count, list) {
        list.hidden = !count;
        var prev = list.previousElementSibling;
        if (prev && prev.tagName === "H3") prev.hidden = !count;
      });
      if (matrix) {
        matrix.querySelectorAll("tbody tr").forEach(function (tr) {
          var a = tr.querySelector("a[href]"), c = a && combo(a);
          var lead = tr.querySelector(".fc-alliance, .fc-horde");
          if (c) tr.hidden = !raceOk(c.race, s);
          else if (lead) tr.hidden = !!s.race || (!!s.faction && !lead.classList.contains("fc-" + s.faction));
          tr.querySelectorAll("td a[href]").forEach(function (link) {
            var cc = combo(link); if (cc) link.closest("td").classList.toggle("fc-dim", !roleOk(cc.cls, s));
          });
        });
      }
      status.textContent = !active ? "Showing all 9 classes and " + guides + " race guides." :
        classes ? "Showing " + classes + (classes === 1 ? " class" : " classes") + " and " + guides + (guides === 1 ? " race guide." : " race guides.") :
        "No guide matches that combination.";
      reset.hidden = !active;
      if (fromUser) {
        var q = new URLSearchParams(location.search);
        ["faction", "role", "race"].forEach(function (k) { q.delete(k); });
        if (s.faction) q.set("faction", s.faction);
        if (s.roles.length) q.set("role", s.roles.join(","));
        if (s.race) q.set("race", s.race);
        var qs = q.toString();
        history.replaceState(history.state, "", location.pathname + (qs ? "?" + qs : "") + location.hash);
      }
    }
    /* Restore from the URL so a filtered view can be shared */
    var q = new URLSearchParams(location.search);
    var f0 = q.get("faction");
    if (f0 === "alliance" || f0 === "horde") form.querySelector("#fc-f-faction-" + f0).checked = true;
    (q.get("role") || "").split(",").forEach(function (r) { var c = form.querySelector("#fc-f-role-" + r); if (c) c.checked = true; });
    if (FACTION[q.get("race")]) select.value = q.get("race");
    /* Choosing a race that contradicts the faction resets the faction */
    select.addEventListener("change", function () {
      var fac = FACTION[select.value];
      var cur = form.querySelector("input[name=fc-faction]:checked");
      if (fac && cur && cur.value && cur.value !== fac) form.querySelector("#fc-f-faction-" + fac).checked = true;
    });
    form.addEventListener("change", function (e) {
      if (e.target.name === "fc-faction" && select.value && e.target.value && FACTION[select.value] !== e.target.value) select.value = "";
      apply(true);
    });
    reset.addEventListener("click", function () {
      form.reset(); apply(true); form.querySelector("input").focus();
    });
    apply(false);
  }

  /* ---------- combo switcher: collapsed on phones ---------- */
  function initSwitcher(root) {
    root.querySelectorAll("details.fc-switcher__box").forEach(function (d) {
      if (!d.dataset.fcInit) {
        d.dataset.fcInit = "1";
        d.open = !phone.matches;
      }
    });
  }
  phone.addEventListener && phone.addEventListener("change", function () {
    document.querySelectorAll("details.fc-switcher__box").forEach(function (d) { d.open = !phone.matches; });
  });

  /* ---------- class progressions: the add-on picker ---------- */
  /* The picker holds 3 radio groups (race, talents, gear). Each chapter of the page holds
     .fc-addon blocks with data-pick and data-value. window.fcPick (overrides/main.html) writes
     the CSS that shows the picked blocks. The picks are saved per class and are in the URL. */
  var PICKS = ["race", "talents", "gear"];
  function initPicker(root) {
    var P = window.fcPick;
    if (!P) return;
    var box = root.querySelector(".fc-pick");
    if (!box) { P.paint(null); return; }
    var cls = box.getAttribute("data-class"), key = "fc:pick:" + cls;
    var state = P.read(cls);
    var all = box.querySelector("input[name=fc-all]");
    PICKS.forEach(function (k) {
      var radios = Array.prototype.slice.call(box.querySelectorAll('input[name="fc-' + k + '"]'));
      var hit = radios.filter(function (r) { return r.value === state[k]; })[0] || radios[0];
      if (hit) { hit.checked = true; state[k] = hit.value; }
    });
    if (all) all.checked = !!state.all;
    P.paint(state);
    if (box.dataset.fcInit) return;
    box.dataset.fcInit = "1";
    box.addEventListener("change", function (e) {
      var t = e.target;
      if (!t || !t.name) return;
      if (t.name === "fc-all") state.all = t.checked || undefined;
      else state[t.name.slice(3)] = t.value;
      save(key, state);
      P.paint(state);
      try {
        var q = new URLSearchParams(location.search);
        PICKS.forEach(function (k) { if (state[k]) q.set(k, state[k]); });
        history.replaceState(history.state, "", location.pathname + "?" + q.toString() + location.hash);
      } catch (err) { /* file: URLs */ }
      var names = PICKS.map(function (k) {
        var r = box.querySelector('input[name="fc-' + k + '"]:checked');
        return r ? r.parentNode.textContent.trim() : "";
      }).filter(Boolean).join(", ");
      announce(state.all ? "All add-ons show" : "Add-ons: " + names);
    });
  }

  /* ---------- scrollable tables become labelled, focusable regions ---------- */
  function labelScrollers(root) {
    root.querySelectorAll(".md-typeset__scrollwrap").forEach(function (wrap) {
      if (wrap.scrollWidth > wrap.clientWidth + 1) {
        var heading = null, el = wrap;
        while (el && !heading) {
          var prev = el.previousElementSibling;
          while (prev && !/^H[2-4]$/.test(prev.tagName)) prev = prev.previousElementSibling;
          if (prev) heading = prev; else el = el.parentElement;
          if (el && el.classList && el.classList.contains("md-content__inner")) break;
        }
        var label = heading ? textOf(heading) : "Table";
        wrap.tabIndex = 0;
        wrap.setAttribute("role", "region");
        wrap.setAttribute("aria-label", label.slice(0, 60) + " (scrollable table)");
      } else {
        wrap.removeAttribute("tabindex");
        wrap.removeAttribute("role");
        wrap.removeAttribute("aria-label");
      }
    });
  }

  /* ---------- glossary abbreviations: reachable by keyboard and touch ---------- */
  /* The first use of each abbreviation per page becomes focusable, so content.tooltips
     shows its definition on focus; screen readers get it through aria-describedby/title. */
  function initAbbr(root) {
    var seen = {};
    root.querySelectorAll("abbr[title]").forEach(function (ab) {
      var t = ab.textContent;
      if (seen[t] || ab.closest("a, button, summary, h1, h2, h3, h4, .fc-chip, .badge, .tier, .lvl, .md-tag")) return;
      seen[t] = 1;
      ab.tabIndex = 0;
    });
  }

  /* ---------- per page ---------- */
  function onPage() {
    var root = content();
    if (!root) return;
    var steps = [labelPermalinks, initPicker, initProgress,initFilter, initSwitcher, initAbbr, buildContents, labelScrollers];
    steps.forEach(function (fn) {
      try { fn(root); } catch (err) { if (window.console) console.error("codex.js:", fn.name, err); }
    });
    document.querySelectorAll(".fc-keys-open[hidden]").forEach(function (b) { b.hidden = false; });
    if (location.hash) setTimeout(function () { flash(location.hash.slice(1)); }, 60);
  }

  if (window.document$ && typeof window.document$.subscribe === "function") window.document$.subscribe(onPage);
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", onPage);
  else onPage();
})();

/* Name Material's landmark widgets for assistive tech (QA audit) */
(function () {
  var prog = document.querySelector(".md-progress");
  if (prog && !prog.hasAttribute("aria-label")) prog.setAttribute("aria-label", "Page loading");
  var search = document.querySelector(".md-search");
  if (search && !search.hasAttribute("aria-label")) search.setAttribute("aria-label", "Search");
})();
