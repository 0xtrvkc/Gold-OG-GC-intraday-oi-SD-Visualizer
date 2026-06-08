# Gold / GC Intraday OI — Standard Deviation Visualizer

A live, browser-based chart for Gold Futures (GC) that overlays intraday options volume, open interest, and implied volatility onto a normal distribution centered on the future price.

**Live:** https://0xtrvkc.github.io/Gold-OG-GC-intraday-oi-SD-Visualizer/

---

## What it does

The chart pulls live intraday data from [Vol2Vol](https://github.com/pageth/Vol2VolData) and plots:

- A **normal distribution bell curve** centered on the future price (μ), with σ calculated from IV and DTE
- **±1σ / ±2σ / ±3σ zone lines** with color-coded labels at the top of the chart
- **Call and put volume bars** per strike (blue = calls, yellow = puts)
- **Open interest bars** as hollow outlines over the volume bars (red = OI puts, green = OI calls)
- **Implied volatility smile curve** across the strike range
- **Future price line** (dashed blue) with its own ±1σ zone derived from smile-interpolated IV
- **Vol Zone** — a configurable ±σ band around any price you choose, using IV at that strike
- **Expected move arrow** at the baseline showing ±move in price units
- **Stats bar** showing exact μ±1/2/3σ price levels, total call/put volume, and IV

---

## Controls

| Control | What it does |
|---|---|
| **Mean (μ)** | Auto-set to the future price. Type to override; reset button restores it. |
| **Std Dev (σ)** | Auto-calculated as `IV × Mean × √(DTE/252)`. Override manually if needed. |
| **Auto-Refresh** | Polling interval — 10s, 30s, 60s, or 5 min. |
| **Price — Vol Zone** | Slider to place the red ±σ zone at any strike. Snaps to 00/25/50/75. |
| **Vol at Price (%)** | IV used for the vol zone. Auto-interpolated from the smile; editable. |
| **Zoom +/−/Reset** | Zoom in/out on the x-axis. Also scroll-to-zoom and drag-to-pan. |

---

## Chart elements

```
─────────────────────────────────────────────
 −3σ  −2σ  −1σ    μ   +1σ  +2σ  +3σ        ← labels at top
 │    │    │      │    │    │    │
 │    │    │  ╭───╮    │    │    │           ← bell curve
 │    │    │ ╱     ╲   │    │    │
 │   ▐▌   ▐▌▐▌   ▐▌▐▌  ▐▌   │              ← call/put bars
─────────────────────────────────────────────
 3250 3275 3300 3325 3350 ...               ← price axis
```

- **Solid colored verticals** — σ level lines (red=±1σ, orange=±2σ, yellow=±3σ)
- **Blue dashed vertical** — current future price
- **Hollow bar outlines** — open interest (red outline = puts, green outline = calls)
- **Purple curve** — implied volatility smile
- **Red shaded zone** — vol zone at your selected price ± one σ

---

## Data source

Data is fetched from [`pageth/Vol2VolData`](https://github.com/pageth/Vol2VolData) on GitHub — two files updated intraday:

- `IntradayData.txt` — strike-level call/put volume, IV smile, future price, DTE
- `OIData.txt` — strike-level open interest for calls and puts

No API key or server required. Runs entirely in the browser.

---

## Usage

Open the live link above, or clone and open `index.html` directly:

```bash
git clone https://github.com/0xtrvkc/Gold-OG-GC-intraday-oi-SD-Visualizer.git
cd Gold-OG-GC-intraday-oi-SD-Visualizer
open index.html
```

No build step. No dependencies. Single HTML file.

---

## Keyboard / mouse shortcuts

| Action | How |
|---|---|
| Zoom in/out | Scroll wheel over chart |
| Pan left/right | Click and drag |
| Pinch zoom | Two-finger pinch (mobile) |
| Force refresh | Click **↺ Refresh** button |
