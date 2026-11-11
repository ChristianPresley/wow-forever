// Screenshots of the built site for visual review.
// Usage: node tests/shots.mjs <outDir> [page,page,...]   (env: SITE_DIR, SHOT_SCHEMES=light,dark, SHOT_WIDTHS=1440,390, SHOT_FULL=1)
// Pages are base-path-relative ("", "guides/mage/", "guides/mage/?race=gnome#l20").
import { mkdirSync } from "node:fs";
import { join } from "node:path";
import { chromium } from "playwright-core";
import { startServer } from "./serve.mjs";

const out = process.argv[2] || "tests/reports/shots";
const pages = (process.argv[3] || ",guides/,guides/mage/,guides/mage/talents/,guides/mage/equipment/,guides/mage/gnome/,professions/,professions/tailoring/,content/dungeons/,content/dungeons/hall-of-thanes/,characters/races/,community/glossary/").split(",");
const schemes = (process.env.SHOT_SCHEMES || "light,dark").split(",");
const widths = (process.env.SHOT_WIDTHS || "1440,390").split(",").map(Number);
const full = process.env.SHOT_FULL === "1";
mkdirSync(out, { recursive: true });

const { server, url: base } = await startServer({ dir: process.env.SITE_DIR || "site", port: Number(process.env.PORT || 0) });
const browser = await chromium.launch(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : { channel: "chrome" });
for (const scheme of schemes) {
  for (const width of widths) {
    const ctx = await browser.newContext({ viewport: { width, height: width < 600 ? 844 : 900 }, colorScheme: scheme, deviceScaleFactor: 1, reducedMotion: "reduce" });
    const page = await ctx.newPage();
    for (const p of pages) {
      await page.goto(base + p, { waitUntil: "networkidle" });
      const hash = p.includes("#") ? p.split("#")[1] : "";
      if (hash) await page.evaluate((h) => { const e = document.getElementById(h); if (e) window.scrollTo(0, e.getBoundingClientRect().top + scrollY - 80); }, hash);
      await page.waitForTimeout(250);
      const name = (p.replace(/[?#=&]/g, "_").replace(/\/+$/, "").replace(/\//g, "_") || "home") + `.${width}.${scheme}.png`;
      await page.screenshot({ path: join(out, name), fullPage: full && !hash });
      console.log(name);
    }
    await ctx.close();
  }
}
await browser.close();
server.close();
