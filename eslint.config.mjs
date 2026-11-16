// ESLint: the wiki's browser scripts (docs/javascripts) and the Node test scripts (tests).
// Run with `npm run lint:js`. The browser scripts are plain ES5-style files with no build step.
import js from "@eslint/js";
import globals from "globals";

export default [
  { ignores: ["site/**", "node_modules/**", ".venv/**", ".cache/**", ".claude/**", ".lighthouseci/**", "tests/reports/**", "docs/assets/**"] },
  js.configs.recommended,
  {
    files: ["docs/javascripts/**/*.js"],
    languageOptions: { ecmaVersion: 2020, sourceType: "script", globals: { ...globals.browser } },
    rules: {
      "no-unused-vars": ["error", { args: "none", caughtErrors: "none" }],
      "no-empty": ["error", { allowEmptyCatch: true }],
      "no-implicit-globals": "error",
      "no-prototype-builtins": "off",
    },
  },
  {
    files: ["tests/**/*.mjs", "*.mjs"],
    // the test scripts also hold functions that run inside the page (page.evaluate), so browser names are known too
    languageOptions: { ecmaVersion: 2023, sourceType: "module", globals: { ...globals.node, ...globals.browser } },
    rules: { "no-unused-vars": ["error", { args: "none", caughtErrors: "none" }], "no-empty": ["error", { allowEmptyCatch: true }] },
  },
];
