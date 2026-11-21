# Acceptance criteria and test scenarios

| Requirement | Given | When | Then |
|---|---|---|---|
| FR-01 | The simulator is running | One cycle elapses | A reading is generated for T-01, T-02 and T-03 |
| FR-02 | Recent data is available | The browser refreshes | Current values and status are displayed for each turbine |
| FR-03 | A turbine previously reported normally | Three consecutive cycles have no report | The communication-loss alarm becomes active |
| FR-04 | A communication-loss alarm is active | The turbine reports successfully | The alarm clears on that cycle |
| FR-05 | The simulator is running | Measurements are produced | Rows with timestamps and state are stored in SQLite |

## Manual verification
1. Run `python -m scada_sim.app`.
2. Visit http://127.0.0.1:8000.
3. Observe T-02 transition through offline/no-alarm to communication alarm.
4. Confirm its alarm clears when it resumes reporting.
5. Run `python -m unittest discover -s tests -v` and confirm tests pass.

Important: these are project-level acceptance scenarios, not validated operational SCADA acceptance criteria.

## Modbus TCP Acceptance Criteria

| ID | Given | When | Then |
|---|---|---|---|
| FR-06 | The Modbus server is running | The application polls T-01 | The latest measurements are received |
| FR-07 | T-01 is communicating normally | Three consecutive polling attempts fail | A communication-loss alarm is activated |
| FR-08 | Modbus communication is unavailable | The dashboard refreshes | Current measurements display N/A and quality is COMMUNICATION_LOST |
| FR-09 | A valid measurement was received | Communication is subsequently lost | The last valid measurement and timestamp remain visible |
| FR-10 | A communication-loss alarm is active | A valid Modbus response is received | The alarm clears and data quality returns to GOOD |
