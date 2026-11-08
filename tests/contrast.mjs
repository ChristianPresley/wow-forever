// Contrast sweep of key UI roles in both colour schemes, computed from rendered colours
// (alpha-blended over the real background chain). Complements axe, which leaves text on
// gradients/backgrounds as "needs review". env: SITE_DIR, REPORT_DIR, CONTRAST_PAGES
import { chromium } from "playwright-core";
import { mkdirSync, writeFileSync } from "node:fs";
import { startServer } from "./serve.mjs";

const SITE_DIR = process.env.SITE_DIR || "site";
const OUT = process.env.REPORT_DIR || "tests/reports";
const PAGES = (process.env.CONTRAST_PAGES || ",about/,characters/classes/mage/,guides/mage/human/,content/dungeons/hall-of-thanes/,community/glossary/,sources/").split(",");
const ROLES = {
  "body text": ".md-typeset p", "link": ".md-typeset p a", "h1": ".md-typeset h1", "h2": ".md-typeset h2",
  "header title": ".md-header__topic", "tab link": ".md-tabs__link", "sidebar link": ".md-nav--primary .md-nav__link",
  "active sidebar link": ".md-nav__link--active", "toc link": ".md-nav--secondary .md-nav__link", "breadcrumb": ".md-path__link",
  "table header": ".md-typeset th", "table cell": ".md-typeset td", "inline code": ".md-typeset p code",
  "admonition title": ".md-typeset .admonition-title, .md-typeset summary", "admonition body": ".md-typeset .admonition p, .md-typeset details p",
  "footer link": ".md-footer__link", "copyright": ".md-copyright", "source/repo": ".md-source__repository",
  "search placeholder": ".md-search__input", "tag": ".md-tag", "caption/small": ".md-typeset small, .md-typeset figcaption",
};

const { server, url: base } = await startServer({ dir: SITE_DIR, port: Number(process.env.PORT || 0) });
const browser = await chromium.launch(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : { channel: "chrome" });
const rows = [];
for (const scheme of ["light", "dark"]) for (const p of PAGES) {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, colorScheme: scheme, reducedMotion: "reduce" });
  await ctx.route((u) => !u.href.startsWith(base.replace(/\/wow-forever\/$/, "")), (r) => r.abort());
  const page = await ctx.newPage();
  await page.goto(base + p, { waitUntil: "load" });
  const res = await page.evaluate((roles) => {
    const parse = (c) => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const [r, g, b, a = 1] = m[1].split(/[ ,/]+/).filter(Boolean).map(Number); return [r, g, b, a]; };
    const blend = (top, bot) => [0, 1, 2].map((i) => top[i] * top[3] + bot[i] * (1 - top[3])).concat(1);
    const lum = ([r, g, b]) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
    let img = false;
    const bgOf = (el) => { img = false; const stack = []; for (let e = el; e; e = e.parentElement) { const st = getComputedStyle(e); if (st.backgroundImage !== "none") img = true; const c = parse(st.backgroundColor); if (c && c[3] > 0) { stack.push(c); if (c[3] >= 1) break; } } let bg = [255, 255, 255, 1]; for (const c of stack.reverse()) bg = blend(c, bg); return bg; };
    const out = {};
    for (const [role, sel] of Object.entries(roles)) {
      const el = [...document.querySelectorAll(sel)].find((e) => e.getClientRects().length && getComputedStyle(e).visibility !== "hidden");
      if (!el) continue;
      const cs = getComputedStyle(el); const bg = bgOf(el); let fg = parse(cs.color); fg = blend([fg[0], fg[1], fg[2], fg[3] * Number(cs.opacity)], bg);
      const [l1, l2] = [lum(fg), lum(bg)].sort((a, b) => b - a);
      const px = parseFloat(cs.fontSize), large = px >= 24 || (px >= 18.66 && Number(cs.fontWeight) >= 700);
      const hex = (c) => "#" + c.slice(0, 3).map((v) => Math.round(v).toString(16).padStart(2, "0")).join("");
      out[role] = { ratio: +((l1 + 0.05) / (l2 + 0.05)).toFixed(2), fg: hex(fg), bg: hex(bg), px, need: large ? 3 : 4.5, bgImage: img };
    }
    return { scheme: document.body.dataset.mdColorScheme, out };
  }, ROLES);
  for (const [role, v] of Object.entries(res.out)) rows.push({ scheme, attr: res.scheme, page: p || "/", role, ...v });
  await ctx.close();
}
await browser.close(); server.close();

// Collapse per scheme+role: keep the worst page (solid backgrounds rank before image/gradient ones).
const worst = {};
const rank = (r) => (r.bgImage && r.ratio < r.need ? 100 : 0) + r.ratio;
for (const r of rows) { const k = `${r.scheme}|${r.role}`; if (!worst[k] || rank(r) < rank(worst[k])) worst[k] = r; }
let md = `# Contrast sweep (rendered colours, worst page per role)\n\n| Scheme | Role | Ratio | Need | FG | BG | px | Worst page |\n|---|---|---|---|---|---|---|---|\n`;
for (const r of Object.values(worst).sort((a, b) => a.scheme.localeCompare(b.scheme) || a.ratio - b.ratio))
  md += `| ${r.scheme} | ${r.role} | ${r.ratio < r.need ? (r.bgImage ? r.ratio + " (manual: text on image/gradient)" : "**" + r.ratio + "** ✗") : r.ratio} | ${r.need} | ${r.fg} | ${r.bg}${r.bgImage ? " (bg image)" : ""} | ${r.px} | ${r.page} |\n`;
mkdirSync(OUT, { recursive: true });
writeFileSync(`${OUT}/contrast.md`, md);
console.log(md);
process.exit(Object.values(worst).some((r) => r.ratio < r.need && !r.bgImage) ? 1 : 0);
