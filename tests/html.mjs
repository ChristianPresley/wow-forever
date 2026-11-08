// html-validate over the built site. Theme-template noise is turned off in tests/htmlvalidate.json.
// env: SITE_DIR, REPORT_DIR, HTML_MAX_ERRORS (default 0)
import { HtmlValidate, FileSystemConfigLoader } from "html-validate";
import { readFileSync, writeFileSync, mkdirSync, readdirSync } from "node:fs";
import { join, relative, sep } from "node:path";

const SITE_DIR = process.env.SITE_DIR || "site";
const OUT = process.env.REPORT_DIR || "tests/reports";
const MAX = Number(process.env.HTML_MAX_ERRORS ?? 0);
const config = JSON.parse(readFileSync(new URL("./htmlvalidate.json", import.meta.url), "utf8"));
delete config.$schema;
const hv = new HtmlValidate(new FileSystemConfigLoader(config));

const files = [];
const walk = (d) => { for (const e of readdirSync(d, { withFileTypes: true })) { const p = join(d, e.name); if (e.isDirectory()) walk(p); else if (e.name.endsWith(".html")) files.push(p); } };
walk(SITE_DIR);

const byRule = {}; let errors = 0, warnings = 0;
for (const f of files) {
  const report = await hv.validateFile(f);
  for (const r of report.results) for (const m of r.messages) {
    m.severity === 2 ? errors++ : warnings++;
    const k = (byRule[m.ruleId] ??= { rule: m.ruleId, severity: m.severity === 2 ? "error" : "warning", count: 0, files: new Set(), examples: [] });
    k.count++; k.files.add(relative(SITE_DIR, f).split(sep).join("/"));
    if (k.examples.length < 3) k.examples.push(`${relative(SITE_DIR, f).split(sep).join("/")}:${m.line}:${m.column} ${m.message} (\`${m.selector ?? ""}\`)`);
  }
}
let md = `# html-validate\n\n${files.length} files. **${errors} errors, ${warnings} warnings.**\n\n`;
for (const r of Object.values(byRule).sort((a, b) => (a.severity > b.severity ? 1 : -1) || b.count - a.count))
  md += `## ${r.rule} (${r.severity}): ${r.count} in ${r.files.size} files\n${r.examples.map((e) => `- ${e}`).join("\n")}\n\n`;
mkdirSync(OUT, { recursive: true });
writeFileSync(`${OUT}/html.md`, md);
console.log(md.split("\n").slice(0, 3).join("\n"));
if (process.env.GITHUB_STEP_SUMMARY) writeFileSync(process.env.GITHUB_STEP_SUMMARY, md, { flag: "a" });
process.exit(errors > MAX ? 1 : 0);
