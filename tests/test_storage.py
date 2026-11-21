import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from scada_sim import app

class TestStorage(unittest.TestCase):
    def test_persistence(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(app, "DB", Path(tmp) / "measurements.sqlite3"):
                conn = app.open_database()
                conn.execute("INSERT INTO measurements VALUES (?, ?, ?, ?, ?, ?, ?)",
                            ("2026-11-21T12:00:00+00:00", "T-01", 1, 8.3, 600, 1, 0))
                conn.commit()
                n = conn.execute("SELECT COUNT(*) FROM measurements").fetchone()[0]
                conn.close()
                self.assertEqual(n, 1)
