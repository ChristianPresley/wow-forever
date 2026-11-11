// The CSS minifier (mkdocs-minify-plugin) can drop the space before a pseudo-class in the first selector of
// an @media block: ".md-typeset :is(h2, h3)" becomes ".md-typeset:is(h2,h3)", and the rule matches nothing.
// This gate compares each source stylesheet with the built one: the number of descendant pseudo-classes
// (" :is(", " :where(", " :not(", " :has(") must be the same.
// Usage: node tests/css.mjs   (env: SITE_DIR)
import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const site = process.env.SITE_DIR || "site";
const src = "docs/stylesheets";
const strip = (css) => css.replace(/\/\*[\s\S]*?\*\//g, "");
const count = (css) => (strip(css).match(/[\w\])*]\s+:(?:is|where|not|has)\(/g) || []).length;
const built = readdirSync(join(site, "stylesheets")).filter((f) => f.endsWith(".css"));
let bad = 0;
for (const name of readdirSync(src).filter((f) => f.endsWith(".css"))) {
  const stem = name.replace(/\.css$/, "");
  const out = built.find((f) => f === name || (f.startsWith(stem + ".") && f.endsWith(".css")));
  if (!out) { console.error(`css: ${name} is not in ${site}/stylesheets`); bad++; continue; }
  const a = count(readFileSync(join(src, name), "utf8")), b = count(readFileSync(join(site, "stylesheets", out), "utf8"));
  if (a !== b) {
    bad++;
    const lost = strip(readFileSync(join(site, "stylesheets", out), "utf8")).match(/[{}][^{}]*?[\w\])*]:(?:is|where|not|has)\([^{}]*/g) || [];
    console.error(`css: ${name}: ${a} descendant pseudo-classes in the source, ${b} in the build. Look at these built selectors:`);
    lost.filter((s) => /^\{/.test(s)).slice(0, 20).forEach((s) => console.error("  " + s.slice(1, 120)));
  }
}
if (bad) { console.error(`css: ${bad} stylesheet(s) lost a selector space. Do not start an @media block with a selector that has " :is(".`); process.exit(1); }
console.log(`css: ${built.length} built stylesheets, no selector space lost`);
