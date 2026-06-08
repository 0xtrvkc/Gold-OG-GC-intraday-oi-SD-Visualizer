# GC intraday OI + SD visualizer

live: https://0xtrvkc.github.io/Gold-OG-GC-intraday-oi-SD-Visualizer/

plots gold futures options volume, open interest, and IV smile on top of a normal distribution centered on the future price. auto-refreshes.

single html file, no build, no deps, just open it.

---

**what's on the chart**

- bell curve centered on future price, σ = `IV × price × √(DTE/252)`
- ±1/2/3σ lines color coded (red/orange/yellow)
- call/put volume bars per strike
- OI as hollow outlines over the volume bars
- IV smile curve
- blue dashed line = future price with its own ±1σ zone
- red zone = manually placed vol band at whatever strike/IV you set
- expected move arrow along the bottom

**controls**

- mean defaults to future price, override if you want
- σ is auto but you can type in your own
- vol zone slider snaps to 00/25/50/75, IV auto-interpolates from smile
- scroll to zoom, drag to pan

**data**

pulls from [pageth/Vol2VolData](https://github.com/pageth/Vol2VolData) — `IntradayData.txt` for volume/IV/future price and `OIData.txt` for open interest. no api key needed, just raw github files.

---

```bash
git clone https://github.com/0xtrvkc/Gold-OG-GC-intraday-oi-SD-Visualizer.git
open index.html
```
