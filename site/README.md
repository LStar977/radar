# Radar website

Interactive marketing site for Radar, starring Echo, the bat companion animated in Rive.

## What's on the page

- **Hero sonar.** Click anywhere in the dark to send a ping. The ring reveals hidden customer posts, and Echo reacts when it finds one.
- **Echo flies with you.** A single live Rive instance flies between "perches" in each section. Its eyes follow the cursor, it changes animation for each section, and tapping it makes it react.
- **Business picker.** Choose Electrician, Plumber, Roofer, Café, Dentist or Internet provider, and the rest of the page updates to match.
- **How it works.** A scroll-driven, four-step story: setup, scan, signals and reply.
- **Range map.** Drag the shop pin or the ring around Chicago, or switch to the nationwide view.
- **Meet Echo.** Buttons that play Echo's animations, plus a talk mode.
- Pricing toggle, bento features and a confetti finale.

## Run it locally

```sh
python3 -m http.server 8000 --directory site
# open http://localhost:8000
```

Opening `index.html` straight from disk also works, but serving it over HTTP matches production.

## Edit and rebuild

Edit `src/page.html`, then run:

```sh
python3 site/build.py
```

The build inlines `assets/echo.riv` (base64) and the SVG fallback rig from `assets/echo.svg` into `index.html`.

## Deploy

Upload `index.html` and `rive.wasm` together to any static host (Netlify, Vercel, GitHub Pages, Cloudflare Pages). The Rive runtime script loads from unpkg (`@rive-app/canvas@2.44.0`), and the page points it at the local `rive.wasm`.

## Echo and Rive

- `assets/echo.riv` is the character file, originally exported as "Muse". The artboard and state machine inside it are still named `Muse` and `MuseController`; the page uses those names, and visitors only see "Echo".
- Controls come from the `MuseController` view model: `mode` (0 to 19), `lookX`, `lookY`, `speaking` and `replay`.
- If a browser can't run Rive (no WebAssembly, or the runtime is blocked), the page swaps in an SVG version of Echo built from `assets/echo.svg`, with CSS animations for the main modes.
- With reduced motion turned on, Echo stops flying, pings and the marquee stop, and celebrations are toned down.

All businesses, posts and numbers on the page are samples.
