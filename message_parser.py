from tools import shift_bits, getBits, getSpeed

def parse_can_message(message, shift_amount=0):
    """
    Parses a received CAN message into a dictionary with timestamp,
    arbitration ID, data length code (DLC), and data (in hex string format).
    Shifts the data bits by the specified amount.
    """
    shifted_data = shift_bits(message.data, shift_amount)

    parsed_data = {
        "timestamp": message.timestamp,
        "arbitration_id": message.arbitration_id,
        "dlc": message.dlc,
        "data": shifted_data,
    }

    data_str = " ".join(f"{byte:02x}" for byte in message.data)
    parsed_data["data_str"] = data_str

    return parsed_data

def group_can_data(canId, data: bytearray) -> dict:
    """
    This function, given the data from a CANFrame, organizes all of the data
    into a dictionary, which can be used to access certain data values given a key.
    This Data will change depending on what type of CANID is given.
    You can see the keys for each here.
    There are also a few other keys that have been added, such as speed.
    """
    # motor controllers
    if(canId == 0x0885025 or canId == 0x08850245 or canId == 0x08850265 or canId == 0x08850285):
        canData = {'DataType': 'mc',
                'BatteryVoltage': getBits(data, 0, 9),
                'BatteryCurrent': getBits(data, 10, 18),
                'BatteryCurrentDirection': getBits(data, 19, 19),
                'MotorCurrentPeakAverage': getBits(data, 20, 29),
                'FETTemperature': getBits(data, 30, 34),
                'MotorRotatingSpeed': getBits(data, 35, 46),
                'PWMDuty': getBits(data, 47, 56),
                'LeadAngle': getBits(data, 57, 63),
                'Speed': getSpeed(getBits(data, 20, 29))}
    # bms
    elif(canId == 0x289):
        canData = {'DataType': 'bms',
                   'SOC': getBits(data, 0, 7),
                   'HighCellVolts': getBits(data, 8, 23),
                   'LowCellVolts': getBits(data, 24, 39),
                   'Temp': getBits(data, 56, 63)}
    # MPPTS  out volts and out current
    elif(canId == 0x601 or canId == 0x611):
        canData = {'DataType': 'mpptsvolt',
                   'OutVolts': getBits(data, 0, 31),
                   'OutCurrent': getBits(data, 32, 63)}
    # MPPTS temp
    elif(canId == 0x602 or canId == 0x612):
        canData = {'DataType': 'mpptstemp',
                   'ControllerTemp': getBits(data, 32, 64)}
    else:
        canData = None

    
    return canData

    