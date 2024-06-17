def parse_can_message(message):
    """
    Parses a received CAN message into a dictionary with timestamp,
    arbitration ID, data length code (DLC), and data (in hex string format).
    """
    parsed_data = {
        "timestamp": message.timestamp,
        "arbitration_id": message.arbitration_id,
        "dlc": message.dlc,
        "data": message.data,
    }

    data_str = " ".join(f"{byte:02x}" for byte in message.data)
    parsed_data["data_str"] = data_str

    return parsed_data
