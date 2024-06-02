def parse_can_message(message):
    # Function to parse CAN message data
    parsed_data = {
        'timestamp': message.timestamp,
        'arbitration_id': message.arbitration_id,
        'dlc': message.dlc,
        'data': message.data,
    }

    # Add custom parsing logic here
    # Example: Format data bytes as a hexadecimal string
    data_str = ' '.join(f'{byte:02x}' for byte in message.data)
    parsed_data['data_str'] = data_str

    return parsed_data