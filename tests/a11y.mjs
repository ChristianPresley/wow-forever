// axe-core scan of every built page, in both colour schemes, at desktop width,
// plus a 375px pass over a sample. Writes tests/reports/a11y.{json,md}.
//
// env: SITE_DIR (default site), A11Y_MAX_VIOLATIONS (default 0), A11Y_PAGES (comma list
// of page paths to restrict to), A11Y_MOBILE_SAMPLE (default 12), A11Y_CONCURRENCY (4),
// CHROME_PATH (else Playwright's "chrome" channel, preinstalled on GitHub ubuntu runners).
import { chromium } from "playwright-core";
import { AxeBuilder } from "@axe-core/playwright";
import { mkdirSync, writeFileSync } from "node:fs";
import { startServer } from "./serve.mjs";
import { listPages } from "./pages.mjs";

const SITE_DIR = process.env.SITE_DIR || "site";
const MAX = Number(process.env.A11Y_MAX_VIOLATIONS ?? 0);
const CONCURRENCY = Number(process.env.A11Y_CONCURRENCY || 4);
const MOBILE_SAMPLE = Number(process.env.A11Y_MOBILE_SAMPLE ?? 12);
const OUT = process.env.REPORT_DIR || "tests/reports";
const TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"];

let pages = listPages(SITE_DIR);
if (process.env.A11Y_PAGES) pages = process.env.A11Y_PAGES.split(",").map((s) => s.trim());

// Mobile sample: home, every section index, then an even spread of the rest.
const sectionIdx = pages.filter((p) => p.split("/").length === 2);
const rest = pages.filter((p) => !sectionIdx.includes(p) && p !== "");
const step = Math.max(1, Math.floor(rest.length / Math.max(1, MOBILE_SAMPLE - sectionIdx.length - 1)));
const mobile = ["", ...sectionIdx, ...rest.filter((_, i) => i % step === 0)].slice(0, MOBILE_SAMPLE);

const jobs = [];
for (const p of pages) for (const scheme of ["light", "dark"]) jobs.push({ page: p, scheme, width: 1280, height: 900 });
for (const p of mobile) for (const scheme of ["light", "dark"]) jobs.push({ page: p, scheme, width: 375, height: 812 });

const { server, url: base } = await startServer({ dir: SITE_DIR, port: Number(process.env.PORT || 0) /* 0 = any free port */ });
const browser = await chromium.launch(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : { channel: "chrome" });

const results = [];
async function run(job) {
  const ctx = await browser.newContext({ viewport: { width: job.width, height: job.height }, colorScheme: job.scheme, reducedMotion: "reduce" });
  // Hermetic: the built site self-hosts fonts (privacy plugin); block the GitHub repo-stats API etc.
  await ctx.route((u) => !u.href.startsWith(base.replace(/\/wow-forever\/$/, "")), (r) => r.abort());
  const page = await ctx.newPage();
  const consoleErrors = [];
  page.on("pageerror", (e) => consoleErrors.push(String(e)));
  page.on("console", (m) => { if (m.type() === "error" && !m.text().startsWith("Failed to load resource")) consoleErrors.push(m.text()); });
  page.on("response", (res) => { if (res.status() >= 400 && res.url().startsWith(base)) consoleErrors.push(`HTTP ${res.status()} ${res.url().replace(base, "/")}`); });
  try {
    await page.goto(base + job.page, { waitUntil: "load", timeout: 30000 });
    await page.waitForTimeout(250);
    const scheme = await page.evaluate(() => document.body.getAttribute("data-md-color-scheme"));
    const r = await new AxeBuilder({ page }).withTags(TAGS).analyze();
    // target-size "partially obscured" on a sidebar link = the link half-scrolled out of the sticky
    // sidebar's visible area at this scroll position (a scan artefact, not a size defect). Report apart.
    const clipped = (v, n) => v.id === "target-size" && /partially obscured/.test(n.failureSummary || "") && /md-nav/.test(n.target.join(" "));
    const map = (v, keep) => ({ id: v.id, impact: v.impact, help: v.help, helpUrl: v.helpUrl,
      nodes: v.nodes.filter((n) => keep === !clipped(v, n)).map((n) => ({ target: n.target.join(" "), summary: n.failureSummary?.split("\n").slice(0, 3).join(" ") })) });
    results.push({ ...job, scheme_attr: scheme, consoleErrors,
      violations: r.violations.map((v) => map(v, true)).filter((v) => v.nodes.length),
      scrollClipped: r.violations.map((v) => map(v, false)).reduce((a, v) => a + v.nodes.length, 0),
      incomplete: r.incomplete.map((v) => ({ id: v.id, count: v.nodes.length })) });
  } catch (e) {
    results.push({ ...job, error: String(e), violations: [], incomplete: [], consoleErrors });
  } finally { await ctx.close(); }
}

const queue = [...jobs];
await Promise.all(Array.from({ length: CONCURRENCY }, async () => { while (queue.length) await run(queue.shift()); }));
await browser.close(); server.close();

// Aggregate by rule and by rule+selector so repeated template issues collapse.
const byRule = {};
for (const r of results) for (const v of r.violations) {
  const k = byRule[v.id] ??= { id: v.id, impact: v.impact, help: v.help, helpUrl: v.helpUrl, pages: new Set(), nodes: 0, targets: {} };
  k.pages.add(`${r.page || "(home)"} [${r.scheme}${r.width < 768 ? ", 375px" : ""}]`); k.nodes += v.nodes.length;
  for (const n of v.nodes) (k.targets[n.target] ??= { count: 0, summary: n.summary }).count++;
}
const total = Object.values(byRule).reduce((a, r) => a + r.nodes, 0);
const errors = results.filter((r) => r.error);
const jsErrors = results.filter((r) => r.consoleErrors.length);

mkdirSync(OUT, { recursive: true });
writeFileSync(`${OUT}/a11y.json`, JSON.stringify({ tags: TAGS, jobs: results.length, total, results }, null, 2));
let md = `# axe-core ${TAGS.join(", ")}\n\n${results.length} page loads (${pages.length} pages x 2 schemes at 1280px, ${mobile.length} x 2 at 375px). ` +
  `**${total} violating nodes** across ${Object.keys(byRule).length} rules. Load errors: ${errors.length}. Pages with JS console errors: ${jsErrors.length}. ` +
  `Informational (not counted): ${results.reduce((a, r) => a + (r.scrollClipped || 0), 0)} sidebar links reported by target-size as "partially obscured" because they were half-scrolled at the sidebar's clip edge.\n\n`;
for (const r of Object.values(byRule).sort((a, b) => b.nodes - a.nodes)) {
  md += `## ${r.id} (${r.impact}): ${r.nodes} nodes on ${r.pages.size} page loads\n${r.help}. ${r.helpUrl}\n\n`;
  for (const [t, v] of Object.entries(r.targets).sort((a, b) => b[1].count - a[1].count).slice(0, 8)) md += `- \`${t}\` x${v.count}: ${v.summary ?? ""}\n`;
  md += `- pages: ${[...r.pages].slice(0, 10).join("; ")}${r.pages.size > 10 ? " ..." : ""}\n\n`;
}
if (errors.length) md += `## Load errors\n${errors.map((e) => `- ${e.page}: ${e.error}`).join("\n")}\n\n`;
if (jsErrors.length) md += `## JS console errors\n${[...new Set(jsErrors.flatMap((r) => r.consoleErrors.map((c) => `- ${r.page || "(home)"}: ${c.slice(0, 200)}`)))].slice(0, 30).join("\n")}\n`;
writeFileSync(`${OUT}/a11y.md`, md);
console.log(md.split("\n").slice(0, 3).join("\n"));
if (process.env.GITHUB_STEP_SUMMARY) writeFileSync(process.env.GITHUB_STEP_SUMMARY, md, { flag: "a" });
process.exit(total > MAX || errors.length ? 1 : 0);
