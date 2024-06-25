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
