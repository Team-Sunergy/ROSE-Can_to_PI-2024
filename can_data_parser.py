import os
import time
import can

# Define CAN message filters to specify which CAN messages to receive
bus_filters = [
    {"can_id": 0x612, "can_mask": 0x1FFFFFFF, "extended": False},       #MPPT 1
    {"can_id": 0x611, "can_mask": 0x1FFFFFFF, "extended": False},       #MPPT 1
    {"can_id": 0x602, "can_mask": 0x1FFFFFFF, "extended": False},       #MPPT 0
    {"can_id": 0x601, "can_mask": 0x1FFFFFFF, "extended": False},       #MPPT 0
    {"can_id": 0x289, "can_mask": 0x1FFFFFFF, "extended": False},       #BMS 
    {"can_id": 0x08850225, "can_mask": 0x1FFFFFFF, "extended": True},   #Motor RearLeft
    {"can_id": 0x08850245, "can_mask": 0x1FFFFFFF, "extended": True},   #Motor RearRight
    {"can_id": 0x08850265, "can_mask": 0x1FFFFFFF, "extended": True},   #Motor FrontLeft
    {"can_id": 0x08850285, "can_mask": 0x1FFFFFFF, "extended": True},   #Motor FrontLeft
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
            channel="can0", bustype="socketcan", can_filters=bus_filters
        )
        print("Initialized bus & Filter")
        return bus
    except OSError:
        print("Cannot find PiCAN board.")
        exit()

def shift_bits(data, shift_amount):
    """
    Shifts the bits of each byte in the data by the specified amount.
    """
    shifted_data = bytearray()
    for byte in data:
        shifted_byte = (byte << shift_amount) & 0xFF | (byte >> (8 - shift_amount))
        shifted_data.append(shifted_byte)
    return shifted_data

def getBits(canId: int, low: int, high: int) -> int:
    """
    Extracts bits from `low` to `high` (inclusive) from the given `canId`.
    """
    mask = (1 << (high - low + 1)) - 1
    return (canId >> low) & mask

def parse_can_message(message, shift_amount=0):
    """
    Parses a received CAN message into a dictionary with timestamp,
    arbitration ID, data length code (DLC), and data (in hex string format).
    Shifts the data bits by the specified amount.
    """
    shifted_data = shift_bits(message.data, shift_amount)

    parsed_data = {
        "timestamp": message.timestamp,
        "arbitration_id": message.arbitration_id,
        "dlc": message.dlc,
        "data": shifted_data,
    }

    # Convert shifted data bytes to a hex string
    data_str = " ".join(f"{byte:02x}" for byte in shifted_data)
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

    shift_amount = 0  # Set the amount to shift the data bits

    try:
        print("In the try")
        while True:
            message = bus.recv()  # Wait until a CAN message is received
            parsed_message = parse_can_message(message, shift_amount)  # Parse the received message with bit shifting
            bits_extracted = getBits(parsed_message['arbitration_id'], 4, 11)
            print(f"Extracted Bits: {bits_extracted:x}")

            # Print the parsed message details
            print(f"Timestamp: {parsed_message['timestamp']:.6f}")
            print(f"ID: {parsed_message['arbitration_id']:x}")
            print(f"DLC: {parsed_message['dlc']}")
            print(f"Data: {parsed_message['data_str']}")
            print("-" * 30)
            time.sleep(.01)

    except KeyboardInterrupt:
        # Shut down the CAN interface when the program is interrupted
        shutdown_can_interface()
        print("\n\rKeyboard interrupt")

if __name__ == "__main__":
    main()
