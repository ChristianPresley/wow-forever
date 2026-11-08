/* Forever Codex: small progressive enhancements.
   Runs on every page view, including instant-navigation swaps (document$). */

/* Ctrl/Cmd+K opens search, matching the docs-site convention */
document.addEventListener("keydown", function (e) {
  if ((e.ctrlKey || e.metaKey) && !e.altKey && e.key.toLowerCase() === "k") {
    var toggle = document.querySelector('[data-md-toggle="search"]');
    if (!toggle) return;
    e.preventDefault();
    toggle.checked = true;
    toggle.dispatchEvent(new Event("change"));
    var input = document.querySelector(".md-search__input");
    if (input) setTimeout(function () { input.focus(); }, 0);
  }
});

document$.subscribe(function () {
  /* Scrollable tables become labelled, keyboard-focusable regions (Safari doesn't auto-focus scrollers) */
  document.querySelectorAll(".md-typeset__scrollwrap").forEach(function (wrap) {
    if (wrap.scrollWidth > wrap.clientWidth + 1) {
      var heading = null, el = wrap;
      while (el && !heading) {
        var prev = el.previousElementSibling;
        while (prev && !/^H[2-4]$/.test(prev.tagName)) prev = prev.previousElementSibling;
        if (prev) heading = prev; else el = el.parentElement;
        if (el && el.classList && el.classList.contains("md-content__inner")) break;
      }
      var label = heading ? heading.textContent.replace(/\s*¶\s*$/, "").trim() : "Table";
      wrap.tabIndex = 0;
      wrap.setAttribute("role", "region");
      wrap.setAttribute("aria-label", label.slice(0, 60) + " (scrollable table)");
    } else {
      wrap.removeAttribute("tabindex");
      wrap.removeAttribute("role");
      wrap.removeAttribute("aria-label");
    }
  });
});
