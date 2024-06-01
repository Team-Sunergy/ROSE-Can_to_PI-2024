import os
import json
import can
import logging
from supabase import create_client, Client
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Supabase configuration
SUPABASE_URL = 'https://qewzbllhuxtfxzudwtdm.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFld3pibGxodXh0Znh6dWR3dGRtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTcyMDIxMDAsImV4cCI6MjAzMjc3ODEwMH0.uIw4f7uJEmzK4UhoPn5abCIx9KmSQO0c3zzJBiH3Hsg'

def initialize_supabase() -> Client:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        logging.info("Supabase initialized successfully.")
        return supabase
    except Exception as e:
        logging.error(f"Failed to initialize Supabase: {e}")
        exit(1)

def read_can_data(supabase: Client):
    try:
        # Set up CAN bus interface
        bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
        logging.info("Listening for CAN messages...")

        while True:
            # Receive CAN message
            message = bus.recv()
            if message is not None:
                data = {
                    'id': message.arbitration_id,
                    'data': list(message.data),
                    'timestamp': datetime.fromtimestamp(message.timestamp).isoformat()
                }
                logging.info(f"Received message: {data}")
                # Send received data to Supabase
                send_to_supabase(supabase, data)
    except KeyboardInterrupt:
        logging.info("Interrupted by user, exiting...")
    except Exception as e:
        logging.error(f"Error reading CAN data: {e}")
    finally:
        bus.shutdown()

def send_to_supabase(supabase: Client, data: dict):
    try:
        # Insert data into Supabase table
        response = supabase.table('can_data').insert(data).execute()
        if response.error:
            raise Exception(response.error)
        logging.info(f"Data sent to Supabase: {response.data}")
    except Exception as e:
        logging.error(f"Failed to send data to Supabase: {e}")
        # Save data to USB if Supabase send fails
        save_to_usb(data)

def save_to_usb(data: dict):
    usb_path = '/path/to/usb_drive/can_data_backup.json'  # Path to save data on USB
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(usb_path), exist_ok=True)

        # Create an empty JSON file if it does not exist
        if not os.path.exists(usb_path):
            with open(usb_path, 'w') as f:
                json.dump([], f)

        # Read existing data from the USB file
        with open(usb_path, 'r') as f:
            existing_data = json.load(f)

        # Append new data to the existing data
        existing_data.append(data)

        # Write updated data back to the USB file
        with open(usb_path, 'w') as f:
            json.dump(existing_data, f, indent=4)

        logging.info(f"Data saved to USB: {usb_path}")
    except Exception as e:
        logging.error(f"Failed to save data to USB: {e}")

if __name__ == "__main__":
    supabase_client = initialize_supabase()
    read_can_data(supabase_client)
