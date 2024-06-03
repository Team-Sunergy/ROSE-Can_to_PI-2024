import os
import time
import can

def setup_can_interface():
    print('\n\rCAN Data Parser')
    print('Bring up CAN0....')
    # Bring down the interface if it's already up
    os.system("sudo /sbin/ip link set can0 down")
    # Bring up the interface with the correct settings
    os.system("sudo /sbin/ip link set can0 up type can bitrate 250000")
    time.sleep(0.1)
    print('Ready')

def shutdown_can_interface():
    os.system("sudo /sbin/ip link set can0 down")
    print('\n\rCAN interface shut down')

def initialize_bus():
    try:
        bus = can.interface.Bus(channel='can0', bustype='socketcan')  # Correct interface type
        print('Initialized bus')
        return bus
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

    # Example: Print data in hex format
    data_str = ' '.join(f'{byte:02x}' for byte in message.data)
    parsed_data['data_str'] = data_str

    return parsed_data

def main():
    setup_can_interface()
    print('The setup_can_interface done')
    bus = initialize_bus()
    print('Bus varible is set')

    try:
        print('In the try')
        while True:
            message = bus.recv()  # Wait until a message is received.
            parsed_message = parse_can_message(message)

            print(f"Timestamp: {parsed_message['timestamp']:.6f}")
            print(f"ID: {parsed_message['arbitration_id']:x}")
            print(f"DLC: {parsed_message['dlc']}")
            print(f"Data: {parsed_message['data_str']}")
            print('-' * 30)

    except KeyboardInterrupt:
        shutdown_can_interface()
        print('\n\rKeyboard interrupt')

if __name__ == '__main__':
    main()
