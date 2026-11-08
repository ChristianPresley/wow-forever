// Tiny static server for the built site, mounted under the GitHub Pages base path.
// Usage: node tests/serve.mjs [siteDir] [port]   (env: SITE_DIR, PORT, BASE_PATH)
import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import { extname, join, normalize, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";
import { gzipSync } from "node:zlib";

const TYPES = {
  ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8", ".mjs": "text/javascript; charset=utf-8",
  ".json": "application/json", ".xml": "application/xml", ".txt": "text/plain; charset=utf-8",
  ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
  ".webp": "image/webp", ".avif": "image/avif", ".ico": "image/x-icon", ".gif": "image/gif",
  ".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf", ".gz": "application/gzip",
};

export const BASE_PATH = process.env.BASE_PATH ?? "/wow-forever/";

export function startServer({ dir = process.env.SITE_DIR || "site", port = process.env.PORT ? Number(process.env.PORT) : 4173 } = {}) {
  const root = resolve(dir);
  const server = createServer(async (req, res) => {
    try {
      let path = decodeURIComponent(new URL(req.url, "http://x").pathname);
      if (path === "/" || path === BASE_PATH.slice(0, -1)) { res.writeHead(302, { location: BASE_PATH }); return res.end(); }
      if (!path.startsWith(BASE_PATH)) { res.writeHead(404); return res.end("outside base path"); }
      let file = normalize(join(root, path.slice(BASE_PATH.length)));
      if (file !== root && !file.startsWith(root + sep)) { res.writeHead(403); return res.end(); }
      let info = await stat(file).catch(() => null);
      if (info?.isDirectory()) { file = join(file, "index.html"); info = await stat(file).catch(() => null); }
      if (!info) {
        const body = await readFile(join(root, "404.html")).catch(() => "Not found");
        res.writeHead(404, { "content-type": TYPES[".html"] }); return res.end(body);
      }
      const type = TYPES[extname(file).toLowerCase()] || "application/octet-stream";
      let body = await readFile(file);
      const headers = { "content-type": type, "cache-control": "no-cache" };
      // GitHub Pages gzips text responses; do the same so transfer-size budgets are realistic.
      if (/text|json|xml|svg/.test(type) && /gzip/.test(req.headers["accept-encoding"] || "")) { body = gzipSync(body); headers["content-encoding"] = "gzip"; headers.vary = "accept-encoding"; }
      res.writeHead(200, headers);
      res.end(body);
    } catch (err) { res.writeHead(500); res.end(String(err)); }
  });
  return new Promise((ok) => server.listen(port, "127.0.0.1", () => ok({ server, url: `http://127.0.0.1:${server.address().port}${BASE_PATH}` })));
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const { url } = await startServer({ dir: process.argv[2] || undefined, port: process.argv[3] ? Number(process.argv[3]) : undefined });
  console.log(`Serving on ${url}`);
}
