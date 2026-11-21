"""Offline simulation + local HTTP dashboard. Standard library only."""
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from html import escape
import json
from pathlib import Path
import random
import sqlite3
import threading
import time

from scada_sim.core import AlarmEvaluator, simulate_reading

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "measurements.sqlite3"
IDS = ("T-01", "T-02", "T-03")
state_lock = threading.Lock()
latest = {}
stop_event = threading.Event()

def open_database():
    DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS measurements (
        timestamp_utc TEXT NOT NULL,
        turbine_id TEXT NOT NULL,
        cycle INTEGER NOT NULL,
        wind_speed REAL NOT NULL,
        power_kw REAL NOT NULL,
        online INTEGER NOT NULL,
        alarm INTEGER NOT NULL
    )""")
    conn.commit()
    return conn

def run_simulation():
    rng = random.Random(42)
    evaluator = AlarmEvaluator(missed_cycles_threshold=3)
    conn = open_database()
    cycle = 0
    try:
        while not stop_event.is_set():
            cycle += 1
            stamp = datetime.now(timezone.utc).isoformat()
            updates = {}
            for turbine_id in IDS:
                reading = simulate_reading(turbine_id, cycle, rng)
                alarm = evaluator.evaluate(reading)
                updates[turbine_id] = {
                    "timestamp_utc": stamp,
                    "turbine_id": turbine_id,
                    "wind_speed": reading.wind_speed,
                    "power_kw": reading.power_kw,
                    "online": reading.online,
                    "alarm": alarm,
                    "missed_cycles": evaluator.missed[turbine_id],
                }
                conn.execute(
                    "INSERT INTO measurements VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (stamp, turbine_id, cycle, reading.wind_speed,
                     reading.power_kw, int(reading.online), int(alarm)),
                )
            conn.commit()
            with state_lock:
                latest.update(updates)
            stop_event.wait(1)
    finally:
        conn.close()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/turbines":
            with state_lock:
                payload = json.dumps({"turbines": list(latest.values())}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
        elif self.path == "/":
            payload = (ROOT / "dashboard" / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
        else:
            self.send_error(404, "Not found")
            return
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

def main():
    worker = threading.Thread(target=run_simulation, daemon=True)
    worker.start()
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("Local dashboard: http://127.0.0.1:8000")
    print("Demo only. No real turbine or SCADA connection.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        stop_event.set()
        server.server_close()
        worker.join(timeout=3)

if __name__ == "__main__":
    main()
