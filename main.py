from can_interface import setup_can_interface, shutdown_can_interface
from bus import initialize_bus
from message_parser import parse_can_message, group_can_data
from tools import getBits, send_request_frame0_periodically, getSpeed
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import queue
import threading
from mockDataTransfer import *

        
def worker_thread(queue, bus):
    """A worker thread that generates canData and puts it on the queue."""
    print("Running worker thread.")
    while True:
        data = canCollection(bus)
        queue.put(data) # puts data in queue
        time.sleep(0.1)  # controls the rate of data generation.

def canCollection(bus):
    print("In the try")
    try:
        message = bus.recv()
        parsed_message = parse_can_message(message) # recieves parsed message
        data = parsed_message['data']
        # group up data into a table
        groupedData = group_can_data(parsed_message['arbitration_id'], data=data)
        # used for seeing can frames
        
        if groupedData["DataType"] == 'mppt1error' or groupedData['DataType'] == 'mppt0error':
            print(groupedData["DataType"])
            print("LowArrayPower: " + str(groupedData['LowArrayPower']))
            print("MosfetOverheat: " + str(groupedData['MosfetOverheat']))
            print("BatteryLow: "+ str(groupedData['BatteryLow']))
            print("BatteryFull: " + str(groupedData['BatteryFull']))
            print("12VUnderVoltage: " + str(groupedData['12VUnderVoltage']))
            print("HWOvercurrent: " + str(groupedData['HWOvercurrent']))
            print("HWOvervoltage: " + str(groupedData['HWOvervoltage']))

        print(f"Timestamp: {parsed_message['timestamp']:.6f}")
        print(f"ID: {parsed_message['arbitration_id']:x}")
        print(f"DLC: {parsed_message['dlc']}")
        print(f"Data: {parsed_message['data_str']}")
        print("-" * 30)
        print("STATE OF CHARGE: " + str(groupedData['SOC']))

        
        # used for sending data, contains all different types of possible categories (mppts, bms, mc)
        # depending on what CAN frame ID is
        return groupedData
    
    except KeyboardInterrupt:
        shutdown_can_interface()
        print("\n\rKeyboard interrupt")

# data queue for data
dataQueue = queue.Queue()

def main():
    """
    Main function to set up the CAN interface, initialize the bus, and continuously
    receive and parse CAN messages until interrupted by user.
    """
    setup_can_interface()
    print("The setup_can_interface done")
    bus = initialize_bus()
    print("Bus variable is set")
    # this is for motor controllers
    send_request_frame0_periodically(bus=bus)
    print("Sending request frame0 in main...")
    worker = threading.Thread(target=worker_thread, args=(dataQueue, bus))
    worker.start()
    #mainWin.after(100, updateGuiData, dataQueue)
    #startGui()

if __name__ == "__main__":
    main()


