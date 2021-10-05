import asyncio
import logging
import signal
import time
from datetime import datetime

from wave_reader import discover_devices

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Event loop to run asynchronous tasks.
    loop = asyncio.get_event_loop()
    # Scan for BTLE Wave devices.
    devices = loop.run_until_complete(discover_devices())
    # Get sensor readings from available wave devices.

    if len(devices) == 0:
        logger.info("Didn't find any devices")
        exit

    run = True

    def handler_stop_signals(signum, frame):
        print(f"{datetime.now().isoformat()} -Quitting...")

        global run
        run = False

    signal.signal(signal.SIGINT, handler_stop_signals)
    signal.signal(signal.SIGTERM, handler_stop_signals)

    while run:
        for device in devices:
            print(
                f"{datetime.now().isoformat()} - Reading sensor values, address={device.address} serial={device.serial}"
            )

            try:
                sensor_readings = loop.run_until_complete(device.get_sensor_values())
            except Exception as exc:
                print(
                    f"{datetime.now().isoformat()} -Failed to read sensor values from {device.address}"
                )
                break

            print(sensor_readings)

        time.sleep(10)
