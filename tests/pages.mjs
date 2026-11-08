// Lists built pages as base-path-relative URLs ("", "about/", "guides/mage/human/").
import { readdirSync } from "node:fs";
import { join, relative, sep } from "node:path";

export function listPages(dir) {
  const out = [];
  const walk = (d) => {
    for (const e of readdirSync(d, { withFileTypes: true })) {
      const p = join(d, e.name);
      if (e.isDirectory()) { if (e.name !== "assets" && e.name !== "search") walk(p); }
      else if (e.name === "index.html") out.push(relative(dir, d).split(sep).join("/"));
    }
  };
  walk(dir);
  return out.map((p) => (p ? p + "/" : "")).sort();
}
