from tools import shift_bits, getBits, getSpeed, get32FloatBits, get16FloatBits

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

canData = {'DataType': 'none',
           'BatteryVoltage': 0,
           'BatteryCurrent': 0,
           'BatteryCurrentDirection': 'none',
           'MotorCurrentPeakAverage': 'none',
           'FETTemperature': 'none',
           'MotorRotatingSpeed': 'none',
           'PWMDuty': 'none',
           'LeadAngle': 'none',
           'Speed': 0,
           'SOC': 0,
           'SOC2': 0,
           'HighCellVolts': 'none',
           'LowCellVolts': 'none',
           'Temp': 'none',
           'InputVoltage0': 0,
           'InputCurrent0': 0,
           'InputVoltage1': 0,
           'InputCurrent1': 0,
           'OutputVoltage0': 0,
           'OutputCurrent0': 0,
           'OutputVoltage1': 0,
           'OutputCurrent1': 0,
           'MosfetTemperature': 'none',
           'Mode': 0, 
           'ControllerTemperature': 'none',
           'LowArrayPower': 'none',
           'MosfetOverheat': 'none',
           'BatteryLow': 'none',
           'BatteryFull': 'none',
           '12VUnderVoltage': 'none',
           'HWOvercurrent': 'none',
           'HWOvervoltage': 'none',
           'PackCurrent': 0,
           'State': 0,
           'FaultID': 0}

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
        canData.update({'DataType': 'mc',
                'BatteryVoltage': getBits(data, 0, 9),
                'BatteryCurrent': getBits(data, 10, 18),
                'BatteryCurrentDirection': getBits(data, 19, 19),
                'MotorCurrentPeakAverage': getBits(data, 20, 29),
                'FETTemperature': getBits(data, 30, 34),
                'MotorRotatingSpeed': getBits(data, 35, 46),
                'PWMDuty': getBits(data, 47, 56),
                'LeadAngle': getBits(data, 57, 63)})
    # bms
    elif(canId == 0x289):
        canData.update({'DataType': 'bms',
                   'SOC': getBits(data, 56, 63)/2,
                   'Temp': getBits(data, 0, 7)})
    elif(canId == 0x301):
        canData.update({'DataType': 'bmsData',
                   'PackCurrent': getBits(data, 0, 7),
                   'PackDCL': getBits(data, 8, 15),
                   'PackCCL': getBits(data, 16, 23)})

    # MPPT0 InputVoltage and InputCurrent
    elif(canId == 0x600):
        canData.update({'DataType': 'mppt0Input',
                   'InputVoltage0': get32FloatBits(data, 0, 31),
                   'InputCurrent0': get32FloatBits(data, 32, 63)})
    # MPPT1 InputVoltage and InputCurrent
    elif(canId == 0x610):
        canData.update({'DataType': 'mppt1Input',
                   'InputVoltage1': get32FloatBits(data, 0, 31),
                   'InputCurrent1': get32FloatBits(data, 32, 63)})
    # MPPT0 OutputVoltage and OutputCurrent
    elif(canId == 0x601):
        canData.update({'DataType': 'mppt0Output',
                   'OutputVoltage': get32FloatBits(data, 0, 31),
                   'OutputCurrent': get32FloatBits(data, 32, 63)})
    # MPPT1 OutputVoltage and OutputCurrent
    elif(canId == 0x611):
        canData.update({'DataType': 'mppt1Output',
                   'OutputVoltage': get32FloatBits(data, 0, 31),
                   'OutputCurrent': get32FloatBits(data, 32, 63)})
    # MPPTS temp
    elif(canId == 0x602 or canId == 0x612):
        canData.update({'DataType': 'mpptsTemp',
                   'MosfetTemperature': get32FloatBits(data, 0, 31),
                   'ControllerTemperature': get32FloatBits(data, 32, 63)})
    elif(canId == 0x605):
        canData.update({'DataType': 'mppt0error',
                    'Mode': getBits(data, 40, 40),
                    'LowArrayPower': bool(getBits(data, 23, 23)),
                    'MosfetOverheat': bool(getBits(data, 22, 22)),
                    'BatteryLow': bool(getBits(data, 21, 21)),
                    'BatteryFull': bool(getBits(data, 20, 20)),
                    '12VUnderVoltage': bool(getBits(data, 19, 19)),
                    'HWOverCurrent': bool(getBits(data, 17, 17)),
                    'HWOverVoltage': bool(getBits(data, 16, 16))})
    elif(canId == 0x615):
        canData.update({'DataType': 'mppt1error',
                    'Mode': getBits(data, 40, 40),
                    'LowArrayPower': bool(getBits(data, 23, 23)), #adding the 'bool' here simply makes it so it turns the 1 or 0 into a bool
                    'MosfetOverheat': bool(getBits(data, 22, 22)),
                    'BatteryLow': bool(getBits(data, 21, 21)),
                    'BatteryFull': bool(getBits(data, 20, 20)),
                    '12VUnderVoltage': bool(getBits(data, 19, 19)),
                    'HWOverCurrent': bool(getBits(data, 17, 17)),
                    'HWOverVoltage': bool(getBits(data, 16, 16))})
    elif(canId == 0x69):
        canData.update({'DataType': 'Speed',
                        'Speed': getBits(data, 0, 7)})
    elif(canId == 0x420):
        canData.update({'DataType': 'STM',
                        'State': getBits(data, 0, 7),
                        'FaultID': getBits(data, 8, 15)})
    
    return canData

    
