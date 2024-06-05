import can

# filters for the motor controllers, mask of 0x1FFFFFFF checks all 29 bits
# of extended ID
mcFilters = [
    {"can_id": 0x08850225, "can_mask": 0x1FFFFFFF, "extended": True},
    {"can_id": 0x08850245, "can_mask": 0x1FFFFFFF, "extended": True},
    {"can_id": 0x08850265, "can_mask": 0x1FFFFFFF, "extended": True},
    {"can_id": 0x08850285, "can_mask": 0x1FFFFFFF, "extended": True},
]

# defines canbus
bus = can.interface.Bus(channel="can0",
             interface="socketcan",
             can_filters=mcFilters)
# sets filters (i'm not sure if this is needed)
bus.set_filters(mcFilters)

# for messages (which have been filtered)
for msg in bus:
    # there are a lot of different scenarios for can messages to filter. 
    # i want to check for the
    print(msg)

# accepts an input as an hex, and low and high bits, and returns
# hex in the range of low and high order bits
# for example, getBits(0x08850285, 4, 11) returns x28
def getBits(canId: hex, low: int, high: int) -> hex:
    tempcanId = canId

    tempcanId = tempcanId >> low #right shift = low
    tempcanId = tempcanId << ((31 - high) + low) 
    tempcanId = tempcanId >> (31 - high) + low
    
    return tempcanId

# this is a boolean function that simplifies checking if bits are what we need or not
def checkBits(canId: hex, bits: hex, low: int, high: int) -> bool:
    b = getBits(canId, low, high)
    return bits & b == bits