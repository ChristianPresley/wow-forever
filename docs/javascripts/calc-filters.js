/* Forever Codex calculator filters: one filter bar for every table in the DPS and healing calculators.
   A calculator keeps its own `state` object and its own draw(); it describes its controls and this
   builds them, writes the choices into `state`, and calls back.

     var ff = ForeverFilters.build(state, [
       { type: "chips",   key: "cls",  label: "Class", pills: true, options: [["priest", "Priest"], ...] },   // many of
       { type: "choice",  key: "gear", label: "Gear",  options: [["crafted", "Best craftable"], ["none", "None"]] }, // one of
       { type: "select",  key: "race", label: "Race",  options: [["all", "All races"], ...] },
       { type: "range",   key: "level", label: "Level", values: [1, 2, ... 60] },
       { type: "search",  key: "q",    label: "Search", placeholder: "Spec or race" },
       { type: "toggle",  key: "best", label: "Best race only" }
     ], draw, { label: "Filter the table" });
     box.appendChild(ff.el);   ...   ff.count(shown, total, "spec and race pairs");

   Every control is a native input (checkbox, radio, select, range, search), so keyboard and
   screen-reader behaviour is the browser's own. "chips" stores an array: empty means all.
   The bar shows how many rows match and has a Reset button that returns to the starting state. */
(function () {
  "use strict";
  var uid = 0;

  function el(tag, attrs, kids) {
    var n = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) { if (k === "text") n.textContent = attrs[k]; else n.setAttribute(k, attrs[k]); });
    (kids || []).forEach(function (c) { if (c) n.appendChild(typeof c === "string" ? document.createTextNode(c) : c); });
    return n;
  }
  function copy(v) { return Array.isArray(v) ? v.slice() : v; }
  function same(a, b) { return Array.isArray(a) ? Array.isArray(b) && a.length === b.length && a.every(function (v) { return b.indexOf(v) >= 0; }) : a === b; }

  // Does a value pass a "chips" (array, empty = all) or a single-choice ("all" = all) filter?
  function match(sel, value) {
    if (Array.isArray(sel)) return !sel.length || sel.indexOf(value) >= 0;
    return sel === "all" || sel == null || sel === value;
  }
  // Does every word of the search text appear in one of the parts?
  function text(q, parts) {
    q = (q || "").trim().toLowerCase();
    if (!q) return true;
    var hay = parts.filter(Boolean).join(" ").toLowerCase();
    return q.split(/\s+/).every(function (w) { return hay.indexOf(w) >= 0; });
  }

  function build(state, controls, onChange, opts) {
    opts = opts || {};
    var id = "ff" + (++uid), syncers = [], defaults = {};
    controls.forEach(function (c) { defaults[c.key] = copy(state[c.key]); });
    var root = el("div", { "class": "ff", role: "group", "aria-label": opts.label || "Filters" });
    var fields = el("div", { "class": "ff-fields" });
    var count = el("p", { "class": "ff-count", role: "status" });
    var reset = el("button", { type: "button", "class": "ff-reset", text: "Reset filters" });

    function dirty() { return controls.some(function (c) { return !same(state[c.key], defaults[c.key]); }); }
    function refresh() { reset.disabled = !dirty(); syncers.forEach(function (f) { f(); }); }
    function changed(c) { if (c && c.after) c.after(); refresh(); onChange(); }

    function field(c, body, group) {
      // a set of inputs is a fieldset with a legend; a single input is a label
      if (group) return el("fieldset", { "class": "ff-field ff-field--" + c.type }, [el("legend", { text: c.label }), body]);
      return el("div", { "class": "ff-field ff-field--" + c.type }, [body]);
    }

    controls.forEach(function (c, ci) {
      var name = id + "-" + ci;
      if (c.type === "chips") {
        var box = el("div", { "class": "ff-chips" });
        var all = el("button", { type: "button", "class": "ff-all", text: c.all || "All" });
        all.addEventListener("click", function () { state[c.key] = []; changed(c); });
        box.appendChild(all);
        var inputs = c.options.map(function (o) {
          var input = el("input", { type: "checkbox", "class": "fc-sr-only", value: o[0] });
          input.addEventListener("change", function () {
            var picked = inputs.filter(function (i) { return i.checked; }).map(function (i) { return i.value; });
            state[c.key] = picked.length === inputs.length ? [] : picked;      // everything ticked is the same as no filter
            changed(c);
          });
          box.appendChild(el("label", { "class": "ff-chip" }, [input, el("span", { "class": c.pills ? "pill pill--" + o[0] : "ff-chip-text", text: o[1] })]));
          return input;
        });
        syncers.push(function () {
          var sel = state[c.key] || [];
          inputs.forEach(function (i) { i.checked = sel.indexOf(i.value) >= 0; });
          all.setAttribute("aria-pressed", sel.length ? "false" : "true");
          box.classList.toggle("is-filtered", sel.length > 0);
        });
        fields.appendChild(field(c, box, true));
      } else if (c.type === "choice") {
        var seg = el("div", { "class": "ff-seg" });
        var radios = c.options.map(function (o) {
          var input = el("input", { type: "radio", "class": "fc-sr-only", name: name, value: o[0] });
          input.addEventListener("change", function () { if (input.checked) { state[c.key] = o[0]; changed(c); } });
          seg.appendChild(el("label", { "class": "ff-seg-opt" }, [input, el("span", { "class": c.pills && o[0] !== "all" ? "pill pill--" + o[0] : "ff-seg-text", text: o[1] })]));
          return input;
        });
        syncers.push(function () { radios.forEach(function (i) { i.checked = i.value === String(state[c.key]); }); });
        fields.appendChild(field(c, seg, true));
      } else if (c.type === "select") {
        var s = el("select", { id: name });
        c.options.forEach(function (o) { s.appendChild(el("option", { value: o[0], text: o[1] })); });
        s.addEventListener("change", function () { state[c.key] = s.value; changed(c); });
        syncers.push(function () { s.value = state[c.key]; });
        fields.appendChild(field(c, el("label", { "class": "ff-label", "for": name }, [el("span", { text: c.label }), s])));
      } else if (c.type === "search") {
        var q = el("input", { type: "search", id: name, placeholder: c.placeholder || "", autocomplete: "off", spellcheck: "false" });
        var timer = 0;
        q.addEventListener("input", function () {
          clearTimeout(timer);
          timer = setTimeout(function () { state[c.key] = q.value; changed(c); }, 120);
        });
        syncers.push(function () { if (document.activeElement !== q) q.value = state[c.key] || ""; });
        fields.appendChild(field(c, el("label", { "class": "ff-label", "for": name }, [el("span", { text: c.label }), q])));
      } else if (c.type === "range") {
        var vals = c.values, r = el("input", { type: "range", id: name, min: "0", max: String(vals.length - 1), step: "1" });
        var n = el("input", { type: "number", min: String(vals[0]), max: String(vals[vals.length - 1]), "aria-label": c.label + ", type a value" });
        var down = el("button", { type: "button", "class": "ff-step", "aria-label": c.label + " down", text: "−" });
        var up = el("button", { type: "button", "class": "ff-step", "aria-label": c.label + " up", text: "+" });
        function set(i) {
          i = Math.max(0, Math.min(vals.length - 1, i));
          if (state[c.key] !== vals[i]) { state[c.key] = vals[i]; changed(c); } else refresh();
        }
        function near(v) { var best = 0; vals.forEach(function (x, i) { if (Math.abs(x - v) < Math.abs(vals[best] - v)) best = i; }); return best; }
        r.addEventListener("input", function () { set(parseInt(r.value, 10)); });
        n.addEventListener("change", function () { var v = parseFloat(n.value); if (!isNaN(v)) set(near(v)); else refresh(); });
        down.addEventListener("click", function () { set(vals.indexOf(state[c.key]) - 1); });
        up.addEventListener("click", function () { set(vals.indexOf(state[c.key]) + 1); });
        syncers.push(function () {
          var i = vals.indexOf(state[c.key]);
          r.value = String(i);
          r.setAttribute("aria-valuetext", c.label + " " + state[c.key]);
          if (document.activeElement !== n) n.value = String(state[c.key]);
          down.disabled = i <= 0; up.disabled = i >= vals.length - 1;
        });
        fields.appendChild(field(c, el("div", { "class": "ff-range" }, [el("label", { "class": "ff-label-inline", "for": name, text: c.label }), down, r, up, n])));
      } else if (c.type === "toggle") {
        var t = el("input", { type: "checkbox", "class": "fc-sr-only", id: name });
        t.addEventListener("change", function () { state[c.key] = t.checked; changed(c); });
        syncers.push(function () { t.checked = !!state[c.key]; });
        fields.appendChild(field(c, el("label", { "class": "ff-switch", "for": name }, [t, el("span", { "class": "ff-track", "aria-hidden": "true" }), el("span", { text: c.label })])));
      }
    });

    reset.addEventListener("click", function () {
      controls.forEach(function (c) { state[c.key] = copy(defaults[c.key]); if (c.after) c.after(); });
      refresh();
      onChange();
    });
    root.appendChild(fields);
    root.appendChild(el("div", { "class": "ff-foot" }, [count, reset]));
    refresh();
    return {
      el: root,
      sync: refresh,
      count: function (shown, total, noun) {
        count.textContent = shown === total ? "Showing all " + total.toLocaleString("en-US") + " " + noun + "."
          : shown ? "Showing " + shown.toLocaleString("en-US") + " of " + total.toLocaleString("en-US") + " " + noun + "."
            : "No " + noun + " match these filters. Reset the filters to see all " + total.toLocaleString("en-US") + ".";
        count.classList.toggle("is-empty", !shown);
      }
    };
  }

  window.ForeverFilters = { build: build, match: match, text: text };
})();
