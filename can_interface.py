import os
import time

def setup_can_interface():
    """
    Sets up the CAN interface by bringing down the interface if it's already up,
    and then bringing it up with the specified bitrate.
    """
    print("\n\rCAN Data Parser")
    print("Bring up CAN0....")
    os.system("sudo /sbin/ip link set can0 down")
    os.system("sudo /sbin/ip link set can0 up type can bitrate 250000")
    time.sleep(0.1)
    print("Ready")

def shutdown_can_interface():
    """
    Shuts down the CAN interface.
    """
    os.system("sudo /sbin/ip link set can0 down")
    print("\n\rCAN interface shut down")
