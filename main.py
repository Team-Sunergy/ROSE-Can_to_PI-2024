import os
import time
import can
from cloud_store import store_data_to_supabase

print("Main Application")

# Initialize CAN bus
try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
    print('Cannot find PiCAN board.')
    exit()

def parse_can_message(message):
    # Function to parse CAN message data
    parsed_data = {
        'timestamp': message.timestamp,
        'arbitration_id': message.arbitration_id,
        'dlc': message.dlc,
        'data': message.data,
    }
    
    # Add custom parsing logic here
    # Example: Format data bytes as a hexadecimal string
    data_str = ' '.join(f'{byte:02x}' for byte in message.data)
    parsed_data['data_str'] = data_str

    return parsed_data

try:
    while True:
        message = bus.recv()  # Wait until a message is received.
        parsed_message = parse_can_message(message)
        
        # Example: Store parsed data to Supabase
        store_data_to_supabase(parsed_message)
        
        # Add GUI code here
        
        # Delay for stability
        time.sleep(0.1)
        
except KeyboardInterrupt:
    # Catch keyboard interrupt
    os.system("sudo /sbin/ip link set can0 down")
    print('\n\rKeyboard interrupt')
