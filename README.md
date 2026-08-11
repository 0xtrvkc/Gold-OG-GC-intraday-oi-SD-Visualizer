https://0xtrvkc.github.io/Gold-OG-GC-intraday-oi-SD-Visualizer/
# SD Visualizer · GC Intraday

A single-file, no-backend dashboard for visualizing Gold futures (GC) options
activity against a normal distribution. It plots intraday volume and open
interest by strike, overlays ±3σ zones, and tracks how price behaves relative
to those zones through the trading day.

Everything lives in one `index.html` — no build step, no server. Open it in
a browser and it pulls live data straight from GitHub-hosted sources.

## Features

- **Normal distribution chart** — empirical rule (68–95–99.7) bands, ±3σ
  zones, minor/major gridlines, centered on the computed mean.
- **Intraday volume & OI overlay** — calls/puts by strike, toggle between
  Both / Intraday only / OI only.
- **Sigma gauge** — shows where the current future price sits relative to
  the distribution (e.g. "+1σ → +2σ, 40% from +1σ").
- **Vol Zone** — an optional ±σ band computed from a price/vol you enter
  yourself, independent of the live future price.
- **Auto / manual σ mode** — auto-computed standard deviation from live
  data, or override it manually.
- **Big Chart Playback** — scrub or auto-play back through the day's
  intraday/OI snapshots instead of only viewing the live state.
- **History charts** — time-series views of key metrics through the day,
  with the same scrub/playback controls.
- **DTE ladder** — snapshot matching across a fixed set of days-to-expiry
  rungs (1.0 → 0.0 in 0.1 steps), so you can compare the same underlying
  setup at different points in its life.
- **Trade Recorder** *(currently hidden — see [Known issues](#known-issues))*
  — logs Open/Exit trades with the full option-chain snapshot at save time,
  including an "At Time" backfill mode that matches a picked clock time to
  the closest historical snapshot. Exports as tab-separated data via
  "Copy for Sheets" for pasting straight into Google Sheets.
- **Light/dark theme toggle.**

## Data sources

| Source | What | Where |
|---|---|---|
| `pageth/Vol2VolData` | Live `IntradayData.txt` / `OIData.txt` — current snapshot, fetched directly | `raw.githubusercontent.com` |
| `pageth/Vol2VolData` commit history | Historical OI snapshots (via commit log + raw blob fetch per commit) | `api.github.com` |
| `0xtrvkc/itd-oi-db` | `data/vol2vol.db` — a SQLite log of intraday + OI snapshots polled every 5 min, used for Big Chart Playback, History charts, DTE ladder, and Trade Recorder At-Time backfill | `raw.githubusercontent.com`, parsed client-side with [sql.js](https://github.com/sql-js/sql.js) |

An optional GitHub personal access token (read-only, no scopes needed) can
be entered in the UI to raise the `api.github.com` rate limit from 60/hr to
5,000/hr for commit-history lookups. It's stored only in the browser's
`localStorage` and is never sent anywhere except `api.github.com`.

## Known issues

- **Trade Recorder is currently hidden** (`#trade-recorder-section` is
  `display:none` in `index.html`). The upstream `itd-oi-db` intraday
  snapshot feed silently stopped updating for a stretch, which broke
  At-Time backfill matching. The section's markup/JS is untouched — remove
  the `display:none` once the upstream feed is confirmed healthy again.

## Usage

Just open `index.html` in a browser — no install, no dependencies to run
locally. All computation happens client-side.

## Related repo

The snapshot database this dashboard reads (`data/vol2vol.db`) is produced
by a separate scheduled fetcher: [0xtrvkc/itd-oi-db](https://github.com/0xtrvkc/itd-oi-db).
