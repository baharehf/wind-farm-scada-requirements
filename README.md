# Wind Farm SCADA Requirements & Monitoring — Learning Prototype

A small, **local, simulated** wind-farm monitoring application intended to demonstrate requirements engineering and basic software verification. It does **not** connect to real turbines or Nordex systems.

## What it does
- Simulates three wind turbines, each reporting wind speed, power output and communication status.
- Writes time-stamped measurements to a local SQLite database.
- Detects a communication failure when a turbine misses three simulated reporting cycles.
- Displays the latest values and current alarms in a browser.
- Includes functional requirements, acceptance criteria, a traceability matrix and automated tests.

## Run (Python 3.10+; no packages to install)

```bash
python -m scada_sim.app
```

Open http://127.0.0.1:8000 in your browser. Press Ctrl+C to stop.

The simulation deliberately disconnects turbine **T-02** periodically to exercise the alarm flow.

## Run automated tests

```bash
python -m unittest discover -s tests -v
```

## Requirements engineering demonstration
See:
- [`requirements/stakeholder_requirements.md`](requirements/stakeholder_requirements.md)
- [`requirements/functional_specification.md`](requirements/functional_specification.md)
- [`requirements/acceptance_criteria.md`](requirements/acceptance_criteria.md)
- [`requirements/traceability_matrix.csv`](requirements/traceability_matrix.csv)

## System design

```text
Local simulated turbine readings
             |
             v
        Alarm evaluator
             |
             v
     SQLite measurement log
             |
             v
    Local HTTP dashboard
```

## Scope and limitations
- Educational demonstration, not safety-certified SCADA software.
- Simulated signals only. No industrial device interfaces or external network connectivity.
- Local HTTP server binds to **127.0.0.1**, not the public internet.
- Alarm threshold is a project assumption, not a Nordex operating requirement.
- OPC UA, Modbus TCP, user roles and cyber-security hardening are **planned extensions**, not implemented features.

## Suggested next extensions
1. Add a Modbus TCP simulator and client; document register mapping and failure behaviour.
2. Add a requirement review/change history and stronger traceability to tests.
3. Add historical charts and filtering by turbine.
4. Add a CI test workflow and incident reports.

## CV description (only after running and understanding the work)
*Developed a local Python prototype of a simulated wind-farm monitoring workflow with SQLite storage, communication-failure alarms, acceptance criteria, traceability documentation and unit tests.*
