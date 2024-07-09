import math
from math import pi
import can
import threading
import time
import struct

# these might be better to define in main
TIRE_DIAMETER = 21.5 # in inches
NUM_OF_INCHES_IN_MILE = 63360
MINUTES_IN_HOUR = 60
PI = math.pi

# tools for use in can data gathering
def shift_bits(data, shift_amount):
    """
    Shifts the bits of each byte in the data by the specified amount.
    """
    shifted_data = bytearray()
    for byte in data:
        shifted_byte = (byte << shift_amount) & 0xFF | (byte >> (8 - shift_amount))
        shifted_data.append(shifted_byte)
    return shifted_data

def getBits(canMessage: bytearray, low: int, high: int) -> int:
    """
    Extracts bits from `low` to `high` (inclusive) from the given.
    """
    mask = (1 << (high - low + 1)) - 1
    return (int.from_bytes(canMessage, byteorder='big') >> low) & mask

def get32FloatBits(canMessage: bytearray, low: int, high: int) -> float:
    """
    Extracts bits from `low` to `high` (inclusive) from the given bytearray
    and converts them to a float. Assumes `high - low + 1 == 32`.
    """
    # Ensure the range is exactly 32 bits
    if high - low + 1 != 32:
        raise ValueError("The range must be exactly 32 bits to convert to a float.")
    
    # Create a mask for 32 bits
    mask = (1 << 32) - 1

    # Extract the 32 bits and shift them into position
    extracted_bits = (int.from_bytes(canMessage, byteorder='big') >> low) & mask
    
    # Convert the extracted bits to a 4-byte array
    float_bytes = extracted_bits.to_bytes(4, byteorder='big')
    
    # Unpack the 4-byte array as a float
    return struct.unpack('<f', float_bytes)[0]


def get16FloatBits(canMessage: bytearray, low: int) -> float:
    """
    Extracts a 16-bit float starting from `low` bit in the given bytearray.
    """
    # Ensure the range is exactly 16 bits
    num_bits = 16
    
    # Calculate the byte range
    start_byte = low // 8
    end_byte = (low + num_bits - 1) // 8
    
    # Extract the relevant bytes
    float_bytes = canMessage[start_byte:end_byte + 1]
    
    # If the extracted bytes are not exactly 2, pad with zero bytes if necessary
    if len(float_bytes) < 2:
        float_bytes += bytes(2 - len(float_bytes))
    
    # Unpack the 2-byte array as a float
    return struct.unpack('<e', float_bytes)[0]

# if given bits, will return the correct speed of a vehicle given diameter of tires
def getSpeed(RPM):
    """
    Obtains speed given RPM
    """
    return RPM * TIRE_DIAMETER * PI * MINUTES_IN_HOUR/NUM_OF_INCHES_IN_MILE

def send_requests_frame0(bus):
    """
    Sends a request for Frame0 on the given CAN bus.
    """
    # Create a request messages for Frame0
    #Log_Req_RL1, message to rear left
    request_frame0_RL1 = can.Message(arbitration_id=0x08F89540, 
                                 data=[0x07],  # Data to request Frame0, 7 is frame0, 1, 2
                                 is_extended_id=True)  # true as it is 29bit frame
    
    #Log_Req_RR1, message to rear right
    request_frame0_RR1 = can.Message(arbitration_id=0x08F91540, 
                                 data=[0x07],  # Data to request Frame0, 7 is frame0, 1, 2
                                 is_extended_id=True)  # true as it is 29bit frame
    # Sends request messages
    # try:
    #     bus.send(request_frame0_RL1)
    #     print("Request for Frame0 RL1 sent")
    # except can.CanError:
    #     print("Failed to send request for Frame0 RL1")

    # try:
    #     bus.send(request_frame0_RR1)
    #     print("Request for Frame0 RR1 sent")
    # except can.CanError:
    #     print("Failed to send request for Frame0 RR1")

def returnErrorColor(bit):
    if(bit == 0):
        return 'lime'
    else: # if bit == 1
        return 'yellow'

def send_request_frame0_periodically(bus):
    def send_requests():
        while True:
            send_requests_frame0(bus)
            time.sleep(0.5)

    threading.Thread(target=send_requests).start()
    print("Started thread to send request frame0...")
