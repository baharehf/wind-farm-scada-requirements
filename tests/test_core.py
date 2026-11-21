import random
import unittest
from scada_sim.core import Reading, AlarmEvaluator, simulate_reading

class TestSimulation(unittest.TestCase):
    def test_simulator_ids(self):
        for turbine in ("T-01", "T-02", "T-03"):
            reading = simulate_reading(turbine, 1, random.Random(42))
            self.assertEqual(turbine, reading.turbine_id)

    def test_alarm_after_three_misses(self):
        e = AlarmEvaluator(3)
        offline = Reading("T-02", 1, 7.0, 0.0, False)
        self.assertFalse(e.evaluate(offline))
        self.assertFalse(e.evaluate(offline))
        self.assertTrue(e.evaluate(offline))

    def test_alarm_clears_on_recovery(self):
        e = AlarmEvaluator(3)
        offline = Reading("T-02", 1, 7.0, 0.0, False)
        for _ in range(3):
            e.evaluate(offline)
        self.assertTrue(e.missed["T-02"] >= 3)
        self.assertFalse(e.evaluate(Reading("T-02", 2, 8.0, 300.0, True)))
        self.assertEqual(e.missed["T-02"], 0)

    def test_invalid_threshold(self):
        with self.assertRaises(ValueError):
            AlarmEvaluator(0)
