import math
from math import pi

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
    return (int.from_bytes(canMessage, byteorder='little') >> low) & mask


# if given bits, will return the correct speed of a vehicle given diameter of tires
def getSpeed(RPM):
    return RPM * TIRE_DIAMETER * PI * MINUTES_IN_HOUR/NUM_OF_INCHES_IN_MILE