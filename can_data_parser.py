import os
import time
import can

# Define CAN message filters to specify which CAN messages to receive
mcFilters = [
    {"can_id": 0x08850225, "can_mask": 0x1FFFFFFF, "extended": True},
    {"can_id": 0x08850245, "can_mask": 0x1FFFFFFF, "extended": True},
    {"can_id": 0x08850265, "can_mask": 0x1FFFFFFF, "extended": True},
    {"can_id": 0x08850285, "can_mask": 0x1FFFFFFF, "extended": True},
]

def setup_can_interface():
    """
    Sets up the CAN interface by bringing down the interface if it's already up,
    and then bringing it up with the specified bitrate.
    """
    print("\n\rCAN Data Parser")
    print("Bring up CAN0....")
    # Bring down the CAN interface if it's already up
    os.system("sudo /sbin/ip link set can0 down")
    # Bring up the CAN interface with a bitrate of 250000
    os.system("sudo /sbin/ip link set can0 up type can bitrate 250000")
    time.sleep(0.1)  # Wait for a short period to ensure the interface is up
    print("Ready")

def shutdown_can_interface():
    """
    Shuts down the CAN interface.
    """
    os.system("sudo /sbin/ip link set can0 down")
    print("\n\rCAN interface shut down")

def initialize_bus():
    """
    Initializes the CAN bus with the specified channel and filters.
    Returns the bus object if successful, otherwise exits the program.
    """
    try:
        bus = can.interface.Bus(
            channel="can0", bustype="socketcan", can_filters=mcFilters
        )
        print("Initialized bus & Filter")
        return bus
    except OSError:
        print("Cannot find PiCAN board.")
        exit()

def parse_can_message(message):
    """
    Parses a received CAN message into a dictionary with timestamp,
    arbitration ID, data length code (DLC), and data (in hex string format).
    """
    parsed_data = {
        "timestamp": message.timestamp,
        "arbitration_id": message.arbitration_id,
        "dlc": message.dlc,
        "data": message.data,
    }

    # Convert data bytes to a hex string
    data_str = " ".join(f"{byte:02x}" for byte in message.data)
    parsed_data["data_str"] = data_str

    return parsed_data

def main():
    """
    Main function to set up the CAN interface, initialize the bus, and continuously
    receive and parse CAN messages until interrupted by the user.
    """
    setup_can_interface()
    print("The setup_can_interface done")
    bus = initialize_bus()
    print("Bus variable is set")

    try:
        print("In the try")
        while True:
            message = bus.recv()  # Wait until a CAN message is received
            parsed_message = parse_can_message(message)  # Parse the received message

            # Print the parsed message details
            print(f"Timestamp: {parsed_message['timestamp']:.6f}")
            print(f"ID: {parsed_message['arbitration_id']:x}")
            print(f"DLC: {parsed_message['dlc']}")
            print(f"Data: {parsed_message['data_str']}")
            print("-" * 30)

    except KeyboardInterrupt:
        # Shut down the CAN interface when the program is interrupted
        shutdown_can_interface()
        print("\n\rKeyboard interrupt")

if __name__ == "__main__":
    main()
