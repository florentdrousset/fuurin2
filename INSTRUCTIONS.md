Fuurin project - Working instructions and history

Owner intent (from 2025-08-28):
- Build a Japanese learning and reading progress tracking site (early prototype from v0).
- Later add HTMX/Alpine interactivity and eventually a backend.
- Keep an instructions/history file to stay organized.
- Extract all inline CSS from the HTML pages into a single reusable CSS library.

Decisions (2025-08-28):
1) CSS consolidation
   - Created styles.css at repo root as the single source of truth for styles used by index.html, dashboard.html, and activity-feed.html.
   - Centralized: resets, layout, navigation, sidebar, cards, tables, charts, heatmap, progress, streak, tabs/controls/actions, and common variables via CSS custom properties.
   - Linked styles.css in each HTML <head>. Remaining inline style attributes for dynamic widths/heights (e.g., bar-fill height, progress-fill width) were left as inline style attributes because they represent data-driven or component-state values; they can later be driven by HTMX/Alpine.

2) Utility and variables
   - Introduced CSS variables for colors and spacing shades to make editing easier. Future design changes can be applied by updating variables.

3) HTMX partial navigation (2025-08-28)
   - Added HTMX (CDN) to all pages and enabled hx-boost on <body> so link clicks fetch new pages via AJAX.
   - Set hx-target="#content" (the <main> on each page) and hx-select="main.main-content > .content-wrapper" so only the inner content swaps, keeping top nav and sidebar.
   - Enabled hx-push-url="true" for proper browser history/back/forward.
   - Added a small script to update the active nav item after swaps and on popstate.
   - Made the heatmap script idempotent and also trigger on htmx:afterSwap so it renders when arriving via HTMX.

4) HTMX loading policy (2025-08-28)
   - Current: Local vendored copy at assets/js/htmx.min.js (version 1.9.12) loaded with defer.
   - Rationale: Offline capability, no external dependency, predictable load.
   - Note: Serve the site over http(s) (e.g., python -m http.server) for HTMX fetch to work reliably; file:// may block XHR in some browsers.

5) Next steps (suggested)
   - Add transition effects for swaps (e.g., hx-swap="innerHTML transition:true").
   - Consider extracting the nav-active updater into a small JS file shared by all pages.
   - Later, return server-side fragments with only .content-wrapper to reduce payload.

Changelog:
 - 2025-08-28: Added styles.css and linked it in all pages. Added this INSTRUCTIONS.md.
 - 2025-08-28: Removed all inline <style> blocks from index.html, dashboard.html, and activity-feed.html; all styles are now in styles.css. Replaced remaining inline style attributes with utility classes (e.g., w-xx, h-xx, bg-xx, flex utilities).
 - 2025-08-28: Restored missing styles for index.html bottom grid (Recent Achievements, Goals, Quick Actions) by adding .bottom-grid and achievement/goal/action classes to styles.css.
 - 2025-08-28: Integrated HTMX partial navigation with preserved layout, active nav syncing, and heatmap re-init after swaps.
 - 2025-08-28: Switched HTMX to a local vendored copy (assets/js/htmx.min.js) and removed CDN dependency.
- 2025-08-28: Added a micro chart helper (assets/js/fuurin-charts.js) and wired the Weekly Study Time bars to data-attributes for clean rendering/animation after HTMX swaps. Added data-max="100" to Weekly Study Time to match baseline percentages exactly.
