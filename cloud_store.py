import os
import supabase
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase_client = supabase.create_client(supabase_url, supabase_key)

def store_data_to_supabase(parsed_data):
    # Store parsed data to Supabase
    table_name = "can_data"
    response = supabase_client.table(table_name).insert(parsed_data)
    if response.status_code == 201:
        print("Data stored successfully.")
    else:
        print("Failed to store data:", response.error)

# Example usage:
# parsed_data = {
#     "timestamp": 1234567890.123,
#     "arbitration_id": 123,
#     "dlc": 8,
#     "data": [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08],
#     "data_str": "01 02 03 04 05 06 07 08"
# }
# store_data_to_supabase(parsed_data)
