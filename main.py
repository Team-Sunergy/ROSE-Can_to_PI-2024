import tkthread; tkthread.patch()

from can_interface import setup_can_interface, shutdown_can_interface
from bus import initialize_bus
from message_parser import parse_can_message, group_can_data
from tools import getBits, send_request_frame0_periodically, getSpeed
from gui import startGui, updateGuiData

def main():
    """
    Main function to set up the CAN interface, initialize the bus, and continuously
    receive and parse CAN messages until interrupted by user.
    """
    setup_can_interface()
    print("The setup_can_interface done")
    bus = initialize_bus()
    print("Bus variable is set")
    startGui()
    print("Gui started up")
    # this is for motor controllers
    send_request_frame0_periodically(bus=bus)
    print("Sending request frame0 in main...")

    try:
        print("In the try")
        while True:
            message = bus.recv()
            parsed_message = parse_can_message(message) # recieves parsed message
            data = parsed_message['data']
            
            # used for seeing can frames
            print(f"Timestamp: {parsed_message['timestamp']:.6f}")
            print(f"ID: {parsed_message['arbitration_id']:x}")
            print(f"DLC: {parsed_message['dlc']}")
            print(f"Data: {parsed_message['data_str']}")
            print("-" * 30)
            
            # used for sending data, contains all different types of possible categories (mppts, bms, mc)
            # depending on what CAN frame ID is
            canData = group_can_data(data=data)
            updateGuiData(data=data)

            



    except KeyboardInterrupt:
        shutdown_can_interface()
        print("\n\rKeyboard interrupt")

if __name__ == "__main__":
    main()
