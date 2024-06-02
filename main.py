import os
import time
import can
from cloud_store import store_data_to_supabase
from can_data_parser import parse_can_message

print("Main Application")

# Initialize CAN bus
try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
    print('Cannot find PiCAN board.')
    exit()

try:
    while True:
        message = bus.recv()  # Wait until a message is received.
        parsed_message = parse_can_message(message)

        # Store parsed data to Supabase
        store_data_to_supabase(parsed_message)

        # Add GUI code here

        # Delay for stability
        time.sleep(0.1)

except KeyboardInterrupt:
    # Catch keyboard interrupt
    os.system("sudo /sbin/ip link set can0 down")
    print('\n\rKeyboard interrupt')