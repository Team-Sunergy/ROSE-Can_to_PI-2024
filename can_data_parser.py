import can

def receive_can_messages(channel='can0', bustype='socketcan'):
    """
    Receives and prints CAN messages from the specified channel and bus type using a Printer listener.
    
    Parameters:
    - channel (str): The name of the CAN interface (default: 'can0').
    - bustype (str): The type of the CAN interface (default: 'socketcan').
    """
    try:
        # Initialize the CAN bus with the specified channel and bus type
        bus = can.interface.Bus(channel=channel, bustype=bustype)
        print(f"Listening for CAN messages on {channel}...")
        
        # Create a Printer listener to print received messages
        printer = can.Printer()
        can.Notifier(bus, [printer])
        
        # Continuously listen for incoming CAN messages
        while True:
            pass  # No need to manually receive messages, the Printer listener handles it

    except KeyboardInterrupt:
        print("Stopped by user")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    receive_can_messages()