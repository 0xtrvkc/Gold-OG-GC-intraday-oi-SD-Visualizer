"""
vol2vol local API
─────────────────
Serves history from data/vol2vol.db so the SD Visualizer can
backfill its session-history charts from real recorded data.

Also serves index.html at / so you can open http://localhost:5000
instead of a file:// path (avoids CORS issues with the /history call).

Usage:
    python api.py
    # or with a custom db path / port:
    DB_PATH=data/vol2vol.db PORT=5000 python api.py

Endpoints:
    GET /                       → index.html
    GET /history?date=YYYY-MM-DD → JSON array of history points for that date
                                   defaults to today (local date)
    GET /history?date=today      → same as today
"""

import os
import sqlite3
import json
from datetime import datetime, timezone, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
DB_PATH   = os.environ.get("DB_PATH",   "data/vol2vol.db")
PORT      = int(os.environ.get("PORT",  5000))
HTML_FILE = os.environ.get("HTML_FILE", "index.html")

# ── DB query ──────────────────────────────────────────────────────────────────
def fetch_history(date_str: str) -> list[dict]:
    """
    Return one point per fetch-snapshot for the given UTC date.

    Each row in `intraday` represents one strike at one fetch time.
    We aggregate across strikes to get per-snapshot totals:
      - vol        : headline IV% (same for all strikes in a snapshot)
      - intraCall  : SUM(call)  — intraday call volume
      - intraPut   : SUM(put)   — intraday put volume
      - oiCall     : MAX(call_oi) — total OI calls (header field, same per snapshot)
      - oiPut      : MAX(put_oi)  — total OI puts
      - future     : MAX(future_price)

    fetched_at is stored as an ISO string with UTC offset, e.g.
    '2026-06-30T00:20:12.000373+00:00'. We filter by the date portion
    in UTC (matching how the DB was written).
    """
    if not Path(DB_PATH).exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH!r}. "
                                f"Run from the repo root or set DB_PATH env var.")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur  = conn.cursor()

    # Filter by UTC date — fetched_at starts with the date string
    day_start = f"{date_str}T00:00:00"
    day_end   = f"{date_str}T23:59:59.999999"

    cur.execute("""
        SELECT
            fetched_at,
            MAX(vol)          AS vol,
            SUM(call)         AS intraCall,
            SUM(put)          AS intraPut,
            MAX(call_oi)      AS oiCall,
            MAX(put_oi)       AS oiPut,
            MAX(future_price) AS future
        FROM intraday
        WHERE fetched_at >= ? AND fetched_at <= ?
        GROUP BY fetched_at
        ORDER BY fetched_at
    """, (day_start, day_end))

    rows = cur.fetchall()
    conn.close()

    points = []
    for r in rows:
        # Parse the ISO timestamp (with UTC offset) → epoch ms
        ts_str = r["fetched_at"]
        try:
            # Python 3.11+ handles +00:00 natively; for older versions strip offset
            if ts_str.endswith("+00:00"):
                ts_str_clean = ts_str[:-6]
                dt = datetime.fromisoformat(ts_str_clean).replace(tzinfo=timezone.utc)
            else:
                dt = datetime.fromisoformat(ts_str)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue  # skip malformed timestamp

        epoch_ms = int(dt.timestamp() * 1000)

        points.append({
            "t":         epoch_ms,
            "vol":       r["vol"],        # already a percentage-point number e.g. 31.74
            "intraCall": r["intraCall"],
            "intraPut":  r["intraPut"],
            "oiCall":    r["oiCall"],
            "oiPut":     r["oiPut"],
            "future":    r["future"],
        })

    return points


def today_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


# ── HTTP handler ──────────────────────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        # Cleaner console output
        print(f"  {self.address_string()} {fmt % args}")

    def send_json(self, data, status=200):
        body = json.dumps(data, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")  # allow file:// and localhost origins
        self.end_headers()
        self.wfile.write(body)

    def send_error_json(self, status, message):
        self.send_json({"error": message}, status=status)

    def do_OPTIONS(self):
        # Pre-flight CORS
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path   = parsed.path.rstrip("/") or "/"
        params = parse_qs(parsed.query)

        # ── GET / → serve index.html ─────────────────────────────────────────
        if path == "/":
            html_path = Path(HTML_FILE)
            if not html_path.exists():
                self.send_error_json(404, f"index.html not found at {HTML_FILE!r}")
                return
            body = html_path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        # ── GET /history ──────────────────────────────────────────────────────
        if path == "/history":
            date_param = params.get("date", [None])[0]
            if not date_param or date_param.lower() == "today":
                date_str = today_utc()
            else:
                # Validate format
                try:
                    datetime.strptime(date_param, "%Y-%m-%d")
                    date_str = date_param
                except ValueError:
                    self.send_error_json(400, "Invalid date format. Use YYYY-MM-DD or 'today'.")
                    return

            try:
                points = fetch_history(date_str)
                self.send_json({"date": date_str, "points": points, "count": len(points)})
            except FileNotFoundError as e:
                self.send_error_json(503, str(e))
            except Exception as e:
                self.send_error_json(500, f"Query failed: {e}")
            return

        self.send_error_json(404, f"Unknown path: {path!r}")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"vol2vol API")
    print(f"  DB:   {DB_PATH}")
    print(f"  HTML: {HTML_FILE}")
    print(f"  http://localhost:{PORT}")

    # Ensure fetched_at index exists — keeps day queries fast even at 10yr+ scale.
    # CREATE INDEX IF NOT EXISTS is a no-op if the index already exists.
    if Path(DB_PATH).exists():
        try:
            _conn = sqlite3.connect(DB_PATH)
            _conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_intraday_fetched_at "
                "ON intraday (fetched_at)"
            )
            _conn.commit()
            _conn.close()
            print(f"  index: idx_intraday_fetched_at OK")
        except Exception as e:
            print(f"  index: could not create ({e})")

    print()

    server = HTTPServer(("127.0.0.1", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped.")
