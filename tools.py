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

# gets certain bits from data
def getBits(canId: int, low: int, high: int) -> int:
    """
    Extracts bits from `low` to `high` (inclusive) from the given `canId`.
    """
    mask = (1 << (high - low + 1)) - 1
    return (canId >> low) & mask