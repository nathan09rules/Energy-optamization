from bleak import BleakClient, BleakScanner
import asyncio

async def main():
    print("Scanning...")
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)

    address = "1c:69:20:93:CF:5A"  # Replace with your ESP32 address
    async with BleakClient(address) as client:
        print("Connected!")

        # UUID for TX (sending) characteristic
        CHAR_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

        while True:
            data = await client.read_gatt_char(CHAR_UUID)
            print(data.decode())

asyncio.run(main())
