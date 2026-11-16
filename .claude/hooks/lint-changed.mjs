// Claude Code PostToolUse hook: lint the file that Claude has just written or edited.
// Registered in .claude/settings.json for Edit, Write, MultiEdit and NotebookEdit.
//
// It reads the hook payload (JSON) on stdin, picks the linter for the file type, and runs it on
// that one file. Clean: exit 0, no output. Findings: they go to stderr with exit code 2, which
// Claude Code gives back to Claude so that it fixes them. The full check is `npm run lint`.
//
//   .js .mjs                    ESLint         (eslint.config.mjs)
//   docs/stylesheets/**/*.css   Stylelint      (.stylelintrc.json)
//   tools/**/*.py               Ruff           (ruff.toml)
//   docs/**/*.md                unslop-prose   (tools/unslop_prose/lint.py)
//
// Test it by hand:
//   echo '{"tool_input":{"file_path":"docs/index.md"}}' | node .claude/hooks/lint-changed.mjs
import { spawnSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");

function payload() {
  try { return JSON.parse(readFileSync(0, "utf8")); } catch { return {}; }
}

function python() {
  const found = [".venv/Scripts/python.exe", ".venv/bin/python"].map((p) => path.join(root, p)).find(existsSync);
  return found || (process.platform === "win32" ? "python" : "python3");
}

const data = payload();
const given = (data.tool_input && (data.tool_input.file_path || data.tool_input.notebook_path)) || (data.tool_response && data.tool_response.filePath);
if (!given) process.exit(0);
const file = path.resolve(root, given);
const rel = path.relative(root, file).split(path.sep).join("/");
if (rel.startsWith("..") || path.isAbsolute(rel) || !existsSync(file)) process.exit(0);   // not a file of this repository
if (/^(site|node_modules|\.venv|\.cache|\.claude|\.lighthouseci)\//.test(rel)) process.exit(0);

const node = process.execPath;
const ext = path.extname(rel).toLowerCase();
let name, cmd, args;
if (ext === ".js" || ext === ".mjs") {
  name = "ESLint"; cmd = node; args = [path.join(root, "node_modules/eslint/bin/eslint.js"), "--no-warn-ignored", rel];
} else if (ext === ".css" && rel.startsWith("docs/stylesheets/")) {
  name = "Stylelint"; cmd = node; args = [path.join(root, "node_modules/stylelint/bin/stylelint.mjs"), rel];
} else if (ext === ".py" && rel.startsWith("tools/")) {
  name = "Ruff"; cmd = python(); args = ["-m", "ruff", "check", "--quiet", rel];
} else if (ext === ".md" && rel.startsWith("docs/")) {
  name = "unslop-prose"; cmd = python(); args = [path.join(root, "tools/unslop_prose/lint.py"), rel];
} else {
  process.exit(0);
}

const run = spawnSync(cmd, args, { cwd: root, encoding: "utf8", env: { ...process.env, PYTHONIOENCODING: "utf-8", NO_COLOR: "1", FORCE_COLOR: "0" } });
if (run.status === 0) process.exit(0);
const out = [run.stdout, run.stderr].filter(Boolean).join("\n").trim() || (run.error ? String(run.error) : "no output");
if (run.error || run.status === null) {
  // the linter did not start (not installed?): say so, but do not report it as a finding
  console.log(`lint hook: ${name} did not run on ${rel}: ${out}. Install with npm ci and pip install -r requirements-dev.txt.`);
  process.exit(0);
}
process.stderr.write(`${name} found problems in ${rel}. Fix them before you continue.\n\n${out}\n`);
process.exit(2);
