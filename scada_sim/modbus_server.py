
"""Simulated wind turbine Modbus TCP server.

Compatible with PyModbus 3.16.x.
This server runs locally and does not connect to real equipment.
"""

import asyncio
import math

from pymodbus.server import ModbusTcpServer
from pymodbus.simulator import DataType, SimData, SimDevice

HOST = "127.0.0.1"
PORT = 5020
DEVICE_ID = 1


async def update_measurements(server):
    """Update the turbine measurements every second."""

    cycle = 0

    while True:
        wind_speed = 8 + 2 * math.sin(cycle / 5)
        power_kw = min(
            2000,
            (wind_speed / 12) ** 3 * 2000
        )

        registers = [
            int(wind_speed * 10),
            int(power_kw),
            1,
        ]

        await server.async_setValues(
            DEVICE_ID,
            3,
            0,
            registers
        )

        print(
            f"Wind: {wind_speed:.1f} m/s | "
            f"Power: {power_kw:.0f} kW | "
            f"Status: ONLINE"
        )

        cycle += 1
        await asyncio.sleep(1)


async def main():

    device = SimDevice(
        DEVICE_ID,
        SimData(
            address=0,
            values=[0, 0, 0],
            datatype=DataType.REGISTERS,
        ),
    )

    server = ModbusTcpServer(
        device,
        address=(HOST, PORT),
    )

    print(f"Starting Modbus TCP server on {HOST}:{PORT}")

    update_task = asyncio.create_task(
        update_measurements(server)
    )

    try:
        await server.serve_forever()
    finally:
        update_task.cancel()
        await asyncio.gather(
            update_task,
            return_exceptions=True
        )


if __name__ == "__main__":
    asyncio.run(main())
