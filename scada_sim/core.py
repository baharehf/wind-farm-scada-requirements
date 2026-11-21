"""Pure logic for simulated turbines and a simple communication-loss alarm."""
from dataclasses import dataclass
import math
import random

@dataclass(frozen=True)
class Reading:
    turbine_id: str
    cycle: int
    wind_speed: float
    power_kw: float
    online: bool

def simulate_reading(turbine_id: str, cycle: int, rng: random.Random) -> Reading:
    """Generate plausible demo values, not an engineering turbine power model."""
    online = not (turbine_id == "T-02" and cycle % 20 in range(9, 15))
    wind_speed = round(max(0.0, 8 + 2 * math.sin(cycle / 4) + rng.uniform(-1, 1)), 2)
    power_kw = round(min(2000, (wind_speed / 12) ** 3 * 2000), 2) if online else 0.0
    return Reading(turbine_id, cycle, wind_speed, power_kw, online)

class AlarmEvaluator:
    """Raise an alarm after a configurable number of consecutive missed cycles."""
    def __init__(self, missed_cycles_threshold: int = 3):
        if missed_cycles_threshold < 1:
            raise ValueError("threshold must be >= 1")
        self.threshold = missed_cycles_threshold
        self.missed = {}

    def evaluate(self, reading: Reading) -> bool:
        self.missed[reading.turbine_id] = (
            0 if reading.online else self.missed.get(reading.turbine_id, 0) + 1
        )
        return self.missed[reading.turbine_id] >= self.threshold
