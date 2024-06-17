import can

# motor controller filters
mcFilters = [
    {"can_id": 0x08850225, "can_mask": 0x1FFFFFFF, "extended": True},
    {"can_id": 0x08850245, "can_mask": 0x1FFFFFFF, "extended": True},
    {"can_id": 0x08850265, "can_mask": 0x1FFFFFFF, "extended": True},
    {"can_id": 0x08850285, "can_mask": 0x1FFFFFFF, "extended": True},
]

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
