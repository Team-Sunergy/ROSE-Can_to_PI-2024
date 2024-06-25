from can_interface import setup_can_interface, shutdown_can_interface
from bus import initialize_bus
from message_parser import parse_can_message, group_can_data
from tools import getBits, send_request_frame0_periodically, getSpeed
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import queue
from mockDataTransfer import *

# data queue for data
dataQueue = queue.Queue()

# window
mainWin = tk.Tk()
mainWin.title("raspberry pi interface")
mainWin.geometry('800x480')

# configures columns
mainWin.columnconfigure(0, weight=1)
mainWin.columnconfigure(1, weight=1)
mainWin.rowconfigure(0, weight=1)


# configure left window
leftWindow = tk.Frame(mainWin, borderwidth=5, relief='raised')
leftWindow.columnconfigure(0, weight=1)
leftWindow.columnconfigure(1, weight=10)
leftWindow.columnconfigure(2, weight=1)
leftWindow.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)
leftWindow.grid_propagate(False) # makes it so grid doesnt expand based on labels inside

rightWindow = tk.Frame(mainWin, borderwidth=5, relief='raised')
rightWindow.columnconfigure(0, weight=1)
rightWindow.columnconfigure(1, weight=1)
rightWindow.columnconfigure(2, weight=1)
rightWindow.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
rightWindow.grid_propagate(False)

# place widgets
rightWindow.grid(row=0, column=1, sticky='nsew')
leftWindow.grid(row=0, column=0, sticky='nsew')

# place widget in left window
speedCarLabel = ttk.Label(leftWindow, text="SPEED", font=('Helvetica', '10'))
speedCarLabel.grid(row=4, column=1, sticky='s')
speedActual = ttk.Label(leftWindow, text="inf spd", font=("Helvetica", "65", "bold"), borderwidth=2, relief="raised")
speedActual.grid(row=5, column=1, sticky='n')

# right window labels
socLabel = ttk.Label(rightWindow, text=" SOC ", font=("Helvetica", "15"), borderwidth=2, relief='raised')
motorCurrentInLabel = ttk.Label(rightWindow, text=" MOTOR CURRENT IN: ", font=("Helvetica", "15"), borderwidth=2, relief='raised')
motorCurrentOutLabel = ttk.Label(rightWindow, text=" ZACH METER: ", font=("Helvetica", "15"),borderwidth=2, relief='raised')
deltaVoltageLabel = ttk.Label(rightWindow, text=" DELTA VOLTAGE: ", font=("Helvetica", "15"), borderwidth=2, relief='raised')
HappinessStatusLabel = ttk.Label(rightWindow, text=" HAPPINESS STATUS: HAPPY!!!", font=("Helvetica", "15"), borderwidth=2, relief='raised')


socLabel.grid(row=2, column=0)
motorCurrentInLabel.grid(row=3, column=0, sticky='w')
motorCurrentOutLabel.grid(row=4, column=0, sticky='w')
deltaVoltageLabel.grid(row=5, column=0, sticky='w')
HappinessStatusLabel.grid(row=6, column=0, sticky='w')

def startGui(dataQ):
    """starts the gui loop given data"""
    print("Starting gui")
    mainWin.after(100, updateGuiData, dataQ)
    mainWin.mainloop()

def updateGuiData(dataQueue):
    try:
        # non-blocking get from queue
        data = dataQueue.get_nowait()
    except queue.Empty:
        # no new data
        pass
    else:
        # data received, update labels
        update_label(data=data)

    # Schedule next check
    mainWin.after(100, updateGuiData, dataQueue)

        
def update_label(data: dict):
        """private for gui.py, takes data dict
        and updates label"""
        if data['DataType'] != "none":
            # update speed with speed
            speedActual.config(text=str(data['Speed']))
            socLabel.config(text=" SOC" + str(data['SOC']))
            motorCurrentInLabel(text=" MOTOR CURRENT IN: " + str(data['MotorCurrentPeakAverage']))
            motorCurrentOutLabel(text= " ZACH METER: " + str(data['FETTemperature']))
            deltaVoltageLabel(text = " DELTA VOLTAGE: " + str(data['BatteryVoltage']))
        else:
             speedActual.config(text="none")


def main():
    data = None
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
    startGui(dataQ=dataQueue)


    try:
        print("In the try")
        while True:
            message = bus.recv()
            parsed_message = parse_can_message(message) # recieves parsed message
            data = parsed_message['data']
            
            # used for seeing can frames
            print(f"Timestamp: {parsed_message['timestamp']:.6f}")
            print(f"ID: {parsed_message['arbitration_id']:x}")
            print(f"DLC: {parsed_message['dlc']}")
            print(f"Data: {parsed_message['data_str']}")
            print("-" * 30)
            
            # used for sending data, contains all different types of possible categories (mppts, bms, mc)
            # depending on what CAN frame ID is
            canData = group_can_data(data=data) 
            dataQueue.put(canData)           



    except KeyboardInterrupt:
        shutdown_can_interface()
        print("\n\rKeyboard interrupt")

if __name__ == "__main__":
    main()


