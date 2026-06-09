# GC Intraday SD Visualizer

Normal distribution visualizer for Gold Futures (GC) with intraday vol/OI overlay. Single HTML file, no build step, no dependencies.
https://0xtrvkc.github.io/Gold-OG-GC-intraday-oi-SD-Visualizer/

## What it does

- Plots a normal distribution centered on GC=F open price (auto-fetched)
- Overlays intraday call/put volume bars and open interest (hollow) bars per strike
- Shows ±1σ/2σ/3σ zones computed from IV × mean × √(DTE/365)
- SD gauge sidebar shows where the live future price sits relative to σ bands
- Vol zone: draw a ±1σ band at any price/IV combo you want
- Zoom + pan + scrollbar on the chart
- Light/dark theme

## Data sources

**Price** — `GC=F` open price via Yahoo Finance (`query1/query2.finance.yahoo.com`). Rotates through 3 CORS proxies (allorigins, corsproxy.io, thingproxy) since YF blocks direct browser requests. Falls back to localStorage cache if all proxies fail.

**Intraday vol + OI** — fetched from [`pageth/Vol2VolData`](https://github.com/pageth/Vol2VolData) on GitHub (raw text files). Two files:
- `IntradayData.txt` — per-strike call/put volume + IV smile for the current session
- `OIData.txt` — per-strike open interest

Both are CSV-ish with a header line containing future price, DTE, and totals. Auto-refreshes on a configurable interval (10s / 30s / 60s / 5min).

## Controls

| thing | what |
|---|---|
| Mean (μ) | auto = GC=F open. edit to override |
| Std Dev (σ) | auto-computed from IV smile at future price. toggle to manual if you want to plug in your own |
| ⟳ Auto / ✎ Manual | locks/unlocks the σ input |
| Price — Vol Zone | draw a ±σ band at a specific price. uses interpolated IV from the smile |
| Zoom / scroll | mousewheel to zoom, drag to pan, or use the scrollbar below the chart |
| Both / Intraday / OI | toggle which bars are visible |
| Stacked / Side-by-side | bar layout |

## Running it

Just open `index.html` in a browser. Everything is inline. CORS proxies handle the Yahoo Finance call — if they're all down the chart still loads with cached price.

No server needed. No npm. No nonsense.

## Notes

- Yahoo Finance CORS situation is a mess and always has been. If the price badge shows "cached" that's why, not a bug.
- The IV smile interpolation is linear between nearest strikes. Good enough for eyeballing levels.
- Strikes outside the current view are not drawn but data is still there — just zoom/pan out.
