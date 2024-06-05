import can

# filters for the motor controllers, mask of 0x1FFFFFFF checks all 29 bits
# of extended ID
filters = [
    {"can_id": 0x8850225, "can_mask": 0x1FFFFFFF, "extended": True},
    {"can_id": 0x8850245, "can_mask": 0x1FFFFFFF, "extended": True},
    {"can_id": 0x8850265, "can_mask": 0x1FFFFFFF, "extended": True},
    {"can_id": 0x8850285, "can_mask": 0x1FFFFFFF, "extended": True},
]
