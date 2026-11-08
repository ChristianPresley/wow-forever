// Summarises Lighthouse JSON reports (from lhci's filesystem upload) into markdown.
// Usage: node tests/lhci-summary.mjs [reportDir] [out.md]
import { readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
const dir = process.argv[2] || "tests/reports/lhci";
const out = process.argv[3] || join(dir, "summary.md");
const kb = (n) => (n / 1024).toFixed(0);
let md = "# Lighthouse (mobile emulation, simulated throttling; median-performance run per URL)\n\n| Page | Perf | A11y | BP | SEO | FCP | LCP | TBT | CLS | JS KB | CSS KB | Font KB | Total KB | Req |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n";
const fails = {};
// Keep the median-performance run per URL (lhci's own aggregation for assertions).
const byUrl = {};
for (const f of readdirSync(dir).filter((f) => f.endsWith(".json") && f.startsWith("127"))) {
  const r = JSON.parse(readFileSync(join(dir, f), "utf8"));
  (byUrl[r.finalDisplayedUrl || r.finalUrl] ??= []).push(r);
}
const runs = Object.values(byUrl).map((rs) => rs.sort((x, y) => x.categories.performance.score - y.categories.performance.score)[Math.floor(rs.length / 2)]);
for (const r of runs.sort((x, y) => (x.finalDisplayedUrl || x.finalUrl).localeCompare(y.finalDisplayedUrl || y.finalUrl))) {
  const c = r.categories, a = r.audits, rs = Object.fromEntries(a["resource-summary"].details.items.map((i) => [i.resourceType, i]));
  const path = new URL(r.finalDisplayedUrl || r.finalUrl).pathname.replace("/wow-forever/", "/") || "/";
  md += `| ${path} | ${Math.round(c.performance.score * 100)} | ${Math.round(c.accessibility.score * 100)} | ${Math.round(c["best-practices"].score * 100)} | ${Math.round(c.seo.score * 100)} | ${a["first-contentful-paint"].displayValue} | ${a["largest-contentful-paint"].displayValue} | ${a["total-blocking-time"].displayValue} | ${a["cumulative-layout-shift"].displayValue} | ${kb(rs.script?.transferSize || 0)} | ${kb(rs.stylesheet?.transferSize || 0)} | ${kb(rs.font?.transferSize || 0)} | ${kb(rs.total.transferSize)} | ${rs.total.requestCount} |\n`;
  for (const cat of ["accessibility", "best-practices", "seo", "performance"])
    for (const ref of c[cat].auditRefs) { const au = a[ref.id]; if (ref.weight > 0 && au.score !== null && au.score < 0.9) (fails[`${cat}: ${ref.id}: ${au.title}`] ??= []).push(path); }
}
md += "\n## Audits scoring below 0.9\n\n" + Object.entries(fails).sort((x, y) => y[1].length - x[1].length).map(([k, v]) => `- ${k} (${v.length}): ${v.join(", ")}`).join("\n") + "\n";
writeFileSync(out, md);
console.log(md);
