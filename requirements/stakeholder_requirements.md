# Stakeholder requirements (fictional exercise)

These stakeholder statements are **invented for training**, not elicited from Nordex or a real service team.

| ID | Stakeholder need |
|---|---|
| STK-01 | As an operator, I need to see the latest status and measurements for each turbine. |
| STK-02 | As a service engineer, I need to know when a turbine stops sending data. |
| STK-03 | As an investigator, I need a timestamped measurement history for later analysis. |

## Open questions for a real requirements workshop
- What is the expected measurement interval? Are timestamps assigned by devices or server?
- What exactly constitutes loss of communication versus a device shutdown?
- How quickly must the alarm appear? Should it latch or clear automatically?
- Which measurement units, ranges and data-retention requirements apply?
- Who can acknowledge or change alarms, and what cybersecurity controls are required?
