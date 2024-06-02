import can

def receive_can_messages(channel='can0', bustype='socketcan'):
    try:
        # Set up the CAN bus
        bus = can.interface.Bus(channel=channel, bustype=bustype)
        print(f"Listening for CAN messages on {channel}...")

        # Create a listener that will print received messages
        while True:
            message = bus.recv()
            if message:
                print(f"Received message: {message}")

    except KeyboardInterrupt:
        print("Stopped by user")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    receive_can_messages()
