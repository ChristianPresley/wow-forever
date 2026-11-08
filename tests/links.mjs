// Offline internal link + anchor checker for the built site (no network).
// CI also runs lychee for external links; this is the fast local equivalent of
// `lychee --offline --include-fragments`. env: SITE_DIR, REPORT_DIR, LINKS_MAX_BROKEN (0)
import { readFileSync, writeFileSync, mkdirSync, readdirSync, existsSync, statSync } from "node:fs";
import { join, relative, sep, dirname, posix } from "node:path";

const SITE_DIR = process.env.SITE_DIR || "site";
const OUT = process.env.REPORT_DIR || "tests/reports";
const MAX = Number(process.env.LINKS_MAX_BROKEN ?? 0);
const SITE_URL = "https://christianpresley.github.io/wow-forever/";
const BASE = "/wow-forever/";

const files = [];
const walk = (d) => { for (const e of readdirSync(d, { withFileTypes: true })) { const p = join(d, e.name); if (e.isDirectory()) walk(p); else if (e.name.endsWith(".html")) files.push(relative(SITE_DIR, p).split(sep).join("/")); } };
walk(SITE_DIR);

// Attribute values may be double-, single- or un-quoted (minify_html drops quotes).
const VAL = String.raw`(?:"([^"]*)"|'([^']*)'|([^\s"'=<>]+))`;
const TAG = /<(a|link|img|script|source|iframe)\b((?:[^>"']|"[^"]*"|'[^']*')*)>/g;
const URL_ATTR = new RegExp(String.raw`\s(?:href|src)=` + VAL, "g");
const ID_ATTR = new RegExp(String.raw`\s(?:id|name)=` + VAL, "g");
const idCache = new Map();
const decode = (s) => s.replace(/&amp;/g, "&").replace(/&#x27;|&#39;/g, "'").replace(/&quot;/g, '"');
function ids(file) {
  if (!idCache.has(file)) {
    const html = readFileSync(join(SITE_DIR, file), "utf8");
    idCache.set(file, new Set([...html.matchAll(ID_ATTR)].map((m) => decode(m[1] ?? m[2] ?? m[3]))));
  }
  return idCache.get(file);
}
function resolveTarget(path) {
  let p = path.replace(/^\/+/, "");
  const full = join(SITE_DIR, p);
  if (existsSync(full) && statSync(full).isDirectory()) return existsSync(join(full, "index.html")) ? posix.join(p, "index.html") : null;
  return existsSync(full) ? p : null;
}

const broken = [], external = new Set(); let checked = 0;
for (const file of files) {
  if (file === "404.html") continue; // uses absolute site_url paths by design
  const html = readFileSync(join(SITE_DIR, file), "utf8").replace(/(<script\b[^>]*>)[\s\S]*?<\/script>/g, "$1</script>");
  const pageDir = posix.dirname(file);
  for (const t of html.matchAll(TAG)) for (const m of t[2].matchAll(URL_ATTR)) {
    let url = decode(m[1] ?? m[2] ?? m[3]).trim();
    if (!url || /^(mailto|tel|javascript|data):/i.test(url)) continue;
    if (url.startsWith(SITE_URL)) url = BASE + url.slice(SITE_URL.length);
    if (/^(https?:)?\/\//i.test(url)) { external.add(url.split("#")[0]); continue; }
    checked++;
    const [pathPart, frag] = url.split("#");
    const clean = decodeURIComponent(pathPart.split("?")[0]);
    let target;
    if (!clean) target = file;
    else if (clean.startsWith(BASE)) target = resolveTarget(clean.slice(BASE.length));
    else if (clean.startsWith("/")) target = null;
    else target = resolveTarget(posix.normalize(posix.join(pageDir, clean)));
    if (!target) { broken.push({ file, url, why: "missing target" }); continue; }
    if (frag && target.endsWith(".html") && !ids(target).has(decodeURIComponent(frag))) broken.push({ file, url, why: `missing anchor #${frag}` });
  }
}

const uniq = new Map(); for (const b of broken) { const k = `${b.url} (${b.why})`; (uniq.get(k) ?? uniq.set(k, []).get(k)).push(b.file); }
let md = `# Internal links (offline)\n\n${files.length} files, ${checked} internal links/assets checked, ${external.size} unique external URLs (checked online by lychee in CI). **${broken.length} broken.**\n\n`;
for (const [k, fs] of [...uniq].sort((a, b) => b[1].length - a[1].length)) md += `- \`${k}\` in ${fs.length} file(s): ${fs.slice(0, 5).join(", ")}${fs.length > 5 ? " ..." : ""}\n`;
mkdirSync(OUT, { recursive: true });
writeFileSync(`${OUT}/links.md`, md);
writeFileSync(`${OUT}/external-urls.txt`, [...external].sort().join("\n") + "\n");
console.log(md.split("\n").slice(0, 3).join("\n"));
if (process.env.GITHUB_STEP_SUMMARY) writeFileSync(process.env.GITHUB_STEP_SUMMARY, md, { flag: "a" });
process.exit(broken.length > MAX ? 1 : 0);
