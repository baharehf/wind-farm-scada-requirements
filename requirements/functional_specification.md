# Functional specification, version 0.1

## Assumptions
This demonstration uses one-second reporting cycles and declares a communication-loss alarm after three consecutive missed cycles. These choices are illustrative and require stakeholder agreement for real systems.

| ID | Functional requirement | Source |
|---|---|---|
| FR-01 | The simulator shall produce one reading per cycle for each of three named turbines. | STK-01 |
| FR-02 | The dashboard shall display the latest wind speed, power estimate, connection status and timestamp for each turbine. | STK-01 |
| FR-03 | The alarm evaluator shall raise a communication-loss alarm when a turbine has failed to report for three consecutive simulated cycles. | STK-02 |
| FR-04 | The alarm evaluator shall clear the communication-loss alarm after a valid report from the turbine. | STK-02 |
| FR-05 | The application shall persist each simulated reading and its alarm state with a UTC timestamp in SQLite. | STK-03 |

## Non-functional constraints
- NFR-01: Serve the demonstration dashboard only on localhost by default.
- NFR-02: Automated tests shall verify FR-03 and FR-04.
- NFR-03: Documentation shall clearly distinguish simulations from real equipment integrations.

## Change-control example
If a stakeholder requests a 10-second threshold instead of three reporting cycles, update the approved requirement, implementation, acceptance tests and traceability matrix together.
