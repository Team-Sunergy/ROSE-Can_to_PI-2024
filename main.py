from can_interface import setup_can_interface, shutdown_can_interface
from bus import initialize_bus
from message_parser import parse_can_message
from tools import getBits, send_request_frame0_periodically


def main():
    """
    Main function to set up the CAN interface, initialize the bus, and continuously
    receive and parse CAN messages until interrupted by user.
    """
    setup_can_interface()
    print("The setup_can_interface done")
    bus = initialize_bus()
    print("Bus variable is set")
    send_request_frame0_periodically(bus)
    print("Sending request frame0 in main...")

    try:
        print("In the try")
        while True:
            message = bus.recv()
            parsed_message = parse_can_message(message) # recieves parsed message
            data = parsed_message['data']
            
            print(f"Timestamp: {parsed_message['timestamp']:.6f}")
            print(f"ID: {parsed_message['arbitration_id']:x}")
            print(f"DLC: {parsed_message['dlc']}")
            print(f"Data: {parsed_message['data_str']}")
            print("-" * 30)
            print(getBits(data, 0, 7))


    except KeyboardInterrupt:
        shutdown_can_interface()
        print("\n\rKeyboard interrupt")

if __name__ == "__main__":
    main()
