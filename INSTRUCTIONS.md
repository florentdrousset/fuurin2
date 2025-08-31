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
 - 2025-08-31: Centralized client scripts in SvelteKit layout (+layout.svelte) so all routes include /assets/js/htmx.min.js and /assets/js/fuurin-charts.js; removed per-page script includes from home and activity feed to avoid double-loading. Moved active-nav updater to layout so it works on all routes. Updated answer: migration to SvelteKit is operational for /, /dashboard, /activity-feed. Dev: npm run dev; Build: npm run build; Preview: npm run preview.

Migration to SvelteKit (2025-08-29):
- Introduced a minimal SvelteKit setup to run the app as a proper SPA/SSR app.
- Key files added:
  - package.json: scripts now use svelte-kit build/preview; dev uses vite dev.
  - svelte.config.js with @sveltejs/adapter-auto.
  - vite.config.ts with sveltekit plugin.
  - tsconfig.json extending @sveltejs/kit/tsconfig.
  - src/routes/+layout.svelte imports src/app.css which @imports existing styles.css.
  - src/routes/+page.svelte (home), src/routes/dashboard/+page.svelte, src/routes/activity-feed/+page.svelte created by porting the corresponding HTML pages.
  - static/assets/js contains vendored htmx.min.js stub and fuurin-charts.js for client scripts.
- Asset strategy:
  - CSS: We keep styles.css at repo root and import it inside src/app.css to avoid large refactors. All pages inherit the styling via the root layout.
  - JS: Client-side scripts are served from /assets/js via the static/ directory; references updated to absolute paths (e.g., /assets/js/htmx.min.js).
- Routing changes:
  - Links updated to SvelteKit routes: "/", "/dashboard", "/activity-feed".
  - Active-nav updater script adapted to use pathname rather than .html filenames.
- How to run locally:
  1) Install deps: npm install
  2) Dev server: npm run dev (default http://localhost:5173)
  3) Build: npm run build
  4) Preview production build: npm run preview (default http://localhost:4173)
- Docker image:
  - Dockerfile added for multi-stage build. Build and run:
    - docker build -t fuurin2 .
    - docker run -it --rm -p 3000:3000 fuurin2
  - The container exposes port 3000 (SvelteKit build with adapter-auto selects Node adapter in container).
- Notes:
  - The vendored htmx.min.js in static is a lightweight stub that only fires htmx lifecycle events used by our inline scripts; replace with the official htmx when needed.
  - Static assets must live under static/ to be served by SvelteKit at runtime. We duplicated assets/js there; keep root copies for history if needed or remove later.


Démarrage rapide (SvelteKit) — FR (2025-08-29):
- Prérequis: Node.js 18+ (recommandé Node 20+), npm. Vérifiez avec: node -v, npm -v.

Lancer en local (développement):
1) npm install
2) npm run dev
   - Ouvrez: http://localhost:5173

Build et aperçu production:
1) npm run build
2) npm run preview
   - Ouvrez: http://localhost:4173

Avec Docker (production):
1) docker build -t fuurin2 .
2) docker run -it --rm -p 3000:3000 fuurin2
   - Ouvrez: http://localhost:3000

Avec Docker Compose — le plus simple:
1) docker compose up --build
   - Ouvrez: http://localhost:3000
2) Arrêter: docker compose down
3) Changer de port: éditez docker-compose.yml (ports: "3001:3000") ou lancez avec: docker compose run -p 3001:3000 web

Notes Windows / Dépannage:
- Si “npm n’est pas reconnu”: installez Node.js depuis https://nodejs.org/, rouvrez votre terminal PowerShell.
- Pare-feu Windows: acceptez l’invite lors du premier lancement pour permettre l’écoute locale.
- Port déjà utilisé: changez de port (dev: npm run dev -- --port=5174 ; preview: npm run preview -- --port=4174 ; docker: mappez un autre port, ex. -p 3001:3000).
- OneDrive: les chemins OneDrive fonctionnent; évitez les caractères spéciaux non ASCII dans les noms de dossier si vous rencontrez des soucis.
- htmx: une version “stub” est servie depuis /assets/js pour ce prototype; remplacez-la par la version officielle si vous avez besoin de la navigation boostée.
