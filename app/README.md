# Radar app prototype

A clickable prototype of the Radar app, with Echo (the Rive bat) living inside it. Everything runs in the browser on sample data. There is no backend.

## What you can do

- **Onboarding.** Paste a website (or pick a sample), watch Echo "read" it, confirm the profile, set a range on the map, choose alerts, and land in a backfilled Radar. A custom domain is guessed into a business type: "acmeplumbing.com" becomes a plumber.
- **Radar (home).** KPIs, a live feed that gets a new lead every few seconds, filters (hot, asking now, switching, records and news), sort, search (press `/`), a mini map, top areas and sources.
- **Lead details.** The original post, a heat score breakdown, why Echo flagged it, and an AI reply draft. You can switch tone (friendly, professional, short), copy it, mark the lead won (with a job value and confetti) or not a fit (with a reason).
- **Pipeline.** Drag and drop between New, Contacted, Quoted, Won and Lost, with totals and win rate. Works with touch too.
- **Map.** Drag your shop pin or the range ring. Hover a dot for the post, or click it to open the lead. The internet provider sample switches to a nationwide map.
- **Insights.** Return on Radar, leads per day (hot vs. other), sources, funnel and cumulative revenue. Each chart has hover tooltips and a table view.
- **Settings.** Business profile and services, range plus Territory Lock, alerts, integrations (pretend), plan usage, theme, and demo controls: switch business, replay setup, reset.
- **Ask Echo.** A scripted chat (press `E`). Echo flies into the chat, thinks, types and shows lead cards.
- **Echo everywhere.** One live Rive instance flies between the onboarding stage, the sidebar, the chat, the lead drawer on mobile and empty states. It reacts to events: found, pointing at the drawer, typing while drafting, celebrating wins, and dozing off after 45 seconds of inactivity.

## Run it

Serve the repo root so the app can reach the shared Rive runtime in `site/`:

```sh
python3 -m http.server 8000
# open http://localhost:8000/app/
```

## Edit and rebuild

Edit `src/app.html`, then run:

```sh
python3 app/build.py
```

The build reuses Echo's assets from `site/assets/` (Rive file plus SVG fallback rig) and writes `index.html`, which loads `../site/rive.wasm`. To host the app on its own, run `python3 app/build.py --fragment out.html` for a copy that expects `rive.wasm` next to it.

## Notes

- State (onboarding done, pipeline moves, settings) is kept in your browser's localStorage. Settings → Appearance → Reset demo data clears it.
- Charts follow a colorblind-checked palette (validated for light and dark), with thin marks, one axis per chart, a legend for 2+ series, and a table view for every chart.
- Radar never posts for the user. Replies are copied and posted by a person, which matches the compliance approach in the kickoff book.
