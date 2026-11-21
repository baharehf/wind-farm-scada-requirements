
"""Tests for the SCADA Modbus monitoring requirements."""

import unittest
from unittest.mock import patch, MagicMock

from scada_sim.app import read_modbus_turbine
from scada_sim.core import AlarmEvaluator, Reading

class TestModbusCommunication(unittest.TestCase):

    @patch("scada_sim.app.ModbusTcpClient")
    def test_successful_modbus_read(self, mock_client_class):
        """FR-06: Read valid measurements through Modbus."""

        mock_client = MagicMock()
        mock_client.connect.return_value = True
        mock_client.read_holding_registers.return_value.registers = [
            95, 850, 1
        ]
        mock_client.read_holding_registers.return_value.isError.return_value = False
        mock_client_class.return_value = mock_client

        result = read_modbus_turbine()

        self.assertEqual(result["wind_speed"], 9.5)
        self.assertEqual(result["power_kw"], 850)
        self.assertTrue(result["online"])

        mock_client.close.assert_called_once()

    @patch("scada_sim.app.ModbusTcpClient")
    def test_connection_failure(self, mock_client_class):
        """FR-07: Detect a failed Modbus connection."""

        mock_client = MagicMock()
        mock_client.connect.return_value = False
        mock_client_class.return_value = mock_client

        result = read_modbus_turbine()

        self.assertIsNone(result)
        mock_client.close.assert_called_once()

    @patch("scada_sim.app.ModbusTcpClient")
    def test_modbus_error_response(self, mock_client_class):
        """FR-07: Detect an invalid Modbus response."""

        mock_client = MagicMock()
        mock_client.connect.return_value = True
        mock_client.read_holding_registers.return_value.isError.return_value = True
        mock_client_class.return_value = mock_client

        result = read_modbus_turbine()

        self.assertIsNone(result)
        mock_client.close.assert_called_once()


class TestCommunicationRequirements(unittest.TestCase):
    """Verify alarm activation and recovery behaviour."""

    def test_fr07_alarm_after_three_failures(self):
        """FR-07: Alarm after three missed polling cycles."""
        evaluator = AlarmEvaluator(missed_cycles_threshold=3)

        offline = Reading(
            turbine_id="T-01",
            cycle=1,
            wind_speed=0.0,
            power_kw=0.0,
            online=False,
        )

        self.assertFalse(evaluator.evaluate(offline))
        self.assertFalse(evaluator.evaluate(offline))
        self.assertTrue(evaluator.evaluate(offline))

    def test_fr10_alarm_clears_after_recovery(self):
        """FR-10: Alarm clears after communication recovery."""
        evaluator = AlarmEvaluator(missed_cycles_threshold=3)

        offline = Reading("T-01", 1, 0.0, 0.0, False)
        online = Reading("T-01", 2, 8.5, 700.0, True)

        for _ in range(3):
            evaluator.evaluate(offline)

        self.assertTrue(evaluator.evaluate(offline))
        self.assertFalse(evaluator.evaluate(online))
        self.assertEqual(evaluator.missed["T-01"], 0)

if __name__ == "__main__":
    unittest.main()
