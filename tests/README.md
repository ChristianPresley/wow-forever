# Quality gates

Automated checks for the built site, run by `.github/workflows/quality.yml` on every pull
request, every push to `main` and weekly (link rot). All check jobs are currently
**non-blocking** (`continue-on-error: true`); remove that line from a job to make it gate merges.

| Check | Tool | Script | Threshold (env) |
|---|---|---|---|
| Accessibility, WCAG 2.0/2.1/2.2 A+AA, light **and** dark scheme, 1280px all pages + 375px sample | axe-core 4.x via `@axe-core/playwright` + local Chrome | `tests/a11y.mjs` | `A11Y_MAX_VIOLATIONS=0` |
| HTML validity | `html-validate` (`recommended` preset, theme-template noise off) | `tests/html.mjs`, `tests/htmlvalidate.json` | `HTML_MAX_ERRORS=0` |
| Internal links and `#anchors` (offline) | built-in checker | `tests/links.mjs` | `LINKS_MAX_BROKEN=0` |
| External links | lychee (CI only) | `tests/lychee.toml` | 403/429 accepted |
| Performance, a11y, SEO, byte budgets | Lighthouse CI | `tests/lighthouserc.json`, `tests/lhci-summary.mjs` | see assertions |

## Run locally

```bash
npm ci
NO_MKDOCS_2_WARNING=1 .venv/Scripts/mkdocs.exe build --strict
npm run test:html
npm run test:a11y          # uses installed Chrome (or set CHROME_PATH)
npm run test:links
CHROME_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe" npm run test:lhci
npm run test:lhci:summary
```

Point any script at another build with `SITE_DIR=<dir>` and `REPORT_DIR=<dir>`. Reports go
to `tests/reports/` (git-ignored). `node tests/serve.mjs [dir] [port]` serves a build under
the `/wow-forever/` base path with gzip, like GitHub Pages.

## Notes

- Scans are hermetic: requests to anything but the local server are blocked (the theme's
  GitHub repo-stats fetch otherwise hits API rate limits and pollutes console checks).
- Colour scheme is driven by `prefers-color-scheme` emulation; the run records
  `data-md-color-scheme` per page so a broken toggle would show up as a wrong scheme.
- `html-validate` rules disabled in `htmlvalidate.json` are ones that only fire on markup
  emitted by the Material theme itself (e.g. `tabindex=""`, `rel="edit"`, raw `&` in nav
  titles, the search `<form>` without a submit button). Content-level rules stay on.
- Automated tools find roughly half of WCAG failures. Keyboard, screen-reader and zoom
  checks still need a human pass.
