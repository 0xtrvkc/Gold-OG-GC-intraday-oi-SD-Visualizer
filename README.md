# SD Visualizer · GC Intraday 

https://0xtrvkc.github.io/Gold-OG-GC-intraday-oi-SD-Visualizer/
A single-file, client-side dashboard for watching Gold Futures (GC) options flow through the trading day — intraday volume and open interest by strike, plotted against a normal-distribution ±3σ price curve, with session history, a DTE low-IV ladder, and a manual trade recorder.

No build step, no backend required. It's one `index.html` — open it in a browser or serve it as a static page (e.g. GitHub Pages).

## What it does

- **σ curve + strike bars** — plots the expected-move normal distribution (μ = gold futures price, σ = IV/16 × mean) alongside intraday volume and open-interest bars at each strike, so you can see where flow is clustering relative to the statistical zones.
- **Price / IV smile controls** — mean and σ can run in auto mode (live futures price, IV-derived expected distance) or be overridden manually; a "Price — Vol Zone" slider lets you probe implied vol at any price point along the smile.
- **Playback scrubber** — drag through the trading day to replay how the intraday/OI bars evolved, or jump back to live.
- **Session History charts** — time-series of futures price, IV, and call/put totals (intraday + OI) for the current session, restored from `localStorage` and backfilled from a public snapshot DB so history survives a refresh.
- **DTE Low-IV Ladder** — a small table showing the lowest available IV at each 0.1 DTE rung (1.0 → 0.0) for the day, matched from actual snapshots rather than interpolated.
- **Trade Recorder** — a manual log for marking trade Opens/Exits. See below.
- **Macro news box** — pulls short-form macro headlines relevant to gold from a companion JSON feed.
- Light/dark theme toggle, zoom/pan on the chart, and a PWA manifest so it can be added to a phone home screen.

## Trade Recorder

A lightweight, in-memory trade log built for fast entry during the session:

- **Save Open / Save Exit** are the only two buttons needed to log a row — no manual fields. Future price and timestamp are captured automatically from whatever the page is showing at that instant.
- Every row also snapshots the **entire options chain** at save time (intraday + OI call/put at every strike), not just totals — expandable per row via a "N strikes" toggle without cluttering the main table.
- **Open/Exit pairing** is automatic via a monotonic "Magic #"; if more than one position is open at once, a "Closing" dropdown appears so you can pick which one an Exit belongs to.
- **Editable after the fact**: Future Price (in case the auto-captured tick was stale) and a Win/Lose Result tag (Exit rows only) can both be corrected/filled in later, right in the table.
- **Strategy** (Mean Reverse / Recovery / Follow Squeeze / After Squeeze) and **Martingale step** (#1–#4) tags on Open rows, for classifying entries as you go.
- **Copy for Sheets** exports the whole log as tab-separated values, ready to paste into Google Sheets/Excel. Per-strike columns are built from the *union* of every strike seen across the session (the visible strike range drifts through the day), sorted and sparse-filled — rows that never saw a given strike just get a blank cell instead of a guessed value. Every exported cell is sanitized to strip `=` so nothing gets misread as a spreadsheet formula.
- Everything is in-memory only and clears on page refresh — meant to be copied out before you reload.

## Data sources

All data is fetched client-side from public raw files — no API keys required for normal use:

| Source | Purpose |
|---|---|
| `pageth/Vol2VolData` (`IntradayData.txt`, `OIData.txt`) | Live intraday volume + open interest by strike |
| `0xtrvkc/itd-oi-db` (`vol2vol.db`, read via [sql.js](https://sql.js.org/)) | Public snapshot history — backfills Session History charts and the DTE ladder across refreshes/devices |
| `0xtrvkc/BTC-Daily-Short-Call-Premium-Income-Checklist` (`macro.json`) | Macro news headlines |
| Yahoo/GC=F (via the app's gold price fetch) | Live gold futures price for the Mean (μ) auto value |

An optional **GitHub personal access token** (read-only, no scopes needed) can be entered in the header — it raises GitHub's unauthenticated API rate limit (60/hr → 5,000/hr) for the day's first-snapshot IV lookup. It's stored only in the browser's `localStorage` and sent only to `api.github.com`.

If a local `api.py` server is running on `localhost:5000`, the app will also opportunistically backfill session history from it (dev-only; silently skipped when unavailable, e.g. on GitHub Pages).

## Running it

Just open `index.html` in a browser. For the sql.js/History backfill and service-worker/manifest features to behave correctly, serving it over `http(s)` (e.g. `python3 -m http.server`, or GitHub Pages) is recommended over `file://`.

## Notes

- Everything — chart, history, DTE ladder, trade recorder — runs entirely in the browser. There is no server-side component required for normal operation.
- Session History and the Trade Recorder are two separate stores: history persists (localStorage + public DB backfill), the trade log is intentionally ephemeral (clears on refresh) since it's meant to be copied out per session.
