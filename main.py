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
from tkinter import *
import customtkinter
import ttkbootstrap as tb
from PIL import Image


from tkinter import Tk, Frame, Label
from tkinter.font import Font
from PIL import Image, ImageTk

# definition of main window
root = Tk()
root.title("GUI for Driver Interface")
root.geometry('800x480')

mainWin = Frame(root, bg='#E5E5E5')
mainWin.pack(fill='both', expand=True)

secondWin = Frame(mainWin, bg='white')
secondWin.place(relx=0.0, rely=0.095, relwidth=1, relheight=0.905)

versionLabel = Label(mainWin, text="version 0.2", font=('Gotham', 10), background="#E5E5E5")
versionLabel.place(relx=0.99, rely=0.015, anchor='ne')

# Fonts
dashFont = Font(family='Gotham', weight='bold', size=30)
socFont = Font(family='Gotham', weight='bold', size=10)
speedFont = Font(family='Gotham', weight='bold', size=200)
errorFont = Font(family='Gotham', size=7)
errorFont2 = Font(family='Gotham', size=8)

speedometerNum = Label(secondWin, text="25", font=speedFont, bg="white")
speedometerNum.place(relx=0.5, rely=0.45, anchor='center')

# define SOC frame (top left)
socFrame = Frame(secondWin, bg='#E5E5E5', relief='raised', borderwidth=1)
socFrame.place(x=5, y=5, width=200, height=100)

socLabel = Label(socFrame, text='STATE OF CHARGE', font=socFont, background='#E5E5E5',)
socLabel.place(relx=0.5, rely=0.01, anchor='n')

socVal = Label(socFrame, text='95.5%', font=dashFont, background='#E5E5E5',)
socVal.place(relx=0.5, rely=0.5, anchor='center')

# define AMPS frame
ampsInFrame = Frame(master=secondWin,
                                  width=200,
                                  height=100,
                                  background='#E5E5E5',
                                  borderwidth=1,
                                  relief='raised',
                                  )
ampsInLabel = Label(master=ampsInFrame,
                                text='AMPERAGE IN',
                                font=socFont,
                                foreground='black',
                                background='#E5E5E5',
                                )
ampsInValue = Label(master=ampsInFrame,
                                     text='3.2AMPS',
                                     font=dashFont,
                                     foreground='black',
                                     background='#E5E5E5',
                                     )
ampsInLabel.place(relx=0.5, rely=0.01, anchor='n')
ampsInValue.place(relx=0.5, rely=0.5, anchor='center')
ampsInFrame.place(x=5,y=428,anchor='sw')



ampsOutFrame = Frame(master=secondWin,
                                  width=200,
                                  height=100,
                                  background='#E5E5E5',
                                  borderwidth=1,
                                  relief='raised',
                                   )
ampsOutLabel = Label(master=ampsOutFrame,
                                text='AMPERAGE OUT',
                                font=socFont,
                                foreground='black',
                                background='#E5E5E5',
                                )
ampsOutValue = Label(master=ampsOutFrame,
                                     text='1.9AMPS',
                                     font=dashFont,
                                     foreground='black',
                                     background='#E5E5E5',
                                     )
ampsOutValue.place(relx=0.5, rely=0.5, anchor='center')
ampsOutLabel.place(relx=0.5, rely=0.01, anchor='n')
ampsOutFrame.place(x=795,y=428,anchor='se')

ampsDiffFrame = Frame(master=secondWin,
                                    width=300,
                                    height=75,
                                    background='#E5E5E5',
                                    borderwidth=1,
                                    relief='raised',
                                    )
ampsDiffValue = Label(master=ampsDiffFrame,
                                     text='1.3A',
                                     font=Font(family='Gotham', weight='bold', size=25),
                                     foreground='black',
                                     background='#E5E5E5',
                                     )
ampsDiffLabel = Label(master=ampsDiffFrame,
                                     text='AMP IN/AMP OUT',
                                     font=socFont,
                                     foreground='black',
                                     background='#E5E5E5',
                                    )
ampsDiffValue.place(relx=0.5, rely=0.53, anchor='center')
ampsDiffLabel.place(relx=0.5, rely=0.02,anchor='n')
ampsDiffFrame.place(x=400,y=428,anchor='s')


# BELOW ARE ALL THE ANNOYING ERROR FRAME DIAGNOSTICS
errorFrame = Frame(master=secondWin,
                                  width=200,
                                  height=175,
                                  background='#E5E5E5',
                                  borderwidth=1,
                                  relief='raised'
                                  )
errorFrameLabel = Label(master=errorFrame,
                                         text="MPPTS Status",
                                         font=errorFont2,
                                         foreground='black',
                                         background='#E5E5E5',
                                         )
mpptsErrorLabel = Label(master=errorFrame,
                                    text="mppt0 mppt1",
                                    font=errorFont2,
                                    background='#E5E5E5',
                                    foreground='black')


mpptHWOverCurrentLabel = Label(master=errorFrame,
                                                 text="mpptHWOverCurrent:",
                                                 font=errorFont,
                                                 foreground='black',
                                                 background='#E5E5E5',
                                                 anchor='w',)
mppt0HWOverCurrent = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)
mppt1HWOverCurrent = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)

mpptHWOverVoltageLabel = Label(master=errorFrame,
                                                 text="mpptHWOverVoltage:",
                                                 font=errorFont,
                                                 foreground='black',
                                                 background='#E5E5E5',
                                                 anchor='w')
mppt0HWOverVoltage = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)
mppt1HWOverVoltage = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)

mppt12VUnderVoltageLabel = Label(master=errorFrame,
                                                   text="mppt12VUnderVoltage:",
                                                   font=errorFont,
                                                   foreground='black',
                                                   background='#E5E5E5',
                                                   anchor='w')
mppt012VUnderVoltage = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)
mppt112VUnderVoltage = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)

mpptBatteryFullLabel = Label(master=errorFrame,
                                               text="mpptBatteryFull:",
                                               font=errorFont,
                                               foreground='black',
                                               background='#E5E5E5',
                                               anchor='w')
mppt0BatteryFull = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)
mppt1BatteryFull = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)

mpptBatteryLowLabel = Label(master=errorFrame,
                                              text="mpptBatteryLow:",
                                              font=errorFont,
                                              foreground='black',
                                              background='#E5E5E5',
                                              anchor='w')
mppt0BatteryLow = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)
mppt1BatteryLow = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)

mpptMosfetOverheatLabel = Label(master=errorFrame,
                                                  text="mpptMosfetOverheat:",
                                                  font=errorFont,
                                                  foreground='black',
                                                  background='#E5E5E5',
                                                  anchor='w')
mppt0MosfetOverheat = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)
mppt1MosfetOverheat = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)

mpptLowArrayPowerLabel = Label(master=errorFrame,
                                         text="mpptLowArrayPower:",
                                         font=errorFont,
                                         foreground='black',
                                         background='#E5E5E5',
                                         anchor='w')
mppt0LowArrayPower = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)
mppt1LowArrayPower = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)


# placing error labels
errorFrameLabel.place(relx=0.03, rely=0.006, anchor='nw')
mpptsErrorLabel.place(relx=0.59, rely=0.006, anchor='nw')

mpptLowArrayPowerLabel.place(relx=0.03, rely=0.22, anchor='w')
mppt0LowArrayPower.place(relx=0.6, rely=0.22, anchor='w')
mppt1LowArrayPower.place(relx=0.8, rely=0.22, anchor='w')

mpptMosfetOverheatLabel.place(relx=0.03, rely=0.34, anchor='w')
mppt0MosfetOverheat.place(relx=0.6, rely=0.34, anchor='w')
mppt1MosfetOverheat.place(relx=0.8, rely=0.34, anchor='w')

mpptBatteryLowLabel.place(relx=0.03, rely=0.4532, anchor='w')
mppt0BatteryLow.place(relx=0.6, rely=0.4532, anchor='w')
mppt1BatteryLow.place(relx=0.8, rely=0.4532, anchor='w')

mpptBatteryFullLabel.place(relx=0.03, rely=0.5648, anchor='w')
mppt0BatteryFull.place(relx=0.6, rely=0.5648, anchor='w')
mppt1BatteryFull.place(relx=0.8, rely=0.5648, anchor='w')

mppt12VUnderVoltageLabel.place(relx=0.03, rely=0.6864, anchor='w')
mppt012VUnderVoltage.place(relx=0.6, rely=0.6864, anchor='w')
mppt112VUnderVoltage.place(relx=0.8, rely=0.6864, anchor='w')

mpptHWOverVoltageLabel.place(relx=0.03, rely=0.798, anchor='w')
mppt0HWOverVoltage.place(relx=0.6, rely=0.798, anchor='w')
mppt1HWOverVoltage.place(relx=0.8, rely=0.798, anchor='w')

mpptHWOverCurrentLabel.place(relx=0.03, rely=0.90, anchor='w')
mppt0HWOverCurrent.place(relx=0.6, rely= 0.90, anchor='w')
mppt1HWOverCurrent.place(relx=0.8, rely=0.90, anchor='w')



# place on frame
errorFrame.place(x=795,y=5,anchor='ne')


img = Image.open('Logo.png')
img = img.resize((84, 37))
sunergyLogo = ImageTk.PhotoImage(img)
logoLabel = Label(mainWin, image=sunergyLogo, background='#E5E5E5')
logoLabel.image = sunergyLogo  
logoLabel.place(x=400, y=0, anchor='n')

def startGui():
    """starts the gui loop given data"""
    print("Starting gui")
    root.mainloop()

def updateGuiData(dataQueue):
    """updates gui via a queue system"""
    try:
        # non-blocking get from queue
        data = dataQueue.get_nowait()
    except queue.Empty:
        print("no new data")
        pass
    else:
        # data received, update labels
        update_label(data=data)
    # schedule next update
    mainWin.after(100, updateGuiData, dataQueue)

        
def update_label(data: dict):
        """private for gui.py, takes data dict
        and updates label"""
        print("updating label")
        if data['DataType'] != 'none':
            # update speed with speed
            speedometerNum.config(amountused=f"{data['Speed']:.1f}")
            socVal.config(text=f"{data['SOC']:.1f}")
            ampsInValue.config(text=f"{data['OutputCurrent0'] + data['OutputCurrent1']:.1f}")
            ampsOutValue.config(text=f"{data['OutputCurrent0'] + data['OutputCurrent1']:.1f}")
            ampsDiffValue.config(text="idk")
        else:
            pass


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
        
        print(f"Timestamp: {parsed_message['timestamp']:.6f}")
        print(f"ID: {parsed_message['arbitration_id']:x}")
        print(f"DLC: {parsed_message['dlc']}")
        print(f"Data: {parsed_message['data_str']}")
        print("-" * 30)
        print("SOC: " + str(groupedData['SOC']))

        
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
    root.after(100, updateGuiData, dataQueue)
    startGui()

if __name__ == "__main__":
    main()


