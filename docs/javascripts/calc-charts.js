/* Forever Codex calculator charts: a small SVG line and stacked-area chart with no dependencies.
   window.ForeverCharts.draw(container, options) draws one chart and returns { update(options) }.
     options.label    accessible name of the chart
     options.x        x values (levels), ascending
     options.xLabel   axis title; options.unit is added to values in the tooltip ("DPS")
     options.series   [{ name, values, slot, short }]   slot 0-5 picks the colour and never changes for an entity;
                      short is the label at the end of the line (the name when absent)
                      [{ name, values, context: true }]   a thin grey line with no legend entry
     options.stacked  true: series are stacked areas, and the tooltip adds a total
     options.marker   x value to mark with a vertical line (the level chosen in the filters)
     options.note     text under the legend
   Identity is never colour alone: a legend is always drawn for two or more series, up to four
   lines are labelled at their end, and every caller puts a table of the same numbers under the
   chart. The crosshair follows the pointer or the arrow keys and lists every series at that x. */
(function () {
  "use strict";
  var NS = "http://www.w3.org/2000/svg";
  function svg(tag, attrs, kids) {
    var e = document.createElementNS(NS, tag);
    Object.keys(attrs || {}).forEach(function (k) { if (k === "text") e.textContent = attrs[k]; else e.setAttribute(k, attrs[k]); });
    (kids || []).forEach(function (c) { if (c) e.appendChild(c); });
    return e;
  }
  function html(tag, attrs, kids) {
    var e = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) { if (k === "text") e.textContent = attrs[k]; else e.setAttribute(k, attrs[k]); });
    (kids || []).forEach(function (c) { if (c) e.appendChild(c); });
    return e;
  }
  function niceStep(max, count) {
    var raw = max / count, pow = Math.pow(10, Math.floor(Math.log10(raw))), f = raw / pow;
    return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10) * pow;
  }
  function fmt(v) { return v == null ? "–" : (Math.abs(v) >= 100 ? Math.round(v).toLocaleString("en-US") : v.toFixed(1)); }
  function clip(s, n) { return s.length > n ? s.slice(0, n - 1) + "…" : s; }

  function draw(container, opts) {
    var wrap = html("div", { "class": "fc-chart" });
    var legend = html("ul", { "class": "fc-chart-legend" });
    var note = html("p", { "class": "fc-chart-note" });
    var plot = html("div", { "class": "fc-chart-plot" });
    var tip = html("div", { "class": "fc-chart-tip", hidden: "" });
    wrap.appendChild(legend); wrap.appendChild(note); wrap.appendChild(plot); plot.appendChild(tip);
    container.replaceChildren(wrap);
    var active = null, geom = null;

    function render() {
      var x = opts.x, shown = opts.series.filter(function (s) { return !s.context; }), ctx = opts.series.filter(function (s) { return s.context; });
      var W = Math.max(280, plot.clientWidth || 720), H = opts.stacked ? 260 : 300;
      var endLabels = !opts.stacked && shown.length > 0 && shown.length <= 4 && W >= 560;
      var longest = 0;
      shown.forEach(function (s) { longest = Math.max(longest, (s.short || s.name).length); });
      var m = { l: 46, r: endLabels ? Math.min(230, 16 + 6.3 * Math.min(longest, 34)) : 14, t: 24, b: 36 };
      var pw = W - m.l - m.r, ph = H - m.t - m.b;
      // stack: cumulative tops per series
      var tops = shown.map(function (s) { return s.values.slice(); });
      if (opts.stacked) for (var i = 1; i < tops.length; i++) for (var j = 0; j < x.length; j++) tops[i][j] = (tops[i][j] || 0) + (tops[i - 1][j] || 0);
      var max = 0;
      tops.concat(ctx.map(function (s) { return s.values; })).forEach(function (vals) { vals.forEach(function (v) { if (v > max) max = v; }); });
      var step = niceStep(max || 1, 4), top = Math.ceil((max || 1) / step) * step;
      var sx = function (k) { return m.l + (x.length > 1 ? k / (x.length - 1) : 0.5) * pw; };
      var sy = function (v) { return m.t + ph - v / top * ph; };
      var path = function (vals) {
        var d = "", pen = false;
        vals.forEach(function (v, k) { if (v == null) { pen = false; return; } d += (pen ? "L" : "M") + sx(k).toFixed(1) + " " + sy(v).toFixed(1); pen = true; });
        return d;
      };
      var root = svg("svg", { viewBox: "0 0 " + W + " " + H, width: W, height: H, role: "img", tabindex: "0", "aria-label": opts.label + ". Use the left and right arrow keys to read values; the table below has every number." });
      // grid and y axis
      for (var g = 0; g <= top + 1e-9; g += step) {
        root.appendChild(svg("line", { "class": "fc-chart-grid", x1: m.l, x2: m.l + pw, y1: sy(g), y2: sy(g) }));
        root.appendChild(svg("text", { "class": "fc-chart-tick", x: m.l - 6, y: sy(g) + 3.5, "text-anchor": "end", text: Math.round(g).toLocaleString("en-US") }));
      }
      // x axis
      x.forEach(function (v, k) {
        if (!(k === 0 || v % 10 === 0)) return;
        root.appendChild(svg("line", { "class": "fc-chart-grid", x1: sx(k), x2: sx(k), y1: m.t + ph, y2: m.t + ph + 4 }));
        root.appendChild(svg("text", { "class": "fc-chart-tick", x: sx(k), y: m.t + ph + 16, "text-anchor": "middle", text: String(v) }));
      });
      root.appendChild(svg("text", { "class": "fc-chart-axis", x: m.l + pw / 2, y: H - 4, "text-anchor": "middle", text: opts.xLabel || "" }));
      if (opts.unit) root.appendChild(svg("text", { "class": "fc-chart-axis", x: 4, y: 11, "text-anchor": "start", text: opts.unit }));
      // marker (the level chosen in the filters)
      var mk = x.indexOf(opts.marker);
      if (mk >= 0) root.appendChild(svg("line", { "class": "fc-chart-marker", x1: sx(mk), x2: sx(mk), y1: m.t, y2: m.t + ph }));
      // context lines
      ctx.forEach(function (s) { root.appendChild(svg("path", { "class": "fc-chart-ctx", d: path(s.values) })); });
      // series
      if (opts.stacked) {
        for (var a = shown.length - 1; a >= 0; a--) {
          var up = tops[a], low = a ? tops[a - 1] : x.map(function () { return 0; }), d = "";
          up.forEach(function (v, k) { d += (k ? "L" : "M") + sx(k).toFixed(1) + " " + sy(v).toFixed(1); });
          for (var k2 = x.length - 1; k2 >= 0; k2--) d += "L" + sx(k2).toFixed(1) + " " + sy(low[k2]).toFixed(1);
          root.appendChild(svg("path", { "class": "fc-chart-area fc-viz-fill-" + shown[a].slot, d: d + "Z" }));
        }
      } else {
        shown.forEach(function (s) {
          root.appendChild(svg("path", { "class": "fc-chart-line fc-viz-stroke-" + s.slot, d: path(s.values) }));
          var last = s.values.length - 1;
          if (s.values[last] != null) root.appendChild(svg("circle", { "class": "fc-chart-dot fc-viz-fill-" + s.slot, cx: sx(last), cy: sy(s.values[last]), r: 4 }));
        });
        if (endLabels) {
          var labs = shown.map(function (s) { var v = s.values[s.values.length - 1]; return { s: s, y: v == null ? null : sy(v) }; })
            .filter(function (l) { return l.y != null; }).sort(function (p, q) { return p.y - q.y; });
          for (var n = 1; n < labs.length; n++) if (labs[n].y - labs[n - 1].y < 13) labs[n].y = labs[n - 1].y + 13;   // keep end labels apart
          labs.forEach(function (l) { root.appendChild(svg("text", { "class": "fc-chart-end", x: m.l + pw + 9, y: l.y + 3.5, text: clip(l.s.short || l.s.name, 34) })); });
        }
      }
      // crosshair layer
      var hair = svg("line", { "class": "fc-chart-hair", y1: m.t, y2: m.t + ph, visibility: "hidden" });
      var dots = shown.map(function (s) { return svg("circle", { "class": "fc-chart-dot fc-viz-fill-" + s.slot, r: 4, visibility: "hidden" }); });
      root.appendChild(hair); dots.forEach(function (c) { root.appendChild(c); });
      var hit = svg("rect", { x: m.l, y: m.t, width: pw, height: ph, fill: "transparent" });
      root.appendChild(hit);
      geom = { sx: sx, sy: sy, tops: tops, shown: shown, hair: hair, dots: dots, m: m, pw: pw, W: W };

      function show(k) {
        active = k;
        hair.setAttribute("x1", sx(k)); hair.setAttribute("x2", sx(k)); hair.setAttribute("visibility", "visible");
        var rows = [], total = 0;
        shown.forEach(function (s, idx) {
          var v = s.values[k], yv = opts.stacked ? tops[idx][k] : v;
          if (v == null) { dots[idx].setAttribute("visibility", "hidden"); return; }
          dots[idx].setAttribute("cx", sx(k)); dots[idx].setAttribute("cy", sy(yv)); dots[idx].setAttribute("visibility", opts.stacked ? "hidden" : "visible");
          total += v;
          rows.push({ s: s, v: v });
        });
        rows.sort(function (p, q) { return q.v - p.v; });
        var kids = [html("p", { "class": "fc-chart-tip-h", text: (opts.xLabel || "x") + " " + x[k] })];
        if (opts.stacked) kids.push(html("p", { "class": "fc-chart-tip-row" }, [html("strong", { text: fmt(total) + (opts.unit ? " " + opts.unit : "") }), html("span", { text: " total" })]));
        rows.forEach(function (r) {
          if (opts.stacked && r.v < 0.05) return;
          kids.push(html("p", { "class": "fc-chart-tip-row" }, [html("i", { "class": "fc-chart-key fc-viz-bg-" + r.s.slot }), html("strong", { text: fmt(r.v) }), html("span", { text: " " + r.s.name })]));
        });
        tip.replaceChildren.apply(tip, kids);
        tip.hidden = false;
        var px = sx(k), tw = tip.offsetWidth, left = px + 14 + tw > W ? px - 14 - tw : px + 14;
        tip.style.left = Math.max(0, left) + "px"; tip.style.top = m.t + "px";
      }
      function hide() { active = null; hair.setAttribute("visibility", "hidden"); dots.forEach(function (c) { c.setAttribute("visibility", "hidden"); }); tip.hidden = true; }
      function nearest(ev) {
        var r = root.getBoundingClientRect(), px = (ev.clientX - r.left) * (W / r.width);
        return Math.max(0, Math.min(x.length - 1, Math.round((px - m.l) / pw * (x.length - 1))));
      }
      root.addEventListener("pointermove", function (ev) { show(nearest(ev)); });
      root.addEventListener("pointerleave", function () { if (document.activeElement !== root) hide(); });
      root.addEventListener("focus", function () { if (active == null) show(mk >= 0 ? mk : x.length - 1); });
      root.addEventListener("blur", hide);
      root.addEventListener("keydown", function (ev) {
        var k = active == null ? (mk >= 0 ? mk : x.length - 1) : active;
        if (ev.key === "ArrowLeft") k = Math.max(0, k - 1);
        else if (ev.key === "ArrowRight") k = Math.min(x.length - 1, k + 1);
        else if (ev.key === "Home") k = 0;
        else if (ev.key === "End") k = x.length - 1;
        else if (ev.key === "Escape") { hide(); return; }
        else return;
        ev.preventDefault(); show(k);
      });
      var old = plot.querySelector("svg");
      if (old) old.replaceWith(root); else plot.insertBefore(root, tip);
      tip.hidden = true; active = null;

      // legend: always present for two or more series; a swatch that mirrors the mark, then the name in text colour
      legend.replaceChildren.apply(legend, shown.length > 1 || opts.stacked ? shown.map(function (s) {
        var v = mk >= 0 ? s.values[mk] : null;
        return html("li", {}, [html("i", { "class": (opts.stacked ? "fc-chart-box" : "fc-chart-key") + " fc-viz-bg-" + s.slot }), html("span", { text: s.name }),
          v != null ? html("small", { text: " " + fmt(v) }) : null]);
      }) : []);
      legend.hidden = !legend.children.length;
      note.textContent = opts.note || ""; note.hidden = !opts.note;
    }

    render();
    var timer = 0, lastW = plot.clientWidth;
    if (window.ResizeObserver) new ResizeObserver(function () {
      if (plot.clientWidth === lastW) return;
      lastW = plot.clientWidth; clearTimeout(timer); timer = setTimeout(render, 60);
    }).observe(plot);
    return { update: function (next) { opts = next; render(); }, geometry: function () { return geom; } };
  }

  window.ForeverCharts = { draw: draw, format: fmt, SLOTS: 6 };
})();
