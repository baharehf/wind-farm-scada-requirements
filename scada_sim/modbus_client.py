
"""Read turbine data from a local Modbus TCP server."""

from pymodbus.client import ModbusTcpClient

HOST = "127.0.0.1"
PORT = 5020
DEVICE_ID = 1


def main():
    client = ModbusTcpClient(HOST, port=PORT, timeout=3)

    if not client.connect():
        print("ERROR: Cannot connect to Modbus server.")
        print("Make sure modbus_server.py is running.")
        return

    try:
        response = client.read_holding_registers(
            address=0,
            count=3,
            device_id=DEVICE_ID
        )

        if response.isError():
            print("Modbus response error:", response)
            return

        registers = response.registers

        wind_speed = registers[0] / 10.0
        power_kw = registers[1]
        turbine_online = bool(registers[2])

        print("=== WIND TURBINE MONITORING ===")
        print(f"Wind speed: {wind_speed:.1f} m/s")
        print(f"Power output: {power_kw} kW")
        print(f"Turbine online: {turbine_online}")

    except Exception as error:
        print(f"Communication error: {error}")

    finally:
        client.close()


if __name__ == "__main__":
    main()
