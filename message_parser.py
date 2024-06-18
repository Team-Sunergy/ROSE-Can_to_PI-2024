from tools import shift_bits 

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
